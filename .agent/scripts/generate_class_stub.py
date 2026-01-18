"""
Generate Class Stub Tool.

Creates Python class stub from TDD specification.

Meta
----
Tool Definition : .agent/tools/isp_generate_class_stub.md
Knowledge Source: .agent/knowledge/sources/constraints/isp_stub_only.md
                  .agent/knowledge/sources/constraints/isp_numpy_docstrings.md
Architect       : Antigravity IDE

Usage
-----
    python generate_class_stub.py --tdd-id TDD-1 --needs-json docs/_build/json/needs.json

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import json
import sys
from pathlib import Path


def load_needs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


TEMPLATE = '''class {class_name}:
    """
    {description}

    Ref: |{tdd_id}|
    """

    def __init__(self):
        """Initialize {class_name}."""
        pass
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tdd-id", required=True)
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--output")
    args = parser.parse_args()

    path = Path(args.needs_json)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr); return 1

    try:
        needs = load_needs(path)
        if args.tdd_id not in needs:
            print(f"Error: {args.tdd_id} not found", file=sys.stderr); return 1

        tdd = needs[args.tdd_id]
        title = tdd.get("title", args.tdd_id)
        class_name = "".join(w.capitalize() for w in title.split()[:3])
        desc = tdd.get("content", title)[:100]

        code = TEMPLATE.format(class_name=class_name, description=desc, tdd_id=args.tdd_id)
        if args.output: Path(args.output).write_text(code)
        else: print(code)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
