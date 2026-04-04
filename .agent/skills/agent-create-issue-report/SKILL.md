---
name: agent-create-issue-report
version: 1.1.0
description: Routes legacy direct references to `agent-create-issue-report` toward the canonical `artifact-issue-report` owner contract while preserving the historical validator CLI path for compatibility. Use when a task, document, or script explicitly names `agent-create-issue-report` or its validator path. Do not use when the request can target `artifact-issue-report` directly.
---

<when_to_use>

- Use when the request explicitly names `agent-create-issue-report`.
- Use when the request references the legacy validator CLI path under `.agent/skills/agent-create-issue-report/scripts/validate_issue_report.py`.
- Do not use when the request can be expressed directly as `artifact-issue-report` generation, maintenance, or validation work.
- Example prompt: "Use `agent-create-issue-report` to regenerate ISSUE-004 for this tracker."
- Example prompt: "Run the legacy issue-report validator path against this report."
</when_to_use>

<how_to_use>

1. Read `.agent/skills/artifact-issue-report/SKILL.md` first and treat it as the authoritative execution contract.
2. Map the legacy request into the active owner mode:
   - `generate` when the request identifies `ISSUE_ID`, `ISSUES_TRACKER_PATH`, and `OUTPUT_PATH`
   - `maintain` when the request targets an existing issue report plus a tracker
   - `validate` when the request only asks to validate an issue report
3. Hand off to `artifact-issue-report` immediately after resolving the mode. Do not restate or supersede the downstream owner contract.
4. Preserve the historical validator CLI entry point only when a task or external reference explicitly calls the legacy script path:
   - `python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py <ISSUE_REPORT_PATH> --mode auto`
5. Return the downstream owner result unchanged except when clarifying that the legacy entry point was handled through the canonical owner.
</how_to_use>

<constraints>

- Do not maintain an independent procedural contract here; `artifact-issue-report` is the active owner.
- Do not duplicate or fork the canonical validator logic in this shim.
- Do not keep local canonical resource copies such as report templates or reference guidance in this package.
- Do not hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/` instead.
- Keep skill-local paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>

- Read `.agent/skills/artifact-issue-report/SKILL.md` to resolve the active owner mode and follow the canonical issue-report lifecycle.
- Run `scripts/validate_issue_report.py` only when a task explicitly invokes the legacy validator path and needs compatibility preserved.
</resources_reference>
