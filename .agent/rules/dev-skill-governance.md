---
name: "dev-skill-governance"
version: "1.3.0"
description: "Glob-scoped lifecycle governance rule for `.agent/skills/` packages requiring root README updates, SemVer-aligned version bumps, and vendored schema mirror synchronization."
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
8. Skills Index Non-Requirement: Until the repository has a deterministic skills-index generator, this rule does not by itself require `.agent/skills/index.md` regeneration for ordinary skill-internal edits.

</constraints>

<verification_step>
Before finishing any task that changes files under `.agent/skills/`, silently verify: the touched skill has an updated root `README.md`; `SKILL.md` version and the latest README history version match; the README SemVer classification matches the numeric version delta; every required schema mirror exists under `resources/schema/<schema-id>/`; no vendored mirror was hand-edited instead of re-synced; and canonical schema changes were propagated to every dependent skill with at least a patch bump.
</verification_step>
