#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

import yaml

TRIGGER_ORDER = {
    "always_on": 0,
    "glob": 1,
    "manual": 2,
    "auto": 3,
    "@mention": 4,
}

TRIGGER_LABELS = {
    "always_on": "always-on",
    "glob": "glob-scoped",
    "manual": "manual",
    "auto": "auto",
    "@mention": "@mention",
}


@dataclass
class RuleRecord:
    rule_id: str
    filename: str
    description: str
    trigger: str
    priority: str
    execution_tier: str | None
    globs: str | None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def extract_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found.")
    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in frontmatter: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Frontmatter must parse to a key-value mapping.")
    return parsed


def normalize_description(value: str) -> str:
    return " ".join(value.split())


def category_for_trigger(trigger: str) -> str:
    return f"{trigger}_rules"


def build_keywords(record: RuleRecord) -> list[str]:
    tokens = re.split(r"[-_]", record.rule_id.lower())
    keywords = ["rule", record.trigger, record.priority, *[token for token in tokens if token]]
    deduped: list[str] = []
    for keyword in keywords:
        if keyword not in deduped:
            deduped.append(keyword)
    return deduped


def rule_records(rules_dir: Path) -> list[RuleRecord]:
    records: list[RuleRecord] = []
    for path in sorted(rules_dir.glob("*.md"), key=lambda item: item.name.lower()):
        if path.name.lower() == "index.md":
            continue
        content = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        rule_id = str(frontmatter.get("name", path.stem)).strip() or path.stem
        description = normalize_description(str(frontmatter.get("description", "Rule asset.")))
        trigger = str(frontmatter.get("trigger", "")).strip()
        priority = str(frontmatter.get("priority", "")).strip()
        execution_tier = str(frontmatter.get("execution_tier", "")).strip() or None
        globs = str(frontmatter.get("globs", "")).strip() or None
        records.append(
            RuleRecord(
                rule_id=rule_id,
                filename=path.name,
                description=description,
                trigger=trigger,
                priority=priority,
                execution_tier=execution_tier,
                globs=globs,
            )
        )

    return sorted(records, key=lambda record: (TRIGGER_ORDER.get(record.trigger, 99), record.rule_id.lower()))


def render_selection_map(records: list[RuleRecord]) -> list[str]:
    if not records:
        return ["*No rules are currently defined.*"]
    return [f"- `{record.rule_id}`: {record.description}" for record in records]


def render_manifest(records: list[RuleRecord]) -> str:
    manifest_records = []
    for record in records:
        manifest_record: dict[str, object] = {
            "id": record.rule_id,
            "definition": f".agent/rules/{record.filename}",
            "asset_structure": "flat-file",
            "category": category_for_trigger(record.trigger),
            "trigger": record.trigger,
            "priority": record.priority,
            "implementation": f".agent/rules/{record.filename}",
            "keywords": build_keywords(record),
            "use_when": [record.description],
        }
        if record.globs:
            manifest_record["globs"] = record.globs
        manifest_records.append(manifest_record)

    return yaml.safe_dump({"rules": manifest_records}, sort_keys=False, allow_unicode=False).strip()


def render_records(records: list[RuleRecord]) -> list[str]:
    if not records:
        return ["*No rules are currently defined.*"]

    lines: list[str] = [
        "Records are grouped by trigger order (`always_on`, `glob`, `manual`, `auto`, `@mention`) and sorted by rule id within each group.",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"### `{record.rule_id}`",
                "",
                f"- Definition: [`{record.filename}`]({record.filename})",
                f"- Best used for: {record.description}",
                f"- Trigger: `{record.trigger}` ({TRIGGER_LABELS.get(record.trigger, record.trigger)})",
                f"- Priority: `{record.priority}`",
            ]
        )
        if record.globs:
            lines.append(f"- Glob scope: `{record.globs}`")
        if record.execution_tier:
            lines.append(f"- Execution tier: `{record.execution_tier}`")
        lines.extend(
            [
                "- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.",
                "",
            ]
        )

    return lines[:-1]


def render_category_totals(records: list[RuleRecord]) -> list[str]:
    totals: list[str] = []
    for trigger in TRIGGER_ORDER:
        count = sum(1 for record in records if record.trigger == trigger)
        if count:
            totals.append(f"- `{category_for_trigger(trigger)}`: `{count}`")
    totals.append(f"- `total`: `{len(records)}`")
    return totals


def build_index(records: list[RuleRecord]) -> str:
    lines = [
        "# Agent Rules Index",
        "",
        "> Consolidated registry of rule assets in `.agent/rules/`.",
        ">",
        "> Scope: discovery, first-pass selection, and quick routing across reusable rule definitions.",
        ">",
        f"> Total rules: `{len(records)}`",
        ">",
        "> Parent: [`.agent/`](..)",
        ">",
        "> Authority rule: if this index conflicts with a linked rule definition, the linked rule file is authoritative.",
        "",
        "## Use This Index",
        "",
        "1. Use the selection map to identify the most likely rule by trigger context.",
        "2. Use the manifest to confirm the definition path, activation mode, and priority before opening the rule.",
        "3. Open the linked rule definition before relying on exact constraints or verification steps.",
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
            "## Rule Records",
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
            "- This file is a discovery and selection aid, not the execution contract.",
            "- Do not infer exact constraint wording, verification semantics, or override behavior from summaries in this index alone.",
            "- When a task depends on exact trigger scope, priority handling, or behavioral requirements, defer to the linked rule definition.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    rules_dir = repo_root() / ".agent" / "rules"
    index_path = rules_dir / "index.md"
    records = rule_records(rules_dir)
    with index_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_index(records))
    print("[OK] rules index updated successfully.")


if __name__ == "__main__":
    main()
