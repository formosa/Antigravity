# DESIGN_JUSTIFICATION: Antigravity dev-create-schema Assets v1.20.3

<document_purpose>
This document establishes the verified architectural pattern and authority order for the
`dev-create-schema` skill's internal schema bundle, which governs how Antigravity `.d.ts`
schema files are authored, validated, and indexed.
</document_purpose>

<authority_order>
1. `resources/schema/schema.d.ts` — Authoritative TypeScript interface contract for all Antigravity schema files.
2. `scripts/validate_schema.py` — Authoritative validation contract; determines what constitutes a structurally correct schema.
3. `scripts/scaffold_schema.py` — Authoritative scaffolding contract for initial schema directory layout.
4. `.agent/skills/dev-create-schema/SKILL.md` — Authoritative skill instruction surface.
5. External references listed below are informative only and must not override the local contract unless the contract is intentionally revised.
</authority_order>

<schema_evaluation_and_justification>
- **Strict TypeScript typing:** The `.d.ts` format provides machine-readable contracts that the validator can check structurally and that agents can reason over without guessing types.
- **JSDoc annotations:** Required on all non-obvious fields to reduce ambiguity during schema authoring and agent interpretation.
- **Changelog tracking:** Each `.d.ts` file carries an inline changelog comment so that schema version history remains co-located with the definition rather than in a separate document.
- **README as justification surface:** Every schema directory includes a `README.md` that records the authority order, design rationale, and modification history, preventing silent drift.
- **Index synchronization:** The `update_index.py` script ensures the `.agent/schemas/index.md` always reflects current schema state after any create or update operation.
</schema_evaluation_and_justification>

<authoritative_reference_repository>
1. Local contract surface: `resources/schema/schema.d.ts`
2. Local validator contract: `scripts/validate_schema.py`
3. Local scaffolding contract: `scripts/scaffold_schema.py`
4. [TypeScript Handbook — Declaration Files](https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html) — Authoritative reference for `.d.ts` interface authoring.
5. [Google Gemini prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) — Informative reference for agentic optimization of schema annotations.
</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification  | Description                                                                                                                                                                                    |
| :--------- | :------ | :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-01 | v1.0.0  | Initial Release | Constructed initial `schema.d.ts` per Antigravity v1.18.3 standards for Issues Tracker artifacts.                                                                                             |
| 2026-04-02 | v1.20.3 | Repair          | Replaced stale Issues Tracker content with correct `SchemaFileDefinition` contract; updated authority order, reference repository, and design justification to reflect dev-create-schema scope. |

</modification_history>
