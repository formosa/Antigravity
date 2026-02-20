---
type: skill
name: md060-strict-aligner
description: Identifies markdown tables with the MD060/table-column-style violation and repairs them using a local Python script to achieve absolute character-count vertical pipe alignment.
scope: workspace
---

# SKILL: md060-strict-aligner

## Goal

Repair markdown tables violating `MD060/table-column-style` by routing them through a deterministic local formatting script.

## Context & Scope

This skill triggers when you detect malformed markdown tables or encounter linting errors regarding misaligned pipes (`|`). Because LLM tokenization makes manual space-counting unreliable, you MUST use the provided `align_table.py` script to perform the repair.

## Execution Protocol

1. **Identify & Extract:** Locate the target markdown table requiring MD060 repair. Copy the exact text of the malformed table.
2. **Execute Script:** Pipe the copied table text into the `align_table.py` script located in this skill's directory using standard input.
   - *Command Example:* `echo "<table_text>" | python .agent/skills/md060-strict-aligner/align_table.py`
3. **Capture Output:** Read the standard output from the script execution.
4. **Replace:** Replace the malformed markdown table in the original document with the exact standard output from the script.
5. **Verify:** Confirm that the script executed successfully and that the resulting table columns are padded with spaces, with all `|` characters forming perfectly straight vertical lines.

## Directives & Constraints

- NEVER attempt to pad the table columns manually using your own text generation. You MUST use the Python script.
- DO NOT alter the underlying data or semantic meaning of the table cells before passing them to the script.
- IF the script throws an error or the table is fundamentally unparsable: HALT execution immediately, output the error, and request user clarification.
- OUTPUT ONLY the final, repaired markdown table in your response, or commit it directly to the file if operating in an autonomous loop.
