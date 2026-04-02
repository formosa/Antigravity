---
name: md060-strict-aligner
version: 1.1.1
description: Deterministically aligns Markdown tables to satisfy MD060 with minimal, structure-preserving edits.
---

<when_to_use>

- The user asks to fix MD060 table alignment violations.
- Markdown table formatting must be normalized without content rewrites.
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

- `.agent/skills/md060-strict-aligner/align_table.py`
</resources_reference>
