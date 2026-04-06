#!/usr/bin/env python3
"""
Sync vendored skill-local schema mirrors from canonical .agent/schemas/ directories.

role: schema mirror synchronization utility
entrypoints: main
reads: skill README, canonical schemas
writes: skill-local schema mirrors
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors; schema missing
coupling: coupled to skill README and schema structure
determinism: deterministic
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

REQUIRED_SCHEMA_RELATIONSHIP_KEYS = {
    "schema_of_this_skill",
    "owned_schema_ids",
    "consumed_schema_ids",
    "mirror_root",
    "mirror_policy",
}


def extract_tag_block(content: str, block_name: str) -> str | None:
    """
    Extract the content between XML-style tags of a specific name.

    purpose: structural extraction
    """
    pattern = rf"(?ms)^[ \t]*<{block_name}>[ \t]*\r?\n(.*?)^[ \t]*</{block_name}>[ \t]*$"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def repo_root() -> Path:
    """
    Resolve the repository root directory.

    purpose: path resolution base
    """
    return Path(__file__).resolve().parents[4]


def parse_schema_relationships(skill_path: Path) -> dict:
    """
    Extract and validate the schema relationship mapping from the skill README.

    purpose: metadata extraction
    """
    readme_path = skill_path / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError(f"Skill README not found: {readme_path}")

    content = readme_path.read_text(encoding="utf-8")
    block = extract_tag_block(content, "schema_relationships")
    if block is None:
        raise ValueError(f"README is missing <schema_relationships>: {readme_path}")

    fence_match = re.search(r"```yaml\s*\r?\n(.*?)\r?\n```", block, re.DOTALL)
    raw_yaml = fence_match.group(1) if fence_match else block
    parsed = yaml.safe_load(raw_yaml)
    if not isinstance(parsed, dict):
        raise ValueError(f"<schema_relationships> must parse to a YAML mapping: {readme_path}")

    keys = set(parsed.keys())
    missing = REQUIRED_SCHEMA_RELATIONSHIP_KEYS - keys
    unexpected = keys - REQUIRED_SCHEMA_RELATIONSHIP_KEYS
    if missing:
        raise ValueError(f"<schema_relationships> is missing keys: {', '.join(sorted(missing))}")
    if unexpected:
        raise ValueError(f"<schema_relationships> has unexpected keys: {', '.join(sorted(unexpected))}")

    if parsed["schema_of_this_skill"] != "skill":
        raise ValueError("`schema_of_this_skill` must be `skill`.")

    for field_name in ("owned_schema_ids", "consumed_schema_ids"):
        field_value = parsed[field_name]
        if not isinstance(field_value, list) or not all(isinstance(item, str) and item.strip() for item in field_value):
            raise ValueError(f"`{field_name}` must be a list of non-empty schema IDs.")

    if parsed["mirror_root"] != "resources/schema/":
        raise ValueError("`mirror_root` must be `resources/schema/`.")

    if parsed["mirror_policy"] != "read-only-derived-from-.agent/schemas":
        raise ValueError("`mirror_policy` must be `read-only-derived-from-.agent/schemas`.")

    return parsed


def collect_required_schema_ids(schema_relationships: dict) -> list[str]:
    """
    Amalgamate all required schema IDs into a unique list.

    purpose: schema ID collection
    """
    schema_ids: list[str] = []
    for schema_id in [
        schema_relationships["schema_of_this_skill"],
        *schema_relationships["owned_schema_ids"],
        *schema_relationships["consumed_schema_ids"],
    ]:
        if schema_id not in schema_ids:
            schema_ids.append(schema_id)
    return schema_ids


def sync_skill(skill_path: str | Path) -> list[str]:
    """
    Synchronize the local schema mirror directory with canonical source headers.

    purpose: schema mirror synchronization
    preconditions: skill folder and README exist
    postconditions: returns list of synced schema IDs
    mutates: filesystem (overwrites mirrors)
    reads: filesystem (canonical schemas)
    writes: filesystem (mirrors)
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: process-local
    """
    skill_dir = Path(skill_path).resolve()
    if not (skill_dir / "SKILL.md").exists():
        raise FileNotFoundError(f"Not a skill directory: {skill_dir}")

    relationships = parse_schema_relationships(skill_dir)
    required_schema_ids = collect_required_schema_ids(relationships)
    canonical_root = repo_root() / ".agent" / "schemas"
    mirror_root = skill_dir / Path(relationships["mirror_root"].rstrip("/"))
    mirror_root.mkdir(parents=True, exist_ok=True)

    for child in list(mirror_root.iterdir()):
        if child.is_file():
            child.unlink()
        elif child.is_dir() and child.name not in required_schema_ids:
            shutil.rmtree(child)

    for schema_id in required_schema_ids:
        source_dir = canonical_root / schema_id
        target_dir = mirror_root / schema_id
        if not source_dir.exists():
            raise FileNotFoundError(f"Canonical schema directory not found: {source_dir}")
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)

    return required_schema_ids


def iter_skill_dirs(skills_root: Path) -> list[Path]:
    """
    Identify all candidate skill directories within a root folder.

    purpose: skill discovery
    """
    return sorted(
        [entry for entry in skills_root.iterdir() if entry.is_dir() and (entry / "SKILL.md").exists()],
        key=lambda item: item.name,
    )


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for schema synchronization.

    purpose: CLI configuration extraction
    """
    parser = argparse.ArgumentParser(description="Sync skill-local schema mirrors from canonical .agent/schemas/ directories.")
    parser.add_argument("skill_paths", nargs="*", help="Skill directory paths.")
    parser.add_argument("--all", action="store_true", help="Sync every skill under .agent/skills/.")
    return parser.parse_args()


def main() -> None:
    """
    Execute the schema synchronization workflow from CLI.

    purpose: entrypoint
    """
    args = parse_args()
    if args.all:
        skills_root = Path(args.skill_paths[0]).resolve() if args.skill_paths else repo_root() / ".agent" / "skills"
        skill_dirs = iter_skill_dirs(skills_root)
    else:
        if not args.skill_paths:
            print("Usage: python sync_schema_mirrors.py <skill_directory> [<skill_directory> ...] [--all]")
            sys.exit(1)
        skill_dirs = [Path(path).resolve() for path in args.skill_paths]

    for skill_dir in skill_dirs:
        synced_ids = sync_skill(skill_dir)
        print(f"Synced {skill_dir.name}: {', '.join(synced_ids)}")


if __name__ == "__main__":
    main()
