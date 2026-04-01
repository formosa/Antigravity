<document_purpose>
This document defines how agent skills must format outputs using the Antigravity v1.20.3+ Artifact System (current stable: v1.21.9).
</document_purpose>

<artifact_generation_rules>
Do not generate generic Markdown reports. All complex workflows must end by generating one of the following Execution State Artifacts:

1. **Implementation_Plan.md:** Used during the Planning phase. Must preserve compatibility with `.agent/schemas/implementation-plan/implementation-plan.d.ts`. Required YAML frontmatter keys: `task`, `model`, `version`, and `thinking_level`. Required body blocks: `<objective>`, `<phases>`, `<atomic_steps>`, and `<verification>`. `<risks_and_mitigations>` remains optional but is recommended for non-trivial or higher-risk work. Do not introduce unsupported frontmatter keys or new top-level sections unless the schema and companion implementation-plan assets are revised together. Each `<verification>` item must map 1:1 to the corresponding `<atomic_steps>` item. Requires human approval before the agent modifies code.

   **Naming scheme (REQUIRED):** `YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md`
   - `YYYYMMDD` — ISO date at creation (e.g., `20260401`)
   - `HHMMSS`   — 24-hour local time at creation (e.g., `143022`)
   - `<uuid8>`  — First 8 characters of a newly generated UUID v4 (e.g., `a3f7c12b`)
   - Example: `20260401-143022-a3f7c12b-IMPLEMENTATION_PLAN.md`

   **Storage path:** `.agent/plans/`

   **Progress tracking:** For complex, long-running, or high-risk plans, `<atomic_steps>` must be organized into named sections with `[ ]` / `[X]` progress checkboxes. Each checkbox must be updated to `[X]` immediately after the section's successful completion. Do not batch updates across sections.

   **Lifecycle:** Once ALL steps are successfully completed (all checkboxes `[X]`), the agent MUST relocate the artifact from `.agent/plans/` to `.agent/plans/processed/`, preserving the filename.

2. **Task.md:** Used to track active granular execution. Must include `<pre_check>` and `<rollback_procedure>` blocks.

3. **Walkthrough.md:** Used as proof-of-work upon completion. Must include `<execution_summary>`, `<architectural_changes>`, and explicit terminal commands in `<verification_steps>`.
</artifact_generation_rules>

<contract_stability_rules>

- Treat the schema, example artifact, output patterns, and accepted plan corpus as one contract surface.
- Improve planning rigor inside the artifact's existing structure before proposing contract expansion.
- Do not treat richer internal planning logic as justification for adding new artifact sections.
- If a skill requires a new frontmatter key or top-level block, update the schema and companion documentation first.
</contract_stability_rules>

<xml_fenced_outputs>
When generating localized files like `CHANGELOG.md` or configuration logs, isolate strict formatting rules using localized XML tags to prevent instruction drift.

Example:
**Codebase Modification:** Update the `CHANGELOG.md` adhering strictly to the required formatting guidelines.
<changelog_constraints>

- Group changes by type: Added, Changed, Deprecated, Removed, Fixed, Security.
- Use imperative mood in all bullet points.
</changelog_constraints>
</xml_fenced_outputs>
