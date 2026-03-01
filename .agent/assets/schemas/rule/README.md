# DESIGN_JUSTIFICATION: Antigravity Rule Assets v1.18.3

<document_purpose>
This document serves as the verified, single-source-of-truth reference for the architectural design of Rule assets within the Antigravity IDE v1.18.3 ecosystem. It is formatted explicitly for ingestion by Gemini 3.1 Pro and Gemini 3 Flash models to establish the correct parsing logic for conditional constraints.
</document_purpose>

<schema_evaluation_and_justification>

- **Frontmatter Parsing & Progressive Disclosure:** The IDE v1.18.3 routing engine mandates a strict separation of metadata. The `description` field is required for semantic discovery, while `trigger` and `globs` allow the engine to dynamically inject targeted rules only when relevant files (e.g., `*.py`) are active, preventing context window bloat and instruction dilution.
- **Deterministic Conflict Resolution:** The frontmatter `priority` parameter provides the IDE's unified semantic router with explicit weighting logic, ensuring critical security or architectural rules automatically override conflicting lower-priority stylistic suggestions.
- **Cognitive Optimization & Silent Verification:** The schema leverages Gemini 3.1 Pro's advanced reasoning capabilities by explicitly defining a `verification_step`. This forces the agent into a "silent verification" loop, checking compliance against the rule before emitting final code outputs.
- **XML Content Fencing:** XML tags (e.g., `<constraints>`, `<verification_step>`) must be strategically deployed within the `body_content` to isolate strict behavioral rules from active workspace context, preventing instruction drift and anchoring the LLM's attention mechanism to the required boundaries.
</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Google Antigravity - Wikipedia](https://en.wikipedia.org/wiki/Google_Antigravity)
   - Details the Antigravity v1.18.3 release on February 19, 2026. Identifies the IDE's agent-first paradigm and the necessity of progressive disclosure via dynamic file injection.

2. [Rules / Workflows - Google Antigravity Documentation](https://antigravity.google/docs/rules-workflows)
   - Official documentation confirming that rule assets require YAML frontmatter for trigger definitions (such as `glob` matching) to selectively inject constraints into the LLM context only when applicable.

3. [Gemini 3.1 Pro, Building with Advanced Intelligence in Google Antigravity](https://antigravity.google/blog/gemini-3-1-pro-in-google-antigravity)
   - Verifies the integration of Gemini 3.1 Pro (released February 19, 2026). Emphasizes silent verification execution and the model's ability to interpret strict negative boundaries when rules are properly fenced.

4. [Gemini 3.1 Pro - Model Card - Google DeepMind](https://deepmind.google/models/model-cards/gemini-3-1-pro/)
   - Defines Gemini 3.1 Pro as state-of-the-art for reasoning and agentic coding, requiring explicit and structured formatting to maximize its 1M-token context window without hallucinating rule overrides.

5. [Gemini 3.1 Pro Preview API is now live on APIYI: Analysis of 6 major core upgrades](https://help.apiyi.com/en/gemini-3-1-pro-preview-api-available-apiyi-guide-en.html)
   - Confirms Gemini 3.1 Pro's doubled reasoning scores on the ARC-AGI-2 benchmark (77.1%), highlighting its architectural enhancements for processing strict logic chains and enforcing prioritized rules.

6. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official documentation confirming the optimal use of XML-style delimiters (e.g., `<constraints>`, `<verification_step>`) to isolate strict rules from active generation instructions.

7. [Antigravity IDE v1.18.3 Architecture & Schemas - Google Open Source](https://google.github.io/adk-docs/architecture-v1-18)
   - Explicitly details the structural separation of machine-parseable YAML metadata (for the IDE router) and XML-delimited body content (for the LLM), rejecting flat-file structures.

8. [Progressive Disclosure and Semantic Routing in Antigravity - Zeabur](https://zeabur.com/blogs/google-antigravity-routing-engine)
   - Explains how Antigravity handles targeted context limits, confirming that `trigger` mechanisms (like glob pattern matching) are the recommended approach over global injection for non-universal rules.
</authoritative_reference_repository>

<modification_history>

| Date | Version | Classification | Description |
| :--- | :--- | :--- | :--- |
| 2026-03-01 | v1.1.0 | Optimization | Enhanced `rule.d.ts` with dense JSDoc annotations and schema versioning to align with the Gemini 3.1 Pro prompt optimization framework. |

</modification_history>
