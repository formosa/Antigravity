"""
Validate Tier Compliance Tool.

Validates DDR tag content against tier-specific constraints.

Meta
----
Tool Definition : .agent/tools/validate_tier_compliance.md
Knowledge Source: .agent/knowledge/sources/constraints/brd_technology_agnostic.md
                  .agent/knowledge/sources/constraints/nfr_numeric_constraints.md
                  .agent/knowledge/sources/constraints/fsd_no_implementation.md
                  .agent/knowledge/sources/constraints/isp_stub_only.md
Architect       : Antigravity IDE

Usage
-----
    python validate_tier_compliance.py --needs-json docs/_build/json/needs.json --all

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

TIER_ORDER = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]

TECH_TERMS_PATTERN = r"\b(Python|JavaScript|Java|React|ZeroMQ|PySide6|pvporcupine|" \
                     r"RTX|CUDA|AMD|TCP|MQTT|REST|API|PostgreSQL|Redis|SQLite|" \
                     r"JSON|YAML|Protobuf|Docker|Kubernetes|AWS|Azure|GPU|CPU)\b"

RULES: dict[str, list[tuple[str, callable]]] = {
    "BRD": [
        ("tech_agnostic", lambda c: not re.search(TECH_TERMS_PATTERN, c, re.I)),
        ("measurable", lambda c: bool(re.search(r"\b(KPI|metric|measure|success|target)\b", c, re.I))),
        ("stakeholder_focus", lambda c: bool(re.search(r"\b(user|customer|stakeholder|business)\b", c, re.I))),
    ],
    "NFR": [
        ("numeric_targets", lambda c: bool(re.search(r"\b\d+\s*(ms|%|seconds?|MB|GB|requests?/sec)\b", c, re.I))),
        ("constraint_language", lambda c: bool(re.search(r"\b(shall|must|limit|maximum|minimum)\b", c, re.I))),
    ],
    "FSD": [
        ("no_impl", lambda c: not re.search(r"\b(def |class |return |import )\b", c)),
        ("behavioral_language", lambda c: bool(re.search(r"\b(when|then|user|shall|can|will)\b", c, re.I))),
    ],
    "SAD": [
        ("pattern_reference", lambda c: bool(re.search(r"\b(pattern|topology|component|layer|service)\b", c, re.I))),
    ],
    "ICD": [
        ("schema_definition", lambda c: bool(re.search(r"\b(schema|format|field|type|contract|interface)\b", c, re.I))),
    ],
    "TDD": [
        ("class_structure", lambda c: bool(re.search(r"\b(class|method|function|interface)\b", c, re.I))),
    ],
    "ISP": [
        ("stub_only", lambda c: "pass" in c or not re.search(r"\b(if |for |while |return (?!None))\b", c)),
        ("has_docstring", lambda c: '"""' in c or "'''" in c),
    ],
}


def get_tier(tag_id: str) -> str | None:
    if not tag_id: return None
    prefix = tag_id.split("-")[0].split(".")[0].upper()
    return prefix if prefix in TIER_ORDER else None


def load_needs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


def validate(needs: dict, target_id: str = None, target_tier: str = None) -> dict:
    violations = []
    checked = 0

    for nid, ndata in needs.items():
        tier = get_tier(nid)
        if target_id and nid != target_id: continue
        if target_tier and tier != target_tier: continue
        if tier not in RULES: continue

        checked += 1
        content = ndata.get("content", "") + " " + ndata.get("title", "")
        for rule_name, check in RULES[tier]:
            try:
                if not check(content):
                    violations.append({"id": nid, "tier": tier, "rule": rule_name})
            except: pass

    return {"checked": checked, "violations": len(violations), "details": violations}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--id", help="Single tag ID")
    parser.add_argument("--tier", help="All in tier")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        print(json.dumps(validate(load_needs(path), args.id, args.tier), indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
