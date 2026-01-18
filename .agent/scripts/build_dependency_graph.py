"""
Build Dependency Graph Tool.

Constructs citation dependency graph from needs.json.

Meta
----
Tool Definition : .agent/tools/trace_build_dependency_graph.md
Knowledge Source: .agent/knowledge/sources/protocols/traceability_chain.md
Architect       : Antigravity IDE

Usage
-----
    python build_dependency_graph.py --needs-json docs/_build/json/needs.json

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any

TIER_ORDER: list[str] = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]


def get_tier(tag_id: str) -> str | None:
    if not tag_id:
        return None
    prefix = tag_id.split("-")[0].split(".")[0].upper()
    return prefix if prefix in TIER_ORDER else None


def load_needs(path: Path) -> dict[str, dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


def build_graph(needs: dict, include_orphans: bool = False) -> dict[str, Any]:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    for nid, ndata in needs.items():
        tier = get_tier(nid)
        nodes[nid] = {"tier": tier, "title": ndata.get("title", nid),
                      "parents": ndata.get("links", []), "children": []}

    for nid, node in nodes.items():
        for pid in node["parents"]:
            if pid in nodes:
                nodes[pid]["children"].append(nid)
                edges.append({"source": nid, "target": pid})

    orphans = [n for n, d in nodes.items() if d["tier"] != "BRD" and not d["parents"]]
    roots = [n for n, d in nodes.items() if d["tier"] == "BRD"]

    def has_cycle() -> bool:
        visited, rec = set(), set()
        def dfs(n):
            visited.add(n); rec.add(n)
            for p in nodes.get(n, {}).get("parents", []):
                if p not in visited and dfs(p): return True
                if p in rec: return True
            rec.remove(n); return False
        return any(dfs(n) for n in nodes if n not in visited)

    if not include_orphans:
        nodes = {k: v for k, v in nodes.items() if k not in orphans or v["tier"] == "BRD"}

    tiers = {}
    for n in nodes.values():
        t = n["tier"] or "UNKNOWN"
        tiers[t] = tiers.get(t, 0) + 1

    return {"nodes": nodes, "edges": edges,
            "stats": {"total_nodes": len(nodes), "total_edges": len(edges),
                      "orphan_count": len(orphans), "root_count": len(roots), "has_cycles": has_cycle()},
            "tiers_summary": tiers}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build DDR dependency graph.")
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--include-orphans", action="store_true")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        result = build_graph(load_needs(path), args.include_orphans)
        out = json.dumps(result, indent=2)
        if args.output: Path(args.output).write_text(out, encoding="utf-8")
        else: print(out)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
