# Agent Skills Index

> Consolidated registry of skill assets in `.agent/skills/`.
>
> Scope: discovery, first-pass selection, and quick routing across current skill contracts.
>
> Total skills: `10`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked skill definition, the linked `SKILL.md` is authoritative.

## Use This Index

1. Use the selection map to identify the most likely skill by task intent.
2. Use the manifest to confirm the skill category, definition path, and best-fit use conditions.
3. Open the linked `SKILL.md` before acting whenever exact routing boundaries, execution steps, or validation protocol matter.

> Naming note: `asset-rule`, `asset-skill`, and `asset-workflow` are the current runtime-routed owner-skill family and intentionally use `asset-<asset-family>`. `artifact-implementation-plan`, `artifact-brainstorm`, and `artifact-issue-tracker` are the current artifact-centric owners and intentionally use `artifact-<artifact-family>`. Foundational cross-cutting contracts should prefer `core-<capability>`; `core-schema` is the active schema-authoring contract, and legacy `dev-schema` requests map to it during the transition. Routing skills should prefer `*-router`; `agent-asset-router` is active and `agent-artifact-router` is reserved for future use only. Skills outside the `asset-*`, `artifact-*`, `core-*`, and `*-router` families remain lowercase hyphen-case. Legacy unlisted skills are outside this migration scope.

## Selection Map

- `agent-create-issue-report`: generate one standalone resolution report for a single tracked issue.
- `artifact-issue-tracker`: serve as the Artifact-Centric Owner for governed Issues Tracker creation, maintenance, validation, and audit.
- `artifact-brainstorm`: serve as the Artifact-Centric Owner for governed brainstorm artifacts such as `brainstorm.md`.
- `agent-asset-router`: classify agent-asset requests and route them to the correct dedicated execution contract or schema-first path.
- `artifact-implementation-plan`: serve as the Artifact-Centric Owner for governed implementation-plan artifacts before execution begins.
- `asset-rule`: create or standardize reusable rule assets and keep the rules index aligned.
- `core-schema`: create or update canonical `.d.ts` schemas and related schema governance assets through the foundational `core-*` schema-authoring contract. Legacy `dev-schema` requests map here.
- `asset-skill`: scaffold or standardize skill folders under `.agent/skills/`.
- `asset-workflow`: create or standardize reusable workflows under `.agent/workflows/`.
- `md060-strict-aligner`: align Markdown tables with minimal structure-preserving edits.

## Manifest

```yaml
skills:
  - id: agent-create-issue-report
    definition: .agent/skills/agent-create-issue-report/SKILL.md
    category: issue_artifacts
    implementation: .agent/skills/agent-create-issue-report/
    keywords:
      - issue
      - report
      - resolution
      - tracker
      - audit
    use_when:
      - generating a standalone report for one tracked issue
      - investigating a single issue without editing the tracker

  - id: artifact-issue-tracker
    definition: .agent/skills/artifact-issue-tracker/SKILL.md
    category: issue_artifacts
    implementation: .agent/skills/artifact-issue-tracker/
    keywords:
      - issues-tracker
      - initialize
      - refresh
      - migrate
      - validate
      - audit
      - artifact-centric-owner
    use_when:
      - creating a blank issues tracker from the canonical template
      - updating, migrating, validating, or auditing an existing issues tracker
      - using the dedicated owner utility for the Issues Tracker artifact lifecycle

  - id: artifact-brainstorm
    definition: .agent/skills/artifact-brainstorm/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/artifact-brainstorm/
    keywords:
      - brainstorm
      - ideas
      - hypotheses
      - candidates
      - artifact-centric-owner
    use_when:
      - drafting, repairing, validating, or auditing governed brainstorm artifacts
      - using the dedicated owner utility for brainstorm artifact lifecycle management

  - id: agent-asset-router
    definition: .agent/skills/agent-asset-router/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/agent-asset-router/
    keywords:
      - agent-asset
      - front-door
      - routing
      - classification
      - schema-first
    use_when:
      - routing an unclear or mixed agent-asset request
      - handing off agent-asset work to the correct dedicated execution contract
      - deciding whether agent-asset work is skill-first or schema-first

  - id: artifact-implementation-plan
    definition: .agent/skills/artifact-implementation-plan/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/artifact-implementation-plan/
    keywords:
      - implementation-plan
      - artifact-centric-owner
      - planning
      - handoff
      - phases
    use_when:
      - drafting, refining, regenerating, or auditing a governed implementation-plan artifact
      - using the dedicated owner utility for implementation-plan artifact lifecycle management

  - id: asset-rule
    definition: .agent/skills/asset-rule/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/asset-rule/
    keywords:
      - rule
      - scaffold
      - validation
      - index
      - constraints
    use_when:
      - creating or updating reusable rules under .agent/rules/
      - validating rule assets and keeping the rules index synchronized
      - maintaining owner-managed rule governance assets

  - id: core-schema
    definition: .agent/skills/core-schema/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/core-schema/
    keywords:
      - core
      - schema
      - d.ts
      - scaffold
      - validation
      - index
    use_when:
      - creating or updating a canonical schema with the foundational `core-*` schema-authoring contract
      - rebuilding the schema directory index after schema changes
      - maintaining owner-managed schema governance assets
      - handling legacy `dev-schema` requests through the renamed `core-schema` contract

  - id: asset-skill
    definition: .agent/skills/asset-skill/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/asset-skill/
    keywords:
      - skill
      - scaffold
      - mirror
      - packaging
      - validation
    use_when:
      - creating a new skill
      - standardizing an existing skill folder
      - scaffolding a future runtime-routed or artifact-centric owner skill

  - id: asset-workflow
    definition: .agent/skills/asset-workflow/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/asset-workflow/
    keywords:
      - workflow
      - repeatable
      - steps
      - verification
    use_when:
      - creating a reusable workflow asset
      - standardizing an existing workflow
      - validating or re-indexing workflow assets after updates

  - id: md060-strict-aligner
    definition: .agent/skills/md060-strict-aligner/SKILL.md
    category: formatting_and_refactoring
    implementation: .agent/skills/md060-strict-aligner/
    keywords:
      - markdown
      - table
      - alignment
      - md060
    use_when:
      - fixing table alignment violations
      - preserving Markdown table meaning while normalizing spacing

```

## Skill Records

### `agent-create-issue-report`

- Definition: [`agent-create-issue-report/SKILL.md`](agent-create-issue-report/SKILL.md)
- Implementation: [`.agent/skills/agent-create-issue-report/`](agent-create-issue-report)
- Best used for: generating one validator-checked standalone report for a single tracked issue.
- Open the linked definition when report structure, evidence rules, or validator usage matters.

### `artifact-issue-tracker`

- Definition: [`artifact-issue-tracker/SKILL.md`](artifact-issue-tracker/SKILL.md)
- Implementation: [`.agent/skills/artifact-issue-tracker/`](artifact-issue-tracker)
- Best used for: serving as the Artifact-Centric Owner utility for Issues Tracker initialization, maintenance, migration, validation, and audit.
- Open the linked definition when tracker mode selection, overwrite rules, evidence standards, migration behavior, or validator usage matters.

### `artifact-brainstorm`

- Definition: [`artifact-brainstorm/SKILL.md`](artifact-brainstorm/SKILL.md)
- Implementation: [`.agent/skills/artifact-brainstorm/`](artifact-brainstorm)
- Best used for: serving as the Artifact-Centric Owner utility for brainstorm artifact creation, repair, validation, and governance in `brainstorm.md`.
- Open the linked definition when brainstorm formatting, citation rules, validator usage, or owner-boundary behavior matters.

### `agent-asset-router`

- Definition: [`agent-asset-router/SKILL.md`](agent-asset-router/SKILL.md)
- Implementation: [`.agent/skills/agent-asset-router/`](agent-asset-router)
- Best used for: front-door routing when the correct direct-route skill for an agent asset is unclear or mixed.
- Open the linked definition when you need the direct-route matrix, deterministic owner-handoff rules, schema-first fallback rules, or RFQ gates.

### `artifact-implementation-plan`

- Definition: [`artifact-implementation-plan/SKILL.md`](artifact-implementation-plan/SKILL.md)
- Implementation: [`.agent/skills/artifact-implementation-plan/`](artifact-implementation-plan)
- Best used for: serving as the Artifact-Centric Owner utility for implementation-plan artifact creation, regeneration, audit, and governance before execution begins.
- Open the linked definition when naming rules, phase structure, or verification mapping matters.

### `asset-rule`

- Definition: [`asset-rule/SKILL.md`](asset-rule/SKILL.md)
- Implementation: [`.agent/skills/asset-rule/`](asset-rule)
- Best used for: authoring deterministic rule assets with scaffold, validation, and rules-index synchronization.
- Open the linked definition when rule structure, trigger semantics, validation checks, or rules-index regeneration matters.

### `core-schema`

- Definition: [`core-schema/SKILL.md`](core-schema/SKILL.md)
- Implementation: [`.agent/skills/core-schema/`](core-schema)
- Best used for: canonical schema creation, schema updates, and schema index regeneration through the foundational `core-*` contract; legacy `dev-schema` requests map here.
- Open the linked definition when scaffold commands, schema README governance, owner-skill schema alignment, legacy transition handling, or validation rules matter.

### `asset-skill`

- Definition: [`asset-skill/SKILL.md`](asset-skill/SKILL.md)
- Implementation: [`.agent/skills/asset-skill/`](asset-skill)
- Best used for: scaffolding or standardizing skill folders with lifecycle governance and schema mirrors, including future runtime-routed and artifact-centric owners.
- Open the linked definition when packaging, mirror sync, root README requirements, owner-skill pattern reuse, or trigger testing matters.

### `asset-workflow`

- Definition: [`asset-workflow/SKILL.md`](asset-workflow/SKILL.md)
- Implementation: [`.agent/skills/asset-workflow/`](asset-workflow)
- Best used for: authoring deterministic workflow assets with scaffold, validation, and index-sync lifecycle support.
- Open the linked definition when workflow structure, index regeneration, section requirements, or execution constraints matter.

### `md060-strict-aligner`

- Definition: [`md060-strict-aligner/SKILL.md`](md060-strict-aligner/SKILL.md)
- Implementation: [`.agent/skills/md060-strict-aligner/`](md060-strict-aligner)
- Best used for: structure-preserving Markdown table alignment fixes.
- Open the linked definition when the request must remain table-only and broader Markdown edits are out of scope.

## Category Totals

- `formatting_and_refactoring`: `1`
- `issue_artifacts`: `2`
- `orchestration_and_authoring`: `7`
- `total`: `10`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract for any skill.
- Do not infer trigger boundaries, exact outputs, or validation semantics from the summaries in this index alone.
- When a task depends on exact routing, execution order, or safety protocol, defer to the linked `SKILL.md`.
