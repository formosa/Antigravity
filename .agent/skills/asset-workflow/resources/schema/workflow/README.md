# DESIGN_JUSTIFICATION: Antigravity Workflow Assets v1.2.1

<document_purpose>
This document establishes the canonical local contract for Antigravity workflow assets and the owner-managed lifecycle used to scaffold, validate, and index those workflows.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: asset-workflow
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/workflow/workflow.d.ts`
2. `.agent/skills/asset-workflow/scripts/quick_validate.py`
3. `.agent/skills/asset-workflow/scripts/init_workflow.py`
4. `.agent/skills/asset-workflow/scripts/update_index.py`
5. `.agent/skills/asset-workflow/SKILL.md`
6. Vendored mirrors under `.agent/skills/<skill>/resources/schema/workflow/` are derived copies and must not override the canonical contract.
7. External references listed below are informative only and must not override the local contract unless the contract is intentionally revised.
</authority_order>

<schema_evaluation_and_justification>

- The frontmatter remains intentionally lightweight: `version` and `description` are required, while `name` stays optional so workflows remain easy to author and review.
- Canonical workflow files live under `.agent/workflows/` and must be governed from `.agent/schemas/workflow/` rather than by ad hoc local variants embedded inside skills.
- `asset-workflow` owns the workflow lifecycle end to end: scaffolding from the canonical example, structural validation, and deterministic regeneration of `.agent/workflows/index.md`.
- Vendored mirrors under skills preserve self-contained packaging without fragmenting authority away from the canonical workflow schema.
- A workflow index is part of the operational lifecycle, not an optional afterthought, because repeatable discovery boundaries are required for safe first-pass routing.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local contract surface: `.agent/schemas/workflow/workflow.d.ts`
2. Local validator contract: `.agent/skills/asset-workflow/scripts/quick_validate.py`
3. Local scaffolding contract: `.agent/skills/asset-workflow/scripts/init_workflow.py`
4. Local workflow-index contract: `.agent/skills/asset-workflow/scripts/update_index.py`
5. [Prompt design strategies | Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/prompting-strategies)

</authoritative_reference_repository>

<modification_history>

| Date | Version | Classification | Description |
| :--- | :--- | :--- | :--- |
| 2026-03-01 | v1.1.0 | Optimization | Enhanced `workflow.d.ts` with dense JSDoc annotations and schema versioning to align with the Gemini 3.1 Pro prompt optimization framework. |
| 2026-04-03 | v1.2.0 | Governance | Replaced stale authority guidance with the current local owner-skill contract, established canonical-plus-vendored-mirror governance, and aligned workflow lifecycle references with `asset-workflow` scaffold, validation, and index tooling. |
| 2026-04-03 | v1.2.1 | Governance | Updated the canonical workflow-governance metadata and authority references to the hardened `asset-*` owner-skill naming family so renamed runtime-routed owners remain the single authoritative surface. |

</modification_history>
