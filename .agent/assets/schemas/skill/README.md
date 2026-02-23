# DESIGN_JUSTIFICATION: Antigravity Skill Assets v1.18.3

<document_purpose>
This document serves as the verified, single-source-of-truth reference for the architectural design of Skill assets within the Antigravity IDE v1.18.3 ecosystem. It is formatted explicitly for ingestion by Gemini 3.1 Pro and Gemini 3 Flash models to establish the correct parsing logic for progressive disclosure capabilities.
</document_purpose>

<schema_evaluation_and_justification>

- **Progressive Disclosure & Semantic Routing:** The IDE v1.18.3 routing engine does not load all capabilities at startup. Instead, it relies strictly on the `description` parameter in the YAML frontmatter to semantically match user intent and dynamically load the skill into the LLM's context window only when relevant.
- **Architectural Cleanup:** Legacy parameters such as `scope` and `priority` have been eliminated from the frontmatter. A skill's scope is dictated by its physical directory installation, and priority sorting is reserved exclusively for the Rules engine.
- **Context-First XML Fencing:** The `<when_to_use>` block acts as a secondary, silent verification step for Gemini 3.1 Pro before it executes the `<how_to_use>` payload, preventing the model from utilizing the skill out of context.
- **Resource Referencing:** The `<resources_reference>` block establishes strict paths for the LLM to access auxiliary scripts, few-shot examples, or code templates securely isolated within the skill's specific subdirectory.
</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Google Antigravity - Wikipedia](https://en.wikipedia.org/wiki/Google_Antigravity)
   - Details the Antigravity v1.18.3 release on February 19, 2026. Identifies the IDE's agent-first paradigm and the necessity of progressive disclosure for skill loading.

2. [Authoring Google Antigravity Skills - Google Codelabs](https://codelabs.developers.google.com/getting-started-with-antigravity-skills)
   - Official documentation confirming that skill assets require precise `description` YAML frontmatter for trigger definitions, and establishing the exact directory structures required for custom capabilities.

3. [Build with Google Antigravity](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
   - Outlines the shift to autonomous task orchestration and details how custom skills extend the baseline model via modular tool integration.

4. [Gemini 3.1 Pro - Model Card - Google DeepMind](https://deepmind.google/models/model-cards/gemini-3-1-pro/)
   - Defines Gemini 3.1 Pro as state-of-the-art for reasoning and agentic coding, requiring explicit and structured formatting to maximize its 1M-token context window without hallucinating operations.

5. [Gemini 3.1 Pro Preview API is now live on APIYI: Analysis of 6 major core upgrades](https://help.apiyi.com/en/gemini-3-1-pro-preview-api-available-apiyi-guide-en.html)
   - Confirms Gemini 3.1 Pro's doubled reasoning scores on the ARC-AGI-2 benchmark (77.1%), highlighting its architectural enhancements for processing multi-step execution steps found within `<how_to_use>` blocks.

6. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official documentation confirming the optimal use of XML-style delimiters (e.g., `<when_to_use>`, `<how_to_use>`) to isolate situational triggers from active generation instructions.

7. [Antigravity IDE v1.18.3 Architecture & Schemas - Google Open Source](https://google.github.io/adk-docs/architecture-v1-18)
   - Explicitly details the structural separation of machine-parseable YAML metadata (for the semantic router) and XML-delimited body content (for the LLM), rejecting flat-file structures.

8. [Progressive Disclosure and Semantic Routing in Antigravity - Zeabur](https://zeabur.com/blogs/google-antigravity-routing-engine)
   - Explains how Antigravity handles capabilities via the unified background router, confirming that agents should semantically trigger dynamic module loading via `SKILL.md` descriptions rather than explicitly spawning sub-agents.
</authoritative_reference_repository>
