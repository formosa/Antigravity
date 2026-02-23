# Google Antigravity v1.18.3: Agent Configuration Technical Reference

> **Document Version**: 3.0.0 | **Last Updated**: 2026-02-23 | **Target Platform**: Google Antigravity IDE v1.18.3+ | **Target Model**: Gemini 3.1 Pro

---

## Executive Summary

Google Antigravity implements an **agent-first development platform** where configuration assets operate through a hierarchical, progressive disclosure architecture. This reference is explicitly optimized for the **Gemini 3.1 Pro** reasoning engine, enforcing strict structural separation between machine-parseable YAML frontmatter and LLM-consumable XML body content.

**What's changed from v1.16.5 to v1.18.3:**

- **Personas Deprecated**: Legacy `AGENTS.md` and floating personas are replaced entirely by the global `GEMINI.md` configuration and its mandatory `thought_signature_protocol`.
- **Schema Strictness**: Flat JSON/YAML schemas are rejected for agent prompts. All Markdown assets must utilize explicit XML content fencing (e.g., `<constraints>`, `<when_to_use>`) to anchor the LLM's attention mechanism.
- **Artifact-Driven Execution**: Agents must explicitly generate execution state artifacts (`implementation_plan.md`, `task.md`) to maintain persistent memory rather than relying on implicit context.
- **Rule Triggering**: Frontmatter uses `trigger` instead of `activation`. Priority weighting (`critical`, `high`, etc.) is now mandatory for conflict resolution.
- **Skill Progressive Disclosure**: Skills mandate `<when_to_use>` and `<how_to_use>` blocks instead of legacy `goal` or `instructions` fields.

---

## 1. Core Configuration Asset Types

### 1.1 Asset Taxonomy

| Asset Type | Scope | Activation | Purpose | Format |
| :--- | :--- | :--- | :--- | :--- |
| **Global Config** | Workspace | Always-on | Defines cognitive parameters and state protocol | `GEMINI.md` |
| **Rules** | Global/Workspace | Configurable | Passive behavioral constraints and verifications | `.md` (YAML + XML) |
| **Workflows** | Global/Workspace | `/command` | On-demand deterministic multi-step macros | `.md` (YAML + XML) |
| **Skills** | Global/Workspace | Intent-matched | Progressive capability extension | Directory (`SKILL.md`) |
| **Tools (MCP)** | Workspace | Always-available | Deterministic function execution | `.mcp.json` |
| **Artifacts** | Workspace | Auto-generated | Execution state tracking and proof-of-work | `.md` / `.jsonl` |

### 1.2 Scope Hierarchy and Directory Layout

```plaintext
<workspace>/
├── GEMINI.md                               # Master configuration and cognitive directives
├── .mcp.json                               # Workspace-scoped MCP tool registry
├── .context/                               # Knowledge base (project-specific)
│   ├── root-framework.md
│   └── architecture.md
├── artifacts/                              # Generated execution state plans and logs
│   ├── implementation_plan.md
│   └── task-XXXXXX.md
└── .agent/
    ├── rules/                              # Workspace Rules
    │   └── strict-python.md
    ├── workflows/                          # Workspace Workflows
    │   └── integration-deploy.md
    └── skills/                             # Workspace Skills
        └── ddr-inheritance-validator/
            ├── SKILL.md
            ├── scripts/
            └── resources/
```

---

## 2. Configuration Schemas

### 2.1 GEMINI.md (Master Configuration)

Replaces legacy personas. Controls cognitive load, model fallbacks, and multi-turn state.

```markdown
---
description: "Primary configuration for the workspace."
models: ["gemini-3.1-pro-preview", "gemini-3.1-pro", "gemini-3-flash"]
version: "20260223_v118"
scope: "workspace"
thinking_level: "medium"
temperature: 0.1
---

<workspace_context>
[Define heavy architectural context, tech stack, and primary libraries here.]
</workspace_context>

<cognitive_directives>
[Define reasoning parameters and structured output requirements here.]
</cognitive_directives>

<security_and_execution_guardrails>
[Define absolute boundaries, e.g., no destructive shell commands.]
</security_and_execution_guardrails>

<thought_signature_protocol>
MANDATORY: You must circulate all received thought signatures back into your subsequent turns without modification to prevent catastrophic context loss.
</thought_signature_protocol>
```

### 2.2 Rules (`.agent/rules/*.md`)

Defines conditional, file-specific guidelines injected dynamically by the semantic router. Workspace rules override global rules via priority scoring.

```markdown
---
name: strict-python-architecture
description: Enforces type safety and exception handling.
trigger: glob
globs: "*.py, src/**/*.py"
priority: critical
---

<constraints>
- **Type Safety:** All signatures must have comprehensive type hints.
- **Exception Handling:** Bare `except:` blocks are strictly prohibited.
</constraints>

<verification_step>
SILENT VERIFICATION INSTRUCTIONS:
Scan all newly generated `def` statements to confirm complete type annotations before emitting code.
</verification_step>
```

### 2.3 Workflows (`.agent/workflows/*.md`)

Defines active, user-triggered sequential operations. Workflows must utilize decision trees for deterministic logic forks.

```markdown
---
name: strict-integration-deploy
description: Orchestrates deployment pipeline involving testing and conditional merging.
---

### steps
1. **Context Assimilation:** Generate `Pre_Deployment_Audit.md`.
2. **Review Checkpoint:** Pause execution and request explicit human approval.
3. **Test Suite Execution (Decision Tree):** Run integration tests.
    - **IF** tests pass 100%, **THEN** proceed.
    - **IF** tests fail, **THEN** capture logs into `Error_Trace.md` and halt.

### verification_plan
- The `Pre_Deployment_Audit.md` must be explicitly approved prior to testing.
```

### 2.4 Skills (`.agent/skills/<name>/SKILL.md`)

Solves context saturation via progressive disclosure. Loaded only when the semantic router matches user intent to the frontmatter `description`.

```markdown
---
name: ddr-inheritance-validator
description: Validates inheritance chains and constraint violations in documentation.
---

<when_to_use>
- The user explicitly requests validation of the DDR framework.
- The active task involves saving or modifying a root constraints document.
</when_to_use>

<how_to_use>
1. **Verify Context:** Ensure Python 3.12+ is available.
2. **Execute Validation:** Run `python scripts/validate.py`.
3. **Parse Output:** If exit code is 2, generate a `conflict_report.md` artifact and immediately halt execution.
</how_to_use>

<resources_reference>
- `scripts/validate.py`
</resources_reference>
```

---

## 3. Execution State Artifacts

Relying on implicit LLM memory leads to context rot across long context windows. Antigravity v1.18.3 enforces state tracking via specific generated artifacts.

1. **Implementation Plan (`implementation_plan.md`):** Generated during PLANNING mode. Must contain `<phases>`, `<atomic_steps>`, and `<verification>` blocks. Requires human approval before the agent modifies codebase.
2. **Task List (`task.md` / `TASK-XXXXXX.md`):** Dynamic checklist governing atomic execution. Tracks `<task_dependencies>` and forces `<rollback_procedure>` definitions for fail-safes.
3. **Walkthrough (`walkthrough.md`):** Post-execution summary. Provides deterministic `<verification_steps>` (e.g., specific UI clicks or terminal commands) as proof-of-work for the human developer.

---

## 4. Execution Policies

Configure via **Settings → Agent Manager → Execution Policies**.

### 4.1 Terminal Execution Policy

- **Auto (Review-Driven):** Agent autonomously decides when to checkpoint based on command risk. Allows traceability scripts (`grep`, `find`) to run unblocked. *Recommended for DDR workloads.*
- **Off (Strict Mode):** Executes only commands in the allowlist. Poses issues for continuous tracing workflows.

### 4.2 JavaScript Execution Policy

- **Request Review:** Prompts before any browser subagent executes JS payload on a page. *Recommended.*

---

## 5. Tools (MCP): Deterministic Function Layer

Use direct Workspace configurations (`.mcp.json`) over Global configurations or Router patterns. This eliminates IPC latency hops and optimizes the Time to First Token (TTFT) for Gemini 3.1 Pro.

```json
{
  "mcpServers": {
    "project-api": {
      "command": "node",
      "args": ["./scripts/mcp-server.js"],
      "env": {
        "API_KEY": "${env:PROJECT_API_KEY}",
        "BASE_URL": "https://api.myproject.internal"
      }
    }
  }
}
```

---

## 6. Knowledge Injection Methods

Keep heavy architecture documents in `.context/`. Do not auto-load root files universally.

1. **`@`-mention:** Fastest method for on-demand injection (`@.context/architecture.md`).
2. **Rule-Based Load:** Triggered via globs when relevant files are open.
3. **Skill-Embedded:** Linked dynamically via `<resources_reference>` in a `SKILL.md` payload.

---

## 7. Configuration Precedence & Routing

**Routing Order:**

1. Workspace Rules override Global Rules (based on `priority` scoring).
2. Workspace Skills override Global Skills.
3. User `/command` triggers Workflows directly.
4. If no explicit command, semantic router matches intent to Skill `description`.
5. Global `GEMINI.md` anchors the entire context window continuously.

---

## Appendix A: CLI Reference (`agy`)

```bash
# Trigger a workflow directly
agy /validate-ddr

# Verify MCP tools are connected
agy --mcp-status

# Validate workflow schema syntax
agy --validate-workflow .agent/workflows/deploy.md

# List all discoverable skills via semantic router
agy --list-skills
```
