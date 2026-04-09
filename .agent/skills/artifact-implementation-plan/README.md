# artifact-implementation-plan Skill Lifecycle

<document_purpose>
This document records lifecycle governance, artifact ownership, canonical schema relationships, and modification history for the `artifact-implementation-plan` skill.
</document_purpose>

<authority_order>

1. `SKILL.md` - authoritative execution and routing contract for the skill.
2. This `README.md` - authoritative lifecycle, schema relationship, and modification history record for the skill.
3. `.agent/schemas/implementation-plan/` - canonical schema authority for implementation-plan artifact structure and governance.
4. `.agent/plans/` and `.agent/plans/processed/` - governed implementation-plan artifact surfaces managed by this skill.
5. Vendored schema mirrors under `resources/schema/` are read-only derived copies for packaging and local reference.
</authority_order>

<schema_relationships>

```yaml
schema_of_this_skill: skill
owned_schema_ids:
  - implementation-plan
consumed_schema_ids: []
mirror_root: resources/schema/
mirror_policy: read-only-derived-from-.agent/schemas
```

</schema_relationships>

<modification_history>

| Date       | Version | SemVer  | Classification        | Description                                                                                                                                                                                                                                                     |
| :--------- | :------ | :------ | :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-01 | 5.0.0   | initial | Baseline Capture      | Recorded the pre-existing skill version as the lifecycle baseline for governance enforcement.                                                                                                                                                                   |
| 2026-04-01 | 5.0.1   | patch   | Governance            | Added the root lifecycle README, declared canonical schema relationships, and migrated implementation-plan schema references to vendored mirrors.                                                                                                               |
| 2026-04-02 | 5.0.2   | patch   | Governance            | Clarified plan-trigger boundaries, added example prompts and resource-action annotations, and synchronized the vendored skill schema mirror to the repaired canonical contract.                                                                                 |
| 2026-04-02 | 5.1.0   | minor   | Rename                | Finalized the direct-noun owner contract name and updated active authority surfaces to use `artifact-implementation-plan`.                                                                                                                                      |
| 2026-04-03 | 5.2.0   | minor   | Behavioral Refinement | Reoriented plan generation toward patchability-first decomposition, required bounded atomic edit batches with local verification stop/go gates, and clarified canonical `.agent/schemas/implementation-plan/` authority relative to read-only vendored mirrors. |
| 2026-04-03 | 5.3.0   | minor   | Owner Subtype         | Promoted `artifact-implementation-plan` to the first `Artifact-Centric Owner`, declared ownership of the canonical `implementation-plan` schema, and aligned the skill package around end-to-end implementation-plan artifact governance.                       |
| 2026-04-03 | 6.0.0   | major   | Naming Hardening      | Hardened the artifact-owner naming contract around the `artifact-*` family, updated package authority surfaces to the renamed skill path, and prepared the implementation-plan package for mirror resynchronization under the new naming regime.                |
| 2026-04-07 | 6.0.1   | patch   | Runtime Target Refresh | Replaced stale `AGENTS.md`-first and `gemini-3.1-*` assumptions with the current runtime-target-backed `.agent/rules/` plus optional `~/.gemini/GEMINI.md` guidance, downgraded `.gemini/antigravity/brain/` to optional historical context, and synchronized the owner contract with the current implementation-plan schema surface. |

| 2026-04-09 | 6.0.2   | patch   | Package Hygiene | Removed ignored vendored-schema `.bak` mirrors and any transient cache residue from the packaged skill tree so the owner package contains only live durable assets. |

</modification_history>
