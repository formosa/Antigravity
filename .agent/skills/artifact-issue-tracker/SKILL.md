---
name: artifact-issue-tracker
version: 1.0.3
description: Serves as the Artifact-Centric Owner for Issues Tracker artifacts by initializing blank `IT-1.0` trackers, refreshing and migrating populated trackers to `IT-1.1`, and validating or auditing tracker integrity against the canonical `issues-tracker` contract. Use when the task is to create, maintain, validate, or audit a governed Issues Tracker. Do not use when the task is to generate a standalone issue report, rewrite the canonical tracker schema, or patch target YAML or spec files.
---

<when_to_use>

- The user asks to create, initialize, seed, validate, audit, refresh, reevaluate, maintain, expand, or migrate an Issues Tracker.
- The task needs a blank tracker generated from the canonical `IT-1.0` template.
- The task references an existing tracker plus target YAML/spec files, local audits, local issue reports, or other repo documents that may contain issue leads.
- The task requires validating existing `OPEN` issues, adding `Option C`, adding a comparative analysis, endorsing one strategy, or attaching authoritative online citations directly inside the tracker.
- The task is to validate or audit a tracker artifact without changing the target DDR/spec sources.
- Do not use this skill to generate a standalone issue report artifact; route that work to `artifact-issue-report`.
- Do not use this skill to redefine `.agent/schemas/issues-tracker/`; route schema-authoring changes to `core-schema`.
- Do not use this skill to patch target YAML or spec files.
- Example prompt: "Initialize an issues tracker for DDR System v7.0 at ddr/DDR_v7_Issues_Tracker.md by Anthony Formosa."
- Example prompt: "Refresh ISSUE-004 and ISSUE-009 in ddr/DDR_v6.3_Issues_Tracker.md using the sibling DDR YAML files."
- Example prompt: "Validate this issues tracker and tell me whether it is already `IT-1.1` compliant."

</when_to_use>

<how_to_use>

## Operating mode

- **Owner subtype:** `Artifact-Centric Owner` for the `issues-tracker` artifact family.
- **Owned artifact surface:** a governed Issues Tracker Markdown file at the user-supplied path.
- **Canonical schema authority:** `.agent/schemas/issues-tracker/`.
- **Validation surfaces:** `.agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py` and `.agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py`.

## Deterministic protocol

1. Resolve inputs and run mode before mutation:
   - Optional: `MODE` (`auto` by default)
   - `initialize` mode when the request is to create a blank tracker
   - `maintain` mode when the request is to refresh, migrate, or expand an existing tracker
   - `validate` mode when the request is to validate or audit tracker structure without substantive content edits
   - Required for `initialize`: `SUBJECT_SYSTEM_NAME`, `AUTHOR_NAME`, `OUTPUT_PATH`
   - Required for `maintain` or `validate`: `ISSUES_TRACKER_PATH`
   - Optional for `maintain` or `validate`: `TARGET_FILE_PATHS`, `REFERENCE_DOC_PATHS`, `ISSUE_IDS`
   - Optional for `initialize`: `SUBJECT_FILE_PATH`, `OVERWRITE_EXISTING` (default `false`)
2. Load the local contract surfaces first:
   - Read `.agent/schemas/issues-tracker/README.md` and `.agent/schemas/issues-tracker/issues-tracker.d.ts`.
   - Read `resources/schema/issues-tracker/README.md` and `resources/schema/issues-tracker/issues-tracker.d.ts` only as packaged mirrors after consulting the canonical schema.
   - In `initialize` mode, read `resources/schema/issues-tracker/template.md` and `resources/schema/issues-tracker/example.md`.
   - In `maintain` or `validate` mode, read `## ISSUE REGISTRY` first, then `## DOCUMENT METADATA`, before deep-reading issue bodies.
3. Apply hard RFQ or halt gates before mutation:
   - If any required field is missing, halt and return `RFQ` naming the missing field(s).
   - If `OUTPUT_PATH` already exists in `initialize` mode and `OVERWRITE_EXISTING` is not explicitly true, halt and request overwrite approval.
   - If `ISSUES_TRACKER_PATH` is missing or unreadable, halt and return `RFQ` with the exact missing path or error.
   - If the request asks to redefine `.agent/schemas/issues-tracker/` and edit a tracker artifact in the same pass, halt and route schema work through `core-schema` first.
   - If the request asks for a standalone single-issue report, halt and route the task to `artifact-issue-report`.
4. Execute `initialize` mode when a blank tracker is requested:
   - Read the canonical blank template exactly from `resources/schema/issues-tracker/template.md`.
   - Perform literal replacement only:
     - `{{SUBJECT_SYSTEM_NAME}}`
     - `{{DOCUMENT_ID}}` -> `ITR-<UPPERCASE-HYPHENATED-SUBJECT-SLUG>`
       where `SUBJECT_SYSTEM_NAME` is normalized by uppercasing alphanumeric tokens, replacing punctuation and whitespace with hyphens, collapsing repeated hyphens, and trimming leading or trailing hyphens
     - `{{YYYY-MM-DD}}` -> current ISO date
     - `{{AUTHOR_NAME}}`
     - `{{OPEN_ISSUES_COUNT}}` -> `0`
     - `{{TOTAL_ISSUES_COUNT}}` -> `0`
     - `{{RESOLVED_ISSUES_COUNT}}` -> `0`
   - Write the rendered tracker to `OUTPUT_PATH`.
   - Validate with `python .agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py <OUTPUT_PATH> --mode canonical`.
5. Execute `maintain` mode when an existing tracker must be refreshed:
   - Determine run scope:
     - Full mode: `ISSUE_IDS` omitted. Process every `OPEN` issue and perform new-issue discovery.
     - Filtered mode: `ISSUE_IDS` provided. Process only those issue IDs and skip broad new-issue discovery.
   - Resolve the evidence base:
     - Use explicit `TARGET_FILE_PATHS` when provided.
     - Otherwise infer sibling target files from the tracker directory and subject version. Prefer nearby `ddr_node_schema*.yaml` and `ddr_system*.yaml`.
     - Load explicit `REFERENCE_DOC_PATHS`.
     - Also inspect same-directory `*Issue_Identification_Audit*.md`, matching per-issue report files, and any local paths already cited by the tracker.
   - Upgrade the tracker contract on first write when needed:
     - If `document.format_version` is `IT-1.0`, migrate the tracker to `IT-1.1`.
     - Update `document.format_version`, the footer banner, the embedded `## ISSUE SCHEMA`, and the `## RESOLUTION WORKFLOW` so they match the `IT-1.1` contract.
     - Ensure every populated issue block contains `Resolution-[NNN]: Option C - ...`, `Comparative Analysis-[NNN]`, `Recommendation-[NNN]`, and `Supporting Citations-[NNN]`.
   - Revalidate each selected issue against decisive local evidence:
     - Investigate the claims against the target YAML/spec files first.
     - Use repo-local audits or issue reports only when they are supported by the target files.
     - Run local schema probes only when they materially confirm or disprove a claim. Keep those probes scratch-only and never modify repo-tracked target files.
     - Rewrite `Problem Statement`, `Evidence & Justification`, `Impact Assessment`, and `Notes` only as needed to make them technically accurate and internally consistent.
     - Preserve existing `Option A` and `Option B` unless they are factually wrong, materially incomplete, or no longer distinct.
   - Add strategy comparison and recommendation content for each selected issue:
     - Add a genuinely distinct `Option C`.
     - Add `Comparative Analysis-[NNN]` comparing the blast radius, compatibility implications, enforcement strength, and implementation complexity of Options A, B, and C.
     - Add `Recommendation-[NNN]` with exactly one endorsed option using `**Endorsed Option:** \`Option A|B|C\`` plus concise technical rationale.
     - Add `Supporting Citations-[NNN]` as 1-3 single-line bullets in the canonical citation format.
     - Use recent authoritative web sources for recommendation support, preferring official specifications, standards bodies, and primary vendor documentation.
   - Discover new issues in full mode only:
     - Add a new issue only when it is materially supported, technically important, and not a trivial duplicate or narrow restatement of an existing issue.
   - Rebuild tracker bookkeeping after edits:
     - Update registry rows and sort them by severity then issue number.
     - Update dependency-map rows when new or revised dependencies are materially supported.
     - Refresh `document.last_modified`, footer date, `open_issues`, and `resolved_issues`.
     - Count `open_issues` as `OPEN` plus `IN_REVIEW`. Count `resolved_issues` as `RESOLVED`.
     - Keep statuses conservative. Do not mark issues `RESOLVED` unless the user explicitly expands scope.
   - Validate with `python .agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py <ISSUES_TRACKER_PATH>`.
6. Execute `validate` mode when the request is to validate or audit an Issues Tracker without broader edits:
   - Use `python .agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py <ISSUES_TRACKER_PATH> --mode legacy` for historical `v4` or `v5` trackers with parser-header markers.
   - Use `python .agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py <ISSUES_TRACKER_PATH> --mode canonical` for blank `IT-1.0` trackers.
   - Use `python .agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py <ISSUES_TRACKER_PATH>` for populated `IT-1.1` trackers or migration-readiness audits.
   - Report the exact validator result and any migration-relevant structural failures without mutating target DDR/spec files.
7. Return one concise success line including the tracker path when initialization or maintenance succeeds. Return the exact validator result when validation-only mode is requested.

Examples:

- Initialize:
  - Request: `Initialize an issues tracker for DDR System v7.0 at .agent/assets/proposals/active/v7/DDR_v7_Issues_Tracker.md by Anthony Formosa.`
  - Result: `Issues Tracker initialized: .agent/assets/proposals/active/v7/DDR_v7_Issues_Tracker.md`
- Full maintenance:
  - Request: `Update .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md against the v6.2 DDR YAML files and refresh all open issues.`
  - Result: `Issues Tracker updated: .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md`
- Validation:
  - Request: `Validate .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md for IT-1.1 compliance.`
  - Result: `VALID [IT-1.1] .agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md`

</how_to_use>

<constraints>

- Do not use this skill to generate a standalone single-issue report; `artifact-issue-report` remains the dedicated owner contract for that artifact family.
- Do not author or revise `.agent/schemas/issues-tracker/` through this skill; canonical schema work belongs to `core-schema`.
- Never patch the target DDR YAML/spec files. This skill is tracker-initialization, tracker-maintenance, and tracker-validation only.
- Never fabricate evidence, schema-probe outcomes, issue IDs, citations, local file references, or validation outcomes.
- Never broaden a filtered run into broad new-issue discovery.
- Never add `Option C` if it is a near-copy of Option A or Option B.
- Keep the embedded `## ISSUE SCHEMA` and `## RESOLUTION WORKFLOW` synchronized with the `IT-1.1` format when a tracker is migrated.
- Preserve the separate `IT-1.0` blank-initialization and `IT-1.1` populated-maintenance profiles. Do not collapse them into one overloaded format through this skill.
- Preserve unrelated issue content during maintenance; update only what the evidence requires.
- Do not hand-edit vendored mirrors under `resources/schema/`; refresh them from `.agent/schemas/`.

</constraints>

<resources_reference>

- Read `.agent/schemas/issues-tracker/README.md` to confirm canonical tracker governance, lifecycle ownership, and profile semantics.
- Read `.agent/schemas/issues-tracker/issues-tracker.d.ts` to verify the active tracker contract before editing.
- Read `resources/schema/issues-tracker/template.md` when initializing a blank tracker.
- Read `resources/schema/issues-tracker/example.md` to compare blank `IT-1.0` output against the canonical example.
- Read `resources/schema/issues-tracker/example-it-1.1.md` to mirror the canonical populated tracker structure.
- Read `.agent/skills/artifact-issue-tracker/resources/reference.md` to preserve local tracker authoring, evidence, and validation conventions across all operating modes.
- Run `.agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py` to validate blank or legacy tracker artifacts.
- Run `.agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py` to validate populated `IT-1.1` tracker artifacts.

</resources_reference>
