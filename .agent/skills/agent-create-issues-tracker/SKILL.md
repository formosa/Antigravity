---
name: agent-create-issues-tracker
version: 1.0.0
description: Initializes a new blank Issues Tracker from the shared canonical template when the user needs a fresh tracker, not when they want to add issues or generate issue reports.
---

<when_to_use>

- The user asks to create or initialize a new Issues Tracker file.
- The task needs a blank tracker for a project, specification, or system under review.
- Do not use this skill to add issues to an existing tracker or to generate per-issue resolution reports.
</when_to_use>

<how_to_use>

1. Resolve parameters from context:
   - Required: `SUBJECT_SYSTEM_NAME`, `AUTHOR_NAME`, `OUTPUT_PATH`
   - Optional: `SUBJECT_FILE_PATH`, `OVERWRITE_EXISTING` (default `false`)
2. Run pre-flight checks:
   - If any required parameter is missing, halt and return `RFQ` naming the missing field(s).
   - If `OUTPUT_PATH` already exists and `OVERWRITE_EXISTING` is not explicitly true, halt and return `RFQ` requesting overwrite approval.
3. Read the canonical blank template exactly from:
   - `.agent/schemas/issues-tracker/template.md`
4. Perform literal replacement only:
   - `{{SUBJECT_SYSTEM_NAME}}`
   - `{{DOCUMENT_ID}}` -> `ITR-<UUID4>`
   - `{{YYYY-MM-DD}}` -> current ISO date
   - `{{AUTHOR_NAME}}`
   - `{{OPEN_ISSUES_COUNT}}` -> `0`
   - `{{TOTAL_ISSUES_COUNT}}` -> `0`
   - `{{RESOLVED_ISSUES_COUNT}}` -> `0`
5. Write the rendered tracker to `OUTPUT_PATH`.
6. Validate the written file with:
   - `python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py <OUTPUT_PATH> --mode canonical`
7. If validation fails, halt and return `RFQ` with the exact validator failure.
8. Return one concise success line including the output path.

Examples:

- Success:
  - Request: `Initialize an issues tracker for DDR System v7.0 at .agent/assets/proposals/active/v7/DDR_v7_Issues_Tracker.md by Anthony Formosa.`
  - Result: `Issues Tracker initialized: .agent/assets/proposals/active/v7/DDR_v7_Issues_Tracker.md`
- RFQ / refusal:
  - Request: `Recreate the existing tracker at .agent/assets/proposals/active/v6.2/DDR_v6.1_Issues_Tracker.md.`
  - Result: `RFQ: Target file already exists. Explicit overwrite approval is required before replacing it.`
</how_to_use>

<constraints>

- Never fabricate example issues or populate issue entries during initialization.
- Preserve the canonical section headings and table structure from the shared template.
- Do not emit unresolved placeholders.
- Keep the skill scoped to blank tracker initialization only.
- Treat `SUBJECT_FILE_PATH` as optional context; the template must remain fully readable even when it is absent.
</constraints>

<resources_reference>

- `.agent/schemas/issues-tracker/template.md`
- `.agent/schemas/issues-tracker/README.md`
- `.agent/schemas/issues-tracker/example.md`
- `.agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py`
- `.agent/skills/agent-create-issues-tracker/resources/reference.md`
</resources_reference>
