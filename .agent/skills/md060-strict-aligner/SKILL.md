---
name: md060-strict-aligner
version: 1.1.2
description: Deterministically aligns Markdown tables to satisfy MD060 with minimal, structure-preserving edits. Use when the task is to fix table alignment violations without changing prose or table meaning. Do not use when the request requires broader Markdown rewrites or non-table content changes.
---

<when_to_use>

- The user asks to fix MD060 table alignment violations.
- Markdown table formatting must be normalized without content rewrites.
- Do not use this skill when the request is to rewrite Markdown prose, change headings, or refactor non-table structure.
- Example prompt: "Fix the MD060 table alignment errors in this README."
- Example prompt: "Normalize the tables in docs/spec.md without changing any text content."
</when_to_use>

<how_to_use>

1. Identify the markdown file(s) and target tables.
2. Run the aligner script for deterministic formatting.
3. Re-run lint/check to confirm MD060 passes.
4. Report exact files changed and lint result.

If the file has malformed table syntax that cannot be safely aligned, halt and request clarification.
</how_to_use>

<constraints>
- Never alter non-table prose.
- Never change table semantic content.
- Keep edits minimal for token and diff efficiency.
</constraints>

<resources_reference>

- Run `.agent/skills/md060-strict-aligner/align_table.py` to apply deterministic table alignment without rewriting non-table prose.
</resources_reference>
