---
name: antigravity-rule-assets-readme
description: "Authoritative documentation and design justification for Rule assets within the Antigravity IDE v1.18.3 ecosystem."
version: "1.2.0"
trigger: manual
priority: low
execution_tier: standard
---

<document_purpose>

# DESIGN_JUSTIFICATION: Antigravity Rule Assets

This document serves as the verified reference for Rule assets within the Antigravity IDE v1.18.3 ecosystem. It establishes the parsing logic for conditional constraints in Gemini 3.1 Pro and Gemini 3 Flash.

</document_purpose>

<schema_evaluation_and_justification>

- **Frontmatter Parsing:** The `description` field is required for semantic discovery by the IDE routing engine.
- **Trigger Optimization:** Using `glob` instead of `always_on` prevents instruction dilution and reduces latency by only injecting rules when relevant files are active.
- **Deterministic Conflict Resolution:** The `priority` parameter allows the unified semantic router to resolve overrides between conflicting rules.
- **Hardware-Aware Execution:** The `execution_tier` utilizes standard thread mapping to ensure IDE responsiveness without starving the host OS.
- **XML Content Fencing:** `<constraints>` and `<verification_step>` tags isolate behavioral rules from workspace context to prevent instruction drift.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Google Antigravity - Wikipedia](https://en.wikipedia.org/wiki/Google_Antigravity) - Details the v1.18.3 release and agent-first paradigm.
2. [Gemini 3.1 Pro - Model Card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) - Establishes XML fencing as the state-of-the-art for reasoning anchoring.
3. [Antigravity IDE Architecture](https://google.github.io/adk-docs/architecture-v1-18) - The authoritative schema for YAML/XML separation.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                    |
| :--------- | :------ | :------------- | :------------------------------------------------------------- |
| 2026-03-01 | v1.1.0  | Optimization   | Aligned with Gemini 3.1 Pro prompt framework.                  |
| 2026-03-02 | v1.2.0  | Architecture   | Integrated `execution_tier` for 24-thread parallel validation. |

</modification_history>

<schema_governance>
```yaml
primary_owner_skill: dev-schema
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>
