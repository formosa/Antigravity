#!/usr/bin/env python3
"""
Quick validation script for Antigravity v1.18.3 Skills
"""

import sys
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Strict v1.18.3 Frontmatter Validation
    ALLOWED_PROPERTIES = {'name', 'description'}
    DEPRECATED_PROPERTIES = {'type', 'priority', 'scope', 'tags', 'metadata'}

    detected_keys = set(frontmatter.keys())

    if detected_keys.intersection(DEPRECATED_PROPERTIES):
        return False, "CRITICAL: Detected deprecated legacy tags (e.g., type, priority, scope). Remove them for v1.18.3 compliance."

    unexpected_keys = detected_keys - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, f"Unexpected key(s) in frontmatter: {', '.join(unexpected_keys)}."

    if 'description' not in frontmatter:
        return False, "Missing 'description' (Required for Semantic Routing)"

    # Strict v1.18.3 XML Body Validation
    if '<when_to_use>' not in content or '</when_to_use>' not in content:
        return False, "Missing required <when_to_use> XML block."

    if '<how_to_use>' not in content or '</how_to_use>' not in content:
        return False, "Missing required <how_to_use> XML block."

    return True, "Skill is valid and v1.18.3 compliant!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
