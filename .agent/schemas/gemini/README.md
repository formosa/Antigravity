# DESIGN_JUSTIFICATION: Antigravity GEMINI.md Configuration v1.21.9

<document_purpose>
This document establishes the verified architectural foundation for the optional global `~/.gemini/GEMINI.md` companion surface within the Antigravity IDE v1.21.9 ecosystem. Workspace-local execution rules remain anchored in `.agent/rules/`; `GEMINI.md` is retained only for optional Gemini-specific global controls.
</document_purpose>

<schema_evaluation_and_justification>

- **Companion-Surface Scope:** The schema now treats `~/.gemini/GEMINI.md` as an optional global companion rather than the primary workspace rule surface, which keeps local repository rules authoritative under `.agent/rules/`.
- **Context Inversion (Heavy Data First):** The schema positions `<workspace_context>` at the beginning of the XML payload so high-value project context lands before operational directives in long-window Gemini 3 sessions.
- **Cognitive Throttling:** `thinking_level` remains the explicit depth/latency control surface and is still sufficient for balancing `gemini-3-pro-preview` against `gemini-3-flash-preview`.
- **Surface Coexistence:** The contract is explicit that `GEMINI.md` and `.agent/rules/` can coexist, but only `.agent/rules/` should be treated as the local workspace execution authority by default.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Gemini API models](https://ai.google.dev/gemini-api/docs/models)
   - Current official model catalog for Gemini model identifiers and availability.
2. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official guidance for XML-style delimiters, long-context instruction placement, and stable prompt structure.
3. [ADK Coding with AI](https://adk.dev/tutorials/coding-with-ai/)
   - Current Google-authored workflow guidance for Antigravity-style coding environments and workspace-local `.agent/` contracts.
4. [Conductor should be integrated into Antigravity to ensure long term context retention](https://discuss.ai.google.dev/t/conductor-should-be-integrated-into-antigravity-to-ensure-long-term-context-retention/113384)
   - Forum evidence for the current `.agent/rules/` plus optional `~/.gemini/GEMINI.md` surface split used by active Antigravity workflows.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                                                                                                                                                  |
| :--------- | :------ | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `gemini.d.ts` with dense JSDoc annotations and enforced explicitly constrained unions to align with the Gemini 3.1 Pro prompt optimization framework.                               |
| 2026-04-01 | v1.1.1  | Clarification  | Reworded the GEMINI.md design justification so it no longer implies exclusive workspace-rule authority when `AGENTS.md` is present.                                                          |
| 2026-04-04 | v1.1.2  | Governance     | Updated `primary_owner_skill` from `dev-schema` to `core-schema` so canonical schema stewardship reflects the new foundational `core-*` family without changing the GEMINI contract surface. |
| 2026-04-07 | v1.21.9 | Compatibility  | Replaced stale `v1.18.3`, `AGENTS.md`, and `gemini-3.1-*` compatibility claims with the current `.agent/rules/` plus optional `~/.gemini/GEMINI.md` model and runtime guidance.            |

</modification_history>

<schema_governance>

```yaml
primary_owner_skill: core-schema
distribution_model: canonical-plus-vendored-mirror
```

</schema_governance>
