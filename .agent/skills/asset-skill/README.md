# asset-skill Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `asset-skill` skill.
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
| 2026-04-02 | 2.3.0 | minor | Rename | Finalized the direct-noun owner contract name and updated active authority surfaces to use `asset-skill`. |
| 2026-04-03 | 2.4.0 | minor | Owner Pattern | Added a shared owner-skill pattern resource and updated the active skill-authoring contract to reuse that pattern when scaffolding future owner skills. |
| 2026-04-03 | 2.4.1 | patch | Owner Pattern | Refined the shared owner-skill pattern to define when dedicated `dev-<owned-asset>-governance` rules are warranted and updated the execution contract to reuse that selection criteria. |
| 2026-04-03 | 2.4.2 | patch | Owner Pattern | Formalized `Owner Skill` as a term requiring schema-side ownership metadata, non-empty `owned_schema_ids`, and an owned asset-family lifecycle while preserving routers and consumer-only skills as non-owner exceptions. |
| 2026-04-03 | 2.4.3 | patch | Naming Convention | Codified `asset-<asset-family>` as the runtime-routed owner-skill naming family for `rule`, `skill`, and `workflow`, added soft validator guidance for future owner skills, and aligned skill-authoring instructions with that convention. |
| 2026-04-03 | 2.5.0 | minor | Owner Taxonomy | Added the `Artifact-Centric Owner` subtype beside runtime-routed owner skills, aligned skill-authoring guidance with the broadened taxonomy, and updated validation/scaffolding references so non-runtime artifact owners are treated as first-class owner contracts. |
| 2026-04-03 | 3.0.0 | major | Naming Hardening | Hardened the active skill naming families around `asset-*`, `artifact-*`, and `*-router`, updated validator and scaffolder guidance to prefer those families, and aligned the renamed owner and router skill packages to the new contract. |
| 2026-04-03 | 3.0.1 | patch | Owner Taxonomy | Updated the shared owner-skill taxonomy resource to recognize `artifact-brainstorm` as an Artifact-Centric Owner and removed brainstorm from the non-owner exception list. |
| 2026-04-04 | 3.1.0 | minor | Core Family | Added the foundational `core-*` family to the shared skill-authoring taxonomy, taught the active scaffolding contract when to classify a skill as a `Foundational Core Contract`, and aligned `core-schema` migration guidance with the owner-pattern resource. |
| 2026-04-04 | 3.2.0 | minor | Collection Governance | Replaced the old `dev-<owned-asset>-governance` convention with `<plural-directory>-governance` for collection-scoped directory governance rules and aligned the active skill-authoring contract with the renamed governance-rule family. |
| 2026-04-04 | 3.2.1 | patch | Tracker Owner Naming | Recognized `artifact-issue-tracker` as the established Artifact-Centric Owner for the `issues-tracker` schema, taught the validator about the canonical singular owner name, and aligned skill-authoring guidance with that exception. |
| 2026-04-04 | 3.2.2 | patch | Issue Report Owner Naming | Recognized `artifact-issue-report` as the established Artifact-Centric Owner for the `issue` schema, taught the validator about the canonical owner-name override, and aligned the shared owner-skill pattern with the completed issue-report migration. |

</modification_history>
