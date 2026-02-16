# Google Antigravity v1.16.5: Agent Configuration Technical Reference

> **Document Version**: 2.0.0 | **Last Updated**: 2026-02-15 | **Target Platform**: Google Antigravity IDE v1.16.5+

---

## Executive Summary

Google Antigravity implements an **agent-first development platform** where configuration assets (Personas, Rules, Tools, Workflows, Skills, Knowledge) operate through a hierarchical, progressive disclosure architecture. This document provides implementation standards for configuring agent relationships and asset interactions, updated and verified against the v1.16.5 release.

**What's changed in v1.16.5:**

- "Secure Mode" renamed to **Strict Mode**
- `@`-mention search speed improvements
- Skill `SKILL.md` now supports a YAML frontmatter block (`name:`, `description:`)
- Skill static assets directory canonically renamed from `references/` → `resources/`
- CLI entrypoint updated: `gemini` → `agy`
- Agent execution modes clarified: **Planning** and **Fast**
- Three independent execution policy axes: Terminal, Review, and JavaScript

---

## 1. Core Configuration Asset Types

### 1.1 Asset Taxonomy

| Asset Type | Scope | Activation | Purpose | Format |
| :----------- | :------ | :----------- | :-------- | :------- |
| **Personas** | Implicit/Defined | System instruction | Define agent behavioral identity | Markdown (system_instruction) |
| **Rules** | Global/Workspace | Always-on | Passive behavioral constraints | Markdown (`.md`) |
| **Workflows** | Global/Workspace | User-triggered | On-demand prompt templates | Markdown (`.md`) |
| **Skills** | Global/Workspace | Context-matched | Progressive capability extension | Directory (`SKILL.md` + assets) |
| **Tools (MCP)** | Global | Always-available | Deterministic function execution | JSON config + MCP server |
| **Knowledge** | Workspace | Reference-based | Domain-specific context | Markdown/text files |

### 1.2 Scope Hierarchy

```plaintext
Global Scope (~/.gemini/)
├── GEMINI.md                           # Global Rules (system instructions)
├── antigravity/
│   ├── mcp_config.json                 # MCP Tool configuration
│   ├── global_workflows/               # Global Workflows
│   │   └── *.md
│   ├── skills/                         # Global Skills
│   │   └── skill-name/
│   │       ├── SKILL.md
│   │       ├── scripts/
│   │       ├── resources/              # Static assets (v1.16.5: was 'references/')
│   │       └── examples/
│   ├── browserAllowlist.txt            # Browser domain allowlist
│   └── terminalDenylist.txt            # Command denylist

Workspace Scope (<workspace>/)
├── .agent/
│   ├── rules/                          # Workspace Rules
│   │   └── *.md
│   ├── workflows/                      # Workspace Workflows
│   │   └── *.md
│   └── skills/                         # Workspace Skills
│       └── skill-name/
│           ├── SKILL.md
│           ├── scripts/
│           ├── resources/
│           └── examples/
├── AGENTS.md                           # Workspace-specific persona/rules
└── .context/                           # Knowledge base (project-specific)
```

> **Note**: The global config `terminalAllowlist.txt` is honored only when the Terminal Execution Policy is set to **Request Review**. The `terminalDenylist.txt` is always enforced.

---

## 2. Execution Policies (v1.16.5)

Before configuring assets, understand the three independent policy axes that govern agent autonomy. These are set via **Settings → Agent Manager** or during the initial setup wizard.

### 2.1 Terminal Execution Policy

Controls whether the agent may run shell commands autonomously.

| Mode | Behavior | Recommended For |
| :---- | :-------- | :--------------- |
| **Always Proceed** | Executes all commands without approval (except denylist) | Greenfield projects, trusted sandboxes |
| **Request Review** | Prompts the user before every terminal command | Production systems, critical infrastructure |

### 2.2 Review Policy

Controls when the agent pauses for human review of its generated Artifacts (plans, diffs, reports).

| Mode | Behavior |
| :---- | :-------- |
| **Always Proceed** | Agent never requests a review checkpoint |
| **Agent Decides** | Agent autonomously determines when to checkpoint *(recommended)* |
| **Request Review** | Agent always pauses and requires explicit user approval before proceeding |

### 2.3 JavaScript Execution Policy

Controls browser subagent behavior when interacting with web pages.

| Mode | Behavior |
| :---- | :-------- |
| **Always Proceed** | Agent executes JavaScript in the browser without pausing. Maximum autonomy; highest security exposure. |
| **Request Review** | Agent prompts before executing any JavaScript. |
| **Disabled** | Agent will never execute JavaScript in the browser. |

### 2.4 Preset Profiles

For convenience, the following named profiles map to combinations of the above three policies.

| Profile | Terminal | Review | JavaScript | Notes |
| :-------- | :-------- | :------ | :---------- | :----- |
| **Strict Mode** *(renamed from "Secure Mode" in v1.16.5)* | Request Review | Request Review | Disabled | Maximum safety; enforces human review for all agent actions |
| **Review-Driven Development** *(recommended)* | Agent Decides | Agent Decides | Request Review | Balanced autonomy; suitable for most development |
| **Agent-Driven Development** | Always Proceed | Always Proceed | Always Proceed | Full autonomy; use only in fully sandboxed environments |
| **Custom** | User-defined | User-defined | User-defined | Granular control |

> **Security Notice**: Strict Mode is the only profile that prevents the agent from autonomously running targeted exploits. It is strongly recommended for production-adjacent work and regulated environments.

---

## 3. Personas: Behavioral Identity Layer

### 3.1 Definition

Personas define **agent behavioral identity** through system instructions. Antigravity does not expose explicit Persona files; personas are implemented through:

1. **Rules** — persistent, always-on persona definitions
2. **`AGENTS.md`** — workspace-level identity and execution protocol
3. **Workflow preambles** — task-specific persona switching

### 3.2 Implementation Patterns

#### Pattern A: Global Persona via Rules

**Location**: `~/.gemini/GEMINI.md`

```markdown
# Global Persona Definition

You are a Senior Software Architect specializing in distributed systems.

## Core Principles
- Prioritize system resilience over raw performance
- Design for failure scenarios first
- Question assumptions before implementing

## Behavioral Constraints
- Never auto-execute destructive operations (DROP, DELETE, rm -rf)
- Always propose architectural diagrams for complex changes
- Require explicit approval for production deployments
```

#### Pattern B: Workspace-Specific Persona

**Location**: `<workspace>/AGENTS.md`

```markdown
# Project-Specific Agent Persona

You are an expert in n8n automation software using n8n-MCP tools.

## Execution Protocol
1. **Silent execution**: No commentary between tool calls
2. **Parallel by default**: Execute independent operations simultaneously
3. **Templates first**: Always check template library before building
4. **Multi-level validation**: Quick check → Full validation → Workflow validation

## Domain Expertise
- Workflow orchestration patterns
- n8n node configuration
- Error handling strategies
```

**Auto-load instruction** — add to `~/.gemini/GEMINI.md`:

```markdown
## Workspace Persona Loading
- Check for AGENTS.md in the project workspace root
- Load all instructions from AGENTS.md as system-level constraints
- Recursively check sub-folders for AGENTS.md with section-specific instructions
```

#### Pattern C: Workflow-Embedded Persona

**Location**: `<workspace>/.agent/workflows/architecture-review.md`

```markdown
---
name: Architecture Review
trigger: /architecture-review
description: Critique system topology for resilience gaps
---

# Architecture Review Workflow

**Persona**: You are The Architect — a principal engineer focused on system design critique.

**Execution Steps**:
1. Analyze current system topology
2. Identify single points of failure
3. Propose resilience improvements
4. Generate architecture diagram artifact
```

### 3.3 Persona → Workflow Binding

Workflows can invoke **phase-specific personas**:

```markdown
---
name: Code Review
trigger: /review
description: Multi-phase code review with specialist personas
---

# Code Review Workflow

**Phase 1: Security Analysis** (Persona: Security Auditor)
- Scan for hardcoded credentials
- Check input validation
- Verify authentication flows

**Phase 2: Performance Analysis** (Persona: Performance Engineer)
- Identify N+1 queries
- Check algorithmic complexity
- Review caching strategies

**Phase 3: Maintainability Analysis** (Persona: Senior Developer)
- Assess code clarity
- Check test coverage
- Verify documentation
```

---

## 4. Rules: Passive Behavioral Constraints

### 4.1 Characteristics

| Property | Value |
| :--------- | :------ |
| **Activation** | Always-on; loaded into every agent context |
| **Scope** | Global (`~/.gemini/GEMINI.md`) or Workspace (`<workspace>/.agent/rules/*.md`) |
| **Precedence** | Workspace rules override global rules |
| **Analogy** | System constitution; immutable guardrails |

### 4.2 Implementation Standards

#### Global Rules (`~/.gemini/GEMINI.md`)

```markdown
# Global Development Standards

## Code Quality
* All code must follow PEP 8 (Python) / ESLint (JavaScript)
* Each new feature goes in its own file
* Include example methods for demonstration
* Always use Numpy-style docstrings for Python

## Security
* Never generate hardcoded API keys
* Always use environment variables for secrets
* Validate all user inputs
* Sanitize database queries (parameterized statements only)

## Documentation
* Every public function requires a docstring
* Complex algorithms need inline comments
* Update README.md when adding new features

## Testing
* Minimum 80% test coverage for new code
* Write tests before implementation (TDD)
* Include edge case tests
```

#### Workspace Rules (`<workspace>/.agent/rules/python-standards.md`)

```markdown
# Python-Specific Rules

## Type Hints
- All function signatures must include type hints
- Use `from __future__ import annotations` for forward references
- Prefer `list[str]` over `List[str]` (Python 3.9+)

## Error Handling
- Never use bare `except:` clauses
- Always log exceptions with context
- Use custom exception classes for business logic errors

## Project Structure
```

```plaintext
project/
├── src/
│   ├── __init__.py
│   ├── core/           # Business logic
│   ├── api/            # External interfaces
│   └── utils/          # Helpers
├── tests/
└── docs/
```

### 4.3 Rules → Workflow Interaction

Rules **constrain** workflow execution. Workflows **cannot override** rules.

```markdown
# Global Rule
* Never deploy to production without approval

# Workflow: Deploy
---
name: Deploy to Production
trigger: /deploy-prod
---

**Pre-execution Check**: Verify deployment approval exists in JIRA
**Blocker**: If no approval found, halt and prompt user
**Execution**: Proceeds only if rule constraint is satisfied
```

---

## 5. Workflows: On-Demand Prompt Templates

### 5.1 Characteristics

| Property | Value |
| :--------- | :------ |
| **Activation** | User-triggered via `/workflow-name` |
| **Scope** | Global (`~/.gemini/antigravity/global_workflows/`) or Workspace (`<workspace>/.agent/workflows/`) |
| **Analogy** | Saved prompts / Task macros |

### 5.2 Workflow File Structure

```markdown
---
name: Generate Unit Tests
trigger: /generate-unit-tests
description: Creates comprehensive unit tests for all Python modules
---

# Generate Unit Tests Workflow

## Execution Protocol

1. **Discovery Phase**
   - Scan `src/` directory for all `.py` files
   - Exclude `__init__.py` and test files
   - Generate file list artifact

2. **Test Generation Phase**
   For each discovered module:
   - Analyze public functions and classes
   - Generate pytest test file in `tests/test_<module>.py`
   - Include: happy path, edge cases, error conditions
   - Naming convention: `test_<function>_<scenario>`

3. **Validation Phase**
   - Run `pytest --collect-only` to verify syntax
   - Generate coverage report
   - Create artifact: `test_coverage_summary.md`

## Quality Requirements
- Minimum 3 test cases per function
- Use fixtures for common setup
- Mock external dependencies (API calls, DB queries)
- Include docstrings in test functions

## Deliverables
- Test files: `tests/test_*.py`
- Artifact: Test coverage summary
- Artifact: Test execution log
```

### 5.3 Workflow → Skill Composition

Workflows can compose **multiple skills** into a pipeline:

```markdown
---
name: Full Stack Deploy
trigger: /deploy
description: End-to-end deployment pipeline
---

# Full Stack Deployment Workflow

## Phase 1: Pre-deployment (Skill: `code-quality-check`)
- Run linters; execute test suite; generate coverage report

## Phase 2: Build (Skill: `docker-build`)
- Build Docker images; tag with commit SHA; push to registry

## Phase 3: Infrastructure (Skill: `terraform-apply`)
- Validate Terraform plan; apply infrastructure changes

## Phase 4: Deployment (Skill: `kubernetes-deploy`)
- Update K8s manifests; apply deployment; monitor rollout

## Phase 5: Verification (Skill: `smoke-test`)
- Execute smoke tests; verify health endpoints; generate deployment artifact
```

---

## 6. Skills: Progressive Capability Extension

### 6.1 Architecture Principle

**Skills solve context saturation.** Instead of loading all capabilities into every agent context, skills are dynamically loaded only when the agent matches user intent to a skill description.

```plaintext
Agent Request (User Prompt)
          │
          ▼
Skill Discovery (Manifest Matching)
  - Parse user intent
  - Match to skill descriptions (metadata only)
          │
          ▼
Skill Loading (Progressive Disclosure)
  - Load SKILL.md into context
  - Reference scripts/resources/examples on-demand
          │
          ▼
Skill Execution
  - Follow SKILL.md instructions
  - Execute scripts if needed
  - Generate artifacts
```

### 6.2 Skill Directory Structure

```plaintext
skill-name/
├── SKILL.md              # Required: Skill definition and instructions
├── scripts/              # Optional: Executable automation
│   ├── run.py
│   └── util.sh
├── resources/            # Optional: Static reference materials (v1.16.5)
│   ├── api-schema.json
│   └── documentation.md
├── examples/             # Optional: Few-shot learning examples
│   ├── example-1.md
│   └── example-2.md
└── assets/               # Optional: Images, templates
    └── template.yaml
```

> **v1.16.5 Change**: The static assets subdirectory is canonically `resources/` (previously `references/`). Both are functional, but `resources/` is the current convention per official documentation.

### 6.3 SKILL.md Specification (v1.16.5)

SKILL.md now supports an optional YAML frontmatter block for machine-readable metadata. The `description` field is critical — it is the primary signal used by the agent for intent-based skill discovery.

```markdown
---
name: git-commit-formatter
description: Enforces Conventional Commits specification for all git commit messages.
---

# Skill: Git Commit Formatter

## Description
Enforces Conventional Commits specification for all git commits.

## Trigger Patterns
- User writes or requests a commit message
- User invokes `git commit`
- Workflow includes a commit step

## Instructions

### Pre-commit Analysis
1. Parse the user's intended commit message
2. Identify commit type from keywords:
   - "fix", "bug" → `fix:`
   - "feature", "add" → `feat:`
   - "docs", "documentation" → `docs:`
   - "refactor" → `refactor:`
   - "test" → `test:`
   - "chore", "build" → `chore:`

### Message Construction
Format: `<type>(<scope>): <subject>`

- **type**: Commit category (required)
- **scope**: Affected component (optional)
- **subject**: Brief description (max 50 chars)

### Validation Rules
- Subject must start with lowercase
- No period at end of subject
- Subject must use imperative mood ("add" not "added")

### Example Transformations
| User Input | Formatted Output |
| :----------- | :----------------- |
| "fixed the login bug" | `fix(auth): resolve login validation error` |
| "Added new API endpoint" | `feat(api): add user profile endpoint` |
| "updated docs" | `docs: update API documentation` |

## Deliverables
- Artifact: `formatted_commit.txt` with proposed message
- Prompt user for approval before executing `git commit`
```

### 6.4 Skill Patterns

#### Pattern 1: Basic Router (SKILL.md only)

Use for simple instruction sets with no external assets.

```markdown
---
name: json-formatter
description: Formats and validates JSON documents with sorted keys and 2-space indentation.
---

# Skill: JSON Formatter

## Instructions
1. Parse input JSON
2. Validate syntax
3. Pretty-print with 2-space indentation
4. Sort keys alphabetically
5. Return formatted JSON
```

#### Pattern 2: Resource Pattern (SKILL.md + `/resources`)

Use when incorporating large static documents to avoid bloating context. The agent reads from `resources/` on-demand rather than loading everything upfront.

```plaintext
license-header-skill/
├── SKILL.md
└── resources/
    └── apache-2.0-header.txt
```

```markdown
---
name: license-header-adder
description: Adds the standard Apache 2.0 license header to new source files.
---

# Skill: Apache License Header

## Instructions
1. Check if file already starts with the license header
2. If missing, read template from `resources/apache-2.0-header.txt`
3. Insert header at file beginning
4. Preserve existing file content below the header
```

#### Pattern 3: Few-Shot Pattern (SKILL.md + `/examples`)

Use to teach complex transformations through concrete input/output pairs.

```plaintext
pydantic-generator/
├── SKILL.md
└── examples/
    ├── input-1.json
    ├── output-1.py
    ├── input-2.json
    └── output-2.py
```

```markdown
---
name: json-to-pydantic
description: Converts JSON schemas into typed Pydantic BaseModel classes.
---

# Skill: JSON to Pydantic Model

## Instructions
1. Analyze JSON structure
2. Infer field types and optionality
3. Generate Pydantic BaseModel class
4. Follow patterns demonstrated in `examples/`

## Reference Examples
- **Simple Object**: See `examples/input-1.json` → `examples/output-1.py`
- **Nested Arrays**: See `examples/input-2.json` → `examples/output-2.py`
```

#### Pattern 4: Script Delegation Pattern (SKILL.md + `/scripts`)

Use when execution should be delegated to deterministic scripts.

```plaintext
database-migration/
├── SKILL.md
└── scripts/
    ├── migrate.py
    └── rollback.sh
```

```markdown
---
name: database-migration
description: Executes versioned database migrations with automatic rollback on failure.
---

# Skill: Database Migration

## Instructions
1. Parse user's target environment (dev/staging/prod)
2. Execute: `python scripts/migrate.py --env <environment> --dry-run`
3. Present dry-run output and request user approval
4. On confirmation, re-execute without `--dry-run`
5. If exit code != 0, execute `bash scripts/rollback.sh --env <environment>`
6. Generate artifact: `migration_log.md`

## Safety Constraints
- **Production**: Always default to `--dry-run`; require explicit approval to proceed
- **Staging**: Require approval for schema changes
- **Dev**: Full permissions; dry-run optional
```

---

## 7. Tools (MCP): Deterministic Function Layer

### 7.1 MCP Architecture

MCP servers expose **deterministic tools** to agents. Tools are always available once configured — they do not use progressive loading like Skills.

```plaintext
Antigravity Agent
      │
      ▼
MCP Client (mcp_config.json)
  - Manages server connections
  - Routes tool calls
      │
  ┌───┼───┬──────┬──────┐
  ▼   ▼   ▼      ▼      ▼
GitHub Slack Notion Postgres Custom
 MCP   MCP   MCP    MCP    MCP
```

### 7.2 MCP Configuration

**Location**: `~/.gemini/antigravity/mcp_config.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "mcp/postgres",
        "postgresql://user:pass@localhost/db"
      ]
    },
    "custom-tool": {
      "command": "node",
      "args": ["/absolute/path/to/custom-mcp-server/index.js"],
      "env": {
        "API_KEY": "${CUSTOM_API_KEY}",
        "LOG_LEVEL": "error"
      }
    }
  }
}
```

### 7.3 Skills vs. MCP Tools: Design Decision Matrix

| Factor | Use Skill | Use MCP Tool |
| :------- | :---------- | :------------- |
| **Context Sensitivity** | High (load only when relevant) | Low (always available) |
| **Execution Complexity** | Multi-step procedures | Single function calls |
| **State Management** | May maintain ephemeral state | Stateless preferred |
| **Infrastructure** | File-based; no server required | Requires running MCP server |
| **Example** | "Generate release notes from commits" | "Execute SQL query" |

### 7.4 MCP Router Pattern (Advanced)

For complex tool ecosystems, implement a **single router MCP** that proxies to multiple backends to minimize context pollution:

```json
{
  "mcpServers": {
    "router": {
      "command": "npx",
      "args": ["-y", "rube-mcp"],
      "env": {
        "RUBE_BACKENDS": "github,slack,postgres,notion"
      }
    }
  }
}
```

---

## 8. Knowledge: Domain-Specific Context

### 8.1 Knowledge Base Structure

```plaintext
<workspace>/
├── .context/                    # Knowledge base directory
│   ├── architecture.md          # System architecture docs
│   ├── api-contracts.yaml       # API specifications
│   ├── deployment-guide.md      # Operations procedures
│   └── domain-glossary.md       # Business terminology
└── docs/                        # Traditional documentation
    └── README.md
```

### 8.2 Knowledge Injection Methods

#### Method 1: Direct `@`-mention in Prompt

```plaintext
"Review the authentication flow for security issues.
 Reference @.context/architecture.md for the current design."
```

> **v1.16.5**: `@`-mention search speed has been improved, making this the preferred method for on-demand context injection.

#### Method 2: Skill-Embedded Knowledge

```markdown
# Skill: Security Audit

## Instructions
1. Load system architecture from `.context/architecture.md`
2. Identify authentication/authorization components
3. Cross-reference with OWASP Top 10
4. Generate security findings artifact
```

#### Method 3: Rule-Based Auto-Loading

```markdown
# Knowledge Context Protocol (~/.gemini/GEMINI.md)

- Always check for `.context/` directory in the workspace
- Load `.context/architecture.md` for system design questions
- Load `.context/domain-glossary.md` for business term questions
- Cite source file whenever referencing knowledge base content
```

#### Method 4: Resource-Bundled Knowledge (within Skills)

```plaintext
data-validation-skill/
├── SKILL.md
└── resources/
    ├── validation-rules.json
    └── error-messages.yaml
```

---

## 9. Configuration Precedence & Conflict Resolution

### 9.1 Precedence Hierarchy

```plaintext
Highest Priority
    ↓
┌─────────────────────────────────────┐
│ 1. Workspace Rules                  │  (.agent/rules/*.md)
├─────────────────────────────────────┤
│ 2. Workspace Skills                 │  (.agent/skills/*/SKILL.md)
├─────────────────────────────────────┤
│ 3. Global Rules                     │  (~/.gemini/GEMINI.md)
├─────────────────────────────────────┤
│ 4. Global Skills                    │  (~/.gemini/antigravity/skills/)
├─────────────────────────────────────┤
│ 5. MCP Tools                        │  (mcp_config.json)
└─────────────────────────────────────┘
    ↓
Lowest Priority
```

### 9.2 Conflict Resolution Rules

| Scenario | Resolution |
| :--------- | :----------- |
| Workspace Rule ≠ Global Rule | Workspace rule overrides |
| Workflow invokes restricted operation | Rule blocks execution (rules are immutable) |
| Skill A and Skill B both match intent | Agent scores by `description` field relevance |
| MCP Tool conflicts with Skill approach | Skill provides methodology; tool provides execution |

---

## 10. Agent Execution Modes

### 10.1 Planning Mode vs. Fast Mode

Antigravity exposes two agent execution modes selectable per conversation from the Agent Manager dropdown.

| Mode | Behavior | Use When |
| :---- | :-------- | :-------- |
| **Planning** *(default)* | Agent organizes work into task groups, produces intermediate Artifacts, and reasons through multi-step plans before executing | Deep research, complex refactors, collaborative or multi-agent work |
| **Fast** | Agent executes directly without a planning phase | Simple tasks: renaming variables, running bash commands, small localized changes |

---

## 11. Advanced Patterns

### 11.1 Multi-Agent Orchestration

Antigravity's Agent Manager supports **parallel agent spawning** across workspaces:

```markdown
---
name: Microservices Refactor
trigger: /refactor-services
description: Spawns parallel agents per service
---

# Multi-Agent Refactor Workflow

## Agent Allocation
- **Agent A** (Workspace: `service-auth`): Refactor authentication service
- **Agent B** (Workspace: `service-payment`): Refactor payment service
- **Agent C** (Workspace: `service-notification`): Refactor notification service

## Synchronization Points
1. All agents complete Phase 1 (API contract definition)
2. Merge contracts into `shared-contracts.yaml`
3. All agents proceed to Phase 2 (implementation)
4. Orchestrator runs end-to-end test suite

## Artifact Collection
- `artifacts/agent-a-plan.md`
- `artifacts/agent-b-plan.md`
- `artifacts/agent-c-plan.md`
- `artifacts/integration-test-results.md`
```

### 11.2 Persona State Machines

Implement **persona transitions** within complex workflows:

```markdown
---
name: Code Review State Machine
trigger: /review
description: Multi-phase review with sequential persona hand-offs
---

## State 1: Initial Review (Persona: Senior Developer)
**Focus**: Architecture and design patterns
**Output**: Architectural feedback artifact

## State 2: Security Review (Persona: Security Engineer)
**Trigger**: Architecture feedback approved
**Focus**: Vulnerability scanning, auth/authz
**Output**: Security findings artifact

## State 3: Performance Review (Persona: Performance Engineer)
**Trigger**: No critical security issues
**Focus**: Query optimization, caching, algorithmic efficiency
**Output**: Performance recommendations artifact

## State 4: Final Approval (Persona: Tech Lead)
**Trigger**: All previous states passed
**Output**: Approval artifact with merge authorization
```

### 11.3 Self-Improving Knowledge Base

```markdown
---
name: self-improvement-logger
description: Logs agent decisions and outcomes for future optimization and rule proposals.
---

# Skill: Self-Improvement Logger

## Instructions

### Execution Logging
For every significant decision:
1. Record: user intent, chosen approach, outcome
2. Append to `.agent/execution-log.jsonl`

### Pattern Recognition (Monthly)
1. Analyze execution log for frequently failing patterns
2. Generate proposed rules: `suggested-rules.md`
3. Prompt user for review and approval before applying
```

---

## 12. Security & Guardrails

### 12.1 Execution Policy Configuration

Set via **Settings → Agent Manager → Execution Policies** or via the initial setup wizard. See Section 2 for the full policy reference.

### 12.2 Terminal Command Lists

**Denylist** — always enforced across all profiles:

```plaintext
~/.gemini/antigravity/terminalDenylist.txt
────────────────────────────────────────
rm -rf
DROP DATABASE
DELETE FROM
sudo rm
mkfs
dd if=
```

**Allowlist** — honored only under Request Review policy:

```plaintext
~/.gemini/antigravity/terminalAllowlist.txt
────────────────────────────────────────
ls
cat
grep
git status
git log
npm test
pytest
```

### 12.3 Browser Security

**Allowlist Configuration**:

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

**Rule Integration**:

```markdown
# Browser Restrictions (~/.gemini/GEMINI.md)

- Only navigate to domains listed in `browserAllowlist.txt`
- Prompt user before accessing any unlisted domain
- Never auto-submit forms on external sites
- Always request permission before downloading files from the web
```

---

## 13. Implementation Best Practices

### 13.1 Naming Conventions

| Asset Type | Convention | Examples |
| :----------- | :----------- | :--------- |
| **Rules** | `kebab-case.md` | `python-standards.md`, `security-policy.md` |
| **Workflows** | `kebab-case.md` | `deploy-production.md`, `generate-tests.md` |
| **Skills** | `kebab-case/` | `git-commit-formatter/`, `pydantic-generator/` |
| **MCP Servers** | `camelCase` | `"githubMcp"`, `"slackIntegration"` |

### 13.2 Recommended File Organization

```plaintext
~/.gemini/
├── GEMINI.md                           # Core global rules + persona
├── antigravity/
│   ├── mcp_config.json                 # MCP tool registry
│   ├── browserAllowlist.txt
│   ├── terminalDenylist.txt
│   ├── global_workflows/
│   │   ├── code-review.md
│   │   └── documentation.md
│   └── skills/
│       ├── license-header/
│       ├── conventional-commits/
│       └── python-formatter/

<project-workspace>/
├── .agent/
│   ├── rules/
│   │   ├── project-standards.md
│   │   └── api-conventions.md
│   ├── workflows/
│   │   ├── release.md
│   │   └── migration.md
│   └── skills/
│       ├── database-migration/
│       └── api-integration/
├── .context/
│   ├── architecture.md
│   ├── api-spec.yaml
│   └── glossary.md
└── AGENTS.md
```

### 13.3 Documentation Standards

**Workflow frontmatter** (required fields):

```markdown
---
name: Workflow Display Name
trigger: /command
description: One-line summary of what this workflow does
---
```

**SKILL.md frontmatter** (required fields for intent-matching):

```markdown
---
name: skill-kebab-name
description: Precise, intent-rich description to maximize discovery accuracy
---
```

**Rule file anatomy**:

```markdown
# Rule Title

## Purpose
One sentence explaining why this rule exists.

## Scope
What this rule applies to (languages, file types, operations).

## Enforcement
How violations are detected and resolved.

## Examples
✅ Correct usage
❌ Incorrect usage
```

---

## 14. Testing & Validation

### 14.1 CLI Reference (v1.16.5)

> **Breaking change**: The CLI entrypoint changed from `gemini` to `agy` in v1.15.x. All commands below use the current `agy` binary.

```bash
# Trigger a workflow
agy /test-workflow

# Verify artifacts were generated
ls -la artifacts/

# Check agent logs
cat ~/.gemini/logs/agent.log

# Verify MCP tools are connected
agy --mcp-status

# Test a workflow in dry-run mode
agy /deploy --dry-run

# List all discoverable skills
agy --list-skills

# Watch logs in real time
tail -f ~/.gemini/logs/agent.log
```

### 14.2 Automated Workflow Validation (CI)

```yaml
# .github/workflows/validate-workflows.yml
name: Validate Antigravity Workflows
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Antigravity CLI
        run: npm install -g @google/antigravity
      - name: Validate Workflow Syntax
        run: |
          for workflow in .agent/workflows/*.md; do
            agy --validate-workflow "$workflow"
          done
```

### 14.3 Skill Test Template

```markdown
# Skill Test: <Skill Name>

## Test Case 1: Basic Functionality
**Input**: [Sample input data]
**Expected Output**: [Expected result]
**Validation**: [How to verify success]

## Test Case 2: Edge Case
**Input**: [Edge case data]
**Expected Output**: [Expected handling]
**Validation**: [Verification steps]

## Test Case 3: Error Handling
**Input**: [Invalid data]
**Expected Output**: [Error message/graceful failure]
**Validation**: [Verification steps]
```

---

## 15. Troubleshooting Guide

### 15.1 Common Issues

| Problem | Diagnosis | Solution |
| :-------- | :---------- | :--------- |
| Workflow not triggering | Incorrect trigger syntax in frontmatter | Ensure `trigger: /exact-command` format |
| Skill not loading | Description too vague for intent matching | Improve frontmatter `description:` with action-oriented language |
| MCP tool unavailable | Server failed to start | Verify `mcp_config.json` paths and env var expansion |
| Rule being ignored | Workspace/global rule conflict | Check precedence hierarchy; workspace rule wins |
| Context overflow | Too many skills loading simultaneously | Make skill `description:` fields more specific |
| `agy` command not found | Old `gemini` CLI still in PATH | Reinstall with `npm install -g @google/antigravity` |

### 15.2 Debugging Techniques

**Inspect active context** by asking the agent directly:

```plaintext
"Debug: List all currently loaded skills, active rules, and available MCP tools."
```

**Isolate a skill for testing**:

```bash
# Create a temporary test workspace
mkdir /tmp/skill-test && cd /tmp/skill-test

# Copy only the target skill
cp -r ~/.gemini/antigravity/skills/my-skill .agent/skills/

# Test in isolation
agy "Test the my-skill functionality with sample input"
```

**Enable verbose logging** (in `~/.gemini/GEMINI.md`):

```markdown
## Debug Settings
- Log level: DEBUG
- Log all tool calls
- Log skill discovery process
- Log rule evaluation
```

### 15.3 Performance Optimization

**Reduce context size using the Resource pattern**:

```plaintext
# Before: Heavy Context
Loads entire 50 KB API documentation into context on every activation.

# After: Resource Pattern
SKILL.md (2 KB):
- Summarizes the API in under 10 lines
- References full docs in /resources/api-docs.md
- Agent fetches specific sections on-demand via @-mention
```

**Enable parallel execution in workflows**:

```markdown
---
name: Optimized Test Suite
trigger: /test-parallel
description: Runs all quality checks concurrently
---

## Phase 1: Concurrent Checks (Execute in parallel, NOT sequential)
- Unit tests: `pytest`
- Linting: `ruff`
- Type checking: `mypy`
- Integration tests: `pytest --integration`

## Phase 2: Aggregate Results
Wait for all parallel tasks, then merge and report.
```

---

## 16. Migration & Maintenance

### 16.1 Version Control Strategy

**Recommended `.gitignore`**:

```gitignore
# Antigravity runtime state
.gemini/logs/
.agent/state/
artifacts/tmp/

# Secrets — NEVER commit
mcp_secrets.json

# Commit these (team-shared):
# .agent/rules/
# .agent/workflows/
# .agent/skills/
# AGENTS.md
# .context/
```

### 16.2 Upgrade Path

**Pre-upgrade checklist**:

1. Back up `~/.gemini/` directory
2. Export `mcp_config.json`
3. Document active workflows and skills

**Post-upgrade validation**:

```bash
agy --mcp-status
agy /deploy --dry-run
agy --list-skills
tail -f ~/.gemini/logs/agent.log  # check for deprecation warnings
```

### 16.3 Skill Deprecation Protocol

```markdown
---
name: old-skill-name
description: DEPRECATED — Use new-skill-name instead.
---

# Skill: [Deprecated Skill Name]

> ⚠️ **DEPRECATED** as of v1.15.0.
> **Migration Path**: Use `new-skill-name` instead.
> **Removal Date**: 2026-04-01

## Legacy Instructions
[Original skill content preserved for reference]

## Migration Guide
1. Replace `old-skill` references with `new-skill`
2. Update workflow triggers from `/old-command` to `/new-command`
3. Review parameter changes: [list differences]
```

---

## 17. Relationship Summary Matrix

### 17.1 Asset Interaction Table

| From → To | Personas | Rules | Workflows | Skills | MCP Tools | Knowledge |
| :---------- | :--------- | :------ | :---------- | :------- | :---------- | :---------- |
| **Personas** | N/A | Embedded in Rules | Define workflow-specific persona | Guides skill execution style | N/A | Shapes knowledge interpretation |
| **Rules** | Defines global persona | Can reference other rules | **CONSTRAINS** execution | **CONSTRAINS** execution | Restricts tool usage | N/A |
| **Workflows** | Invokes personas per phase | **OBEYS** rules | Can chain workflows | **COMPOSES** multiple skills | Orchestrates tool calls | References knowledge files |
| **Skills** | Adopts execution persona | **OBEYS** rules | Invoked by workflows | Can depend on other skills | Uses tools for execution | Bundles knowledge in `/resources` |
| **MCP Tools** | N/A | **OBEYS** rules | Called by workflows | Called by skills | Can compose other tools | N/A |
| **Knowledge** | Informs persona context | N/A | Provides workflow context | Provides skill reference data | N/A | Can reference other knowledge |

### 17.2 Activation Flow

```plaintext
User Request
    │
    ▼
┌────────────────────────────────┐
│ 1. Load Global Rules           │  (Always-on constraints)
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 2. Load Workspace Rules        │  (Override globals)
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 3. Apply Persona               │  (From rules / AGENTS.md)
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│ 4. Check for Workflow Match    │  (Explicit /trigger)
└───────────────┬────────────────┘
         ┌──────┴──────┐
         ▼             ▼
     Match?         No Match
         │             │
         │             ▼
         │   ┌────────────────────────┐
         │   │ 5a. Skill Discovery    │
         │   │ (Intent → description) │
         │   └───────────┬────────────┘
         └───────────────┘
                         │
                         ▼
         ┌────────────────────────────────┐
         │ 6. Load MCP Tools              │  (Always available)
         └───────────────┬────────────────┘
                         │
                         ▼
         ┌────────────────────────────────┐
         │ 7. Execute with Constraints    │
         │ - Rules enforced               │
         │ - Policies applied             │
         │ - Tools called as needed       │
         │ - Artifacts generated          │
         └────────────────────────────────┘
```

---

## 18. Quick Reference

### 18.1 When to Use Each Asset

| Use Case | Asset Type | Rationale |
| :--------- | :----------- | :---------- |
| Define coding standards | **Rule** | Always-on constraint |
| Save complex prompt template | **Workflow** | Reusable, user-triggered procedure |
| Add domain-specific capability | **Skill** | Progressive disclosure (loads only when relevant) |
| Integrate external API | **MCP Tool** | Deterministic function execution |
| Enforce behavioral identity | **Persona** | Identity/style enforcement |
| Provide reference material | **Knowledge** | Static context retrieval |

### 18.2 File Location Cheat Sheet

```plaintext
Global Configuration:
~/.gemini/GEMINI.md                              → Global Rules + Persona
~/.gemini/antigravity/mcp_config.json            → MCP Tool Registry
~/.gemini/antigravity/global_workflows/          → Global Workflows
~/.gemini/antigravity/skills/                    → Global Skills
~/.gemini/antigravity/browserAllowlist.txt       → Browser domain allowlist
~/.gemini/antigravity/terminalDenylist.txt       → Command denylist (always enforced)
~/.gemini/antigravity/terminalAllowlist.txt      → Command allowlist (Request Review mode)

Workspace Configuration:
<workspace>/.agent/rules/                        → Workspace Rules
<workspace>/.agent/workflows/                    → Workspace Workflows
<workspace>/.agent/skills/                       → Workspace Skills
<workspace>/AGENTS.md                           → Workspace Persona
<workspace>/.context/                           → Knowledge Base
```

### 18.3 Syntax Quick Reference

**Rule**:

```markdown
# Rule Title
## Purpose | ## Scope | ## Enforcement | ## Examples (✅/❌)
```

**Workflow**:

```markdown
---
name: Display Name
trigger: /command
description: One-liner
---
```

**SKILL.md** (v1.16.5):

```markdown
---
name: skill-name
description: Intent-rich description for discovery
---
# Skill: Name
## Description | ## Trigger Patterns | ## Instructions | ## Deliverables
```

**MCP Config**:

```json
{
  "mcpServers": {
    "serverName": {
      "command": "executable",
      "args": ["arg1"],
      "env": {"KEY": "${ENV_VAR}"}
    }
  }
}
```

---

## Appendix A: Migration from Traditional IDEs

| Traditional IDE Feature | Antigravity Equivalent |
| :------------------------ | :----------------------- |
| Code snippets | Workflows (with `/trigger`) |
| Linter configurations | Rules (e.g., `eslint-rules.md`) |
| IDE plugins | Skills (progressive loading) |
| External tools (git, docker) | MCP Tools |
| Workspace settings | `.agent/` directory configuration |
| Project documentation | `.context/` knowledge base |
| Code templates | Skill examples (`/examples`) |

**Migration Strategy**:

1. Convert linter configs → Rules
2. Export code snippets → Workflows
3. Identify external tools → Configure MCP
4. Document domain knowledge → Create `.context/` files
5. Define team standards → Create `AGENTS.md` persona

---

## Appendix B: v1.14.2 → v1.16.5 Migration Checklist

| Item | Action Required |
| :---- | :-------------- |
| CLI binary | Update scripts: `gemini` → `agy` |
| Strict Mode | Update references: "Secure Mode" → "Strict Mode" |
| Skill static assets | Rename `references/` → `resources/` (optional but recommended) |
| SKILL.md files | Add YAML frontmatter (`name:`, `description:`) for improved discovery |
| Execution policies | Review three-axis policy model (Terminal, Review, JavaScript) |
| Deprecated skills | Update deprecation notice version and removal date |

---

## Appendix C: Reference Links

- **Official Documentation**: [antigravity.google/docs](https://antigravity.google/docs)
- **Download**: [antigravity.google/download](https://antigravity.google/download)
- **Google Developers Blog**: [developers.googleblog.com](https://developers.googleblog.com)
- **Getting Started Codelab**: [codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **AI Studio**: [aistudio.google.com](https://aistudio.google.com)
