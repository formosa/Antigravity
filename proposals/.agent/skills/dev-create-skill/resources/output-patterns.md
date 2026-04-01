<document_purpose>
This document defines how agent skills must format outputs using the Antigravity v1.20.3 Artifact System.
</document_purpose>

<artifact_generation_rules>
Do not generate generic Markdown reports. All complex workflows must end by generating one of the following Execution State Artifacts:

1. **Implementation_Plan.md:** Used during the Planning phase.
   - Must preserve compatibility with `.agent/schemas/implementation-plan/implementation-plan.d.ts`.
   - Required YAML frontmatter keys: `task`, `model`, `version`, `output_path`, `processed_path`.
   - Required body blocks: `<objective>`, `<phases>`, `<atomic_steps>`, and `<verification>`.
   - `<risks_and_mitigations>` remains optional but is required for any step classified as high-risk (Request Review).
   - Do not introduce unsupported frontmatter keys or new top-level sections unless the schema and companion assets are revised together.
   - Each `<verification>` item must map 1:1 to the corresponding `<atomic_steps>` item by number.
   - `<atomic_steps>` must use named `####` group headers and `- [ ]` completion trackers per step.
   - Requires human approval before the executor modifies any code or file.
   - **File naming:** `YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md` where `<uuid8>` is the first 8 hex characters of a newly generated UUID4.
   - **Output path:** `.agent/plans/<filename>`
   - **Post-execution archive path:** `.agent/plans/processed/<filename>` — executor must relocate the artifact here upon full verification completion.

2. **Task.md:** Used to track active granular execution.
   - Must include `<pre_check>` and `<rollback_procedure>` blocks.

3. **Walkthrough.md:** Used as proof-of-work upon task completion.
   - Must include `<execution_summary>`, `<architectural_changes>`, and explicit terminal commands in `<verification_steps>`.
</artifact_generation_rules>

<contract_stability_rules>

- Treat the schema, example artifact, output patterns, and accepted plan corpus as one unified contract surface.
- Improve planning rigor inside the artifact's existing structure before proposing contract expansion.
- Do not treat richer internal planning logic as justification for adding new artifact sections.
- If a skill requires a new frontmatter key or top-level block, update the schema and all companion documentation first.
- `output_path` and `processed_path` are now required frontmatter fields as of schema v1.20.3. Plans missing these fields are non-compliant.
</contract_stability_rules>

<completion_tracker_rules>

- Every `<atomic_steps>` item must be prefixed with `- [ ]` at artifact creation time.
- The executing agent updates each completed step to `- [X]` immediately after its corresponding `<verification>` check passes.
- Steps must not be marked `[X]` speculatively or in advance of verification.
- Groups are defined by `####` headers. Group names must reflect genuine phase or responsibility boundaries.
</completion_tracker_rules>

<xml_fenced_outputs>
When generating localized files such as `CHANGELOG.md` or configuration logs, isolate strict formatting rules using localized XML tags to prevent instruction drift.

Example:
**Codebase Modification:** Update the `CHANGELOG.md` adhering strictly to the required formatting guidelines.
<changelog_constraints>

- Group changes by type: Added, Changed, Deprecated, Removed, Fixed, Security.
- Use imperative mood in all bullet points.
</changelog_constraints>
</xml_fenced_outputs>

<model_routing_reference>

| Task type | Assigned model |
| :--- | :--- |
| Architecture, planning, high-complexity reasoning | `gemini-3.1-pro-preview` |
| High-volume, low-latency implementation steps | `gemini-3-flash` |
| **Deprecated — do not use** | `gemini-3-pro-preview` (discontinued 2026-03-26) |

</model_routing_reference>
