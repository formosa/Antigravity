# Google Antigravity v1.16.5: Agent Configuration Technical Reference

> **Build**: `1.16.5-6703236727046144` | **Last Updated**: 2026-02-15 | **Document Version**: 3.0.0

---

## Executive Summary

Google Antigravity is an **agent-first development platform** — a VS Code fork — where autonomous agents plan, code, test, and browse on your behalf. Configuration is expressed through a small set of composable text-based assets (Personas, Rules, Workflows, Skills, MCP Tools, Knowledge) organized across a strict scope hierarchy. This reference covers every asset type, all execution policy axes, security guardrails, and operational patterns, validated against the v1.16.5 release.

### v1.14.2 → v1.16.5 Delta

| Area | Change |
| :---- | :------ |
| CLI binary | `gemini` → `agy` *(breaking)* |
| Preset profile name | "Secure Mode" → **Strict Mode** |
| SKILL.md | YAML frontmatter (`name:`, `description:`) now supported |
| Skill static assets dir | `references/` → `resources/` *(canonical rename)* |
| Rule activation | `activation:` and `glob:` frontmatter fields formalized |
| Workspace MCP | `.mcp.json` at project root now valid alternative to global config |
| Execution policy | Expanded from single-axis to three independent axes |
| Agent modes | **Planning** and **Fast** modes formalized with UI dropdown |
| `@`-mention search | Significantly faster context injection |

---

## 1. Architecture Overview

### 1.1 System Components

| Component | Function | Access |
| :---------- | :-------- | :------ |
| **Agent Manager** | Spawn, monitor, and interact with parallel agents | `Cmd+E` |
| **Editor Surface** | VS Code-based editing with inline agent | `Cmd+I` |
| **Browser Subagent** | Headless Chrome automation and web verification | Integrated extension |
| **Terminal Agent** | Shell command execution under policy control | Governed by Terminal Policy |
| **Artifact System** | Task outputs: plans, diffs, reports, logs | Auto-generated per task |

### 1.2 Configuration Asset Taxonomy

| Asset | Scope | Activation | Purpose | Format |
| :------ | :---- | :--------- | :------- | :------ |
| **Personas** | Implicit/Defined | System instruction | Behavioral identity | Markdown in Rules/AGENTS.md |
| **Rules** | Global / Workspace | Always-on or triggered | Immutable behavioral constraints | `.md` with optional frontmatter |
| **Workflows** | Global / Workspace | `/command` trigger | Reusable prompt macros | `.md` with YAML frontmatter |
| **Skills** | Global / Workspace | Intent-matched (progressive) | On-demand capability extension | Directory (`SKILL.md`) or `.yaml` |
| **MCP Tools** | Global / Workspace | Always-available | Deterministic function execution | `mcp_config.json` / `.mcp.json` |
| **Knowledge** | Workspace | `@`-mention or rule-loaded | Domain-specific static context | Markdown / YAML / text |

### 1.3 Scope Hierarchy & File Layout

```plaintext
Global Scope (~/.gemini/)
├── GEMINI.md                                # Global Rules + Persona
└── antigravity/
    ├── mcp_config.json                      # Global MCP Tool registry
    ├── security_config.json                 # Terminal + browser policies
    ├── browserAllowlist.txt                 # Trusted domains
    ├── terminalAllowlist.txt                # Allowed commands (Off/Request Review mode)
    ├── terminalDenylist.txt                 # Blocked commands (always enforced)
    ├── global_workflows/
    │   └── *.md                             # Cross-project Workflows
    └── skills/
        └── <skill-name>/
            ├── SKILL.md                     # Skill definition
            ├── scripts/                     # Executable automation
            ├── resources/                   # Static reference assets (v1.16.5)
            └── examples/                    # Few-shot learning examples

Workspace Scope (<workspace>/)
├── AGENTS.md                                # Workspace Persona
├── .mcp.json                                # Workspace MCP config (v1.16.5)
├── .context/                                # Knowledge base
│   ├── architecture.md
│   ├── api-contracts.yaml
│   └── domain-glossary.md
└── .agent/
    ├── rules/           *.md                # Workspace Rules
    ├── workflows/       *.md                # Workspace Workflows
    ├── skills/
    │   └── <skill-name>/                    # Directory-pattern Skill
    │       ├── SKILL.md
    │       ├── scripts/
    │       ├── resources/
    │       └── examples/
    └── execution-log.jsonl                  # Agent decision log
```

**Precedence**: Workspace always overrides Global within the same asset type.

---

## 2. Execution Policies

All three axes are configured independently via **Settings → Agent Manager → Execution Policies** or the initial setup wizard.

### 2.1 Terminal Execution Policy

| Mode | Behavior | Risk |
| :---- | :-------- | :---- |
| **Off** (Allowlist-only) | Executes only commands in `terminalAllowlist.txt`; blocks all others | Lowest |
| **Auto** | Agent's internal risk model decides execution vs. review prompts | Moderate |
| **Turbo** | Executes all commands except `terminalDenylist.txt` | Highest |

**Security config** (`~/.gemini/antigravity/security_config.json`):

```json
{
  "terminal_policy": "auto",
  "allowlist": ["ls", "cat", "grep", "git status", "git log", "npm test", "pytest"],
  "denylist": ["rm -rf", "DROP DATABASE", "DELETE FROM", "sudo rm", "mkfs", "dd if="],
  "require_confirmation_for": ["git push", "git reset --hard", "docker rm", "kubectl delete"]
}
```

> `require_confirmation_for` enforces a mandatory user prompt for high-impact commands regardless of the active Terminal Policy mode.

### 2.2 Review Policy

| Mode | Behavior |
| :---- | :-------- |
| **Always Proceed** | Never requests a review checkpoint |
| **Agent Decides** *(recommended)* | Agent determines when to checkpoint based on task risk and complexity |
| **Request Review** | Always pauses for explicit user approval before proceeding |

### 2.3 JavaScript Execution Policy

| Mode | Behavior | Exposure |
| :---- | :-------- | :-------- |
| **Disabled** | No JavaScript execution in browser | None |
| **Request Review** | Prompts before each JS execution | Low |
| **Always Proceed** | Unrestricted; maximum autonomy | Highest |

### 2.4 Preset Profiles

| Profile | Terminal | Review | JavaScript | Use Case |
| :-------- | :-------- | :------ | :---------- | :-------- |
| **Strict Mode** *(formerly "Secure Mode")* | Off | Request Review | Disabled | Regulated / production-adjacent work |
| **Review-Driven** *(recommended)* | Auto | Agent Decides | Request Review | Most development scenarios |
| **Agent-Driven** | Turbo | Always Proceed | Always Proceed | Fully sandboxed environments only |
| **Custom** | User-defined | User-defined | User-defined | Specialized requirements |

### 2.5 Agent Execution Modes

Selected per conversation via the **Planning / Fast** dropdown in Agent Manager (`Cmd+L`).

| Mode | Behavior | Use When |
| :---- | :-------- | :-------- |
| **Planning** *(default)* | Organizes work into task groups; produces intermediate Artifacts before executing | Complex features, refactors, multi-agent work |
| **Fast** | Executes directly without a planning phase | Simple tasks: renaming, small bash commands, localized fixes |

---

## 3. Personas: Behavioral Identity Layer

Personas are not standalone files — they are expressed through Rules, `AGENTS.md`, and Workflow preambles.

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

You are an expert in n8n automation using n8n-MCP tools.

## Execution Protocol
1. **Silent execution**: No commentary between tool calls
2. **Parallel by default**: Execute independent operations simultaneously
3. **Templates first**: Check template library before building from scratch
4. **Multi-level validation**: Quick check → Full validation → Workflow validation
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
Scan for hardcoded credentials; validate input handling; audit auth flows.
Output: security findings artifact.

## Phase 2: Performance (Persona: Performance Engineer)
Identify N+1 queries; review caching; check algorithmic complexity.
Output: performance recommendations artifact.

## Phase 3: Maintainability (Persona: Senior Developer)
Assess code clarity; verify test coverage; check documentation completeness.

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
| **Precedence** | Workspace rules override global rules |
| **Immutability** | Workflows and skills cannot override rules |

### 4.2 Rule Activation Methods

Declared in YAML frontmatter at the top of each rule file.

| Method | Frontmatter | Behavior |
| :------ | :---------- | :-------- |
| **Always On** | `activation: always_on` | Injected into every agent context automatically |
| **Manual** | `activation: manual` | Loaded only when explicitly `@mentioned` in chat |
| **Model Decision** | `activation: model_decision` | Agent self-loads when it determines the rule is relevant |
| **Glob** | `activation: always_on` + `glob: ["*.py"]` | Activates automatically when matched files are in context |

### 4.3 Rule Implementation

#### Global Rules (`~/.gemini/GEMINI.md`)

```markdown
---
activation: always_on
---

# Global Development Standards

## Code Quality
* All Python code must follow PEP 8
* Always use Numpy-style docstrings
* Each new feature goes in its own file

## Security
* Never generate hardcoded API keys or secrets
* Always use environment variables for credentials
* Validate all user inputs; use parameterized DB queries only

## Testing
* Minimum 80% test coverage for new code
* Write tests before implementation (TDD)
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
- All function signatures must include type hints
- Use `from __future__ import annotations` for forward references
- Prefer `list[str]` over `List[str]` (Python 3.9+)

## Error Handling
- Never use bare `except:` clauses
- Always log exceptions with full context
- Use custom exception classes for business logic errors
```

#### On-Demand Security Rule

```markdown
---
activation: manual
---

# Extended Security Audit Standards

## OWASP Compliance
- Apply all OWASP Top 10 mitigations
- Enforce CSP headers on all HTTP responses
- Require MFA for all admin operations

## Usage
@security-audit-rules
```

---

## 5. Workflows: On-Demand Prompt Macros

### 5.1 Characteristics

| Property | Value |
| :-------- | :---- |
| **Activation** | `/command` trigger typed in Agent Manager |
| **Scope** | Global (`~/.gemini/antigravity/global_workflows/`) or Workspace (`.agent/workflows/`) |
| **Format** | Markdown with required YAML frontmatter (`name:`, `trigger:`, `description:`) |

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
For each module:
- Analyze public functions and classes
- Generate `tests/test_<module>.py`
- Include: happy path, edge cases, error conditions
- Naming convention: `test_<function>_<scenario>`

## Validation
- Run `pytest --collect-only` to verify syntax
- Generate artifact: `test_coverage_summary.md`

## Quality Requirements
- Minimum 3 test cases per function; use fixtures for shared setup
- Mock all external dependencies (APIs, DB queries)
```

### 5.3 Workflow → Skill Composition

```markdown
---
name: Full Stack Deploy
trigger: /deploy
description: End-to-end deployment pipeline composing multiple skills
---

## Phase 1: Quality (Skill: `code-quality-check`)
Run linters, test suite, and generate coverage report.

## Phase 2: Build (Skill: `docker-build`)
Build images, tag with commit SHA, push to registry.

## Phase 3: Infrastructure (Skill: `terraform-apply`)
Validate and apply Terraform plan.

## Phase 4: Deploy (Skill: `kubernetes-deploy`)
Update manifests, apply deployment, monitor rollout.

## Phase 5: Verify (Skill: `smoke-test`)
Execute smoke tests, verify health endpoints, generate deployment artifact.
```

---

## 6. Skills: Progressive Capability Extension

### 6.1 Architecture Principle

Skills solve **context saturation**. Capabilities load only when the agent matches user intent to a skill's `description` — unmatched skills consume zero context tokens.

```plaintext
User Request
    │
    ▼
Skill Discovery
  Match intent → frontmatter description (metadata only; no content loaded)
    │
    ▼
Skill Loading (Progressive Disclosure)
  Load SKILL.md; access scripts/resources/examples on-demand
    │
    ▼
Skill Execution → Artifacts
```

### 6.2 Skill Formats

| Format | Best For | Location |
| :------ | :-------- | :-------- |
| **Directory + SKILL.md** | Multi-file skills with scripts, examples, resources | `.agent/skills/<name>/` |
| **Lightweight YAML** | Script-free skills; minimal context footprint | `.agent/skills/<name>.yaml` |

#### Directory-Based Skill Structure

```plaintext
<skill-name>/
├── SKILL.md           # Required: definition + instructions
├── scripts/           # Optional: executable automation
├── resources/         # Optional: static reference assets (v1.16.5)
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

### 6.3 SKILL.md Specification (v1.16.5)

The `description` frontmatter field is the primary intent-matching signal — write it as an action-oriented phrase describing exactly what the skill does.

```markdown
---
name: git-commit-formatter
description: Enforces Conventional Commits specification for all git commit messages.
---

# Skill: Git Commit Formatter

## Trigger Patterns
- User writes or requests a commit message
- Workflow includes a commit step

## Instructions

### Commit Type Detection
| Keyword | Type |
| :------- | :---- |
| "fix", "bug" | `fix:` |
| "feature", "add" | `feat:` |
| "docs", "documentation" | `docs:` |
| "refactor" | `refactor:` |
| "test" | `test:` |
| "chore", "build" | `chore:` |

### Message Format
`<type>(<scope>): <subject>`
Subject: lowercase, imperative mood, ≤ 50 chars, no trailing period.

### Examples
| Input | Output |
| :---- | :----- |
| "fixed login bug" | `fix(auth): resolve login validation error` |
| "Added API endpoint" | `feat(api): add user profile endpoint` |
| "updated docs" | `docs: update API documentation` |

## Deliverables
- Artifact: `formatted_commit.txt`
- Prompt user for approval before executing `git commit`
```

### 6.4 Skill Patterns Reference

| Pattern | Structure | Use Case |
| :------- | :-------- | :-------- |
| **Basic Router** | `SKILL.md` only | Simple instruction sets; no external assets |
| **Resource** | `SKILL.md` + `/resources` | Large static docs fetched on-demand, not preloaded |
| **Few-Shot** | `SKILL.md` + `/examples` | Complex transformations taught via I/O pairs |
| **Script Delegation** | `SKILL.md` + `/scripts` | Deterministic operations delegated to scripts |

**Script Delegation example**:

```markdown
---
name: database-migration
description: Executes versioned database migrations with automatic rollback on failure.
---

# Skill: Database Migration

## Instructions
1. Detect target environment (dev / staging / prod)
2. Default to dry-run: `python scripts/migrate.py --env <env> --dry-run`
3. Present output; request explicit confirmation before live run
4. On non-zero exit: `bash scripts/rollback.sh --env <env>`
5. Generate artifact: `migration_log.md`

## Safety
- **Production**: `--dry-run` is mandatory; remove only on explicit user confirmation
- **Staging**: Require approval for schema-altering operations
- **Dev**: Full permissions
```

### 6.5 Skills vs. MCP Tools

| Factor | Skill | MCP Tool |
| :------ | :---- | :-------- |
| Architecture | File-based; ephemeral | Client-server; persistent process |
| Overhead | Low | Higher |
| Context loading | Progressive; on-demand | Always injected |
| State | Stateless | Stateful |
| Best for | Multi-step procedures, code generation, analysis | External APIs, databases, Slack, GitHub |

---

## 7. MCP Tools: Deterministic Function Layer

### 7.1 Architecture

MCP tools are always available once configured — no progressive loading. The agent calls them directly during execution.

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
    },
    "custom-tool": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-server/index.js"],
      "env": {
        "API_KEY": "${CUSTOM_API_KEY}",
        "LOG_LEVEL": "error"
      }
    }
  }
}
```

### 7.3 Workspace MCP Configuration (v1.16.5 — `<workspace>/.mcp.json`)

For project-specific integrations. Use `${env:VAR}` substitution — **never commit secrets**.

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

### 7.4 MCP Router Pattern (Multi-Backend)

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

Routes all calls through a single router to minimize context pollution. Backend tools load on-demand.

---

## 8. Knowledge: Domain-Specific Context

### 8.1 Structure

```plaintext
<workspace>/.context/
├── architecture.md          # System design
├── api-contracts.yaml       # API specifications
├── deployment-guide.md      # Operations procedures
└── domain-glossary.md       # Business terminology
```

### 8.2 Injection Methods

| Method | Syntax | When to Use |
| :------ | :------ | :----------- |
| **Direct `@`-mention** | `@.context/architecture.md` | On-demand; explicit in prompt |
| **Skill-embedded** | Directive in SKILL.md instructions | Knowledge always needed by a specific skill |
| **Rule-based auto-load** | Directive in `GEMINI.md` | Contextually relevant every session |
| **Resource-bundled** | Files in skill's `resources/` | Knowledge scoped to one skill only |

**Rule-based auto-load** (`~/.gemini/GEMINI.md`):

```markdown
## Knowledge Context Protocol
- Check for `.context/` directory in the workspace root
- Load `architecture.md` for system design questions
- Load `domain-glossary.md` for business terminology questions
- Always cite source file when referencing knowledge base content
```

---

## 9. Configuration Precedence

### 9.1 Hierarchy

```plaintext
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

### 9.2 Conflict Resolution

| Scenario | Resolution |
| :-------- | :--------- |
| Workspace Rule ≠ Global Rule | Workspace rule wins |
| Workflow invokes restricted operation | Rule blocks execution — rules are immutable |
| Multiple skills match same intent | Agent scores by frontmatter `description` relevance |
| MCP Tool vs. Skill approach conflict | Skill provides methodology; tool provides execution |

### 9.3 Full Activation Flow

```plaintext
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
4. Apply Persona (GEMINI.md / AGENTS.md)
    │
    ▼
5. Check for /workflow trigger
    ├── Match  → Execute workflow → compose skills → call tools
    └── No match → Skill Discovery (intent → description match)
    │
    ▼
6. Inject always-available MCP Tools
    │
    ▼
7. Execute with all constraints enforced
   → Generate Artifacts → Optionally request review
```

---

## 10. Advanced Patterns

### 10.1 Multi-Agent Orchestration

```markdown
---
name: Microservices Refactor
trigger: /refactor-services
description: Spawns parallel agents per service with sync checkpoints
---

## Agent Allocation
- **Agent A** (Workspace: `service-auth`): Refactor authentication
- **Agent B** (Workspace: `service-payment`): Refactor payments
- **Agent C** (Workspace: `service-notification`): Refactor notifications

## Synchronization Points
1. All agents complete API contract definition
2. Merge contracts → `shared-contracts.yaml`
3. All agents implement against merged contracts
4. Orchestrator runs end-to-end test suite
```

### 10.2 Conditional Skill Routing

```markdown
---
name: dynamic-db-connector
description: Routes database connections to the skill matching the current environment.
---

# Skill: Dynamic Database Connector

## Instructions
1. Read `APP_ENV` environment variable
2. Route:
   - `dev` → load `postgres-dev-skill` (full permissions)
   - `staging` → load `postgres-staging-skill` (approval required for schema changes)
   - `prod` → load `postgres-prod-skill` (read-only queries enforced)
```

### 10.3 Self-Improving Knowledge Base

```markdown
---
name: self-improvement-logger
description: Logs agent decisions and outcomes; generates rule proposals from patterns.
---

# Skill: Self-Improvement Logger

## Execution Logging
After every significant decision, append to `.agent/execution-log.jsonl`:

```json
{
  "timestamp": "2026-02-15T10:30:00Z",
  "user_intent": "Deploy to production",
  "approach": "Blue-green deployment via kubernetes-deploy skill",
  "outcome": "SUCCESS",
  "duration_seconds": 180
}
```

## Monthly Review

1. Analyze log for recurring failure patterns
2. Generate `suggested-rules.md`
3. Prompt user for review before applying any proposals

---

## 11. Security & Guardrails

### 11.1 Browser Security

```plaintext
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
- Prompt user before accessing any unlisted domain
- Never auto-submit forms on external sites
- Always request permission before downloading files
```

### 11.2 Secrets Management

- Use `${ENV_VAR}` / `${env:VAR}` substitution in all JSON configs — never hardcode credentials
- Store project secrets in Antigravity's encrypted credential store
- Add `.mcp.json` and `mcp_secrets.json` to `.gitignore`

### 11.3 Version Control

```gitignore
# Runtime state — never commit
.gemini/logs/
.agent/state/
artifacts/tmp/
mcp_secrets.json

# Commit these (team-shared):
# .agent/rules/
# .agent/workflows/
# .agent/skills/
# AGENTS.md
# .context/
# .mcp.json  (with ${env:VAR} substitution — no raw secrets)
```

---

## 12. Testing & Validation

### 12.1 CLI Reference (`agy`)

```bash
agy /test-workflow                             # Trigger a workflow
agy /deploy --dry-run                          # Dry-run a deployment workflow
agy --mcp-status                              # Verify MCP connections
agy --list-skills                             # List all discoverable skills
agy --validate-workflow .agent/workflows/release.md
tail -f ~/.gemini/logs/agent.log              # Stream agent logs
```

### 12.2 CI Workflow Validation

```yaml
# .github/workflows/validate-antigravity.yml
name: Validate Antigravity Configuration
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install CLI
        run: npm install -g @google/antigravity
      - name: Validate Workflows
        run: |
          for wf in .agent/workflows/*.md; do
            agy --validate-workflow "$wf"
          done
      - name: Smoke-check Skills
        run: agy --list-skills
```

### 12.3 Skill Test Template

```markdown
# Skill Test: <Skill Name>

## Test Case 1: Basic Functionality
**Input**: [Sample input]  **Expected**: [Expected result]  **Validation**: [How to verify]

## Test Case 2: Edge Case
**Input**: [Edge case data]  **Expected**: [Expected handling]  **Validation**: [Steps]

## Test Case 3: Error Handling
**Input**: [Invalid data]  **Expected**: [Graceful failure / error message]  **Validation**: [Steps]
```

---

## 13. Troubleshooting

| Problem | Diagnosis | Solution |
| :------- | :-------- | :-------- |
| Workflow not triggering | Incorrect trigger syntax | Ensure `trigger: /exact-command` in frontmatter |
| Skill not loading | Description too vague | Use action-oriented language in frontmatter `description:` |
| Skill over-activating | Description too broad | Narrow description; switch to `activation: manual` |
| MCP tool unavailable | Server failed to start | Check JSON syntax; verify env vars; run `agy --mcp-status` |
| Rule being ignored | Precedence conflict | Verify workspace rule location; check `activation:` field |
| Context overflow | Too many skills activating | Tighten `description:` fields; switch broad skills to `manual` |
| `agy` not found | Old `gemini` CLI in PATH | `npm install -g @google/antigravity` |
| `.mcp.json` not recognized | Pre-v1.16.5 installation | Update to v1.16.5+; confirm file is in workspace root |

**Inspect active context**:

```plaintext
"Debug: List all currently loaded rules, active skills, and available MCP tools."
```

**Isolate a skill for testing**:

```bash
mkdir /tmp/skill-test && cd /tmp/skill-test
mkdir -p .agent/skills
cp -r ~/.gemini/antigravity/skills/my-skill .agent/skills/
agy "Test my-skill with sample input"
```

---

## 14. Reference Summary

### 14.1 Asset Interaction Matrix

| From → To | Personas | Rules | Workflows | Skills | MCP Tools | Knowledge |
| :--------- | :------- | :---- | :-------- | :----- | :-------- | :-------- |
| **Personas** | N/A | Embedded in Rules | Define phase personas | Guides execution style | N/A | Shapes interpretation |
| **Rules** | Defines global persona | Can cross-reference | **CONSTRAINS** | **CONSTRAINS** | Restricts tool usage | N/A |
| **Workflows** | Invokes per-phase personas | **OBEYS** | Can chain | **COMPOSES** | Orchestrates calls | References files |
| **Skills** | Adopts execution persona | **OBEYS** | Invoked by | Can depend on others | Calls for execution | Bundles in `resources/` |
| **MCP Tools** | N/A | **OBEYS** | Called by | Called by | Can compose others | N/A |
| **Knowledge** | Informs persona | N/A | Provides context | Provides reference | N/A | Can cross-reference |

### 14.2 When to Use Each Asset

| Use Case | Asset | Rationale |
| :-------- | :---- | :--------- |
| Define coding standards | **Rule** (`always_on`) | Enforced in every context |
| Language/file-specific standards | **Rule** with `glob:` | Activates only on matched files |
| Reusable multi-step prompt | **Workflow** | Triggered on demand via `/command` |
| On-demand domain capability | **Skill** | Progressive; loads only when intent matches |
| External API / DB integration | **MCP Tool** | Deterministic; always available |
| Behavioral identity | **Persona** (in Rules/AGENTS.md) | Persistent across all interactions |
| Static reference material | **Knowledge** (`.context/`) | Injected via `@`-mention or rule |

### 14.3 File Locations Cheat Sheet

```
~/.gemini/GEMINI.md                              Global Rules + Persona
~/.gemini/antigravity/mcp_config.json            Global MCP registry
~/.gemini/antigravity/security_config.json       Terminal + browser policies
~/.gemini/antigravity/browserAllowlist.txt       Browser domain allowlist
~/.gemini/antigravity/terminalDenylist.txt       Always-enforced command denylist
~/.gemini/antigravity/terminalAllowlist.txt      Command allowlist (Off mode)
~/.gemini/antigravity/global_workflows/          Global Workflows
~/.gemini/antigravity/skills/                    Global Skills

<workspace>/AGENTS.md                           Workspace Persona
<workspace>/.mcp.json                           Workspace MCP config (v1.16.5)
<workspace>/.context/                           Knowledge base
<workspace>/.agent/rules/                       Workspace Rules
<workspace>/.agent/workflows/                   Workspace Workflows
<workspace>/.agent/skills/                      Workspace Skills
<workspace>/.agent/execution-log.jsonl          Agent decision log
```

### 14.4 Syntax Quick Reference

**Rule frontmatter**:

```markdown
---
activation: always_on | manual | model_decision
glob: ["*.py", "src/**/*.ts"]   # optional; implies always_on
---
```

**Workflow frontmatter** (all three fields required):

```markdown
---
name: Display Name
trigger: /command
description: One-line summary
---
```

**SKILL.md frontmatter** (required for intent-matching):

```markdown
---
name: skill-kebab-name
description: Action-oriented, intent-rich phrase for discovery accuracy
---
```

**MCP entry**:

```json
"serverName": {
  "command": "executable",
  "args": ["arg1"],
  "env": {"KEY": "${ENV_VAR}"}
}
```

---

## 15. Keyboard Shortcuts

| Shortcut | Action |
| :-------- | :------ |
| `Cmd + E` | Open Agent Manager panel |
| `Cmd + L` | Open Agent Manager chat / toggle Planning ⇄ Fast mode |
| `Shift + Cmd + L` | Start new Agent conversation |
| `Cmd + I` | Open inline agent chat in Editor |
| `Cmd + ,` | Open Settings |
| `` Ctrl + ` `` | Toggle terminal panel |
| `Tab` | Accept code completion |
| `Escape` | Cancel active agent operation |
| `Cmd + Enter` | Approve pending agent action |
| `Cmd + Backspace` | Reject pending agent action |

---

## 16. Version History

| Version | Release | Key Changes |
| :------- | :------ | :---------- |
| **1.16.5** | 2025-12-22 | Strict Mode rename; `.mcp.json` workspace support; rule `activation:`/`glob:` frontmatter; `resources/` canonical dir; `agy` CLI |
| 1.15.8 | 2025-11 | Multi-model support; Planning/Fast modes formalized |
| 1.14.2 | 2025-10 | Skills framework introduction; initial SKILL.md spec |
| 1.13.3 | 2025-09 | Browser subagent improvements; initial MCP integration |

**Update cadence**: Auto-updates 3× weekly (Mon/Wed/Fri, 09:00 UTC).

---

## Appendix A: Migration from Traditional IDEs

| Traditional Feature | Antigravity Equivalent |
| :------------------ | :--------------------- |
| Code snippets | Workflows (`/trigger`) |
| Linter configurations | Rules with `glob:` frontmatter |
| IDE plugins | Skills (progressive loading) |
| External tools (git, docker) | MCP Tools |
| Workspace settings | `.agent/` directory |
| Project documentation | `.context/` knowledge base |
| Code templates | Skill `examples/` directory |

**Migration checklist**:

1. Convert linter configs → Rules with `glob:` frontmatter
2. Export code snippets → Workflows with `/trigger`
3. Identify external integrations → Configure MCP servers
4. Document domain knowledge → Populate `.context/`
5. Define team standards → Author `AGENTS.md`

## Appendix B: Reference Links

- **Official Docs**: [antigravity.google/docs](https://antigravity.google/docs)
- **Download**: [antigravity.google/download](https://antigravity.google/download)
- **Getting Started Codelab**: [codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **AI Studio**: [aistudio.google.com](https://aistudio.google.com)
