# agent-create-issue-report Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `agent-create-issue-report` compatibility shim.
</document_purpose>

<authority_order>
1. `SKILL.md` - authoritative compatibility-routing contract for the shim.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the shim.
3. `.agent/skills/artifact-issue-report/SKILL.md` - active owner contract for standalone issue-report artifacts.
4. `.agent/skills/agent-create-issue-report/scripts/validate_issue_report.py` - legacy CLI wrapper that delegates to the canonical validator.
5. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
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

| Date       | Version | SemVer | Classification   | Description |
| :--------- | :------ | :----- | :--------------- | :---------- |
| 2026-04-01 | 1.0.0   | initial | Baseline Capture | Recorded the pre-existing skill version as the lifecycle baseline for governance enforcement. |
| 2026-04-01 | 1.0.1   | patch   | Governance       | Added the root lifecycle README, declared canonical schema relationships, and migrated schema references to vendored mirrors. |
| 2026-04-02 | 1.0.2   | patch   | Governance       | Clarified trigger boundaries with example prompts, annotated each operational resource as read or run, and synchronized the vendored skill schema mirror to the repaired canonical contract. |
| 2026-04-03 | 1.0.3   | patch   | Naming Alignment | Resynchronized the vendored skill-schema mirror after the canonical skill-governance contract adopted the hardened `asset-*`, `artifact-*`, and `*-router` naming families. |
| 2026-04-04 | 1.1.0   | minor   | Compatibility Shim | Converted `agent-create-issue-report` into a staged compatibility alias that routes to `artifact-issue-report` and retains only the legacy validator CLI wrapper. |

</modification_history>
