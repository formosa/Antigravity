# asset-rule Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `asset-rule` skill.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/rule/` - canonical schema authority for rule asset structure and governance.
4. `.agent/schemas/index/` - canonical schema authority for the rules directory index.
5. `.agent/skills/asset-rule/scripts/` - authoritative local tooling for rule scaffolding, validation, and index synchronization.
6. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>
```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - rule
consumed_schema_ids:
  - index
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date | Version | SemVer | Classification | Description |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-03 | 1.0.0 | initial | Initial Release | Created the `asset-rule` owner skill, declared ownership of the canonical `rule` schema plus the consumed `index` schema, and aligned the package around scaffold, validation, and rules-index tooling. |
| 2026-04-03 | 2.0.0 | major | Naming Hardening | Hardened the runtime-routed owner naming contract around the `asset-*` family, updated package authority surfaces to the renamed skill path, and prepared the rule package for mirror resynchronization under the new naming regime. |

</modification_history>
