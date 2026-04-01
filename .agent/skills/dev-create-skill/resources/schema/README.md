# DESIGN_JUSTIFICATION: Antigravity Skill Assets v1.20.3

<document_purpose>
This document identifies the authoritative local contract for Antigravity skill assets and the official external references that inform `dev-create-skill`.
</document_purpose>

<authority_order>
1. `resources/schema/skill.d.ts`
2. `scripts/quick_validate.py`
3. `scripts/init_skill.py`
4. `.agent/skills/dev-create-skill/SKILL.md`
5. Official external references listed below, which are informative and must not override the local contract unless the contract is intentionally revised
</authority_order>

<schema_evaluation_and_justification>
- `description` is the primary routing surface and must say what the skill does, when it should trigger, and its nearest exclusions.
- `version` remains required for Antigravity v1.20.3 compatibility and validator coherence.
- XML-delimited body sections preserve deterministic boundaries between trigger checks, execution flow, constraints, and resource declarations.
- `<resources_reference>` should point only to existing skill-local files and should say whether each file is read or run.
- Validation distinguishes hard structural failures from quality warnings so existing skills remain usable while new skills are pushed toward clearer routing and safer packaging.
</schema_evaluation_and_justification>

<authoritative_reference_repository>
1. Local contract surface: `resources/schema/skill.d.ts`
2. Local validator contract: `scripts/quick_validate.py`
3. Local scaffolding contract: `scripts/init_skill.py`
4. [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)
5. [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf?file=a-practical-guide-to-building-agents.pdf)
6. [OpenAI Trace grading](https://developers.openai.com/api/docs/guides/trace-grading)
7. [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
8. [Google Gemini prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
</authoritative_reference_repository>

<modification_history>

| Date | Version | Classification | Description |
| :--- | :--- | :--- | :--- |
| 2026-03-01 | v1.1.0 | Optimization | Added schema-oriented design notes for Antigravity skill assets. |
| 2026-04-01 | v1.20.3 | Hardening | Replaced non-authoritative references, clarified local authority order, and aligned guidance with the active validator and scaffolder. |

</modification_history>
