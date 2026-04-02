---
name: dev-check-schema
description: "Enforces RuleDefinition frontmatter integrity for .agent/rules/ assets and canonical schema-markdown governance hygiene for .agent/schemas/ assets."
version: "1.2.0"
trigger: glob
globs: ".agent/schemas/**/*.md, .agent/rules/**/*.md"
priority: critical
execution_tier: standard
---

<constraints>

# Antigravity Asset Schema Enforcement

- **Rule Frontmatter Scope:** Only files under `.agent/rules/` are governed by the `RuleDefinition` frontmatter contract. Those rule assets MUST include `version: "1.2.0"`, a non-placeholder `description`, and XML-fenced body content.
- **Rule Execution Tier:** Rule assets MUST use `execution_tier: standard` unless a heavy, non-LLM parallel workload is explicitly justified.
- **Canonical Schema README Governance:** Canonical schema READMEs under `.agent/schemas/<schema-id>/README.md` MUST preserve accurate `<document_purpose>`, `<schema_governance>`, `<authority_order>`, and `<modification_history>` content aligned with the adjacent schema directory.
- **Schema Example Fidelity:** Example or template markdown under `.agent/schemas/` MUST remain aligned with the adjacent `.d.ts` contract and MUST NOT contain unresolved `TODO`, `N/A`, or generic filler text that would misrepresent the schema.
- **Rule Body Fencing:** `.agent/rules/*.md` files MUST wrap all body content inside `<constraints>` and optional `<verification_step>` blocks. Do not apply this rule-body requirement to schema README or example assets.

</constraints>

<verification_step>

1. **Rule Asset Check:** If the target file is under `.agent/rules/`, validate its YAML keys against `rule.d.ts`, confirm `version: "1.2.0"`, and reject overbroad claims that try to impose rule-only frontmatter requirements on schema markdown assets.
2. **Schema README Check:** If the target file is a canonical schema `README.md`, confirm the owner-skill metadata, authority order, and modification history remain synchronized with the adjacent schema directory.
3. **Example or Template Check:** If the target file is a schema example or template markdown asset, confirm it still reflects the adjacent `.d.ts` contract and does not contain unresolved placeholders.

</verification_step>
