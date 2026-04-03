# dev-workflow Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `dev-workflow` skill.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/workflow/` - canonical schema authority for workflow asset structure and governance.
4. `.agent/schemas/index/` - canonical schema authority for the workflow directory index.
5. `.agent/skills/dev-workflow/scripts/` - authoritative local tooling for workflow scaffolding, validation, and index synchronization.
6. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>
```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - workflow
consumed_schema_ids:
  - index
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date | Version | SemVer | Classification | Description |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-01 | 1.0.0 | initial | Baseline Capture | Recorded the pre-existing skill version as the lifecycle baseline for governance enforcement. |
| 2026-04-01 | 1.0.1 | patch | Governance | Added the root lifecycle README, declared canonical schema relationships, and migrated workflow schema references to vendored mirrors. |
| 2026-04-02 | 1.0.2 | patch | Governance | Clarified workflow-trigger boundaries, annotated schema resources as read operations, removed unused scaffold artifacts, and synchronized the vendored skill schema mirror to the repaired canonical contract. |
| 2026-04-02 | 1.1.0 | minor | Rename | Finalized the direct-noun owner contract name and updated active authority surfaces to use `dev-workflow`. |
| 2026-04-03 | 1.2.0 | minor | Owner Contract | Promoted `dev-workflow` to a full owner contract for workflow assets by declaring ownership of the canonical workflow schema, adding the consumed workflow-index contract, and aligning the package around scaffold, validation, and index-sync tooling. |
| 2026-04-03 | 1.2.1 | patch | Mirror Sync | Resynchronized the consumed index-schema mirror after `.agent/rules/index.md` adopted the full-form directory-index contract. |

</modification_history>
