# agent-asset-router Skill Lifecycle

<document_purpose>
This document records lifecycle governance, canonical schema relationships, and modification history for the `agent-asset-router` skill.
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
| 2026-04-02 | 1.0.0 | initial | Initial Release | Created the `agent-asset-router` front-door orchestration skill, declared the consumed `index` schema dependency, and established lifecycle governance for schema-first agent-asset routing. |
| 2026-04-02 | 1.0.1 | patch | Governance | Resynchronized the consumed index schema mirror after the canonical v1.1.0 hardening pass. |
| 2026-04-02 | 1.0.2 | patch | Routing | Updated the direct-route matrix and packaged references to target the renamed direct-noun owner skills. |
| 2026-04-03 | 1.0.3 | patch | Alignment | Tightened the router contract around discovery, deterministic owner handoff, and RFQ gates while explicitly preserving downstream owner skills as the authoritative execution contracts. |
| 2026-04-03 | 1.0.4 | patch | Routing | Added `asset-rule` to the direct-route matrix, removed `rule` from schema-first fallback routing, and resynchronized the consumed index-schema mirror after rules-index adoption updates. |
| 2026-04-03 | 1.0.5 | patch | Terminology | Aligned active router wording with the formal `Owner Skill` definition by switching broad owner-skill references to direct-route or dedicated-contract language while preserving owner-skill terminology only for actual owner-family cases. |
| 2026-04-03 | 1.0.6 | patch | Naming Convention | Clarified that `asset-rule`, `asset-skill`, and `asset-workflow` are the current runtime-routed owner-skill family using `asset-<asset-family>` naming while keeping `dev-schema` and the router itself outside that family. |
| 2026-04-03 | 2.0.0 | major | Naming Hardening | Hardened the router contract around the active `asset-*`, `artifact-*`, and `*-router` naming families, updated the direct-route matrix to use the renamed owner packages, and reserved `agent-artifact-router` as a future concept only. |
| 2026-04-03 | 2.1.0 | minor | Routing | Added `artifact-brainstorm` to the direct-route matrix, removed `brainstorm` from schema-first fallback routing, and aligned the router with brainstorm's promotion to an Artifact-Centric Owner. |
| 2026-04-04 | 2.2.0 | minor | Core Family Migration | Promoted `core-schema` as the active foundational schema-authoring contract, rewired schema-first fallback routing and direct-route guidance to the renamed package, and normalized legacy `dev-schema` requests to `core-schema`. |
| 2026-04-04 | 2.2.1 | patch | Tracker Owner Migration | Replaced the split tracker routes with `artifact-issue-tracker` as the sole direct-route Issues Tracker contract and aligned explicit tracker-maintenance wording with the new full-lifecycle owner skill. |
| 2026-04-04 | 2.3.0 | minor | Issue Report Owner Migration | Added `artifact-issue-report` as the canonical direct-route issue-report contract, expanded direct-route wording to cover report maintenance and validation, and retired `agent-create-issue-report` from the router's primary path. |

</modification_history>
