"""
Generate Traceability Report Tool.

Analyzes DDR citation chains and generates violation reports.

Meta
----
Tool Definition : .agent/tools/trace_generate_report.md
Knowledge Source: .agent/knowledge/sources/protocols/traceability-chain.md
Architect       : Antigravity IDE

Usage
-----
    python generate_traceability_report.py --needs-json docs/_build/json/needs.json --output report.md

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import json
import sys
from pathlib import Path

TIER_ORDER = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]

# Strict Parent-Child Hierarchy (Protocol: traceability-chain.md)
VALID_PARENTS = {
    "NFR": ["BRD"],
    "FSD": ["BRD", "NFR"],
    "SAD": ["FSD", "NFR"],
    "ICD": ["SAD", "NFR"],
    "TDD": ["SAD", "ICD"],
    "ISP": ["TDD"]
}


def get_tier(tag_id: str) -> str | None:
    if not tag_id: return None
    prefix = tag_id.split("-")[0].split(".")[0].upper()
    return prefix if prefix in TIER_ORDER else None


def get_block_id(tag_id: str) -> str:
    return tag_id.split(".")[0]


def get_tier_idx(tier: str | None) -> int:
    return TIER_ORDER.index(tier) if tier in TIER_ORDER else -1


def load_needs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


def analyze(needs: dict, severity: str = "ALL") -> dict:
    violations, valid = [], []
    needs_set = set(needs.keys())

    for nid, ndata in needs.items():
        tier = get_tier(nid)
        # BRD is Root; no parents required
        if tier == "BRD": continue

        links = ndata.get("links", [])
        ntitle = ndata.get("title", "No Title")
        nviol = []

        if not links:
            nviol.append({"id": nid, "title": ntitle, "type": "ORPHAN", "severity": "ERROR",
                          "message": "No parent citations", "cited": "None"})

        for pid in links:
            ptier = get_tier(pid)
            ptitle = needs.get(pid, {}).get("title", "Unknown") if pid in needs else "Unknown"

            # 1. Existential Check
            if pid not in needs_set:
                nviol.append({"id": nid, "title": ntitle, "type": "MISSING_PARENT", "severity": "ERROR",
                              "message": f"Parent '{pid}' not found", "cited": pid})
                continue

            # 2. Atomic -> Block Exception (Allow FSD-1.1 -> FSD-1)
            # Must be strictly same-prefix block parent
            if pid == get_block_id(nid) and nid != pid:
                continue

            # 3. Valid Citation Matrix Check (Strict Layering)
            # If tier is unknown or not in matrix (e.g., unexpected prefix), default to strict error
            allowed_parents = VALID_PARENTS.get(tier, [])
            if ptier not in allowed_parents:
                # Determine specific violation type for clarity
                if ptier == tier:
                     # Sibling Prohibition (Protocol: sibling-prohibition.md)
                     # Treat as ERROR per strict enforcement
                     nviol.append({"id": nid, "title": ntitle, "type": "SIBLING_CITATION", "severity": "ERROR",
                                  "message": f"Cites sibling '{pid}'", "cited": f"{pid} ({ptitle})"})
                else:
                    # Forward Ref OR Skip-Level
                    # We use 'INVALID_PARENT_TIER' to cover both cases under the strict matrix
                    nviol.append({"id": nid, "title": ntitle, "type": "INVALID_PARENT_TIER", "severity": "ERROR",
                                  "message": f"Invalid parent tier '{ptier}' for '{tier}'. Allowed: {allowed_parents}",
                                  "cited": f"{pid} ({ptitle})"})

        if nviol: violations.extend(nviol)
        else: valid.append(nid)

    if severity != "ALL":
        violations = [v for v in violations if v["severity"] == severity]

    by_type = {}
    for v in violations:
        by_type.setdefault(v["type"], []).append(v)

    return {"summary": {"total": len(needs), "violations": len(violations),
                        "valid": len(valid), "by_type": {k: len(v) for k, v in by_type.items()}},
            "violations": violations, "valid_samples": valid[:10]}


def format_out(result: dict, fmt: str) -> str:
    if fmt == "json": return json.dumps(result, indent=2)
    if fmt == "summary":
        lines = [f"Analyzed: {result['summary']['total']}", f"Violations: {result['summary']['violations']}"]
        for t, c in result["summary"]["by_type"].items(): lines.append(f"  {t}: {c}")
        return "\n".join(lines)

    lines = [f"# Traceability Report",
             f"**Analyzed:** {result['summary']['total']} tags | **Violations:** {result['summary']['violations']}",
             ""]

    # Group by Type for better readability
    by_type = result["summary"]["by_type"]
    violations = result["violations"]

    for v_type in by_type.keys():
        type_violations = [v for v in violations if v['type'] == v_type]
        lines.append(f"## {v_type} ({len(type_violations)})")
        lines.append("| ID | Title | Severity | Cited Tag | Message |")
        lines.append("|:---|:------|:---------|:----------|:--------|")
        for v in type_violations:
            lines.append(f"| `{v['id']}` | {v['title']} | **{v['severity']}** | {v['cited']} | {v['message']} |")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--format", choices=["json", "markdown", "summary"], default="summary")
    parser.add_argument("--severity", choices=["ERROR", "WARNING", "ALL"], default="ALL")
    parser.add_argument("--output", help="Path to output file (default: stdout)")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        content = format_out(analyze(load_needs(path), args.severity), args.format)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            print(content)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
