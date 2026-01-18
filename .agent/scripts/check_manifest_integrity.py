"""
Check Manifest Integrity Tool.

Validates reconciliation manifest blocks against DDR structure requirements.

Meta
----
Tool Definition : .agent/tools/check_manifest_integrity.md
Knowledge Source: .agent/knowledge/sources/patterns/manifest_structure.md
                  .agent/knowledge/sources/protocols/reconciliation_dirty_flag.md
Architect       : Antigravity IDE

Usage
-----
    python check_manifest_integrity.py --manifest-dir docs/ --needs-json docs/_build/json/needs.json

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Required fields per manifest_structure.md §Fields
REQUIRED_FIELDS: list[str] = [
    ":section_id:", ":integrity_status:", ":timestamp:",
    ":tag_count:", ":tag_inventory:", ":pending_items:"
]
VALID_INTEGRITY_STATUS: list[str] = ["CLEAN", "DIRTY"]

def load_needs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


def check_manifests(manifest_dir: Path, needs: dict) -> dict:
    """
    Validate all reconciliation manifests in directory.

    Parameters
    ----------
    manifest_dir : Path
        Directory to search for manifest files.
    needs : dict
        Loaded needs.json dictionary for tag validation.

    Returns
    -------
    dict
        Validation results with manifests_checked, issues count, and details.
    """
    issues = []
    manifests = list(manifest_dir.rglob("reconciliation_manifest.rst"))

    for mpath in manifests:
        content = mpath.read_text(encoding="utf-8")
        manifest_issues = []

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in content:
                manifest_issues.append({
                    "manifest": str(mpath), "type": "MISSING_FIELD",
                    "field": field, "severity": "ERROR"
                })

        # Check integrity_status value
        status_match = re.search(r':integrity_status:\s*"?(\w+)"?', content)
        if status_match:
            status_val = status_match.group(1)
            if status_val not in VALID_INTEGRITY_STATUS:
                manifest_issues.append({
                    "manifest": str(mpath), "type": "INVALID_STATUS",
                    "value": status_val, "severity": "ERROR"
                })

        # Check tag_count vs tag_inventory mismatch (anti-pattern)
        count_match = re.search(r':tag_count:\s*(\d+)', content)
        inventory_match = re.search(r':tag_inventory:\s*\[([^\]]*)\]', content)
        if count_match and inventory_match:
            declared_count = int(count_match.group(1))
            inventory_items = [t.strip().strip('"\'')
                               for t in inventory_match.group(1).split(",") if t.strip()]
            if declared_count != len(inventory_items):
                manifest_issues.append({
                    "manifest": str(mpath), "type": "COUNT_MISMATCH",
                    "declared": declared_count, "actual": len(inventory_items),
                    "severity": "ERROR"
                })

        # Check pending items reference valid tags
        pending = re.findall(r'"target_tag":\s*"([^"]+)"', content)
        for tag in pending:
            if tag and tag not in needs:
                manifest_issues.append({
                    "manifest": str(mpath), "type": "MISSING_TAG",
                    "tag": tag, "severity": "WARNING"
                })

        issues.extend(manifest_issues)

    by_type = {}
    for issue in issues:
        t = issue.get("type", "UNKNOWN")
        by_type[t] = by_type.get(t, 0) + 1

    return {
        "manifests_checked": len(manifests),
        "issues": len(issues),
        "by_type": by_type,
        "details": issues
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-dir", default="docs/")
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    args = parser.parse_args()

    needs_path = Path(args.needs_json)
    if not needs_path.exists():
        print(f"Error: {needs_path} not found", file=sys.stderr); return 1

    try:
        print(json.dumps(check_manifests(Path(args.manifest_dir), load_needs(needs_path)), indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
