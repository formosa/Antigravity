#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill archive.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

from quick_validate import print_validation_result, validate_skill
from sync_schema_mirrors import sync_skill

SKIP_DIR_NAMES = {".pytest_cache", "__pycache__"}
SKIP_FILE_NAMES = {".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def should_skip(file_path: Path) -> bool:
    if any(part in SKIP_DIR_NAMES for part in file_path.parts):
        return True
    if file_path.name in SKIP_FILE_NAMES:
        return True
    if file_path.suffix in SKIP_SUFFIXES:
        return True
    return False


def package_skill(skill_path: str | Path, output_dir: str | Path | None = None) -> Path | None:
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"Error: Skill folder not found: {skill_path}")
        return None

    print("Syncing schema mirrors from canonical .agent/schemas/ ...")
    try:
        sync_skill(skill_path)
    except Exception as exc:
        print(f"Schema mirror sync failed: {exc}")
        return None

    print("Validating Antigravity v1.20.3 compliance...")
    validation_result = validate_skill(skill_path)
    print_validation_result(validation_result)
    if not validation_result.valid:
        print("\nValidation failed. Packaging aborted.")
        return None

    skill_name = skill_path.name
    output_path = Path(output_dir).resolve() if output_dir else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)

    skill_filename = output_path / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in sorted(skill_path.rglob("*")):
                if not file_path.is_file() or should_skip(file_path):
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

        print(f"\nSuccessfully packaged to: {skill_filename}")
        print("Tip: Verify discovery in the IDE using: agy --list-skills")
        return skill_filename

    except Exception as exc:
        print(f"Error creating .skill file: {exc}")
        return None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/package_skill.py <path/to/skill-folder> [output-directory]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    package_result = package_skill(skill_path, output_dir)
    sys.exit(0 if package_result else 1)


if __name__ == "__main__":
    main()
