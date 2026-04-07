---
name: agent-asset-router
version: 2.3.1
description: Routes Antigravity agent-asset work to the correct dedicated execution contract using the local skills registry, deterministic direct-route handoff, and schema-first classification for uncovered asset families. Use when the user frames the task at the agent-asset level, when the correct direct-route skill is unclear or mixed, or when determining whether schema work must happen first. Legacy `dev-schema` requests normalize to `core-schema` during routing. Do not use when the request is already expressed in the exact vocabulary of a dedicated execution contract such as direct skill scaffolding, direct rule authoring, canonical schema authoring, workflow creation, implementation-plan generation, brainstorm artifact maintenance, explicit issues-tracker lifecycle management, or standalone issue-report generation, maintenance, or validation.
---

<when_to_use>

- Use when the user asks for an Antigravity agent asset and the request is framed at the asset layer rather than in the exact language of a dedicated execution contract.
- Use when the request mixes asset-authoring concerns, such as asking for a new agent asset category, asking whether a report should become a skill or schema, or asking for one front-door skill to cover several asset families.
- Use when the request needs schema-first classification for asset families that do not yet have a dedicated owner skill.
- Do not use when the request is already clearly and narrowly expressed as direct skill scaffolding, canonical schema authoring, workflow creation, implementation-plan drafting, brainstorm artifact creation or maintenance, explicit issues-tracker lifecycle management, or standalone issue-report generation, maintenance, or validation.
- Do not use when the task is an ordinary project feature change outside `.agent/`.
- `asset-rule`, `asset-skill`, and `asset-workflow` are the current direct-route runtime-routed owner skills and intentionally follow the `asset-<asset-family>` naming family.
- Example prompt: "Create a front-door skill for agent assets and make sure it routes to the right owner contracts."
- Example prompt: "I need a new agent asset for tracking task execution state, but I do not know whether that starts as a schema or a skill."
- Example prompt: "Should this new report format become a skill, a schema, or both?"
</when_to_use>

<how_to_use>

1. Resolve the request into one of three modes before doing any asset mutation:
   - Direct dedicated-contract match
   - Schema-first classification for an uncovered asset family
   - RFQ because the request is still ambiguous or asks for incompatible outcomes in one pass
2. Read `.agent/skills/index.md` first and treat it as the discovery registry only. Use it to shortlist the most likely direct-route skill by intent, then open the linked `SKILL.md` before following any exact execution contract.
3. Apply the direct-route matrix:
   - `asset-skill` for new or existing skill folders under `.agent/skills/`
   - `asset-rule` for reusable rule assets under `.agent/rules/`
   - `core-schema` for canonical `.agent/schemas/<schema-id>/` work and schema index regeneration
   - `asset-workflow` for reusable workflow assets under `.agent/workflows/`
   - `artifact-implementation-plan` for governed implementation-plan artifacts under `.agent/plans/`
   - `artifact-brainstorm` for governed brainstorm artifacts such as `brainstorm.md`
   - `artifact-issue-tracker` for blank tracker initialization, tracker refresh and migration, or tracker validation and audit
   - `artifact-issue-report` for standalone single-issue report generation, maintenance, or validation
   - Treat `asset-rule`, `asset-skill`, and `asset-workflow` as the runtime-routed owner-skill family that intentionally uses `asset-<asset-family>` naming; treat `artifact-implementation-plan`, `artifact-brainstorm`, `artifact-issue-tracker`, and `artifact-issue-report` as the active `artifact-<artifact-family>` owners; treat `core-schema` as the active foundational `core-*` contract; keep this router outside those naming families
   - Treat `agent-artifact-router` as a reserved future route name only; do not create it or route to it unless a later contract explicitly introduces that router
4. If the request is a direct dedicated-contract match, stop using this skill as the primary execution contract. Read the selected `SKILL.md`, hand off explicitly to that path, and do not restate or supersede the downstream execution contract.
5. Apply the schema-first fallback matrix only when no dedicated owner skill exists yet:
   - Route `task`, `index`, `walkthrough`, `security-policy`, and `gemini` through `core-schema`
   - Treat the example artifact or existing canonical example as the required input for schema authoring
   - After the schema work is clear, determine whether a downstream dedicated owner skill is still needed; do not invent that skill unless the request actually requires one
   - Normalize legacy `dev-schema` wording to `core-schema` before handing off to the downstream contract
6. Enforce hard RFQ gates before proceeding:
   - If the request still maps cleanly to more than one direct-route skill after reading the registry and candidate `SKILL.md` files, halt with `RFQ` naming the candidate skills and the missing discriminator
   - If the user asks to define a new asset class and also author the final asset instance in the same pass, halt with `RFQ` and require the class/contract decision first
   - If schema-first routing is required but no governing example artifact or authoritative sample is available, halt with `RFQ` naming the missing example
   - If the request asks for outputs that belong to conflicting direct-route skills in a single atomic change, halt with `RFQ` and split the workstreams explicitly
7. Keep this skill orchestration-only and instruction-only by default. Do not add local scripts unless deterministic routing can no longer be expressed directly in `SKILL.md`.
8. Before completing the task, verify that the chosen owner path is explicit, that no extra asset family was invented silently, and that all generated or modified files still defer to their canonical owner contracts.
</how_to_use>

<constraints>
- Do not duplicate or supersede the procedural contract of existing direct-route skills; route to them and use them as authoritative once selected.
- Do not invent new asset families, schema IDs, or owner skills without a demonstrated gap grounded in existing `.agent/` contracts.
- Do not guess when the request still fits multiple direct-route skills after reading the skills index and the candidate `SKILL.md` files; issue `RFQ` instead.
- Do not define a new asset class and produce a governed final artifact instance in one unqualified pass.
- Do not hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/` instead.
- Keep all referenced paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>

- Read `.agent/skills/index.md` first to shortlist the correct direct-route skill before opening any candidate execution contract.
- Read `.agent/skills/asset-skill/SKILL.md` when the request is specifically about skill creation or refinement.
- Read `.agent/skills/asset-rule/SKILL.md` when the request is specifically about rule creation, refinement, validation, or rules-index maintenance.
- Read `.agent/skills/core-schema/SKILL.md` when the request requires canonical schema authoring or schema-first fallback routing.
- Read `.agent/skills/asset-workflow/SKILL.md` when the request is specifically about workflow assets.
- Read `.agent/skills/artifact-implementation-plan/SKILL.md` when the request is specifically about implementation-plan artifacts.
- Read `.agent/skills/artifact-brainstorm/SKILL.md` when the request is specifically about brainstorm artifacts.
- Read `.agent/skills/artifact-issue-tracker/SKILL.md` when the request is to initialize, refresh, migrate, validate, or audit an Issues Tracker.
- Read `.agent/skills/artifact-issue-report/SKILL.md` when the request is to generate, maintain, migrate, or validate a standalone single-issue report.
- Read `.agent/skills/asset-skill/resources/owner-skill-pattern.md` to preserve shared owner-skill governance vocabulary while keeping this router orchestration-only.
- Read `resources/schema/skill/skill.d.ts` to confirm the required skill frontmatter and XML block contract.
- Read `resources/schema/index/index.d.ts` to verify the directory-index structure used by `.agent/skills/index.md`.
- Read `resources/schema/index/example.md` to preserve the canonical section order and authority-boundary language for the skills registry.
</resources_reference>
