# md060-strict-aligner Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `md060-strict-aligner` skill.
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
owned_schema_ids: []
consumed_schema_ids: []
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```

</schema_relationships>

<modification_history>

| Date       | Version | SemVer  | Classification   | Description                                                                                                                                                                                        |
| :--------- | :------ | :------ | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-01 | 1.1.0   | initial | Baseline Capture | Recorded the pre-existing skill version as the lifecycle baseline for governance enforcement.                                                                                                      |
| 2026-04-01 | 1.1.1   | patch   | Governance       | Added the root lifecycle README, declared canonical schema relationships, and aligned the skill with vendored schema mirror packaging.                                                             |
| 2026-04-02 | 1.1.2   | patch   | Governance       | Clarified MD060 trigger boundaries, added example prompts, annotated the operational script as a run target, and synchronized the vendored skill schema mirror to the repaired canonical contract. |
| 2026-04-03 | 1.1.3   | patch   | Naming Alignment | Resynchronized the vendored skill-schema mirror after the canonical skill-governance contract adopted the hardened `asset-*`, `artifact-*`, and `*-router` naming families.                        |

| 2026-04-09 | 1.1.4   | patch   | Package Hygiene | Removed ignored vendored-schema `.bak` mirrors from the packaged skill tree so the formatter package contains only live durable assets. |

</modification_history>
