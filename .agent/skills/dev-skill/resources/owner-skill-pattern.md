<document_purpose>
This document defines the shared owner-skill pattern used by Antigravity skills that directly create, update, validate, or index a governed agent asset family.
</document_purpose>

<owner_skill_pattern>

- `SKILL.md` is the execution contract. It defines trigger boundaries, ordered operating steps, constraints, and explicit resources.
- The root `README.md` is lifecycle governance only. It records authority order, schema relationships, and modification history.
- Canonical schemas live under `.agent/schemas/` and remain the single writable contract surface for asset-family definitions.
- Skill-local `resources/schema/` directories are vendored read-only mirrors copied from `.agent/schemas/` for packaging and local reference.
- Deterministic scripts belong in `scripts/` only when they reduce ambiguity, scaffold repeat-safe outputs, perform structural validation, or regenerate governed indexes.
- Owner skills follow a validation-first lifecycle: scaffold or open the target asset, apply bounded edits, validate the result, then sync mirrors or indexes before handoff.
- Owner skills must include RFQ or halt gates whenever the request is ambiguous enough that proceeding would silently redefine an asset class, ownership boundary, or canonical contract.

</owner_skill_pattern>

<role_exceptions>

- Front-door routing skills such as `dev-agent-asset` should reuse the same governance vocabulary but remain orchestration-only unless deterministic routing can no longer be expressed directly in `SKILL.md`.
- Lightweight asset families may keep their artifact schema compact as long as governance, ownership, validation, and index responsibilities remain explicit.

</role_exceptions>
