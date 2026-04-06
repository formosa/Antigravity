# artifact-brainstorm Skill Lifecycle

<document_purpose>
This document records lifecycle governance, artifact ownership, canonical schema relationships, and modification history for the `artifact-brainstorm` skill.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/brainstorm/` - canonical schema authority for brainstorm artifact structure, governance, seed content, and source-reference basis.
4. `brainstorm.md` or an explicitly supplied alternate output path - governed brainstorm artifact surface managed by this skill.
5. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>
```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - brainstorm
consumed_schema_ids: []
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date       | Version | SemVer  | Classification             | Description                                                                                                                                                                                                                  |
| :--------- | :------ | :------ | :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-03 | 1.0.0   | initial | Owner Migration            | Created `artifact-brainstorm` as the Artifact-Centric Owner for brainstorm artifacts, migrated the lifecycle contract from the deprecated predecessor package, and aligned ownership with the canonical `brainstorm` schema. |
| 2026-04-03 | 1.0.1   | patch   | Source Reference Migration | Updated the skill package to use `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml` as the schema-owned source reference and aligned the packaged mirror with the canonical schema asset.                         |
| 2026-04-04 | 1.0.2   | patch   | Core Routing               | Repointed canonical schema-authoring guidance from `dev-schema` to `core-schema` and aligned the brainstorm owner contract with the new foundational `core-*` family terminology.                                            |

</modification_history>