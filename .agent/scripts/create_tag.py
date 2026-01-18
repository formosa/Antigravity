"""
Create Tag Tool.

Generates a new DDR tag with proper ID format, tier validation, and parent citation.

Meta
----
Tool Definition : .agent/tools/tag_create.md
Knowledge Source: .agent/knowledge/sources/patterns/tag_syntax.md
                  .agent/knowledge/sources/constraints/tag_immutability.md
                  .agent/knowledge/sources/constraints/tag_citation_required.md
Architect       : Antigravity IDE

Usage
-----
    python create_tag.py --tier BRD --title "Project Purpose"
    python create_tag.py --tier FSD --title "User Login" --parent BRD-001

Exit Codes
----------
0 : Success (RST directive printed to stdout)
1 : Error (Details printed to stderr)
"""

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Optional

# Valid DDR tiers and their full names
VALID_TIERS = {
    "BRD": "Business Requirements Document",
    "NFR": "Non-Functional Requirements",
    "FSD": "Feature Specification Document",
    "SAD": "System Architecture Document",
    "ICD": "Interface Contract Document",
    "TDD": "Technical Design Document",
    "ISP": "Implementation Stub Prototype"
}

# Tiers that require parent citation (all except BRD)
REQUIRES_PARENT = ["NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]

# Tier hierarchy for parent validation
# Source: .agent/knowledge/sources/concepts/tier_hierarchy.md §Validation Hierarchy
TIER_HIERARCHY: dict[str, list[str]] = {
    "BRD": [],           # BRD has no parent requirement (root authority)
    "NFR": ["BRD"],      # NFR ← BRD
    "FSD": ["BRD", "NFR"],  # FSD ← BRD, NFR
    "SAD": ["FSD"],      # SAD ← FSD
    "ICD": ["SAD", "NFR"],  # ICD ← SAD, NFR
    "TDD": ["SAD", "ICD"],  # TDD ← SAD, ICD
    "ISP": ["TDD"]       # ISP ← TDD
}


def generate_short_uuid() -> str:
    """
    Generate a short UUID for tag IDs.

    Returns
    -------
    str
        8-character hexadecimal string from UUID4.
    """
    return str(uuid.uuid4())[:8]


def validate_parent_tier(child_tier: str, parent_id: str) -> tuple[bool, str]:
    """
    Validate that parent tier is appropriate for child tier.

    Parameters
    ----------
    child_tier : str
        The tier of the tag being created.
    parent_id : str
        The ID of the parent tag (e.g., BRD-001).

    Returns
    -------
    tuple[bool, str]
        (is_valid, message)
    """
    if not parent_id:
        if child_tier in REQUIRES_PARENT:
            return False, f"{child_tier} tags require a parent citation"
        return True, "BRD tags do not require parent"

    # Extract parent tier from ID
    parts = parent_id.split("-")
    if len(parts) < 2:
        return False, f"Invalid parent ID format: {parent_id}"

    parent_tier = parts[0].upper()
    if parent_tier not in VALID_TIERS:
        return False, f"Unknown parent tier: {parent_tier}"

    # Check hierarchy
    allowed = TIER_HIERARCHY.get(child_tier, [])
    if parent_tier not in allowed and child_tier != "BRD":
        return False, (
            f"{child_tier} should cite from tiers {allowed}, "
            f"not {parent_tier}"
        )

    return True, f"Valid parent: {parent_tier} → {child_tier}"


def load_existing_needs(needs_path: Path) -> dict:
    """
    Load existing needs from needs.json if available.

    Parameters
    ----------
    needs_path : Path
        Path to needs.json file.

    Returns
    -------
    dict
        Dictionary of need_id -> need_data.
    """
    if not needs_path.exists():
        return {}

    try:
        with open(needs_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract needs from version structure
        versions = data.get("versions", {})
        for version_data in versions.values():
            needs = version_data.get("needs", {})
            if needs:
                return needs
        return {}
    except Exception:
        return {}


def check_id_collision(tag_id: str, needs: dict) -> bool:
    """
    Check if tag ID already exists.

    Parameters
    ----------
    tag_id : str
        The proposed tag ID.
    needs : dict
        Existing needs dictionary.

    Returns
    -------
    bool
        True if ID already exists (collision).
    """
    return tag_id in needs


def create_tag(
    tier: str,
    title: str,
    parent: Optional[str] = None,
    description: str = "",
    needs_path: Optional[Path] = None
) -> dict:
    """
    Create a new DDR tag.

    Parameters
    ----------
    tier : str
        The DDR tier code.
    title : str
        Human-readable title for the tag.
    parent : str, optional
        Parent tag ID for :links: directive.
    description : str, optional
        Tag description/content.
    needs_path : Path, optional
        Path to needs.json for collision detection.

    Returns
    -------
    dict
        Tag creation result with ID, RST directive, and metadata.
    """
    tier = tier.upper().strip()

    if tier not in VALID_TIERS:
        raise ValueError(f"Invalid tier: {tier}. Valid: {list(VALID_TIERS.keys())}")

    # Validate parent
    valid, message = validate_parent_tier(tier, parent)
    if not valid:
        raise ValueError(message)

    # Load existing needs for collision detection
    needs = {}
    if needs_path:
        needs = load_existing_needs(needs_path)

    # Generate unique ID with collision check
    max_attempts = 10
    for _ in range(max_attempts):
        short_id = generate_short_uuid()
        tag_id = f"{tier}-{short_id}"
        if not check_id_collision(tag_id, needs):
            break
    else:
        raise RuntimeError("Failed to generate unique ID after max attempts")

    # Build RST directive
    directive_type = tier.lower()
    rst_lines = [
        f".. {directive_type}:: {title}",
        f"   :id: {tag_id}"
    ]

    if parent:
        rst_lines.append(f"   :links: {parent}")

    if description:
        rst_lines.append("")
        for line in description.split("\n"):
            rst_lines.append(f"   {line}")

    rst_directive = "\n".join(rst_lines)

    return {
        "success": True,
        "tag_id": tag_id,
        "tier": tier,
        "tier_name": VALID_TIERS[tier],
        "title": title,
        "parent": parent,
        "rst_directive": rst_directive,
        "validation": message
    }


def main() -> int:
    """
    CLI entry point for create_tag.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Generate a new DDR tag with proper ID and format."
    )
    parser.add_argument(
        "--tier",
        required=True,
        help=f"DDR tier code. Valid values: {', '.join(VALID_TIERS.keys())}"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Human-readable tag title"
    )
    parser.add_argument(
        "--parent",
        required=False,
        default=None,
        help="Parent tag ID for :links: directive (required for non-BRD tiers)"
    )
    parser.add_argument(
        "--description",
        required=False,
        default="",
        help="Optional description content for the tag"
    )
    parser.add_argument(
        "--needs-json",
        required=False,
        default="docs/_build/json/needs.json",
        help="Path to needs.json for collision detection"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output only JSON metadata (no RST)"
    )

    args = parser.parse_args()

    try:
        needs_path = Path(args.needs_json) if args.needs_json else None

        result = create_tag(
            tier=args.tier,
            title=args.title,
            parent=args.parent,
            description=args.description,
            needs_path=needs_path
        )

        if args.json_only:
            print(json.dumps(result, indent=2))
        else:
            # Print RST directive followed by metadata
            print(result["rst_directive"])
            print()
            print("---")
            print(f"# Tag ID: {result['tag_id']}")
            print(f"# Tier: {result['tier_name']}")
            if result['parent']:
                print(f"# Parent: {result['parent']}")

        return 0

    except ValueError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error creating tag: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
