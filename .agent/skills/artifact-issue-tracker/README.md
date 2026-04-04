# artifact-issue-tracker Skill Lifecycle

<document_purpose>
This document records lifecycle governance, artifact ownership, canonical schema relationships, and modification history for the `artifact-issue-tracker` skill.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/issues-tracker/` - canonical schema authority for Issues Tracker structure, validation profiles, and lifecycle governance.
4. The target Issues Tracker artifact path supplied by the task - governed artifact surface managed by this skill.
5. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>
```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - issues-tracker
consumed_schema_ids: []
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```
</schema_relationships>

<modification_history>

| Date       | Version | SemVer  | Classification  | Description |
| :--------- | :------ | :------ | :-------------- | :---------- |
| 2026-04-04 | 1.0.0   | initial | Owner Migration | Created `artifact-issue-tracker` as the Artifact-Centric Owner for Issues Tracker artifacts, consolidated the legacy create and update tracker contracts into one full-lifecycle skill, and aligned ownership with the canonical `issues-tracker` schema. |
| 2026-04-04 | 1.0.1   | patch   | Owner Reference Alignment | Repointed standalone issue-report routing guidance from `agent-create-issue-report` to `artifact-issue-report` and synchronized the tracker owner contract with the staged issue-report owner migration. |

</modification_history>
