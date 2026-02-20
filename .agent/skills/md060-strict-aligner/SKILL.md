---
type: skill
name: md060-strict-aligner
description: Identifies markdown tables with the MD060/table-column-style violation and repairs them using a local Python script to achieve absolute character-count vertical pipe alignment.
scope: workspace
---

# SKILL: md060-strict-aligner

## Goal

Repair markdown tables violating `MD060/table-column-style` by routing the document through a deterministic local formatting script.

## Context & Scope

This skill triggers when you detect malformed markdown tables or encounter linting errors regarding misaligned pipes (`|`). Because LLM tokenization makes manual space-counting unreliable, you MUST use the provided `align_table.py` script. The script now supports processing entire files autonomously, significantly reducing token overhead and preventing PowerShell pipeline errors.

## Execution Protocol

1. **Locate Target:** Identify the file containing the misaligned markdown table(s).
2. **Execute Autonomous Repair:** run the `align_table.py` script using the `--file` flag with the absolute path to the target file.
   - *Command Example:* `python .agent/skills/md060-strict-aligner/align_table.py --file "c:\absolute\path\to\file.md"`
3. **Verify:** Confirm that the script executed successfully. Check the file to ensure that all table columns are padded correctly, with all `|` characters forming perfectly straight vertical lines, even within blockquotes or nested lists.

## Directives & Constraints

- ALWAYS prioritize the `--file` flag over piping text via `stdin`. This prevents data corruption from shell escaping issues and reduces token usage.
- The script automatically handles document-wide processing; it will identify and align all table blocks in the file while leaving non-table text (paragraphs, code blocks) untouched.
- DO NOT attempt to pad the table columns manually using your own text generation. You MUST use the Python script.
- IF the script throws an error: HALT execution immediately, output the error, and request user clarification.