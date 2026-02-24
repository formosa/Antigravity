#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill archive
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill

def package_skill(skill_path, output_dir=None):
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    print("🔍 Validating Antigravity v1.18.3 compliance...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        return None
    print(f"✅ {message}\n")

    skill_name = skill_path.name
    output_path = Path(output_dir).resolve() if output_dir else Path.cwd()
    output_path.mkdir(parents=True, exist_ok=True)

    skill_filename = output_path / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n✅ Successfully packaged to: {skill_filename}")
        print("💡 Tip: Verify discovery in the IDE using: agy --list-skills")
        return skill_filename

    except Exception as e:
        print(f"❌ Error creating .skill file: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    package_skill(skill_path, output_dir)

if __name__ == "__main__":
    main()
