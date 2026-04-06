#!/usr/bin/env python3
"""
Scaffold a new workflow from the asset-workflow canonical example.

role: workflow asset initializer
entrypoints: main
reads: workflow example template
writes: new workflow markdown file
external_io: fs
state_model: stateless
failure_surface: fs access errors; template missing; invalid name
coupling: coupled to workflow schema and template structure
determinism: deterministic
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VALID_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for workflow scaffolding.

    purpose: CLI configuration extraction
    """
    parser = argparse.ArgumentParser(description="Create a new Antigravity workflow scaffold.")
    parser.add_argument("workflow_name", help="Lowercase hyphen-case workflow name.")
    parser.add_argument(
        "--path",
        default=".agent/workflows",
        help="Output directory for the workflow file. Defaults to .agent/workflows",
    )
    return parser.parse_args()


def repo_root() -> Path:
    """
    Resolve the repository root directory.

    purpose: path resolution base
    """
    return Path(__file__).resolve().parents[4]


def example_path() -> Path:
    """
    Resolve the path to the canonical workflow example template.

    purpose: template discovery
    """
    return Path(__file__).resolve().parents[1] / "resources" / "schema" / "workflow" / "example.md"


def build_content(workflow_name: str, template: str) -> str:
    """
    Generate workflow file content by populating the template with the workflow name.

    purpose: template population
    preconditions: template has name/description frontmatter
    postconditions: returns populated markdown string
    mutates: none
    reads: workflow_name, template
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: coupled to template frontmatter structure

    Parameters
    ----------
    workflow_name : str
        lowercase hyphen-case workflow name
    template : str
        raw markdown template

    Returns
    -------
    str
        populated markdown content

    Raises
    ------
    ValueError
        if template is missing required frontmatter fields
    """
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
    """
    Execute the workflow scaffolding logic.

    purpose: entrypoint
    preconditions: workflow name must be valid; template must exist
    postconditions: new workflow file created in target directory
    mutates: filesystem (creates file and parent dirs)
    reads: filesystem (template)
    writes: filesystem (output workflow)
    external_io: fs
    determinism: deterministic
    idempotency: no (fails if file exists)
    concurrency: process-local
    """
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
