# Knowledge Source Index

> Master lookup table for topic-based navigation of DDR knowledge sources.
>
> **Total Files**: 45 (1 index + 44 content files)
>
> **Layer**: Static DDR Framework Knowledge (reusable across projects)
>
> For project-specific terminology, see: [`context/README.md`](../context/README.md)
>
> **Parent index**: [`knowledge/README.md`](../README.md)

## Quick Lookup

| Topic                          | Type       | Path                                        |
| :----------------------------- | :--------- | :------------------------------------------ |
| Glossary                       | vocabulary | `vocabulary/glossary.md`                    |
| DDR Overview                   | concept    | `concepts/ddr-overview.md`                  |
| Tier Hierarchy                 | concept    | `concepts/tier-hierarchy.md`                |
| Information Flow               | concept    | `concepts/information-flow.md`              |
| Tier: BRD                      | concept    | `concepts/tier-brd.md`                      |
| Tier: NFR                      | concept    | `concepts/tier-nfr.md`                      |
| Tier: FSD                      | concept    | `concepts/tier-fsd.md`                      |
| Tier: SAD                      | concept    | `concepts/tier-sad.md`                      |
| Tier: ICD                      | concept    | `concepts/tier-icd.md`                      |
| Tier: TDD                      | concept    | `concepts/tier-tdd.md`                      |
| Tier: ISP                      | concept    | `concepts/tier-isp.md`                      |
| Classification Decision Tree   | protocol   | `protocols/classification-decision-tree.md` |
| Classification Scoring         | protocol   | `protocols/classification-scoring.md`       |
| Abstraction Upward             | protocol   | `protocols/abstraction-upward.md`           |
| Abstraction Downward           | protocol   | `protocols/abstraction-downward.md`         |
| Abstraction Lateral            | protocol   | `protocols/abstraction-lateral.md`          |
| Traceability Chain             | protocol   | `protocols/traceability-chain.md`           |
| Impact Analysis                | protocol   | `protocols/impact-analysis.md`              |
| Reconciliation Dirty Flag      | protocol   | `protocols/reconciliation-dirty-flag.md`    |
| Reconciliation Inventory       | protocol   | `protocols/reconciliation-inventory.md`     |
| Tag Immutability               | constraint | `constraints/tag-immutability.md`           |
| Tag Citation Required          | constraint | `constraints/tag-citation-required.md`      |
| Sibling Prohibition            | constraint | `constraints/sibling-prohibition.md`        |
| BRD Technology Agnostic        | constraint | `constraints/brd-technology-agnostic.md`    |
| BRD Measurable Metrics         | constraint | `constraints/brd-measurable-metrics.md`     |
| NFR Numeric Constraints        | constraint | `constraints/nfr-numeric-constraints.md`    |
| FSD No Implementation          | constraint | `constraints/fsd-no-implementation.md`      |
| ISP Stub Only                  | constraint | `constraints/isp-stub-only.md`              |
| ISP Numpy Docstrings           | constraint | `constraints/isp-numpy-docstrings.md`       |
| Tag Syntax                     | pattern    | `patterns/tag-syntax.md`                    |
| Manifest Structure             | pattern    | `patterns/manifest-structure.md`            |
| Knowledge Source Template      | pattern    | `patterns/knowledge-source-template.md`     |
| Worked Example: Classification | pattern    | `patterns/worked-example-classification.md` |
| Worked Example: Feature        | pattern    | `patterns/worked-example-feature.md`        |
| Metadata Schema                | pattern    | `patterns/metadata-schema.md`               |
| Source Citation Style          | pattern    | `patterns/source-citation-style.md`         |
| Agent Registry                 | concept    | `concepts/agent-registry.md`                |
| Evaluation Framework           | pattern    | `patterns/evaluation-framework.md`          |
| Contextual Chunking            | pattern    | `patterns/llm-contextual-chunking.md`       |
| Validation Prompts             | pattern    | `patterns/llm-validation-prompts.md`        |
| Template: New Feature          | pattern    | `patterns/template-new-feature.md`          |
| Template: Bug Fix              | pattern    | `patterns/template-bug-fix.md`              |
| Workflow: Document Feature     | protocol   | `protocols/workflow-document-feature.md`    |
| Workflow: Orphan Resolution    | protocol   | `protocols/workflow-orphan-resolution.md`   |
| Trace Complete Chain           | protocol   | `protocols/trace-complete-chain.md`         |
| Tag Deprecation Lifecycle      | constraint | `constraints/tag-deprecation-lifecycle.md`  |

---

## By Archetype

### Concepts (11) ✅

- [DDR Overview](concepts/ddr-overview.md) — Purpose and principles
- [Tier Hierarchy](concepts/tier-hierarchy.md) — Seven-tier structure
- [Information Flow](concepts/information-flow.md) — Cascade and citation
- [Tier: BRD](concepts/tier-brd.md) — Business Requirements
- [Tier: NFR](concepts/tier-nfr.md) — Non-Functional Requirements
- [Tier: FSD](concepts/tier-fsd.md) — Feature Specifications
- [Tier: SAD](concepts/tier-sad.md) — System Architecture
- [Tier: ICD](concepts/tier-icd.md) — Interface Contracts
- [Tier: TDD](concepts/tier-tdd.md) — Technical Design
- [Tier: ISP](concepts/tier-isp.md) — Implementation Stubs
- [Agent Registry](concepts/agent-registry.md) — DDR agent handles and roles

### Protocols (12) ✅

- [Classification Decision Tree](protocols/classification-decision-tree.md) — Primary tier assignment
- [Classification Scoring](protocols/classification-scoring.md) — Ambiguity resolution
- [Abstraction Upward](protocols/abstraction-upward.md) — Parent synthesis
- [Abstraction Downward](protocols/abstraction-downward.md) — Child decomposition
- [Abstraction Lateral](protocols/abstraction-lateral.md) — Sibling generation
- [Traceability Chain](protocols/traceability-chain.md) — Chain validation
- [Impact Analysis](protocols/impact-analysis.md) — Downstream effects
- [Reconciliation Dirty Flag](protocols/reconciliation-dirty-flag.md) — Integrity status
- [Reconciliation Inventory](protocols/reconciliation-inventory.md) — Tag count sync
- [Workflow: Document Feature](protocols/workflow-document-feature.md) — End-to-end feature documentation
- [Workflow: Orphan Resolution](protocols/workflow-orphan-resolution.md) — Orphan tag resolution
- [Trace Complete Chain](protocols/trace-complete-chain.md) — ISP-to-BRD chain rule
- [Implementation Guardrails](protocols/implementation-guardrails.md) — Anti-hallucination execution protocol

### Constraints (10) ✅

- [Tag Immutability](constraints/tag-immutability.md) — IDs never change
- [Tag Citation Required](constraints/tag-citation-required.md) — Parent links mandatory
- [Sibling Prohibition](constraints/sibling-prohibition.md) — No peer citations
- [BRD Technology Agnostic](constraints/brd-technology-agnostic.md) — No tech terms
- [BRD Measurable Metrics](constraints/brd-measurable-metrics.md) — Quantifiable criteria
- [NFR Numeric Constraints](constraints/nfr-numeric-constraints.md) — Specific values
- [FSD No Implementation](constraints/fsd-no-implementation.md) — No code
- [ISP Stub Only](constraints/isp-stub-only.md) — Pass statements only
- [ISP Numpy Docstrings](constraints/isp-numpy-docstrings.md) — Required format
- [Tag Deprecation Lifecycle](constraints/tag-deprecation-lifecycle.md) — Deprecation rules

### Patterns (10) ✅

- [Knowledge Source Template](patterns/knowledge-source-template.md) — Authoring specification
- [Tag Syntax](patterns/tag-syntax.md) — ID format and RST directives
- [Manifest Structure](patterns/manifest-structure.md) — Reconciliation format
- [Worked Example: Classification](patterns/worked-example-classification.md) — Tier assignment demo
- [Worked Example: Feature](patterns/worked-example-feature.md) — End-to-end demo
- [Metadata Schema](patterns/metadata-schema.md) — Canonical validation fields and enums
- [Source Citation Style](patterns/source-citation-style.md) — Provenance citation standard
- [Evaluation Framework](patterns/evaluation-framework.md) — Agent evaluation metrics
- [Contextual Chunking](patterns/llm-contextual-chunking.md) — LLM context retrieval
- [Validation Prompts](patterns/llm-validation-prompts.md) — LLM prompt templates
- [Template: New Feature](patterns/template-new-feature.md) — 7-tier starter template
- [Template: Bug Fix](patterns/template-bug-fix.md) — Bug fix documentation

### Vocabulary (1) ✅

- [Glossary](vocabulary/glossary.md) — Normative terminology

---

## Progress Summary

| Archetype   | Created   | Planned   | Status      |
| :---------- | --------: | --------: | :---------- |
| Concepts    | 11        | 11        | ✅ Complete |
| Protocols   | 13        | 13        | ✅ Complete |
| Constraints | 10        | 10        | ✅ Complete |
| Patterns    | 10        | 10        | ✅ Complete |
| Vocabulary  | 1         | 1         | ✅ Complete |
| **Total**   | **46**    | **46**    | **100%**    |
