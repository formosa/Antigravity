# Agent Skills Index

> Consolidated registry of skill assets in `.agent/skills/`.
>
> Scope: discovery, first-pass selection, and quick routing across current owner skills.
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

## Selection Map

- `agent-create-issue-report`: generate one standalone resolution report for a single tracked issue.
- `agent-create-issues-tracker`: initialize a blank issues tracker from the canonical template.
- `agent-update-issues-tracker`: reevaluate and update an existing issues tracker against local evidence.
- `codex-brainstorm`: capture or reorganize governed brainstorming content in `brainstorm.md`.
- `dev-agent-asset`: classify agent-asset requests and route them to the correct owner contract or schema-first path.
- `dev-implementation-plan`: produce a governed implementation-plan artifact before execution begins.
- `dev-schema`: create or update canonical `.d.ts` schemas and related schema governance assets.
- `dev-skill`: scaffold or standardize skill folders under `.agent/skills/`.
- `dev-workflow`: create or standardize reusable workflows under `.agent/workflows/`.
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

  - id: agent-create-issues-tracker
    definition: .agent/skills/agent-create-issues-tracker/SKILL.md
    category: issue_artifacts
    implementation: .agent/skills/agent-create-issues-tracker/
    keywords:
      - issues-tracker
      - initialize
      - template
      - review
    use_when:
      - creating a blank issues tracker
      - starting a new review tracker from the canonical template

  - id: agent-update-issues-tracker
    definition: .agent/skills/agent-update-issues-tracker/SKILL.md
    category: issue_artifacts
    implementation: .agent/skills/agent-update-issues-tracker/
    keywords:
      - issues-tracker
      - refresh
      - migrate
      - comparative-analysis
    use_when:
      - updating or migrating an existing issues tracker
      - adding comparative analysis or refreshed evidence to tracked issues

  - id: codex-brainstorm
    definition: .agent/skills/codex-brainstorm/SKILL.md
    category: ddr_authoring_and_analysis
    implementation: .agent/skills/codex-brainstorm/
    keywords:
      - brainstorm
      - ideas
      - hypotheses
      - candidates
    use_when:
      - capturing or reorganizing brainstorming artifacts
      - maintaining governed `brainstorm.md` content

  - id: dev-agent-asset
    definition: .agent/skills/dev-agent-asset/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/dev-agent-asset/
    keywords:
      - agent-asset
      - front-door
      - routing
      - classification
      - schema-first
    use_when:
      - routing an unclear or mixed agent-asset request
      - handing off agent-asset work to the correct owner skill
      - deciding whether agent-asset work is skill-first or schema-first

  - id: dev-implementation-plan
    definition: .agent/skills/dev-implementation-plan/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/dev-implementation-plan/
    keywords:
      - implementation-plan
      - planning
      - handoff
      - phases
    use_when:
      - drafting a formal implementation plan before execution
      - regenerating or auditing an implementation-plan artifact

  - id: dev-schema
    definition: .agent/skills/dev-schema/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/dev-schema/
    keywords:
      - schema
      - d.ts
      - scaffold
      - validation
      - index
    use_when:
      - creating or updating a canonical schema
      - rebuilding the schema directory index after schema changes
      - maintaining owner-managed schema governance assets

  - id: dev-skill
    definition: .agent/skills/dev-skill/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/dev-skill/
    keywords:
      - skill
      - scaffold
      - mirror
      - packaging
      - validation
    use_when:
      - creating a new skill
      - standardizing an existing skill folder
      - scaffolding a future owner-contract skill

  - id: dev-workflow
    definition: .agent/skills/dev-workflow/SKILL.md
    category: orchestration_and_authoring
    implementation: .agent/skills/dev-workflow/
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

### `agent-create-issues-tracker`

- Definition: [`agent-create-issues-tracker/SKILL.md`](agent-create-issues-tracker/SKILL.md)
- Implementation: [`.agent/skills/agent-create-issues-tracker/`](agent-create-issues-tracker)
- Best used for: initializing a fresh issues tracker from the canonical blank template.
- Open the linked definition when tracker parameters, overwrite rules, or validator steps matter.

### `agent-update-issues-tracker`

- Definition: [`agent-update-issues-tracker/SKILL.md`](agent-update-issues-tracker/SKILL.md)
- Implementation: [`.agent/skills/agent-update-issues-tracker/`](agent-update-issues-tracker)
- Best used for: refreshing, migrating, or expanding an existing issues tracker using local evidence.
- Open the linked definition when filtered mode, migration behavior, or citation requirements matter.

### `codex-brainstorm`

- Definition: [`codex-brainstorm/SKILL.md`](codex-brainstorm/SKILL.md)
- Implementation: [`.agent/skills/codex-brainstorm/`](codex-brainstorm)
- Best used for: governed brainstorming capture and reorganization in `brainstorm.md`.
- Open the linked definition when brainstorm formatting, citation rules, or Mermaid policy matters.

### `dev-agent-asset`

- Definition: [`dev-agent-asset/SKILL.md`](dev-agent-asset/SKILL.md)
- Implementation: [`.agent/skills/dev-agent-asset/`](dev-agent-asset)
- Best used for: front-door routing when the correct owner skill for an agent asset is unclear or mixed.
- Open the linked definition when you need the direct-route matrix, deterministic owner-handoff rules, schema-first fallback rules, or RFQ gates.

### `dev-implementation-plan`

- Definition: [`dev-implementation-plan/SKILL.md`](dev-implementation-plan/SKILL.md)
- Implementation: [`.agent/skills/dev-implementation-plan/`](dev-implementation-plan)
- Best used for: producing a formal implementation-plan artifact before execution begins.
- Open the linked definition when naming rules, phase structure, or verification mapping matters.

### `dev-schema`

- Definition: [`dev-schema/SKILL.md`](dev-schema/SKILL.md)
- Implementation: [`.agent/skills/dev-schema/`](dev-schema)
- Best used for: canonical schema creation, schema updates, and schema index regeneration.
- Open the linked definition when scaffold commands, schema README governance, owner-skill schema alignment, or validation rules matter.

### `dev-skill`

- Definition: [`dev-skill/SKILL.md`](dev-skill/SKILL.md)
- Implementation: [`.agent/skills/dev-skill/`](dev-skill)
- Best used for: scaffolding or standardizing skill folders with lifecycle governance and schema mirrors.
- Open the linked definition when packaging, mirror sync, root README requirements, owner-skill pattern reuse, or trigger testing matters.

### `dev-workflow`

- Definition: [`dev-workflow/SKILL.md`](dev-workflow/SKILL.md)
- Implementation: [`.agent/skills/dev-workflow/`](dev-workflow)
- Best used for: authoring deterministic workflow assets with scaffold, validation, and index-sync lifecycle support.
- Open the linked definition when workflow structure, index regeneration, section requirements, or execution constraints matter.

### `md060-strict-aligner`

- Definition: [`md060-strict-aligner/SKILL.md`](md060-strict-aligner/SKILL.md)
- Implementation: [`.agent/skills/md060-strict-aligner/`](md060-strict-aligner)
- Best used for: structure-preserving Markdown table alignment fixes.
- Open the linked definition when the request must remain table-only and broader Markdown edits are out of scope.

## Category Totals

- `ddr_authoring_and_analysis`: `1`
- `formatting_and_refactoring`: `1`
- `issue_artifacts`: `3`
- `orchestration_and_authoring`: `5`
- `total`: `10`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract for any skill.
- Do not infer trigger boundaries, exact outputs, or validation semantics from the summaries in this index alone.
- When a task depends on exact routing, execution order, or safety protocol, defer to the linked `SKILL.md`.
