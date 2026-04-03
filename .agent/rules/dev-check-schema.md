---
name: dev-check-schema
description: "Enforces RuleDefinition frontmatter integrity for `.agent/rules/` assets, governed rules-index hygiene, and canonical schema-markdown governance under `.agent/schemas/`."
version: "1.3.0"
trigger: glob
globs: ".agent/schemas/**/*.md, .agent/rules/**/*.md"
priority: critical
execution_tier: standard
---

<constraints>

# Antigravity Asset Schema Enforcement

- **Rule Frontmatter Scope:** Only rule assets under `.agent/rules/` other than `.agent/rules/index.md` are governed by the `RuleDefinition` frontmatter contract. Those rule assets MUST include semantic-version `version` values, non-placeholder `description` text, supported `trigger` and `priority` values, and XML-fenced body content.
- **Rule Trigger/Glob Coupling:** Rules using `trigger: glob` MUST declare non-empty `globs`. Rules using any other trigger MUST NOT declare `globs`.
- **Rule Execution Tier:** Rule assets MUST use `execution_tier: standard` unless a heavy, non-LLM parallel workload is explicitly justified.
- **Rules Index Governance:** `.agent/rules/index.md` MUST remain a generated discovery index aligned with the `index` schema. It MUST summarize live rule metadata without superseding any linked rule definition.
- **Canonical Schema README Governance:** Canonical schema READMEs under `.agent/schemas/<schema-id>/README.md` MUST preserve accurate `<document_purpose>`, `<schema_governance>`, `<authority_order>`, and `<modification_history>` content aligned with the adjacent schema directory.
- **Schema Example Fidelity:** Example or template markdown under `.agent/schemas/` MUST remain aligned with the adjacent `.d.ts` contract and MUST NOT contain unresolved `TODO`, `N/A`, or generic filler text that would misrepresent the schema.
- **Rule Body Fencing:** `.agent/rules/*.md` files MUST wrap all body content inside `<constraints>` and optional `<verification_step>` blocks. Do not apply this rule-body requirement to schema README or example assets.

</constraints>

<verification_step>

1. **Rule Asset Check:** If the target file is a rule asset under `.agent/rules/` other than `index.md`, validate its YAML keys against `rule.d.ts`, confirm `version` uses semantic versioning, enforce the `trigger` and `globs` coupling, and reject overbroad claims that try to impose rule-only frontmatter requirements on schema markdown assets.
2. **Rules Index Check:** If the target file is `.agent/rules/index.md`, confirm it remains a generated discovery index that summarizes live rule metadata without restating or overriding rule-body semantics.
3. **Schema README Check:** If the target file is a canonical schema `README.md`, confirm the owner-skill metadata, authority order, and modification history remain synchronized with the adjacent schema directory.
4. **Example or Template Check:** If the target file is a schema example or template markdown asset, confirm it still reflects the adjacent `.d.ts` contract and does not contain unresolved placeholders.

</verification_step>
