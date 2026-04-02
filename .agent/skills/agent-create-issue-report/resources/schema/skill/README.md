# DESIGN_JUSTIFICATION: Antigravity Skill Assets v1.21.0

<document_purpose>
This document identifies the canonical local contract for Antigravity skill assets and the rules for distributing self-contained vendored schema mirrors into skill packages.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: dev-create-skill
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/skill/skill.d.ts`
2. `.agent/skills/dev-create-skill/scripts/quick_validate.py`
3. `.agent/skills/dev-create-skill/scripts/init_skill.py`
4. `.agent/skills/dev-create-skill/scripts/sync_schema_mirrors.py`
5. `.agent/skills/dev-create-skill/SKILL.md`
6. Vendored mirrors under `.agent/skills/<skill>/resources/schema/skill/` are derived copies and must not override the canonical contract.
7. Official external references listed below are informative only and must not override the local contract unless the contract is intentionally revised.
</authority_order>

<schema_evaluation_and_justification>

- `description` is the primary routing surface and must say what the skill does, when it should trigger, and its nearest exclusions.
- `version` remains required for validator coherence and synchronized lifecycle tracking with the skill root `README.md`.
- XML-delimited body sections preserve deterministic boundaries between trigger checks, execution flow, constraints, and resource declarations.
- Root skill `README.md` records lifecycle governance, schema relationships, and SemVer history without overloading the schema-bundle README.
- Vendored schema mirrors keep packaged `.skill` archives self-contained while preserving `.agent/schemas/skill/` as the single canonical edit surface.
- Validation distinguishes hard structural failures from quality warnings so existing skills remain usable while new skills are pushed toward clearer routing and safer packaging.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local contract surface: `.agent/schemas/skill/skill.d.ts`
2. Local validator contract: `.agent/skills/dev-create-skill/scripts/quick_validate.py`
3. Local scaffolding contract: `.agent/skills/dev-create-skill/scripts/init_skill.py`
4. Local mirror sync contract: `.agent/skills/dev-create-skill/scripts/sync_schema_mirrors.py`
5. [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)
6. [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf?file=a-practical-guide-to-building-agents.pdf)
7. [OpenAI Trace grading](https://developers.openai.com/api/docs/guides/trace-grading)
8. [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
9. [Google Gemini prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification | Description                                                                                                                                                                                                       |
| :--------- | :------ | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-01 | v1.1.0  | Optimization   | Added schema-oriented design notes for Antigravity skill assets.                                                                                                                                                  |
| 2026-04-01 | v1.20.3 | Hardening      | Replaced non-authoritative references, clarified local authority order, and aligned guidance with the active validator and scaffolder.                                                                            |
| 2026-04-01 | v1.21.0 | Governance     | Established the canonical-plus-vendored-mirror distribution model and moved skill lifecycle/version tracking to root skill READMEs.                                                                               |
| 2026-04-02 | v1.21.1 | Repair         | Reconciled the canonical skill schema comments with the live validator by making `<constraints>` and `<resources_reference>` required and replacing hidden-reasoning language with observable execution guidance. |

</modification_history>