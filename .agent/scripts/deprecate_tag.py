"""
Deprecate Tag Tool.

Marks a DDR tag as deprecated and optionally specifies a replacement.

Meta
----
Tool Definition : .agent/tools/tag_deprecate.md
Knowledge Source: .agent/knowledge/sources/constraints/tag_immutability.md
Architect       : Antigravity IDE

Usage
-----
    python deprecate_tag.py --id FSD-001
    python deprecate_tag.py --id FSD-001 --replacement FSD-002

Exit Codes
----------
0 : Success (JSON result printed to stdout)
1 : Error (Details printed to stderr)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Valid DDR tiers
VALID_TIERS = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]


def load_needs(needs_path: Path) -> dict:
    """
    Load all needs from needs.json.

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
        raise FileNotFoundError(f"Needs file not found: {needs_path}")

    with open(needs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    versions = data.get("versions", {})
    for version_data in versions.values():
        needs = version_data.get("needs", {})
        if needs:
            return needs

    raise ValueError("No needs found in needs.json")


def get_tier_from_id(tag_id: str) -> Optional[str]:
    """Extract tier code from tag ID."""
    parts = tag_id.split("-")
    if len(parts) >= 1:
        tier = parts[0].upper()
        if tier in VALID_TIERS:
            return tier
    return None


def find_downstream_dependents(target_id: str, needs: dict) -> list[dict]:
    """
    Find all tags that directly cite the target.

    Parameters
    ----------
    target_id : str
        The tag ID being deprecated.
    needs : dict
        Dictionary of all needs.

    Returns
    -------
    list[dict]
        List of dependent tags.
    """
    dependents = []
    for need_id, need_data in needs.items():
        links = need_data.get("links", [])
        if isinstance(links, str):
            links = [links] if links else []

        if target_id in links:
            dependents.append({
                "id": need_id,
                "tier": get_tier_from_id(need_id),
                "title": need_data.get("title", ""),
                "file": need_data.get("docname", "")
            })

    return dependents


def deprecate_tag(
    tag_id: str,
    replacement: Optional[str],
    needs_path: Path
) -> dict:
    """
    Prepare deprecation for a DDR tag.

    Note: This tool generates deprecation specification but does not
    modify files directly. The agent must apply changes to RST files.

    Parameters
    ----------
    tag_id : str
        The tag ID to deprecate.
    replacement : str, optional
        Replacement tag ID if available.
    needs_path : Path
        Path to needs.json.

    Returns
    -------
    dict
        Deprecation result with migration info.
    """
    tag_id = tag_id.strip()

    # Load needs
    needs = load_needs(needs_path)

    # Check tag exists
    if tag_id not in needs:
        raise ValueError(f"Tag not found: {tag_id}")

    need = needs[tag_id]
    tier = get_tier_from_id(tag_id)

    # Validate replacement if provided
    replacement_valid = True
    replacement_info = None
    if replacement:
        replacement = replacement.strip()
        if replacement not in needs:
            replacement_valid = False
            replacement_info = {
                "id": replacement,
                "exists": False,
                "warning": "Replacement tag does not exist yet"
            }
        else:
            replacement_need = needs[replacement]
            replacement_tier = get_tier_from_id(replacement)
            if replacement_tier != tier:
                replacement_valid = False
                replacement_info = {
                    "id": replacement,
                    "exists": True,
                    "tier": replacement_tier,
                    "warning": f"Replacement tier ({replacement_tier}) differs from deprecated tier ({tier})"
                }
            else:
                replacement_info = {
                    "id": replacement,
                    "exists": True,
                    "tier": replacement_tier,
                    "title": replacement_need.get("title", "")
                }

    # Find dependents that need migration
    dependents = find_downstream_dependents(tag_id, needs)

    # Generate deprecation notice
    deprecation_notice = f"DEPRECATED: This tag is deprecated as of {datetime.now().strftime('%Y-%m-%d')}."
    if replacement:
        deprecation_notice += f" Use {replacement} instead."

    # Build result
    result = {
        "success": True,
        "deprecation": {
            "tag_id": tag_id,
            "tier": tier,
            "title": need.get("title", ""),
            "deprecated_at": datetime.now().isoformat(),
            "replacement": replacement,
            "replacement_valid": replacement_valid,
            "replacement_info": replacement_info
        },
        "source_file": need.get("docname", "") + ".rst",
        "line_number": need.get("lineno"),
        "deprecation_notice": deprecation_notice,
        "affected_children": dependents,
        "affected_count": len(dependents),
        "instructions": [
            f"1. Open {need.get('docname', '')}.rst",
            f"2. Locate tag {tag_id} at line {need.get('lineno', 'unknown')}",
            f"3. Add :status: deprecated to the directive",
            f"4. Add deprecation notice to content: '{deprecation_notice}'"
        ]
    }

    if dependents:
        result["migration_required"] = True
        result["migration_instructions"] = [
            "5. Update dependent tags to reference replacement:",
            *[f"   - {d['id']}: Change :links: {tag_id} to :links: {replacement or 'NEW_TAG'}"
              for d in dependents[:5]],
            *(["   - ...and more"] if len(dependents) > 5 else [])
        ]

    # Generate RST modification example
    result["rst_modification"] = f"""
.. {tier.lower()}:: {need.get('title', '')}
   :id: {tag_id}
   :status: deprecated

   .. warning::
      {deprecation_notice}

   [Original content preserved below...]
"""

    return result


def main() -> int:
    """
    CLI entry point for deprecate_tag.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Mark a DDR tag as deprecated with optional replacement."
    )
    parser.add_argument(
        "--id",
        required=True,
        help="Tag ID to deprecate (e.g., FSD-001)"
    )
    parser.add_argument(
        "--replacement",
        required=False,
        default=None,
        help="Replacement tag ID (optional)"
    )
    parser.add_argument(
        "--needs-json",
        required=False,
        default="docs/_build/json/needs.json",
        help="Path to needs.json file"
    )

    args = parser.parse_args()

    try:
        needs_path = Path(args.needs_json)

        result = deprecate_tag(
            tag_id=args.id,
            replacement=args.replacement,
            needs_path=needs_path
        )

        print(json.dumps(result, indent=2))
        return 0

    except ValueError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error deprecating tag: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
