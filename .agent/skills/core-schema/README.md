# core-schema Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `core-schema` skill. Legacy `dev-schema` requests now route to this renamed foundational contract.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. Canonical schema directories listed in `<schema_relationships>` under `.agent/schemas/`.
4. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>
```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - schema
  - index
  - gemini
  - security-policy
  - task
  - uuid_registry
  - walkthrough
consumed_schema_ids: []
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date       | Version | SemVer  | Classification   | Description                                                                                                                                                                                           |
| :--------- | :------ | :------ | :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-01 | 2.1.0   | initial | Baseline Capture | Recorded the pre-existing skill version as the lifecycle baseline for governance enforcement.                                                                                                         |
| 2026-04-01 | 2.2.0   | minor   | Governance       | Expanded canonical schema governance to require owner metadata, vendored-mirror distribution, and owner-aware schema index regeneration.                                                              |
| 2026-04-02 | 2.2.1   | patch   | Governance       | Replaced Unicode status markers with ASCII-safe schema-tool output, removed the unused scaffold example script, and synchronized the vendored skill schema mirror to the repaired canonical contract. |
| 2026-04-02 | 2.3.0   | minor   | Rename           | Finalized the direct-noun owner contract name and updated active authority surfaces to use `dev-schema`.                                              |
| 2026-04-03 | 2.3.1   | patch   | Alignment        | Aligned schema-authoring guidance with the shared owner-skill pattern so canonical schema governance stays consistent with validation-first owner contracts. |
| 2026-04-03 | 2.3.2   | patch   | Index Terminology | Renamed the generated schema-index column from `Owner Skill` to `Primary Skill` so the registry reflects `primary_owner_skill` without implying every listed skill satisfies the formal `Owner Skill` definition. |
| 2026-04-03 | 2.3.3   | patch   | Naming Alignment | Updated the active schema-authoring contract to reference the renamed shared skill-tooling package and resynchronized the vendored skill-schema mirror after the canonical skill-governance naming hardening. |
| 2026-04-04 | 3.0.0   | major   | Core Family Rename | Promoted the schema-authoring contract into the foundational `core-*` family as `core-schema`, updated active authority surfaces to the renamed package path, and preserved explicit legacy routing guidance for `dev-schema` requests. |
| 2026-04-04 | 3.1.0   | minor   | Ownership Alignment | Expanded the declared `owned_schema_ids` set to match the canonical schemas now governed by `core-schema` and resynchronized the packaged schema mirrors so the skill remains self-contained and ownership-accurate after the migration. |

</modification_history>

