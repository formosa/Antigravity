<document_purpose>
This document defines the shared owner-skill pattern used by Antigravity skills that directly create, update, validate, or index a governed agent asset family.
</document_purpose>

<owner_skill_pattern>

- `Owner Skill` means a skill that serves as the primary execution contract for a governed asset family.
- To qualify as an `Owner Skill` under this pattern, a skill MUST satisfy all of the following:
  - the canonical schema `README.md` for the family names it in `primary_owner_skill`
  - the skill root `README.md` declares non-empty `owned_schema_ids`
  - the skill directly manages a stable asset directory with validation-first lifecycle responsibilities such as scaffolding, validation, and index or mirror synchronization
- `primary_owner_skill` is required schema-side metadata, but it is not sufficient by itself to classify a skill as an `Owner Skill` under this pattern.
- Runtime-routed owner skills use the naming convention `dev-<asset-family>`.
- The current runtime-routed owner-skill family is `dev-rule`, `dev-skill`, and `dev-workflow`.
- Apply `dev-<asset-family>` only when the skill is both an `Owner Skill` and the direct-route execution contract for a reusable asset directory.
- `dev-schema` is intentionally outside this naming family because canonical schema discovery and maintenance are a different governance surface, not a runtime-routed asset family.
- `SKILL.md` is the execution contract. It defines trigger boundaries, ordered operating steps, constraints, and explicit resources.
- The root `README.md` is lifecycle governance only. It records authority order, schema relationships, and modification history.
- Canonical schemas live under `.agent/schemas/` and remain the single writable contract surface for asset-family definitions.
- Skill-local `resources/schema/` directories are vendored read-only mirrors copied from `.agent/schemas/` for packaging and local reference.
- Deterministic scripts belong in `scripts/` only when they reduce ambiguity, scaffold repeat-safe outputs, perform structural validation, or regenerate governed indexes.
- Owner skills follow a validation-first lifecycle: scaffold or open the target asset, apply bounded edits, validate the result, then sync mirrors or indexes before handoff.
- Owner skills must include RFQ or halt gates whenever the request is ambiguous enough that proceeding would silently redefine an asset class, ownership boundary, or canonical contract.
- A dedicated governance rule is warranted only when the skill declares non-empty `owned_schema_ids`, directly manages a stable asset directory, has cross-file lifecycle invariants that exceed a single asset's validator, and can use a trigger surface that does not overlap another governance rule.
- When a dedicated governance rule is warranted, name it `dev-<owned-asset>-governance` and scope it to the owned asset directory instead of mixing multiple governance surfaces into one rule.
- Orchestration-only or consumer-only skills such as `dev-agent-asset`, `dev-implementation-plan`, issue-report or issue-tracker skills, and brainstorm skills remain non-owner skills unless they later gain non-empty `owned_schema_ids` plus an owned asset-family lifecycle.
- Empty or index-only asset families may defer a dedicated governance rule until at least one live non-index asset exists or the lifecycle invariants exceed what the owner skill's scripts can enforce directly.

</owner_skill_pattern>

<role_exceptions>

- Front-door routing skills such as `dev-agent-asset` should reuse the same governance vocabulary but remain orchestration-only unless deterministic routing can no longer be expressed directly in `SKILL.md`.
- Lightweight asset families may keep their artifact schema compact as long as governance, ownership, validation, and index responsibilities remain explicit.

</role_exceptions>
