---
name: "rules-governance"
description: "Glob-scoped collection governance rule for the `.agent/rules/` directory, covering rule frontmatter, preferred naming, XML-fenced bodies, and the generated rules index for the full rules collection surface."
version: "2.0.0"
trigger: "glob"
globs: ".agent/rules/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. Scope Boundary: This rule governs only assets under `.agent/rules/`. It MUST NOT impose schema-directory governance requirements on `.agent/schemas/`.
2. Rule Frontmatter Contract: Rule assets under `.agent/rules/` other than `index.md` MUST satisfy the `RuleDefinition` frontmatter contract with semantic-version `version` values, non-placeholder `description` text, supported `trigger` and `priority` values, and only supported optional keys.
3. Preferred Naming Required: New or renamed rule assets MUST use lowercase hyphen-case for both the filename stem and any explicit `name` field. Modified legacy rule assets MUST be normalized to the preferred naming convention in the same task.
4. Trigger and Glob Coupling: Rules using `trigger: glob` MUST declare non-empty `globs`. Rules using any other trigger MUST NOT declare `globs`.
5. Execution Tier Default: Rule assets MUST use `execution_tier: standard` unless a heavier non-LLM parallel workload is explicitly justified inside the rule.
6. Rule Body Fencing: Rule assets other than `index.md` MUST wrap all body content inside a non-empty `<constraints>` block and MAY include a non-empty `<verification_step>` block when explicit completion checks are needed.
7. Rules Index Governance: `.agent/rules/index.md` MUST remain a generated discovery index aligned with the `index` schema. It MUST summarize live rule metadata without superseding any linked rule definition.

</constraints>

<verification_step>

1. If the target file is a rule asset other than `index.md`, validate its YAML keys against `rule.d.ts`, confirm `version` uses semantic versioning, and confirm the filename stem plus explicit `name` field use lowercase hyphen-case.
2. Confirm the target rule preserves supported `trigger` and `priority` values, keeps `trigger` and `globs` coupled correctly, and uses only allowed `execution_tier` values.
3. Confirm each non-index rule keeps all body content inside `<constraints>` and optional non-empty `<verification_step>` blocks.
4. If the target file is `.agent/rules/index.md`, confirm it remains a generated full-form discovery index aligned with the live rule set and linked rule definitions.

</verification_step>
