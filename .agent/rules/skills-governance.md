---
name: "skills-governance"
version: "2.0.1"
description: "Glob-scoped collection governance rule for the `.agent/skills/` directory, requiring root README updates, SemVer-aligned version bumps, vendored schema mirror synchronization, and lifecycle consistency across the full skills collection surface."
trigger: "glob"
globs: ".agent/skills/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. Root README Update Required: When any file under `.agent/skills/<skill-name>/` changes, the agent MUST update that skill's root `README.md` in the same task.
2. Version Synchronization Required: The changed skill's `SKILL.md` version MUST be incremented in the same task, and the latest row in the root `README.md` `<modification_history>` table MUST match that new version exactly.
3. Strict SemVer Classification: Use `major` for breaking trigger-contract or incompatible input/output changes, `minor` for additive non-breaking capability expansion, and `patch` for README updates, mirror syncs, validator/script hardening, wording cleanup, or non-breaking refactors.
4. Modification History Fidelity: The latest `README.md` history row MUST describe the actual change set with concrete details; placeholder or generic text is not acceptable.
5. Canonical Schema Ownership: Skill-local schema mirrors under `resources/schema/<schema-id>/` are read-only derived copies. Agents MUST NOT hand-edit these mirrors.
6. Mirror Sync Requirement: If a skill consumes or owns a schema, agents MUST refresh the skill-local schema mirrors from `.agent/schemas/` before completing the task.
7. Canonical Schema Change Propagation: If a canonical schema in `.agent/schemas/` changes, every dependent skill mirror MUST be re-synced and each affected skill MUST receive at least a patch version bump plus a matching README history entry.
8. Skills Index Regeneration Requirement: When any skill directory, skill routing description, or skill inventory changes under `.agent/skills/`, regenerate `.agent/skills/index.md` with `python .agent/skills/asset-skill/scripts/update_index.py` before completing the task.

</constraints>

<verification_step>
Before finishing any task that changes files under `.agent/skills/`, silently verify: the touched skill has an updated root `README.md`; `SKILL.md` version and the latest README history version match; the README SemVer classification matches the numeric version delta; every required schema mirror exists under `resources/schema/<schema-id>/`; no vendored mirror was hand-edited instead of re-synced; `.agent/skills/index.md` matches the generated output; and canonical schema changes were propagated to every dependent skill with at least a patch bump.
</verification_step>
