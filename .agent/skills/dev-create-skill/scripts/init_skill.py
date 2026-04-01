#!/usr/bin/env python3
"""
Skill Initializer - Creates a new Antigravity v1.20.3 compliant skill from template.

Usage:
    init_skill.py <skill-name> --path <path> [--resources scripts,resources,assets] [--examples]
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

VALID_RESOURCE_DIRS = {"scripts", "resources", "assets"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

SKILL_TEMPLATE = """---
name: {skill_name}
version: 1.0.0
description: "TODO: Describe exactly what this skill does. Use when the task is a specific trigger context. Do not use when the task is the closest adjacent but out-of-scope work."
---

<when_to_use>
- Use when the user asks for [primary outcome].
- Use when the request mentions [keyword or artifact 1], [keyword or artifact 2], or [target file type].
- Do not use when the task is [adjacent but out-of-scope work].
- Example prompt: "[TODO realistic user prompt 1]"
- Example prompt: "[TODO realistic user prompt 2]"
</when_to_use>

<how_to_use>
1. Gather 2-3 realistic requests this skill must handle and extract the required inputs, outputs, and exclusions they imply.
2. Keep the skill instruction-only unless deterministic scripts or assets materially reduce ambiguity or repeated work.
3. Write ordered actions with explicit inputs, expected outputs, and a verification step before completion.
4. Add only the files this skill will actually use and reference each one in `<resources_reference>` with whether it should be read or run, and why.
5. Validate the finished skill and trigger-test with prompts that should and should not invoke it.
</how_to_use>

<constraints>
- Do not use vague verbs such as "improve" or "optimize" without concrete acceptance criteria.
- Do not assume tools, packages, files, credentials, or permissions exist unless the skill explicitly verifies them.
- Do not reference scripts, resources, or assets that are absent or unused.
- Keep skill-local paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>
- Read `resources/schema/skill.d.ts` to confirm the required frontmatter and XML block contract before finalizing the skill.
</resources_reference>
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example deterministic script for {skill_name}.
"""


def main():
    print("Run the real deterministic workflow for {skill_name} here.")


if __name__ == "__main__":
    main()
'''

EXAMPLE_RESOURCE = """<document_purpose>
This resource file holds domain-specific guidance that is too detailed for SKILL.md and should only be read when the skill actually needs it.
</document_purpose>

<usage_rules>
- Replace this example with real workflow guidance, schemas, or policy text.
- Keep this file referenced directly from `SKILL.md`.
</usage_rules>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new Antigravity skill scaffold.")
    parser.add_argument("skill_name", help="Lowercase hyphen-case skill name.")
    parser.add_argument("--path", required=True, help="Parent directory where the skill folder will be created.")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated optional directories to create: scripts,resources,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Create optional example files inside requested folders.",
    )
    return parser.parse_args()


def parse_resource_dirs(raw_value: str) -> set[str]:
    if not raw_value.strip():
        return set()

    resource_dirs = {item.strip() for item in raw_value.split(",") if item.strip()}
    invalid = sorted(resource_dirs - VALID_RESOURCE_DIRS)
    if invalid:
        valid = ", ".join(sorted(VALID_RESOURCE_DIRS))
        raise ValueError(f"Unsupported resource directory option(s): {', '.join(invalid)}. Valid options: {valid}.")
    return resource_dirs


def copy_schema_bundle(skill_dir: Path) -> None:
    schema_dest_dir = skill_dir / "resources" / "schema"
    source_schema_path = Path(__file__).resolve().parent.parent / "resources" / "schema"
    if source_schema_path.exists():
        shutil.copytree(source_schema_path, schema_dest_dir, dirs_exist_ok=True)


def create_optional_dirs(skill_dir: Path, resource_dirs: set[str], include_examples: bool, skill_name: str) -> None:
    if "scripts" in resource_dirs:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        if include_examples:
            example_script = scripts_dir / "example.py"
            example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8")
            example_script.chmod(0o755)

    if "assets" in resource_dirs:
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(exist_ok=True)

    if "resources" in resource_dirs and include_examples:
        example_resource = skill_dir / "resources" / "reference.md"
        example_resource.write_text(EXAMPLE_RESOURCE, encoding="utf-8")


def init_skill(skill_name: str, path: str, resource_dirs: set[str] | None = None, include_examples: bool = False) -> Path | None:
    resource_dirs = resource_dirs or set()
    skill_dir = Path(path).resolve() / skill_name

    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        print("Error: Skill name must be lowercase letters, digits, or hyphens and be at most 64 characters.")
        return None

    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
    except Exception as exc:
        print(f"Error creating directory: {exc}")
        return None

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(SKILL_TEMPLATE.format(skill_name=skill_name), encoding="utf-8")
        print("Created SKILL.md")
    except Exception as exc:
        print(f"Error creating SKILL.md: {exc}")
        return None

    try:
        copy_schema_bundle(skill_dir)
        create_optional_dirs(skill_dir, resource_dirs, include_examples, skill_name)
        print("Created schema bundle and requested optional directories")
    except Exception as exc:
        print(f"Error creating directories: {exc}")
        return None

    print(f"\nSkill '{skill_name}' initialized successfully at {skill_dir}")
    return skill_dir


def main() -> None:
    args = parse_args()

    try:
        resource_dirs = parse_resource_dirs(args.resources)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    skill_dir = init_skill(args.skill_name, args.path, resource_dirs=resource_dirs, include_examples=args.examples)
    sys.exit(0 if skill_dir else 1)


if __name__ == "__main__":
    main()
