---
name: dev-agent-asset
version: 1.0.3
description: Routes Antigravity agent-asset work to the correct owner contract using the local skills registry, deterministic owner-skill handoff, and schema-first classification for uncovered asset families. Use when the user frames the task at the agent-asset level, when the correct owner skill is unclear or mixed, or when determining whether schema work must happen first. Do not use when the request is already expressed in the exact vocabulary of a dedicated owner contract such as direct skill scaffolding, canonical schema authoring, workflow creation, implementation-plan generation, explicit issues-tracker maintenance, or standalone issue-report generation.
---

<when_to_use>
- Use when the user asks for an Antigravity agent asset and the request is framed at the asset layer rather than in the exact language of a dedicated owner skill.
- Use when the request mixes asset-authoring concerns, such as asking for a new agent asset category, asking whether a report should become a skill or schema, or asking for one front-door skill to cover several asset families.
- Use when the request needs schema-first classification for asset families that do not yet have a dedicated owner skill.
- Do not use when the request is already clearly and narrowly expressed as direct skill scaffolding, canonical schema authoring, workflow creation, implementation-plan drafting, explicit issues-tracker maintenance, or standalone issue-report generation.
- Do not use when the task is an ordinary project feature change outside `.agent/`.
- Example prompt: "Create a front-door skill for agent assets and make sure it routes to the right owner contracts."
- Example prompt: "I need a new agent asset for tracking task execution state, but I do not know whether that starts as a schema or a skill."
- Example prompt: "Should this new report format become a skill, a schema, or both?"
</when_to_use>

<how_to_use>
1. Resolve the request into one of three modes before doing any asset mutation:
   - Direct owner-skill match
   - Schema-first classification for an uncovered asset family
   - RFQ because the request is still ambiguous or asks for incompatible outcomes in one pass
2. Read `.agent/skills/index.md` first and treat it as the discovery registry only. Use it to shortlist the most likely owner skill by intent, then open the linked owner `SKILL.md` before following any exact execution contract.
3. Apply the direct-route matrix:
   - `dev-skill` for new or existing skill folders under `.agent/skills/`
   - `dev-schema` for canonical `.agent/schemas/<schema-id>/` work and schema index regeneration
   - `dev-workflow` for reusable workflow assets under `.agent/workflows/`
   - `dev-implementation-plan` for governed implementation-plan artifacts under `.agent/plans/`
   - `agent-create-issues-tracker` for blank tracker initialization
   - `agent-update-issues-tracker` for tracker refresh, migration, or comparative-analysis updates
   - `agent-create-issue-report` for standalone single-issue reports
4. If the request is a direct owner-skill match, stop using this skill as the primary execution contract. Read the selected owner `SKILL.md`, hand off explicitly to that owner path, and do not restate or supersede the downstream execution contract.
5. Apply the schema-first fallback matrix only when no dedicated owner skill exists yet:
   - Route `rule`, `task`, `index`, `walkthrough`, `security-policy`, `brainstorm`, `gemini`, and `uuid_registry` through `dev-schema`
   - Treat the example artifact or existing canonical example as the required input for schema authoring
   - After the schema work is clear, determine whether a downstream dedicated owner skill is still needed; do not invent that skill unless the request actually requires one
6. Enforce hard RFQ gates before proceeding:
   - If the request still maps cleanly to more than one owner after reading the registry and candidate `SKILL.md` files, halt with `RFQ` naming the candidate owners and the missing discriminator
   - If the user asks to define a new asset class and also author the final asset instance in the same pass, halt with `RFQ` and require the class/contract decision first
   - If schema-first routing is required but no governing example artifact or authoritative sample is available, halt with `RFQ` naming the missing example
   - If the request asks for outputs that belong to conflicting owner skills in a single atomic change, halt with `RFQ` and split the workstreams explicitly
7. Keep this skill orchestration-only and instruction-only by default. Do not add local scripts unless deterministic routing can no longer be expressed directly in `SKILL.md`.
8. Before completing the task, verify that the chosen owner path is explicit, that no extra asset family was invented silently, and that all generated or modified files still defer to their canonical owner contracts.
</how_to_use>

<constraints>
- Do not duplicate or supersede the procedural contract of existing owner skills; route to them and use them as authoritative once selected.
- Do not invent new asset families, schema IDs, or owner skills without a demonstrated gap grounded in existing `.agent/` contracts.
- Do not guess when the request still fits multiple owner skills after reading the skills index and the candidate `SKILL.md` files; issue `RFQ` instead.
- Do not define a new asset class and produce a governed final artifact instance in one unqualified pass.
- Do not hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/` instead.
- Keep all referenced paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>
- Read `.agent/skills/index.md` first to shortlist the correct owner skill before opening any candidate execution contract.
- Read `.agent/skills/dev-skill/SKILL.md` when the request is specifically about skill creation or refinement.
- Read `.agent/skills/dev-schema/SKILL.md` when the request requires canonical schema authoring or schema-first fallback routing.
- Read `.agent/skills/dev-workflow/SKILL.md` when the request is specifically about workflow assets.
- Read `.agent/skills/dev-implementation-plan/SKILL.md` when the request is specifically about implementation-plan artifacts.
- Read `.agent/skills/agent-create-issues-tracker/SKILL.md` when the request is to initialize a blank issues tracker.
- Read `.agent/skills/agent-update-issues-tracker/SKILL.md` when the request is to refresh, migrate, or expand an existing issues tracker.
- Read `.agent/skills/agent-create-issue-report/SKILL.md` when the request is to author a standalone single-issue report.
- Read `.agent/skills/dev-skill/resources/owner-skill-pattern.md` to preserve shared owner-skill governance vocabulary while keeping this router orchestration-only.
- Read `resources/schema/skill/skill.d.ts` to confirm the required skill frontmatter and XML block contract.
- Read `resources/schema/index/index.d.ts` to verify the directory-index structure used by `.agent/skills/index.md`.
- Read `resources/schema/index/example.md` to preserve the canonical section order and authority-boundary language for the skills registry.
</resources_reference>
