# DESIGN_JUSTIFICATION: Antigravity Rule Assets v1.3.0

<document_purpose>
This document establishes the canonical local contract for Antigravity rule assets and the owner-managed lifecycle used to scaffold, validate, and index those rules.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: dev-rule
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/rule/rule.d.ts`
2. `.agent/skills/dev-rule/scripts/quick_validate.py`
3. `.agent/skills/dev-rule/scripts/init_rule.py`
4. `.agent/skills/dev-rule/scripts/update_index.py`
5. `.agent/skills/dev-rule/SKILL.md`
6. Vendored mirrors under `.agent/skills/<skill>/resources/schema/rule/` are derived copies and must not override the canonical contract.
7. External references listed below are informative only and must not override the local contract unless the contract is intentionally revised.
</authority_order>

<schema_evaluation_and_justification>

- `description`, `trigger`, and `priority` form the minimum routing surface needed to discover the correct rule and resolve overlap safely.
- Rule assets stay lightweight by requiring only one mandatory XML body block, `<constraints>`, while keeping `<verification_step>` optional for rules that genuinely need explicit completion checks.
- `version` remains a semantic version string so live rule assets can evolve independently from the canonical schema package version.
- `globs` stays scoped to `glob` rules so file-targeted rules remain precise without burdening `manual` or `always_on` rules with irrelevant fields.
- `dev-rule` owns the rule lifecycle end to end: scaffolding from the canonical example, structural validation of live rules, and deterministic regeneration of `.agent/rules/index.md`.
- Vendored mirrors inside skills preserve self-contained packaging while keeping `.agent/schemas/rule/` as the single canonical edit surface.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local contract surface: `.agent/schemas/rule/rule.d.ts`
2. Local validator contract: `.agent/skills/dev-rule/scripts/quick_validate.py`
3. Local scaffolding contract: `.agent/skills/dev-rule/scripts/init_rule.py`
4. Local rules-index contract: `.agent/skills/dev-rule/scripts/update_index.py`
5. Live rule asset directory: `.agent/rules/`

</authoritative_reference_repository>

<modification_history>

| Date | Version | Classification | Description |
| :--- | :--- | :--- | :--- |
| 2026-03-01 | v1.1.0 | Optimization | Aligned the initial rule contract with the then-current prompt-structure guidance. |
| 2026-03-02 | v1.2.0 | Architecture | Added `execution_tier` and documented rule-asset parsing boundaries for reusable constraints. |
| 2026-04-03 | v1.3.0 | Governance | Replaced stale vendor-facing guidance with the current local owner-skill contract, relaxed rule-asset versioning to semantic version strings, and aligned the package with `dev-rule` scaffold, validation, and index tooling. |

</modification_history>
