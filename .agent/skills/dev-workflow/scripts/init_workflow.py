#!/usr/bin/env python3
"""
Scaffold a new workflow from the dev-workflow canonical example.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VALID_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new Antigravity workflow scaffold.")
    parser.add_argument("workflow_name", help="Lowercase hyphen-case workflow name.")
    parser.add_argument(
        "--path",
        default=".agent/workflows",
        help="Output directory for the workflow file. Defaults to .agent/workflows",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def example_path() -> Path:
    return Path(__file__).resolve().parents[1] / "resources" / "schema" / "workflow" / "example.md"


def build_content(workflow_name: str, template: str) -> str:
    lines = template.splitlines()
    updated: list[str] = []
    in_frontmatter = False
    replaced_name = False
    replaced_description = False

    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            updated.append(line)
            continue

        if in_frontmatter:
            if line.startswith("name:"):
                updated.append(f"name: {workflow_name}")
                replaced_name = True
                continue
            if line.startswith("description:"):
                updated.append(
                    'description: "TODO: Describe the repeatable workflow outcome, trigger context, and closest exclusions."'
                )
                replaced_description = True
                continue

        updated.append(line)

    if not replaced_name or not replaced_description:
        raise ValueError("Workflow example does not expose the expected frontmatter fields.")

    return "\n".join(updated) + "\n"


def main() -> None:
    args = parse_args()
    workflow_name = args.workflow_name.strip()
    if not VALID_NAME_PATTERN.fullmatch(workflow_name):
        print("Error: Workflow name must use lowercase letters, digits, and hyphens only.")
        sys.exit(1)

    output_dir = (repo_root() / args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{workflow_name}.md"

    if output_path.exists():
        print(f"Error: Workflow already exists: {output_path}")
        sys.exit(1)

    template_path = example_path()
    if not template_path.exists():
        print(f"Error: Workflow example not found: {template_path}")
        sys.exit(1)

    template = template_path.read_text(encoding="utf-8")
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_content(workflow_name, template))
    print(f"[OK] Workflow scaffolded: {output_path}")


if __name__ == "__main__":
    main()
