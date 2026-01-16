# DDR Hierarchy Document Formatting Specification

**Version:** 1.1
**Last Updated:** 2026-01-15
**Reference Documents:**
- `27. Antigravity Agent Asset Definition Files.md` (Formatting)
- `antigravity_types.d.ts` (Schema)

---

## 1. Purpose

This specification defines the formatting rules for DDR hierarchy documentation files. It serves as an authoritative ruleset for AI agents to:

1. **Validate** existing file formatting compliance
2. **Transform** files from previous formatting structures to the current standard
3. **Author** new documentation content with consistent styling

---

## 2. Code Block Hierarchy

### 2.1 Parent Code Blocks (Outer-Most)

**Rule:** All outer-most code blocks MUST use **tilde fencing** (`~~~`) with a specified content type.

**Syntax:**
~~~plaintext
~~~<content_type>
<content>
~~~
~~~

**Supported Content Types:**

| Content Type | Purpose |
|:--|:--|
| `markdown` | Rule definitions, tool definitions, workflow definitions |
| `mdc` | Persona definition files (`.mdc` format) |
| `yaml` | YAML configuration files (when content is pure YAML) |
| `plaintext` | Conversational transcripts, terminal output, reports |

**Example — Rule Definition:**
~~~markdown
~~~markdown
---
type: rule
name: "Example Rule"
globs:
  - "docs/**/*.rst"
---
# Rule: Example Rule

## Enforcement Protocol
Content here...
~~~
~~~

----------

### 2.2 Child Code Blocks (Inner/Embedded)

**Rule:** Code blocks nested WITHIN a parent (tilde-fenced) block MUST use **triple backticks** (` ``` `) with a specified content type.

**Syntax:**
~~~plaintext
```<content_type>
<embedded_content>
```
~~~

**Common Child Content Types:**

| Content Type | Purpose |
|:--|:--|
| `rst` | reStructuredText directive examples |
| `python` | Python code examples or algorithms |
| `json` | JSON schema or output examples |
| `mermaid` | Mermaid diagram syntax |
| `plaintext` | Plain text examples, pseudo-code, output templates |
| `yaml` | YAML snippet examples (when embedded) |

----------

### 2.3 Context Notation for Embedded Code Blocks

**Rule:** ALL child code blocks located directly within a parent code block MUST be preceded by a **context notation line**.

**Format:**
~~~plaintext
> **Embedded Example Type:** <contextual description>
~~~

**Placement:** Immediately before the child code block (no blank lines between notation and code block).

**Examples:**

| Context Notation | Appropriate For |
|:--|:--|
| `> **Embedded Example Type:** reStructuredText BRD directive` | RST directive examples |
| `> **Embedded Example Code:** Python function to validate complete citation chain` | Algorithm implementations |
| `> **Embedded Example JSON:** Output of the tool` | JSON output/schema examples |
| `> **Embedded Example Mermaid Syntax:** Tool output` | Mermaid diagrams |
| `> **Embedded Example Type:** plaintext DDR Audit Report template` | Report templates |
| `> **Embedded Example Logic:** Conceptual logic of the rule` | Pseudo-code or logic |

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

| Transition Type | Marker | Example Context |
|:--|:--|:--|
| End of major section (##) | `---` | Before `### 27.10 Conclusion` |
| Between same-level subsections (###, ####) | `----------` | After code block, before next `#### 27.3.X` |
| Minor internal separation | (blank line) | Between paragraphs within a subsection |

---

## 4. Section Header Formatting

### 4.1 Header Hierarchy Rules

**Rule:** Section headers MUST use the correct number of hashtags based on their numerical prefix depth.

**DO NOT** evaluate or count headers contained within code blocks—these are example content and do not follow the document's structural hierarchy.

**Hierarchy Mapping:**

| Decimal Points | Hashtag Count | Example |
|:--|:--|:--|
| 0 (single number) | 2 (`##`) | `## 27. Section Title` |
| 1 | 3 (`###`) | `### 27.1 Subsection Title` |
| 2 | 4 (`####`) | `#### 27.3.1 Sub-subsection Title` |
| 3 | 5 (`#####`) | `##### 27.3.1.1 Deep Subsection Title` |

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
##### 27.3.1.1 Persona Definition
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
**File:** `.agent/personas/ddr_orchestrator.mdc`

**File:** `.agent/rules/ddr_tier_classification.md`

**File:** `.agent/tools/ddr_classify_information.md`
~~~

**Placement:** The file reference appears:
1. Immediately after the subsection header introducing the asset
2. Before the opening tilde fence of the parent code block
3. With one blank line after the reference, before the code block

---

## 6. Inline Formatting Conventions

### 6.1 Emphasis Markers

| Style | Markdown | Purpose |
|:--|:--|:--|
| **Bold** | `**text**` | Key terms, labels, status indicators |
| *Italic* | `*text*` | Definitions, emphasis, foreign phrases |
| `Code` | `` `text` `` | Variable names, file paths, commands, tag IDs |

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
|:--|:--|:--|
| Data 1 | Data 2 | Data 3 |
~~~

**Alignment Specifiers:**
- Left: `|:--|`
- Center: `|:--:|`
- Right: `|--:|`

**Example:**
~~~markdown
| Tier | Agent | Color |
|:--|:--|:--|
| BRD | `@brd_strategist` | `#E1F5FF` |
| NFR | `@nfr_enforcer` | `#FFF3E0` |
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
type: rule
name: "DDR Tier Classification"
globs:
  - "docs/**/*.rst"
priority: 50
severity: mandatory
---
# DDR Tier Classification Rule

## Enforcement Protocol
<content>
~~~
~~~

---

## 10. Whitespace Conventions

### 10.1 Blank Line Rules

| Location | Blank Lines |
|:--|:--|
| After section header | 1 |
| Before section header | 1 (within same level), 2 (after boundary marker) |
| Before/after code blocks | 1 |
| Between context notation and code block | 0 |
| After closing code fence within parent block | 1 |
| Before boundary marker (`---` or `----------`) | 1 |
| After boundary marker | 1 |

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
- [ ] `type` property is first for Rule/Tool/Workflow definitions
- [ ] Handle/slug formats are correct (`@prefix`, `/prefix`)

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

This section defines the schema requirements for Antigravity agent asset definition files. All agent assets use YAML frontmatter conforming to the interfaces defined in `antigravity_types.d.ts` (v1.13+).

### 14.1 Asset Type Overview

| Asset Type | File Pattern | Extension | Purpose |
|:--|:--|:--|:--|
| Persona | `.agent/personas/*.mdc` | `.mdc` | Agent identity, capabilities, and behavior |
| Rule | `.agent/rules/*.md` | `.md` | Constraint enforcement and validation logic |
| Tool | `.agent/tools/*.md` | `.md` | Executable capabilities with command templates |
| Workflow | `.agent/workflows/*.md` | `.md` | Multi-step processes with user interaction |
| Knowledge | `.agent/knowledge/*.md` | `.md` | RAG indexing configuration for context retrieval |
| Evaluation | `.agent/evals/*.md` | `.md` | Automated QA/testing for agent outputs |

----------

### 14.2 Persona Definition Schema

**File Pattern:** `.agent/personas/*.mdc`

**Interface:** `PersonaDefinition`

| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `name` | `string` | ✅ | Human-readable display name (max ~25 chars) |
| `handle` | `@${string}` | ✅ | Unique identifier for summoning/delegation (e.g., `@ddr_orchestrator`) |
| `description` | `string` | ✅ | One-sentence summary of role for Router/User |
| `model` | `enum` | ✅ | LLM backend (see Model Options below) |
| `temperature` | `number` | ✅ | Creativity level: `0.0` (code/linting) to `1.0` (creative/design) |
| `color` | `string` | ✅ | UI visual accent (hex code or color name) |
| `icon` | `string` | ✅ | Avatar icon (Phosphor/Material name or relative SVG path) |
| `tools` | `string[]` | ✅ | Allowlist of executable capabilities |
| `context_globs` | `string[]` | ✅ | Files automatically loaded into context (use `[]` if none) |

**Model Options:**
- `gemini-3-pro-high` — High-reasoning Gemini (recommended for Architects/QA)
- `gemini-3-pro-low` — Standard Gemini
- `gemini-3-flash` — Fast Gemini
- `claude-sonnet-4.5` — Claude standard
- `claude-sonnet-4.5-thinking` — Claude with reasoning
- `claude-opus-4.5-thinking` — Claude high-reasoning
- `gpt-oss-120b-medium` — Open-source GPT variant

**Example Frontmatter:**
~~~yaml
---
name: "DDR Orchestrator"
handle: "@ddr_orchestrator"
description: "Master orchestrator for the DDR documentation system."
model: gemini-3-pro-high
temperature: 0.3
color: "#1E88E5"
icon: "flow-arrow"
tools:
  - classify_information
  - scoring_matrix
  - route_to_specialist
context_globs:
  - ".agent/rules/ddr_*.md"
  - "docs/llm_export/context_flat.md"
---
~~~

----------

### 14.3 Rule Definition Schema

**File Pattern:** `.agent/rules/*.md`

**Interface:** `RuleDefinition`

| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `type` | `'rule'` | ✅ | **Must be first property.** Literal value: `rule` |
| `name` | `string` | ✅ | Display name for "Active Rules" status |
| `globs` | `string[]` | ❌ | File patterns triggering this rule (omit for global rules) |
| `priority` | `number` | ✅ | Conflict resolution rank (higher wins). Default: `1`. Critical Safety: `>50` |
| `trigger` | `string[]` | ❌ | Keywords activating rule regardless of file type |
| `severity` | `enum` | ✅ | Enforcement level: `mandatory` \| `guideline` \| `suggestion` |
| `description` | `string` | ✅ | Precise instruction prompt injected into system context |

**Severity Levels:**
- `mandatory` — Violations are rejected; agent must refuse non-compliant output
- `guideline` — Violations are warned; agent should follow but may deviate with justification
- `suggestion` — Informational; agent may consider but not required

**Example Frontmatter:**
~~~yaml
---
type: rule
name: "DDR Tier Classification"
globs:
  - "docs/**/*.rst"
priority: 50
trigger:
  - "classify"
  - "tier"
severity: mandatory
description: "Always classify information by tier before processing."
---
~~~

----------

### 14.4 Tool Definition Schema

**File Pattern:** `.agent/tools/*.md`
**Script Location:** `.agent/scripts/`

**Interface:** `ToolDefinition`

| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `type` | `'tool'` | ✅ | Literal value: `tool` |
| `name` | `string` | ✅ | Function identifier (snake_case, unique) |
| `description` | `string` | ✅ | Prompt explaining when/how to use the tool |
| `command` | `string` | ✅ | Shell command with `{{args.x}}` templating |
| `runtime` | `enum` | ✅ | Execution environment: `system` \| `node` \| `python` \| `docker` |
| `confirmation` | `enum` | ✅ | User permission: `always` \| `never` (use `never` only for safe read-ops) |
| `args` | `Record<string, ArgSchema>` | ✅ | Schema for required inputs |

**Argument Schema (`ArgSchema`):**
| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `type` | `enum` | ✅ | Data type: `string` \| `number` \| `boolean` |
| `description` | `string` | ✅ | Explanation for LLM to understand usage |
| `required` | `boolean` | ❌ | Whether argument is mandatory (default: `true`) |

**Example Frontmatter:**
~~~yaml
---
type: tool
name: "classify_information"
description: "Classify unstructured information into appropriate DDR tier."
command: ".venv/Scripts/python .agent/scripts/classify_information.py --content \"{{args.content}}\""
runtime: python
confirmation: never
args:
  content:
    type: string
    description: "The information to classify"
    required: true
  context:
    type: string
    description: "Optional context for classification"
    required: false
---
~~~

----------

### 14.5 Workflow Definition Schema

**File Pattern:** `.agent/workflows/*.md`

**Interface:** `WorkflowDefinition`

| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `type` | `'workflow'` | ✅ | Literal value: `workflow` |
| `name` | `string` | ✅ | Action-oriented display title |
| `slug` | `/${string}` | ✅ | Slash command trigger (e.g., `/document-feature`) |
| `description` | `string` | ✅ | Summary for Router to suggest this workflow |
| `mode` | `enum` | ✅ | Execution mode: `interactive` \| `autonomous` |
| `context` | `string[]` | ✅ | Resources to preload (globs or agent handles) |
| `on_finish` | `string` | ✅ | Post-execution action (e.g., `suggest_followup: /audit`) |
| `inputs` | `InputSchema[]` | ✅ | Variables required from user before starting |

**Input Schema (`InputSchema`):**
| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `name` | `string` | ✅ | Variable identifier |
| `type` | `enum` | ✅ | Input type: `text` \| `string` \| `boolean` \| `file_path` |
| `description` | `string` | ❌ | Explanation shown in form UI |
| `default` | `any` | ❌ | Pre-filled value |
| `required` | `boolean` | ❌ | Whether input is mandatory (default: `true`) |

**Mode Descriptions:**
- `interactive` — Pauses for user approval after every step
- `autonomous` — Executes all steps without interruption

**Example Frontmatter:**
~~~yaml
---
type: workflow
name: "New Feature Documentation"
slug: "/document-feature"
description: "Complete workflow for documenting new feature from BRD through ISP."
mode: interactive
context:
  - "@ddr_orchestrator"
  - "docs/llm_export/context_flat.md"
on_finish: "suggest_followup: /traceability-audit"
inputs:
  - name: feature_name
    type: text
    description: "Name of the feature to document"
    required: true
  - name: feature_description
    type: text
    description: "Brief description of the feature"
    required: false
---
~~~

----------

### 14.6 Knowledge Definition Schema

**File Pattern:** `.agent/knowledge/*.md`
**Purpose:** RAG Indexing Configuration

**Interface:** `KnowledgeDefinition`

| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `name` | `string` | ✅ | Unique identifier (snake_case) |
| `sources` | `string[]` | ✅ | Data sources (URLs or file paths) |
| `refresh_schedule` | `enum` | ✅ | Re-indexing frequency: `always` \| `daily` \| `weekly` \| `manual` |
| `strategy` | `enum` | ✅ | Chunking strategy: `code` \| `prose` \| `mixed` |
| `access` | `string[] \| 'public' \| 'private'` | ✅ | Permission scope (agent handles or visibility level) |

**Strategy Descriptions:**
- `code` — Optimized for source code repositories (syntax-aware chunking)
- `prose` — Optimized for documentation (paragraph-aware chunking)
- `mixed` — Hybrid approach for mixed content

**Example Frontmatter:**
~~~yaml
---
name: ddr_meta_standard
sources:
  - "docs/llm_export/context_flat.md"
  - ".agent/assets/ddr_hierarchy/*.md"
refresh_schedule: daily
strategy: prose
access: public
---
~~~

----------

### 14.7 Evaluation Definition Schema

**File Pattern:** `.agent/evals/*.md`
**Purpose:** Automated QA/Testing for Agents

**Interface:** `EvaluationDefinition`

| Property | Type | Required | Description |
|:--|:--|:--|:--|
| `name` | `string` | ✅ | Name of test suite |
| `target_agent` | `@${string}` | ✅ | Agent handle being tested |
| `judge_model` | `enum` | ✅ | Judge LLM (should be stronger than target) |
| `pass_threshold` | `number` | ✅ | Minimum pass score (0-100). Strict: `90+` |
| `scenarios` | `string[]` | ✅ | Input prompts/scenarios to feed the agent |
| `rubric` | `string[]` | ✅ | Grading criteria for the Judge |

**Judge Model Options:**
- `claude-opus-4.5-thinking` — High-reasoning Claude (recommended)
- `gemini-3-pro-high` — High-reasoning Gemini

**Example Frontmatter:**
~~~yaml
---
name: classification_accuracy
target_agent: "@ddr_orchestrator"
judge_model: claude-opus-4.5-thinking
pass_threshold: 95
scenarios:
  - "Enable voice control of smart home devices"
  - "Device discovery must complete in <5s for 50 devices"
rubric:
  - "Correct tier classification (BRD, NFR, FSD, SAD, ICD, TDD, ISP)"
  - "Confidence score accuracy"
  - "Rationale quality and specificity"
---
~~~

----------

### 14.8 Schema Validation Checklist

When validating agent asset files, verify:

- [ ] **Type property first** — For Rule, Tool, and Workflow definitions, `type` must be the first frontmatter property
- [ ] **Handle format** — Persona and Evaluation `handle`/`target_agent` must start with `@`
- [ ] **Slug format** — Workflow `slug` must start with `/`
- [ ] **Required properties** — All required properties are present and non-empty
- [ ] **Enum values** — All enum properties use valid values from the schema
- [ ] **Array properties** — Array properties (like `tools`, `sources`, `scenarios`) are arrays even if single item
- [ ] **Nested schemas** — Tool `args` and Workflow `inputs` conform to their respective sub-schemas

---

## 15. Cross-Reference: Asset Type to Content Type Mapping

When documenting agent assets within DDR hierarchy files, use the following content type mappings for parent code blocks:

| Asset Type | Parent Code Block Fence | Rationale |
|:--|:--|:--|
| Persona | `~~~mdc` | Uses `.mdc` extension with persona-specific format |
| Rule | `~~~markdown` | Standard Markdown with YAML frontmatter |
| Tool | `~~~markdown` | Standard Markdown with YAML frontmatter |
| Workflow | `~~~markdown` | Standard Markdown with YAML frontmatter |
| Knowledge | `~~~markdown` | Standard Markdown with YAML frontmatter |
| Evaluation | `~~~markdown` | Standard Markdown with YAML frontmatter |
| Pure Config | `~~~yaml` | Configuration-only files (e.g., `config.yaml`) |

---

*This specification is normative for all DDR hierarchy documentation files.*
