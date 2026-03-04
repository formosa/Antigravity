---
name: agent-create-issues-tracker
version: 2.0.0
description: Deterministically initializes an Antigravity-compliant Issues Tracker artifact with zero fabricated issues.
---

<when_to_use>

- The user asks to create/initialize a new Issues Tracker document.
- The task needs a fresh defect log for a project/system.
</when_to_use>

<how_to_use>

1. Resolve required parameters from context:
   - `SUBJECT_SYSTEM_NAME`
   - `AUTHOR_NAME`
2. Generate `DOCUMENT_ID` in stable format: `ITR-<UUID4>`.
3. Read template exactly from:
   - `.agent/schemas/issues-tracker/template.md`
4. Perform literal placeholder replacement only:
   - `{{SUBJECT_SYSTEM_NAME}}`
   - `{{DOCUMENT_ID}}`
   - `{{YYYY-MM-DD}}` (ISO date)
   - `{{AUTHOR_NAME}}`
   - `{{TOTAL_ISSUES_COUNT}}` -> `0`
   - `{{RESOLVED_ISSUES_COUNT}}` -> `0`
5. Write the file to the user-requested target path.
6. Return a single concise success line including file path.

If required parameters or template are missing/unreadable, halt and return RFQ.
</how_to_use>

<constraints>
- Never fabricate example issues.
- Preserve template structure and parser headers exactly.
- Do not redesign section layout.
- Keep output concise for token efficiency.
</constraints>

<resources_reference>

- `.agent/schemas/issues-tracker/template.md`
</resources_reference>
