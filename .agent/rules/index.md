# Agent Rules Index

> Consolidated registry of rule assets in `.agent/rules/`.
>
> Scope: discovery, first-pass selection, and quick routing across reusable rule definitions.
>
> Total rules: `4`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked rule definition, the linked rule file is authoritative.

## Use This Index

1. Use the selection map to identify the most likely rule by trigger context.
2. Use the manifest to confirm the definition path, activation mode, and priority before opening the rule.
3. Open the linked rule definition before relying on exact constraints or verification steps.

## Selection Map

- `AGENT_TEMP_ARTIFACT_HYGIENE`: Always-on containment and cleanup policy for one-off agent scripts, diagnostics, and transient run artifacts in the Antigravity workspace.
- `POWERSHELL_EXECUTION_GUARDRAILS`: Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- `dev-check-schema`: Enforces RuleDefinition frontmatter integrity for `.agent/rules/` assets, governed rules-index hygiene, and canonical schema-markdown governance under `.agent/schemas/`.
- `SKILL_CHANGE_GOVERNANCE`: Glob-scoped governance rule requiring skill root README updates, strict SemVer version bumps, and vendored schema mirror resynchronization whenever files under .agent/skills/ change.

## Manifest

```yaml
rules:
- id: AGENT_TEMP_ARTIFACT_HYGIENE
  definition: .agent/rules/AGENT_TEMP_ARTIFACT_HYGIENE.md
  asset_structure: flat-file
  category: always_on_rules
  trigger: always_on
  priority: high
  implementation: .agent/rules/AGENT_TEMP_ARTIFACT_HYGIENE.md
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
- id: POWERSHELL_EXECUTION_GUARDRAILS
  definition: .agent/rules/POWERSHELL_EXECUTION_GUARDRAILS.md
  asset_structure: flat-file
  category: always_on_rules
  trigger: always_on
  priority: critical
  implementation: .agent/rules/POWERSHELL_EXECUTION_GUARDRAILS.md
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
- id: dev-check-schema
  definition: .agent/rules/dev-check-schema.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/dev-check-schema.md
  keywords:
  - rule
  - glob
  - critical
  - dev
  - check
  - schema
  use_when:
  - Enforces RuleDefinition frontmatter integrity for `.agent/rules/` assets, governed
    rules-index hygiene, and canonical schema-markdown governance under `.agent/schemas/`.
  globs: .agent/schemas/**/*.md, .agent/rules/**/*.md
- id: SKILL_CHANGE_GOVERNANCE
  definition: .agent/rules/SKILL_CHANGE_GOVERNANCE.md
  asset_structure: flat-file
  category: glob_rules
  trigger: glob
  priority: critical
  implementation: .agent/rules/SKILL_CHANGE_GOVERNANCE.md
  keywords:
  - rule
  - glob
  - critical
  - skill
  - change
  - governance
  use_when:
  - Glob-scoped governance rule requiring skill root README updates, strict SemVer
    version bumps, and vendored schema mirror resynchronization whenever files under
    .agent/skills/ change.
  globs: .agent/skills/**
```

## Rule Records

Records are grouped by trigger order (`always_on`, `glob`, `manual`, `auto`, `@mention`) and sorted by rule id within each group.

### `AGENT_TEMP_ARTIFACT_HYGIENE`

- Definition: [`AGENT_TEMP_ARTIFACT_HYGIENE.md`](AGENT_TEMP_ARTIFACT_HYGIENE.md)
- Best used for: Always-on containment and cleanup policy for one-off agent scripts, diagnostics, and transient run artifacts in the Antigravity workspace.
- Trigger: `always_on` (always-on)
- Priority: `high`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `POWERSHELL_EXECUTION_GUARDRAILS`

- Definition: [`POWERSHELL_EXECUTION_GUARDRAILS.md`](POWERSHELL_EXECUTION_GUARDRAILS.md)
- Best used for: Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O.
- Trigger: `always_on` (always-on)
- Priority: `critical`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `dev-check-schema`

- Definition: [`dev-check-schema.md`](dev-check-schema.md)
- Best used for: Enforces RuleDefinition frontmatter integrity for `.agent/rules/` assets, governed rules-index hygiene, and canonical schema-markdown governance under `.agent/schemas/`.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/schemas/**/*.md, .agent/rules/**/*.md`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

### `SKILL_CHANGE_GOVERNANCE`

- Definition: [`SKILL_CHANGE_GOVERNANCE.md`](SKILL_CHANGE_GOVERNANCE.md)
- Best used for: Glob-scoped governance rule requiring skill root README updates, strict SemVer version bumps, and vendored schema mirror resynchronization whenever files under .agent/skills/ change.
- Trigger: `glob` (glob-scoped)
- Priority: `critical`
- Glob scope: `.agent/skills/**`
- Execution tier: `standard`
- Open the linked definition when exact constraints, verification steps, or trigger precedence matter.

## Category Totals

- `always_on_rules`: `2`
- `glob_rules`: `2`
- `total`: `4`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- Do not infer exact constraint wording, verification semantics, or override behavior from summaries in this index alone.
- When a task depends on exact trigger scope, priority handling, or behavioral requirements, defer to the linked rule definition.
