# artifact-issue-report Skill Lifecycle

<document_purpose>
This document records lifecycle governance, artifact ownership, canonical schema relationships, and modification history for the `artifact-issue-report` skill.
</document_purpose>

<authority_order>

1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/issue/` - canonical schema authority for issue-report structure, validation expectations, and lifecycle governance.
4. `.agent/schemas/issues-tracker/` - canonical schema authority for the consumed tracker source contract.
5. The target issue-report artifact path supplied by the task - governed artifact surface managed by this skill.
6. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>

```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - issue
consumed_schema_ids:
  - issues-tracker
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```

</schema_relationships>

<modification_history>

| Date       | Version | SemVer  | Classification     | Description                                                                                                                                                                                                           |
| :--------- | :------ | :------ | :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-04 | 1.0.0   | initial | Owner Migration    | Created `artifact-issue-report` as the Artifact-Centric Owner for issue-report artifacts, migrated canonical validator/resources into the new package, and aligned ownership with the canonical `issue` schema.       |
| 2026-04-04 | 1.0.1   | patch   | Sole Owner Cleanup | Removed the deprecated legacy issue-report compatibility package from the active repository contract and retained `artifact-issue-report` as the sole documented owner and validator path for issue-report artifacts. |
| 2026-04-08 | 1.0.2   | patch   | Compatibility Refresh | Resynchronized the consumed `issues-tracker` schema mirrors after the Antigravity 1.21.9 compatibility refresh and updated the active issue-report template/example guidance to the current platform and model defaults. |

| 2026-04-09 | 1.0.3   | patch   | Package Hygiene | Removed ignored vendored-schema `.bak` mirrors and transient script cache residue from the packaged skill tree so the owner package contains only live durable assets. |

</modification_history>
