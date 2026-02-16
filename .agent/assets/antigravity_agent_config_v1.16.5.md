# Google Antigravity v1.16.5: Agent Configuration Technical Reference

> **Build**: `1.16.5-6703236727046144` | **Last Updated**: 2026-02-15 | **Document Version**: 4.3.0

---

## Executive Summary

Google Antigravity is an **agent-first development platform** — a VS Code fork — where autonomous agents plan, code, test, and browse on your behalf. All configuration is expressed through composable text assets (Personas, Rules, Workflows, Skills, MCP Tools, Knowledge) organized across a strict scope hierarchy.

This reference is optimized for **DDR (Documentation-Design-Reference) compliant agentic workflows**, incorporating architectural guidance for inheritance traceability, context saturation mitigation, and latency-sensitive toolchain design.

### v1.14.2 → v1.16.5 Delta

| Area | Change | Impact |
| :---- | :------ | :------ |
| CLI binary | `gemini` → `agy` | **Breaking** — update all scripts |
| Static asset directory | `references/` → `resources/` | **Breaking** — v1.16.5 treats `references/` as unknown; agent cannot find assets |
| Rule activation | `activation:` + `glob:` frontmatter formalized | Enables file-scoped and model-triggered rules |
| SKILL.md frontmatter | YAML `name:` + `description:` block supported | Required for reliable intent-matching |
| Workspace MCP | `.mcp.json` at project root | Preferred over global config for project-scoped tools |
| Preset name | "Secure Mode" → **Strict Mode** | Update any references in team docs |
| Agent modes | **Planning** / **Fast** modes formalized | Selectable per conversation |
| `@`-mention search | Significantly faster | Now the preferred on-demand context method |

> ⚠️ **Migration Priority**: Rename all `references/` directories to `resources/` before upgrading to v1.16.5. Failure to do so will cause skills to silently fail to locate their assets.

---

## 1. Architecture Overview

### 1.1 System Components

| Component | Function | Access |
| :---------- | :-------- | :------ |
| **Agent Manager** | Spawn, monitor, interact with parallel agents | `Cmd+E` |
| **Editor Surface** | VS Code-based editing with inline agent | `Cmd+I` |
| **Browser Subagent** | Headless Chrome automation and verification | Integrated extension |
| **Terminal Agent** | Shell command execution under policy control | Governed by Terminal Policy |
| **Artifact System** | Task outputs: plans, diffs, reports, logs | Auto-generated per task |

> **Parallel Agent Memory Ceiling (32 GB RAM)**: Each agent can consume up to its full Node.js heap allocation. Chromium 142.x browser subagent instances add a further 1–1.5 GB each. The table below shows allocated ceilings vs. observed typical peaks for a 3-agent DDR configuration on this hardware:
>
> | Component | Allocated (Max) | Actual Peak (Typical) |
> | :--------- | :-------------- | :-------------------- |
> | IDE + Language Server | 2.0 GB | 2.5 GB |
> | 3× Agents (8 GB heap each) | 24.0 GB | ~18.0 GB |
> | 3× Browser Subagents | 4.5 GB | ~3.0 GB |
> | Windows 11 Pro OS | 4.0 GB | 4.0 GB |
> | **Total** | **34.5 GB** | **~27.5 GB** |
>
> The ~27.5 GB typical peak leaves a **~4.5 GB buffer** for file system caching and OS overhead, preventing the Ryzen 9 5900X from being throttled by NVMe page-file swapping. At 4 agents hitting full heap + 4 browser instances, the worst-case projection is ~42 GB — exceeding physical RAM. **For high-inheritance DDR tasks, the hard limit is 3 concurrent complex agents.** Reserve a 4th slot only for lightweight orchestrator agents that do not trigger browser subagents or heavy `grep`/`find` operations.

### 1.2 Configuration Asset Taxonomy

| Asset | Scope | Activation | Purpose | Format |
| :------ | :---- | :--------- | :------- | :------ |
| **Personas** | Implicit / Defined | System instruction | Behavioral identity | Markdown in Rules / AGENTS.md |
| **Rules** | Global / Workspace | Configurable (see §4.2) | Immutable behavioral constraints | `.md` with YAML frontmatter |
| **Workflows** | Global / Workspace | `/command` trigger | Reusable prompt macros | `.md` with YAML frontmatter |
| **Skills** | Global / Workspace | Intent-matched (progressive) | On-demand capability extension | Directory (`SKILL.md`) or `.yaml` |
| **MCP Tools** | Global / Workspace | Always-available | Deterministic function execution | `mcp_config.json` / `.mcp.json` |
| **Knowledge** | Workspace | `@`-mention or rule-loaded | Domain-specific static context | Markdown / YAML / text |

### 1.3 Scope Hierarchy & File Layout

```
Global Scope (~/.gemini/)
├── GEMINI.md                                # Global Rules + Persona
└── antigravity/
    ├── mcp_config.json                      # Global MCP registry
    ├── security_config.json                 # Terminal + browser policies
    ├── browserAllowlist.txt
    ├── terminalAllowlist.txt                # Honored in Off mode only
    ├── terminalDenylist.txt                 # Always enforced
    ├── global_workflows/  *.md
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            ├── scripts/
            ├── resources/                   # ← v1.16.5: was 'references/' (BREAKING)
            └── examples/

Workspace Scope (<workspace>/)
├── AGENTS.md                                # Workspace Persona
├── .mcp.json                                # Workspace MCP config
├── .context/                                # Knowledge base
│   ├── root-framework.md                    # DDR: immutable root constraints
│   ├── architecture.md
│   ├── api-contracts.yaml
│   └── domain-glossary.md
└── .agent/
    ├── rules/           *.md
    ├── workflows/       *.md
    ├── skills/          <skill-name>/
    │                    ├── SKILL.md
    │                    ├── scripts/
    │                    ├── resources/
    │                    └── examples/
    └── execution-log.jsonl
```

**Precedence rule**: Workspace always overrides Global within the same asset type. This is a **binary override**, not additive inheritance — use `glob:` frontmatter in Rules to approximate multi-level scoping.

---

## 2. Execution Policies

### 2.1 Three Independent Policy Axes

Configure via **Settings → Agent Manager → Execution Policies** or the initial setup wizard.

#### Terminal Execution Policy

| Mode | Behavior | Risk |
| :---- | :-------- | :---- |
| **Off** | Executes only `terminalAllowlist.txt` commands | Lowest — but blocks `grep`, `find`, `python` unless explicitly listed |
| **Auto** *(recommended)* | Agent's risk model decides execution vs. review | Moderate — allows traceability scripts to run unblocked |
| **Turbo** | Executes everything except `terminalDenylist.txt` | Highest |

#### Review Policy

| Mode | Behavior |
| :---- | :-------- |
| **Always Proceed** | No review checkpoints |
| **Agent Decides** *(recommended)* | Agent self-checkpoints based on task risk |
| **Request Review** | Always pauses for explicit user approval |

#### JavaScript Execution Policy

| Mode | Behavior |
| :---- | :-------- |
| **Disabled** | No browser JS execution |
| **Request Review** *(recommended)* | Prompts before each execution |
| **Always Proceed** | Unrestricted; highest exposure |

### 2.2 Preset Profiles

| Profile | Terminal | Review | JS | Use Case |
| :-------- | :-------- | :------ | :-- | :-------- |
| **Strict Mode** *(formerly "Secure Mode")* | Off | Request Review | Disabled | Maximum safety — but **blocks traceability scripts**; not recommended for DDR |
| **Review-Driven** *(recommended for DDR)* | Auto | Agent Decides | Request Review | Balanced; allows `grep`/`find`/`python` to run without constant interruption |
| **Agent-Driven** | Turbo | Always Proceed | Always Proceed | Fully sandboxed environments only |
| **Custom** | User-defined | User-defined | User-defined | — |

> **DDR Policy Recommendation**: Use **Review-Driven** (`terminal_policy: auto`). Strict Mode's Off terminal policy will block the `grep` and `find` operations required by inheritance traceability scripts, causing constant workflow interruptions. Strict Mode is appropriate for production-facing or regulated environments, not documentation-framework agents.

**Security config** (`~/.gemini/antigravity/security_config.json`):

```json
{
  "terminal_policy": "auto",
  "allowlist": ["ls", "cat", "grep", "find", "python", "pytest", "git status", "git log"],
  "denylist": ["rm -rf", "DROP DATABASE", "DELETE FROM", "sudo rm", "mkfs", "dd if="],
  "require_confirmation_for": ["git push", "git reset --hard", "docker rm", "kubectl delete"],
  "node_options": {
    "NODE_OPTIONS": "--max-old-space-size=8192"
  },
  "ddr_sync": {
    "on_file_save": {
      "glob": [".context/**/*.md"],
      "action": "reindex_inheritance_graph",
      "skill": "ddr-inheritance-validator"
    }
  }
}
```

> `require_confirmation_for` enforces a mandatory user prompt for high-impact commands **regardless of the active Terminal Policy mode** — the correct mechanism for protecting destructive operations without switching to Off mode.

> **Node.js Heap**: On Windows 11 with Node.js 22.x, Agent Manager defaults to a ~4 GB heap. Setting `--max-old-space-size=8192` raises the ceiling to 8 GB, preventing IDE crashes when agents execute concurrent `grep`/`find` operations across large documentation trees. Note that this is a **per-process ceiling**, not a global allocation — agents only consume up to this limit if the workload demands it. However, if all 3–4 agents simultaneously reach their ceiling alongside active browser subagents (~1.5 GB each) and OS overhead (~4 GB), total RAM usage can approach or exceed 32 GB. Keep concurrent complex agents at **3 or fewer** for DDR workloads to maintain headroom and avoid disk swap.

> **DDR Sync Trigger**: `on_file_save` with the `.context/**/*.md` glob forces an inheritance graph re-index whenever any parent node is saved. This is the primary mitigation for the sync-lag race condition described in §11.1.

### 2.3 Agent Execution Modes

Selected per conversation from the **Planning / Fast** dropdown (`Cmd+L`).

| Mode | Behavior | Use When |
| :---- | :-------- | :-------- |
| **Planning** *(default)* | Produces task groups and intermediate Artifacts before executing | Complex documentation, refactors, multi-agent orchestration |
| **Fast** | Executes directly; no planning phase | Simple tasks: renaming, small bash commands, localized edits |

---

## 3. Personas: Behavioral Identity Layer

Personas are not standalone files — expressed through Rules, `AGENTS.md`, and Workflow preambles.

### 3.1 Implementation Patterns

#### Pattern A — Global Persona (`~/.gemini/GEMINI.md`)

```markdown
# Global Persona

You are a Senior Software Architect specializing in distributed systems.

## Core Principles
- Prioritize resilience over raw performance
- Design for failure scenarios first
- Question assumptions before implementing

## Behavioral Constraints
- Never auto-execute destructive operations (DROP, DELETE, rm -rf)
- Require explicit approval for production deployments
- Always propose architecture diagrams for complex changes
```

#### Pattern B — Workspace Persona (`<workspace>/AGENTS.md`)

```markdown
# Project Persona

You are a DDR-compliant documentation architect.

## Execution Protocol
1. **Silent execution**: No commentary between tool calls
2. **Parallel by default**: Execute independent operations simultaneously (max 4 agents)
3. **Templates first**: Check `.context/root-framework.md` before authoring any document
4. **Inheritance first**: Resolve all `inherits_from` references before generating content
```

**Auto-load instruction** — add to `~/.gemini/GEMINI.md`:

```markdown
## Workspace Persona Loading
- Check for AGENTS.md in the project workspace root
- Load all instructions from AGENTS.md as system-level constraints
- Recurse into sub-folders for section-specific AGENTS.md files
```

#### Pattern C — Workflow-Embedded Persona

```markdown
---
name: Architecture Review
trigger: /architecture-review
description: Critique system topology for resilience gaps
---

**Persona**: You are The Architect — a principal engineer focused on system design.

1. Analyze current system topology
2. Identify single points of failure
3. Propose resilience improvements
4. Generate architecture diagram artifact
```

### 3.2 Persona State Machine (Multi-Phase Workflows)

```markdown
---
name: Code Review
trigger: /review
description: Multi-phase review with sequential specialist persona hand-offs
---

## Phase 1: Security (Persona: Security Auditor)
Scan for hardcoded credentials; validate inputs; audit auth flows → security findings artifact.

## Phase 2: Performance (Persona: Performance Engineer)
Identify N+1 queries; review caching; check algorithmic complexity → recommendations artifact.

## Phase 3: Maintainability (Persona: Senior Developer)
Assess clarity; verify test coverage; check documentation completeness.

## Phase 4: Final Approval (Persona: Tech Lead)
**Trigger**: All previous phases passed.
Synthesize findings; issue merge authorization artifact.
```

---

## 4. Rules: Passive Behavioral Constraints

### 4.1 Characteristics

| Property | Value |
| :-------- | :---- |
| **Scope** | Global (`~/.gemini/GEMINI.md`) or Workspace (`.agent/rules/*.md`) |
| **Precedence** | Workspace overrides Global (binary, not additive) |
| **Immutability** | Workflows and skills cannot override rules |
| **Multi-level scope** | Use `glob:` frontmatter to approximate directory-level scoping |

### 4.2 Rule Activation Methods

| Method | Frontmatter | Behavior | Best For |
| :------ | :---------- | :-------- | :-------- |
| **Always On** | `activation: always_on` | Injected into every agent context | Universal coding standards |
| **Manual** | `activation: manual` | Loaded only when `@mentioned` | Heavy reference docs; load on-demand to avoid bloat |
| **Model Decision** | `activation: model_decision` | Agent self-loads when relevant | Inheritance guards, domain-specific constraints |
| **Glob** | `activation: always_on` + `glob:` | Activates on matched file patterns | Language-specific or directory-scoped rules |

### 4.3 Rule Implementation

#### Global Standards (`~/.gemini/GEMINI.md`)

```markdown
---
activation: always_on
---

# Global Development Standards

## Code Quality
* Follow PEP 8 (Python) / ESLint (JavaScript)
* Always use Numpy-style docstrings for Python
* Each new feature goes in its own file

## Security
* Never hardcode API keys or secrets; use environment variables
* Validate all user inputs; use parameterized DB queries only

## Testing
* Minimum 80% test coverage; write tests before implementation (TDD)
* Include edge case and error condition tests
```

#### File-Scoped Workspace Rule

```markdown
---
activation: always_on
glob: ["*.py", "tests/**/*.py"]
---

# Python-Specific Rules

## Type Hints
- All signatures must include type hints
- Use `from __future__ import annotations` for forward references
- Prefer `list[str]` over `List[str]` (Python 3.9+)

## Error Handling
- Never use bare `except:` clauses
- Always log exceptions with full context
- Use custom exception classes for business logic errors
```

#### DDR Inheritance Guard (Model Decision)

This rule activates automatically when the agent detects documents containing `inherits_from` metadata — eliminating the need to manually load it while avoiding token bloat in irrelevant contexts.

```markdown
---
activation: model_decision
description: Activates when creating or modifying a document that contains an 'inherits_from' field.
---

# Rule: DDR Traceability

## Inheritance Resolution Protocol
1. **Identify Parent**: Locate the file path in the `inherits_from` metadata field
2. **Context Injection**: Load the parent document via `@`-mention protocol
3. **Validation**: Verify all `REQUIRED_BY_PARENT` tags are satisfied in the current draft
4. **Failure State**: If a conflict is found, generate `conflict_report.md` artifact and halt

## Scope
Applies to all documents in `.context/` and `.agent/` that declare `inherits_from`.
```

#### On-Demand Security Rule (Manual)

```markdown
---
activation: manual
---

# Extended Security Audit Standards

## OWASP Compliance
- Apply all OWASP Top 10 mitigations
- Enforce CSP headers on all HTTP responses
- Require MFA for all admin operations

## Usage: @security-audit-rules
```

---

## 5. Workflows: On-Demand Prompt Macros

### 5.1 Characteristics

| Property | Value |
| :-------- | :---- |
| **Activation** | `/command` typed in Agent Manager |
| **Scope** | Global (`~/.gemini/antigravity/global_workflows/`) or Workspace (`.agent/workflows/`) |
| **Required frontmatter** | `name:`, `trigger:`, `description:` |

### 5.2 Workflow File Specification

```markdown
---
name: Generate Unit Tests
trigger: /generate-unit-tests
description: Creates comprehensive pytest unit tests for all Python modules
---

# Generate Unit Tests

## Discovery
Scan `src/` for all `.py` files; exclude `__init__.py` and existing test files.

## Test Generation
For each module: analyze public functions/classes; generate `tests/test_<module>.py`.
- Include: happy path, edge cases, error conditions
- Naming: `test_<function>_<scenario>`

## Validation
Run `pytest --collect-only`; generate artifact: `test_coverage_summary.md`.

## Quality
- Minimum 3 test cases per function; fixtures for shared setup
- Mock all external dependencies
```

### 5.3 Workflow → Skill Composition

```markdown
---
name: Full Stack Deploy
trigger: /deploy
description: End-to-end deployment pipeline composing multiple skills
---

## Phase 1: Quality    (Skill: code-quality-check) — linters, tests, coverage
## Phase 2: Build      (Skill: docker-build)        — images, tag with SHA, push
## Phase 3: Infra      (Skill: terraform-apply)     — validate + apply plan
## Phase 4: Deploy     (Skill: kubernetes-deploy)   — manifests, rollout, monitor
## Phase 5: Verify     (Skill: smoke-test)          — health endpoints, artifact
```

---

## 6. Skills: Progressive Capability Extension

### 6.1 Architecture Principle

Skills solve **context saturation**: a skill's full content loads only when the agent matches user intent to the skill's `description` frontmatter. All other skills consume zero context tokens.

```
User Request
    │
    ▼
Skill Discovery — match intent against frontmatter description only
    │
    ▼
Skill Loading (Progressive) — load SKILL.md; fetch scripts/resources/examples on-demand
    │
    ▼
Skill Execution → Artifacts
```

### 6.2 Skill Formats

| Format | Best For | Path |
| :------ | :-------- | :---- |
| **Directory + SKILL.md** | Multi-file skills with scripts, examples, resources | `.agent/skills/<name>/` |
| **Lightweight YAML** | Script-free, minimal-context skills | `.agent/skills/<name>.yaml` |

#### Directory Structure

```
<skill-name>/
├── SKILL.md           # Required
├── scripts/           # Optional: executable automation
├── resources/         # Optional: static assets (v1.16.5 — was references/)
├── examples/          # Optional: few-shot I/O pairs
└── assets/            # Optional: images, templates
```

#### Lightweight YAML Skill

```yaml
# .agent/skills/database-backup.yaml
name: Database Backup
description: Creates a timestamped backup of the development PostgreSQL database.
trigger: manual

steps:
  - Verify database connectivity
  - Create ./backups/ directory if absent
  - Execute: pg_dump -Fc dbname > ./backups/db_$(date +%Y%m%d_%H%M%S).dump
  - Verify backup file size > 0
  - Report success with file path and size
```

### 6.3 SKILL.md Specification

```markdown
---
name: git-commit-formatter
description: Enforces Conventional Commits specification for all git commit messages.
---

# Skill: Git Commit Formatter

## Trigger Patterns
- User writes or requests a commit message
- Workflow includes a commit step

## Commit Type Detection
| Keyword | Type |
| :------- | :---- |
| "fix", "bug" | `fix:` |
| "feature", "add" | `feat:` |
| "docs", "documentation" | `docs:` |
| "refactor" | `refactor:` |
| "test" | `test:` |
| "chore", "build" | `chore:` |

## Message Format
`<type>(<scope>): <subject>` — lowercase, imperative mood, ≤ 50 chars, no trailing period.

## Deliverables
Artifact: `formatted_commit.txt` → prompt for approval before `git commit`
```

### 6.4 Skill Patterns

| Pattern | Structure | Use Case |
| :------- | :-------- | :-------- |
| **Basic Router** | `SKILL.md` only | Simple instruction sets |
| **Resource** | `SKILL.md` + `/resources` | Large static docs; fetched on-demand |
| **Few-Shot** | `SKILL.md` + `/examples` | Complex transformations via I/O pairs |
| **Script Delegation** | `SKILL.md` + `/scripts` | Deterministic operations delegated to scripts |

**Script Delegation example**:

```markdown
---
name: database-migration
description: Executes versioned database migrations with automatic rollback on failure.
---

# Skill: Database Migration

## Instructions
1. Detect environment (dev / staging / prod)
2. Default to dry-run: `python scripts/migrate.py --env <env> --dry-run`
3. Present output; require explicit confirmation before live run
4. On non-zero exit: `bash scripts/rollback.sh --env <env>`
5. Generate artifact: `migration_log.md`

## Safety
- **Production**: `--dry-run` mandatory; remove only on explicit confirmation
- **Staging**: Approval required for schema-altering operations
- **Dev**: Full permissions
```

### 6.5 DDR Validator Skill

This skill provides deterministic inheritance traceability for DDR-compliant documentation frameworks. It wraps `agy --validate-workflow` in a Python script that traverses the document tree and checks Markdown cross-references.

```markdown
---
name: ddr-inheritance-validator
description: Validates DDR document inheritance chains; checks that child documents satisfy all parent REQUIRED_BY_PARENT constraints.
---

# Skill: DDR Inheritance Validator

## Trigger Patterns
- User runs `/validate-ddr` workflow
- Agent detects `inherits_from:` field in any document under `.context/` or `.agent/`
- Post-edit hook on any `.context/*.md` file

## Instructions
1. Invoke: `python scripts/validate_inheritance.py --root .context/root-framework.md`
2. Script traverses the `inherits_from` graph top-down
3. For each child node:
   a. Load parent document via `@`-mention
   b. Extract all `REQUIRED_BY_PARENT:` tags
   c. Verify each tag is satisfied in the child document
4. Interpret exit codes as follows:

| Exit Code | Meaning | Agent Action |
| :--------- | :------- | :----------- |
| `0` | Clean pass | Generate `artifacts/inheritance_tree.md`; continue |
| `1` | Soft warning — constraint violation | Generate `artifacts/conflict_report.md`; halt and prompt user |
| `2` | **Dependency loop detected** | Present `artifacts/inheritance_tree.md` to user; **do not attempt auto-fix**; request structural clarification before proceeding |

> ⚠️ **Exit code `2` is a hard halt.** A dependency loop (A inherits B inherits A) cannot be resolved by the agent deterministically. Attempting auto-resolution risks compounding the structural corruption. The user must manually restructure the inheritance graph.

## Script Interface
```bash
# Full validation
python scripts/validate_inheritance.py --root .context/root-framework.md

# Single document check
python scripts/validate_inheritance.py --doc .context/subsystem-auth.md

# Dry-run (report only, no halt)
python scripts/validate_inheritance.py --root .context/root-framework.md --dry-run
```

## Deliverables
- `artifacts/conflict_report.md` — violations with file paths and offending tags
- `artifacts/inheritance_tree.md` — resolved dependency graph (Mermaid format)

## Dependencies
- Python 3.9+
- `scripts/validate_inheritance.py` (see `/scripts`)
- `agy --validate-workflow` for workflow syntax checks

## Deployment Prerequisites
Before first use, ensure the following steps are completed in the `agy` terminal environment:

```bash
# Mark script executable
chmod +x .agent/skills/ddr-inheritance-validator/scripts/validate_inheritance.py

# Verify Python resolves correctly within the agy terminal context
# (agy spawns its own shell; system PATH may differ from your login shell)
agy "run: python --version"

# If Python is not found, add an explicit symlink or path export to GEMINI.md:
# export PATH="/path/to/python3/bin:$PATH"
```

> **Windows 11 note**: `chmod` is not applicable on NTFS. Instead, confirm that the Python executable referenced in your `PATH` is accessible from within the `agy`-spawned terminal session. The `agy` terminal inherits the system `PATH` at launch time — if Python was installed after Antigravity, a full IDE restart is required for the path to be picked up.
```

### 6.6 Skills vs. MCP Tools

| Factor | Skill | MCP Tool |
| :------ | :---- | :-------- |
| Architecture | File-based; ephemeral | Client-server; persistent process |
| Overhead | Low | Higher; running process per server |
| Context loading | Progressive; on-demand only | Always injected |
| State | Stateless | Stateful |
| Latency | Low (local execution) | Variable (network + IPC) |
| Best for | Multi-step procedures, codegen, validation scripts | External APIs, databases, Slack, GitHub |

---

## 7. MCP Tools: Deterministic Function Layer

### 7.1 Architecture

MCP tools are always available once configured — no progressive loading. Calls are synchronous IPC between Agent Manager and the MCP server process.

### 7.2 Global MCP Configuration (`~/.gemini/antigravity/mcp_config.json`)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/postgres",
               "postgresql://user:pass@localhost/db"]
    }
  }
}
```

### 7.3 Workspace MCP Configuration (`<workspace>/.mcp.json`)

Preferred for project-scoped tools. Keeps workspace concerns isolated from global config.

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

### 7.4 MCP Router Pattern — Use With Caution

The router pattern routes all tool calls through a single proxy MCP server that dynamically loads backends.

```json
{
  "mcpServers": {
    "router": {
      "command": "npx",
      "args": ["-y", "rube-mcp"],
      "env": { "RUBE_BACKENDS": "github,slack,postgres,notion" }
    }
  }
}
```

> ⚠️ **DDR / Latency Warning**: The router pattern adds one IPC hop to every tool call, increasing Time to First Token (TTFT). For documentation validation workflows where tool call latency must stay under ~200 ms, use **direct workspace `.mcp.json` connections** instead of the router. Reserve the router pattern for exploratory or background tasks where latency is not critical.

---

## 8. Knowledge: Domain-Specific Context

### 8.1 Structure

```
<workspace>/.context/
├── root-framework.md        # DDR: immutable root constraints (load via @-mention)
├── architecture.md
├── api-contracts.yaml
└── domain-glossary.md
```

### 8.2 Injection Methods

| Method | Syntax | When to Use |
| :------ | :------ | :----------- |
| **`@`-mention** | `@.context/root-framework.md` | On-demand; explicit in prompt — preferred for heavy docs |
| **Skill-embedded** | Directive in SKILL.md | Knowledge always needed by a specific skill |
| **Rule-based auto-load** | Directive in `GEMINI.md` | Relevant every session; low-weight files only |
| **Resource-bundled** | Files in `skill/resources/` | Knowledge scoped entirely to one skill |

> **DDR Context Strategy**: Keep `root-framework.md` out of `always_on` auto-load. Load it via `@`-mention in the DDR Inheritance Guard rule (§4.3) and DDR Validator Skill (§6.5). This prevents the root constraints document from consuming context tokens on every unrelated agent task.

**Rule-based auto-load** (`~/.gemini/GEMINI.md`):

```markdown
## Knowledge Context Protocol
- Check for `.context/` in the workspace root
- Load `architecture.md` for system design questions
- Load `domain-glossary.md` for business terminology questions
- Always cite source file when referencing knowledge base content
- Do NOT auto-load `root-framework.md` — load via @-mention only
```

---

## 9. Configuration Precedence

### 9.1 Hierarchy

```
Highest Priority
    ▼
1. Workspace Rules          .agent/rules/*.md
2. Workspace Skills         .agent/skills/*/SKILL.md
3. Global Rules             ~/.gemini/GEMINI.md
4. Global Skills            ~/.gemini/antigravity/skills/
5. MCP Tools                mcp_config.json / .mcp.json
    ▼
Lowest Priority
```

> **Important**: Precedence is a **binary override** — workspace replaces global for the same rule. It is not additive inheritance. To approximate multi-level inheritance (e.g., root → parent → leaf constraints in DDR), use `glob:` frontmatter to scope rules to specific directory patterns, and enforce cross-document validation via the DDR Validator Skill.

### 9.2 Conflict Resolution

| Scenario | Resolution |
| :-------- | :--------- |
| Workspace Rule ≠ Global Rule | Workspace wins |
| Workflow invokes restricted operation | Rule blocks execution — rules are immutable |
| Multiple skills match same intent | Agent scores by frontmatter `description` relevance |
| MCP Tool vs. Skill approach | Skill provides methodology; tool provides execution |
| DDR inheritance conflict detected | DDR Validator halts and generates `conflict_report.md` |

### 9.3 Activation Flow

```
User Request
    │
    ▼
1. Load Global Rules (always_on)
    │
    ▼
2. Load Workspace Rules (override globals)
    │
    ▼
3. Apply glob-matched rules for files in context
    │
    ▼
4. Evaluate model_decision rules (e.g., DDR Inheritance Guard)
    │
    ▼
5. Apply Persona (GEMINI.md / AGENTS.md)
    │
    ▼
6. Check for /workflow trigger
    ├── Match  → Execute workflow → compose skills → call tools
    └── No match → Skill Discovery (intent → description match)
    │
    ▼
7. Inject always-available MCP Tools
    │
    ▼
8. Execute with all constraints enforced
   → Generate Artifacts → Request review if policy dictates
```

---

## 10. DDR-Optimized Workspace Configuration

This section provides a reference configuration for DDR-compliant agentic documentation workflows, incorporating the Stateful Traceability Pattern.

### 10.1 Recommended DDR File Structure

```
<workspace>/
├── AGENTS.md                                # DDR-aware Persona
├── .mcp.json                                # Direct workspace MCP (no router)
├── .context/
│   ├── root-framework.md                    # Immutable root constraints (@-mention only)
│   ├── architecture.md
│   └── domain-glossary.md
└── .agent/
    ├── rules/
    │   ├── ddr-schema.md                    # always_on + glob: ["**/*.md"]
    │   └── python-standards.md              # always_on + glob: ["*.py"]
    ├── workflows/
    │   ├── validate-ddr.md                  # /validate-ddr trigger
    │   └── generate-tests.md
    └── skills/
        └── ddr-inheritance-validator/
            ├── SKILL.md
            └── scripts/
                └── validate_inheritance.py
```

### 10.2 DDR Schema Rule

```markdown
---
activation: always_on
glob: ["**/*.md"]
---

# Rule: DDR Document Schema

## Frontmatter Placement (Critical)
YAML frontmatter MUST be the very first content in every `.md` file and MUST
fit within the first 512 bytes. The `activation: model_decision` Inheritance Guard
(§4.3) relies on the Language Server scanning the first 1024 tokens of a file —
if large headers or boilerplate precede the frontmatter, the rule will silently
fail to trigger. No content, comments, or blank lines may appear before the
opening `---` delimiter.

## Required YAML Frontmatter (all .md documents)

```yaml
---
id: <unique-kebab-id>
title: <Document Title>
version: <semver>
inherits_from: <relative/path/to/parent.md>  # omit for root documents
status: draft | review | approved
---
```

## Enforcement
If a document is missing required frontmatter fields, OR if the frontmatter does
not begin at byte 0 of the file, halt and prompt the user to correct the
structure before continuing.
```

### 10.3 DDR Validation Workflow

```markdown
---
name: Validate DDR Inheritance
trigger: /validate-ddr
description: Runs the DDR Inheritance Validator skill across the full .context/ tree
---

# DDR Validation Workflow

## Phase 1: Schema Check (Skill: `ddr-inheritance-validator`)
Verify all `.context/*.md` files contain valid frontmatter.

## Phase 2: Inheritance Traversal (Skill: `ddr-inheritance-validator`)
Execute: `python scripts/validate_inheritance.py --root .context/root-framework.md`
Halt on any conflict; generate `artifacts/conflict_report.md`.

## Phase 3: Report
On clean pass: generate `artifacts/inheritance_tree.md` (Mermaid graph).
Notify user with summary of validated nodes and depth of inheritance chain.
```

---

## 11. Advanced Patterns

### 11.1 Multi-Agent Orchestration

> ⚠️ **Sync-Lag / Compliance Drift Risk**: Antigravity v1.16.5 does **not** hot-reload injected context into an active agent session. If the Orchestrator agent modifies `root-framework.md` while a Leaf Author agent is mid-generation, the Leaf Author will complete its document against a **stale version** of the parent. The DDR Validator will not catch this drift until the next `/validate-ddr` run.
>
> **Mitigation**: The `on_file_save` DDR sync trigger (§2.1) re-indexes the inheritance graph on every parent save, making drift detectable immediately. For critical root changes, use **sequential orchestration** — pause all Leaf Author agents, apply the root change, run `/validate-ddr`, then resume. Never modify `root-framework.md` while dependent agents are active.

```markdown
---
name: Microservices Refactor
trigger: /refactor-services
description: Spawns parallel agents per service with sync checkpoints (max 4 concurrent)
---

## Agent Allocation (max 3 complex agents for DDR; reserve slot 4 for lightweight orchestrator only)
- **Agent A** (Workspace: `service-auth`): Refactor authentication
- **Agent B** (Workspace: `service-payment`): Refactor payments
- **Agent C** (Workspace: `service-notification`): Refactor notifications
- **Agent D** (Orchestrator — lightweight): API contract merge + end-to-end tests

## Synchronization Points
1. Agents A-C complete API contract definition
2. Agent D merges contracts → `shared-contracts.yaml`
3. **Checkpoint**: Pause A-C; run `/validate-ddr`; confirm no compliance drift
4. Agents A-C implement against merged contracts
5. Agent D runs end-to-end test suite
```

### 11.2 Self-Improving Knowledge Base

```markdown
---
name: self-improvement-logger
description: Logs agent decisions and outcomes; generates rule proposals from failure patterns.
---

# Skill: Self-Improvement Logger

## Execution Logging
After every significant decision, append to `.agent/execution-log.jsonl`:
```json
{
  "timestamp": "2026-02-15T10:30:00Z",
  "user_intent": "...",
  "approach": "...",
  "outcome": "SUCCESS | FAILURE",
  "duration_seconds": 0
}
```

## Monthly Review
1. Analyze log for recurring failure patterns
2. Generate `suggested-rules.md`
3. Prompt user for review before applying any changes
```

---

## 12. Security & Guardrails

### 12.1 Browser Security

```
~/.gemini/antigravity/browserAllowlist.txt
────────────────────────────────────────
localhost
127.0.0.1
*.internal.company.com
staging.myapp.com
docs.google.com
github.com
```

```markdown
## Browser Policy (GEMINI.md)
- Navigate only to domains in browserAllowlist.txt
- Prompt before accessing any unlisted domain
- Never auto-submit forms on external sites
- Always request permission before downloading files
```

### 12.2 Secrets Management

- Use `${ENV_VAR}` / `${env:VAR}` substitution in all JSON configs — never hardcode
- Store secrets in Antigravity's encrypted credential store
- Add `.mcp.json` secrets and `mcp_secrets.json` to `.gitignore`

### 12.3 Version Control

```gitignore
# Never commit
.gemini/logs/
.agent/state/
artifacts/tmp/
mcp_secrets.json

# Commit (team-shared)
# .agent/rules/
# .agent/workflows/
# .agent/skills/
# AGENTS.md
# .context/
# .mcp.json  (with ${env:VAR} only — no raw secrets)
```

---

## 13. Testing & Validation

### 13.1 CLI Reference (`agy`)

```bash
agy /validate-ddr                             # Run DDR inheritance validation
agy /deploy --dry-run                         # Dry-run deployment workflow
agy --mcp-status                             # Verify MCP connections
agy --list-skills                            # List discoverable skills
agy --validate-workflow .agent/workflows/release.md
tail -f ~/.gemini/logs/agent.log             # Stream agent logs
```

### 13.2 CI Validation

```yaml
# .github/workflows/validate-antigravity.yml
name: Validate Antigravity Configuration
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @google/antigravity
      - name: Validate Workflows
        run: for wf in .agent/workflows/*.md; do agy --validate-workflow "$wf"; done
      - name: Validate DDR Inheritance
        run: python .agent/skills/ddr-inheritance-validator/scripts/validate_inheritance.py
               --root .context/root-framework.md --dry-run
      - name: Smoke-check Skills
        run: agy --list-skills
```

### 13.3 Skill Test Template

```markdown
# Skill Test: <Name>

## Test 1 — Basic Functionality
Input: [data]  |  Expected: [result]  |  Validation: [how to verify]

## Test 2 — Edge Case
Input: [data]  |  Expected: [handling]  |  Validation: [steps]

## Test 3 — Error Handling
Input: [invalid]  |  Expected: [graceful failure]  |  Validation: [steps]
```

---

## 14. Troubleshooting

| Problem | Diagnosis | Solution |
| :------- | :-------- | :-------- |
| Skill can't find asset | `references/` not renamed | Rename to `resources/`; v1.16.5 treats old path as unknown |
| Traceability scripts blocked | Terminal Policy = Off | Switch to Auto (Review-Driven profile) |
| Workflow not triggering | Wrong trigger syntax | Ensure `trigger: /exact-command` in frontmatter |
| Skill not loading | Vague description | Rewrite `description:` as action-oriented phrase |
| Skill over-activating | Broad description | Narrow it; switch to `activation: manual` |
| MCP tool unavailable | Server not started | Check JSON syntax; verify env vars; `agy --mcp-status` |
| High TTFT on tool calls | Using MCP Router | Replace with direct `.mcp.json` workspace connection |
| Context overflow | Too many skills loading | Tighten `description:` fields; use `model_decision` activation |
| 4+ agents degrading / disk swap | Node.js heap + browser RAM exceeds 32 GB | Reduce DDR agents to ≤ 3; avoid browser subagents in parallel DDR tasks |
| Inheritance Guard not triggering | Frontmatter not in first 512 bytes | Move YAML frontmatter to byte 0; remove all preceding content |
| Compliance Drift after root change | Stale context in active agent | Pause dependent agents; run `/validate-ddr`; resume after clean pass |
| Exit code 2 from validator | Dependency loop in inheritance graph | Do not auto-fix; present `inheritance_tree.md` to user for manual restructure |
| `validate_inheritance.py` not found | Script not on Python path in `agy` terminal | Confirm Python is in system PATH before IDE launch; restart IDE if installed after |
| `validate_inheritance.py` permission denied | Script not executable (Linux/macOS) | `chmod +x .agent/skills/ddr-inheritance-validator/scripts/validate_inheritance.py` |
| `agy` not found | Old `gemini` CLI | `npm install -g @google/antigravity` |
| `.mcp.json` ignored | Pre-v1.16.5 install | Update to v1.16.5+; confirm file is at workspace root |

**Inspect active context**:

```
"Debug: List all loaded rules, active skills, and available MCP tools."
```

---

## 15. Reference Summary

### 15.1 Asset Interaction Matrix

| From → To | Personas | Rules | Workflows | Skills | MCP Tools | Knowledge |
| :--------- | :------- | :---- | :-------- | :----- | :-------- | :-------- |
| **Personas** | N/A | Embedded in Rules | Define phase personas | Guides execution style | N/A | Shapes interpretation |
| **Rules** | Defines global persona | Can cross-reference | **CONSTRAINS** | **CONSTRAINS** | Restricts usage | N/A |
| **Workflows** | Invokes per-phase personas | **OBEYS** | Can chain | **COMPOSES** | Orchestrates calls | References files |
| **Skills** | Adopts execution persona | **OBEYS** | Invoked by | Can depend on others | Calls for execution | Bundles in `resources/` |
| **MCP Tools** | N/A | **OBEYS** | Called by | Called by | Can compose others | N/A |
| **Knowledge** | Informs persona | N/A | Provides context | Provides reference | N/A | Can cross-reference |

### 15.2 When to Use Each Asset

| Use Case | Asset | Key Detail |
| :-------- | :---- | :---------- |
| Universal coding standards | **Rule** (`always_on`) | Injected into every context |
| Language/file-specific standards | **Rule** with `glob:` | Activates on matched files only |
| DDR inheritance guard | **Rule** (`model_decision`) | Loads only when `inherits_from` detected |
| Reusable multi-step prompt | **Workflow** | `/command` trigger |
| On-demand domain capability | **Skill** (directory) | Progressive; intent-matched |
| Simple script-free tasks | **Skill** (YAML) | Minimal context footprint |
| External API / DB integration | **MCP Tool** | Direct `.mcp.json` for latency-sensitive work |
| Behavioral identity | **Persona** (Rules / AGENTS.md) | Persistent across all interactions |
| Static reference material | **Knowledge** (`.context/`) | `@`-mention for heavy docs |

### 15.3 File Locations Cheat Sheet

```
~/.gemini/GEMINI.md                              Global Rules + Persona
~/.gemini/antigravity/mcp_config.json            Global MCP registry
~/.gemini/antigravity/security_config.json       Terminal + browser policies
~/.gemini/antigravity/browserAllowlist.txt       Browser domain allowlist
~/.gemini/antigravity/terminalDenylist.txt       Always-enforced denylist
~/.gemini/antigravity/terminalAllowlist.txt      Allowlist (Off mode only)
~/.gemini/antigravity/global_workflows/          Global Workflows
~/.gemini/antigravity/skills/                    Global Skills

<workspace>/AGENTS.md                           Workspace Persona
<workspace>/.mcp.json                           Workspace MCP (v1.16.5)
<workspace>/.context/                           Knowledge base
<workspace>/.context/root-framework.md          DDR root constraints (@-mention only)
<workspace>/.agent/rules/                       Workspace Rules
<workspace>/.agent/workflows/                   Workspace Workflows
<workspace>/.agent/skills/                      Workspace Skills
<workspace>/.agent/execution-log.jsonl          Agent decision log
```

### 15.4 Syntax Quick Reference

```markdown
# Rule frontmatter
---
activation: always_on | manual | model_decision
glob: ["*.py", "src/**/*.ts"]   # optional; implies always_on
---

# Workflow frontmatter (all three required)
---
name: Display Name
trigger: /command
description: One-line summary
---

# SKILL.md frontmatter (required for intent-matching)
---
name: skill-kebab-name
description: Action-oriented, intent-rich phrase
---
```

```json
// MCP entry
"serverName": {
  "command": "executable",
  "args": ["arg1"],
  "env": {"KEY": "${ENV_VAR}"}
}
```

---

## 16. Keyboard Shortcuts

| Shortcut | Action |
| :-------- | :------ |
| `Cmd + E` | Open Agent Manager panel |
| `Cmd + L` | Open chat / toggle Planning ⇄ Fast |
| `Shift + Cmd + L` | New Agent conversation |
| `Cmd + I` | Inline agent chat in Editor |
| `Cmd + ,` | Settings |
| `` Ctrl + ` `` | Toggle terminal |
| `Tab` | Accept completion |
| `Escape` | Cancel agent operation |
| `Cmd + Enter` | Approve pending action |
| `Cmd + Backspace` | Reject pending action |

---

## 17. Version History

| Version | Release | Key Changes |
| :------- | :------ | :---------- |
| **1.16.5** | 2025-12-22 | Strict Mode; `.mcp.json`; rule `activation:`/`glob:`; `resources/` (breaking); SKILL.md frontmatter; `agy` CLI |
| 1.15.8 | 2025-11 | Multi-model support; Planning/Fast modes |
| 1.14.2 | 2025-10 | Skills framework; initial SKILL.md spec |
| 1.13.3 | 2025-09 | Browser subagent; initial MCP integration |

**Update cadence**: Auto-updates 3× weekly (Mon/Wed/Fri, 09:00 UTC).

---

## Appendix A: Migration Checklist (v1.14.2 → v1.16.5)

| # | Action | Priority |
| :- | :------ | :-------- |
| 1 | Rename all `references/` → `resources/` in skill directories | **Critical** |
| 2 | Update all scripts: `gemini` → `agy` | **Critical** |
| 3 | Add YAML frontmatter to all `SKILL.md` files (`name:`, `description:`) | High |
| 4 | Add `activation:` frontmatter to all rule files | High |
| 5 | Move project-specific MCP servers to `.mcp.json` at workspace root | Medium |
| 6 | Set `--max-old-space-size=8192` in `security_config.json` | **Critical for DDR** |
| 7 | Mark `validate_inheritance.py` executable; confirm Python in `agy` terminal PATH | **Critical for DDR** |
| 8 | Update team docs: "Secure Mode" → "Strict Mode" | Low |
| 9 | Switch DDR workflows from Strict Mode → Review-Driven profile | **Critical for DDR** |

## Appendix B: Traditional IDE Migration

| Traditional Feature | Antigravity Equivalent |
| :------------------ | :--------------------- |
| Code snippets | Workflows (`/trigger`) |
| Linter configs | Rules with `glob:` frontmatter |
| IDE plugins | Skills (progressive loading) |
| External tools | MCP Tools (direct `.mcp.json`) |
| Workspace settings | `.agent/` directory |
| Project documentation | `.context/` knowledge base |
| Code templates | Skill `examples/` directory |

## Appendix C: Reference Links

- **Official Docs**: [antigravity.google/docs](https://antigravity.google/docs)
- **Download**: [antigravity.google/download](https://antigravity.google/download)
- **Getting Started Codelab**: [codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **AI Studio**: [aistudio.google.com](https://aistudio.google.com)
