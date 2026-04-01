# DESIGN_JUSTIFICATION: Antigravity Implementation Plan Assets v1.21.9

<document_purpose>
This document serves as the verified reference for the architectural design of Implementation Plan artifacts within the Antigravity IDE v1.21.9 ecosystem, optimized for Gemini 3.1 Pro Preview's enhanced reasoning, improved token efficiency, and custom-tool agentic capabilities.
</document_purpose>

<schema_evaluation_and_justification>

- **Split-Step Verification:** By formally separating the planning phase into an explicitly approved artifact, the schema prevents the model from initiating uncontrolled code generation. Human approval is required before any file modifications occur.
- **Phased Orchestration:** The `<phases>` array enables Gemini 3.1 Pro Preview to act as master architect, routing complex logic to itself (`gemini-3.1-pro-preview` or `gemini-3.1-pro-preview-customtools`) while delegating high-volume, low-latency implementation tasks to `gemini-3-flash` or `gemini-3.1-flash`.
- **XML Data Isolation:** Using `<atomic_steps>` and `<verification>` blocks forces the model to pair every intended action with a measurable success condition, anchoring attention to verifiable outcomes.
- **Progress Tracking:** Named sections with `[ ]` / `[X]` checkboxes within `<atomic_steps>` provide executor-level transparency for long-running, complex, or high-risk plans. Immediate per-section updates prevent state drift during multi-step agentic runs.
- **Plan Lifecycle Management:** Standardized naming (`YYYYMMDD-HHMMSS-<uuid8>-IMPLEMENTATION_PLAN.md`), active storage (`.agent/plans/`), and processed relocation (`.agent/plans/processed/`) create an auditable execution record without requiring external tracking systems.
- **Thinking Level Control:** Explicit `thinking_level` frontmatter (`HIGH` / `MEDIUM` / `LOW`) exposes Gemini 3.1 Pro's dynamic reasoning budget. `MEDIUM` is the recommended default for standard engineering tasks; `HIGH` is reserved for architectural planning and novel multi-system coordination. This directly reduces token cost and latency without sacrificing plan quality on bounded tasks.
- **Large-Context Anchoring:** An optional HTML comment block at the artifact's end restates the objective and in-scope constraints. This counteracts known attention degradation in long-context inputs (>50K tokens) by ensuring the executor's attention mechanism terminates on the highest-priority constraints.
- **Custom-Tool Endpoint:** Specifying `gemini-3.1-pro-preview-customtools` as the assigned model for tool-heavy phases (view_file, search_code, bash) activates the endpoint variant optimized for custom-tool prioritization, improving reliability in structured agentic workflows.
</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Gemini 3.1 Pro — Model Card — Google DeepMind](https://deepmind.google/models/model-cards/gemini-3-1-pro/)
   - Confirms improved token efficiency, agentic capability gains, and expanded `thinking_level` parameter (LOW / MEDIUM / HIGH).
2. [Gemini 3.1 Pro — Vertex AI Documentation — Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro)
   - Documents `gemini-3.1-pro-preview-customtools` endpoint; confirms `gemini-3-pro-preview` deprecation as of March 26, 2026.
3. [Gemini 3 Developer Guide — Google AI for Developers](https://ai.google.dev/gemini-api/docs/gemini-3)
   - Specifies `thinking_level` parameter behavior, default verbosity reduction, and context management best practices (instructions at end of large context payloads).
4. [Antigravity IDE v1.21.9 — Google Antigravity](https://antigravity.google/)
   - Mandates verifiable artifacts over opaque tool calls during complex multi-file modifications. v1.20.3+ reads rules from AGENTS.md in addition to GEMINI.md; auto-continue enabled by default.
5. [Authoring Google Antigravity Skills — Google Codelabs](https://codelabs.developers.google.com/getting-started-with-antigravity-skills)
   - Defines SKILL.md structure, on-demand context loading behavior, and workspace vs. global skill scope.
</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description |
| :--------- | :------ | :------------- | :---------- |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `implementation_plan.d.ts` with JSDoc annotations and version tracking to align with Gemini 3.1 Pro prompt optimization framework. |
| 2026-04-01 | v2.0.0  | Major Revision | Updated model IDs to `gemini-3.1-pro-preview` (deprecated `gemini-3-pro-preview` removed March 26, 2026). Added `thinking_level` frontmatter field. Introduced plan naming scheme, `.agent/plans/` storage, `.agent/plans/processed/` lifecycle, and progress-tracking checkboxes for complex/long-running/high-risk plans. Added `gemini-3.1-pro-preview-customtools` as executor endpoint option. Added large-context anchor pattern. Targeted Antigravity v1.21.9. |

</modification_history>
