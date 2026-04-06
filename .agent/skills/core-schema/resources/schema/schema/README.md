# DESIGN_JUSTIFICATION: Antigravity Schema Assets v1.21.1

<document_purpose>
This document establishes the canonical contract for Antigravity `.d.ts` schema assets and the rules for distributing those schemas as read-only vendored mirrors inside skills.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: core-schema
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/schema/schema.d.ts`
2. `.agent/skills/core-schema/scripts/validate_schema.py`
3. `.agent/skills/core-schema/scripts/scaffold_schema.py`
4. `.agent/skills/core-schema/scripts/update_index.py`
5. `.agent/skills/core-schema/SKILL.md`
6. Vendored mirrors under `.agent/skills/<skill>/resources/schema/<schema-id>/` are derived copies and must not override the canonical contract.
7. External references listed below are informative only and must not override the local contract unless the contract is intentionally revised.
</authority_order>

<schema_evaluation_and_justification>

- Strict TypeScript typing provides machine-readable contracts that validators and agents can reason over without guessing types.
- JSDoc annotations are required on non-obvious fields to reduce ambiguity during schema authoring and interpretation.
- Canonical schema directories in `.agent/schemas/` provide a single edit surface for each schema, reducing drift and conflicting local variants.
- Vendored mirrors under skills preserve package self-containment without fragmenting schema authority across many writable copies.
- Every schema README includes governance metadata and modification history so ownership, distribution policy, and version progression remain explicit and auditable.
- Owner-aware index synchronization keeps `.agent/schemas/index.md` aligned with both technical structure and stewardship boundaries.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local contract surface: `.agent/schemas/schema/schema.d.ts`
2. Local validator contract: `.agent/skills/core-schema/scripts/validate_schema.py`
3. Local scaffolding contract: `.agent/skills/core-schema/scripts/scaffold_schema.py`
4. Local index contract: `.agent/skills/core-schema/scripts/update_index.py`
5. [TypeScript Handbook — Declaration Files](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html)
6. [Google Gemini prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification   | Description                                                                                                                                                                                      |
| :--------- | :------ | :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-01 | v1.0.0  | Initial Release  | Constructed the initial schema-file contract for Antigravity `.d.ts` authoring.                                                                                                                  |
| 2026-04-01 | v1.20.3 | Repair           | Replaced stale issues-tracker content with the correct `SchemaFileDefinition` contract and aligned the local authority surface with dev-schema.                                                  |
| 2026-04-01 | v1.21.0 | Governance       | Established the canonical-plus-vendored-mirror distribution model and explicit primary ownership metadata for schema directories.                                                                |
| 2026-04-04 | v1.21.1 | Naming Alignment | Repointed the canonical schema-authoring authority surface from `dev-schema` to `core-schema` and preserved the schema contract unchanged while the foundational `core-*` family becomes active. |

</modification_history>