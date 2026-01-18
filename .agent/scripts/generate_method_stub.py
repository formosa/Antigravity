"""
Generate Method Stub Tool.

Creates Python method stub with Numpy-style docstring.

Meta
----
Tool Definition : .agent/tools/isp_generate_method_stub.md
Knowledge Source: .agent/knowledge/sources/constraints/isp_stub_only.md
                  .agent/knowledge/sources/constraints/isp_numpy_docstrings.md
Architect       : Antigravity IDE

Usage
-----
    python generate_method_stub.py --name process_message --tdd-ref TDD-1.2

Exit Codes
----------
0 : Success
1 : Error
"""
import argparse
import sys

TEMPLATE = '''def {name}(self{params_str}) -> {return_type}:
    """
    {description}

    Implements: |{tdd_ref}|
{fsd_line}
    Parameters
    ----------
{params_doc}
    Returns
    -------
    {return_type}
        {return_desc}
{raises_doc}    """
    pass
'''


def parse_params(params_str: str) -> tuple[str, str]:
    if not params_str: return "", "    None"
    parts = [p.strip() for p in params_str.split(",")]
    sig_parts, doc_parts = [], []
    for p in parts:
        segs = p.split(":")
        name = segs[0]
        ptype = segs[1] if len(segs) > 1 else "Any"
        desc = segs[2] if len(segs) > 2 else "Parameter description."
        sig_parts.append(f"{name}: {ptype}")
        doc_parts.append(f"    {name} : {ptype}\n        {desc}")
    return ", " + ", ".join(sig_parts), "\n".join(doc_parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--params", help="name:type:desc,...")
    parser.add_argument("--return-type", default="None")
    parser.add_argument("--return-desc", default="Return value.")
    parser.add_argument("--description", default="Method description.")
    parser.add_argument("--tdd-ref", required=True)
    parser.add_argument("--fsd-ref")
    parser.add_argument("--raises", help="Type:condition,...")
    args = parser.parse_args()

    params_str, params_doc = parse_params(args.params)
    fsd_line = f"    Requirements: |{args.fsd_ref}|\n" if args.fsd_ref else ""

    raises_doc = ""
    if args.raises:
        raises_doc = "\n    Raises\n    ------\n"
        for r in args.raises.split(","):
            parts = r.split(":")
            raises_doc += f"    {parts[0]}\n        {parts[1] if len(parts) > 1 else 'Error condition.'}\n"

    print(TEMPLATE.format(name=args.name, params_str=params_str, return_type=args.return_type,
                          description=args.description, tdd_ref=args.tdd_ref, fsd_line=fsd_line,
                          params_doc=params_doc, return_desc=args.return_desc, raises_doc=raises_doc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
