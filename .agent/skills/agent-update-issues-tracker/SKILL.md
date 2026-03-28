---
name: agent-update-issues-tracker
description: Reevaluate and update an existing Issues Tracker against its target DDR or specification files and related local audits. Use when Codex must validate `OPEN` issues, refine issue evidence and wording, add a distinct `Option C`, add comparative analysis and an endorsed recommendation, attach authoritative web citations, migrate a tracker from `IT-1.0` to `IT-1.1`, or append newly discovered significant issues without modifying the target YAML or spec files.
---

<when_to_use>
- The user asks to update, refresh, reevaluate, maintain, expand, or migrate an existing Issues Tracker.
- The task references an existing tracker plus target YAML/spec files, local audits, local issue reports, or other repo documents that may contain issue leads.
- The task requires validating existing `OPEN` issues, adding `Option C`, adding a comparative analysis, endorsing one strategy, or attaching authoritative online citations directly inside the tracker.
- Do not use this skill to initialize a blank tracker or to generate a standalone issue report artifact.
</when_to_use>

<how_to_use>
1. Resolve inputs from context:
   - Required: `ISSUES_TRACKER_PATH`
   - Optional: `TARGET_FILE_PATHS`, `REFERENCE_DOC_PATHS`, `ISSUE_IDS`
2. Run pre-flight checks before deep analysis:
   - If `ISSUES_TRACKER_PATH` is missing or unreadable, halt and return `RFQ` with the exact missing path or error.
   - Read `## ISSUE REGISTRY` first, then `## DOCUMENT METADATA`, before reading issue bodies.
   - Determine run mode:
     - Full mode: `ISSUE_IDS` omitted. Process every `OPEN` issue and perform new-issue discovery.
     - Filtered mode: `ISSUE_IDS` provided. Process only those issue IDs and skip broad new-issue discovery.
3. Resolve the local evidence base:
   - Use explicit `TARGET_FILE_PATHS` when provided.
   - Otherwise infer sibling target files from the tracker directory and subject version. Prefer nearby `ddr_node_schema*.yaml` and `ddr_system*.yaml`.
   - Load explicit `REFERENCE_DOC_PATHS`.
   - Also inspect same-directory `*Issue_Identification_Audit*.md`, matching per-issue report files, and any local paths already cited by the tracker.
4. Upgrade the tracker contract on first write when needed:
   - If `document.format_version` is `IT-1.0`, migrate the tracker to `IT-1.1`.
   - Update `document.format_version`, the footer banner, the embedded `## ISSUE SCHEMA`, and the `## RESOLUTION WORKFLOW` so they match the `IT-1.1` contract.
   - Ensure every populated issue block contains:
     - `Resolution-[NNN]: Option C - ...`
     - `Comparative Analysis-[NNN]`
     - `Recommendation-[NNN]`
     - `Supporting Citations-[NNN]`
5. Revalidate each selected existing issue against decisive local evidence:
   - Investigate the claims against the target YAML/spec files first.
   - Use repo-local audits or issue reports to widen, narrow, or confirm the issue only when they are supported by the target files.
   - Run local schema probes when they materially confirm or disprove a claim. Keep those probes scratch-only; do not modify repo-tracked target files.
   - Rewrite `Problem Statement`, `Evidence & Justification`, `Impact Assessment`, and `Notes` only as needed to make them technically accurate, sufficiently detailed, and internally consistent.
   - Preserve existing `Option A` and `Option B` unless they are factually wrong, materially incomplete, or no longer distinct.
6. Add strategy comparison and recommendation content for each selected issue:
   - Add a genuinely distinct `Option C`. It must differ materially from `Option A` and `Option B`, not just reword the same design decision.
   - Add `Comparative Analysis-[NNN]` comparing the blast radius, compatibility implications, enforcement strength, and implementation complexity of Options A, B, and C.
   - Add `Recommendation-[NNN]` with exactly one endorsed option using this structure:
     - `**Endorsed Option:** \`Option A|B|C\``
     - one or more concise paragraphs explaining the technical rationale
   - Add `Supporting Citations-[NNN]` as 1-3 single-line bullets in this form:
     - `- [Source Name](https://example.com): One-line explanation of why the source supports the endorsed option.`
   - Use recent authoritative web sources for recommendation support. Prefer official specifications, standards bodies, primary vendor documentation, or other primary authoritative references.
7. Discover new issues in full mode only:
   - Review the target files and referenced local documents for significant concerns not already tracked.
   - Add a new issue only when the concern is materially supported, technically important, and not a trivial duplicate or narrow restatement of an existing issue.
   - When a referenced document presents a possible issue, investigate it against the target files before adding it.
8. Rebuild tracker bookkeeping after edits:
   - Update registry rows and sort them by severity then issue number.
   - Update dependency-map rows when new or revised dependencies are materially supported.
   - Refresh `document.last_modified`, footer date, `open_issues`, and `resolved_issues`.
   - Count `open_issues` as `OPEN` plus `IN_REVIEW`. Count `resolved_issues` as `RESOLVED`.
   - Keep statuses conservative. Do not mark issues `RESOLVED` unless the user explicitly expands scope.
9. Validate the final tracker:
   - Run `python .agent/skills/agent-update-issues-tracker/scripts/validate_updated_issues_tracker.py <ISSUES_TRACKER_PATH>`
   - If validation fails, halt and return `RFQ` with the exact validator failure.
10. Return one concise success line including the updated tracker path.

Examples:

- Full mode:
  - Request: `Update .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md against the v6.2 DDR YAML files and refresh all open issues.`
  - Result: `Issues Tracker updated: .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md`
- Filtered mode:
  - Request: `Refresh ISSUE-004 and ISSUE-009 in .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md using the sibling audit files.`
  - Result: `Issues Tracker updated: .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md`
</how_to_use>

<constraints>
- Never patch the target DDR YAML/spec files. This skill is tracker-analysis and tracker-update only.
- Never fabricate evidence, schema-probe outcomes, issue IDs, citations, or local file references.
- Never broaden a filtered run into broad new-issue discovery.
- Never add `Option C` if it is a near-copy of Option A or Option B.
- Keep the embedded `## ISSUE SCHEMA` and `## RESOLUTION WORKFLOW` synchronized with the `IT-1.1` format when a tracker is migrated.
- Preserve unrelated issue content; update only what the evidence requires.
</constraints>

<resources_reference>
- `.agent/schemas/issues-tracker/README.md`
- `.agent/schemas/issues-tracker/issues-tracker.d.ts`
- `.agent/schemas/issues-tracker/example-it-1.1.md`
- `.agent/skills/agent-update-issues-tracker/resources/reference.md`
- `.agent/skills/agent-update-issues-tracker/scripts/validate_updated_issues_tracker.py`
- `.agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md`
- `.agent/assets/proposals/active/v6.3/DDR_v6.2_Issue_Identification_Audit-2.md`
</resources_reference>
