#!/usr/bin/env python3
"""
Quick validation script for Antigravity v1.20.3 skills.
"""

import re
import sys
import yaml
from pathlib import Path

REQUIRED_FRONTMATTER_KEYS = {"description", "version"}
OPTIONAL_FRONTMATTER_KEYS = {"name"}
DEPRECATED_PROPERTIES = {"type", "priority", "scope", "tags", "metadata"}
REQUIRED_XML_BLOCKS = (
    "when_to_use",
    "how_to_use",
    "constraints",
    "resources_reference",
)


def has_xml_block(content, block_name):
    pattern = rf"<{block_name}>\s*.*?\s*</{block_name}>"
    return re.search(pattern, content, re.DOTALL) is not None


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    detected_keys = set(frontmatter.keys())

    if detected_keys.intersection(DEPRECATED_PROPERTIES):
        return False, "CRITICAL: Detected deprecated legacy tags (e.g., type, priority, scope). Remove them for v1.20.3 compliance."

    allowed_properties = REQUIRED_FRONTMATTER_KEYS | OPTIONAL_FRONTMATTER_KEYS
    unexpected_keys = detected_keys - allowed_properties
    if unexpected_keys:
        return False, f"Unexpected key(s) in frontmatter: {', '.join(unexpected_keys)}."

    missing_required = REQUIRED_FRONTMATTER_KEYS - detected_keys
    if missing_required:
        return False, f"Missing required frontmatter key(s): {', '.join(sorted(missing_required))}."

    for block_name in REQUIRED_XML_BLOCKS:
        if not has_xml_block(content, block_name):
            return False, f"Missing required <{block_name}> XML block."

    return True, "Skill is valid and v1.20.3 compliant."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
