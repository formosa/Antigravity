---
name: artifact-issue-report
version: 1.0.3
description: Serves as the Artifact-Centric Owner for issue-report artifacts by generating canonical standalone issue reports, maintaining or upgrading existing reports, and validating canonical or legacy report integrity against the canonical `issue` contract. Use when the task is to create, modify, migrate, or validate a governed issue report. Do not use when the task is to edit the source Issues Tracker, patch target DDR/spec/YAML files, or rewrite the canonical `issue` schema.
---

<when_to_use>

- Use when the user asks to generate a standalone issue report for one tracked issue.
- Use when the request asks to maintain, refresh, migrate, or validate an existing issue-report artifact.
- Use when the request identifies an `ISSUE_ID` plus an Issues Tracker document and expects a canonical issue report as output.
- Do not use when the task is to edit the source Issues Tracker, redefine `.agent/schemas/issue/`, or implement the underlying repository fix.
- Example prompt: "Generate an issue report for ISSUE-004 from ddr/DDR_v6.3_Issues_Tracker.md and write it to ddr/reports/ISSUE-004.md."
- Example prompt: "Upgrade this legacy issue report to the canonical format and keep it aligned with the current tracker."
- Example prompt: "Validate this issue report and tell me whether it is canonical or legacy."
</when_to_use>

<how_to_use>

## Operating mode

- **Owner subtype:** `Artifact-Centric Owner` for the `issue` artifact family.
- **Owned artifact surface:** a governed issue-report Markdown file at the user-supplied path.
- **Canonical schema authority:** `.agent/schemas/issue/`.
- **Consumed source contract:** `.agent/schemas/issues-tracker/`.
- **Validation surface:** `.agent/skills/artifact-issue-report/scripts/validate_issue_report.py`.

## Deterministic protocol

1. Resolve the inputs and mode before reading deeply:
   - Optional: `MODE` (`auto` by default)
   - `generate` mode when the request is to create a new standalone issue report
   - `maintain` mode when the request is to update, migrate, or repair an existing issue report
   - `validate` mode when the request is to validate an issue report without mutating it
   - Required for `generate`: `ISSUE_ID`, `ISSUES_TRACKER_PATH`, `OUTPUT_PATH`
   - Required for `maintain`: `ISSUE_REPORT_PATH`, `ISSUES_TRACKER_PATH`
   - Required for `validate`: `ISSUE_REPORT_PATH`
   - Optional for `maintain`: `OUTPUT_PATH`, `OVERWRITE_EXISTING` (default `false`)
   - Optional for `generate`: `OVERWRITE_EXISTING` (default `false`)
2. Load the local contract surfaces first:
   - Read `.agent/schemas/issue/README.md` and `.agent/schemas/issue/issue.d.ts`.
   - Read `.agent/schemas/issues-tracker/README.md` and `.agent/schemas/issues-tracker/issues-tracker.d.ts`.
   - Read `resources/schema/issue/README.md` and `resources/schema/issue/issue.d.ts` only as packaged mirrors after consulting the canonical schema.
   - In `generate` or `maintain` mode, read `## ISSUE REGISTRY` first, then `## DOCUMENT METADATA`, before deep-reading issue bodies.
3. Apply hard RFQ or halt gates before mutation:
   - If any required field is missing, halt and return `RFQ` naming the missing field(s).
   - If `ISSUES_TRACKER_PATH` or `ISSUE_REPORT_PATH` is unreadable, halt and return `RFQ` with the exact missing path or error.
   - If `OUTPUT_PATH` already exists and `OVERWRITE_EXISTING` is not explicitly true, halt and request overwrite approval.
   - If `ISSUE_ID` is not present in the tracker registry, halt and return `RFQ` listing valid issue IDs.
   - If `maintain` mode targets an existing report whose embedded issue id does not match the selected tracker issue, halt and return `RFQ` describing the mismatch.
4. Execute `generate` mode when a new issue report is requested:
   - Parse the target issue from the tracker and synthesize the canonical Agent Context fields: `id`, `status`, `severity`, `type`, `tier_refs`, `section_ref`, `rule_refs`, and `updated`.
   - Include `resolved` only when the issue status is `RESOLVED`. Prefer the date from the tracker resolution callout; otherwise fall back to `updated`.
   - Investigate only the smallest decisive set of local files needed to validate the issue. Prefer repo-relative evidence and tracker-cited sources.
   - Read `resources/report-template.md` and `resources/reference.md` before drafting.
   - Generate the canonical two-option report shape with `Option A`, `Option B`, comparative analysis, endorsement, and `### 4. Implementation Note`.
   - Write the report to `OUTPUT_PATH`.
5. Execute `maintain` mode when an existing issue report must be updated:
   - Default `OUTPUT_PATH` to `ISSUE_REPORT_PATH` when an explicit output path is not supplied.
   - Detect whether the existing report is canonical or legacy by using the validator's mode-detection logic.
   - If the report is legacy, upgrade it to the canonical format on first write while preserving the issue identity, historically relevant evidence, and any materially useful strategy narrative that still matches the tracker and local files.
   - Re-read the source tracker issue and the smallest decisive local evidence set, then update the report sections that are stale, unsupported, or structurally non-canonical.
   - Preserve the report's scope as a standalone issue artifact. Do not add tracker-only sections such as `Option C`.
   - Write the updated report to `OUTPUT_PATH`.
6. Execute `validate` mode when the request is to validate an issue report without broader edits:
   - Run `python .agent/skills/artifact-issue-report/scripts/validate_issue_report.py <ISSUE_REPORT_PATH> --mode auto` unless the request explicitly asks for canonical-only or legacy-only validation.
   - Report the exact validator result and any structural failures without mutating the report.
7. Validate every generated or maintained report before success:
   - Run `python .agent/skills/artifact-issue-report/scripts/validate_issue_report.py <TARGET_REPORT_PATH> --mode auto`
   - If validation fails, halt and return `RFQ` with the exact validator failure.
8. Return one concise success line including the written or validated report path.
</how_to_use>

<constraints>
- Do not modify the source Issues Tracker document through this skill.
- Do not patch target DDR/spec/YAML files while creating or maintaining an issue report.
- Do not author or revise `.agent/schemas/issue/` through this skill; canonical schema work belongs to `core-schema`.
- Do not fabricate evidence, tracker fields, line numbers, citations, or validator outcomes.
- Do not emit canonical `Option C` or any extra top-level section beyond the canonical issue-report template.
- Do not leave unresolved placeholders in canonical output.
- Do not hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/` instead.
- Keep skill-local paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>

- Read `.agent/schemas/issue/README.md` to confirm canonical issue-report governance, profiles, and ownership.
- Read `.agent/schemas/issue/issue.d.ts` to verify the active issue-report contract before generating or maintaining a report.
- Read `.agent/schemas/issues-tracker/README.md` to confirm the consumed tracker profile and registry semantics.
- Read `.agent/schemas/issues-tracker/issues-tracker.d.ts` to verify the tracker metadata fields used to synthesize report context.
- Read `resources/report-template.md` to preserve the canonical report section order and required phrasing during generation or migration.
- Read `resources/reference.md` to preserve local evidence, strategy, and implementation-note conventions.
- Read `resources/schema/issue/example.md` to mirror the canonical issue-report structure.
- Read `resources/schema/issue/example-legacy-v4.md` when preserving or upgrading historical report lineage.
- Run `scripts/validate_issue_report.py` to validate canonical or legacy issue reports before returning success.
- Run `scripts/test_validate_issue_report.py` when hardening validator behavior or regression coverage.
</resources_reference>
