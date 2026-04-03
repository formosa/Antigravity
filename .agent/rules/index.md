# Agent Rules Index

> Consolidated registry of rule assets in `.agent/rules/`.
>
> Scope: discovery, first-pass selection, and quick routing across reusable rule definitions.
>
> Total rules: `5`
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
- `powershell-execution-guardrails`: Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- `dev-rule-governance`: Glob-scoped governance rule for `.agent/rules/` assets covering rule frontmatter, preferred naming, XML-fenced bodies, and generated rules-index alignment.
- `dev-schema-governance`: Glob-scoped governance rule for `.agent/schemas/` assets covering canonical `.d.ts` contracts, schema README governance blocks, example fidelity, and the table-only schema index.
- `dev-skill-governance`: Glob-scoped lifecycle governance rule for `.agent/skills/` packages requiring root README updates, SemVer-aligned version bumps, and vendored schema mirror synchronization.

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
    syntax, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- id: dev-rule-governance
  definition: .agent/rules/dev-rule-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/dev-rule-governance.md
  keywords:
  - rule
  - glob
  - critical
  - dev
  - governance
  use_when:
  - Glob-scoped governance rule for `.agent/rules/` assets covering rule frontmatter,
    preferred naming, XML-fenced bodies, and generated rules-index alignment.
  globs: .agent/rules/**
- id: dev-schema-governance
  definition: .agent/rules/dev-schema-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/dev-schema-governance.md
  keywords:
  - rule
  - glob
  - critical
  - dev
  - schema
  - governance
  use_when:
  - Glob-scoped governance rule for `.agent/schemas/` assets covering canonical `.d.ts`
    contracts, schema README governance blocks, example fidelity, and the table-only
    schema index.
  globs: .agent/schemas/**
- id: dev-skill-governance
  definition: .agent/rules/dev-skill-governance.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/dev-skill-governance.md
  keywords:
  - rule
  - glob
  - critical
  - dev
  - skill
  - governance
  use_when:
  - Glob-scoped lifecycle governance rule for `.agent/skills/` packages requiring
    root README updates, SemVer-aligned version bumps, and vendored schema mirror
    synchronization.
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
- Best used for: Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- Trigger: `always_on` (always-on)
- Priority: `critical`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `dev-rule-governance`

- Definition: [`dev-rule-governance.md`](dev-rule-governance.md)
- Best used for: Glob-scoped governance rule for `.agent/rules/` assets covering rule frontmatter, preferred naming, XML-fenced bodies, and generated rules-index alignment.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/rules/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `dev-schema-governance`

- Definition: [`dev-schema-governance.md`](dev-schema-governance.md)
- Best used for: Glob-scoped governance rule for `.agent/schemas/` assets covering canonical `.d.ts` contracts, schema README governance blocks, example fidelity, and the table-only schema index.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/schemas/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `dev-skill-governance`

- Definition: [`dev-skill-governance.md`](dev-skill-governance.md)
- Best used for: Glob-scoped lifecycle governance rule for `.agent/skills/` packages requiring root README updates, SemVer-aligned version bumps, and vendored schema mirror synchronization.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/skills/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

## Category Totals

- `always_on_rules`: `2`
- `glob_rules`: `3`
- `total`: `5`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- Do not infer exact constraint wording, verification semantics, or override behavior from summaries in this index alone.
- When a task depends on exact trigger scope, priority handling, or behavioral requirements, defer to the linked rule definition.
