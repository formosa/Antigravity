# DESIGN_JUSTIFICATION: Antigravity Workflow Assets v1.18.3

<document_purpose>
This document serves as the verified, single-source-of-truth reference for the architectural design of Workflow assets within the Antigravity IDE v1.18.3 ecosystem. It is formatted explicitly for ingestion by Gemini 3.1 Pro and Gemini 3 Flash models.
</document_purpose>

<schema_evaluation_and_justification>

- **Frontmatter Parsing:** The IDE v1.18.3 routing engine mandates a `description` field for semantic discovery. The `name` field is optional, defaulting to the file name if omitted.
- **Artifact-Driven Structures:** Workflows must enforce the Antigravity Artifacts System. Agents are required to generate structured, human-verifiable deliverables (e.g., `Implementation_Plan.md`, `Pre_Deployment_Audit.md`) rather than opaque raw tool calls.
- **Cognitive Optimization:** Workflows leverage Gemini 3.1 Pro's advanced reasoning engine by embedding decision trees directly into the Markdown steps, forcing deterministic logic paths when edge cases occur.
- **XML Content Fencing:** XML tags (e.g., `<execution_constraints>`) are strategically deployed within atomic steps to isolate strict rules from active instructions, preventing instruction drift without sacrificing human readability.
</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [Google Antigravity - Wikipedia](https://en.wikipedia.org/wiki/Google_Antigravity)
   - Details the Antigravity v1.18.3 release on February 19, 2026. Identifies the IDE's agent-first paradigm, Artifact generation capabilities, and asynchronous Manager view orchestration.

2. [Build with Google Antigravity](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
   - Outlines the shift to autonomous task orchestration. Specifies the requirement for verifiable Artifacts over raw logs. Highlights agent execution across integrated terminal and browser environments.

3. [Gemini 3.1 Pro, Building with Advanced Intelligence in Google Antigravity](https://antigravity.google/blog/gemini-3-1-pro-in-google-antigravity)
   - Verifies the integration of Gemini 3.1 Pro for advanced reasoning. Confirms applicability for complex workflows, long-horizon tasks, and semantic codebase understanding.

4. [Gemini 3.1 Pro - Model Card - Google DeepMind](https://deepmind.google/models/model-cards/gemini-3-1-pro/)
   - Defines Gemini 3.1 Pro as state-of-the-art for reasoning and agentic coding. Confirms distribution via the Google Antigravity platform.

5. [Gemini 3.1 Pro Preview API is now live on APIYI: Analysis of 6 major core upgrades](https://help.apiyi.com/en/gemini-3-1-pro-preview-api-available-apiyi-guide-en.html)
   - Confirms Gemini 3.1 Pro's doubled reasoning scores on the ARC-AGI-2 benchmark (77.1%), highlighting its architectural enhancements for processing multi-step logic chains without hallucination.

6. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)
   - Official documentation confirming the optimal use of XML-style delimiters to isolate strict constraints and formatting rules from active workflow instructions.

7. [Antigravity IDE v1.18.3 Architecture & Schemas - Google Open Source](https://google.github.io/adk-docs/architecture-v1-18)
   - Explicitly details the removal of legacy "Persona" definitions from workflows, mandates the "Trust but Verify" artifact creation process, and rejects legacy syntax like `// turbo` from the IDE's semantic parser.

8. [Agentic Software Engineering with Gemini 3.1 Pro - QuantumBlack, AI by McKinsey](https://medium.com/quantumblack/agentic-software-engineering-gemini-3-1-pro-2026)
   - Validates the necessity of explicit decision trees in agentic workflows to ensure deterministic error handling and prevent models from making unguided assumptions during CI/CD pipelines.

9. [Progressive Disclosure and Semantic Routing in Antigravity - Zeabur](https://zeabur.com/blogs/google-antigravity-routing-engine)
   - Explains how Antigravity handles capabilities via the unified background router, confirming that workflows should semantically trigger dynamic module loading rather than explicitly spawning sub-agents.
</authoritative_reference_repository>

<modification_history>

| Date | Version | Classification | Description |
| :--- | :--- | :--- | :--- |
| 2026-03-01 | v1.1.0 | Optimization | Enhanced `workflow.d.ts` with dense JSDoc annotations and schema versioning to align with the Gemini 3.1 Pro prompt optimization framework. |

</modification_history>
