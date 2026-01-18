"""
Update Tag Tool.

Updates an existing DDR tag and marks affected children for reconciliation.

Meta
----
Tool Definition : .agent/tools/tag_update.md
Knowledge Source: .agent/knowledge/sources/protocols/reconciliation_dirty_flag.md
Architect       : Antigravity IDE

Usage
-----
    python update_tag.py --id FSD-001 --field title --value "New Title"
    python update_tag.py --id FSD-001 --field description --value "Updated content"

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

# Fields that can be updated
UPDATEABLE_FIELDS = ["title", "description", "status", "content"]

# Fields that trigger downstream reconciliation
RECONCILIATION_TRIGGERS = ["title", "description", "content"]


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
        The tag ID being updated.
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


def generate_update_diff(
    tag_id: str,
    field: str,
    old_value: str,
    new_value: str,
    dependents: list[dict]
) -> dict:
    """
    Generate a diff showing the proposed update.

    Parameters
    ----------
    tag_id : str
        The tag being updated.
    field : str
        The field being updated.
    old_value : str
        Current value.
    new_value : str
        New value.
    dependents : list[dict]
        Tags that will need reconciliation.

    Returns
    -------
    dict
        Update specification.
    """
    requires_reconciliation = field in RECONCILIATION_TRIGGERS and len(dependents) > 0

    return {
        "tag_id": tag_id,
        "tier": get_tier_from_id(tag_id),
        "field": field,
        "old_value": old_value if len(old_value) < 200 else f"{old_value[:200]}...",
        "new_value": new_value if len(new_value) < 200 else f"{new_value[:200]}...",
        "timestamp": datetime.now().isoformat(),
        "requires_reconciliation": requires_reconciliation,
        "affected_children": dependents if requires_reconciliation else [],
        "affected_count": len(dependents) if requires_reconciliation else 0,
        "reconciliation_action": (
            "Mark affected children with dirty flag for review"
            if requires_reconciliation else None
        )
    }


def update_tag(
    tag_id: str,
    field: str,
    value: str,
    needs_path: Path
) -> dict:
    """
    Prepare an update for a DDR tag.

    Note: This tool generates the update specification but does not
    modify files directly. The agent must apply changes to RST files.

    Parameters
    ----------
    tag_id : str
        The tag ID to update.
    field : str
        The field to update.
    value : str
        The new value.
    needs_path : Path
        Path to needs.json.

    Returns
    -------
    dict
        Update result with diff and reconciliation info.
    """
    tag_id = tag_id.strip()
    field = field.lower().strip()

    # Validate field
    if field not in UPDATEABLE_FIELDS:
        raise ValueError(
            f"Invalid field: {field}. Valid fields: {UPDATEABLE_FIELDS}"
        )

    # Load needs
    needs = load_needs(needs_path)

    # Check tag exists
    if tag_id not in needs:
        raise ValueError(f"Tag not found: {tag_id}")

    need = needs[tag_id]

    # Get current value
    old_value = ""
    if field == "title":
        old_value = need.get("title", "")
    elif field == "description" or field == "content":
        old_value = need.get("content", need.get("description", ""))
    elif field == "status":
        old_value = need.get("status", "") or ""

    # Find dependents for reconciliation
    dependents = find_downstream_dependents(tag_id, needs)

    # Generate update diff
    diff = generate_update_diff(tag_id, field, old_value, value, dependents)

    # Build result
    result = {
        "success": True,
        "update": diff,
        "source_file": need.get("docname", "") + ".rst",
        "line_number": need.get("lineno"),
        "instructions": [
            f"1. Open {need.get('docname', '')}.rst",
            f"2. Locate tag {tag_id} at line {need.get('lineno', 'unknown')}",
            f"3. Update {field} from '{diff['old_value']}' to '{value}'"
        ]
    }

    if diff["requires_reconciliation"]:
        result["reconciliation_required"] = True
        result["reconciliation_instructions"] = [
            "4. Set integrity_status to DIRTY per reconciliation_dirty_flag.md",
            "5. Review affected children for semantic consistency:",
            *[f"   - {d['id']} ({d['tier']}): {d['title']}" for d in dependents[:5]],
            *([f"   - ...and {len(dependents) - 5} more"] if len(dependents) > 5 else [])
        ]

    return result


def main() -> int:
    """
    CLI entry point for update_tag.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Update a DDR tag and identify reconciliation needs."
    )
    parser.add_argument(
        "--id",
        required=True,
        help="Tag ID to update (e.g., FSD-001)"
    )
    parser.add_argument(
        "--field",
        required=True,
        help=f"Field to update. Valid: {', '.join(UPDATEABLE_FIELDS)}"
    )
    parser.add_argument(
        "--value",
        required=True,
        help="New value for the field"
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

        result = update_tag(
            tag_id=args.id,
            field=args.field,
            value=args.value,
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
        print(f"Error updating tag: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
