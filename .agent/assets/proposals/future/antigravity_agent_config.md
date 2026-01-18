# Google Antigravity v1.14.2: Agent Configuration Technical Reference

## Executive Summary

Google Antigravity implements an **agent-first development platform** where configuration assets (Personas, Rules, Tools, Workflows, Skills, Knowledge) operate through a hierarchical, progressive disclosure architecture. This document provides implementation standards for configuring agent relationships and asset interactions.

---

## 1. Core Configuration Asset Types

### 1.1 Asset Taxonomy

| Asset Type | Scope | Activation | Purpose | Format |
|:-----------|:------|:-----------|:--------|:-------|
| **Personas** | Implicit/Defined | System instruction | Define agent behavioral identity | Markdown (system_instruction) |
| **Rules** | Global/Workspace | Always-on | Passive behavioral constraints | Markdown (`.md`) |
| **Workflows** | Global/Workspace | User-triggered | On-demand prompt templates | Markdown (`.md`) |
| **Skills** | Global/Workspace | Context-matched | Progressive capability extension | Directory (`SKILL.md` + assets) |
| **Tools (MCP)** | Global | Always-available | Deterministic function execution | JSON config + MCP server |
| **Knowledge** | Workspace | Reference-based | Domain-specific context | Markdown/text files |

### 1.2 Scope Hierarchy

```
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
│   │       ├── references/
│   │       └── examples/
│   └── browserAllowlist.txt            # Security constraints

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
│           ├── references/
│           └── examples/
├── AGENTS.md                           # Workspace-specific persona/rules
└── .context/                           # Knowledge base (project-specific)
```

---

## 2. Personas: Behavioral Identity Layer

### 2.1 Definition

Personas define **agent behavioral identity** through system instructions. While Antigravity does not expose explicit "Persona" files, personas are implemented through:

1. **System Instructions** (API-level)
2. **Rules** (embedded persona definitions)
3. **Workflow preambles** (task-specific personas)

### 2.2 Implementation Patterns

#### Pattern A: Global Persona via Rules

**Location**: `~/.gemini/GEMINI.md`

```markdown
# Global Persona Definition

You are a Senior Software Architect specializing in distributed systems.

## Core Principles
- Always prioritize system resilience over performance
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

**Activation**: Add to `~/.gemini/GEMINI.md`:

```markdown
# Auto-load workspace personas
- Check for the presence of AGENTS.md files in the project workspace
- Load and apply all instructions from AGENTS.md as system-level constraints
- May contain sub-folder AGENTS.md with section-specific instructions
```

#### Pattern C: Workflow-Embedded Persona

**Location**: `<workspace>/.agent/workflows/architecture-review.md`

```markdown
---
name: Architecture Review
trigger: /architecture-review
---

# Architecture Review Workflow

**Persona**: You are The Architect, a principal engineer focused on system design critique.

**Execution Steps**:
1. Analyze current system topology
2. Identify single points of failure
3. Propose resilience improvements
4. Generate architecture diagram artifact
```

### 2.3 Persona → Workflow Binding

Workflows can **invoke specific personas** for execution phases:

```markdown
---
name: Code Review
trigger: /review
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

## 3. Rules: Passive Behavioral Constraints

### 3.1 Characteristics

| Property | Value |
|:---------|:------|
| **Activation** | Always-on (loaded into every agent context) |
| **Scope** | Global (`~/.gemini/GEMINI.md`) or Workspace (`<workspace>/.agent/rules/*.md`) |
| **Precedence** | Workspace rules override global rules |
| **Analogy** | System instructions / Constitution |

### 3.2 Implementation Standards

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
* Every public function requires docstring
* Complex algorithms need inline comments
* Update README.md when adding new features

## Testing
* Minimum 80% test coverage for new code
* Always write tests before implementation (TDD)
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
project/
├── src/
│   ├── __init__.py
│   ├── core/           # Business logic
│   ├── api/            # External interfaces
│   └── utils/          # Helpers
├── tests/
└── docs/
```
```

### 3.3 Rules → Workflow Interaction

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
**Execution**: (Only proceeds if rule satisfied)
```

---

## 4. Workflows: On-Demand Prompt Templates

### 4.1 Characteristics

| Property | Value |
|:---------|:------|
| **Activation** | User-triggered via `/workflow-name` |
| **Scope** | Global (`~/.gemini/antigravity/global_workflows/`) or Workspace (`<workspace>/.agent/workflows/`) |
| **Analogy** | Saved prompts / Task templates |

### 4.2 Implementation Standards

#### Workflow File Structure

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
   - Ensure test naming follows `test_<function>_<scenario>` convention

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

### 4.3 Workflow → Skill Integration

Workflows can **compose multiple skills** for complex operations:

```markdown
---
name: Full Stack Deploy
trigger: /deploy
---

# Full Stack Deployment Workflow

## Phase 1: Pre-deployment (Skill: `code-quality-check`)
- Run linters
- Execute test suite
- Generate coverage report

## Phase 2: Build (Skill: `docker-build`)
- Build Docker images
- Tag with commit SHA
- Push to registry

## Phase 3: Infrastructure (Skill: `terraform-apply`)
- Validate Terraform plan
- Apply infrastructure changes
- Capture resource IDs

## Phase 4: Deployment (Skill: `kubernetes-deploy`)
- Update K8s manifests
- Apply deployment
- Monitor rollout status

## Phase 5: Verification (Skill: `smoke-test`)
- Execute smoke test suite
- Verify health endpoints
- Generate deployment artifact
```

---

## 5. Skills: Progressive Capability Extension

### 5.1 Architecture Principle

**Skills solve context saturation**: Instead of loading all capabilities into every agent context, skills are **dynamically loaded only when relevant**.

```
┌─────────────────────────────────────────┐
│  Agent Request (User Prompt)            │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Skill Discovery (Manifest Matching)    │
│  - Parse user intent                    │
│  - Match to skill descriptions          │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Skill Loading (Progressive Disclosure) │
│  - Load SKILL.md into context           │
│  - Reference scripts/references/examples│
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Skill Execution                        │
│  - Follow SKILL.md instructions         │
│  - Execute scripts if needed            │
│  - Generate artifacts                   │
└─────────────────────────────────────────┘
```

### 5.2 Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required: Skill definition and instructions
├── scripts/              # Optional: Executable automation
│   ├── run.py
│   └── util.sh
├── references/           # Optional: Static reference materials
│   ├── api-schema.json
│   └── documentation.md
├── examples/             # Optional: Few-shot learning examples
│   ├── example-1.md
│   └── example-2.md
└── assets/               # Optional: Images, templates
    └── template.yaml
```

### 5.3 SKILL.md Specification

```markdown
# Skill: Git Commit Formatter

## Description
Enforces Conventional Commits specification for all git commits.

## Trigger Patterns
- User writes commit message
- User invokes `git commit`
- Workflow includes commit step

## Instructions

### Pre-commit Analysis
1. Parse the user's intended commit message
2. Identify the commit type from keywords:
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
- Subject must be imperative mood ("add" not "added")

### Example Transformations
| User Input | Formatted Output |
|:-----------|:-----------------|
| "fixed the login bug" | `fix(auth): resolve login validation error` |
| "Added new API endpoint" | `feat(api): add user profile endpoint` |
| "updated docs" | `docs: update API documentation` |

## Execution Flow
```python
# Pseudo-code execution protocol
def format_commit(user_message):
    commit_type = detect_type(user_message)
    scope = extract_scope(user_message) or None
    subject = clean_subject(user_message)
    
    formatted = f"{commit_type}"
    if scope:
        formatted += f"({scope})"
    formatted += f": {subject}"
    
    return formatted
```

## Deliverables
- Artifact: `formatted_commit.txt` with proposed message
- Prompt user for approval before executing `git commit`
```

### 5.4 Skill Patterns

#### Pattern 1: Basic Router (SKILL.md only)

**Use Case**: Simple instruction set without external assets

```markdown
# Skill: JSON Formatter

## Description
Formats and validates JSON documents

## Instructions
1. Parse input JSON
2. Validate syntax
3. Pretty-print with 2-space indentation
4. Sort keys alphabetically
5. Return formatted JSON
```

#### Pattern 2: Reference Pattern (SKILL.md + /references)

**Use Case**: Incorporating large static documents without bloating context

**Structure**:
```
license-header-skill/
├── SKILL.md
└── references/
    └── apache-2.0-header.txt
```

**SKILL.md**:
```markdown
# Skill: Apache License Header

## Instructions
1. Check if file starts with license header
2. If missing, read template from `references/apache-2.0-header.txt`
3. Insert header at file beginning
4. Preserve existing file content
```

#### Pattern 3: Few-Shot Pattern (SKILL.md + /examples)

**Use Case**: Teaching complex transformations through examples

**Structure**:
```
pydantic-generator/
├── SKILL.md
└── examples/
    ├── input-1.json
    ├── output-1.py
    ├── input-2.json
    └── output-2.py
```

**SKILL.md**:
```markdown
# Skill: JSON to Pydantic Model

## Instructions
1. Analyze JSON structure
2. Infer field types
3. Generate Pydantic BaseModel class
4. Follow patterns demonstrated in `examples/`

## Reference Examples
- **Simple Object**: See `examples/input-1.json` → `examples/output-1.py`
- **Nested Arrays**: See `examples/input-2.json` → `examples/output-2.py`
```

#### Pattern 4: Tool Use Pattern (SKILL.md + /scripts)

**Use Case**: Delegating execution to deterministic scripts

**Structure**:
```
database-migration/
├── SKILL.md
└── scripts/
    ├── migrate.py
    └── rollback.sh
```

**SKILL.md**:
```markdown
# Skill: Database Migration

## Instructions
1. Parse user's target environment (dev/staging/prod)
2. Execute migration script: `scripts/migrate.py --env <environment>`
3. Capture script output
4. If exit code != 0, execute `scripts/rollback.sh`
5. Generate artifact: `migration_log.md`

## Script Interface
```bash
# Execute migration
python scripts/migrate.py --env staging --dry-run

# Rollback if needed
bash scripts/rollback.sh --env staging --version <previous>
```

## Safety Constraints
- **Production**: Always require explicit approval before execution
- **Dry Run**: Default to `--dry-run` flag, remove only on confirmation
```

### 5.5 Skills → Workflow Composition

Workflows orchestrate **multi-skill sequences**:

```markdown
---
name: Release Process
trigger: /release
---

# Release Workflow

## Phase 1: Version Bump (Skill: `semantic-versioning`)
- Analyze commit history since last tag
- Determine version bump (major/minor/patch)
- Update version files

## Phase 2: Changelog (Skill: `changelog-generator`)
- Generate changelog from commits
- Format using Keep a Changelog standard
- Create artifact: `CHANGELOG.md`

## Phase 3: Git Operations (Skill: `git-release`)
- Create release branch
- Commit version changes
- Tag with new version
- Push to remote

## Phase 4: Build (Skill: `docker-build`)
- Build release artifacts
- Tag with version number
- Push to registry

## Phase 5: Deployment (Skill: `kubernetes-deploy`)
- Update production manifests
- Apply deployment
- Monitor rollout
```

---

## 6. Tools (MCP): Deterministic Function Layer

### 6.1 Model Context Protocol (MCP) Architecture

MCP servers expose **deterministic tools** to agents. Tools are **always available** once configured (no progressive loading like Skills).

```
┌─────────────────────────────────────────┐
│  Antigravity Agent                      │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  MCP Client (mcp_config.json)           │
│  - Manages server connections           │
│  - Routes tool calls                    │
└─────────────┬───────────────────────────┘
              │
         ┌────┼────┬────────┬───────┐
         ▼    ▼    ▼        ▼       ▼
    ┌─────┬─────┬──────┬────────┬──────┐
    │GitHub│Slack│Notion│Postgres│Custom│
    │ MCP │ MCP │ MCP  │  MCP   │ MCP  │
    └─────┴─────┴──────┴────────┴──────┘
```

### 6.2 MCP Configuration

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
        "run",
        "-i",
        "--rm",
        "mcp/postgres",
        "postgresql://user:pass@localhost/db"
      ]
    },
    "custom-tool": {
      "command": "node",
      "args": [
        "/absolute/path/to/custom-mcp-server/index.js"
      ],
      "env": {
        "API_KEY": "${CUSTOM_API_KEY}",
        "LOG_LEVEL": "error"
      }
    }
  }
}
```

### 6.3 Tool Discovery

Once configured, MCP tools are **automatically available** to agents:

```
Agent Context (Automatic Tool Injection):
┌─────────────────────────────────────────────────────┐
│ Available Tools (from MCP):                         │
│ - github_create_issue(title, body, labels)          │
│ - github_list_prs(repo, state)                      │
│ - slack_send_message(channel, text)                 │
│ - postgres_execute_query(sql)                       │
│ - custom_tool_analyze(data)                         │
└─────────────────────────────────────────────────────┘
```

### 6.4 Skills vs. MCP Tools: Design Decision Matrix

| Factor | Use Skill | Use MCP Tool |
|:-------|:----------|:-------------|
| **Context Sensitivity** | High (load only when relevant) | Low (always available) |
| **Execution Complexity** | Multi-step procedures | Single function calls |
| **State Management** | May require ephemeral state | Stateless preferred |
| **Infrastructure** | File-based (no server) | Requires MCP server |
| **Example** | "Generate release notes from commits" | "Execute SQL query" |

### 6.5 Tools → Skills Integration

Skills can **orchestrate tool usage**:

```markdown
# Skill: GitHub Release Automation

## Instructions
1. Use tool `github_list_commits(since_tag)` to get commits
2. Parse commit messages for changelog
3. Use tool `github_create_release(tag, notes)` to publish
4. Use tool `slack_send_message(channel, text)` to notify team

## Tool Call Sequence
```python
# Pseudo-code
commits = github_list_commits(since_tag="v1.0.0")
changelog = generate_changelog(commits)
release = github_create_release(
    tag="v1.1.0",
    notes=changelog
)
slack_send_message(
    channel="#releases",
    text=f"Released {release.tag}"
)
```
```

### 6.6 MCP Router Pattern (Advanced)

For complex tool ecosystems, implement a **single router MCP** that proxies to multiple backends:

```json
{
  "mcpServers": {
    "rube-router": {
      "command": "npx",
      "args": ["-y", "rube-mcp"],
      "env": {
        "RUBE_BACKENDS": "github,slack,postgres,notion"
      }
    }
  }
}
```

**Benefit**: Agent only sees one MCP connection, reducing context pollution. Router dynamically loads backend tools on-demand.

---

## 7. Knowledge: Domain-Specific Context

### 7.1 Knowledge Base Structure

```
<workspace>/
├── .context/                    # Knowledge base directory
│   ├── architecture.md          # System architecture docs
│   ├── api-contracts.yaml       # API specifications
│   ├── deployment-guide.md      # Ops procedures
│   └── domain-glossary.md       # Business terminology
└── docs/                        # Traditional documentation
    └── README.md
```

### 7.2 Knowledge → Agent Injection

Knowledge files are **referenced explicitly** by agents or skills:

#### Method 1: Direct Reference in Prompt

```
User Prompt:
"Review the authentication flow for security issues. Reference @.context/architecture.md for current design."
```

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
# Global Rule (~/.gemini/GEMINI.md)

## Knowledge Context Protocol
- Always check for `.context/` directory in workspace
- Load `.context/architecture.md` for system design questions
- Load `.context/domain-glossary.md` for business term questions
- Cite source file when using knowledge base information
```

### 7.3 Knowledge → Skill Composition

Skills can **bundle knowledge** in `/references`:

```
data-validation-skill/
├── SKILL.md
└── references/
    ├── validation-rules.json
    └── error-messages.yaml
```

**SKILL.md**:
```markdown
# Skill: Data Validation

## Instructions
1. Load validation rules from `references/validation-rules.json`
2. Apply rules to user input data
3. Map violations to error messages from `references/error-messages.yaml`
4. Generate validation report artifact
```

---

## 8. Configuration Precedence & Conflict Resolution

### 8.1 Precedence Hierarchy

```
Highest Priority
    ↓
┌─────────────────────────────────────┐
│ 1. Workspace Rules                  │  (.agent/rules/*.md)
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. Workspace Skills                 │  (.agent/skills/*/SKILL.md)
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Global Rules                     │  (~/.gemini/GEMINI.md)
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Global Skills                    │  (~/.gemini/antigravity/skills/)
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. MCP Tools                        │  (mcp_config.json)
└─────────────────────────────────────┘
    ↓
Lowest Priority
```

### 8.2 Conflict Resolution Rules

| Scenario | Resolution |
|:---------|:-----------|
| **Workspace Rule ≠ Global Rule** | Workspace rule overrides |
| **Workflow invokes restricted operation** | Rule blocks execution (rules are immutable) |
| **Skill A and Skill B both match** | Agent chooses based on description relevance score |
| **MCP Tool conflicts with Skill** | Skill provides methodology; tool provides execution |

### 8.3 Example: Deployment Conflict

**Global Rule**: "Never deploy to production without approval"

**Workflow**: "Deploy to Production" attempts auto-deployment

**Resolution**:
```
Agent Execution Flow:
1. Workflow `/deploy-prod` triggered
2. Agent checks Global Rules
3. Finds constraint: "Never deploy to production without approval"
4. Agent prompts user: "This workflow requires approval. JIRA ticket ID?"
5. If no approval provided → Halt execution
6. If approval provided → Proceed with deployment
```

---

## 9. Advanced Patterns

### 9.1 Multi-Agent Orchestration

Antigravity supports **parallel agent spawning**. Coordinate via Workflows:

```markdown
---
name: Microservices Refactor
trigger: /refactor-services
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
4. All agents complete Phase 3 (integration tests)
5. Orchestrator agent runs end-to-end test suite

## Artifact Collection
- `artifacts/agent-a-plan.md`
- `artifacts/agent-b-plan.md`
- `artifacts/agent-c-plan.md`
- `artifacts/integration-test-results.md`
```

### 9.2 Conditional Skill Loading

Implement **skill routing** based on runtime conditions:

```markdown
# Skill: Dynamic Database Connector

## Description
Connects to appropriate database based on environment

## Trigger Patterns
- Database query requests
- Schema inspection requests

## Instructions

### Environment Detection
1. Check environment variable `APP_ENV`
2. Route to appropriate skill:
   - `dev` → Load `postgres-dev-skill`
   - `staging` → Load `postgres-staging-skill`
   - `prod` → Load `postgres-prod-skill`

### Safety Checks
- **Production**: Read-only queries only (no DML)
- **Staging**: Require approval for schema changes
- **Dev**: Full permissions
```

### 9.3 Persona State Machines

Implement **persona transitions** for complex workflows:

```markdown
---
name: Code Review State Machine
trigger: /review
---

# Code Review Workflow

## State 1: Initial Review (Persona: Senior Developer)
**Focus**: High-level architecture and design patterns
**Output**: Architectural feedback artifact

## State 2: Security Review (Persona: Security Engineer)
**Trigger**: Architecture feedback approved
**Focus**: Vulnerability scanning, auth/authz review
**Output**: Security findings artifact

## State 3: Performance Review (Persona: Performance Engineer)
**Trigger**: No critical security issues
**Focus**: Query optimization, caching, algorithmic efficiency
**Output**: Performance recommendations artifact

## State 4: Final Approval (Persona: Tech Lead)
**Trigger**: All previous reviews passed
**Focus**: Synthesis of findings, approval decision
**Output**: Approval artifact with merge authorization
```

---

## 10. Security & Guardrails

### 10.1 Terminal Execution Policies

Configure agent autonomy for command execution:

```
Terminal Command Auto Execution Policies:
┌───────────────────────────────────────────────────┐
│ TURBO (Autopilot)                                 │
│ - Agent executes all commands without approval    │
│ - Use: Greenfield projects, trusted environments │
└───────────────────────────────────────────────────┘
            ↓ (Risk increases downward)
┌───────────────────────────────────────────────────┐
│ AUTO (Agent-Assisted - RECOMMENDED)               │
│ - Agent executes safe commands (ls, cat, grep)    │
│ - Prompts for destructive ops (rm, DROP, DELETE)  │
│ - Use: Most development scenarios                 │
└───────────────────────────────────────────────────┘
            ↓
┌───────────────────────────────────────────────────┐
│ OFF (Review-Driven)                               │
│ - Agent prompts for EVERY command                 │
│ - Use: Production systems, critical infrastructure│
└───────────────────────────────────────────────────┘
```

**Configuration**: Settings → Agent Manager → Terminal Policy

### 10.2 Allow/Deny Lists

**Allow List** (in `OFF` mode):
```
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

**Deny List** (in `TURBO`/`AUTO` mode):
```
~/.gemini/antigravity/terminalDenylist.txt
────────────────────────────────────────
rm -rf
DROP DATABASE
DELETE FROM
sudo rm
mkfs
dd if=
```

### 10.3 Browser Security

**Allowlist Configuration**:
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

**Rule Integration**:
```markdown
# Global Rule (~/.gemini/GEMINI.md)

## Browser Restrictions
- Only navigate to domains in `browserAllowlist.txt`
- Prompt user if attempting to access unlisted domain
- Never auto-submit forms on external sites
- Always ask before downloading files from web
```

---

## 11. Implementation Best Practices

### 11.1 Naming Conventions

| Asset Type | Convention | Examples |
|:-----------|:-----------|:---------|
| **Rules** | `kebab-case.md` | `python-standards.md`, `security-policy.md` |
| **Workflows** | `kebab-case.md` | `deploy-production.md`, `generate-tests.md` |
| **Skills** | `kebab-case/` | `git-commit-formatter/`, `pydantic-generator/` |
| **MCP Servers** | `camelCase` | `"githubMcp"`, `"slackIntegration"` |
| **Personas** | N/A (embedded in rules/workflows) | N/A |

### 11.2 File Organization Strategy

```
Recommended Structure:
~/.gemini/
├── GEMINI.md                           # Core global rules + persona
├── antigravity/
│   ├── mcp_config.json                 # MCP tool registry
│   ├── global_workflows/
│   │   ├── code-review.md              # Cross-project workflows
│   │   └── documentation.md
│   └── skills/
│       ├── license-header/             # Reusable skills
│       ├── conventional-commits/
│       └── python-formatter/

<project-workspace>/
├── .agent/
│   ├── rules/
│   │   ├── project-standards.md        # Project-specific constraints
│   │   └── api-conventions.md
│   ├── workflows/
│   │   ├── release.md                  # Project-specific workflows
│   │   └── migration.md
│   └── skills/
│       ├── database-migration/         # Project-specific skills
│       └── api-integration/
├── .context/
│   ├── architecture.md                 # Knowledge base
│   ├── api-spec.yaml
│   └── glossary.md
└── AGENTS.md                           # Project persona definition
```

### 11.3 Documentation Standards

Every asset should include:

**Rules**:
```markdown
# Rule Name

## Purpose
One sentence explaining why this rule exists.

## Scope
What this rule applies to (languages, file types, operations).

## Enforcement
How violations are detected and resolved.

## Examples
âœ… Correct usage
âŒ Incorrect usage
```

**Workflows**:
```markdown
---
name: Workflow Name
trigger: /command
description: One-line summary
---

# Workflow Name

## Prerequisites
What must exist before execution.

## Execution Steps
Numbered list with clear phases.

## Deliverables
What artifacts are generated.

## Rollback Procedure
How to undo if needed.
```

**Skills**:
```markdown
# Skill: Skill Name

## Description
One paragraph explaining capability.

## Trigger Patterns
When this skill activates.

## Instructions
Step-by-step execution protocol.

## Examples (if applicable)
Reference to `/examples` directory.

## Dependencies
Required tools, libraries, or other skills.
```

### 11.4 Testing & Validation

#### Testing Workflows

**Manual Testing**:
```bash
# In workspace with test workflow
gemini /test-workflow

# Verify artifacts generated
ls -la artifacts/

# Check logs for errors
cat ~/.gemini/logs/agent.log
```

**Automated Testing** (via CI):
```yaml
# .github/workflows/validate-workflows.yml
name: Validate Antigravity Workflows
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Antigravity
        run: npm install -g @google/antigravity
      - name: Validate Workflow Syntax
        run: |
          for workflow in .agent/workflows/*.md; do
            gemini --validate-workflow "$workflow"
          done
```

#### Testing Skills

**Skill Test Template** (`skill-name/tests/test_skill.md`):
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
**Expected Output**: [Error message/handling]
**Validation**: [Verification steps]
```

---

## 12. Migration & Maintenance

### 12.1 Version Control Strategy

**Recommended `.gitignore`**:
```gitignore
# Antigravity logs
.gemini/logs/

# Local agent state
.agent/state/

# Temporary artifacts
artifacts/tmp/

# MCP secrets
mcp_secrets.json

# DO commit:
# - .agent/rules/
# - .agent/workflows/
# - .agent/skills/
# - AGENTS.md
# - .context/
```

**Shared Team Configuration**:
```
Repository Structure for Team:
project/
├── .agent/                     # Committed (team-shared)
│   ├── rules/
│   ├── workflows/
│   └── skills/
├── .context/                   # Committed (team-shared)
├── AGENTS.md                   # Committed (team-shared)
└── .agent-local/               # Gitignored (developer-specific)
    └── overrides.md
```

### 12.2 Upgrade Path

When updating Antigravity versions:

**Pre-Upgrade Checklist**:
1. Backup `~/.gemini/` directory
2. Export current `mcp_config.json`
3. Document active workflows and skills
4. Test in isolated workspace first

**Post-Upgrade Validation**:
```bash
# Verify MCP tools still connect
gemini --mcp-status

# Test critical workflows
gemini /deploy --dry-run

# Check skill discovery
gemini --list-skills

# Review logs for deprecation warnings
tail -f ~/.gemini/logs/agent.log
```

### 12.3 Skill Deprecation Protocol

```markdown
# Skill: [Deprecated Skill Name]

**⚠️ DEPRECATED**: This skill is deprecated as of v1.15.0.
**Migration Path**: Use `new-skill-name` instead.
**Removal Date**: 2026-03-01

## Legacy Instructions
[Original skill content preserved for reference]

## Migration Guide
1. Replace references to `old-skill` with `new-skill`
2. Update workflow triggers from `/old-command` to `/new-command`
3. Review changed parameters: [list differences]
```

---

## 13. Troubleshooting Guide

### 13.1 Common Issues

| Problem | Diagnosis | Solution |
|:--------|:----------|:---------|
| **Workflow not triggering** | Check trigger syntax in frontmatter | Ensure `trigger: /exact-command` format |
| **Skill not loading** | Manifest description too vague | Improve `## Description` to match user intent patterns |
| **MCP tool unavailable** | Server failed to start | Check `mcp_config.json` for correct paths/env vars |
| **Rule being ignored** | Workspace rule conflicts | Check precedence hierarchy |
| **Context overflow** | Too many skills loaded | Use more specific skill descriptions for targeting |

### 13.2 Debugging Techniques

**Enable Verbose Logging**:
```bash
# In ~/.gemini/GEMINI.md
## Debug Settings
- Log level: DEBUG
- Log all tool calls
- Log skill discovery process
- Log rule evaluation
```

**Inspect Agent Context**:
```
User Prompt:
"Debug: Show me all currently loaded skills, rules, and available MCP tools in your context."

Agent Response:
┌─────────────────────────────────────────┐
│ Active Configuration                    │
├─────────────────────────────────────────┤
│ Rules (2):                              │
│  - Global: GEMINI.md                    │
│  - Workspace: project-standards.md      │
│                                         │
│ Skills (3):                             │
│  - git-commit-formatter                 │
│  - python-formatter                     │
│  - conventional-commits                 │
│                                         │
│ MCP Tools (12):                         │
│  - github_create_issue                  │
│  - slack_send_message                   │
│  - postgres_execute_query               │
│  - ...                                  │
└─────────────────────────────────────────┘
```

**Test Skill Isolation**:
```bash
# Create test workspace
mkdir /tmp/skill-test
cd /tmp/skill-test

# Copy only target skill
cp -r ~/.gemini/antigravity/skills/test-skill .agent/skills/

# Test in isolation
gemini "Test the test-skill functionality"
```

### 13.3 Performance Optimization

**Reduce Context Size**:
```markdown
# Skill Optimization

## Before (Heavy Context)
Loads entire 50KB API documentation into context on every activation.

## After (Reference Pattern)
SKILL.md (2KB):
- Loads only relevant API section based on user intent
- References full docs in `/references` directory
- Agent fetches specific sections on-demand
```

**Parallel Execution**:
```markdown
---
name: Optimized Test Suite
trigger: /test-parallel
---

# Parallel Test Execution

## Phase 1: Concurrent Test Runs
Execute in parallel (NOT sequential):
- Unit tests (pytest)
- Integration tests (pytest-integration)
- Linting (ruff)
- Type checking (mypy)

## Phase 2: Aggregate Results
Wait for all parallel tasks to complete, then merge reports.
```

---

## 14. Advanced Use Cases

### 14.1 Cross-Repository Orchestration

**Scenario**: Coordinate changes across microservices

**Implementation**:
```markdown
---
name: Multi-Repo Feature Deploy
trigger: /deploy-feature
---

# Multi-Repository Feature Deployment

## Inputs
- Feature name
- Target environment

## Execution

### Step 1: Repository Updates
For each repository in [auth-service, payment-service, notification-service]:
1. Clone repository
2. Create feature branch
3. Apply feature-specific changes
4. Run tests
5. Create pull request

### Step 2: Integration Verification
1. Deploy all services to staging environment
2. Run end-to-end test suite
3. Generate integration report artifact

### Step 3: Production Deployment
If all tests pass:
1. Merge all PRs
2. Tag releases
3. Deploy to production (staggered rollout)
4. Monitor metrics for 15 minutes
5. Notify team via Slack MCP tool
```

### 14.2 Self-Improving Agents

**Pattern**: Agents learn from execution logs

```markdown
# Skill: Self-Improvement Logger

## Description
Logs agent decisions and outcomes for future optimization

## Instructions

### Execution Logging
For every significant decision:
1. Record: User intent, chosen approach, outcome
2. Store in `.agent/execution-log.jsonl`

### Pattern Recognition
Monthly task:
1. Analyze execution log
2. Identify frequently failing patterns
3. Generate new rule proposals: `suggested-rules.md`
4. Prompt user for review and approval

### Example Log Entry
```json
{
  "timestamp": "2026-01-18T10:30:00Z",
  "user_intent": "Deploy to production",
  "approach": "Used blue-green deployment",
  "outcome": "SUCCESS",
  "duration_seconds": 180,
  "notes": "Zero downtime achieved"
}
```
```

### 14.3 Compliance & Audit Trails

**Scenario**: Maintain SOC2/ISO27001 compliance

```markdown
# Workflow: Compliance Audit Trail

## Trigger
Automatically after every production deployment

## Execution

### Step 1: Capture Deployment Metadata
- Timestamp
- User who triggered deployment
- Git commit SHA
- Approval ticket ID (JIRA)
- Environment target

### Step 2: Log to Immutable Store
Use MCP tool: `audit_log_append(entry)`
- Writes to append-only log
- Cryptographically signed
- Stored in compliance S3 bucket

### Step 3: Generate Compliance Report
Artifact: `compliance/deploy-<timestamp>.md`
- Includes all approval chains
- Links to test results
- Records any exceptions/overrides

### Step 4: Notify Compliance Team
Slack MCP: Send summary to #compliance channel
```

---

## 15. Relationship Summary Matrix

### 15.1 Asset Interaction Table

| From → To | Personas | Rules | Workflows | Skills | MCP Tools | Knowledge |
|:----------|:---------|:------|:----------|:-------|:----------|:----------|
| **Personas** | N/A | Embedded in Rules | Can define workflow-specific persona | Guides skill execution behavior | N/A | Shapes knowledge interpretation |
| **Rules** | Defines global persona | Can reference other rules | **CONSTRAINS** workflow execution | **CONSTRAINS** skill execution | Restricts tool usage | N/A |
| **Workflows** | Invokes personas for phases | **OBEYS** rules | Can chain workflows | **COMPOSES** multiple skills | Orchestrates tool calls | References knowledge files |
| **Skills** | Adopts execution persona | **OBEYS** rules | Invoked by workflows | Can depend on other skills | Uses tools for execution | Bundles knowledge in `/references` |
| **MCP Tools** | N/A | **OBEYS** rules | Called by workflows | Called by skills | Can compose other tools | N/A |
| **Knowledge** | Informs persona context | N/A | Provides workflow context | Provides skill reference data | N/A | Can reference other knowledge |

### 15.2 Activation Flow

```
User Request
    │
    ▼
┌─────────────────────────────┐
│ 1. Load Global Rules        │ (Always-on constraints)
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 2. Load Workspace Rules     │ (Override globals)
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 3. Apply Persona            │ (From rules/workflows)
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 4. Check for Workflow Match │ (Explicit trigger)
└─────────────┬───────────────┘
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
   Match?          No Match
       │             │
       │             ▼
       │      ┌─────────────────────────────┐
       │      │ 5a. Skill Discovery         │
       │      │ (Progressive loading)       │
       │      └─────────────┬───────────────┘
       │                    │
       └────────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │ 6. Load MCP Tools           │ (Always available)
              └─────────────┬───────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │ 7. Execute with Constraints │
              │ - Rules enforced            │
              │ - Tools called as needed    │
              │ - Artifacts generated       │
              └─────────────────────────────┘
```

---

## 16. Quick Reference Card

### 16.1 When to Use Each Asset

| Use Case | Asset Type | Rationale |
|:---------|:-----------|:----------|
| Define coding standards | **Rule** | Always-on constraint |
| Save complex prompt template | **Workflow** | Reusable, triggered procedure |
| Add domain-specific capability | **Skill** | Progressive disclosure (only loads when relevant) |
| Integrate external API | **MCP Tool** | Deterministic function execution |
| Embed behavior into execution | **Persona** | Identity/style enforcement |
| Provide reference material | **Knowledge** | Static context retrieval |

### 16.2 File Location Cheat Sheet

```
Global Configuration:
~/.gemini/GEMINI.md                          → Global Rules + Persona
~/.gemini/antigravity/mcp_config.json        → MCP Tool Registry
~/.gemini/antigravity/global_workflows/      → Global Workflows
~/.gemini/antigravity/skills/                → Global Skills

Workspace Configuration:
<workspace>/.agent/rules/                    → Workspace Rules
<workspace>/.agent/workflows/                → Workspace Workflows
<workspace>/.agent/skills/                   → Workspace Skills
<workspace>/AGENTS.md                        → Workspace Persona
<workspace>/.context/                        → Knowledge Base

Security:
~/.gemini/antigravity/browserAllowlist.txt   → Browser restrictions
~/.gemini/antigravity/terminalAllowlist.txt  → Command whitelist
~/.gemini/antigravity/terminalDenylist.txt   → Command blacklist
```

### 16.3 Syntax Quick Reference

**Rule Syntax**:
```markdown
# Rule Title

## Purpose
Why this rule exists

## Scope
What it applies to

## Examples
âœ… Correct
âŒ Incorrect
```

**Workflow Syntax**:
```markdown
---
name: Display Name
trigger: /command
description: One-liner
---

# Workflow Title

## Steps
1. First step
2. Second step
```

**Skill Manifest**:
```markdown
# Skill: Name

## Description
What this skill does

## Trigger Patterns
When it activates

## Instructions
How to execute
```

**MCP Config**:
```json
{
  "mcpServers": {
    "serverName": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {"KEY": "value"}
    }
  }
}
```

---

## 17. Conclusion

Google Antigravity's agent configuration system implements a **hierarchical, composable architecture** where:

1. **Rules** establish immutable behavioral constraints
2. **Personas** define execution identity and style
3. **Workflows** provide reusable prompt templates
4. **Skills** enable progressive capability disclosure
5. **MCP Tools** expose deterministic function execution
6. **Knowledge** provides domain-specific context

The system prioritizes:
- **Workspace > Global** for precedence
- **Progressive disclosure** for context management
- **Constraint immutability** for safety
- **Composability** for complex orchestration

Proper implementation requires understanding the **activation hierarchy**, **relationship constraints**, and **security guardrails** to build robust, maintainable AI-assisted development workflows.

---

## Appendix A: Reference Links

- **Antigravity Documentation**: [Google AI Studio](https://aistudio.google.com)
- **MCP Specification**: [Model Context Protocol](https://modelcontextprotocol.io)
- **Skills Repository**: Community-contributed skills at [GitHub](https://github.com/topics/antigravity-skill)
- **Support**: [Antigravity Community Forums](https://groups.google.com/forum/#!forum/antigravity-users)

---

## Appendix B: Migration from Traditional IDEs

| Traditional IDE Feature | Antigravity Equivalent |
|:------------------------|:-----------------------|
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

**Document Version**: 1.0.0  
**Last Updated**: 2026-01-18  
**Target Platform**: Google Antigravity IDE v1.14.2+  
**Author**: Technical Reference for DDR-Compliant Development