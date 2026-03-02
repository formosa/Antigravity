# DESIGN_JUSTIFICATION: Antigravity Rule Assets v1.18.3

<document_purpose>
This document serves as the verified reference for Rule assets within the Antigravity IDE v1.18.3 ecosystem. It establishes the parsing logic for conditional constraints in Gemini 3.1 Pro and Gemini 3 Flash.
</document_purpose>

<schema_evaluation_and_justification>

- **Frontmatter Parsing:** The `description` field is required for semantic discovery by the IDE routing engine.
- **Trigger Optimization:** Using `glob` instead of `always_on` prevents instruction dilution and reduces latency by only injecting rules when relevant files are active.
- **Deterministic Conflict Resolution:** The `priority` parameter allows the unified semantic router to resolve overrides between conflicting rules.
- **Hardware-Aware Execution:** The `execution_tier` maps high-priority validation to local CPU threads (e.g., Ryzen 9 5900X) to ensure non-blocking "Silent Verification".
- **XML Content Fencing:** `<constraints>` and `<verification_step>` tags isolate behavioral rules from workspace context to prevent instruction drift.
</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Google Antigravity - Wikipedia](https://en.wikipedia.org/wiki/Google_Antigravity) - Details the v1.18.3 release and agent-first paradigm.
2. [Rules / Workflows - Google Antigravity Documentation](https://antigravity.google/docs/rules-workflows) - Confirms YAML frontmatter and glob matching requirements.
3. [Gemini 3.1 Pro in Google Antigravity](https://antigravity.google/blog/gemini-3-1-pro-in-google-antigravity) - Verifies "Silent Verification" loops for the Feb 2026 update.
4. [Gemini 3.1 Pro - Model Card](https://deepmind.google/models/model-cards/gemini-3-1-pro/) - Establishes XML fencing as the state-of-the-art for reasoning anchoring.
5. [Gemini 3.1 Pro API Analysis](https://help.apiyi.com/en/gemini-3-1-pro-preview-api-available-apiyi-guide-en.html) - Confirms 77.1% ARC-AGI-2 score for strict logic processing.
6. [Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) - Best practices for instruction isolation.
7. [Antigravity IDE v1.18.3 Architecture](https://google.github.io/adk-docs/architecture-v1-18) - The authoritative schema for YAML/XML separation.
</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description |
| :--------- | :------ | :------------- | :---------- |
| 2026-03-01 | v1.1.0  | Optimization   | Aligned with Gemini 3.1 Pro prompt framework. |
| 2026-03-02 | v1.2.0  | Architecture   | Integrated `execution_tier` for 24-thread parallel validation. |
</modification_history>
