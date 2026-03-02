---
name: dev-check-schema
description: "Enforces strict schema compliance for all Antigravity agent asset definition files based on the modular interfaces in .agent/assets/schemas/."
trigger: always_on
priority: critical
---
# Antigravity Asset Schema Enforcement

<constraints>
This rule mandates strict adherence to the TypeScript interfaces defined in the modular schema directory `.agent/assets/schemas/` when creating or modifying any agent asset file.

## Schema Reference

| File Pattern                                    | Interface                      | Required Frontmatter Keys                      |
| :---------------------------------------------- | :----------------------------- | :--------------------------------------------- |
| `~/.gemini/GEMINI.md` or `.agent/GEMINI.md`     | `GeminiMdConfiguration`        | `description`, `models`, `version`, `scope`    |
| `implementation_plan.md` or `.agent/plans/*.md` | `ImplementationPlanDefinition` | `task`, `model`                                |
| `.agent/rules/*.md`                             | `RuleDefinition`               | `description`, `trigger`, `priority`           |
| `.agent/rules/SECURITY_GUARDRAILS.md`           | `SecurityPolicyDefinition`     | `name`, `description`, `trigger`, `priority`   |
| `.agent/skills/<skill-name>/SKILL.md`           | `SkillDefinition`              | `description`                                  |
| `task.md` or `TASK-XXXXXX.md`                   | `TaskDefinition`               | `task_id`, `title`, `priority`, `target_model` |
| `walkthrough.md`                                | `WalkthroughDefinition`        | N/A                                            |
| `.agent/workflows/*.md`                         | `WorkflowDefinition`           | `description`                                  |

## Enforcement Protocol

1. **Pre-Write Validation**: Before writing any file matching the `globs` patterns, validate all YAML frontmatter keys against the corresponding interface in `.agent/assets/schemas/`.
2. **Type Constraint Checking**: Ensure values match the types specified in the `.d.ts` definitions (e.g., `priority` in `RuleDefinition` must match `'low' | 'medium' | 'high' | 'critical'`).
3. **Implicit Uncertainty Protocol**: If uncertain about the optimal value for any required field, the agent **MUST** halt and ask the user clarifying questions before proceeding. Do not use placeholder or generic values.

</constraints>
