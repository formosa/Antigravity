# 27. Antigravity: Agent Asset Definition Files

## 27.1 Overview of Antigravity Integration

Google's Antigravity IDE provides a framework for defining custom AI agents through structured asset files. This section establishes specialized agent configurations optimized for maintaining, validating, and extending the DDR documentation system within the Antigravity environment.

**Integration Philosophy:**

- **Agents as Documentation Stewards:** Each agent specializes in one tier or cross-tier validation
- **Human-Agent Collaboration:** Agents enforce constraints while humans provide creative direction
- **Continuous Validation:** Real-time integrity checking during documentation authoring
- **Context-Aware Assistance:** Agents retrieve relevant parent/child tags automatically

## 27.2 Core Agent Architecture

### 27.2.1 Agent Hierarchy

~~~markdown
# Agent Topology

Root Agent: DDR_Orchestrator
  ├── Tier Specialists:
  │   ├── BRD_Strategist (Business Requirements)
  │   ├── NFR_Enforcer (Non-Functional Requirements)
  │   ├── FSD_Analyst (Feature Specifications)
  │   ├── SAD_Architect (System Architecture)
  │   ├── ICD_DataEngineer (Interface Contracts)
  │   ├── TDD_Designer (Technical Design)
  │   └── ISP_CodeGenerator (Implementation Stubs)
  ├── Cross-Tier Validators:
  │   ├── Traceability_Auditor
  │   ├── Orphan_Detective
  │   └── AntiPattern_Scanner
  └── Utility Agents:
      ├── Tag_Reconciler
      ├── Manifest_Manager
      └── Migration_Assistant
~~~

----------

## 27.3 Specialist Agent Definitions

### 27.3.1 DDR_Orchestrator (Standard Enforcement)

The DDR_Orchestrator is the master agent for the DDR documentation system. This section presents the associated asset definitions organized by asset type per schema specifications.

#### 27.3.1.1 Skill Definition

**File:** `.agent/skills/ddr_orchestrator/SKILL.md`

~~~markdown
---
name: "DDR Orchestrator"
description: "Master orchestrator for the DDR documentation system. Routes tasks to tier specialists."
---

<when_to_use>

- Serving as lead architect for the DDR documentation system.
- Maintaining the big picture of how all tiers connect while delegating specialized tasks to tier-specific agents.
- Enforcing the seven-tier hierarchy and ensuring no information falls through the cracks.
</when_to_use>

<how_to_use>

- Utilize complete knowledge of DDR tier hierarchy and relationships.
- Manage traceability requirements (`:links: PARENT` citations).
- Oversee the reconciliation manifest system.
- Determine when to delegate vs. handle tasks directly.
- Communication Style: Concise and directive. When presented with new information, immediately classify it by tier and route to the appropriate specialist agent using tags, tiers, and traceability chains.
</how_to_use>

<constraints>

- Maintain >95% accuracy in tier classification across all 7 tiers.
- Enforce strict adherence to the ddr_glossary controlled vocabulary.
</constraints>

<resources_reference>

- .agent/scripts/classify_information.py
- .agent/scripts/scoring_matrix.py
- .agent/scripts/route_to_specialist.py
- .agent/rules/ddr_*.md
- .agent/assets/ddr_hierarchy/*.md
- docs/llm_export/context_flat.md
- docs/00_glossary/terms.rst
</resources_reference>
~~~

#### 27.3.1.2 Associated Rule Definitions

**File:** `.agent/rules/ddr_tier_classification.md`

~~~markdown
---
name: "DDR Tier Classification"
description: "Always classify information by tier before processing using the DDR decision tree."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "medium"
---
<constraints>

## Enforcement Protocol: DDR Tier Classification

Before any documentation task, invoke classification workflow:

1. Apply decision tree (Report Section 4.1)
2. If ambiguous, use scoring matrix (Report Section 4.2)
3. Route to tier-specific agent
4. Never allow mixed-tier content in single tag
</constraints>
~~~

**File:** `.agent/rules/ddr_traceability_mandate.md`

~~~markdown
---
name: "DDR Traceability Mandate"
description: "Every tag must cite parent (except BRD root). Enforces complete traceability chains."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "high"
---
<constraints>

## Enforcement Protocol: DDR Traceability Mandate

Before confirming any new tag creation:

- Check if tag has `:links: PARENT` citation
- Verify cited parent exists in documentation
- If orphan detected, invoke Orphan_Detective agent
- Reject tag creation if parent validation fails
</constraints>
~~~

**File:** `.agent/rules/ddr_id_immutability.md`

~~~markdown
---
name: "DDR ID Immutability"
description: "Tag IDs are immutable database keys. Never allow renumbering or reuse of deleted IDs."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "critical"
---
<constraints>

## Enforcement Protocol: DDR ID Immutability

- Never allow renumbering of existing tags
- Never allow reuse of deleted tag IDs
- Only permit sequential ID appending (e.g., add FSD-21 after FSD-20)
- DEPRECATED markers allowed, but original ID preserved
</constraints>
~~~

**File:** `.agent/rules/ddr_manifest_integrity.md`

~~~markdown
---
name: "DDR Manifest Integrity"
description: "Reconciliation manifests must stay synchronized with tag inventory."
trigger: "glob"
globs: "docs/**/*.rst, docs/**/reconciliation_manifest.rst"
priority: "medium"
---
<constraints>

## Enforcement Protocol: DDR Manifest Integrity

After any tag addition/deletion/modification:

- Invoke Manifest_Manager to update `:tag_count:`
- Update `:tag_inventory:` list with exact tag IDs
- Set `:integrity_status:` to DIRTY if dependencies affected
- Append to `:pending_items:` if conflicts detected
</constraints>
~~~

#### 27.3.1.3 Associated Workflow Definitions

**File:** `.agent/workflows/ddr_new_feature_documentation.md`

~~~markdown
---
name: "New Feature Documentation"
description: "Complete workflow for documenting new feature from BRD through ISP."
---

## Steps

1. **Gather Requirements** - Interview user for business context
2. **Create BRD** - Generate business requirements tags
3. **Derive Constraints** - Interview for performance/resource limits
4. **Create NFR** - Generate non-functional requirements
5. **Specify Behavior** - Define user-facing workflows
6. **Design Architecture** - Select patterns and components
7. **Define Contracts** - Create data schemas
8. **Blueprint Components** - Design classes and methods
9. **Generate Stubs** - Create implementation scaffolding
10. **Validate Traceability** - Audit complete chain
11. **Update Manifests** - Synchronize reconciliation data
12. **Present Summary** - Report all created artifacts

## Verification Plan

- All 7 tiers have at least one tag created
- Traceability chain is complete from ISP to BRD
- No forbidden terms in BRD content
- All manifests are synchronized (status: CLEAN)
~~~

**File:** `.agent/workflows/ddr_orphan_resolution.md`

~~~markdown
---
name: "Orphan Resolution"
description: "Resolve tags without proper parent citations through upward abstraction or downward specification."
---

## Steps

1. **Classify orphan direction**:
   - BRD tier: No action (root allowed)
   - Has implementation detail: Upward abstraction needed
   - Is high-level requirement: Downward specification needed

2. **Execute resolution**:
   - Upward: Synthesize appropriate parent tag
   - Downward: Decompose into child specifications

3. **Validate synthesis** via Traceability_Auditor

4. **Update documentation** via Manifest_Manager

## Verification Plan

- Resolved tag has at least one valid parent citation
- Parent tag exists in documentation
- No circular dependencies introduced
~~~

----------

### 27.3.2 BRD_Strategist (Business Requirements)

The BRD_Strategist is a specialized agent for authoring Business Requirements Document (BRD) tier content. This section presents the associated Antigravity asset definitions organized by asset type per schema specifications.

#### 27.3.2.1 Skill Definition

**File:** `.agent/skills/brd_strategist/SKILL.md`

~~~markdown
---
name: "BRD Strategist"
description: "Strategic business analyst for BRD tier content. Abstracts technical details to business objectives."
---

<when_to_use>

- Serving as a strategic business analyst for Business Requirements Document (BRD) tier content.
- Managing market positioning and ROI analysis.
- Abstracting technical details to business objectives (competitive advantage, user value, metrics).
</when_to_use>

<how_to_use>

- Perform market opportunity analysis and stakeholder value propositioning.
- Define success metrics (SLAs, adoption rates, satisfaction scores).
- Develop competitive differentiation strategies and frame regulatory compliance as a business driver.
- Communication Style: Executive-level; concise, outcome-focused, ROI-oriented. Use business terminology (market share, user engagement) over technical jargon.
</how_to_use>

<constraints>

- NEVER mention specific technologies (ZeroMQ, ONNX, PostgreSQL, etc.).
- NEVER describe implementation details (sockets, threads, algorithms).
- NEVER specify data structures or protocols.
- ALWAYS frame requirements as business problems/opportunities with measurable success metrics.
- Maintain 100% compliance with technology-agnostic constraint; zero leakage of implementation details.
</constraints>

<resources_reference>

- .agent/scripts/abstract_to_business.py
- .agent/scripts/derive_success_metrics.py
- docs/01_brd/*.rst
- .agent/rules/brd_*.md
</resources_reference>
~~~

#### 27.3.2.2 Associated Rule Definitions

**File:** `.agent/rules/brd_technology_agnostic.md`

~~~markdown
---
name: "BRD Technology Agnostic"
description: "BRD content must be 100% technology-agnostic. No specific technologies, implementations, or protocols."
trigger: "glob"
globs: "docs/01_brd/*.rst"
priority: "critical"
---
<constraints>

## Forbidden Terms

- ZeroMQ, ONNX, PostgreSQL, React, Docker
- socket, thread, API, REST, GraphQL
- GPU, CUDA, CPU core, RAM allocation

## Enforcement Protocol: BRD Technology Agnostic

Scan all BRD content for forbidden terms. Any detection requires immediate abstraction to business capability (e.g., "local processing" instead of "GPU inference").
</constraints>
~~~

**File:** `.agent/rules/brd_measurable_metrics.md`

~~~markdown
---
name: "BRD Measurable Metrics"
description: "All BRD success criteria must be quantifiable with numeric targets and units."
trigger: "glob"
globs: "docs/01_brd/*.rst"
priority: "high"
---
<constraints>

## Enforcement Protocol: BRD Measurable Metrics

Success metrics must include numeric targets with units:

- Percentages: "60% user adoption"
- Time: "within 3 months"
- Counts: "500 users", "50 devices"
- Currency: "$100K revenue"

## Example

❌ "Improve user engagement"
✅ "Target: 60% user adoption within 3 months"
</constraints>
~~~

**File:** `.agent/rules/brd_stakeholder_focus.md`

~~~markdown
---
name: "BRD Stakeholder Focus"
description: "Requirements must explicitly identify benefiting stakeholders."
trigger: "glob"
globs: "docs/01_brd/*.rst"
priority: "medium"
---
<constraints>

## Enforcement Protocol: BRD Stakeholder Focus

For each business requirement, ask: "Who benefits and how?"

## Typical Stakeholders

- End users (what do they gain?)
- Enterprise customers (revenue impact?)
- Business owners (competitive advantage?)
- Compliance officers (regulatory requirements?)
- Developers (productivity improvements?)
</constraints>
~~~

#### 27.3.2.3 Associated Workflow Definitions

**File:** `.agent/workflows/brd_create_tag.md`

~~~markdown
---
name: "Create BRD Tag"
description: "Author new BRD tag from user input with technology abstraction validation."
---

## Steps

1. **Extract Business Problem** - Interview for pain point or market opportunity
2. **Identify Stakeholders** - Who benefits and how?
3. **Define Success** - Invoke `derive_success_metrics` tool
4. **Draft Content** - Generate RST directive with BRD-X ID
5. **Validate Technology-Agnostic** - Invoke BRD_R1 rule
6. **Revise If Needed** - Abstract any detected technology references
7. **Confirm With User** - Present for approval

## Verification Plan

- Tag ID is unique and sequential
- Content contains zero forbidden technology terms
- Success metrics are quantifiable
~~~

----------

### 27.3.3 Traceability_Auditor (Cross-Tier Validator)

The Traceability_Auditor is a cross-tier validation agent ensuring complete traceability chains from business requirements (BRD) through implementation stubs (ISP). This section presents the associated Antigravity asset definitions organized by asset type per schema specifications.

#### 27.3.3.1 Skill Definition

**File:** `.agent/skills/traceability_auditor/SKILL.md`

~~~markdown
---
name: "Traceability Auditor"
description: "Cross-tier validation agent ensuring complete traceability chains. Detects broken citations, orphans, and cycles."
---

<when_to_use>

- Performing documentation integrity audits as a meticulous QA engineer.
- Validating dependency graphs, citation chains, and reconciliation manifests.
- Detecting system errors such as broken links, circular references, or inconsistent inventories.
</when_to_use>

<how_to_use>

- Apply graph theory to detect cycles, orphans, and unreachable nodes.
- Parse citation syntax including `:links: PARENT` extraction.
- Perform automated testing and report generation.
- Communication Style: Precise and systematic. Report findings with tag IDs, line numbers, and actionable fix suggestions.
</how_to_use>

<constraints>

- Maintain 100% accuracy in cycle and orphan detection algorithms.
- Report findings with precise tag IDs and contextual rationale.
</constraints>

<resources_reference>

- .agent/scripts/build_dependency_graph.py
- .agent/scripts/generate_traceability_report.py
- .agent/scripts/visualize_traceability.py
- docs/**/*.rst
- .agent/rules/trace_*.md
- docs/_build/json/needs.json
</resources_reference>
~~~

#### 27.3.3.2 Associated Rule Definitions

**File:** `.agent/rules/trace_complete_chain.md`

~~~markdown
---
name: "Trace Complete Chain"
description: "Every ISP tag must trace back to BRD root through complete citation chain."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "critical"
---
<constraints>

## Enforcement Protocol: Trace Complete Chain

Traverse citations upward from any tag until:

1. BRD root is reached (VALID)
2. Cycle is detected (ERROR: CIRCULAR_DEPENDENCY)
3. Missing parent is found (ERROR: BROKEN_CHAIN)

## Validation Algorithm

> **Embedded Example Code:** Python function to validate complete citation chain
```python

def validate_complete_chain(tag_id, documentation):
visited = set()
current = tag_id
chain = [current]

while not current.startswith("BRD"):
if current in visited:
return {"valid": False, "error": "CIRCULAR_DEPENDENCY", "cycle": chain}
visited.add(current)
parents = extract_citations(documentation[current])
if len(parents) == 0:
return {"valid": False, "error": "BROKEN_CHAIN", "orphan": current}
current = parents[0]
chain.append(current)

return {"valid": True, "chain": chain, "depth": len(chain)}

```
</constraints>
~~~

**File:** `.agent/rules/trace_no_forward_references.md`

~~~markdown
---
name: "No Forward References"
description: "Parent tags must exist before children cite them. No dangling references allowed."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "high"
---
<constraints>

## Enforcement Protocol: No Forward References

For every citation in the documentation:

- Verify the cited parent tag exists
- Report MISSING_PARENT error if parent not found
- Suggest creation of parent or correction of citation
</constraints>
~~~

**File:** `.agent/rules/trace_no_sibling_citations.md`

~~~markdown
---
name: "No Sibling Citations"
description: "Tags may not cite siblings (same tier and same block). Cite common parent instead."
trigger: "glob"
globs: "docs/**/*.rst"
priority: "high"
---
<constraints>

## Enforcement Protocol: No Sibling Citations

For each citation, check:

1. Extract tier and block from both tags
2. If same tier AND same block → SIBLING_CITATION error
3. Provide suggestion to cite common parent tier

## Pattern Detection

> **Embedded Example Logic:** Conceptual logic of the rule
```plaintext

TAG-X.1 citing TAG-X.2 → VIOLATION
TAG-X citing TAG-Y → VALID (different blocks)

```
</constraints>
~~~

#### 27.3.3.3 Associated Workflow Definitions

**File:** `.agent/workflows/trace_comprehensive_audit.md`

~~~markdown
---
name: "Comprehensive Audit"
description: "Full documentation integrity validation across all tiers and manifests."
---

## Steps

1. **Build Graph** - Invoke `build_dependency_graph` tool
2. **Generate Report** - Invoke `generate_traceability_report` tool
3. **Check Manifests** - Delegate to Manifest_Manager agent
4. **Scan Anti-Patterns** - Delegate to AntiPattern_Scanner agent
5. **Compile Results** - Aggregate all validation outputs
6. **Present Findings** - Generate formatted audit report

## Report Template

> **Embedded Example Type:** plaintext DDR Audit Report template
```plaintext

═══════════════════════════════════════════
DDR INTEGRITY AUDIT REPORT
═══════════════════════════════════════════

Overall Status: ${status}

STATISTICS:

- Total Tags: ${total_tags}
- Max Chain Depth: ${max_depth}
- Average Chain Length: ${avg_chain_length}

ERRORS: ${error_count}
WARNINGS: ${warning_count}

Next Steps:

1. Fix all ERROR-level issues (blocking)
2. Address WARNING-level issues (recommended)
3. Re-run audit after fixes applied
═══════════════════════════════════════════

```
## Verification Plan

- All document tiers scanned (BRD through ISP)
- All reconciliation manifests verified
- Graph contains zero orphans (except BRD) and zero cycles
~~~

**File:** `.agent/workflows/trace_tag_to_root.md`

~~~markdown
---
name: "Trace Tag to Root"
description: "Show complete citation chain for a specific tag from current tier to BRD root."
---

## Steps

1. **Validate Tag Exists** - Check tag_id exists in documentation
2. **Build Chain** - Invoke TRACE_R1_Complete_Chain rule
3. **Visualize Chain** - Invoke `visualize_traceability` tool
4. **Present Chain** - Display formatted output with Mermaid diagram

## Output Format

> **Embedded Example Type:** plaintext traceability chain output
```plaintext

Traceability Chain for ISP-5:
ISP-5 → TDD-3 → SAD-2 → FSD-1 → NFR-1 → BRD-1

Chain Depth: 6 tiers
Validation: ✅ VALID

```
## Verification Plan

- Final node in chain is a BRD tag
- No broken links in the displayed chain
- Mermaid diagram renders correctly
~~~

----------

### 27.3.4 ISP_CodeGenerator (Implementation Stub Agent)

The ISP_CodeGenerator is a specialized agent for generating Python implementation stubs. This section presents the associated Antigravity asset definitions organized by asset type per schema specifications.

#### 27.3.4.1 Skill Definition

**File:** `.agent/skills/isp_codegenerator/SKILL.md`

~~~markdown
---
name: "ISP Code Generator"
description: "Generates Python implementation stubs with Numpy-style docstrings, traceability markers, and implementation guidance."
---

<when_to_use>

- Serving as a lead Python developer focusing on clean, well-documented code stubs.
- Providing structural guidance and implementation docstrings without providing full implementation bodies.
- Developing structure for Python 3.11+ environments.
</when_to_use>

<how_to_use>

- Implement Python idioms, type hints, and Numpy-style docstring formats.
- Apply class/method design patterns.
- Incorporate performance considerations (AMD Ryzen 9, RTX 3080) and API expertise (ONNX Runtime, ZeroMQ, PySide6).
- Communication Style: Technical but pedagogical; docstrings should teach developers how to implement logic with notes and error handling guidance.
</how_to_use>

<constraints>

- NEVER write complete function bodies (use `pass` statements).
- ALWAYS include traceability markers (Implements: TAG-ID).
- ALWAYS provide implementation notes in docstrings.
- MUST use Numpy-style docstrings and type hints for all parameters and returns.
- Maintain 100% compliance with ISP stub-only and traceability constraints.
</constraints>

<resources_reference>

- .agent/scripts/generate_class_stub.py
- .agent/scripts/generate_method_stub.py
- .agent/scripts/add_implementation_hints.py
- docs/**/*.rst
- src/**/*.py
- .agent/rules/isp_*.md
- .agent/assets/python_patterns/*.yaml
</resources_reference>
~~~

#### 27.3.4.2 Associated Rule Definitions

**File:** `.agent/rules/isp_stub_only.md`

~~~markdown
---
name: "ISP Stub Only"
description: "Function bodies must contain only `pass` statements. Actual logic belongs in implementation, not stubs."
trigger: "glob"
globs: "src/**/*.py"
priority: "critical"
---
<constraints>

## Enforcement Protocol: ISP Stub Only

Parse generated code with AST. For each function/method:

1. Allow docstrings
2. Allow `pass` statement
3. Reject any other statements (return, if, for, while, try, etc.)

## Validation Algorithm

> **Embedded Example Type:** Python AST validation algorithm
```python

def validate_stub(code):
ast_tree = ast.parse(code)

for node in ast.walk(ast_tree):
if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

# Filter out docstrings

non_docstring_body = [
stmt for stmt in node.body
if not isinstance(stmt, ast.Expr) or
not isinstance(stmt.value, ast.Constant)
]

# Check remaining statements

if len(non_docstring_body) > 1:
return {"valid": False, "error": f"Function {node.name} has implementation beyond stub"}

if len(non_docstring_body) == 1:
if not isinstance(non_docstring_body[0], ast.Pass):
return {"valid": False, "error": f"Function {node.name} body must be `pass`"}

return {"valid": True}

```
</constraints>
~~~

**File:** `.agent/rules/isp_traceability_required.md`

~~~markdown
---
name: "ISP Traceability Required"
description: "All classes/functions must reference parent TDD tags in docstrings via Implements or References section."
trigger: "glob"
globs: "src/**/*.py"
priority: "high"
---
<constraints>

## Enforcement Protocol: ISP Traceability Required

Verify docstrings contain traceability markers:

- `Implements:` section with TDD tag ID
- `References:` section with related tags
- `Ref:` inline reference (alternative syntax)

## Pattern Detection

> **Embedded Example Type:** Python docstring traceability pattern
```python

Implements
----------
TDD-5.2

```
Any entity missing these markers fails validation.
</constraints>
~~~

**File:** `.agent/rules/isp_numpy_docstring.md`

~~~markdown
---
name: "ISP Numpy Docstring"
description: "All docstrings must follow Numpy format with required sections."
trigger: "glob"
globs: "src/**/*.py"
priority: "high"
---
<constraints>

## Required Sections by Entity Type

### Functions

- Parameters
- Returns
- References

### Classes

- Attributes
- Implements

### Methods

- Parameters
- Implementation Notes
- References
</constraints>
~~~

#### 27.3.4.3 Associated Workflow Definitions

**File:** `.agent/workflows/isp_create_from_tdd.md`

~~~markdown
---
name: "Create ISP from TDD"
description: "Generate complete implementation stub from TDD blueprint with full traceability."
---

## Steps

1. **Validate TDD Exists** - Check tdd_tag exists in documentation
2. **Extract TDD Metadata** - Parse class_name, dependencies, methods
3. **Gather Related Tags** - Find ICD and SAD tags cited by TDD
4. **Generate Class Stub** - Invoke `generate_class_stub` tool
5. **Add Implementation Notes** - Invoke `add_implementation_hints` tool
6. **Inject Hints into Docstrings** - Enhance code with hints
7. **Validate Stub** - Invoke ISP_R1_Stub_Only rule
8. **Validate Traceability** - Invoke ISP_R2_Traceability_Required rule
9. **Format Code** - Apply Black formatter (line_length: 88)
10. **Present Stub** - Display generated code with next steps

## Completion Message

> **Embedded Example Type:** plaintext workflow completion message
```plaintext

Generated implementation stub for ${tdd_tag}.

Next steps:

1. Review docstrings for accuracy
2. Implement logic (replace `pass` statements)
3. Run type checker: mypy ${filename}
4. Run tests

```
## Verification Plan

- Generated file contains correct class/method signatures
- Numpy-style docstrings present for all entities
- `Implements:` tag correctly references parent TDD
- File passes `validate_stub` AST check
~~~

----------

## 27.4 Custom Script Resources

### 27.4.1 Tag Management Scripts

**Script:** `.agent/scripts/tag_create.py`

~~~markdown
# Tool: Create Tag

## Overview

Generates a new DDR tag with:

- Auto-assigned sequential ID within tier
- Properly formatted Sphinx-Needs RST directive
- Citation links to parent tags
- Tier compliance validation before creation

## Output Format

> **Embedded Example Type:** reStructuredText BRD directive output
```rst

.. brd:: Business requirement description
:id: BRD-5
:links: (none for root tier)

```
## Implementation

> **Embedded Example Type:** Python create_tag function implementation
```python

def create_tag(tier, content, parent_tags, block_id=None):
if block_id is None:
block_id = get_next_block_id(tier)

tag_id = f"{tier}-{block_id}"
citations_text = ", ".join(parent_tags)

formatted = (
f".. {tier.lower()}:: {content}\n"
f"   :id: {tag_id}\n"
f"   :links: {citations_text}\n"
)

validation = validate_tier_compliance(tier, content)
if not validation["valid"]:
raise ValueError(f"Tier violation: {validation['error']}")

return {"tag_id": tag_id, "formatted_content": formatted, "citations": parent_tags}

```
~~~

**Script:** `.agent/scripts/tag_update.py`

~~~markdown
# Tool: Update Tag

## Overview

Updates an existing tag with:

- Semantic diff analysis between old and new content
- Detection of affected child tags (downstream impact)
- Manifest dirty flagging if reconciliation needed
- Change logging for audit trail

## Implementation

> **Embedded Example Type:** Python update_tag function implementation
```python

def update_tag(tag_id, new_content, change_reason=None):
old_content = get_tag_content(tag_id)
affected_children = find_tags_citing(tag_id)
changes = analyze_semantic_changes(old_content, new_content)

reconciliation_required = (
changes["constraints_added"] or
changes["constraints_removed"] or
len(affected_children) > 0
)

set_tag_content(tag_id, new_content)

if reconciliation_required:
section = get_section_for_tag(tag_id)
set_manifest_dirty(section, tag_id, affected_children)

log_tag_modification(tag_id, old_content, new_content, change_reason)

return {
"tag_id": tag_id,
"affected_children": affected_children,
"reconciliation_required": reconciliation_required
}

```
~~~

**Script:** `.agent/scripts/tag_deprecate.py`

~~~markdown
# Tool: Deprecate Tag

## Overview

Marks a tag as deprecated with:

- DEPRECATED marker added to tag content
- Optional reference to replacement tag
- All children flagged for review
- Original ID preserved (never reused)

## Output Format

> **Embedded Example Type:** reStructuredText deprecated tag format
```rst

.. brd:: [DEPRECATED v2.0 → See BRD-10]
:id: BRD-5

Original content...

**Deprecation Reason:** Superseded by consolidated requirement.

```
~~~

**Script:** `.agent/scripts/tag_extract_citations.py`

~~~markdown
# Tool: Extract Citations

## Overview

Parses citation references from tag content following the `:links:` directive format.

## Implementation

> **Embedded Example Type:** Python extract_citations function
```python

import re

def extract_citations(content):
pattern = r':links:\s*([^\n]+)'
match = re.search(pattern, content)
if match:
return [t.strip() for t in match.group(1).split(',')]
return []

```
~~~

**Script:** `.agent/scripts/tag_find_citing.py`

~~~markdown
# Tool: Find Tags Citing

## Overview

Searches all documentation to find tags that cite the specified parent.
Used for downstream impact analysis during updates or deprecations.

## Output

> **Embedded Example Type:** JSON find_tags_citing output schema
```json

[
{"tag_id": "NFR-3", "tier": "NFR", "content_preview": "Performance..."},
{"tag_id": "FSD-7", "tier": "FSD", "content_preview": "Voice control..."}
]

```
~~~

### 27.4.2 Validation Scripts

**Script:** `.agent/scripts/validate_tier_compliance.py`

~~~markdown
# Tool: Validate Tier Compliance

## Overview

Checks content against tier-specific validation rules:

- **BRD**: No technology terms, must be business-focused
- **NFR**: Must contain numeric constraints
- **FSD**: No implementation code, behavior only
- **ICD**: Must define data structures/schemas
- **TDD**: Structure only, no algorithm logic
- **ISP**: Must be executable Python stubs

## Tier Rules

| Tier   | Forbidden Terms                               | Required Elements                     |
| ------ | --------------------------------------------- | ------------------------------------- |
| BRD    | ZeroMQ, ONNX, API, socket, thread, class, GPU | business value, stakeholder, metric   |
| NFR    | -                                             | metric, constraint, limit (+ numbers) |
| FSD    | zmq.ROUTER, onnxruntime, class, def           | behavior description                  |
| ICD    | -                                             | schema, format, contract              |
| TDD    | implementation, algorithm                     | class, method, component              |
| ISP    | -                                             | def, pass (must be code)              |
~~~

**Script:** `.agent/scripts/check_manifest_integrity.py`

~~~markdown
# Tool: Check Manifest Integrity

## Overview

Compares reconciliation manifests against actual documentation to detect:

- Tag count mismatches
- Missing tags (in docs but not manifest)
- Extra tags (in manifest but not docs)

## Output

> **Embedded Example Type:** JSON manifest integrity check output
```json

{
"accurate": false,
"manifest_count": 15,
"actual_count": 17,
"missing_tags": ["BRD-16", "BRD-17"],
"extra_tags": [],
"section": "brd-root"
}

```
~~~

**Script:** `.agent/scripts/detect_anti_patterns.py`

~~~markdown
# Tool: Detect Anti-Patterns

## Overview

Scans documentation for common mistakes:

| Pattern                 | Severity   | Description                       |
| ----------------------- | ---------- | --------------------------------- |
| `technology_in_brd`     | ERROR      | Technology terms in BRD tier      |
| `implementation_in_fsd` | ERROR      | Code/implementation in FSD tier   |
| `schema_in_sad`         | WARNING    | Code blocks in SAD tier           |
| `sibling_citation`      | ERROR      | Peer tags citing each other       |
| `missing_rationale`     | WARNING    | Design decision without "why"     |
| `vague_nfr`             | WARNING    | Qualitative terms without numbers |

## Output

> **Embedded Example Type:** JSON anti-pattern detection output
```json

{
"total_violations": 3,
"by_severity": {"error": 2, "warning": 1, "info": 0},
"violations": [
{"tag_id": "BRD-5", "pattern": "technology_in_brd", "severity": "error", "message": "...", "fix": "..."}
]
}

```
~~~

----------

## 27.5 Benefits Summary

### 27.5.1 For Human Developers

**Reduced Cognitive Load:**

- Agents handle tier classification automatically
- Real-time validation catches mistakes immediately
- Suggested parent tags eliminate manual searching

**Faster Documentation:**

- Complete feature workflow: 15-20 minutes (vs. 2-3 hours manual)
- Automated stub generation from blueprints
- Pre-filled traceability chains

**Higher Quality:**

- 100% traceability coverage (automated validation)
- Zero anti-pattern violations (real-time detection)
- Consistent terminology (glossary enforcement)

### 27.5.2 For AI Agents

**Structured Context:**

- Clear tier boundaries enable specialized expertise
- Tag-based retrieval provides precise context windows
- Reconciliation manifests track system state

**Verifiable Outputs:**

- Automated evaluation against ground truth
- Continuous validation feedback loop
- Measurable quality metrics

**Scalable Collaboration:**

- Agent hierarchy mirrors documentation hierarchy
- Parallel processing (BRD + NFR agents work simultaneously on different features)
- Conflict-free workflows (strict causal ordering)

### 27.5.3 For Project Maintainability

**Living Documentation:**

- Auto-updating manifests track inventory
- Dirty flags signal when reconciliation needed
- Version history preserved via immutable IDs

**Onboarding Efficiency:**

- New developers use Tag Navigator to explore
- Traceability graphs show "why" behind "what"
- Code stubs with implementation guidance

**Audit Compliance:**

- 100% traceable from code → business requirement
- Automated compliance reports
- Change history with rationale tracking

----------

## 27.6 Conclusion

The Antigravity agent asset definitions transform the DDR from a static documentation framework into a **dynamic, AI-assisted knowledge management system**. By encoding the rules, workflows, and validation logic into agent skills and rules, we enable:

1. **Automated Classification:** Unstructured information instantly routed to appropriate tier
2. **Real-Time Validation:** Mistakes caught during authoring, not in review
3. **Intelligent Assistance:** Context-aware suggestions based on current tier and content
4. **Complete Traceability:** Automated chain validation from ISP code stubs to BRD business cases
5. **Scalable Workflows:** End-to-end feature documentation in minutes, not hours

This integration creates a **human-AI collaborative development environment** where:

- **Humans** provide creative direction, domain expertise, and strategic decisions
- **AI Agents** enforce constraints, maintain consistency, and automate tedious tasks
- **The DDR** serves as the shared knowledge graph connecting both

The result is documentation that is not merely comprehensive, but **actively maintained, continuously validated, and genuinely useful** as both a human reference and a machine-parseable specification for LLM-assisted development.
