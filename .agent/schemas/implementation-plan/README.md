# DESIGN_JUSTIFICATION: Antigravity Implementation Plan Assets v1.21.9

<document_purpose>
This document serves as the verified reference for the architectural design of Implementation Plan artifacts within the Antigravity IDE v1.21.9 ecosystem, optimized for `gemini-3-pro-preview` planning phases and `gemini-3-flash-preview` implementation-heavy execution phases.
</document_purpose>

<schema_evaluation_and_justification>

- **Split-Step Verification:** By formally separating planning into an explicitly approved artifact, the schema prevents uncontrolled code generation and reduces hallucination risk during executor handoff.
- **Phased Orchestration:** The optional `<phases>` array lets `gemini-3-pro-preview` handle architecture-heavy planning while routing high-volume edit execution to `gemini-3-flash-preview`.
- **XML Data Isolation:** Using `<atomic_steps>` and `<verification>` blocks forces the plan to pair every intended action with a measurable post-state.
- **Task-Group Completion Tracking:** Named `####` group headers with `- [ ]` / `- [X]` trackers preserve executor resume safety without expanding the contract surface.
- **Deterministic File Naming:** The `YYYYMMDD-HHMMSS[-NN]-IMPLEMENTATION_PLAN.md` convention keeps plans chronological, collision-safe, and easy to audit across `.agent/plans/` and `.agent/plans/processed/`.
- **Rules-Surface Discipline:** Local execution rules default to `.agent/rules/`, while `~/.gemini/GEMINI.md` is treated only as an optional global companion surface.
- **Live-Contract Authority:** The normative contract for new plans resides in the active schema, example artifact, runtime-target manifest, output-pattern rules, and the owner skill. Historical artifacts under `.agent/plans/processed/` remain review references only.
- **Grounded Planning Discipline:** The planner is expected to cite local evidence or cited external references rather than converting uncertainty into implied certainty.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Gemini API models](https://ai.google.dev/gemini-api/docs/models)
   - Current official model catalog for the active planning and execution model IDs.
2. [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog)
   - Official record of current Gemini model rollouts and deprecations relevant to plan artifacts.
3. [Prompt Design Strategies — Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Supports the Intent + Context + Constraints prompt structure used by the plan schema.
4. [ADK Coding with AI](https://adk.dev/tutorials/coding-with-ai/)
   - Current Google-authored guidance for Antigravity-style `.agent/` workspace conventions and coding flows.
5. [Conductor should be integrated into Antigravity to ensure long term context retention](https://discuss.ai.google.dev/t/conductor-should-be-integrated-into-antigravity-to-ensure-long-term-context-retention/113384)
   - Forum evidence for the current `.agent/rules/` and optional `~/.gemini/GEMINI.md` rule-surface split used in practice.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :--------- | :------ | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `implementation_plan.d.ts` with dense JSDoc annotations and version tracking aligned to Gemini 3.1 Pro prompt optimization framework.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 2026-04-01 | v1.20.3 | Major revision | Updated planner model to `gemini-3.1-pro-preview` (deprecated `gemini-3-pro-preview`). Added `output_path` and `processed_path` frontmatter fields. Introduced task-group `####` headers and `[ ]`/`[X]` completion trackers in `<atomic_steps>`. Defined `.agent/plans/` and `.agent/plans/processed/` storage convention with a timestamp-plus-derived-token naming scheme. Updated AGENTS.md as primary rules file per Antigravity v1.20.3. Strengthened anti-hallucination and grounding rules. Clarified that historical processed plans are review references rather than a compatibility surface. |
| 2026-04-03 | v1.20.4 | Governance     | Clarified that `artifact-implementation-plan` is the Artifact-Centric Owner for implementation-plan artifacts and aligned schema-side governance language with the shared owner-skill taxonomy.                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 2026-04-03 | v1.20.5 | Governance     | Updated the canonical implementation-plan governance metadata and authority references to the hardened `artifact-*` owner naming family while preserving `Primary Skill` schema-index terminology.                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 2026-04-06 | v1.20.6 | Simplification | Removed the random identifier token from new implementation-plan artifacts and replaced it with a timestamp-first naming convention that adds a numeric collision suffix only when needed.                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 2026-04-07 | v1.21.9 | Compatibility  | Replaced stale `AGENTS.md`-first and `gemini-3.1-*` compatibility claims with the current `.agent/rules/`, optional `~/.gemini/GEMINI.md`, and `gemini-3-pro-preview` / `gemini-3-flash-preview` contract surface.                                                                                                                                                                                                                                                                                                                                                                                                     |

</modification_history>

<schema_governance>

```yaml
primary_owner_skill: artifact-implementation-plan
distribution_model: canonical-plus-vendored-mirror
```

</schema_governance>
