---
name: "tools-governance"
version: "1.0.0"
description: "Glob-scoped collection governance rule for the `.agent/tools/` directory, covering tool definition frontmatter contracts, implementation-script alignment, tools index accuracy, and prohibition of orphaned tool definitions."
trigger: "glob"
globs: ".agent/tools/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. Scope Boundary: This rule governs only assets under `.agent/tools/`. It MUST NOT impose governance requirements on `.agent/scripts/`, `.agent/rules/`, or `.agent/schemas/`.
2. Tool Definition Frontmatter Contract: Tool definition files under `.agent/tools/` other than `index.md` MUST contain valid YAML frontmatter with the required keys: `type` (must be `tool`), `name`, `description`, `command`, `runtime`, `confirmation`, and `args`.
3. Implementation Alignment Required: Every tool definition's `command` field MUST reference a script implementation that exists under `.agent/scripts/`. If the referenced implementation does not exist, the tool definition MUST be flagged as orphaned.
4. Interpreter Path Consistency: Tool definitions that invoke Python scripts MUST reference the workspace-local interpreter path (`${workspaceFolder}/.venv/Scripts/python.exe`) consistent with the `powershell-execution-guardrails` rule and the `runtime-target.yaml` Windows execution configuration.
5. Tools Index Governance: `.agent/tools/index.md` MUST remain a generated full-form discovery index aligned with the `index` schema. It MUST accurately list all non-index tool definitions under `.agent/tools/` with correct manifest metadata, implementation links, and safety contract summaries.
6. Live Files Only: The tools index and any tool metadata MUST reflect only tool definitions that currently exist in the repository. Stale references to removed tool definitions MUST NOT be retained.
7. No Orphaned Definitions: Tool definitions MUST NOT exist without a working implementation script. If an implementation is removed, the corresponding tool definition MUST be removed or updated in the same task.

</constraints>

<verification_step>

1. If the target file is a tool definition other than `index.md`, validate its YAML frontmatter contains all required keys (`type`, `name`, `description`, `command`, `runtime`, `confirmation`, `args`) and confirm the `command` field references an existing `.agent/scripts/` implementation.
2. Confirm the tool definition's interpreter path is consistent with the workspace-local interpreter preference defined in `runtime-target.yaml`.
3. If the target file is `.agent/tools/index.md`, confirm it accurately inventories all non-index tool definitions with correct implementation links, manifest metadata, and safety contract summaries.
4. Confirm no tool definition references a removed or nonexistent implementation script.

</verification_step>
