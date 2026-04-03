# dev-skill Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `dev-skill` skill.
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
  - skill
consumed_schema_ids: []
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date | Version | SemVer | Classification | Description |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-01 | 2.1.0 | initial | Baseline Capture | Recorded the pre-existing skill version as the lifecycle baseline for governance enforcement. |
| 2026-04-01 | 2.2.0 | minor | Governance | Expanded scaffolding, validation, and packaging to require root skill READMEs and synced vendored schema mirrors. |
| 2026-04-02 | 2.2.1 | patch | Governance | Aligned the validator and canonical skill schema wording around required blocks, refreshed contract messaging to be version-agnostic, and synchronized the vendored skill schema mirror to the repaired canonical contract. |
| 2026-04-02 | 2.3.0 | minor | Rename | Finalized the direct-noun owner contract name and updated active authority surfaces to use `dev-skill`. |
| 2026-04-03 | 2.4.0 | minor | Owner Pattern | Added a shared owner-skill pattern resource and updated the active skill-authoring contract to reuse that pattern when scaffolding future owner skills. |

</modification_history>
