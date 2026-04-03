#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

import yaml


@dataclass
class WorkflowRecord:
    workflow_id: str
    filename: str
    description: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def extract_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def workflow_records(workflows_dir: Path) -> list[WorkflowRecord]:
    records: list[WorkflowRecord] = []
    for path in sorted(workflows_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        content = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        workflow_id = str(frontmatter.get("name", path.stem)).strip() or path.stem
        description = " ".join(str(frontmatter.get("description", "Workflow asset.")).split())
        records.append(WorkflowRecord(workflow_id=workflow_id, filename=path.name, description=description))
    return records


def render_selection_map(records: list[WorkflowRecord]) -> list[str]:
    if not records:
        return ["*No workflows are currently defined.*"]
    return [f"- `{record.workflow_id}`: {record.description}" for record in records]


def render_manifest(records: list[WorkflowRecord]) -> str:
    workflows = []
    for record in records:
        workflows.append(
            {
                "id": record.workflow_id,
                "definition": f".agent/workflows/{record.filename}",
                "asset_structure": "flat-file",
                "category": "workflow_assets",
                "keywords": ["workflow", "steps", "verification"],
                "use_when": [record.description],
            }
        )
    manifest = {"workflows": workflows}
    return yaml.safe_dump(manifest, sort_keys=False, allow_unicode=False).strip()


def render_records(records: list[WorkflowRecord]) -> list[str]:
    if not records:
        return ["*No workflows are currently defined.*"]

    lines: list[str] = []
    for record in records:
        lines.extend(
            [
                f"### `{record.workflow_id}`",
                "",
                f"- Definition: [`{record.filename}`]({record.filename})",
                f"- Best used for: {record.description}",
                "- Open the linked definition when exact execution order, verification criteria, or safety boundaries matter.",
                "",
            ]
        )
    return lines[:-1]


def render_category_totals(records: list[WorkflowRecord]) -> list[str]:
    return [
        f"- `workflow_assets`: `{len(records)}`",
        f"- `total`: `{len(records)}`",
    ]


def build_index(records: list[WorkflowRecord]) -> str:
    lines = [
        "# Agent Workflows Index",
        "",
        "> Consolidated registry of workflow assets in `.agent/workflows/`.",
        ">",
        "> Scope: discovery, first-pass selection, and quick routing across reusable workflow definitions.",
        ">",
        f"> Total workflows: `{len(records)}`",
        ">",
        "> Parent: [`.agent/`](..)",
        ">",
        "> Authority rule: if this index conflicts with a linked workflow definition, the linked workflow file is authoritative.",
        "",
        "## Use This Index",
        "",
        "1. Use the selection map to identify the most likely workflow by intent.",
        "2. Use the manifest to confirm the definition path and basic fit before opening the workflow.",
        "3. Open the linked workflow definition before execution whenever exact steps, verification, or safety boundaries matter.",
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
            "## Workflow Records",
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
            "- Do not infer exact outputs, side effects, or approval checkpoints from this index alone.",
            "- When a task depends on exact sequence, verification, or review gates, defer to the linked workflow definition.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    workflows_dir = repo_root() / ".agent" / "workflows"
    index_path = workflows_dir / "index.md"
    records = workflow_records(workflows_dir)
    with index_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_index(records))
    print("[OK] workflow index updated successfully.")


if __name__ == "__main__":
    main()
