# DESIGN_JUSTIFICATION: Antigravity GEMINI.md Configuration v1.18.3

<document_purpose>
This document establishes the verified architectural foundation for the `GEMINI.md` asset, which serves as a supported Gemini-specific configuration surface within the Antigravity IDE v1.18.3 ecosystem using Gemini 3.1 Pro. In workspaces that also provide `AGENTS.md`, rules may be loaded from `AGENTS.md` first while `GEMINI.md` remains an auxiliary configuration surface for Gemini-specific controls.
</document_purpose>

<schema_evaluation_and_justification>

- **Context Inversion (Heavy Data First):** The schema positions `<workspace_context>` at the very beginning of the XML payload. This adheres to the 2026 optimization mandate for 1M+ token windows, ensuring heavy architectural data is established before specific operational directives, which prevents instruction dilution and maximizes attention on terminal constraints.
- **Cognitive Throttling:** The inclusion of `thinking_level: medium` in the frontmatter replaces deprecated budget mechanics, providing the optimal balance of deep reasoning latency and token expenditure for complex PySide6 software engineering.
- **State Preservation:** The `<thought_signature_protocol>` is a mandatory architectural inclusion. It forces the agent to circulate encrypted reasoning state markers, resolving the context-rot issues prevalent in legacy multi-turn, multi-agent orchestrations.
- **Surface Coexistence:** `GEMINI.md` remains a valid configuration asset for Gemini-specific controls, but documentation must not imply exclusive ownership of all workspace rule authority when `AGENTS.md` is present.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Gemini 3.1 Pro - Model Card - Google DeepMind](https://deepmind.google/models/model-cards/gemini-3-1-pro/)
   - Confirms the model's 1M+ token context window capabilities and the necessity of structured formatting to maximize retrieval accuracy without hallucinating overrides.
2. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official documentation confirming the optimal use of XML-style delimiters to isolate strict global constraints and the effectiveness of placing instructions at the bottom of long contexts.
3. [Antigravity IDE v1.18.3 Architecture & Schemas - Google Open Source](https://google.github.io/adk-docs/architecture-v1-18)
   - Documents the supported `GEMINI.md` configuration surface and the strict requirement for the `thought_signature_protocol` to maintain coherence.
4. [Vertex AI Generative AI Docs - Thinking Configuration](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking)
   - Verifies the `thinking_level` parameter (minimal, low, medium, high) as the official mechanism for controlling reasoning depth and execution latency in the Gemini 3 series.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description |
| :--------- | :------ | :------------- | :---------- |
| 2026-03-01 | v1.1.0  | Optimization   | Enhanced `gemini.d.ts` with dense JSDoc annotations and enforced explicitly constrained unions to align with the Gemini 3.1 Pro prompt optimization framework. |
| 2026-04-01 | v1.1.1  | Clarification  | Reworded the GEMINI.md design justification so it no longer implies exclusive workspace-rule authority when `AGENTS.md` is present. |

</modification_history>

<schema_governance>
```yaml
primary_owner_skill: dev-schema
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>
