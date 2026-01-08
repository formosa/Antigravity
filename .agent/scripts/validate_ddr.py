#!/usr/bin/env python3
"""DDR Validation System for Sphinx-Needs Documentation."""
import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

# === CONSTANTS ===
VALID_PARENTS: Dict[str, List[str]] = {
    "BRD": [],
    "NFR": ["BRD"],
    "FSD": ["BRD", "NFR"],
    "SAD": ["FSD"],
    "ICD": ["SAD", "NFR"],
    "TDD": ["SAD", "ICD"],
    "ISP": ["TDD"],
    "TERM": [],
}

# === DATA MODELS ===
@dataclass
class Issue:
    severity: str      # ERROR, WARNING
    category: str      # HIERARCHY, ORPHAN, DUPLICATE, BROKEN_LINK
    tag_id: str
    file_path: str
    message: str

# === CORE FUNCTIONS ===
def load_needs_json(json_path: Path) -> Dict[str, dict]:
    """Load needs.json and return dict keyed by need ID."""
    if not json_path.exists():
        print(f"ERROR: {json_path} not found. Run sphinx-build -b needs first.")
        sys.exit(2)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    version = list(data["versions"].keys())[0]
    return data["versions"][version]["needs"]

def get_prefix(tag_id: str) -> str:
    """Extract prefix from tag ID (e.g., 'BRD' from 'BRD-3.1')."""
    return tag_id.split("-")[0] if "-" in tag_id else ""

def is_atomic_refinement(child_id: str, parent_id: str) -> bool:
    """Check if child refines parent (e.g., BRD-3.1 -> BRD-3)."""
    return child_id.startswith(f"{parent_id}.")

def is_lateral(child_id: str, parent_id: str) -> bool:
    """Check if both are atomics of same block (e.g., BRD-3.1 -> BRD-3.2)."""
    c_prefix, p_prefix = get_prefix(child_id), get_prefix(parent_id)
    if c_prefix != p_prefix:
        return False
    # Both must be atomics (contain .)
    if "." not in child_id or "." not in parent_id:
        return False
    # Extract block (e.g., BRD-3 from BRD-3.1)
    c_block = child_id.rsplit(".", 1)[0]
    p_block = parent_id.rsplit(".", 1)[0]
    return c_block == p_block  # Same block = lateral

def validate(needs: Dict[str, dict]) -> List[Issue]:
    """Run all validation checks."""
    issues: List[Issue] = []
    all_ids: Set[str] = set(needs.keys())

    for need_id, need in needs.items():
        prefix = get_prefix(need_id)
        if prefix not in VALID_PARENTS:
            continue  # Skip unknown prefixes

        file_path = need.get("docname", "unknown")
        links = need.get("links", [])

        # Check: Orphan (non-root with no links)
        if prefix not in ("BRD", "TERM") and not links:
            issues.append(Issue("ERROR", "ORPHAN", need_id, file_path,
                "No parent links. Add :links: field."))
            continue

        for parent_id in links:
            # Check: Broken link
            if parent_id not in all_ids:
                issues.append(Issue("ERROR", "BROKEN_LINK", need_id, file_path,
                    f"Links to non-existent '{parent_id}'."))
                continue

            parent_prefix = get_prefix(parent_id)

            # Check: Atomic refinement (always valid)
            if is_atomic_refinement(need_id, parent_id):
                continue

            # Check: Lateral (always invalid)
            if is_lateral(need_id, parent_id):
                issues.append(Issue("ERROR", "LATERAL", need_id, file_path,
                    f"Lateral link to sibling '{parent_id}'. Remove or use prose."))
                continue

            # Check: Hierarchy
            valid = VALID_PARENTS.get(prefix, [])
            if parent_prefix not in valid:
                expected = ", ".join(valid) if valid else "(root)"
                issues.append(Issue("ERROR", "HIERARCHY", need_id, file_path,
                    f"Links to {parent_prefix}, but {prefix} can only cite: {expected}."))

    # Check: Duplicates
    seen: Dict[str, str] = {}
    for need_id, need in needs.items():
        if need_id in seen:
            issues.append(Issue("ERROR", "DUPLICATE", need_id, need.get("docname", ""),
                f"Duplicate ID. Also defined in '{seen[need_id]}'."))
        seen[need_id] = need.get("docname", "")

    return issues

def generate_reports(issues: List[Issue], needs: Dict, sandbox_dir: Path) -> None:
    """Write JSON and Markdown reports."""
    sandbox_dir.mkdir(parents=True, exist_ok=True)

    # Inventory
    inventory = defaultdict(int)
    for need_id in needs:
        prefix = get_prefix(need_id)
        if prefix:
            inventory[prefix] += 1

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tags": len(needs),
        "inventory": dict(inventory),
        "error_count": sum(1 for i in issues if i.severity == "ERROR"),
        "warning_count": sum(1 for i in issues if i.severity == "WARNING"),
        "issues": [asdict(i) for i in issues],
    }

    # JSON
    with open(sandbox_dir / "ddr_audit.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Markdown
    status = "✅ CLEAN" if report["error_count"] == 0 else f"❌ {report['error_count']} ERRORS"
    md = [
        "# DDR Audit Report",
        f"\n**Timestamp**: {report['timestamp']}",
        f"**Status**: {status}",
        f"\n## Inventory ({report['total_tags']} tags)\n",
        "| Prefix | Count |",
        "|:-------|------:|",
    ]
    for pfx in ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP", "TERM"]:
        if pfx in inventory:
            md.append(f"| {pfx} | {inventory[pfx]} |")

    if issues:
        md.append("\n## Issues\n")
        for i in issues:
            md.append(f"- **{i.category}** `{i.tag_id}` ({i.file_path}): {i.message}")
    else:
        md.append("\n## Issues\n\n*None*")

    with open(sandbox_dir / "ddr_audit.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def main() -> int:
    parser = argparse.ArgumentParser(description="DDR Validation System")
    parser.add_argument("--docs-dir", default="docs", help="Docs directory")
    parser.add_argument("--sandbox-id", required=True, help="UUID for output")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    json_path = docs_dir / "_build" / "json" / "needs.json"
    sandbox_dir = Path(".agent/.sandbox") / f"validate_ddr-{args.sandbox_id}"

    needs = load_needs_json(json_path)
    issues = validate(needs)
    generate_reports(issues, needs, sandbox_dir)

    error_count = sum(1 for i in issues if i.severity == "ERROR")
    print(f"Validation complete. {error_count} errors. Report: {sandbox_dir}/ddr_audit.md")
    return 1 if error_count > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
