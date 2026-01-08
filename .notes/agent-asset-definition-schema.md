# Antigravity Agent Definition Specification (v1.13+)

This document defines the schema for YAML frontmatter across all Antigravity configuration files. It serves as the authoritative reference for configuring Agents, Rules, Tools, Workflows, Knowledge Bases, and Evaluations.

---

## 1. Agent Definition (`.mdc`)
**Purpose:** Defines the identity, behavior, and capabilities of an autonomous agent persona.
**Location:** `.agent/` or `.antigravity/agents/`

### Properties Schema
1.  **name**
    * **Purpose:** Human-readable display name used in UI lists and headers.
    * **Value:** `String` (Max ~25 chars).
    * **Example:** `"Senior Architect"`
    * **Note:** Keep concise to avoid UI truncation.

2.  **handle**
    * **Purpose:** Unique identifier for summoning/delegation (@mention).
    * **Value:** `String` (Must start with `@`).
    * **Example:** `"@architect"`
    * **Note:** Must be unique across the project scope.

3.  **description**
    * **Purpose:** Summary of the agent's role for the user and Router agent.
    * **Value:** `String` (One sentence).
    * **Example:** `"Expert in system design, scalable patterns, and cloud infrastructure."`
    * **Note:** Used by the orchestrator to recommend agents for specific tasks.

4.  **model**
    * **Purpose:** The specific LLM backend powering this agent.
    * **Value:** `Enum` [`gemini-3-pro-high`, `gemini-3-pro-low`, `gemini-3-flash`, `claude-sonnet-4.5`, `claude-sonnet-4.5-thinking`, `claude-opus-4.5-thinking`, `gpt-oss-120b-medium`].
    * **Example:** `"gemini-3-pro-high"`
    * **Note:** Overrides global IDE model settings. Use high-reasoning models for Architects/QAs.

5.  **temperature**
    * **Purpose:** Controls inference randomness/creativity.
    * **Value:** `Float` [0.0 - 1.0].
    * **Example:** `0.7`
    * **Note:** `0.0` for code/linting; `0.7+` for design/writing.

6.  **color**
    * **Purpose:** Visual accent for UI differentiation (avatar rings/chat bubbles).
    * **Value:** `Hex Code` or `Color Name`.
    * **Example:** `#FF4500`
    * **Note:** Essential for readability in multi-agent chat logs.

7.  **icon**
    * **Purpose:** Avatar icon.
    * **Value:** `Icon Name` (Phosphor/Material) or `Relative Path` (SVG).
    * **Example:** `"strategy"`
    * **Note:** Visual cue for the agent's primary function.

8.  **tools**
    * **Purpose:** Allowlist of executable capabilities.
    * **Value:** `List<String>`.
    * **Example:** `["read_file", "google_search"]`
    * **Note:** Restrict `edit_file` and `run_terminal` for "Advisor" type agents to prevent accidents.

9.  **context_globs**
    * **Purpose:** Files automatically loaded into the context window upon activation.
    * **Value:** `List<Glob Pattern>`.
    * **Example:** `["architecture/*.md"]`
    * **Note:** Use sparingly to preserve token budget.

### Implementation Example (`.mdc`)
```yaml
---
name: "Senior Architect"
handle: "@architect"
description: "Expert in system design, scalable patterns, and cloud infrastructure."
model: gemini-3-pro-high
temperature: 0.7
color: #6A5ACD
icon: strategy
tools:
  - read_file
  - google_search
context_globs:
  - "docs/architecture/**/*.md"
  - "README.md"
---
```

---

## 2. Rule Definition (`.mdr`)
**Purpose:** Defines context-aware constraints or guidelines active during editing.
**Location:** `.agent/rules/`

### Properties Schema
1.  **name**
    * **Purpose:** Display name in the "Active Rules" status bar.
    * **Value:** `String`.
    * **Example:** `"TypeScript Strict Mode"`
    * **Note:** Should clearly indicate the constraint being applied.

2.  **globs**
    * **Purpose:** File patterns that trigger this rule's activation.
    * **Value:** `List<Glob Pattern>`.
    * **Example:** `["**/*.ts", "**/*.tsx"]`
    * **Note:** If omitted, rule is global (use caution).

3.  **priority**
    * **Purpose:** Conflict resolution rank (High overrides Low).
    * **Value:** `Integer`.
    * **Example:** `10`
    * **Note:** Default is 1. Critical safety rules should be >50.

4.  **trigger**
    * **Purpose:** Keywords that activate the rule regardless of file type.
    * **Value:** `List<String>`.
    * **Example:** `["refactor", "debug"]`
    * **Note:** Useful for behavioral rules (e.g., "Always explain changes").

5.  **severity**
    * **Purpose:** Enforcement strictness level.
    * **Value:** `Enum` [`mandatory`, `guideline`, `suggestion`].
    * **Example:** `"mandatory"`
    * **Note:** `mandatory` forces the model to reject requests violating the rule.

6.  **description**
    * **Purpose:** Detailed instruction prompt injected into the system context.
    * **Value:** `String`.
    * **Example:** `"Enforce explicit return types on all exported functions."`
    * **Note:** Be precise; this is the actual "rule" text the LLM reads.

### Implementation Example (`.mdr`)
```yaml
---
name: "TypeScript Strict Mode"
globs:
  - "**/*.ts"
  - "**/*.tsx"
priority: 10
trigger:
  - "type check"
severity: mandatory
description: "All functions must have explicit return type annotations. usage of the 'any' type is strictly forbidden."
---
```

---

## 3. Tool Definition (`.mdt`)
**Purpose:** Defines custom executable scripts or workflows exposed as functions to agents.
**Location:** `.agent/tools/`

### Properties Schema
1.  **name**
    * **Purpose:** The function identifier used by the LLM to call the tool.
    * **Value:** `String` (snake_case).
    * **Example:** `"run_db_migration"`
    * **Note:** Must be unique and descriptive.

2.  **description**
    * **Purpose:** The "Prompt" explaining when/how to use the tool.
    * **Value:** `String`.
    * **Example:** `"Applies pending database schema changes."`
    * **Note:** Critical for proper tool selection by the LLM.

3.  **command**
    * **Purpose:** The shell command to execute.
    * **Value:** `String` (Supports `{{args.x}}` templating).
    * **Example:** `"python manage.py migrate {{args.app}}"`
    * **Note:** Commands run in the project root by default.

4.  **runtime**
    * **Purpose:** The execution environment.
    * **Value:** `Enum` [`system`, `node`, `python`, `docker`].
    * **Example:** `"system"`
    * **Note:** `system` uses the default terminal shell (PowerShell/Bash).

5.  **confirmation**
    * **Purpose:** User permission requirement.
    * **Value:** `Enum` [`always`, `never`].
    * **Example:** `"always"`
    * **Note:** Use `never` only for read-only/safe operations.

6.  **args**
    * **Purpose:** Schema definition for required inputs.
    * **Value:** `Object` (JSON Schema style).
    * **Example:** `{ app: { type: string, required: true } }`
    * **Note:** Define clear descriptions for each argument to prevent hallucinated parameters.

### Implementation Example (`.mdt`)
```yaml
---
name: "generate_migration"
description: "Creates a new Django database migration file. Use when the user requests schema updates."
command: "python manage.py makemigrations {{args.app_label}} --name {{args.migration_name}}"
runtime: system
confirmation: always
args:
  app_label:
    type: string
    description: "Target app name (e.g., 'users')."
    required: true
  migration_name:
    type: string
    description: "Descriptive slug for the change (e.g., 'add_phone_field')."
    required: true
---
```

---

## 4. Workflow Definition (`.mdw`)
**Purpose:** Defines multi-step Standard Operating Procedures (SOPs) orchestrating multiple agents.
**Location:** `.agent/workflows/`

### Properties Schema
1.  **name**
    * **Purpose:** Display title in Command Palette.
    * **Value:** `String`.
    * **Example:** `"Generate Feature Spec"`
    * **Note:** Should be Action-Oriented.

2.  **slug**
    * **Purpose:** Slash command trigger.
    * **Value:** `String` (Starts with `/`).
    * **Example:** `"/spec"`
    * **Note:** Primary manual invocation method.

3.  **description**
    * **Purpose:** Summary for the Router agent.
    * **Value:** `String`.
    * **Example:** `"Converts a user idea into a formal PRD."`
    * **Note:** Helps the AI suggest this workflow during conversation.

4.  **mode**
    * **Purpose:** Autonomy level.
    * **Value:** `Enum` [`interactive`, `autonomous`].
    * **Example:** `"autonomous"`
    * **Note:** `interactive` pauses for user approval after every step.

5.  **inputs**
    * **Purpose:** Variables required from the user before starting.
    * **Value:** `List<Input Object>`.
    * **Input Object Properties:**
      * `name` (Required): Identifier key.
      * `type` (Required): `text`, `string`, `boolean`, `file_path`.
      * `description` (Recommended): Helper text for the UI.
      * `default` (Optional): Initial value.
      * `required` (Optional): `true`/`false` (Default: `true`).
    * **Example:** `[{ name: "idea", type: "text" }]`
    * **Note:** Creates a form UI in Antigravity.

6.  **context**
    * **Purpose:** Resources to preload for the duration of the workflow.
    * **Value:** `List<String>` (Globs or Handles).
    * **Example:** `["@architect", "docs/templates/*.md"]`
    * **Note:** Ensures all agents in the chain have access to the same base data.

7.  **on_finish**
    * **Purpose:** Post-execution action.
    * **Value:** `Action String`.
    * **Example:** `"suggest_followup: /scaffold_code"`
    * **Note:** Chains workflows together.

### Implementation Example (`.mdw`)
```yaml
---
name: "Generate Feature Spec"
slug: /spec
description: "Converts a vague user idea into a formal technical specification document."
mode: autonomous
inputs:
  - name: feature_idea
    type: text
    prompt: "Briefly describe the feature."
  - name: filename
    type: string
    default: "specs/new_feature.md"
context:
  - "@architect"
  - "docs/templates/prd.md"
on_finish: "suggest_followup: /scaffold_code"
---
```

---

## 5. Knowledge Definition (`.mdk`)
**Purpose:** Defines static data sources for RAG (Retrieval Augmented Generation) indexing.
**Location:** `.agent/knowledge/`

### Properties Schema
1.  **name**
    * **Purpose:** Identifier for the knowledge base.
    * **Value:** `String` (snake_case).
    * **Example:** `"stripe_api_docs"`
    * **Note:** Used when querying specific indices.

2.  **sources**
    * **Purpose:** Locations of data to ingest.
    * **Value:** `List<String>` (URLs or File Paths).
    * **Example:** `["https://docs.stripe.com", "./pdfs/*.pdf"]`
    * **Note:** Supports web scraping and local binary reading.

3.  **refresh_schedule**
    * **Purpose:** Re-indexing frequency.
    * **Value:** `Enum` [`always`, `daily`, `weekly`, `manual`].
    * **Example:** `"weekly"`
    * **Note:** `always` runs on every build (expensive).

4.  **strategy**
    * **Purpose:** Text chunking optimization.
    * **Value:** `Enum` [`code`, `prose`, `mixed`].
    * **Example:** `"prose"`
    * **Note:** Use `code` for repos, `prose` for documentation/PDFs.

5.  **access**
    * **Purpose:** Permission scope.
    * **Value:** `List<String>` (Agent Handles) or `Enum` [`public`, `private`].
    * **Example:** `["@architect", "@backend"]`
    * **Note:** Limits token usage by restricting which agents "see" this data.

### Implementation Example (`.mdk`)
```yaml
---
name: "internal_design_system"
description: "Full API reference for the proprietary UI library."
sources:
  - "https://design.internal/components"
  - "./design-tokens/*.json"
refresh_schedule: weekly
strategy: code
access:
  - "@frontend"
  - "@designer"
---
```

---

## 6. Evaluation Definition (`.mde`)
**Purpose:** Defines automated test suites (Evals) to verify Agent behavior and output quality.
**Location:** `.agent/evals/`

### Properties Schema
1.  **name**
    * **Purpose:** Name of the test suite.
    * **Value:** `String`.
    * **Example:** `"Tech Lead Persona Check"`
    * **Note:** Displayed in the Evaluation Dashboard.

2.  **target_agent**
    * **Purpose:** The agent being tested.
    * **Value:** `String` (Handle).
    * **Example:** `"@techlead"`
    * **Note:** The eval runs strictly against this configuration.

3.  **judge_model**
    * **Purpose:** The LLM used to score the output.
    * **Value:** `Enum` [`claude-opus-4.5-thinking`, `gemini-3-pro-high`].
    * **Example:** `"claude-opus-4.5-thinking"`
    * **Note:** Should generally be a stronger model than the target agent.

4.  **pass_threshold**
    * **Purpose:** Minimum score (0-100) to pass.
    * **Value:** `Integer`.
    * **Example:** `90`
    * **Note:** Strict evals should be 90+; creative/subjective ones ~70.

5.  **scenarios**
    * **Purpose:** Input prompts to feed the agent.
    * **Value:** `List<String>`.
    * **Example:** `["Review this code: ..."]`
    * **Note:** Represents the "Test Data".

6.  **rubric**
    * **Purpose:** Criteria the Judge uses to grade the response.
    * **Value:** `List<String>`.
    * **Example:** `["Must identify security flaw", "Tone must be critical"]`
    * **Note:** Each rubric item is weighted in the final score.

### Implementation Example (`.mde`)
```yaml
---
name: "Tech Lead Persona Check"
target_agent: "@techlead"
judge_model: claude-opus-4.5-thinking
pass_threshold: 90
scenarios:
  - "Here is a function with no error handling: def run(): pass"
rubric:
  - "Response must identify the lack of error handling."
  - "Response must NOT start with 'Good job'."
  - "Response tone must be critical and direct."
---
```

---

## Summary of File Types

| Extension | Name | Core Function | Primary YAML Focus |
| :--- | :--- | :--- | :--- |
| **`.mdc`** | Agent Definition | **Identity** | `handle`, `model`, `tools` |
| **`.mdr`** | Rule Definition | **Constraints** | `globs`, `trigger`, `severity` |
| **`.mdt`** | Tool Definition | **Actions** | `command`, `args`, `runtime` |
| **`.mdw`** | Workflow Definition | **Orchestration** | `slug`, `mode`, `inputs` |
| **`.mdk`** | Knowledge Definition | **Memory (RAG)** | `sources`, `strategy`, `access` |
| **`.mde`** | Evaluation Definition | **Quality (QA)** | `target_agent`, `rubric`, `judge_model` |
