# Agent Skills Index

> Consolidated registry of skill assets in `.agent/skills/`.
>
> Scope: discovery, first-pass selection, and quick routing across current skill contracts.
>
> Total skills: `11`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked skill definition, the linked `SKILL.md` is authoritative.

## Use This Index

1. Use the selection map to identify the most likely skill by task intent.
2. Use the manifest to confirm the skill category, definition path, and best-fit use conditions.
3. Open the linked `SKILL.md` before acting whenever exact routing boundaries, execution steps, or validation protocol matter.

> Naming note: `asset-rule`, `asset-skill`, and `asset-workflow` are the current runtime-routed owner-skill family and intentionally use `asset-<asset-family>`. `artifact-implementation-plan`, `artifact-brainstorm`, `artifact-issue-tracker`, and `artifact-issue-report` are the current artifact-centric owners and intentionally use `artifact-<artifact-family>`. Foundational cross-cutting contracts should prefer `core-<capability>`; `core-schema` is the active schema-authoring contract, and legacy `dev-schema` requests map to it during the transition. Routing skills should prefer `*-router`; `agent-asset-router` is active and `agent-artifact-router` is reserved for future use only. Skills outside the `asset-*`, `artifact-*`, `core-*`, and `*-router` families remain lowercase hyphen-case.

## Selection Map

- `artifact-issue-report`: use when the user asks to generate a standalone issue report for one tracked issue.
- `artifact-issue-tracker`: the user asks to create, initialize, seed, validate, audit, refresh, reevaluate, maintain, expand, or migrate an Issues Tracker.
- `agent-asset-router`: use when the user asks for an Antigravity agent asset and the request is framed at the asset layer rather than in the exact language of a dedicated execution contract.
- `artifact-brainstorm`: the user asks to create, initialize, seed, repair, validate, audit, or update `brainstorm.md`.
- `artifact-implementation-plan`: the user requests an implementation plan before coding begins.
- `asset-rule`: use when the user asks to create, scaffold, standardize, harden, or re-index a rule in `.agent/rules/`.
- `asset-skill`: use when the user asks to create, scaffold, template, standardize, or harden a skill in `.agent/skills/...`.
- `asset-workflow`: use when the user asks to create, scaffold, standardize, or harden a workflow in `.agent/workflows/`.
- `core-schema`: the user asks to create a new `.d.ts` schema file from an example artifact or document.
- `md060-strict-aligner`: the user asks to fix MD060 table alignment violations.
- `python-docsurface-normalizer`: use when the user asks to populate, rewrite, normalize, or standardize docstrings and code comments in one or more explicit Python files.

## Manifest

```yaml
skills:
- id: artifact-issue-report
  definition: .agent/skills/artifact-issue-report/SKILL.md
  category: issue_artifacts
  implementation: .agent/skills/artifact-issue-report/
  keywords:
  - artifact
  - issue
  - report
  - validate
  - artifact-centric-owner
  use_when:
  - Use when the user asks to generate a standalone issue report for one tracked issue.
  - Use when the request asks to maintain, refresh, migrate, or validate an existing
    issue-report artifact.
  - Use when the request identifies an `ISSUE_ID` plus an Issues Tracker document
    and expects a canonical issue report as output.
- id: artifact-issue-tracker
  definition: .agent/skills/artifact-issue-tracker/SKILL.md
  category: issue_artifacts
  implementation: .agent/skills/artifact-issue-tracker/
  keywords:
  - artifact
  - issue
  - tracker
  - issues-tracker
  - validate
  - audit
  - artifact-centric-owner
  use_when:
  - The user asks to create, initialize, seed, validate, audit, refresh, reevaluate,
    maintain, expand, or migrate an Issues Tracker.
  - The task needs a blank tracker generated from the canonical `IT-1.0` template.
  - The task references an existing tracker plus target YAML/spec files, local audits,
    local issue reports, or other repo documents that may contain issue leads.
  - The task requires validating existing `OPEN` issues, adding `Option C`, adding
    a comparative analysis, endorsing one strategy, or attaching authoritative online
    citations directly inside the tracker.
  - The task is to validate or audit a tracker artifact without changing the target
    DDR/spec sources.
- id: agent-asset-router
  definition: .agent/skills/agent-asset-router/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/agent-asset-router/
  keywords:
  - agent
  - asset
  - router
  - route
  - routing
  - validation
  - scaffold
  - plan
  use_when:
  - Use when the user asks for an Antigravity agent asset and the request is framed
    at the asset layer rather than in the exact language of a dedicated execution
    contract.
  - Use when the request mixes asset-authoring concerns, such as asking for a new
    agent asset category, asking whether a report should become a skill or schema,
    or asking for one front-door skill to cover several asset families.
  - Use when the request needs schema-first classification for asset families that
    do not yet have a dedicated owner skill.
  - '`asset-rule`, `asset-skill`, and `asset-workflow` are the current direct-route
    runtime-routed owner skills and intentionally follow the `asset-<asset-family>`
    naming family.'
- id: artifact-brainstorm
  definition: .agent/skills/artifact-brainstorm/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/artifact-brainstorm/
  keywords:
  - artifact
  - brainstorm
  - audit
  - plan
  - artifact-centric-owner
  use_when:
  - The user asks to create, initialize, seed, repair, validate, audit, or update
    `brainstorm.md`.
  - The task is to capture or reorganize brainstorm entries such as design ideas,
    architectural hypotheses, workflow concepts, or library candidates inside the
    governed brainstorm artifact.
  - The brainstorm artifact is missing and must be initialized from the canonical
    seed and schema-owned source reference.
  - The brainstorm artifact exists but needs structural cleanup, citation repair,
    ID assignment, section placement, field completion, or visual-semantics normalization
    before new entries are appended.
- id: artifact-implementation-plan
  definition: .agent/skills/artifact-implementation-plan/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/artifact-implementation-plan/
  keywords:
  - artifact
  - implementation
  - plan
  - implementation-plan
  - audit
  - artifact-centric-owner
  use_when:
  - The user requests an implementation plan before coding begins.
  - The user asks to create, edit, refine, regenerate, enhance, or audit an existing
    implementation plan artifact.
  - The task has non-trivial scope, dependencies, or risk requiring deterministic
    execution steps.
  - A human-approved planning artifact is required before any code or file modifications
    occur.
- id: asset-rule
  definition: .agent/skills/asset-rule/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/asset-rule/
  keywords:
  - asset
  - rule
  - validate
  - validation
  - scaffold
  - index
  - runtime-routed-owner
  use_when:
  - Use when the user asks to create, scaffold, standardize, harden, or re-index a
    rule in `.agent/rules/`.
  - Use when the task is to improve rule trigger wording, glob scope, verification
    steps, execution-tier hygiene, or rules-index alignment.
- id: asset-skill
  definition: .agent/skills/asset-skill/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/asset-skill/
  keywords:
  - asset
  - skill
  - route
  - routing
  - validation
  - scaffold
  - index
  - runtime-routed-owner
  use_when:
  - Use when the user asks to create, scaffold, template, standardize, or harden a
    skill in `.agent/skills/...`.
  - Use when the task is to improve skill triggering, `SKILL.md` structure, bundled
    resource layout, or skill packaging and validation behavior.
- id: asset-workflow
  definition: .agent/skills/asset-workflow/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/asset-workflow/
  keywords:
  - asset
  - workflow
  - validation
  - scaffold
  - index
  - plan
  - runtime-routed-owner
  use_when:
  - Use when the user asks to create, scaffold, standardize, or harden a workflow
    in `.agent/workflows/`.
  - Use when the task is to improve workflow trigger wording, execution-step determinism,
    verification plans, or workflow-index hygiene.
- id: core-schema
  definition: .agent/skills/core-schema/SKILL.md
  category: orchestration_and_authoring
  implementation: .agent/skills/core-schema/
  keywords:
  - core
  - schema
  - index
  - gemini
  - security-policy
  - task
  - walkthrough
  - validation
  - scaffold
  - plan
  use_when:
  - The user asks to create a new `.d.ts` schema file from an example artifact or
    document.
  - The user asks to update an existing Antigravity schema or schema README.
  - The user asks to regenerate or synchronize the `.agent/schemas/index.md` directory
    index.
  - Legacy requests that still say `dev-schema` should route here; `core-schema` is
    the active foundational schema-authoring contract.
- id: md060-strict-aligner
  definition: .agent/skills/md060-strict-aligner/SKILL.md
  category: formatting_and_refactoring
  implementation: .agent/skills/md060-strict-aligner/
  keywords:
  - md060
  - strict
  - aligner
  - refactoring
  use_when:
  - The user asks to fix MD060 table alignment violations.
  - Markdown table formatting must be normalized without content rewrites.
- id: python-docsurface-normalizer
  definition: .agent/skills/python-docsurface-normalizer/SKILL.md
  category: formatting_and_refactoring
  implementation: .agent/skills/python-docsurface-normalizer/
  keywords:
  - python
  - docsurface
  - normalizer
  - refactoring
  use_when:
  - Use when the user asks to populate, rewrite, normalize, or standardize docstrings
    and code comments in one or more explicit Python files.
  - Use when the request calls for NumPy-style docstrings, agent-optimized Python
    documentation, comment preservation review, or comment/docstring stripping before
    rewrite.
```

## Skill Records

### `artifact-issue-report`

- Definition: [`artifact-issue-report/SKILL.md`](artifact-issue-report/SKILL.md)
- Implementation: [`.agent/skills/artifact-issue-report/`](artifact-issue-report)
- Best used for: Serves as the Artifact-Centric Owner for issue-report artifacts by generating canonical standalone issue reports, maintaining or upgrading existing reports, and validating canonical or legacy report integrity against the canonical `issue` contract. Use when the task is to create, modify, migrate, or validate a governed issue report. Do not use when the task is to edit the source Issues Tracker, patch target DDR/spec/YAML files, or rewrite the canonical `issue` schema.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `artifact-issue-tracker`

- Definition: [`artifact-issue-tracker/SKILL.md`](artifact-issue-tracker/SKILL.md)
- Implementation: [`.agent/skills/artifact-issue-tracker/`](artifact-issue-tracker)
- Best used for: Serves as the Artifact-Centric Owner for Issues Tracker artifacts by initializing blank `IT-1.0` trackers, refreshing and migrating populated trackers to `IT-1.1`, and validating or auditing tracker integrity against the canonical `issues-tracker` contract. Use when the task is to create, maintain, validate, or audit a governed Issues Tracker. Do not use when the task is to generate a standalone issue report, rewrite the canonical tracker schema, or patch target YAML or spec files.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `agent-asset-router`

- Definition: [`agent-asset-router/SKILL.md`](agent-asset-router/SKILL.md)
- Implementation: [`.agent/skills/agent-asset-router/`](agent-asset-router)
- Best used for: Routes Antigravity agent-asset work to the correct dedicated execution contract using the local skills registry, deterministic direct-route handoff, and schema-first classification for uncovered asset families. Use when the user frames the task at the agent-asset level, when the correct direct-route skill is unclear or mixed, or when determining whether schema work must happen first. Legacy `dev-schema` requests normalize to `core-schema` during routing. Do not use when the request is already expressed in the exact vocabulary of a dedicated execution contract such as direct skill scaffolding, direct rule authoring, canonical schema authoring, workflow creation, implementation-plan generation, brainstorm artifact maintenance, explicit issues-tracker lifecycle management, or standalone issue-report generation, maintenance, or validation.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `artifact-brainstorm`

- Definition: [`artifact-brainstorm/SKILL.md`](artifact-brainstorm/SKILL.md)
- Implementation: [`.agent/skills/artifact-brainstorm/`](artifact-brainstorm)
- Best used for: Serves as the Artifact-Centric Owner for Antigravity brainstorm artifacts by creating, seeding, repairing, validating, and auditing governed `brainstorm.md` compendia against the canonical `brainstorm` schema, citation protocol, and Mermaid/visual-semantics rules. Use when the task is to create or maintain a governed brainstorm artifact or its entry content. Do not use when the task is to author the canonical brainstorm schema, finalize normative spec text, or write an implementation plan.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `artifact-implementation-plan`

- Definition: [`artifact-implementation-plan/SKILL.md`](artifact-implementation-plan/SKILL.md)
- Implementation: [`.agent/skills/artifact-implementation-plan/`](artifact-implementation-plan)
- Best used for: Serves as the Artifact-Centric Owner for Antigravity implementation-plan artifacts by creating, refining, auditing, and lifecycle-managing schema-compatible plans optimized for grounded planning, patch-bounded execution batches, task-tracker visibility, and safe executor handoff. Use when the task needs a formal plan artifact before execution begins. Do not use when the requested work is trivial enough to execute directly without a governed plan.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `asset-rule`

- Definition: [`asset-rule/SKILL.md`](asset-rule/SKILL.md)
- Implementation: [`.agent/skills/asset-rule/`](asset-rule)
- Best used for: Use this skill for authors or refines Antigravity-compatible rule assets with explicit trigger boundaries, scaffold and validation tooling, and deterministic rules-index synchronization. Use when the task is to create, standardize, validate, or re-index a reusable rule under `.agent/rules/`. Do not use when the task is standalone canonical schema authoring, specialized rule-derived schema work such as `security-policy`, or ordinary project feature changes.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `asset-skill`

- Definition: [`asset-skill/SKILL.md`](asset-skill/SKILL.md)
- Implementation: [`.agent/skills/asset-skill/`](asset-skill)
- Best used for: Use this skill for authors or refines Antigravity-compatible skills with explicit trigger boundaries, root README lifecycle governance, vendored schema mirrors, generated skills-index maintenance, and validation-first packaging hygiene. Use when the task is to scaffold a new skill or standardize an existing skill folder, including runtime-routed owner skills, artifact-centric owner skills, foundational `core-*` contracts, and routing contracts. Do not use for creating workflows, schemas, or ordinary project features outside the skill contract.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `asset-workflow`

- Definition: [`asset-workflow/SKILL.md`](asset-workflow/SKILL.md)
- Implementation: [`.agent/skills/asset-workflow/`](asset-workflow)
- Best used for: Use this skill for authors or refines Antigravity-compatible workflow assets with explicit trigger boundaries, scaffold and validation tooling, and deterministic workflow-index synchronization. Use when the task is to create or standardize a reusable workflow under `.agent/workflows/`. Do not use when the task is to create a skill, schema, implementation plan, or ordinary project feature change.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `core-schema`

- Definition: [`core-schema/SKILL.md`](core-schema/SKILL.md)
- Implementation: [`.agent/skills/core-schema/`](core-schema)
- Best used for: Serves as the foundational `core-*` contract for canonical Antigravity `.d.ts` schema authoring via scaffold, strict validation, runtime-target compatibility checks, schema-governance README maintenance, and owner-aware index synchronization. Use when the task is to create a new schema from an example artifact, update an existing schema definition, or regenerate the schema directory index for a core-governed schema family. The package vendors the full set of canonical schemas it owns, and legacy `dev-schema` requests map to this contract. Do not use for creating workflows, skills, implementation plans, or project features outside the schema authoring contract.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `md060-strict-aligner`

- Definition: [`md060-strict-aligner/SKILL.md`](md060-strict-aligner/SKILL.md)
- Implementation: [`.agent/skills/md060-strict-aligner/`](md060-strict-aligner)
- Best used for: Use this skill for deterministically aligns Markdown tables to satisfy MD060 with minimal, structure-preserving edits. Use when the task is to fix table alignment violations without changing prose or table meaning. Do not use when the request requires broader Markdown rewrites or non-table content changes.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

### `python-docsurface-normalizer`

- Definition: [`python-docsurface-normalizer/SKILL.md`](python-docsurface-normalizer/SKILL.md)
- Implementation: [`.agent/skills/python-docsurface-normalizer/`](python-docsurface-normalizer)
- Best used for: Use this skill for populate or normalize semantically dense NumPy-style docstrings and meaningful code comments in one or more explicitly named Python files using deterministic analysis, grouped preservation gating, and AST-safe verification. Use when the task is to document existing Python code without changing runtime behavior. Do not use when the request is a directory sweep, non-Python edit, or general refactor.
- Open the linked definition when exact routing boundaries, execution steps, or validation rules matter.

## Category Totals

- `formatting_and_refactoring`: `2`
- `issue_artifacts`: `2`
- `orchestration_and_authoring`: `7`
- `total`: `11`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract for any skill.
- Do not infer trigger boundaries, exact outputs, or validation semantics from the summaries in this index alone.
- When a task depends on exact routing, execution order, or safety protocol, defer to the linked `SKILL.md`.
