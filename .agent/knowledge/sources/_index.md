# Knowledge Source Index

> Master lookup table for topic-based navigation of DDR knowledge sources.
>
> **Total Files**: 46 (1 index + 45 content files)
>
> **Layer**: Static DDR Framework Knowledge (reusable across projects)
>
> For project-specific terminology, see: [`context/_index.md`](../context/_index.md)
>
> **Parent index**: [`knowledge/_index.md`](../_index.md)

## Quick Lookup

| Topic | Type | Path |
|:------|:-----|:-----|
| Glossary | vocabulary | `vocabulary/glossary.md` |
| DDR Overview | concept | `concepts/ddr_overview.md` |
| Tier Hierarchy | concept | `concepts/tier_hierarchy.md` |
| Information Flow | concept | `concepts/information_flow.md` |
| Tier: BRD | concept | `concepts/tier_brd.md` |
| Tier: NFR | concept | `concepts/tier_nfr.md` |
| Tier: FSD | concept | `concepts/tier_fsd.md` |
| Tier: SAD | concept | `concepts/tier_sad.md` |
| Tier: ICD | concept | `concepts/tier_icd.md` |
| Tier: TDD | concept | `concepts/tier_tdd.md` |
| Tier: ISP | concept | `concepts/tier_isp.md` |
| Classification Decision Tree | protocol | `protocols/classification_decision_tree.md` |
| Classification Scoring | protocol | `protocols/classification_scoring.md` |
| Abstraction Upward | protocol | `protocols/abstraction_upward.md` |
| Abstraction Downward | protocol | `protocols/abstraction_downward.md` |
| Abstraction Lateral | protocol | `protocols/abstraction_lateral.md` |
| Traceability Chain | protocol | `protocols/traceability_chain.md` |
| Impact Analysis | protocol | `protocols/impact_analysis.md` |
| Reconciliation Dirty Flag | protocol | `protocols/reconciliation_dirty_flag.md` |
| Reconciliation Inventory | protocol | `protocols/reconciliation_inventory.md` |
| Tag Immutability | constraint | `constraints/tag_immutability.md` |
| Tag Citation Required | constraint | `constraints/tag_citation_required.md` |
| Sibling Prohibition | constraint | `constraints/sibling_prohibition.md` |
| BRD Technology Agnostic | constraint | `constraints/brd_technology_agnostic.md` |
| BRD Measurable Metrics | constraint | `constraints/brd_measurable_metrics.md` |
| NFR Numeric Constraints | constraint | `constraints/nfr_numeric_constraints.md` |
| FSD No Implementation | constraint | `constraints/fsd_no_implementation.md` |
| ISP Stub Only | constraint | `constraints/isp_stub_only.md` |
| ISP Numpy Docstrings | constraint | `constraints/isp_numpy_docstrings.md` |
| Tag Syntax | pattern | `patterns/tag_syntax.md` |
| Manifest Structure | pattern | `patterns/manifest_structure.md` |
| Knowledge Source Template | pattern | `patterns/knowledge_source_template.md` |
| Worked Example: Classification | pattern | `patterns/worked_example_classification.md` |
| Worked Example: Feature | pattern | `patterns/worked_example_feature.md` |
| Persona Content Strategy | pattern | `patterns/persona_content_strategy.md` |
| Agent Registry | concept | `concepts/agent_registry.md` |
| Evaluation Framework | pattern | `patterns/evaluation_framework.md` |
| Contextual Chunking | pattern | `patterns/llm_contextual_chunking.md` |
| Validation Prompts | pattern | `patterns/llm_validation_prompts.md` |
| Template: New Feature | pattern | `patterns/template_new_feature.md` |
| Template: Bug Fix | pattern | `patterns/template_bug_fix.md` |
| Workflow: Document Feature | protocol | `protocols/workflow_document_feature.md` |
| Workflow: Orphan Resolution | protocol | `protocols/workflow_orphan_resolution.md` |
| Trace Complete Chain | protocol | `protocols/trace_complete_chain.md` |
| Tag Deprecation Lifecycle | constraint | `constraints/tag_deprecation_lifecycle.md` |

---

## By Archetype

### Concepts (11) ✅
- [DDR Overview](concepts/ddr_overview.md) — Purpose and principles
- [Tier Hierarchy](concepts/tier_hierarchy.md) — Seven-tier structure
- [Information Flow](concepts/information_flow.md) — Cascade and citation
- [Tier: BRD](concepts/tier_brd.md) — Business Requirements
- [Tier: NFR](concepts/tier_nfr.md) — Non-Functional Requirements
- [Tier: FSD](concepts/tier_fsd.md) — Feature Specifications
- [Tier: SAD](concepts/tier_sad.md) — System Architecture
- [Tier: ICD](concepts/tier_icd.md) — Interface Contracts
- [Tier: TDD](concepts/tier_tdd.md) — Technical Design
- [Tier: ISP](concepts/tier_isp.md) — Implementation Stubs
- [Agent Registry](concepts/agent_registry.md) — DDR agent handles and roles

### Protocols (12) ✅
- [Classification Decision Tree](protocols/classification_decision_tree.md) — Primary tier assignment
- [Classification Scoring](protocols/classification_scoring.md) — Ambiguity resolution
- [Abstraction Upward](protocols/abstraction_upward.md) — Parent synthesis
- [Abstraction Downward](protocols/abstraction_downward.md) — Child decomposition
- [Abstraction Lateral](protocols/abstraction_lateral.md) — Sibling generation
- [Traceability Chain](protocols/traceability_chain.md) — Chain validation
- [Impact Analysis](protocols/impact_analysis.md) — Downstream effects
- [Reconciliation Dirty Flag](protocols/reconciliation_dirty_flag.md) — Integrity status
- [Reconciliation Inventory](protocols/reconciliation_inventory.md) — Tag count sync
- [Workflow: Document Feature](protocols/workflow_document_feature.md) — End-to-end feature documentation
- [Workflow: Orphan Resolution](protocols/workflow_orphan_resolution.md) — Orphan tag resolution
- [Trace Complete Chain](protocols/trace_complete_chain.md) — ISP-to-BRD chain rule

### Constraints (10) ✅
- [Tag Immutability](constraints/tag_immutability.md) — IDs never change
- [Tag Citation Required](constraints/tag_citation_required.md) — Parent links mandatory
- [Sibling Prohibition](constraints/sibling_prohibition.md) — No peer citations
- [BRD Technology Agnostic](constraints/brd_technology_agnostic.md) — No tech terms
- [BRD Measurable Metrics](constraints/brd_measurable_metrics.md) — Quantifiable criteria
- [NFR Numeric Constraints](constraints/nfr_numeric_constraints.md) — Specific values
- [FSD No Implementation](constraints/fsd_no_implementation.md) — No code
- [ISP Stub Only](constraints/isp_stub_only.md) — Pass statements only
- [ISP Numpy Docstrings](constraints/isp_numpy_docstrings.md) — Required format
- [Tag Deprecation Lifecycle](constraints/tag_deprecation_lifecycle.md) — Deprecation rules

### Patterns (11) ✅
- [Knowledge Source Template](patterns/knowledge_source_template.md) — Authoring specification
- [Tag Syntax](patterns/tag_syntax.md) — ID format and RST directives
- [Manifest Structure](patterns/manifest_structure.md) — Reconciliation format
- [Worked Example: Classification](patterns/worked_example_classification.md) — Tier assignment demo
- [Worked Example: Feature](patterns/worked_example_feature.md) — End-to-end demo
- [Persona Content Strategy](patterns/persona_content_strategy.md) — Inline vs. refs decision
- [Evaluation Framework](patterns/evaluation_framework.md) — Agent evaluation metrics
- [Contextual Chunking](patterns/llm_contextual_chunking.md) — LLM context retrieval
- [Validation Prompts](patterns/llm_validation_prompts.md) — LLM prompt templates
- [Template: New Feature](patterns/template_new_feature.md) — 7-tier starter template
- [Template: Bug Fix](patterns/template_bug_fix.md) — Bug fix documentation

### Vocabulary (1) ✅
- [Glossary](vocabulary/glossary.md) — Normative terminology

---

## Progress Summary

| Archetype | Created | Planned | Status |
|:----------|--------:|--------:|:-------|
| Concepts | 11 | 11 | ✅ Complete |
| Protocols | 12 | 12 | ✅ Complete |
| Constraints | 10 | 10 | ✅ Complete |
| Patterns | 11 | 11 | ✅ Complete |
| Vocabulary | 1 | 1 | ✅ Complete |
| **Total** | **46** | **46** | **100%** |
