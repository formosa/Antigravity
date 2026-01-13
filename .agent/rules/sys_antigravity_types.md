---
type: rule
name: "Antigravity Asset Schema Enforcement"
globs:
  - ".agent/personas/**/*"
  - ".agent/rules/**/*"
  - ".agent/tools/**/*"
  - ".agent/workflows/**/*"
  - ".agent/knowledge/**/*"
  - ".agent/evals/**/*"
priority: 100
trigger:
  - "@agent_asset"
  - "@agent_assets"
severity: mandatory
description: "Enforces strict schema compliance for all Antigravity agent asset definition files based on the interfaces in `.agent/assets/antigravity_types.d.ts`. Agent must consult user if uncertain about any value."
---
# Antigravity Asset Schema Enforcement
This rule mandates strict adherence to the TypeScript interfaces defined in `.agent/assets/antigravity_types.d.ts` when creating or modifying any agent asset file.
## Schema Reference
| File Pattern | Interface | Required Frontmatter Keys |
| :--- | :--- | :--- |
| `.agent/personas/*.mdc` | `PersonaDefinition` | `name`, `handle`, `description`, `model`, `temperature`, `color`, `icon`, `tools`, `context_globs` |
| `.agent/rules/*.md` | `RuleDefinition` | `type`, `name`, `priority`, `severity`, `description` |
| `.agent/tools/*.md` | `ToolDefinition` | `type`, `name`, `description`, `command`, `runtime`, `confirmation`, `args` |
| `.agent/workflows/*.md` | `WorkflowDefinition` | `type`, `name`, `slug`, `description`, `mode`, `context`, `on_finish`, `inputs` |
| `.agent/knowledge/*.md` | `KnowledgeDefinition` | `name`, `sources`, `refresh_schedule`, `strategy`, `access` |
| `.agent/evals/*.md` | `EvaluationDefinition` | `name`, `target_agent`, `judge_model`, `pass_threshold`, `scenarios`, `rubric` |
## Enforcement Protocol
1.  **Pre-Write Validation**: Before writing any file matching the `globs` patterns, validate all YAML frontmatter keys against the corresponding interface.
2.  **Type Constraint Checking**: Ensure values match the types specified in `antigravity_types.d.ts` (e.g., `handle` must match `` `@${string}` ``).
3.  **Implicit Uncertainty Protocol**: If uncertain about the optimal value for any required field, the agent **MUST** halt and ask the user clarifying questions before proceeding. Do not use placeholder or generic values.
