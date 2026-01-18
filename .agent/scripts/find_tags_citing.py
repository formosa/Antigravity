"""
Find Tags Citing Tool.

Finds all DDR tags that cite a given parent tag for downstream impact analysis.

Meta
----
Tool Definition : .agent/tools/tag_find_citing.md
Knowledge Source: .agent/knowledge/sources/protocols/impact_analysis.md
Architect       : Antigravity IDE

Usage
-----
    python find_tags_citing.py --id BRD-001
    python find_tags_citing.py --id BRD-001 --needs-json path/to/needs.json

Exit Codes
----------
0 : Success (JSON result printed to stdout)
1 : Error (Details printed to stderr)
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional


# Valid DDR tiers in hierarchy order
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


def find_tags_citing(target_id: str, needs: dict, recursive: bool = False) -> dict:
    """
    Find all tags that cite the target as a parent.

    Parameters
    ----------
    target_id : str
        The tag ID to find citations for.
    needs : dict
        Dictionary of all needs.
    recursive : bool
        If True, also find indirect descendants.

    Returns
    -------
    dict
        Result with citing tags grouped by tier.
    """
    target_id = target_id.strip()

    # Check if target exists
    target_exists = target_id in needs
    target_tier = get_tier_from_id(target_id)
    target_title = ""
    if target_exists:
        target_title = needs[target_id].get("title", "")

    # Find direct citations
    direct_citations = []
    for need_id, need_data in needs.items():
        links = need_data.get("links", [])
        if isinstance(links, str):
            links = [links] if links else []

        if target_id in links:
            citation = {
                "id": need_id,
                "tier": get_tier_from_id(need_id),
                "title": need_data.get("title", ""),
                "link_type": "direct"
            }
            direct_citations.append(citation)

    # Group by tier
    by_tier = defaultdict(list)
    for citation in direct_citations:
        tier = citation["tier"] or "UNKNOWN"
        by_tier[tier].append({
            "id": citation["id"],
            "title": citation["title"]
        })

    # Sort tiers by hierarchy
    sorted_by_tier = {}
    for tier in VALID_TIERS:
        if tier in by_tier:
            sorted_by_tier[tier] = by_tier[tier]
    # Add unknown tier if present
    if "UNKNOWN" in by_tier:
        sorted_by_tier["UNKNOWN"] = by_tier["UNKNOWN"]

    # Recursive descent if requested
    all_descendants = []
    if recursive and direct_citations:
        visited = {target_id}
        queue = [c["id"] for c in direct_citations]

        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            # Find citations of this tag
            for need_id, need_data in needs.items():
                if need_id in visited:
                    continue
                links = need_data.get("links", [])
                if isinstance(links, str):
                    links = [links] if links else []
                if current_id in links:
                    all_descendants.append({
                        "id": need_id,
                        "tier": get_tier_from_id(need_id),
                        "title": need_data.get("title", ""),
                        "parent": current_id
                    })
                    queue.append(need_id)

    result = {
        "success": True,
        "target_id": target_id,
        "target_tier": target_tier,
        "target_title": target_title,
        "target_exists": target_exists,
        "cited_by": direct_citations,
        "cited_by_tier": sorted_by_tier,
        "count": len(direct_citations),
        "impact_summary": (
            f"Modifying {target_id} may affect {len(direct_citations)} direct dependents"
        )
    }

    if recursive:
        result["all_descendants"] = all_descendants
        result["total_impact"] = len(direct_citations) + len(all_descendants)

    return result


def main() -> int:
    """
    CLI entry point for find_tags_citing.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Find all DDR tags that cite a given parent tag."
    )
    parser.add_argument(
        "--id",
        required=True,
        help="Tag ID to find citations for (e.g., BRD-001)"
    )
    parser.add_argument(
        "--needs-json",
        required=False,
        default="docs/_build/json/needs.json",
        help="Path to needs.json file"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include indirect descendants (transitive closure)"
    )

    args = parser.parse_args()

    try:
        needs_path = Path(args.needs_json)
        needs = load_needs(needs_path)

        result = find_tags_citing(
            target_id=args.id,
            needs=needs,
            recursive=args.recursive
        )

        print(json.dumps(result, indent=2))
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error parsing needs.json: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error finding citations: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
