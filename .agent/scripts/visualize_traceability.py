"""
Visualize Traceability Tool.

Generates Mermaid flowchart diagrams from DDR dependency graph.

Meta
----
Tool Definition : .agent/tools/trace_visualize.md
Knowledge Source: .agent/knowledge/sources/concepts/tier_hierarchy.md
Architect       : Antigravity IDE

Usage
-----
    python visualize_traceability.py --needs-json docs/_build/json/needs.json

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import json
import sys
from pathlib import Path
from collections import deque

TIER_ORDER = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]
TIER_COLORS = {"BRD": "#e3f2fd", "NFR": "#fff3e0", "FSD": "#e8f5e9",
               "SAD": "#fce4ec", "ICD": "#f3e5f5", "TDD": "#e0f7fa", "ISP": "#fff8e1"}


def get_tier(tag_id: str) -> str | None:
    if not tag_id: return None
    prefix = tag_id.split("-")[0].split(".")[0].upper()
    return prefix if prefix in TIER_ORDER else None


def load_needs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


def traverse(root: str, direction: str, depth: int, needs: dict) -> set:
    parents = {k: needs[k].get("links", []) for k in needs}
    children = {k: [] for k in needs}
    for nid, plist in parents.items():
        for pid in plist:
            if pid in children: children[pid].append(nid)

    visited = set()
    queue = deque([(root, 0)])
    while queue:
        node, lvl = queue.popleft()
        if node in visited or lvl > depth: continue
        visited.add(node)
        if direction in ("up", "both"):
            for p in parents.get(node, []): queue.append((p, lvl + 1))
        if direction in ("down", "both"):
            for c in children.get(node, []): queue.append((c, lvl + 1))
    return visited


def generate_mermaid(needs: dict, include: set | None = None) -> str:
    parents = {k: needs[k].get("links", []) for k in needs}
    tiers = {t: [] for t in TIER_ORDER}
    for nid in (include or needs.keys()):
        tier = get_tier(nid)
        if tier: tiers[tier].append(nid)

    lines = ["flowchart TD"]
    for tier in TIER_ORDER:
        if not tiers[tier]: continue
        lines.append(f"    subgraph {tier}[\"{tier}\"]")
        for nid in sorted(tiers[tier]):
            safe = nid.replace(".", "_").replace("-", "_")
            title = needs.get(nid, {}).get("title", nid)[:30].replace('"', "'")
            lines.append(f"        {safe}[\"{nid}: {title}\"]")
        lines.append(f"    end")
        lines.append(f"    style {tier} fill:{TIER_COLORS.get(tier)}")

    for nid in (include or needs.keys()):
        safe_c = nid.replace(".", "_").replace("-", "_")
        for pid in parents.get(nid, []):
            if include and pid not in include: continue
            safe_p = pid.replace(".", "_").replace("-", "_")
            lines.append(f"    {safe_c} -->|cites| {safe_p}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--root", help="Root tag ID")
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--direction", choices=["up", "down", "both"], default="both")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        needs = load_needs(path)
        include = traverse(args.root, args.direction, args.depth, needs) if args.root else None
        print(generate_mermaid(needs, include))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
