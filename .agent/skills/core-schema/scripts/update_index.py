#!/usr/bin/env python3
"""
Update the consolidated registry of core schemas.

role: schema index updater
entrypoints: main
reads: core schema READMEs, config.json
writes: index.md
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors; config missing
coupling: coupled to core schema and index schemas
determinism: input-dependent
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


def extract_tag_block(content: str, block_name: str) -> str | None:
    """
    Extract the content between XML-style tags of a specific name.

    purpose: structural extraction
    """
    pattern = rf"(?ms)^[ \t]*<{block_name}>[ \t]*\r?\n(.*?)^[ \t]*</{block_name}>[ \t]*$"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def parse_history_version(content: str) -> str:
    """
    Extract the latest version from the modification history table.

    purpose: metadata extraction
    """
    block = extract_tag_block(content, "modification_history")
    if not block:
        return "1.0.0"
    table_lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return "1.0.0"
    last_row = [part.strip() for part in table_lines[-1].strip().strip("|").split("|")]
    return last_row[1] if len(last_row) >= 2 else "1.0.0"


def parse_owner_skill(content: str) -> str:
    """
    Extract the primary owner skill from the schema governance block.

    purpose: authority extraction
    """
    block = extract_tag_block(content, "schema_governance")
    if not block:
        return "unknown"
    fence_match = re.search(r"```yaml\s*\r?\n(.*?)\r?\n```", block, re.DOTALL)
    raw_yaml = fence_match.group(1) if fence_match else block
    try:
        parsed = yaml.safe_load(raw_yaml)
    except yaml.YAMLError:
        return "unknown"
    if not isinstance(parsed, dict):
        return "unknown"
    return str(parsed.get("primary_owner_skill", "unknown"))


def parse_description(content: str) -> str:
    """
    Identify a suitable description for the schema from its README.

    purpose: UI/prose extraction
    """
    document_purpose = extract_tag_block(content, "document_purpose")
    if document_purpose:
        return " ".join(document_purpose.split())

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "<", "|", "```", "- ")):
            continue
        return line
    return "Schema definition."


def main():
    """
    Execute the core schema index update workflow.

    purpose: entrypoint
    """
    config_path = Path(__file__).parent.parent / "config.json"
    repo_root = Path(__file__).resolve().parents[4]
    schemas_dir = repo_root / ".agent" / "schemas"
    if config_path.exists():
        configured = json.loads(config_path.read_text()).get("default_schema_location", str(schemas_dir))
        configured_path = Path(configured)
        schemas_dir = (repo_root / configured_path).resolve() if not configured_path.is_absolute() else configured_path

    index_md = schemas_dir / "index.md"
    lines = [
        "# SCHEMA DIRECTORY INDEX\n",
        "| Schema Name | Version | Primary Skill | Description |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for schema_dir in sorted([entry for entry in schemas_dir.iterdir() if entry.is_dir()], key=lambda item: item.name):
        readme_path = schema_dir / "README.md"
        if readme_path.exists():
            readme_content = readme_path.read_text(encoding="utf-8")
            version = parse_history_version(readme_content)
            owner_skill = parse_owner_skill(readme_content)
            description = parse_description(readme_content)
        else:
            version = "1.0.0"
            owner_skill = "unknown"
            description = "Schema definition."

        lines.append(f"| {schema_dir.name} | {version} | {owner_skill} | {description} |")

    index_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("[OK] index.md updated successfully.")


if __name__ == "__main__":
    main()
