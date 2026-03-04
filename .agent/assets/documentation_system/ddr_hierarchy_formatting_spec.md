# Documentation System Proposal Formatting Specification

**Version:** 1.1
**Last Updated:** 2026-01-15
**Reference Documents:**

- `.agent\assets\proposals\future\documentation_system\27. Antigravity Agent Asset Definition Files.md` (Formatting)
- `.agent\schemas\` (Modular Schema Definitions, v1.18.3)

---

## 1. Purpose

This specification defines the formatting rules for the Documentation System Proposal files. It serves as an authoritative ruleset for AI agents to:

1. **Validate** existing file formatting compliance
2. **Transform** files from previous formatting structures to the current standard
3. **Author** new documentation content with consistent styling

---

## 2. Code Block Hierarchy

### 2.1 Parent Code Blocks (Outer-Most)

**Rule:** All outer-most code blocks MUST use **tilde fencing** (`~~~`) with a specified content type.

**Syntax:**

~~~plaintext
<content>
~~~

**Supported Content Types:**

| Content Type | Purpose                                                     |
| :----------- | :---------------------------------------------------------- |
| `markdown`   | Skill, Rule, Workflow, and other agent asset definitions    |
| `yaml`       | YAML configuration files (when content is pure YAML)        |
| `rst`        | reStructuredText documentation examples                     |
| `plaintext`  | Conversational transcripts, terminal output, reports        |

**Example — Rule Definition:**

```
  ~~~markdown
  ---
  name: "Example Rule"
  description: "Example Rule description."
  trigger: "glob"
  globs: "docs/**/*.rst"
  priority: "medium"
  ---

# Rule: Example Rule

## Enforcement Protocol

  Content here...
  ~~~
```

----------

### 2.2 Child Code Blocks (Inner/Embedded)

**Rule:** Code blocks nested WITHIN a parent (tilde-fenced) block MUST use **triple backticks** (` ``` `) with a specified content type.

**Syntax:**

```
  ~~~markdown
    ```plaintext
      <embedded_content>
    ```
  ~~~
```

**Common Child Content Types:**

| Content Type | Purpose                                            |
| :----------- | :------------------------------------------------- |
| `rst`        | reStructuredText directive examples                |
| `python`     | Python code examples or algorithms                 |
| `json`       | JSON schema or output examples                     |
| `mermaid`    | Mermaid diagram syntax                             |
| `plaintext`  | Plain text examples, pseudo-code, output templates |
| `yaml`       | YAML snippet examples (when embedded)              |

----------

### 2.3 Context Notation for Embedded Code Blocks

**Rule:** ALL child code blocks located directly within a parent code block MUST be preceded by a **context notation line**.

**Format:**

~~~plaintext
> **Embedded Example <type>:** <contextual description>
~~~

**Placement:** Immediately before the child code block (no blank lines between notation and code block).

**Examples:**

| Context Notation                                                              | Appropriate For             |
| :---------------------------------------------------------------------------- | :-------------------------- |
| `> **Embedded Example reStructuredText:** BRD directive`                      | RST directive examples      |
| `> **Embedded Example Python:** Function to validate complete citation chain` | Algorithm implementations   |
| `> **Embedded Example JSON:** Output of the tool`                             | JSON output/schema examples |
| `> **Embedded Example Mermaid Syntax:** Tool output`                          | Mermaid diagrams            |
| `> **Embedded Example Type:** plaintext DDR Audit Report template`            | Report templates            |
| `> **Embedded Example Logic:** Conceptual logic of the rule`                  | Pseudo-code or logic        |

**Complete Example:**

~~~markdown
~~~markdown

## Validation Algorithm

> **Embedded Example Code:** Python function to validate complete citation chain

```python
def validate_complete_chain(tag_id, documentation):
    visited = set()
    current = tag_id
    chain = [current]
    return {"valid": True, "chain": chain}
```

~~~
~~~

---

## 3. Section Boundary Markers

### 3.1 Hard Section Boundary (`---`)

**Rule:** Use the standard horizontal rule (`---`) for **major** section boundaries.

**Purpose:** Signals a **significant topical transition** or the conclusion of a major documentation unit.

**Usage Locations:**

- End of document (before title of conclusion section)
- Between major numbered sections (at the `##` level)
- Separation of distinct content blocks within knowledge/exemplar definitions

**Format:** Three hyphens on a dedicated line:

~~~plaintext
---
~~~

**Example Context:**

~~~plaintext
#### 27.9.3 For Project Maintainability

<content>

---

### 27.10 Conclusion

<content>
~~~

----------

### 3.2 Soft Section Boundary (`----------`)

**Rule:** Use an extended horizontal rule (`----------`) for **subsection** boundaries.

**Purpose:** Indicates a **moderate topical transition** within the same parent section. Provides visual separation without implying complete topic departure.

**Usage Locations:**

- Between subsections at the `###` level
- After the closing `~~~` of a parent code block, before the next subsection
- Separation of agent definition blocks within the same major section

**Format:** Ten hyphens on a dedicated line:

~~~plaintext
----------
~~~

**Example Context:**

~~~plaintext
~~~

----------

#### 27.3.2 BRD_Strategist (Business Requirements)

<content>

~~~
**Boundary Type Selection Guide:**

| Transition Type                            | Marker       | Example Context                             |
| :----------------------------------------- | :----------- | :------------------------------------------ |
| End of major section (##)                  | `---`        | Before `### 27.10 Conclusion`               |
| Between same-level subsections (###, ####) | `----------` | After code block, before next `#### 27.3.X` |
| Minor internal separation                  | (blank line) | Between paragraphs within a subsection      |

---

## 4. Section Header Formatting

### 4.1 Header Hierarchy Rules

**Rule:** Section headers MUST use the correct number of hashtags based on their numerical prefix depth.

**DO NOT** evaluate or count headers contained within code blocks—these are example content and do not follow the document's structural hierarchy.

**Hierarchy Mapping:**

| Decimal Points    | Hashtag Count | Example                                |
| :---------------- | :------------ | :------------------------------------- |
| 0 (single number) | 2 (`##`)      | `## 27. Section Title`                 |
| 1                 | 3 (`###`)     | `### 27.1 Subsection Title`            |
| 2                 | 4 (`####`)    | `#### 27.3.1 Sub-subsection Title`     |
| 3                 | 5 (`#####`)   | `##### 27.3.1.1 Deep Subsection Title` |

**Validation Algorithm:**
~~~plaintext

decimal_count = count('.') in section_number
required_hashtags = 2 + decimal_count

~~~
**Examples:**
~~~markdown

## 27. Antigravity: Agent Asset Definition Files

### 27.1 Overview of Antigravity Integration

#### 27.3.1 DDR_Orchestrator (Master Agent)

##### 27.3.1.1 Skill Definition

~~~
----------

### 4.2 Header Formatting Style

**Rule:** Headers SHOULD follow sentence case with proper capitalization of proper nouns and abbreviations.

**Examples:**

- ✅ `### 27.1 Overview of Antigravity Integration`
- ✅ `#### 27.3.1 DDR_Orchestrator (Master Agent)`
- ❌ `### 27.1 overview of antigravity integration`

---

## 5. File Path References

### 5.1 File Path Indicator

**Rule:** When introducing asset definition content, precede it with a **File:** reference line.

**Format:**
~~~plaintext

**File:** `<relative_path_to_file>`

~~~
**Path Format:** Use relative paths from project root with forward slashes.

**Examples:**
~~~markdown

**File:** `.agent/skills/ddr_orchestrator/SKILL.md`

**File:** `.agent/rules/ddr_tier_classification.md`

**File:** `.agent/scripts/ddr_classify_information.py`

~~~
**Placement:** The file reference appears:

1. Immediately after the subsection header introducing the asset
2. Before the opening tilde fence of the parent code block
3. With one blank line after the reference, before the code block

---

## 6. Inline Formatting Conventions

### 6.1 Emphasis Markers

| Style    | Markdown     | Purpose                                       |
| :------- | :----------- | :-------------------------------------------- |
| **Bold** | `**text**`   | Key terms, labels, status indicators          |
| *Italic* | `*text*`     | Definitions, emphasis, foreign phrases        |
| `Code`   | `` `text` `` | Variable names, file paths, commands, tag IDs |

### 6.2 Tag ID References

**Rule:** Tag IDs SHOULD be formatted as inline code when referenced in prose.

**Examples:**

- Reference: `BRD-1`, `NFR-19.6`, `FSD-21.3`
- Prose: "The tag `ISP-5` traces back through..."

----------

### 6.3 Agent Handle References

**Rule:** Agent handles SHOULD be formatted as inline code with the `@` prefix.

**Examples:** `@ddr_orchestrator`, `@brd_strategist`, `@traceability_auditor`

---

## 7. Table Formatting

### 7.1 Standard Table Structure

**Rule:** Tables MUST use pipe (`|`) delimiters with header separator row.

**Format:**
~~~plaintext

| Column 1 | Column 2 | Column 3 |
| :------- | :------- | :------- |
| Data 1   | Data 2   | Data 3   |

~~~
**Alignment Specifiers:**

- Left: `|:--|`
- Center: `|:--:|`
- Right: `|--:|`

**Example:**
~~~markdown

| Tier | Agent             | Color     |
| :--- | :---------------- | :-------- |
| BRD  | `@brd_strategist` | `#E1F5FF` |
| NFR  | `@nfr_enforcer`   | `#FFF3E0` |

~~~
---

## 8. List Formatting

### 8.1 Unordered Lists

**Rule:** Use hyphen (`-`) for unordered list items.

**Example:**
~~~markdown

- First item
- Second item
- Nested item

~~~
### 8.2 Ordered Lists

**Rule:** Use numerical prefixes for ordered lists.

**Example:**
~~~markdown

1. First step
2. Second step
3. Third step

~~~
**Special Case — Numbered Steps in Code Blocks:**

Within code blocks representing workflows or procedures, steps MAY use contextual numbering:
~~~markdown

## Steps

1. **Gather Requirements** - Interview user for business context
2. **Create BRD** - Generate business requirements tags

~~~
---

## 9. YAML Frontmatter in Code Blocks

### 9.1 Frontmatter Structure

**Rule:** Asset definitions within parent code blocks MUST begin with YAML frontmatter.

**Format:**
~~~plaintext

---
key: value
array:

- item1
- item2
---

# Markdown Body Content

~~~
**Example:**
~~~markdown

~~~markdown
---
name: "DDR Tier Classification"
description: "Always classify information by tier before processing using the DDR decision tree."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "medium"
---

# DDR Tier Classification Rule

## Enforcement Protocol

<content>
~~~

~~~
---

## 10. Whitespace Conventions

### 10.1 Blank Line Rules

| Location                                       | Blank Lines                                      |
| :--------------------------------------------- | :----------------------------------------------- |
| After section header                           | 1                                                |
| Before section header                          | 1 (within same level), 2 (after boundary marker) |
| Before/after code blocks                       | 1                                                |
| Between context notation and code block        | 0                                                |
| After closing code fence within parent block   | 1                                                |
| Before boundary marker (`---` or `----------`) | 1                                                |
| After boundary marker                          | 1                                                |

### 10.2 Trailing Whitespace

**Rule:** Lines SHOULD NOT have trailing whitespace (spaces/tabs after content).

---

## 11. Document Structure Template

The following template illustrates the expected structure of a DDR hierarchy document:
~~~markdown

## X. Document Title

### X.1 Section Name

<introductory prose>

#### X.1.1 Subsection Name

**File:** `.agent/<type>/<filename>.md`

~~~<content_type>
---
<yaml_frontmatter>
---

# Asset Title

## Subsection Within Code Block

<prose>

> **Embedded Example Type:** <description>
```<inner_content_type>

<embedded_example>

```
<prose continues>
~~~

----------

#### X.1.2 Next Subsection Name

<content>

---

### X.2 Next Major Section

<content>

~~~
---

## 12. Validation Checklist

When validating or transforming documents, verify the following:

- [ ] All outer-most code blocks use tilde fencing (`~~~`)
- [ ] All inner code blocks use backtick fencing (` ``` `)
- [ ] All inner code blocks within parent blocks have context notation
- [ ] Context notation format: `> **Embedded Example Type:** <description>`
- [ ] Hard section boundaries (`---`) separate major sections
- [ ] Soft section boundaries (`----------`) separate subsections
- [ ] Section header hashtag counts match decimal point rules
- [ ] File path references use `**File:** \`path\`` format
- [ ] Tables use pipe delimiters with alignment specifiers
- [ ] YAML frontmatter is properly delimited with `---`
- [ ] Blank line rules are followed consistently
- [ ] No trailing whitespace on lines
- [ ] Agent asset frontmatter conforms to schema (see §14)

---

## 13. Migration Notes

When converting files from previous formatting structures:

1. **Identify all triple-backtick outer blocks** → Convert to tilde fencing
2. **Locate embedded code examples without context notation** → Add appropriate `> **Embedded Example Type:**` lines
3. **Check section boundaries** → Standardize to `---` (hard) and `----------` (soft) per usage context
4. **Validate header hierarchy** → Ensure hashtag counts match section numbering depth
5. **Standardize file references** → Convert to `**File:** \`path\`` format

---

## 14. Agent Asset Schema Requirements

This section defines the schema requirements for Antigravity agent asset definition files. All agent assets use YAML frontmatter conforming to the interfaces defined in the modular schema definition files located in `.agent/schemas/` (v1.18.3).

### 14.1 Asset Type Overview

| Asset Type           | File Pattern                                              | Interface                      |
| :------------------- | :-------------------------------------------------------- | :----------------------------- |
| Gemini Configuration | `~/.gemini/GEMINI.md` or `.agent/GEMINI.md`               | `GeminiMdConfiguration`        |
| Skill                | `.agent/skills/<skill-name>/SKILL.md`                     | `SkillDefinition`              |
| Rule                 | `.agent/rules/*.md`                                       | `RuleDefinition`               |
| Security Policy      | `.agent/rules/SECURITY_GUARDRAILS.md`                     | `SecurityPolicyDefinition`     |
| Workflow             | `.agent/workflows/*.md`                                   | `WorkflowDefinition`           |
| Implementation Plan  | `implementation_plan.md` or `.agent/plans/*.md`           | `ImplementationPlanDefinition` |
| Task                 | `task.md` or `TASK-XXXXXX.md`                             | `TaskDefinition`               |
| Walkthrough          | `walkthrough.md`                                          | `WalkthroughDefinition`        |

----------

### 14.2 Gemini Configuration Schema

**File Pattern:** `~/.gemini/GEMINI.md` or `.agent/GEMINI.md`

**Interface:** `GeminiMdConfiguration`

**Schema Source:** `.agent/schemas/gemini/gemini.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `description` | `string` | ✅ | High-level summary of workspace purpose/scope. |
| `models` | `string[]` | ✅ | Allowed Gemini 3 variants (e.g., `gemini-3.1-pro`). |
| `version` | `string` | ✅ | Schema version for compatibility (e.g., `20260222_v118`). |
| `scope` | `enum` | ✅ | `'global'` (system-wide) or `'workspace'` (local override). |
| `thinking_level` | `enum` | ❌ | AI reasoning depth: `minimal`, `low`, `medium`, `high`. |
| `temperature` | `number` | ❌ | Determinism slider (e.g., `0.1` for strict code). |

| Body Content Field | Interface Mapping | Description |
| :--- | :--- | :--- |
| `workspace_context` | `string` | Primary environment and tech stack baseline. |
| `cognitive_directives` | `string` | Reasoning parameters and output preferences. |
| `security_and_execution_guardrails` | `string` | Strict negative constraints and boundary rules. |
| `thought_signature_protocol` | `string` | Reasoning state persistence requirements. |
| `activation_rules` | `string` | Trigger conditions (e.g., `@mention`). |

**Example Frontmatter:**
~~~yaml

---
description: "DDR System Documentation Workspace"
models:

- "gemini-3.1-pro"
- "gemini-3-flash"
version: "20260222_v118.3"
scope: "workspace"
thinking_level: "medium"
temperature: 0.1
---

~~~
----------

### 14.3 Skill Definition Schema

**File Pattern:** `.agent/skills/<skill-name>/SKILL.md`

**Interface:** `SkillDefinition`

**Schema Source:** `.agent/schemas/skill/skill.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `string` | ❌ | Kebab-case identifier (defaults to directory name). |
| `description` | `string` | ✅ | Primary trigger condition for semantic routing. |

| Body Content Field | XML Tag | Required | Description |
| :--- | :--- | :--- | :--- |
| `when_to_use` | `<when_to_use>` | ✅ | Bullet list of activation scenarios. |
| `how_to_use` | `<how_to_use>` | ✅ | Step-by-step reasoning and output format. |
| `constraints` | `<constraints>` | ❌ | Hard safety guardrails and "Do Not" rules. |
| `resources_reference` | `<resources_reference>` | ❌ | Relative paths to scripts/docs/examples. |

**Example Frontmatter:**
~~~yaml

---
description: "Generate Python code stubs with Numpy-style docstrings from TDD tags."
---

~~~
----------

### 14.4 Rule Definition Schema

**File Pattern:** `.agent/rules/*.md`

**Interface:** `RuleDefinition`

**Schema Source:** `.agent/schemas/rule/rule.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `string` | ❌ | Human-readable display name. |
| `description` | `string` | ✅ | Semantic metadata explaining the rule's purpose. |
| `trigger` | `enum` | ✅ | `auto` \| `manual` \| `glob` \| `always_on` \| `model_decision` \| `@mention` |
| `globs` | `string` | ❌ | Comma-separated wildcard patterns (required for `glob`). |
| `priority` | `enum` | ✅ | Conflict weight: `low` \| `medium` \| `high` \| `critical`. |

| Body Content Field | XML Tag | Required | Description |
| :--- | :--- | :--- | :--- |
| `constraints` | `<constraints>` | ✅ | List of negative and positive constraints. |
| `verification_step` | `<verification_step>` | ❌ | Silent verification checks before final output. |

**Example Frontmatter:**
~~~yaml

---
description: "Ensure all DDR tags follow hierarchical citation rules."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "high"
---

~~~
----------

### 14.5 Security Policy Definition Schema

**File Pattern:** `.agent/rules/SECURITY_GUARDRAILS.md`

**Interface:** `SecurityPolicyDefinition`

**Schema Source:** `.agent/schemas/security-policy/security-policy.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `string` | ✅ | Display name for the security policy. |
| `description` | `string` | ✅ | Summary of protected boundaries. |
| `trigger` | `'always_on'` | ✅ | Security policies must always apply. |
| `priority` | `'critical'` | ✅ | Highest priority for conflict resolution. |

| Body Content Field | XML Tag | Required | Description |
| :--- | :--- | :--- | :--- |
| `forbidden_actions` | `<forbidden_actions>` | ✅ | Array of strictly prohibited agent operations. |
| `allowed_domains` | `<allowed_domains>` | ✅ | List of authorized external domains. |
| `verification_step` | `<verification_step>` | ✅ | Mandatory self-check before outputting code. |

**Example Frontmatter:**
~~~yaml

---
name: "Workspace Execution Policy"
description: "Restricts file deletion and unauthorized domain access."
trigger: "always_on"
priority: "critical"
---

~~~
----------

### 14.6 Workflow Definition Schema

**File Pattern:** `.agent/workflows/*.md`

**Interface:** `WorkflowDefinition`

**Schema Source:** `.agent/schemas/workflow/workflow.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | `string` | ❌ | Shortcut command name (starts with `/`). |
| `description` | `string` | ✅ | Summary of the workflow's purpose. |

| Body Content Field | Interface Mapping | Description |
| :--- | :--- | :--- |
| `steps` | `string` | Numbered sequence of atomic instructions. |
| `verification_plan` | `string` | Conditions for successful completion. |

**Example Frontmatter:**
~~~yaml

---
name: "/document-feature"
description: "End-to-end documentation of new system features."
---

~~~
----------

### 14.7 Implementation Plan Definition Schema

**File Pattern:** `implementation_plan.md` or `.agent/plans/*.md`

**Interface:** `ImplementationPlanDefinition`

**Schema Source:** `.agent/schemas/implementation-plan/implementation-plan.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `task` | `string` | ✅ | High-level overview of the proposed change. |
| `model` | `enum` | ✅ | Planning model: `gemini-3.1-pro` \| `gemini-3.1-pro-preview`. |

| Body Content Field | XML Tag | Required | Description |
| :--- | :--- | :--- | :--- |
| `objective` | `<objective>` | ✅ | Detailed overview and design justification. |
| `phases` | `<phases>` | ❌ | Phased development roadmap for complex tasks. |
| `atomic_steps` | `<atomic_steps>` | ✅ | Array of single-responsibility execution steps. |
| `verification` | `<verification>` | ✅ | Mapped verification checks for each step. |
| `risks_and_mitigations` | `<risks_and_mitigations>` | ❌ | Potential failure points and addressal plan. |

**Example Frontmatter:**
~~~yaml

---
task: "Refactor core engine to use modular schema system."
model: "gemini-3.1-pro"
---

~~~
----------

### 14.8 Task Definition Schema

**File Pattern:** `task.md` or `TASK-XXXXXX.md`

**Interface:** `TaskDefinition`

**Schema Source:** `.agent/schemas/task/task.d.ts`

| Frontmatter Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `task_id` | `string` | ✅ | Globally unique identifier. |
| `title` | `string` | ✅ | Brief description of the task. |
| `priority` | `enum` | ✅ | Order: `low` \| `medium` \| `high` \| `critical`. |
| `target_model` | `enum` | ✅ | `gemini-3.1-pro` \| `gemini-3-flash`. |
| `task_dependencies` | `string[]` | ❌ | Prerequisite task IDs. |
| `file_dependencies` | `string[]` | ❌ | Required file paths. |

| Body Content Field | XML Tag | Required | Description |
| :--- | :--- | :--- | :--- |
| `expected_output` | `<expected_output>` | ✅ | Tangible artifact produced by the task. |
| `constraints` | `<constraints>` | ❌ | Implementation limits and requirements. |
| `pre_check` | `<pre_check>` | ✅ | Instructions to perform before starting. |
| `acceptance_criteria` | `<acceptance_criteria>` | ✅ | Measurable conditions for completion. |
| `rollback_procedure` | `<rollback_procedure>` | ✅ | Reversion steps if verification fails. |

**Example Frontmatter:**
~~~yaml

---
task_id: "T-2026-001"
title: "Interface Refactoring"
priority: "high"
target_model: "gemini-3.1-pro"
---

~~~
----------

### 14.9 Walkthrough Definition Schema

**File Pattern:** `walkthrough.md`

**Interface:** `WalkthroughDefinition`

**Schema Source:** `.agent/schemas/walkthrough/walkthrough.d.ts`

| Body Content Field | XML Tag | Required | Description |
| :--- | :--- | :--- | :--- |
| `execution_summary` | `<execution_summary>` | ✅ | Recap of the solved objective. |
| `architectural_changes` | `<architectural_changes>` | ✅ | Highlight of major file/structural updates. |
| `verification_steps` | `<verification_steps>` | ✅ | Commands/actions to prove the work. |

**Example Body Structure:**
```markdown

<execution_summary>
Successfully migrated legacy Persona assets to the modular Skill system.
</execution_summary>

<architectural_changes>

- Deleted .agent/personas/
- Created .agent/skills/ddr_orchestrator/SKILL.md
</architectural_changes>

<verification_steps>
View .agent/skills/ to verify new structure.
</verification_steps>

```
~~~

----------

### 14.10 Schema Validation Checklist

When validating agent asset files, verify:

- [ ] **Skill body_content** — All body sections are wrapped in appropriate XML tags (`<when_to_use>`, `<how_to_use>`, etc.)
- [ ] **Rule trigger** — `trigger` uses one of: `auto` | `manual` | `glob` | `always_on` | `model_decision` | `@mention`
- [ ] **Rule priority** — `priority` uses one of: `low` | `medium` | `high` | `critical`
- [ ] **Security Policy** — `trigger` is always `'always_on'` and `priority` is always `'critical'`
- [ ] **Required properties** — All required properties defined in the `.d.ts` schema are present and non-empty
- [ ] **Enum values** — All enum properties use valid values from the schema

---

## 15. Cross-Reference: Asset Type to Content Type Mapping

When documenting agent assets within DDR hierarchy files, use the following content type mappings for parent code blocks:

| Asset Type           | Parent Code Block Fence | Rationale                                 |
| :------------------- | :---------------------- | :---------------------------------------- |
| Skill                | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Rule                 | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Security Policy      | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Workflow             | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Implementation Plan  | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Task                 | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Walkthrough          | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Gemini Configuration | `~~~markdown`           | Standard Markdown with YAML frontmatter   |
| Pure Config          | `~~~yaml`               | Configuration-only files (e.g., config.yaml) |

---

*This specification is normative for all DDR hierarchy documentation files.*
