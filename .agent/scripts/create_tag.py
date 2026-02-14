"""
Create Tag Tool.

Generates a new DDR tag with proper ID format, tier validation, and parent citation.
Enforces sequential integer IDs (e.g., FSD-12) based on existing needs.

Meta
----
Tool Definition : .agent/tools/tag_create.md
Knowledge Source: .agent/knowledge/sources/patterns/tag_syntax.md
                  .agent/knowledge/sources/constraints/tag_immutability.md
                  .agent/knowledge/sources/constraints/tag_citation_required.md
Architect       : Antigravity IDE
"""

import argparse
import json
import sys
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
TIER_HIERARCHY: dict[str, list[str]] = {
    "BRD": [],           # BRD has no parent requirement (root authority)
    "NFR": ["BRD"],      # NFR ← BRD
    "FSD": ["BRD", "NFR"],  # FSD ← BRD, NFR
    "SAD": ["FSD", "NFR"],  # SAD ← FSD, NFR
    "ICD": ["SAD", "NFR"],  # ICD ← SAD, NFR
    "TDD": ["SAD", "ICD"],  # TDD ← SAD, ICD
    "ISP": ["TDD"]       # ISP ← TDD
}


def get_next_sequential_id(tier: str, needs: dict) -> str:
    """
    Calculate the next sequential ID for a given tier.
    Example: If FSD-10 exists, returns FSD-11.
    """
    max_id = 0
    prefix = f"{tier}-"

    for need_id in needs.keys():
        if need_id.upper().startswith(prefix):
            try:
                # Extract number part (e.g., FSD-10 -> 10)
                # Handle cases like FSD-10.1 (atomic) by taking the first part
                suffix = need_id[len(prefix):]
                number_part = suffix.split('.')[0]
                num = int(number_part)
                if num > max_id:
                    max_id = num
            except ValueError:
                continue

    return f"{tier}-{max_id + 1}"


def validate_parent_tier(child_tier: str, parent_id: str) -> tuple[bool, str]:
    """
    Validate that parent tier is appropriate for child tier.
    """
    if not parent_id:
        if child_tier in REQUIRES_PARENT:
            return False, f"{child_tier} tags require a parent citation"
        return True, "BRD tags do not require parent"

    parts = parent_id.split("-")
    if len(parts) < 2:
        return False, f"Invalid parent ID format: {parent_id}"

    parent_tier = parts[0].upper()
    if parent_tier not in VALID_TIERS:
        return False, f"Unknown parent tier: {parent_tier}"

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
    Returns empty dict ONLY if file missing, not on error.
    """
    if not needs_path.exists():
        return {}

    try:
        with open(needs_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        versions = data.get("versions", {})
        for version_data in versions.values():
            needs = version_data.get("needs", {})
            if needs:
                return needs
        return {}
    except Exception:
        # Rethrow to fail closed if file exists but is corrupt
        raise


def check_id_collision(tag_id: str, needs: dict) -> bool:
    """Check if tag ID already exists."""
    return tag_id in needs


def create_tag(
    tier: str,
    title: str,
    parent: Optional[str] = None,
    description: str = "",
    needs_path: Optional[Path] = None
) -> dict:
    """Create a new DDR tag."""
    tier = tier.upper().strip()

    if tier not in VALID_TIERS:
        raise ValueError(f"Invalid tier: {tier}. Valid: {list(VALID_TIERS.keys())}")

    valid, message = validate_parent_tier(tier, parent)
    if not valid:
        raise ValueError(message)

    # Load existing needs
    needs = {}
    if needs_path:
        needs = load_existing_needs(needs_path)

    # Generate next sequential ID
    tag_id = get_next_sequential_id(tier, needs)

    # Double check collision just in case
    if check_id_collision(tag_id, needs):
        raise RuntimeError(f"Generated ID {tag_id} already exists (race condition?)")

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
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a new DDR tag with proper ID and format."
    )
    parser.add_argument("--tier", required=True, help="DDR tier code")
    parser.add_argument("--title", required=True, help="Tag title")
    parser.add_argument("--parent", required=False, default=None, help="Parent tag ID")
    parser.add_argument("--description", required=False, default="", help="Tag description")
    parser.add_argument(
        "--needs-json",
        required=False,
        default="docs/_build/json/needs.json",
        help="Path to needs.json"
    )
    parser.add_argument("--json-only", action="store_true", help="Output JSON only")

    args = parser.parse_args()

    try:
        needs_path = Path(args.needs_json) if args.needs_json else None

        # FAIL CLOSED: If needs.json path is provided but file doesn't exist
        # We must assume the user intends to use it.
        # However, for first run, it might not exist.
        # But per requirements, we must enforce valid needs.json for sequential IDs.
        if needs_path and not needs_path.exists():
             print(f"Error: needs.json not found at {needs_path}. Build docs first.", file=sys.stderr)
             return 1

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
            print(result["rst_directive"])
            print()
            print("---")
            print(f"# Tag ID: {result['tag_id']}")
            print(f"# Tier: {result['tier_name']}")
            print("# Reminder: Rebuild docs (make json) to update the index before generating the next tag.")
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
