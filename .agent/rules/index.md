# Agent Rules Index

> Consolidated registry of rule assets in `.agent/rules/`.
>
> Scope: discovery, first-pass selection, and quick routing across reusable rule definitions.
>
> Total rules: `6`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked rule definition, the linked rule file is authoritative.

## Use This Index

1. Use the selection map to identify the most likely rule by trigger context.
2. Use the manifest to confirm the definition path, activation mode, and priority before opening the rule.
3. Open the linked rule definition before relying on exact constraints or verification steps.

## Selection Map

- `agent-temp-artifact-hygiene`: Always-on containment and cleanup policy for one-off agent scripts, diagnostics, and transient run artifacts in the Antigravity workspace.
- `powershell-execution-guardrails`: Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, workspace-interpreter preference, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- `rules-governance`: Glob-scoped collection governance rule for the `.agent/rules/` directory, covering rule frontmatter, preferred naming, XML-fenced bodies, and the generated rules index for the full rules collection surface.
- `schemas-governance`: Glob-scoped collection governance rule for the `.agent/schemas/` directory, covering canonical `.d.ts` contracts, schema README governance blocks, example fidelity, and the table-only schemas index for the full schema collection surface.
- `scripts-governance`: Glob-scoped collection governance rule for the `.agent/scripts/` directory, covering live script inventory accuracy, generated root and tests indexes, compiled-artifact exclusion, and alignment between script implementations and linked tool definitions.
- `skills-governance`: Glob-scoped collection governance rule for the `.agent/skills/` directory, requiring root README updates, SemVer-aligned version bumps, vendored schema mirror synchronization, and lifecycle consistency across the full skills collection surface.

## Manifest

```yaml
rules:
- id: agent-temp-artifact-hygiene
  definition: .agent/rules/agent-temp-artifact-hygiene.md
  asset_structure: flat-file
  category: always_on_rules
  trigger: always_on
  priority: high
  implementation: .agent/rules/agent-temp-artifact-hygiene.md
  keywords:
  - rule
  - always_on
  - high
  - agent
  - temp
  - artifact
  - hygiene
  use_when:
  - Always-on containment and cleanup policy for one-off agent scripts, diagnostics,
    and transient run artifacts in the Antigravity workspace.
- id: powershell-execution-guardrails
  definition: .agent/rules/powershell-execution-guardrails.md
  asset_structure: flat-file
  category: always_on_rules
  trigger: always_on
  priority: critical
  implementation: .agent/rules/powershell-execution-guardrails.md
  keywords:
  - rule
  - always_on
  - critical
  - powershell
  - execution
  - guardrails
  use_when:
  - Always-on Windows PowerShell execution guardrails focused on PowerShell-native
    syntax, workspace-interpreter preference, safe quoting, tool fallback behavior,
    and UTF-8-safe shell I/O.
- id: rules-governance
  definition: .agent/rules/rules-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/rules-governance.md
  keywords:
  - rule
  - glob
  - critical
  - rules
  - governance
  use_when:
  - Glob-scoped collection governance rule for the `.agent/rules/` directory, covering
    rule frontmatter, preferred naming, XML-fenced bodies, and the generated rules
    index for the full rules collection surface.
  globs: .agent/rules/**
- id: schemas-governance
  definition: .agent/rules/schemas-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/schemas-governance.md
  keywords:
  - rule
  - glob
  - critical
  - schemas
  - governance
  use_when:
  - Glob-scoped collection governance rule for the `.agent/schemas/` directory, covering
    canonical `.d.ts` contracts, schema README governance blocks, example fidelity,
    and the table-only schemas index for the full schema collection surface.
  globs: .agent/schemas/**
- id: scripts-governance
  definition: .agent/rules/scripts-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/scripts-governance.md
  keywords:
  - rule
  - glob
  - critical
  - scripts
  - governance
  use_when:
  - Glob-scoped collection governance rule for the `.agent/scripts/` directory, covering
    live script inventory accuracy, generated root and tests indexes, compiled-artifact
    exclusion, and alignment between script implementations and linked tool definitions.
  globs: .agent/scripts/**
- id: skills-governance
  definition: .agent/rules/skills-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/skills-governance.md
  keywords:
  - rule
  - glob
  - critical
  - skills
  - governance
  use_when:
  - Glob-scoped collection governance rule for the `.agent/skills/` directory, requiring
    root README updates, SemVer-aligned version bumps, vendored schema mirror synchronization,
    and lifecycle consistency across the full skills collection surface.
  globs: .agent/skills/**
```

## Rule Records

Records are grouped by trigger order (`always_on`, `glob`, `manual`, `auto`, `@mention`) and sorted by rule id within each group.

### `agent-temp-artifact-hygiene`

- Definition: [`agent-temp-artifact-hygiene.md`](agent-temp-artifact-hygiene.md)
- Best used for: Always-on containment and cleanup policy for one-off agent scripts, diagnostics, and transient run artifacts in the Antigravity workspace.
- Trigger: `always_on` (always-on)
- Priority: `high`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `powershell-execution-guardrails`

- Definition: [`powershell-execution-guardrails.md`](powershell-execution-guardrails.md)
- Best used for: Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, workspace-interpreter preference, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- Trigger: `always_on` (always-on)
- Priority: `critical`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `rules-governance`

- Definition: [`rules-governance.md`](rules-governance.md)
- Best used for: Glob-scoped collection governance rule for the `.agent/rules/` directory, covering rule frontmatter, preferred naming, XML-fenced bodies, and the generated rules index for the full rules collection surface.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/rules/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `schemas-governance`

- Definition: [`schemas-governance.md`](schemas-governance.md)
- Best used for: Glob-scoped collection governance rule for the `.agent/schemas/` directory, covering canonical `.d.ts` contracts, schema README governance blocks, example fidelity, and the table-only schemas index for the full schema collection surface.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/schemas/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `scripts-governance`

- Definition: [`scripts-governance.md`](scripts-governance.md)
- Best used for: Glob-scoped collection governance rule for the `.agent/scripts/` directory, covering live script inventory accuracy, generated root and tests indexes, compiled-artifact exclusion, and alignment between script implementations and linked tool definitions.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/scripts/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `skills-governance`

- Definition: [`skills-governance.md`](skills-governance.md)
- Best used for: Glob-scoped collection governance rule for the `.agent/skills/` directory, requiring root README updates, SemVer-aligned version bumps, vendored schema mirror synchronization, and lifecycle consistency across the full skills collection surface.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/skills/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

## Category Totals

- `always_on_rules`: `2`
- `glob_rules`: `4`
- `total`: `6`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- Do not infer exact constraint wording, verification semantics, or override behavior from summaries in this index alone.
- When a task depends on exact trigger scope, priority handling, or behavioral requirements, defer to the linked rule definition.
