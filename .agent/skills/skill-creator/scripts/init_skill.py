#!/usr/bin/env python3
"""
Skill Initializer - Creates a new Antigravity v1.18.3 compliant skill from template

Usage:
    init_skill.py <skill-name> --path <path>
"""

import sys
import shutil
from pathlib import Path

SKILL_TEMPLATE = """---
name: {skill_name}
version: 1.0.0
description: [TODO: Highly specific trigger phrase outlining exact conditions for semantic routing]
---

<when_to_use>
- [TODO: Define explicit scenarios and keywords where this skill should trigger]
</when_to_use>

<how_to_use>
1. **Context Verification (Silent):** [TODO: Initial validation or environment checks]
2. **Execution:** [TODO: Deterministic, actionable steps]
3. **Artifact Generation:** [TODO: Define the explicit verification artifact to be produced]
</how_to_use>

<constraints>
- [TODO: Add strict negative constraints and boundaries]
- Do not utilize blocking synchronous calls if async is available.
</constraints>

<resources_reference>
- `resources/schema/skill.d.ts`
- [TODO: List relative paths to included scripts or resources]
</resources_reference>
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example deterministic script for {skill_name}
"""

def main():
    print("Executing operations for {skill_name}...")
    # TODO: Add deterministic logic here

if __name__ == "__main__":
    main()
'''

EXAMPLE_RESOURCE = """<document_purpose>
This resource file contains heavy domain knowledge or examples referenced by {skill_title}.
It is loaded via progressive disclosure only when specifically requested by the skill.
</document_purpose>

<domain_rules>
[TODO: Add architectural guidelines, schemas, or API contracts here]
</domain_rules>
"""

def title_case_skill_name(skill_name):
    return ' '.join(word.capitalize() for word in skill_name.split('-'))

def init_skill(skill_name, path):
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ Created SKILL.md (v1.18.3 Compliant)")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    try:
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)

        resources_dir = skill_dir / 'resources'
        resources_dir.mkdir(exist_ok=True)
        example_resource = resources_dir / 'reference.md'
        example_resource.write_text(EXAMPLE_RESOURCE.format(skill_title=skill_title))

        # Replicate Schema
        schema_dest_dir = resources_dir / 'schema'
        creator_schema_path = Path(__file__).resolve().parent.parent / 'resources' / 'schema'
        if creator_schema_path.exists():
            shutil.copytree(creator_schema_path, schema_dest_dir, dirs_exist_ok=True)

        print("✅ Created resource directories & integrated schemas")
    except Exception as e:
        print(f"❌ Error creating directories: {e}")
        return None

    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    return skill_dir

def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]
    init_skill(skill_name, path)

if __name__ == "__main__":
    main()
