#!/usr/bin/env python3
"""
Regenerate the governed skills index in `.agent/skills/`.

role: skills index updater
entrypoints: main
reads: skill markdown files, READMEs
writes: .agent/skills/index.md
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors
coupling: coupled to skill asset and index schemas
determinism: input-dependent
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

import yaml


CATEGORY_ORDER = {
    "issue_artifacts": 0,
    "orchestration_and_authoring": 1,
    "formatting_and_refactoring": 2,
}

FORMATTING_SKILL_IDS = {
    "md060-strict-aligner",
    "python-docsurface-normalizer",
}

NAMING_NOTE = (
    "> Naming note: `asset-rule`, `asset-skill`, and `asset-workflow` are the current "
    "runtime-routed owner-skill family and intentionally use `asset-<asset-family>`. "
    "`artifact-implementation-plan`, `artifact-brainstorm`, `artifact-issue-tracker`, and "
    "`artifact-issue-report` are the current artifact-centric owners and intentionally use "
    "`artifact-<artifact-family>`. Foundational cross-cutting contracts should prefer "
    "`core-<capability>`; `core-schema` is the active schema-authoring contract, and legacy "
    "`dev-schema` requests map to it during the transition. Routing skills should prefer "
    "`*-router`; `agent-asset-router` is active and `agent-artifact-router` is reserved for "
    "future use only. Skills outside the `asset-*`, `artifact-*`, `core-*`, and `*-router` "
    "families remain lowercase hyphen-case."
)


@dataclass
class SkillRecord:
    """
    Represent the generated discovery metadata for one skill asset.
    """

    skill_id: str
    directory_name: str
    description: str
    category: str
    keywords: list[str]
    use_when: list[str]
    best_used_for: str


def repo_root() -> Path:
    """
    Resolve the repository root directory.

    purpose: path resolution base
    """
    return Path(__file__).resolve().parents[4]


def extract_frontmatter(content: str) -> dict:
    """
    Extract and parse YAML frontmatter from Markdown content.

    purpose: metadata extraction
    """
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found.")
    parsed = yaml.safe_load(match.group(1))
    if not isinstance(parsed, dict):
        raise ValueError("Frontmatter must parse to a key-value mapping.")
    return parsed


def extract_tag_block(content: str, block_name: str) -> str | None:
    """
    Extract the content between XML-style tags of a specific name.

    purpose: structural extraction
    """
    pattern = rf"(?ms)^[ \t]*<{block_name}>[ \t]*\r?\n(.*?)^[ \t]*</{block_name}>[ \t]*$"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def parse_fenced_yaml(block_text: str) -> dict | None:
    """
    Extract and parse YAML from a Markdown code fence block.

    purpose: metadata extraction from prose blocks
    """
    fence_match = re.search(r"```yaml\s*\r?\n(.*?)\r?\n```", block_text, re.DOTALL)
    raw_yaml = fence_match.group(1) if fence_match else block_text
    parsed = yaml.safe_load(raw_yaml)
    return parsed if isinstance(parsed, dict) else None


def parse_schema_relationships(readme_path: Path) -> dict | None:
    """
    Parse the schema relationship block from a skill README.

    purpose: schema metadata extraction
    """
    if not readme_path.exists():
        return None
    block = extract_tag_block(readme_path.read_text(encoding="utf-8"), "schema_relationships")
    if block is None:
        return None
    return parse_fenced_yaml(block)


def normalize_sentence(value: str) -> str:
    """
    Collapse whitespace and normalize sentence punctuation.

    purpose: text normalization
    """
    normalized = " ".join(value.split()).strip()
    if normalized and normalized[-1] not in ".!?":
        normalized += "."
    return normalized


def collect_use_when(block_text: str | None) -> list[str]:
    """
    Extract positive trigger bullets from a `<when_to_use>` block.

    purpose: trigger-hint extraction
    """
    if not block_text:
        return []

    entries: list[str] = []
    for raw_line in block_text.splitlines():
        stripped = raw_line.strip()
        if not stripped.startswith("-"):
            continue
        candidate = stripped[1:].strip()
        lowered = candidate.lower()
        if not candidate or lowered.startswith("do not use") or lowered.startswith("example prompt:"):
            continue
        entries.append(normalize_sentence(candidate))
    return entries


def build_keywords(skill_id: str, description: str, category: str, owned_schema_ids: list[str]) -> list[str]:
    """
    Derive deterministic keywords from skill identity and category.

    purpose: manifest keyword generation
    """
    keywords: list[str] = []
    for token in skill_id.split("-"):
        if token and token not in keywords:
            keywords.append(token)

    for schema_id in owned_schema_ids:
        if schema_id and schema_id not in keywords:
            keywords.append(schema_id)

    lowered = description.lower()
    for trigger_word in ("route", "routing", "validate", "validation", "scaffold", "index", "audit", "plan"):
        if trigger_word in lowered and trigger_word not in keywords:
            keywords.append(trigger_word)

    if skill_id.startswith("artifact-") and "artifact-centric-owner" not in keywords:
        keywords.append("artifact-centric-owner")
    if skill_id.startswith("asset-") and "runtime-routed-owner" not in keywords:
        keywords.append("runtime-routed-owner")
    if category == "formatting_and_refactoring" and "refactoring" not in keywords:
        keywords.append("refactoring")
    return keywords


def determine_category(skill_id: str, owned_schema_ids: list[str]) -> str:
    """
    Classify a skill into the generated skills-index categories.

    purpose: category derivation
    """
    if skill_id in FORMATTING_SKILL_IDS:
        return "formatting_and_refactoring"
    if skill_id.startswith("artifact-issue-") or set(owned_schema_ids).intersection({"issue", "issues-tracker"}):
        return "issue_artifacts"
    return "orchestration_and_authoring"


def build_best_used_for(skill_id: str, description: str) -> str:
    """
    Convert a skill description into a concise record summary.

    purpose: record summary generation
    """
    sentence = normalize_sentence(description)
    lowered = sentence.lower()
    if lowered.startswith("serves as"):
        return sentence
    if lowered.startswith("routes"):
        return sentence
    return f"Use this skill for {sentence[0].lower()}{sentence[1:]}" if sentence else f"Use this skill for `{skill_id}`."


def skill_records(skills_dir: Path) -> list[SkillRecord]:
    """
    Discover all skill folders and derive their index records.

    purpose: skill discovery
    """
    records: list[SkillRecord] = []
    for skill_dir in sorted(
        [entry for entry in skills_dir.iterdir() if entry.is_dir() and (entry / "SKILL.md").exists()],
        key=lambda item: item.name.lower(),
    ):
        skill_content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        readme_path = skill_dir / "README.md"
        frontmatter = extract_frontmatter(skill_content)
        description = normalize_sentence(str(frontmatter.get("description", "Skill asset.")))
        when_to_use = collect_use_when(extract_tag_block(skill_content, "when_to_use"))
        schema_relationships = parse_schema_relationships(readme_path) or {}
        owned_schema_ids = schema_relationships.get("owned_schema_ids", [])
        if not isinstance(owned_schema_ids, list):
            owned_schema_ids = []
        owned_schema_ids = [str(item).strip() for item in owned_schema_ids if str(item).strip()]
        skill_id = str(frontmatter.get("name", skill_dir.name)).strip() or skill_dir.name
        category = determine_category(skill_id, owned_schema_ids)
        records.append(
            SkillRecord(
                skill_id=skill_id,
                directory_name=skill_dir.name,
                description=description,
                category=category,
                keywords=build_keywords(skill_id, description, category, owned_schema_ids),
                use_when=when_to_use or [description],
                best_used_for=build_best_used_for(skill_id, description),
            )
        )

    return sorted(records, key=lambda record: (CATEGORY_ORDER.get(record.category, 99), record.skill_id.lower()))


def render_selection_map(records: list[SkillRecord]) -> list[str]:
    """
    Render the selection-map bullets for the skills index.

    purpose: Markdown rendering
    """
    if not records:
        return ["*No skills are currently defined.*"]
    return [f"- `{record.skill_id}`: {record.use_when[0][0].lower()}{record.use_when[0][1:]}" for record in records]


def render_manifest(records: list[SkillRecord]) -> str:
    """
    Render the machine-readable YAML manifest for the skills index.

    purpose: YAML rendering
    """
    manifest = {
        "skills": [
            {
                "id": record.skill_id,
                "definition": f".agent/skills/{record.directory_name}/SKILL.md",
                "category": record.category,
                "implementation": f".agent/skills/{record.directory_name}/",
                "keywords": record.keywords,
                "use_when": record.use_when,
            }
            for record in records
        ]
    }
    return yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False).strip()


def render_records(records: list[SkillRecord]) -> list[str]:
    """
    Render the detailed skill-record sections.

    purpose: Markdown rendering
    """
    if not records:
        return ["*No skills are currently defined.*"]

    lines: list[str] = []
    for record in records:
        lines.extend(
            [
                f"### `{record.skill_id}`",
                "",
                f"- Definition: [`{record.directory_name}/SKILL.md`]({record.directory_name}/SKILL.md)",
                f"- Implementation: [`.agent/skills/{record.directory_name}/`]({record.directory_name})",
                f"- Best used for: {record.best_used_for}",
                "- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.",
                "",
            ]
        )
    return lines[:-1]


def render_category_totals(records: list[SkillRecord]) -> list[str]:
    """
    Render category totals for the generated skills index.

    purpose: count aggregation and rendering
    """
    categories = sorted({record.category for record in records})
    lines = [f"- `{category}`: `{sum(1 for record in records if record.category == category)}`" for category in categories]
    lines.append(f"- `total`: `{len(records)}`")
    return lines


def build_index(records: list[SkillRecord]) -> str:
    """
    Assemble the complete skills index document.

    purpose: full index assembly
    """
    lines = [
        "# Agent Skills Index",
        "",
        "> Consolidated registry of skill assets in `.agent/skills/`.",
        ">",
        "> Scope: discovery, first-pass selection, and quick routing across current skill contracts.",
        ">",
        f"> Total skills: `{len(records)}`",
        ">",
        "> Parent: [`.agent/`](..)",
        ">",
        "> Authority rule: if this index conflicts with a linked skill definition, the linked `SKILL.md` is authoritative.",
        "",
        "## Use This Index",
        "",
        "1. Use the selection map to identify the most likely skill by task intent.",
        "2. Use the manifest to confirm the skill category, definition path, and best-fit use conditions.",
        "3. Open the linked `SKILL.md` before acting whenever exact routing boundaries, execution steps, or validation protocol matter.",
        "",
        NAMING_NOTE,
        "",
        "## Selection Map",
        "",
    ]
    lines.extend(render_selection_map(records))
    lines.extend(
        [
            "",
            "## Manifest",
            "",
            "```yaml",
            render_manifest(records),
            "```",
            "",
            "## Skill Records",
            "",
        ]
    )
    lines.extend(render_records(records))
    lines.extend(
        [
            "",
            "## Category Totals",
            "",
        ]
    )
    lines.extend(render_category_totals(records))
    lines.extend(
        [
            "",
            "## Index Boundaries",
            "",
            "- This file is a discovery and selection aid, not the execution contract for any skill.",
            "- Do not infer trigger boundaries, exact outputs, or validation semantics from the summaries in this index alone.",
            "- When a task depends on exact routing, execution order, or safety protocol, defer to the linked `SKILL.md`.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    """
    Execute the skills index regeneration workflow.

    purpose: entrypoint
    """
    skills_dir = repo_root() / ".agent" / "skills"
    index_path = skills_dir / "index.md"
    records = skill_records(skills_dir)
    with index_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_index(records))
    print("[OK] skills index updated successfully.")


if __name__ == "__main__":
    main()
