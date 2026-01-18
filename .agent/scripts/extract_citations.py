"""
Extract Citations Tool.

Extracts parent citations from a DDR tag's :links: directive.

Meta
----
Tool Definition : .agent/tools/tag_extract_citations.md
Knowledge Source: .agent/knowledge/sources/constraints/tag_citation_required.md
Architect       : Antigravity IDE

Usage
-----
    python extract_citations.py --id FSD-001
    python extract_citations.py --id FSD-001 --needs-json path/to/needs.json

Exit Codes
----------
0 : Success (JSON result printed to stdout)
1 : Error (Details printed to stderr)
"""

import argparse
import json
import sys
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

    Raises
    ------
    FileNotFoundError
        If needs.json does not exist.
    ValueError
        If needs.json cannot be parsed.
    """
    if not needs_path.exists():
        raise FileNotFoundError(f"Needs file not found: {needs_path}")

    with open(needs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract needs from version structure
    versions = data.get("versions", {})
    for version_data in versions.values():
        needs = version_data.get("needs", {})
        if needs:
            return needs

    raise ValueError("No needs found in needs.json")


def get_tier_from_id(tag_id: str) -> Optional[str]:
    """
    Extract tier code from tag ID.

    Parameters
    ----------
    tag_id : str
        Tag ID (e.g., FSD-001).

    Returns
    -------
    str or None
        Tier code if valid, None otherwise.
    """
    parts = tag_id.split("-")
    if len(parts) >= 1:
        tier = parts[0].upper()
        if tier in VALID_TIERS:
            return tier
    return None


def extract_citations(tag_id: str, needs: dict) -> dict:
    """
    Extract parent citations from a tag.

    Parameters
    ----------
    tag_id : str
        The tag ID to analyze.
    needs : dict
        Dictionary of all needs.

    Returns
    -------
    dict
        Extraction result with parents, validation status.
    """
    tag_id = tag_id.strip()

    if tag_id not in needs:
        return {
            "success": False,
            "id": tag_id,
            "error": f"Tag not found: {tag_id}",
            "parents": [],
            "orphan": True
        }

    need = needs[tag_id]
    tier = get_tier_from_id(tag_id)

    # Get links (parent citations)
    links = need.get("links", [])
    if isinstance(links, str):
        links = [links] if links else []

    # Analyze each parent
    parents = []
    missing_parents = []
    for parent_id in links:
        parent_tier = get_tier_from_id(parent_id)
        exists = parent_id in needs

        parent_info = {
            "id": parent_id,
            "tier": parent_tier,
            "exists": exists
        }

        if exists:
            parent_need = needs[parent_id]
            parent_info["title"] = parent_need.get("title", "")
        else:
            missing_parents.append(parent_id)

        parents.append(parent_info)

    # Determine orphan status
    # BRD tags are not orphans (they are root)
    # Other tiers are orphans if they have no valid parents
    is_orphan = False
    if tier != "BRD":
        valid_parents = [p for p in parents if p["exists"]]
        is_orphan = len(valid_parents) == 0

    return {
        "success": True,
        "id": tag_id,
        "tier": tier,
        "title": need.get("title", ""),
        "parents": parents,
        "parent_count": len(parents),
        "missing_parents": missing_parents,
        "orphan": is_orphan,
        "orphan_reason": (
            "No valid parent citations" if is_orphan and tier != "BRD"
            else None
        )
    }


def main() -> int:
    """
    CLI entry point for extract_citations.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Extract parent citations from a DDR tag."
    )
    parser.add_argument(
        "--id",
        required=True,
        help="Tag ID to extract citations from (e.g., FSD-001)"
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
        needs = load_needs(needs_path)

        result = extract_citations(args.id, needs)

        print(json.dumps(result, indent=2))
        return 0 if result["success"] else 1

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error parsing needs.json: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error extracting citations: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
