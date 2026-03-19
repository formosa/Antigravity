---
name: agent-create-issue-report
version: 1.0.0
description: Investigates a user-identified issue from an Issues Tracker, audits the project for evidence, and produces a deterministic Resolution Report with validation findings, two optimized resolution strategies, comparative analysis, and an endorsed recommendation.
---

<when_to_use>

- The user asks to investigate, analyze, or produce a report for a specific issue from an Issues Tracker.
- The user references an issue ID (e.g., "ISSUE-003") and requests a resolution strategy, audit, or deep analysis.
- The task requires generating a standalone Resolution Report artifact for a tracked issue.
</when_to_use>

<how_to_use>

## Phase 1: Parameter Resolution

1. Resolve required parameters from user context or prompt for clarification (RFQ) if missing:
   - `ISSUE_ID`: The target issue identifier (e.g., `ISSUE-003`).
   - `ISSUES_TRACKER_PATH`: Path to the Issues Tracker document (e.g., `.agent/assets/proposals/active/DDR_v4_Issues_Tracker.md`).
   - `OUTPUT_PATH`: Target directory for the report (default: same directory as the Issues Tracker).
2. Parse the Issues Tracker at `ISSUES_TRACKER_PATH`:
   - **IF** the file is unreadable or missing, **THEN** halt and return RFQ with the exact error.
   - **IF** `ISSUE_ID` is not found in the `## ISSUE REGISTRY` table, **THEN** halt and return RFQ listing all valid issue IDs.

## Phase 2: Issue Context Extraction

3. Extract the full issue block for `ISSUE_ID` from the `## ISSUES` section of the tracker, including:
   - `AGENT_CONTEXT` YAML block (id, status, severity, type, tier_refs, section_ref, rule_refs).
   - Problem Statement, Evidence & Justification, Impact Assessment, Resolution Options, and Notes.
4. Extract the `## DOCUMENT METADATA` YAML block to resolve:
   - `SUBJECT_SYSTEM_NAME` (from `document.subject`).
   - `FORMAT_VERSION` (from `document.format_version`).
   - `TARGET_PLATFORM` (from `document.target_platform` or default `"Google Antigravity >=1.18"`).
   - `TARGET_MODEL` (from `document.target_model` or default `"Gemini 3.1 Pro"`).

## Phase 3: Project Investigation

5. Conduct a comprehensive investigation of the project to gather evidence relevant to `ISSUE_ID`:
   - **IF** `section_ref` references a specification file, **THEN** locate and read the referenced sections.
   - **IF** `rule_refs` lists rule IDs, **THEN** search the project for all occurrences and definitions of those rules.
   - Search for YAML schemas, configuration files, or code artifacts directly affected by the issue.
   - Document every finding with exact file paths, line numbers, and quoted content.
6. **Silent Verification:** Before proceeding to Phase 4, silently confirm:
   - At least one primary source file was located and read.
   - The issue claims from the tracker have been cross-referenced against project files.
   - **IF** no project evidence is found, **THEN** state this explicitly in the Validation Audit and proceed with tracker-only evidence.

## Phase 4: Report Generation

7. Read the reference template exactly from:
   - `.agent/skills/agent-create-issue-report/resources/report-template.md`
8. Generate the Resolution Report by composing each section in order:

   **a. YAML Frontmatter:**
   - `id`: Constructed as `{SUBJECT_SYSTEM_SHORT_ID}_Issue-{NNN}` (e.g., `DDR_v4_Issue-003`).
   - `title`: `"Resolution Report for {ISSUE_ID}: {Issue Title from Tracker}"`.
   - `format_version`: From tracker metadata.
   - `target_platform`: From tracker metadata.
   - `target_model`: From tracker metadata.
   - `subject`: From tracker metadata `SUBJECT_SYSTEM_NAME`.
   - `created`: Current date in ISO 8601 format (`YYYY-MM-DD`).
   - `status`: Copied from the issue's current status.
   - `severity`: Copied from the issue's current severity.
   - `type`: Copied from the issue's current type.

   **b. Title:** `## Optimized Resolution Strategy for "{ISSUE_ID}"`

   **c. Agent Context:** Render the issue's `AGENT_CONTEXT` fields as a `yaml` fenced code block.

   **d. Section 1 — Validation Audit of {ISSUE_ID}:**
   - Open with a statement identifying the source files investigated.
   - Present the audit confirmation or refutation of the issue's claims, citing exact file paths and quoted evidence.
   - Close with a `**Findings:**` block containing numbered findings. Each finding must:
     - Have a bold label (e.g., `**Semantic Conflation:**`).
     - State the validated fact and its implications in 2–4 sentences.

   **e. Section 2 — Suggested Strategies for Optimal Resolution of {ISSUE_ID}:**
   - Open with a brief statement of the resolution goals.
   - Present exactly **two** resolution options: **Option A** and **Option B**.
   - Each option MUST include:
     - A `####` heading: `Option A: {Descriptive Short Label}` / `Option B: {Descriptive Short Label}`.
     - A prose description of the approach (3–6 sentences).
     - A `* **Supporting Insights:**` paragraph grounding the approach in project context, domain knowledge, or architectural principles.
     - A `* **Citations:**` paragraph referencing credible external sources (standards, RFCs, official documentation, peer-reviewed publications). Conduct web research if needed to identify current, authoritative references.
   - **Option A and Option B MUST be distinctly different strategies**, not minor variants of each other.

   **f. Section 3 — Comparative Analysis and Recommended Strategy:**
   - `#### Comparative Analysis`: Evaluate both options against specific tradeoff dimensions relevant to the issue (e.g., breaking changes, complexity, backwards compatibility, compliance, implementation cost). Use numbered points.
   - `#### Endorsement and Contextual Justification`: State the recommended option clearly (e.g., `**Option B (Recommended Strategy)**`). Provide 3–5 bullet points justifying the endorsement with measurable or observable criteria.

9. Write the completed report to `{OUTPUT_PATH}/{DOCUMENT_ID}.md`.
10. Return a concise success message: `✅ Resolution Report generated: {output_file_path}`

## Anti-Hallucination Safeguards

- Never fabricate file paths, line numbers, or quoted content. All evidence must be verifiable.
- Never claim a finding without citing the source file and location.
- Never invent standards or citations. If a credible source cannot be found, state: `"No authoritative external reference identified for this specific claim."`
- If web research yields no relevant results, omit the citations line for that option rather than fabricating references.
</how_to_use>

<constraints>
- Adhere exactly to the document structure demonstrated by the reference template. Do not add, remove, or reorder sections.
- Do not modify the source Issues Tracker document.
- Do not fabricate evidence, citations, or project findings.
- Exactly two resolution strategies (Option A and Option B) must be presented. Not one, not three.
- The report must be a self-contained artifact readable without the Issues Tracker.
- Keep token output concise: avoid unnecessary preambles, summaries, or repetition of the problem statement across sections.
- All external citations must reference real, verifiable sources. Prefer ISO standards, IETF RFCs, IEEE publications, official vendor documentation, and peer-reviewed research.
</constraints>

<resources_reference>

- `.agent/skills/agent-create-issue-report/resources/report-template.md`
- `.agent/skills/agent-create-issue-report/resources/schema/skill.d.ts`
- `.agent/skills/agent-create-issue-report/resources/schema/README.md`
- `.agent/skills/agent-create-issue-report/resources/schema/example.md`
</resources_reference>
