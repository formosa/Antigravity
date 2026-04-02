# dev-agent-asset Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `dev-agent-asset` skill.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/skill/` - canonical schema authority for the skill asset format.
4. `.agent/schemas/index/` - canonical schema authority for the `.agent/skills/index.md` registry consumed by this skill.
5. Vendored mirrors under `resources/schema/` - read-only derived copies bundled for self-contained packaging and local reference.
</authority_order>

<schema_relationships>
```yaml
schema_of_this_skill: skill
owned_schema_ids: []
consumed_schema_ids:
  - index
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date | Version | SemVer | Classification | Description |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-02 | 1.0.0 | initial | Initial Release | Created the `dev-agent-asset` front-door orchestration skill, declared the consumed `index` schema dependency, and established lifecycle governance for schema-first agent-asset routing. |

</modification_history>
