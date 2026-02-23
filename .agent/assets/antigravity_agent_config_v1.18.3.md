# Google Antigravity v1.18.3: Agent Configuration Technical Reference

> **Build**: `1.18.3-8904536727049921` | **Last Updated**: 2026-02-23 | **Document Version**: 5.0.0

---

## Executive Summary

Google Antigravity is an **agent-first development platform** where autonomous agents plan, code, test, and browse on your behalf. All configuration is expressed through strict, schema-compliant text assets organized across a global and workspace scope hierarchy.

This reference is explicitly optimized for **Gemini 3.1 Pro**, enforcing strict separation of machine-parseable YAML frontmatter and LLM-consumable XML body content. It utilizes the "Trust but Verify" execution paradigm via explicit Artifact generation.

### v1.16.5 → v1.18.3 Delta

| Area                   | Change                                         | Impact                                                                         |
| :--------------------- | :--------------------------------------------- | :----------------------------------------------------------------------------- |
| **Personas** | Deprecated                                     | Replaced entirely by `GEMINI.md` and the `thought_signature_protocol`.         |
| **Schema Structure** | Strict Frontmatter / Body split                | Flat JSON/YAML schemas are rejected; all assets must use `<xml_fencing>`.      |
| **Rule Triggering** | `activation` → `trigger`                       | Updated YAML frontmatter syntax. Priority sorting is now mandatory.            |
| **Skill Loading** | `<when_to_use>` progressive disclosure         | Legacy `type`, `scope`, and `priority` removed from Skills.                    |
| **Execution State** | Artifact-driven memory                         | Workflows must explicitly generate `implementation_plan.md` and `task.md`.     |

---

## 1. Asset Taxonomy & Directory Structure

Antigravity v1.18.3 routes semantic capabilities automatically based on file placement and YAML frontmatter.

```text
<workspace>/
├── GEMINI.md                                # Master configuration and cognitive directives
├── .mcp.json                                # Project-scoped MCP tools
├── .agent/
│   ├── rules/           *.md                # Immutable constraints (auto/glob/always_on)
│   ├── workflows/       *.md                # /command triggered multi-step macros
│   └── skills/          <skill-name>/
│                        ├── SKILL.md        # Progressive capability extension
│                        ├── scripts/
│                        └── resources/
└── artifacts/           *.md                # Generated execution state plans and logs
```

---

## 2. Configuration Schemas

### 2.1 GEMINI.md (Master Configuration)

Replaces legacy personas. Controls cognitive load, model fallbacks, and multi-turn state via the `thought_signature_protocol`.

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
Define your heavy architectural context, tech stack, and primary libraries here.
</workspace_context>

<cognitive_directives>
Define reasoning parameters and structured output requirements here.
</cognitive_directives>

<security_and_execution_guardrails>
Define absolute boundaries (e.g., no destructive shell commands).
</security_and_execution_guardrails>

<thought_signature_protocol>
MANDATORY: You must circulate all received thought signatures back into your subsequent turns without modification to prevent catastrophic context loss.
</thought_signature_protocol>
```

### 2.2 Rules (`.agent/rules/*.md`)

Defines conditional, file-specific guidelines and negative constraints injected dynamically by the semantic router.

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

Defines active, user-triggered sequential operations for repetitive engineering tasks. Utilizes explicit decision trees.

```markdown
---
name: strict-integration-deploy
description: Orchestrates deployment pipeline involving testing and conditional merging.
---

### steps
1. **Context Assimilation:** Generate `Pre_Deployment_Audit.md`.
2. **Review Checkpoint:** Pause execution and request explicit human approval.
3. **Test Suite Execution (Decision Tree):** Run the integration tests.
    - **IF** tests pass 100%, **THEN** proceed.
    - **IF** tests fail, **THEN** capture logs into `Error_Trace.md` and halt.

### verification_plan
- The `Pre_Deployment_Audit.md` must be explicitly approved prior to testing.
```

### 2.4 Skills (`.agent/skills/<name>/SKILL.md`)

Defines executable capabilities loaded strictly on-demand via progressive disclosure.

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
3. **Parse Output:** If exit code is 2, generate a `conflict_report.md` artifact and immediately halt execution to await human resolution.
</how_to_use>

<resources_reference>
- `scripts/validate.py`
</resources_reference>
```

---

## 3. Execution State Artifacts

Relying on implicit LLM memory leads to context rot. Antigravity v1.18.3 enforces state tracking via specific generated artifacts:

1. **Implementation Plan (`implementation_plan.md`):** The technical design document generated during PLANNING mode. Must contain `<phases>`, `<atomic_steps>`, and `<verification>` blocks. Requires human approval before the agent modifies code.
2. **Task List (`task.md`):** The dynamic checklist governing atomic steps. Tracks `<task_dependencies>` and forces `<rollback_procedure>` definitions for fail-safes.
3. **Walkthrough (`walkthrough.md`):** The post-execution summary. Provides deterministic `<verification_steps>` (e.g., terminal commands) for the human developer to prove the agent's work was successful.

---

## 4. MCP Tools

Use direct Workspace configurations (`.mcp.json`) over Global configurations or Router patterns to eliminate IPC latency hops and optimize the Time to First Token (TTFT).

```json
{
  "mcpServers": {
    "project-api": {
      "command": "node",
      "args": ["./scripts/mcp-server.js"],
      "env": {
        "API_KEY": "${env:PROJECT_API_KEY}"
      }
    }
  }
}
```
