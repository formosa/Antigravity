<document_purpose>
This document defines the shared owner-skill taxonomy and pattern used by Antigravity skills that directly create, update, validate, or index a governed agent asset family.
</document_purpose>

<owner_skill_pattern>

- `Owner Skill` means a skill that serves as the primary execution contract for a governed asset family.
- This pattern recognizes two sibling owner-skill subtypes for non-schema asset families:
  - `Runtime-Routed Owner Skill`: the direct-route owner contract for a reusable asset directory.
  - `Artifact-Centric Owner`: the dedicated utility for the creation, modification, and management lifecycle of one governed artifact family.
- To qualify as an `Owner Skill` under this pattern, a skill MUST satisfy all of the following:
  - the canonical schema `README.md` for the family names it in `primary_owner_skill`
  - the skill root `README.md` declares non-empty `owned_schema_ids`
  - the skill execution contract covers a validation-first lifecycle for the owned asset family
- `primary_owner_skill` is required schema-side metadata, but it is not sufficient by itself to classify a skill as an `Owner Skill` under this pattern.
- Runtime-routed owner skills:
  - directly manage a stable reusable asset directory
  - normally own scaffold, validation, and index or mirror synchronization responsibilities
  - use the naming convention `asset-<asset-family>`
- The current runtime-routed owner-skill family is `asset-rule`, `asset-skill`, and `asset-workflow`.
- Apply `asset-<asset-family>` only when the skill is both an `Owner Skill` and the direct-route execution contract for a reusable asset directory.
- Artifact-Centric Owners:
  - own one stable artifact family end to end
  - serve as the dedicated utility for creating, editing, regenerating, auditing, or otherwise managing those artifacts
  - may govern artifact paths without owning a directory index
  - should prefer the naming convention `artifact-<artifact-family>`
- `artifact-implementation-plan` is the current `Artifact-Centric Owner` for implementation-plan artifacts.
- Routing skills should prefer the `*-router` suffix when the contract is orchestration-first rather than owner-first.
- `agent-asset-router` is the current runtime-routed front-door router, and `agent-artifact-router` is the reserved future router name for artifact-centric routing.
- Standard non-owner, non-router skills should use lowercase hyphen-case naming.
- `dev-schema` is intentionally outside these non-schema owner subtypes because canonical schema discovery and maintenance are a different governance surface.
- `SKILL.md` is the execution contract. It defines trigger boundaries, ordered operating steps, constraints, and explicit resources.
- The root `README.md` is lifecycle governance only. It records authority order, schema relationships, and modification history.
- Canonical schemas live under `.agent/schemas/` and remain the single writable contract surface for asset-family definitions.
- Skill-local `resources/schema/` directories are vendored read-only mirrors copied from `.agent/schemas/` for packaging and local reference.
- Deterministic scripts belong in `scripts/` only when they reduce ambiguity, scaffold repeat-safe outputs, perform structural validation, or regenerate governed indexes.
- Owner skills follow a validation-first lifecycle: scaffold or open the target asset, apply bounded edits, validate the result, then sync mirrors or indexes before handoff.
- Owner skills must include RFQ or halt gates whenever the request is ambiguous enough that proceeding would silently redefine an asset class, ownership boundary, or canonical contract.
- A dedicated governance rule is warranted only when the skill declares non-empty `owned_schema_ids`, directly manages a stable asset directory, has cross-file lifecycle invariants that exceed a single asset's validator, and can use a trigger surface that does not overlap another governance rule.
- When a dedicated governance rule is warranted, name it `dev-<owned-asset>-governance` and scope it to the owned asset directory instead of mixing multiple governance surfaces into one rule.
- Front-door routers remain non-owner skills unless they later gain their own governed asset-family lifecycle.
- Split-lifecycle artifact families remain non-owner until one dedicated skill owns creation, modification, and management for that family.
- Single-purpose creators or consumers such as issue-report or issue-tracker skills, and brainstorm skills remain non-owner unless they later gain non-empty `owned_schema_ids` plus an owned full-lifecycle contract.
- Empty or index-only asset families may defer a dedicated governance rule until at least one live non-index asset exists or the lifecycle invariants exceed what the owner skill's scripts can enforce directly.

</owner_skill_pattern>

<role_exceptions>

- Front-door routing skills such as `agent-asset-router` should reuse the same governance vocabulary but remain orchestration-only unless deterministic routing can no longer be expressed directly in `SKILL.md`.
- Reserve `agent-artifact-router` as the canonical future name when artifact-centric routing expands beyond the current single dedicated owner.
- Canonical schema-authoring contracts such as `dev-schema` remain separate from the `Runtime-Routed Owner Skill` and `Artifact-Centric Owner` subtypes even when they satisfy the broader `Owner Skill` definition.
- Lightweight asset families may keep their artifact schema compact as long as governance, ownership, validation, and index responsibilities remain explicit.

</role_exceptions>
