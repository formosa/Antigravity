"""
Detect Anti-Patterns Tool.

Scans DDR tags for structural and content violations.

Meta
----
Tool Definition : .agent/tools/detect_anti_patterns.md
Knowledge Source: .agent/knowledge/sources/constraints/sibling-prohibition.md
                  .agent/knowledge/sources/constraints/tag-immutability.md
                  .agent/knowledge/sources/protocols/traceability-chain.md
Architect       : Antigravity IDE

Usage
-----
    python detect_anti_patterns.py --needs-json docs/_build/json/needs.json

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

TIER_ORDER = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP", "TERM"]


def get_tier(tag_id: str) -> str | None:
    if not tag_id: return None
    prefix = tag_id.split("-")[0].split(".")[0].upper()
    return prefix if prefix in TIER_ORDER else None


def _is_sibling(tag_a: str, tag_b: str) -> bool:
    """Check if two tags are siblings (share same block parent).

    Examples:
        _is_sibling("FSD-4.3", "FSD-4.4") -> True   # Both under FSD-4
        _is_sibling("FSD-4.1", "FSD-4") -> False    # Parent relationship
        _is_sibling("FSD-3.1", "FSD-4.1") -> False  # Different parents
    """
    # If one is a prefix of the other (parent relationship), not siblings
    if tag_a.startswith(tag_b + ".") or tag_b.startswith(tag_a + "."):
        return False
    # Extract block parent (e.g., "FSD-4.3" -> "FSD-4")
    def get_parent(tag: str) -> str | None:
        if "." in tag:
            return tag.rsplit(".", 1)[0]
        return None
    parent_a, parent_b = get_parent(tag_a), get_parent(tag_b)
    # Siblings share the same block parent
    return parent_a is not None and parent_a == parent_b


def load_needs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


PATTERNS: dict[str, tuple[str, callable]] = {
    "AP001": ("Vertical Pollution", lambda n: n["tier"] in ["BRD", "NFR", "FSD"]
              and re.search(r"\b(def |class |import )\b", n.get("content", ""))),
    "AP002": ("Orphan Tag", lambda n: n["tier"] not in ["BRD", "TERM"] and not n.get("links")),
    "AP003": ("Sibling Citation", lambda n: any(
        get_tier(l) == n["tier"] and _is_sibling(n["id"], l) for l in n.get("links", []))),
    "AP004": ("Forward Reference", lambda n: any(
        get_tier(l) and n["tier"] and TIER_ORDER.index(get_tier(l)) > TIER_ORDER.index(n["tier"])
        for l in n.get("links", []) if get_tier(l))),
    "AP005": ("Missing Title", lambda n: not n.get("title") or n["title"] == n["id"]),
    "AP006": ("Dangling ISP", lambda n: n["tier"] == "ISP"
              and not any(get_tier(l) == "TDD" for l in n.get("links", []))),
    "AP007": ("ID Format Violation", lambda n:
        not re.match(r"^[A-Z]{3}-\d+(\.\d+)?$", n["id"])
        and not re.match(r"^TERM-[A-Z0-9-]+$", n["id"])),
    "AP008": ("Technology Leak in BRD", lambda n: n["tier"] == "BRD" and re.search(
        r"\b(Python|Java|API|SQL|GPU|REST|JSON)\b", n.get("content", ""), re.I)),
    "AP009": ("Empty Content", lambda n:
        not n.get("content", "").strip()
        and len(n.get("title", "")) < 20
        and n["tier"] != "BRD"),
}


def detect(needs: dict, patterns: list | None = None) -> dict:
    violations = []
    check_patterns = patterns if patterns else list(PATTERNS.keys())

    for nid, ndata in needs.items():
        ndata["tier"] = get_tier(nid)
        ndata["id"] = nid
        for pid in check_patterns:
            if pid not in PATTERNS: continue
            name, check = PATTERNS[pid]
            try:
                if check(ndata):
                    violations.append({"id": nid, "pattern": pid, "name": name})
            except: pass

    by_pattern = {}
    for v in violations:
        by_pattern.setdefault(v["pattern"], []).append(v)

    return {"scanned": len(needs), "violations": len(violations),
            "by_pattern": {k: len(v) for k, v in by_pattern.items()},
            "details": violations}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--patterns", help="Comma-separated pattern IDs")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        patterns = args.patterns.split(",") if args.patterns else None
        print(json.dumps(detect(load_needs(path), patterns), indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
