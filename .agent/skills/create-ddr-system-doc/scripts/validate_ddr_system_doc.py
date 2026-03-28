#!/usr/bin/env python3
"""
Validate a generated DDR System documentation artifact against a source spec.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build_ddr_system_doc import load_yaml, validate_output_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a DDR System Markdown document against a DDR specification YAML file."
    )
    parser.add_argument("document_path", help="Path to the generated Markdown document.")
    parser.add_argument("--spec", required=True, help="Path to the DDR specification YAML file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    document_path = Path(args.document_path)
    spec_path = Path(args.spec)

    if not document_path.is_file():
        raise FileNotFoundError(f"Document not found: {document_path}")
    if not spec_path.is_file():
        raise FileNotFoundError(f"Specification file not found: {spec_path}")

    markdown = document_path.read_text(encoding="utf-8")
    spec = load_yaml(spec_path)
    issues = validate_output_text(markdown, spec)
    if issues:
        raise ValueError("Validation failed:\n- " + "\n- ".join(issues))

    print("DDR System documentation is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
