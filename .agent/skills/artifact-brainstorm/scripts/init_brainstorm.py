#!/usr/bin/env python3
"""
Initialize a brainstorm.md file from the canonical seeded source.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SEED = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"
DEFAULT_SOURCE_REFERENCE = (
    REPO_ROOT
    / ".agent"
    / "schemas"
    / "brainstorm"
    / "DDR_AppFramework_Brainstorm.docx"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a brainstorm.md document.")
    parser.add_argument(
        "output",
        nargs="?",
        default="brainstorm.md",
        help="Output path for the initialized brainstorm document.",
    )
    parser.add_argument(
        "--seed",
        default=str(DEFAULT_SEED),
        help="Canonical seed markdown source.",
    )
    parser.add_argument(
        "--source-reference",
        default=str(DEFAULT_SOURCE_REFERENCE),
        help="Reference source document recorded in the initialized output.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser.parse_args()


def render_seed(seed_text: str, source_reference: Path) -> str:
    today = date.today().isoformat()
    return (
        seed_text.replace("{{CREATED_DATE}}", today)
        .replace("{{LAST_REVISED_DATE}}", today)
        .replace("{{SOURCE_REFERENCE_PATH}}", source_reference.as_posix())
    )


def main() -> int:
    args = parse_args()

    output_path = (REPO_ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    seed_path = (REPO_ROOT / args.seed).resolve() if not Path(args.seed).is_absolute() else Path(args.seed)
    source_reference = (
        (REPO_ROOT / args.source_reference).resolve()
        if not Path(args.source_reference).is_absolute()
        else Path(args.source_reference)
    )

    if not seed_path.exists():
        print(f"ERROR: seed file not found: {seed_path}")
        return 1
    if not source_reference.exists():
        print(f"ERROR: source reference not found: {source_reference}")
        return 1
    if output_path.exists() and not args.overwrite:
        print(f"ERROR: output already exists: {output_path}")
        return 1

    rendered = render_seed(seed_path.read_text(encoding="utf-8"), source_reference)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8", newline="\n")

    print(f"Brainstorm initialized: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
