---
name: agent-create-issue-report
version: 1.0.2
description: Generates a standalone v6.1-style Resolution Report for one tracked issue from an Antigravity Issues Tracker. Use when the task is to investigate a single `ISSUE_ID` and write a validator-checked report artifact. Do not use when the task is to edit the tracker itself or implement the fix.
---

<when_to_use>

- The user asks to investigate a tracked issue and produce a Resolution Report artifact.
- The request identifies or implies a single `ISSUE_ID` plus an Issues Tracker document.
- Use this skill for report authoring only, not for fixing the issue or editing the tracker.
- Example prompt: "Generate a resolution report for ISSUE-004 from ddr/DDR_v6.3_Issues_Tracker.md and write it to ddr/reports/ISSUE-004.md."
- Example prompt: "Audit ISSUE-009 in this tracker and produce a standalone issue report artifact."
</when_to_use>

<how_to_use>

1. Resolve parameters from context:
   - Required: `ISSUE_ID`, `ISSUES_TRACKER_PATH`, `OUTPUT_PATH`
   - Optional: `OVERWRITE_EXISTING` (default `false`)
2. Run pre-flight checks before reading deeply:
   - If any required parameter is missing, halt and return `RFQ` naming the missing field(s).
   - If `ISSUES_TRACKER_PATH` is unreadable, halt and return `RFQ` with the exact error.
   - If `OUTPUT_PATH` already exists and overwrite was not explicitly requested, halt and return `RFQ` requesting overwrite approval.
3. Parse the tracker in this order:
   - Read `## ISSUE REGISTRY` first and confirm `ISSUE_ID` exists. If not, halt and return `RFQ` listing valid issue IDs.
   - Read `## DOCUMENT METADATA` and resolve `subject`, `format_version`, `target_platform`, and `target_model`.
   - Read the target issue block from `## ISSUES`.
   - Support both tracker layouts:
     - Canonical `v6.x`: issue heading, `Status/Severity/Type` metadata line, `Tiers Affected/Spec Section` metadata line, numbered subsections, and optional resolution callout.
     - Legacy `v4/v5`: same issue content plus `AGENT_CONTEXT` YAML when present.
4. Synthesize canonical Agent Context for the report:
   - Always include `id`, `status`, `severity`, `type`, `tier_refs`, `section_ref`, `rule_refs`, and `updated`.
   - Set `updated` to the report generation date.
   - Include `resolved` only when the issue status is `RESOLVED`. Prefer the date from the tracker resolution callout; otherwise fall back to `updated`.
5. Investigate only the smallest decisive set of local files needed to validate the issue:
   - Start with the files and sections named by the tracker.
   - Cite repo-relative paths with line spans, not absolute machine paths.
   - Quote only the minimum text needed to support each finding.
   - If no corroborating project files are found, say so explicitly and rely on tracker evidence only.
6. Read these resources before drafting:
   - `.agent/skills/agent-create-issue-report/resources/report-template.md`
   - `.agent/skills/agent-create-issue-report/resources/reference.md`
7. Generate the report exactly from the shared template:
   - Use the canonical `v6.1` report shape with exactly two options: `Option A` and `Option B`.
   - Frontmatter must include `created`, `updated`, and conditional `resolved`.
   - `### Agent Context` must be a fenced YAML block using the synthesized canonical fields.
   - Keep the optional tracker resolution callout only when the tracker provides one.
   - Keep a `* **Citations:**` line under both options. If no authoritative source materially supports an option, use the exact sentence `No authoritative external reference identified for this specific claim.`
   - `### 4. Implementation Note` is always required:
     - If the issue is `RESOLVED`, summarize the implemented change and the validation evidence that confirms the resolution.
     - Otherwise, state clearly that implementation remains pending and that the report itself did not apply a repository patch.
8. Use authoritative external research only when it materially improves the strategy comparison:
   - Prefer official standards, RFCs, formal specifications, or vendor documentation.
   - Keep to 1-2 primary citations per option when possible.
9. Write the report to `OUTPUT_PATH`, then validate it with:
   - `python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py <OUTPUT_PATH> --mode canonical`
10. If validation fails, halt and return `RFQ` with the exact validator failure.
11. Return one concise success line including the written path.

Examples:

- Success:
  - Request: `Generate a report for ISSUE-001 from .agent/assets/proposals/active/v6.2/DDR_v6.1_Issues_Tracker.md and write it to .agent/assets/proposals/active/v6.2/DDR_v6.1_Issue-001.md.`
  - Result: `Resolution Report generated: .agent/assets/proposals/active/v6.2/DDR_v6.1_Issue-001.md`
- RFQ / refusal:
  - Request: `Regenerate ISSUE-001 at .agent/assets/proposals/active/v6.2/DDR_v6.1_Issue-001.md.`
  - Result: `RFQ: Target file already exists. Explicit overwrite approval is required before replacing it.`
</how_to_use>

<constraints>

- Do not modify the source Issues Tracker document.
- Do not implement the fix while generating the report.
- Do not fabricate evidence, line numbers, citations, or project findings.
- Do not emit `Option C` or any extra top-level section beyond the canonical template.
- Do not emit unresolved placeholders.
- Prefer repo-relative paths in the audit narrative and implementation note.
- Keep the report self-contained, evidence-first, and concise.
</constraints>

<resources_reference>

- Read `.agent/skills/agent-create-issue-report/resources/report-template.md` to preserve the canonical report section order and required phrasing.
- Read `.agent/skills/agent-create-issue-report/resources/reference.md` to align the report with local issue-report conventions and evidence expectations.
- Read `resources/schema/issue/README.md` to confirm the issue artifact purpose and field semantics before drafting.
- Read `resources/schema/issue/example.md` to mirror the canonical issue artifact structure and section naming.
- Read `resources/schema/issue/issue.d.ts` to verify the required issue frontmatter and body contract.
- Run `.agent/skills/agent-create-issue-report/scripts/validate_issue_report.py` to validate the written report before returning success.
</resources_reference>
