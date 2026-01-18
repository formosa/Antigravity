"""
Generate Traceability Report Tool.

Analyzes DDR citation chains and generates violation reports.

Meta
----
Tool Definition : .agent/tools/trace_generate_report.md
Knowledge Source: .agent/knowledge/sources/protocols/traceability_chain.md
Architect       : Antigravity IDE

Usage
-----
    python generate_traceability_report.py --needs-json docs/_build/json/needs.json

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


def get_tier(tag_id: str) -> str | None:
    if not tag_id: return None
    prefix = tag_id.split("-")[0].split(".")[0].upper()
    return prefix if prefix in TIER_ORDER else None


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
        links = ndata.get("links", [])
        if tier == "BRD": continue

        nviol = []
        if not links:
            nviol.append({"id": nid, "type": "ORPHAN", "severity": "ERROR",
                          "message": "No parent citations"})

        for pid in links:
            ptier = get_tier(pid)
            if pid not in needs_set:
                nviol.append({"id": nid, "type": "MISSING_PARENT", "severity": "ERROR",
                              "message": f"Parent '{pid}' not found"})
            elif ptier == tier:
                nviol.append({"id": nid, "type": "SIBLING_CITATION", "severity": "WARNING",
                              "message": f"Same-tier citation to '{pid}'"})
            elif ptier and tier and get_tier_idx(ptier) > get_tier_idx(tier):
                nviol.append({"id": nid, "type": "FORWARD_REFERENCE", "severity": "ERROR",
                              "message": f"References lower-tier '{pid}'"})

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
    lines = [f"# Traceability Report", f"- Violations: {result['summary']['violations']}"]
    for v in result["violations"][:20]:
        lines.append(f"- `{v['id']}` [{v['severity']}] {v['type']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--format", choices=["json", "markdown", "summary"], default="summary")
    parser.add_argument("--severity", choices=["ERROR", "WARNING", "ALL"], default="ALL")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        print(format_out(analyze(load_needs(path), args.severity), args.format))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
