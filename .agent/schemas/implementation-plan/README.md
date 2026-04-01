# DESIGN_JUSTIFICATION: Antigravity Implementation Plan Assets v1.20.3

<document_purpose>
This document serves as the verified reference for the architectural design of Implementation Plan artifacts within the Antigravity IDE v1.20.3 ecosystem, optimized for Gemini 3.1 Pro Preview's deep reasoning and agentic execution capabilities.
</document_purpose>

<schema_evaluation_and_justification>

- **Split-Step Verification:** By formally separating planning into an explicitly approved artifact, the schema prevents uncontrolled code generation and reduces hallucination risk during executor handoff.

- **Phased Orchestration:** The `<phases>` array enables `gemini-3.1-pro-preview` to act as master architect, routing complex logic tasks to itself while delegating high-volume, low-latency implementation steps to `gemini-3-flash`.

- **XML Data Isolation:** Using `<atomic_steps>` and `<verification>` blocks forces the model to pair every intended action with a measurable success condition, grounding its attention on verifiable outcomes rather than speculative results.

- **Task-Group Completion Tracking:** Organizing atomic steps under named `####` group headers with `- [ ]` / `- [X]` completion trackers provides human-readable execution state visibility and enables the executor to resume safely after any interruption without re-reading the full artifact.

- **Deterministic File Naming:** The `YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md` convention ensures collision-free artifact identity, chronological sortability, and unambiguous archive traceability. Active plans live in `.agent/plans/`; completed plans are relocated to `.agent/plans/processed/`.

- **AGENTS.md Integration:** As of Antigravity v1.20.3, agent rules are read from `AGENTS.md` (primary) with `GEMINI.md` as fallback. Skills must reference `AGENTS.md` as the authoritative rules surface when present.

- **Live-Contract Authority:** The normative contract for newly generated implementation plans resides in the active schema, example artifact, output-pattern rules, and skill instructions. Historical artifacts already present in `.agent/plans/processed/` remain review references only and are not a compatibility surface for this contract version.

- **Grounded Planning Discipline:** The planner operates as a strictly grounded assistant, relying only on facts present in local project context or cited external references. Uncertainty is surfaced as an RFQ artifact rather than converted to implicit assumption.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Gemini 3 Developer Guide — Google AI for Developers](https://ai.google.dev/gemini-api/docs/gemini-3)
   - Confirms Gemini 3.1 Pro Preview's optimization for long-horizon task orchestration, 1M-token context window, and agentic workflow capabilities.

2. [Prompt Design Strategies — Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Defines the Intent+Context+Constraints prompt formula, grounding directives, and risk assessment logic (read vs. write distinction) used in this skill's step formulation rules.

3. [Antigravity IDE v1.20.3 Changelog — Google AI Developers Forum](https://discuss.ai.google.dev/t/antigravity-update-1-20-3-2026-3-5/129320)
   - Documents AGENTS.md support, default auto-continue behavior, and token accounting fixes that inform this schema version.

4. [Gemini 3 Pro — Vertex AI Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro)
   - Confirms `gemini-3-pro-preview` discontinuation (2026-03-26) and mandatory migration to `gemini-3.1-pro-preview`.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description |
| :--------- | :------ | :------------- | :---------- |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `implementation_plan.d.ts` with dense JSDoc annotations and version tracking aligned to Gemini 3.1 Pro prompt optimization framework. |
| 2026-04-01 | v1.20.3 | Major revision | Updated planner model to `gemini-3.1-pro-preview` (deprecated `gemini-3-pro-preview`). Added `output_path` and `processed_path` frontmatter fields. Introduced task-group `####` headers and `[ ]`/`[X]` completion trackers in `<atomic_steps>`. Defined `.agent/plans/` and `.agent/plans/processed/` storage convention with `YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md` naming scheme. Updated AGENTS.md as primary rules file per Antigravity v1.20.3. Strengthened anti-hallucination and grounding rules. Clarified that historical processed plans are review references rather than a compatibility surface. |

</modification_history>
