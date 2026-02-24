# ANTIGRAVITY v1.18.3 + GEMINI 3.1 PRO — CONSOLIDATED OPTIMIZATION REPORT
<!-- VALIDATION_STATUS: CROSS-VALIDATED | AUDIT_DATE: 2026-02-23 | SCOPE: AG_v1183 + Gemini_3.1_Pro_Preview -->
<!-- SOURCES: 5 constituent AI reports + live source verification against official Google documentation -->

## PART 1 — PLATFORM OVERVIEW

### 1.1 Antigravity IDE v1.18.3

<!-- SOURCE: developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/ -->
<!-- SOURCE: codelabs.developers.google.com/getting-started-google-antigravity -->
<!-- SOURCE: en.wikipedia.org/wiki/Google_Antigravity -->
<!-- SOURCE: google-antigravity.en.uptodown.com/windows (version confirmation) -->
<!-- SOURCE: discuss.ai.google.dev/t/new-version-of-antigravity-same-old-issue (v1.18.3 build metadata) -->

```yaml
platform:
  name: Google Antigravity
  version: 1.18.3
  release_date: 2026-02-19
  vscode_oss_base: 1.107.0
  paradigm: agent-first
  origin: Fork of VS Code / Windsurf acquisition ($2.4B deal)
  availability: Public preview, free for individuals with personal Gmail
  platforms: [Windows 10/11 64-bit, macOS 12+, Linux Ubuntu 20.04+/Debian 10+/Fedora 36+]
  primary_model: gemini-3.1-pro-preview
  supported_models:
    - gemini-3.1-pro-preview
    - gemini-3-flash-preview
    - claude-sonnet-4-5 (Anthropic)
    - gpt-oss-120b (OpenAI open-source variant)
  v1183_changelog_highlights:
    - Gemini 3.1 Pro availability added
    - Models screen in settings (quota visibility)
    - Terminal integration toggle
    - Artifact download from chat UI
    - Agent Skills support introduced
```

### 1.2 Core Surfaces

```yaml
surfaces:
  editor_view:
    description: Familiar VS Code-like IDE surface
    features: [tab completions, inline commands, synchronous coding, agent sidebar]
    mode: synchronous human-driven
  agent_manager:
    description: Mission Control for spawning, monitoring, and orchestrating agents
    features: [multi-agent parallel execution, asynchronous task dispatch, artifact review, inbox tracking]
    mode: asynchronous agent-driven
  browser_subagent:
    description: Integrated browser for visual UI testing and web interaction
    features: [UI verification, dashboard reading, autonomous web navigation]
    browser_allowlist: HOME/.gemini/antigravity/browserAllowlist.txt
```

### 1.3 Execution Modes

```yaml
execution_modes:
  planning_mode:
    description: Agent produces formal IMPLEMENTATION_PLAN.md artifact before writing code
    use_case: Multi-step features, architectural changes, complex refactoring
    artifact_output: [IMPLEMENTATION_PLAN.md, TASK_LIST.md]
    requires_user_approval: true
  fast_mode:
    description: Bypasses task boundaries for immediate localized changes
    use_case: Quick fixes, docstring updates, boilerplate scaffolding
    requires_user_approval: false
terminal_policies:
  always_proceed: Agent auto-executes all terminal commands
  request_review: Agent requests user approval before each terminal command
  agent_decides: Agent decides when to prompt (RECOMMENDED default)
```

---

## PART 2 — MODEL SPECIFICATIONS

### 2.1 Thinking Level Matrix

<!-- SOURCE: ai.google.dev/gemini-api/docs/gemini-3 (updated 2026-02-19) -->
<!-- SOURCE: docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking -->
<!-- SOURCE: ai.google.dev/gemini-api/docs/thought-signatures -->
<!-- SOURCE: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/ -->
<!-- SOURCE: help.apiyi.com/en/gemini-3-1-pro-preview-thinking-level-control-guide-en.html -->

```yaml
models:
  gemini_3_pro:
    api_id: gemini-3-pro
    context_window_tokens: 1_000_000
    max_output_tokens: 64_000
    thinking_levels: [LOW, HIGH]
    default_thinking_level: HIGH
    notes: MEDIUM not supported — applying MEDIUM returns API error
    deprecated_in_antigravity: true  # Deprecated 2026-02-19; replaced by 3.1 Pro Preview

  gemini_3_1_pro_preview:
    api_id: gemini-3.1-pro-preview
    context_window_tokens: 1_000_000
    max_output_tokens: 64_000
    thinking_levels: [LOW, MEDIUM, HIGH]
    default_thinking_level: HIGH
    temperature_default: 1.0
    temperature_note: DO NOT set explicit temperature=0.0 — causes looping/performance degradation on complex tasks
    arc_agi_2_score: 77.1%
    gpqa_diamond_score: 94.3%
    thinking_level_guidance:
      LOW: Simple well-bounded tasks (docstring generation, boilerplate scaffolding)
      MEDIUM: |
        Standard software engineering. Equivalent to Gemini 3 Pro at HIGH.
        Recommended default for Antigravity agentic workflows.
        Reduces TTFT and token expenditure vs HIGH.
      HIGH: |
        Activates Deep Think Mini (encrypted intermediate reasoning chains).
        Reserve for novel algorithm design, multi-repository refactoring,
        complex debugging requiring multi-hop logic.
    api_breaking_change: >
      Field total_reasoning_tokens renamed to total_thought_tokens in Interactions API v1beta.
      Update all codebases referencing the old field name.

  gemini_3_flash_preview:
    api_id: gemini-3-flash-preview
    context_window_tokens: 1_000_000
    max_output_tokens: 64_000
    thinking_levels: [MINIMAL, LOW, MEDIUM, HIGH]
    default_thinking_level: HIGH
    thinking_level_guidance:
      MINIMAL: |
        Fewest thinking tokens. Exclusive to Gemini 3 Flash.
        For repetitive background tasks, bash execution, localized file parsing.
        Still requires thought signature circulation (400 error if absent).
        NOT a general default — only use where reasoning depth provides zero benefit.
      LOW: Moderate judgment tasks, latency-sensitive interactive use
      MEDIUM: Balanced throughput tasks requiring moderate reasoning
      HIGH: Complex Flash tasks requiring full reasoning depth
```

### 2.2 Thought Signature Protocol

<!-- SOURCE: ai.google.dev/gemini-api/docs/thought-signatures -->
<!-- SOURCE: ai.google.dev/gemini-api/docs/gemini-3 -->
<!-- SOURCE: docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking -->
<!-- SOURCE: developers.googleblog.com/new-gemini-api-updates-for-gemini-3/ -->

```yaml
thought_signatures:
  definition: >
    Encrypted, tamper-proof representations of the model's internal reasoning state.
    Must be captured from each API response and re-injected into the next request
    to preserve multi-step reasoning continuity.

  failure_taxonomy:
    function_calling:
      omission_result: HTTP 400 validation error
      severity: HARD FAILURE — pipeline halts immediately
      note: Applies even when thinking_level is MINIMAL for Gemini 3 Flash
    image_generation:
      omission_result: HTTP 400 validation error
      severity: HARD FAILURE — pipeline halts immediately
    text_chat_completions:
      omission_result: Degraded contextual coherence across turns
      severity: SOFT FAILURE — pipeline continues with reduced quality

  sdk_behavior:
    google_genai_python: Automatic circulation when using standard chat history
    google_genai_nodejs: Automatic circulation when using standard chat history
    google_genai_go: Automatic circulation when using standard chat history
    google_genai_java: Automatic circulation when using standard chat history
    raw_rest_api: Manual capture and re-injection required per turn

  gemini_3_vs_gemini_25_behavior:
    gemini_3_function_calling: Signature always present on first functionCall part — MANDATORY to return
    gemini_25_function_calling: Signature on first part — OPTIONAL to return
    gemini_3_text: Signature on last part if model generates thought
    gemini_25_text: No signature on any part

  deep_think_mini_dependency: >
    Thought signatures are the mechanism enabling Deep Think Mini reasoning chains
    to persist across API calls. Omission breaks multi-step agent reasoning state.
```

```python
# Verified thought signature + thinking_level configuration
# Source: ai.google.dev/gemini-api/docs/gemini-3 (2026-02-19)
from google import genai
from google.genai import types

client = genai.Client()

# Gemini 3.1 Pro Preview — MEDIUM for standard engineering tasks
pro_response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents="Refactor the authentication module to use Pydantic v2 strict models.",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.MEDIUM
            # MEDIUM: optimal cost/performance for software engineering
            # Equivalent to Gemini 3 Pro at HIGH
            # Switch to HIGH to activate Deep Think Mini for complex tasks
            # MEDIUM NOT available on Gemini 3 Pro (only LOW/HIGH)
        )
    )
)

# Gemini 3 Flash Preview — MINIMAL for background/validation passes
flash_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Verify ruff and mypy --strict pass on modified files.",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.MINIMAL
            # MINIMAL: fewest thinking tokens — exclusive to Gemini 3 Flash
            # Default for ALL Gemini 3 models is HIGH — must be set explicitly
            # Thought signatures still REQUIRED even at MINIMAL — omission → HTTP 400
        )
    )
)
# SDK automatically circulates thought signatures when using client session or
# appending full model response to chat history.
```

---

## PART 3 — AGENT ASSET FILE TYPES

<!-- SOURCE: codelabs.developers.google.com/getting-started-google-antigravity -->
<!-- SOURCE: codelabs.developers.google.com/getting-started-with-antigravity-skills -->
<!-- SOURCE: github.com/sickn33/antigravity-awesome-skills -->

### 3.1 Asset Tier Classification

```yaml
tier_1_officially_documented:
  description: Confirmed in official Antigravity docs and Google Codelabs — parsed by routing engine
  files:
    - name: GEMINI.md
      locations:
        global: ~/.gemini/GEMINI.md
        workspace: <workspace-root>/GEMINI.md
      scope: Global or Workspace
      parsed_by_routing_engine: true

    - name: SKILL.md
      locations:
        workspace: <workspace-root>/.agent/skills/<skill-name>/SKILL.md
        global: ~/.gemini/antigravity/skills/<skill-name>/SKILL.md
      scope: Workspace or Global
      parsed_by_routing_engine: true
      loading_strategy: progressive_disclosure (loaded only when query matches description)

    - name: RULE_*.md
      locations:
        workspace: <workspace-root>/.agent/rules/
      scope: Workspace
      parsed_by_routing_engine: true
      note: Wildcard naming supports multiple rule files per workspace
      variants: [SECURITY_GUARDRAILS.md, CODE_STYLE.md]

    - name: IMPLEMENTATION_PLAN.md
      locations:
        generated: workspace root or .agent/plans/
      scope: Workspace
      produced_by: Planning Mode
      requires_user_approval_before_execution: true

    - name: TASK_LIST.md
      locations:
        generated: workspace root (paired with IMPLEMENTATION_PLAN.md)
      scope: Workspace
      produced_by: Planning Mode

tier_2_community_convention:
  description: >
    Widely adopted in the Antigravity ecosystem. Not enumerated as named types
    in official Antigravity docs. Treated as standard Markdown context by the
    routing engine; structure enforced by agent convention via GEMINI.md.
  files:
    - name: WORKFLOW_*.md
      locations:
        workspace: <workspace-root>/.agent/workflows/
      scope: Workspace
      invocation: slash-command (/workflow-name)
      note: Community slash-command workflow pattern

    - name: AGENTS.md
      locations:
        workspace: workspace root or .agent/
      scope: Workspace
      note: Community SSoT project constitution pattern
```

---

## PART 4 — SCHEMA DEFINITIONS

### 4.1 GEMINI.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GEMINI_WORKSPACE_CONFIG_V1183",
  "description": "Global or workspace-scoped configuration. Frontmatter parsed by Antigravity routing engine. Body content injected as XML-delimited blocks into context window.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["description", "models", "version", "scope"],
      "properties": {
        "description": { "type": "string" },
        "models": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["gemini-3.1-pro", "gemini-3.1-pro-preview", "gemini-3-pro", "gemini-3-flash"]
          }
        },
        "version": { "type": "string" },
        "scope": { "type": "string", "enum": ["global", "workspace"] },
        "thinking_level": {
          "type": "string",
          "enum": ["minimal", "low", "medium", "high"]
        },
        "temperature": { "type": "number" }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["workspace_context", "cognitive_directives", "security_and_execution_guardrails", "thought_signature_protocol"],
      "properties": {
        "workspace_context": { "type": "string" },
        "cognitive_directives": { "type": "string" },
        "security_and_execution_guardrails": { "type": "string" },
        "thought_signature_protocol": { "type": "string" },
        "activation_rules": { "type": "string" }
      }
    }
  }
}
```

### 4.2 RULE_*.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AGENT_RULE_SCHEMA_V1183",
  "description": "Declarative constraint files enforced by routing engine.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["description", "trigger", "priority"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "trigger": {
          "type": "string",
          "enum": ["auto", "manual", "glob", "always_on", "model_decision", "@mention"]
        },
        "globs": { "type": "string" },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"]
        }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["constraints"],
      "properties": {
        "constraints": { "type": "string" },
        "verification_step": { "type": "string" }
      }
    }
  }
}
```

### 4.3 SKILL.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AGENT_SKILL_SCHEMA_V1183",
  "description": "Reusable capability loaded via progressive disclosure when query matches description trigger.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["description"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["when_to_use", "how_to_use"],
      "properties": {
        "when_to_use": { "type": "string" },
        "how_to_use": { "type": "string" },
        "constraints": { "type": "string" },
        "resources_reference": { "type": "string" }
      }
    }
  }
}
```

### 4.4 WORKFLOW_*.md Schema (Community Convention)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AGENT_WORKFLOW_SCHEMA_V1183",
  "description": "Slash-command-invokable workflow. Community convention.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["description"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["steps"],
      "properties": {
        "steps": { "type": "string" },
        "verification_plan": { "type": "string" }
      }
    }
  }
}
```

### 4.5 AGENTS.md Schema (Community Convention)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AGENTS_CONSTITUTION_SCHEMA_V1183",
  "description": "Project-level SSoT constitution. Community convention. Placed at workspace root or .agent/.",
  "type": "object",
  "required": ["project_identity", "architecture_decisions", "persistent_constraints"],
  "properties": {
    "project_identity": { "type": "string" },
    "architecture_decisions": { "type": "string" },
    "persistent_constraints": { "type": "string" },
    "model_routing": {
      "type": "object",
      "properties": {
        "deep_reasoning_tasks": { "type": "string", "enum": ["gemini-3.1-pro-preview"] },
        "validation_and_background_tasks": { "type": "string", "enum": ["gemini-3-flash-preview"] }
      }
    }
  }
}
```

### 4.6 TASK.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TASK_SCHEMA_V1183",
  "description": "Atomic work units with explicit verification checkpoints.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["task_id", "title", "priority", "target_model"],
      "properties": {
        "task_id": { "type": "string" },
        "title": { "type": "string" },
        "priority": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
        "target_model": { "type": "string", "enum": ["gemini-3.1-pro", "gemini-3-flash"] },
        "task_dependencies": { "type": "array", "items": { "type": "string" } },
        "file_dependencies": { "type": "array", "items": { "type": "string" } }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["expected_output", "pre_check", "acceptance_criteria", "rollback_procedure"],
      "properties": {
        "expected_output": { "type": "string" },
        "constraints": { "type": "string" },
        "pre_check": { "type": "string" },
        "acceptance_criteria": { "type": "array", "items": { "type": "string" } },
        "rollback_procedure": { "type": "string" }
      }
    }
  }
}
```

### 4.7 IMPLEMENTATION_PLAN.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "IMPLEMENTATION_PLAN_SCHEMA_V1183",
  "description": "Agent-generated planning artifact. Requires user review and approval before execution.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["task", "model"],
      "properties": {
        "task": { "type": "string" },
        "model": { "type": "string", "enum": ["gemini-3.1-pro", "gemini-3.1-pro-preview"] }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["objective", "atomic_steps", "verification"],
      "properties": {
        "objective": { "type": "string" },
        "phases": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "phase_id": { "type": "string" },
              "objectives": { "type": "array", "items": { "type": "string" } },
              "task_references": { "type": "array", "items": { "type": "string" } },
              "entry_criteria": { "type": "array", "items": { "type": "string" } },
              "exit_criteria": { "type": "array", "items": { "type": "string" } },
              "assigned_model": { "type": "string", "enum": ["gemini-3.1-pro", "gemini-3-flash"] }
            }
          }
        },
        "atomic_steps": { "type": "array", "items": { "type": "string" } },
        "verification": { "type": "array", "items": { "type": "string" } },
        "risks_and_mitigations": { "type": "string" }
      }
    }
  }
}
```

### 4.8 SECURITY_GUARDRAILS.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SECURITY_GUARDRAILS_SCHEMA_V1183",
  "description": "Specialized RULE_*.md variant for security enforcement.",
  "type": "object",
  "required": ["frontmatter", "body_content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["name", "description", "trigger", "priority"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "trigger": { "type": "string", "enum": ["always_on"] },
        "priority": { "type": "string", "enum": ["critical"] }
      }
    },
    "body_content": {
      "type": "object",
      "required": ["forbidden_actions", "allowed_domains", "verification_step"],
      "properties": {
        "forbidden_actions": { "type": "array", "items": { "type": "string" } },
        "allowed_domains": { "type": "array", "items": { "type": "string" } },
        "verification_step": { "type": "string" }
      }
    }
  }
}

### 4.9 WALKTHROUGH.md Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WALKTHROUGH_SCHEMA_V1183",
  "description": "Post-execution summary and manual verification guide. No frontmatter required.",
  "type": "object",
  "required": ["body_content"],
  "properties": {
    "body_content": {
      "type": "object",
      "required": ["execution_summary", "architectural_changes", "verification_steps"],
      "properties": {
        "execution_summary": { "type": "string" },
        "architectural_changes": { "type": "string" },
        "verification_steps": { "type": "string" }
      }
    }
  }
}
```

---

## PART 5 — COMPLETE ASSET IMPLEMENTATION EXAMPLES

### 5.1 GEMINI.md

```markdown
---
description: "Primary configuration for the Maggie application workspace and DDR System integration."
models: ["gemini-3.1-pro-preview", "gemini-3.1-pro", "gemini-3-flash"]
version: "20260223_v118"
scope: "workspace"
thinking_level: "medium"
temperature: 0.1
---

<workspace_context>
This workspace is dedicated to the development of Maggie, a modern desktop application, and its integration with the DDR System (an agentic documentation architecture).

- **Core Stack:** Python 3.12, PySide6 (Qt 6.9+).
- **Architecture:** The application relies on non-blocking, asynchronous event loops. UI layouts are responsive, utilizing dynamic QGridLayout and QThreadPool for background tasks.
- **Design Language:** All UI elements must adhere to cross-platform Material You 3 paradigms, utilizing native SVG icons for lossless scaling.
- **Agentic Infrastructure:** The DDR System heavily relies on structured schema generation, strict adherence to implementation plans, and atomic verification.
</workspace_context>

<cognitive_directives>

- **Silent Reasoning:** You must perform all complex architectural planning internally. Do not output your intermediate reasoning steps or "Chain of Thought" tokens to the user unless explicitly commanded via `/think`.
- **Output Determinism:** Produce production-ready code. The use of placeholders, elided code (e.g., `# TODO: implement`), or "dummy" variables is strictly prohibited.
- **Artifact Generation:** Always utilize the `Implementation_Plan.md` and `Task.md` schemas to organize multi-file modifications before altering the Maggie codebase.
</cognitive_directives>

<security_and_execution_guardrails>

- Do not execute arbitrary shell commands or modify files outside of the `src/` or `.agent/` directories without an approved execution artifact.
- All network interactions must be limited to official documentation domains (e.g., `doc.qt.io`, `docs.python.org`).
</security_and_execution_guardrails>

<thought_signature_protocol>
You operate within a stateless API session. You will receive encrypted thought signatures representing your internal planning and reasoning state from previous turns. You MUST circulate all received thought signatures back into your subsequent turns without modification or truncation to prevent catastrophic context loss across multi-turn API calls.
</thought_signature_protocol>

<activation_rules>

- always-on
</activation_rules>
```

### 5.2 RULE_CODE_STYLE.md

```markdown
---
name: strict-python-architecture
description: Enforces deterministic type safety, non-blocking asynchronous I/O patterns, and explicit exception handling for all Python modules.
trigger: glob
globs: "*.py, src/**/*.py, scripts/**/*.py"
priority: critical
---

<constraints>
- **Type Safety Mandate:** All function signatures, including internal helpers and class methods, must have comprehensive type hints. Explicitly type `*args` and `**kwargs`. The use of implicit `Any` is prohibited.
- **Concurrency Protocol:** Do not use blocking synchronous libraries (e.g., `requests`, `time.sleep`) inside asynchronous event loops. You must utilize their asynchronous equivalents (e.g., `aiohttp`, `asyncio.sleep`).
- **Exception Handling:** Bare `except:` or `except Exception:` blocks are strictly prohibited. You must catch explicitly anticipated exception classes (e.g., `KeyError`, `aiohttp.ClientError`) and implement deterministic logging.
- **Data Validation:** All incoming external payloads or API responses must be parsed through `pydantic` BaseModel classes rather than raw dictionary manipulation.
- **No Elided Code:** Never generate placeholder comments like `# TODO: implement logic`. All emitted code must be production-ready, complete, and contextually aware of the surrounding implementation.
</constraints>

<verification_step>
SILENT VERIFICATION INSTRUCTIONS:
Before emitting the final codebase modification, you must internally evaluate your generated code against the following matrix:

1. Scan all newly generated `def` and `async def` statements to confirm complete and accurate type annotations.
2. Check the AST logic for any blocking I/O calls mistakenly placed within `async` blocks.
3. Verify that all `try/except` blocks target specific, named error classes.
4. Ensure no placeholder code or "dummy" variables have been utilized.

If any check fails, silently regenerate the code to correct the violation before finalizing the output artifact. Do not output your reasoning process or these validation steps to the user.
</verification_step>
```

### 5.3 SKILL.md (generate-pyside6-ui-widget)

```markdown
---
name: generate-pyside6-ui-widget
description: Generates a complete, responsive PySide6 widget or layout component, integrating native SVG rendering, specifically architected for the Maggie software application.
---

<when_to_use>

- The developer requests the creation, refactoring, or modernization of a user interface element.
- The prompt contains keywords such as: "widget", "PySide6", "UI", "layout", or "interface".
- The active task involves building visual components for the Maggie application frontend.
</when_to_use>

<how_to_use>

1. **Context Verification (Silent):** Confirm the required PySide6 modules (e.g., `QtWidgets`, `QtGui`, `QtSvg`) are available in the workspace context.
2. **Design Blueprinting (Silent):** Plan the widget hierarchy, prioritizing non-blocking UI patterns and responsive layouts (e.g., `QVBoxLayout`, `QGridLayout`).
3. **Asset Integration:** If icons or vector graphics are required, strictly utilize SVG formats rendered via `QSvgWidget` or `QIcon` to ensure lossless scaling across different monitor resolutions and maintain the application's visual fidelity.
4. **Code Generation:** Emit the production-ready Python code within a fenced code block. Ensure all classes inherit from the appropriate PySide6 base classes and include comprehensive type hints.
5. **Verification Artifact:** Output a brief, Markdown-formatted summary of the signals and slots implemented for the developer to review and approve.
</how_to_use>

<constraints>
- Never utilize synchronous blocking calls (e.g., `time.sleep()`) within the main GUI thread; you must rely on `QThread` or `QTimer` for asynchronous operations to keep the Maggie UI responsive.
- Do not hardcode absolute pixel dimensions; utilize dynamic sizing, spacers, and stretch factors.
- All emitted code must be fully type-hinted and production-ready. Do not generate placeholder logic.
</constraints>

<resources_reference>

- `ui_templates/maggie_base_widget.py`
- `assets/svg_icons/`
</resources_reference>
```

### 5.4 WORKFLOW_IMPLEMENT.md (strict-integration-deploy)

```markdown
---
name: strict-integration-deploy
description: Orchestrates a highly deterministic deployment pipeline involving static analysis, artifact generation, testing, and conditional merging using Gemini 3.1 Pro.
---

### steps

1. **Context Assimilation & Artifact Creation:** Analyze the staged modifications in the active workspace. Generate a summary document named `Pre_Deployment_Audit.md` detailing all detected changes, affected dependencies, and potential breaking points.
2. **Review Checkpoint:** Pause execution. **Request explicit human approval** of `Pre_Deployment_Audit.md` before proceeding to automated validation.
3. **Static Analysis & Skill Trigger:** Execute the workspace linter and type-checker.
    - If errors are detected, invoke semantic routing for diagnostic and debugging skills to resolve type conflicts automatically, then regenerate the audit artifact.
    - If no errors are detected, proceed to Step 4.
4. **Test Suite Execution (Decision Tree):** Run the comprehensive integration test suite. Use the following decision matrix to handle the output:
    - **IF** the test suite returns a 100% pass rate, **THEN** proceed to Step 5.
    - **IF** the test suite fails on newly implemented logic, **THEN** halt the workflow, capture the failure logs into `Error_Trace.md`, and notify the user.
    - **IF** the test suite fails on legacy, unmodified logic (regression), **THEN** immediately revert the staged changes and request human intervention.
5. **Codebase Modification:** Once tests pass, update the `CHANGELOG.md` artifact to reflect the verified modifications, adhering strictly to the required formatting guidelines.
    <changelog_constraints>
    - Group changes by type: Added, Changed, Deprecated, Removed, Fixed, Security.
    - Use imperative mood in all bullet points (e.g., "Add new endpoint", not "Added new endpoint").
    - Do not reference internal issue tracker IDs unless explicitly provided in the user prompt.
    </changelog_constraints>
6. **Final Verification:** Perform a final dry-run of the build process. Output the terminal build results as a final verifiable artifact to conclude the workflow.

### verification_plan

- The `Pre_Deployment_Audit.md` artifact must exist and be approved prior to any testing.
- The `CHANGELOG.md` artifact modification must strictly adhere to the XML-fenced `<changelog_constraints>`.
- The workflow must terminate deterministically based on the decision tree if any test regressions occur.
```

### 5.5 AGENTS.md (Community Convention)

```markdown
# PROJECT CONSTITUTION

<project_identity>
Tech stack: Python 3.12, PySide6, Pydantic v2, pytest, ruff, mypy --strict, asyncio.
Target platforms: Windows, macOS, Linux.
</project_identity>

<architecture_decisions>
- UI: PySide6 with QML. No tkinter. No wx.
- Data: Pydantic v2 strict models. No dataclasses for domain objects.
- Concurrency: asyncio + QThreadPool. No blocking calls on main thread.
- Auth: bcrypt + PyJWT. No plain-text credential storage.
- Testing: pytest only. 90%+ coverage enforced.
</architecture_decisions>

<persistent_constraints>
- All code must pass ruff --select=E,F,W and mypy --strict before commit.
- No external network calls outside approved domains.
- No credentials in version-controlled files.
- Every feature requires IMPLEMENTATION_PLAN.md with user approval before execution.
</persistent_constraints>

<model_routing>
deep_reasoning_tasks: gemini-3.1-pro-preview
thinking_level_pro: MEDIUM
validation_and_background_tasks: gemini-3-flash-preview
thinking_level_flash: MINIMAL
</model_routing>
```

### 5.6 SECURITY_GUARDRAILS.md (global-security-guardrails)

```markdown
---
name: global-security-guardrails
description: Enforces absolute security boundaries, network access restrictions, and credential protection protocols across all agentic workflows.
trigger: always_on
priority: critical
---

<forbidden_actions>

- **Credential Exposure:** Never generate, log, or embed hardcoded passwords, API keys, or access tokens within source code, test files, or artifact outputs.
- **Destructive Operations:** Do not utilize `os.system()`, `subprocess.run()`, or `shutil.rmtree()` to execute unverified shell commands or delete directories without explicit user confirmation via an artifact.
- **Data Exfiltration:** Do not write scripts that transmit local workspace data or environment variables to external telemetry or logging servers.
</forbidden_actions>

<allowed_domains>
If a workflow or skill requires documentation retrieval or API integration, you are strictly limited to the following whitelisted domains:

- `*.qt.io`
- `docs.python.org`
- `*.google.com`
- `github.com`
</allowed_domains>

<verification_step>
SILENT SECURITY AUDIT:
Before finalizing any code modification or terminal execution, you must internally parse your generated output against the `<forbidden_actions>` list. If any network requests are formulated, verify the target URL matches the `<allowed_domains>` regex exactly. If a violation is detected, you must silently purge the output and halt the workflow.
</verification_step>
```

### 5.7 WALKTHROUGH.md

```markdown
<execution_summary>
The PySide6 asynchronous worker integration for the Maggie application has been successfully completed. The implementation decouples heavy data processing from the main event loop, ensuring the UI remains highly responsive during extended operations.
</execution_summary>

<architectural_changes>

- **Created:** `src/core/worker.py` - Contains the `QRunnable` architecture and custom signal definitions.
- **Modified:** `src/ui/main_window.py` - Instantiated `QThreadPool.globalInstance()` and connected the worker's `result` signal to the UI update slots.
- **Dependencies:** No external `pip` dependencies were added.
</architectural_changes>

<verification_steps>
To verify the implementation meets the required specifications, please perform the following actions:

1. Open the Antigravity Terminal and ensure your virtual environment is active.
2. Execute the application using: `python -m src.main`
3. Click the "Fetch Data" button on the Maggie dashboard.
4. Attempt to resize the application window while the data is fetching.
   - **Expected Result:** The window should resize smoothly without stuttering, and the fetched data should populate the table once the background thread emits the `result` signal.
</verification_steps>
```

### 5.8 IMPLEMENTATION_PLAN.md

```markdown
---
task: "Architect and implement the main dashboard layout for Maggie"
model: "gemini-3.1-pro"
---

<objective>
Construct the primary PySide6 dashboard interface for the Maggie application, establishing a non-blocking UI architecture utilizing QGridLayout and dynamic widget loading.
</objective>

<phases>
- phase_id: "PHASE_1_UI_SCAFFOLD"
  objectives: ["Establish base QMainWindow", "Configure QGridLayout for dynamic resizing"]
  task_references: ["TASK-MAGGIE-001", "TASK-MAGGIE-002"]
  entry_criteria: ["PySide6 environment verified"]
  exit_criteria: ["Base window renders without errors"]
  assigned_model: "gemini-3.1-pro"
- phase_id: "PHASE_2_ASYNC_WORKERS"
  objectives: ["Implement QThreadPool for background data fetching"]
  task_references: ["TASK-MAGGIE-003"]
  entry_criteria: ["PHASE_1_UI_SCAFFOLD complete"]
  exit_criteria: ["Background tasks update UI without blocking the main event loop"]
  assigned_model: "gemini-3-flash"
</phases>

<atomic_steps>

1. Generate `src/ui/main_window.py` containing the `MaggieDashboard` class inheriting from `QMainWindow`.
2. Implement `setup_ui()` to instantiate a responsive `QGridLayout`.
3. Create `src/core/worker.py` to subclass `QRunnable` for asynchronous event handling.
4. Bind signals from the worker to slots in `MaggieDashboard` to update UI elements safely.
</atomic_steps>

<verification>
1. Verify `main_window.py` contains valid PySide6 imports and no syntax errors.
2. Verify grid layout parameters scale correctly during window resize events.
3. Verify `QRunnable` instances successfully execute external bound methods.
4. Verify signal emission triggers UI updates without raising `QThread` cross-thread violation exceptions.
</verification>

<risks_and_mitigations>

- **Risk:** Cross-thread UI updates causing application crashes.
  **Mitigation:** Strictly enforce the use of Qt Signals and Slots for all data passed from background threads to the main GUI thread.
</risks_and_mitigations>
```

### 5.9 TASK.md

```markdown
---
task_id: "TASK-MAGGIE-003"
title: "Implement QThreadPool for background data fetching"
priority: "high"
target_model: "gemini-3-flash"
task_dependencies: ["TASK-MAGGIE-001"]
file_dependencies: ["src/ui/main_window.py"]
---

<expected_output>
A fully functional `src/core/worker.py` module containing a `QRunnable` subclass and a custom `QObject` signal class.
</expected_output>

<constraints>
- Use `logging` instead of `print()` statements for all background thread monitoring.
- Do not modify `src/ui/main_window.py` during this task; only establish the core worker logic.
</constraints>

<pre_check>
Verify that `PySide6` is actively installed in the current virtual environment and that `src/ui/main_window.py` exists as declared in the file dependencies.
</pre_check>

<acceptance_criteria>

- The `WorkerSignals` class defines at least `finished`, `error`, and `result` signals.
- The `Worker` class successfully inherits from `QRunnable` and implements the `@Slot()` decorator on its `run()` method.
- The file passes `ruff` static analysis without formatting errors.
</acceptance_criteria>

<rollback_procedure>
If `ruff` validation fails or syntax errors are detected, delete the newly created `src/core/worker.py` file, log the specific syntax failure, and halt the workflow to await human intervention.
</rollback_procedure>
```

---

## PART 6 — OPTIMIZATION PRINCIPLES

<!-- COMPOSITE SYNTHESIS: All 5 constituent reports + live source validation -->

```yaml
optimization_principles:

  context_first_placement:
    rule: Inject heavy technical context (schemas, whitelists, prior artifacts) at prompt HEAD
    rationale: Leverages terminal attention weighting in long-context windows
    implementation: workspace_context block appears first in GEMINI.md body

  silent_reasoning:
    rule: Suppress chain-of-thought output; deliver only structured final responses
    implementation: cognitive_directives block in GEMINI.md

  atomic_decomposition:
    rule: Each task step carries exactly one responsibility and one verification condition
    anti_pattern: Multi-responsibility step bundling

  structured_schema_enforcement:
    rule: All outputs validated against JSON schema before emission
    tools: [Pydantic v2, mypy --strict]

  explicit_verification_stage:
    phases: [pre_check (before generation), acceptance_criteria (after), rollback_procedure (on failure)]

  whitelist_grounding:
    rule: RAG pipelines restricted to authoritative domain allowlists
    enforcement: SECURITY_GUARDRAILS.md (always-on)

  model_routing:
    deep_reasoning: gemini-3.1-pro-preview (thinking_level MEDIUM)
    validation_background: gemini-3-flash-preview (thinking_level MINIMAL)
    rule: Never mix roles within a single pipeline stage

  thinking_level_management:
    parameter: thinking_level (replaces deprecated thinking_budget from Gemini 2.5)
    default_all_gemini_3_models: HIGH
    recommended_pro_engineering: MEDIUM
    recommended_flash_background: MINIMAL
    activation_deep_think_mini: thinking_level HIGH on gemini-3.1-pro-preview

  thought_signature_circulation:
    rule: ALWAYS circulate in multi-turn API calls
    hard_failure_scope: [function_calling, image_generation]
    soft_failure_scope: [text_completions, chat]
    sdk_automation: google-genai SDK handles automatically

  temperature_configuration:
    rule: DO NOT set explicit temperature on Gemini 3 models
    default: 1.0 (Gemini 3 series default)
    anti_pattern: temperature=0.0 causes looping and performance degradation

  planning_mode_enforcement:
    rule: All multi-step features require IMPLEMENTATION_PLAN.md with user approval before execution
    assets: [IMPLEMENTATION_PLAN.md, TASK_LIST.md]
```

---

## PART 7 — AGENTIC PIPELINE PATTERN

```
STAGE 1: Context Injection
  → GEMINI.md + AGENTS.md + whitelists injected at prompt HEAD
  → thinking_level: MEDIUM (gemini-3.1-pro-preview)

STAGE 2: Atomic Planning
  → SKILL.md (atomic-implementation-planner) invoked
  → IMPLEMENTATION_PLAN.md artifact produced
  → User review and approval REQUIRED before proceeding

STAGE 3: Thought Signature Initialization
  → Captured from first API response
  → Circulated in ALL subsequent calls (SDK automates; raw REST requires manual handling)

STAGE 4: Deterministic Generation
  → TASK_LIST.md entries executed per target_model + thinking_level assignment
  → gemini-3.1-pro-preview (MEDIUM): architecture, coding tasks
  → gemini-3-flash-preview (MINIMAL): validation, linting, background parsing

STAGE 5: Schema Validation
  → gemini-3-flash-preview (MINIMAL) — silent ruff + mypy --strict pass
  → No auto-fix — failures reported as structured JSON to user

STAGE 6: Security Enforcement
  → SECURITY_GUARDRAILS.md (always-on, overrides all other directives)
  → SECURITY_REVIEW artifact emitted if triggered; user approval required

STAGE 7: Output Finalization
  → Structured Markdown artifact → user review
  → Artifacts downloadable from chat UI (v1.18.3 feature)
```

---

## PART 8 — WHITELIST REGISTRY

### 8.1 Antigravity + Gemini Core

```json
{
  "WHITELIST_ID": "AG_CORE_V1183",
  "PRIORITY_RULE": "GROUP_MATCH > GOOGLE_OFFICIAL > CHANGELOG_RECENCY",
  "ANTIGRAVITY_CORE": [
    "https://antigravity.google/",
    "https://antigravity.google/docs/home",
    "https://antigravity.google/docs/agent",
    "https://antigravity.google/docs/skills",
    "https://antigravity.google/docs/rules-workflows",
    "https://antigravity.google/docs/implementation-plan",
    "https://antigravity.google/changelog",
    "https://codelabs.developers.google.com/getting-started-google-antigravity",
    "https://codelabs.developers.google.com/getting-started-with-antigravity-skills",
    "https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/"
  ],
  "GEMINI_3_SERIES": [
    "https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview",
    "https://ai.google.dev/gemini-api/docs/gemini-3",
    "https://ai.google.dev/gemini-api/docs/thinking",
    "https://ai.google.dev/gemini-api/docs/thought-signatures",
    "https://ai.google.dev/gemini-api/docs/changelog",
    "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro",
    "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-flash",
    "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking",
    "https://deepmind.google/models/model-cards/gemini-3-1-pro/",
    "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/",
    "https://developers.googleblog.com/new-gemini-api-updates-for-gemini-3/"
  ],
  "AGENT_DEVELOPMENT_KIT": [
    "https://google.github.io/adk-docs/",
    "https://google.github.io/adk-docs/agents/",
    "https://github.com/google/adk-python"
  ]
}
```

### 8.2 Python Engineering

```json
{
  "WHITELIST_ID": "PYTHON_ENGINEERING_V1183",
  "PYTHON_CORE": ["https://docs.python.org/3/", "https://peps.python.org/"],
  "TYPING_STATIC_ANALYSIS": [
    "https://mypy.readthedocs.io/",
    "https://typing.readthedocs.io/",
    "https://docs.pydantic.dev/latest/"
  ],
  "ASYNC_CONCURRENCY": [
    "https://docs.python.org/3/library/asyncio.html",
    "https://anyio.readthedocs.io/"
  ],
  "TESTING": ["https://docs.pytest.org/", "https://hypothesis.readthedocs.io/"]
}
```

### 8.3 PySide6 / Qt6

```json
{
  "WHITELIST_ID": "PYSIDE6_V1183",
  "note": "Verify current stable PySide6 version at https://pypi.org/project/PySide6/ before pinning",
  "QT_FOR_PYTHON_OFFICIAL": [
    "https://doc.qt.io/qtforpython-6/",
    "https://doc.qt.io/qt-6/",
    "https://wiki.qt.io/Qt_for_Python",
    "https://pypi.org/project/PySide6/"
  ],
  "QT_DESIGN_PATTERNS": [
    "https://doc.qt.io/qt-6/model-view-programming.html",
    "https://doc.qt.io/qt-6/signalsandslots.html",
    "https://doc.qt.io/qt-6/qthreadpool.html"
  ],
  "QML_AND_UI": [
    "https://doc.qt.io/qt-6/qmlapplications.html",
    "https://doc.qt.io/qt-6/qt6-qmlbook.html"
  ]
}
```

### 8.4 GUI / UX Design

```json
{
  "WHITELIST_ID": "GUI_UX_DESIGN_V1183",
  "GOOGLE_DESIGN": ["https://m3.material.io/", "https://material.io/design"],
  "ACCESSIBILITY": ["https://www.w3.org/WAI/", "https://www.w3.org/TR/WCAG21/"],
  "CROSS_PLATFORM_HIG": [
    "https://developer.apple.com/design/human-interface-guidelines/",
    "https://learn.microsoft.com/en-us/windows/apps/design/"
  ]
}
```

### 8.5 Security Engineering

```json
{
  "WHITELIST_ID": "SECURITY_ENGINEERING_V1183",
  "OWASP": ["https://owasp.org/", "https://cheatsheetseries.owasp.org/"],
  "NIST": ["https://csrc.nist.gov/", "https://nvlpubs.nist.gov/"],
  "GOOGLE_SECURITY": ["https://cloud.google.com/security"]
}
```

---

## PART 9 — VALIDATION AUDIT LOG

```yaml
audit_results:

  A1_platform_version:
    claim: Antigravity v1.18.3 released 2026-02-19
    status: CONFIRMED
    source: google-antigravity.en.uptodown.com, discuss.ai.google.dev (build metadata), github.com/jacopone/antigravity-nix/releases

  A2_model_id_gemini_3_1_pro_preview:
    claim: API model ID is gemini-3.1-pro-preview
    status: CONFIRMED
    source: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/

  A3_model_id_gemini_3_flash_preview:
    claim: API model ID is gemini-3-flash-preview
    status: CONFIRMED
    source: docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-flash

  A4_thinking_level_medium_exclusive_to_3_1:
    claim: MEDIUM thinking_level is available only on 3.1 Pro Preview, not Gemini 3 Pro
    status: CONFIRMED
    source: ai.google.dev/gemini-api/docs/gemini-3; help.apiyi.com/en/gemini-3-1-pro-preview-thinking-level-control-guide-en.html
    note: Applying MEDIUM to Gemini 3 Pro (not 3.1) causes API error

  A5_thinking_level_minimal_exclusive_to_flash:
    claim: MINIMAL thinking_level is exclusive to Gemini 3 Flash
    status: CONFIRMED
    source: docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking

  A6_thought_signatures_400_on_function_calling:
    claim: Omitting thought signatures in function calling returns HTTP 400
    status: CONFIRMED
    source: ai.google.dev/gemini-api/docs/thought-signatures; ai.google.dev/gemini-api/docs/gemini-3

  A7_thought_signatures_minimal_still_required:
    claim: Thought signatures required even when thinking_level is MINIMAL for Gemini 3 Flash
    status: CONFIRMED
    source: docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking
    quote_under_15_words: "required even when thinking level is set to minimal"

  A8_sdk_auto_circulation:
    claim: google-genai SDK (Python/Node/Go/Java) auto-circulates thought signatures
    status: CONFIRMED
    source: ai.google.dev/gemini-api/docs/thought-signatures; developers.googleblog.com/new-gemini-api-updates-for-gemini-3/

  A9_temperature_default_1_0:
    claim: Gemini 3 default temperature is 1.0; explicit temperature=0.0 not recommended
    status: CONFIRMED
    source: ai.google.dev/gemini-api/docs/gemini-3 (migration guidance section)

  A10_skill_locations:
    claim: SKILL.md locations are ~/.gemini/antigravity/skills/ (global) and .agent/skills/ (workspace)
    status: CONFIRMED
    source: codelabs.developers.google.com/getting-started-with-antigravity-skills; codelabs.developers.google.com/getting-started-google-antigravity

  A11_workflow_community_convention:
    claim: WORKFLOW_*.md is community convention, not officially enumerated in Antigravity docs
    status: CONFIRMED via absence
    source: Official Antigravity codelabs document GEMINI.md, SKILL.md, RULE_*.md, artifacts — WORKFLOW_*.md not enumerated

  A12_deep_think_mini:
    claim: thinking_level HIGH on Gemini 3.1 Pro Preview activates Deep Think Mini
    status: CONFIRMED
    source: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/; help.apiyi.com

  A13_gemini_3_pro_deprecated_in_antigravity:
    claim: Gemini 3 Pro deprecated in Antigravity as of v1.18.3; replaced by Gemini 3.1 Pro Preview
    status: CONFIRMED
    source: blog.ni18.in/fix-gemini-3-pro-no-longer-available-in-antigravity/ (corroborated by forum reports)

  A14_constituent_report_discrepancy_temperature:
    claim: Original reports recommended temperature=0.0 for code generation
    status: INCORRECT — CORRECTED
    correction: Gemini 3 default temperature is 1.0; explicit temperature=0.0 causes looping on complex tasks
    source: ai.google.dev/gemini-api/docs/gemini-3

  A15_api_field_rename:
    claim: total_reasoning_tokens renamed to total_thought_tokens in Interactions API v1beta
    status: CONFIRMED
    source: marktechpost.com/2026/02/19/ (corroborated by official API changelog)
```

---

## PART 10 — AUTHORITATIVE SOURCE REGISTRY

```yaml
primary_sources:
  antigravity:
    - url: https://antigravity.google/
    - url: https://antigravity.google/docs/home
    - url: https://antigravity.google/docs/agent
    - url: https://antigravity.google/docs/skills
    - url: https://antigravity.google/docs/rules-workflows
    - url: https://antigravity.google/docs/implementation-plan
    - url: https://antigravity.google/changelog
    - url: https://codelabs.developers.google.com/getting-started-google-antigravity
    - url: https://codelabs.developers.google.com/getting-started-with-antigravity-skills
    - url: https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/

  gemini_3_series:
    - url: https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview
    - url: https://ai.google.dev/gemini-api/docs/gemini-3
    - url: https://ai.google.dev/gemini-api/docs/thinking
    - url: https://ai.google.dev/gemini-api/docs/thought-signatures
    - url: https://ai.google.dev/gemini-api/docs/changelog
    - url: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro
    - url: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-flash
    - url: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking
    - url: https://deepmind.google/models/model-cards/gemini-3-1-pro/
    - url: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/
    - url: https://developers.googleblog.com/new-gemini-api-updates-for-gemini-3/

  agent_development_kit:
    - url: https://google.github.io/adk-docs/
    - url: https://google.github.io/adk-docs/agents/
    - url: https://github.com/google/adk-python

  python_engineering:
    - url: https://docs.python.org/3/
    - url: https://peps.python.org/
    - url: https://mypy.readthedocs.io/
    - url: https://docs.pydantic.dev/latest/
    - url: https://docs.pytest.org/

  pyside6_qt:
    - url: https://doc.qt.io/qtforpython-6/
    - url: https://doc.qt.io/qt-6/
    - url: https://pypi.org/project/PySide6/
    - url: https://wiki.qt.io/Qt_for_Python

  gui_accessibility:
    - url: https://m3.material.io/
    - url: https://www.w3.org/WAI/
    - url: https://www.w3.org/TR/WCAG21/

  security:
    - url: https://owasp.org/
    - url: https://cheatsheetseries.owasp.org/
    - url: https://csrc.nist.gov/
```

---

<!-- END: AG_CONSOLIDATED_REPORT_V1183_20260223 -->
<!-- VALIDATION_COMPLETE: 15 audit items | 14 CONFIRMED | 1 CORRECTED (A14: temperature) -->
<!-- SCOPE_ENFORCED: Antigravity v1.18.3 + Gemini 3.1 Pro Preview only -->
