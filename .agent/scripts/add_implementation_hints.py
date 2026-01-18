"""
Add Implementation Hints Tool.

Enriches ISP stub files with implementation guidance from TDD/ICD references.

Meta
----
Tool Definition : .agent/tools/isp_add_implementation_hints.md
Knowledge Source: .agent/knowledge/sources/constraints/isp_numpy_docstrings.md
Architect       : Antigravity IDE

Usage
-----
    python add_implementation_hints.py --isp-file src/core.py --needs-json docs/_build/json/needs.json

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


def load_needs(path: Path) -> dict:
    """
    Load needs from needs.json.

    Parameters
    ----------
    path : Path
        Path to needs.json.

    Returns
    -------
    dict
        need_id -> need_data mapping.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("versions", {}).get("0.1", {}).get("needs", {})


def add_hints(isp_file: Path, needs: dict, dry_run: bool = False) -> str:
    """
    Add implementation hints to ISP stub file.

    Parameters
    ----------
    isp_file : Path
        Path to ISP Python file.
    needs : dict
        Loaded needs dictionary.
    dry_run : bool
        If True, print instead of write.

    Returns
    -------
    str
        Modified content.
    """
    content = isp_file.read_text(encoding="utf-8")
    refs = re.findall(r"\|([A-Z]{3}-\d+(?:\.\d+)?)\|", content)

    hints = []
    for ref in set(refs):
        if ref in needs:
            tag_content = needs[ref].get("content", "")[:150]
            hints.append(f"# IMPL: From {ref}: {tag_content}")

    if not hints: return content

    # Insert hints before first 'pass'
    hint_block = "\n".join(hints) + "\n"
    new_content = re.sub(r"(\s+)(pass\b)", rf"\1{hint_block}\1pass", content, count=1)

    if dry_run:
        print(new_content)
    else:
        output = isp_file.with_suffix(".hints.py")
        output.write_text(new_content, encoding="utf-8")
        print(f"Written to {output}")

    return new_content


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--isp-file", required=True)
    parser.add_argument("--needs-json", default="docs/_build/json/needs.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    isp = Path(args.isp_file)
    needs_path = Path(args.needs_json)

    if not isp.exists():
        print(f"Error: {isp} not found", file=sys.stderr); return 1
    if not needs_path.exists():
        print(f"Error: {needs_path} not found", file=sys.stderr); return 1

    try:
        add_hints(isp, load_needs(needs_path), args.dry_run)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
