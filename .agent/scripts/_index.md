# Agent Scripts Index

> Master registry of all automation script implementations.
>
> **Total Scripts**: 24
>
> **Package Init**: [`__init__.py`](__init__.py) (not counted — infrastructure only)
>
> **Parent**: [`.agent/`](..)

## Quick Lookup

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [abstract_to_business.py](abstract_to_business.py) | [`brd_abstract_to_business_value.md`](../tools/brd_abstract_to_business_value.md) | Converts technology-specific terminology to business language |
| [add_implementation_hints.py](add_implementation_hints.py) | [`isp_add_implementation_hints.md`](../tools/isp_add_implementation_hints.md) | Enriches ISP stubs with implementation guidance from TDD/ICD |
| [ast_compare.py](ast_compare.py) | [`ast_compare.md`](../tools/ast_compare.md) | **SAFETY GATE.** AST-level code integrity verification |
| [build_dependency_graph.py](build_dependency_graph.py) | [`trace_build_dependency_graph.md`](../tools/trace_build_dependency_graph.md) | Constructs DDR citation dependency graph with cycle detection |
| [check_manifest_integrity.py](check_manifest_integrity.py) | [`check_manifest_integrity.md`](../tools/check_manifest_integrity.md) | Validates reconciliation manifest blocks |
| [classify_information.py](classify_information.py) | [`ddr_classify_information.md`](../tools/ddr_classify_information.md) | Assigns DDR tier via decision tree algorithm |
| [clean_source.py](clean_source.py) | [`clean_source.md`](../tools/clean_source.md) | **DESTRUCTIVE.** Strips docstrings and comments from Python files |
| [create_tag.py](create_tag.py) | [`tag_create.md`](../tools/tag_create.md) | Generates new DDR tag with UUID and parent validation |
| [deprecate_tag.py](deprecate_tag.py) | [`tag_deprecate.md`](../tools/tag_deprecate.md) | Marks DDR tag as deprecated with optional replacement |
| [derive_success_metrics.py](derive_success_metrics.py) | [`brd_derive_success_metrics.md`](../tools/brd_derive_success_metrics.md) | Generates quantifiable success metrics from business objectives |
| [detect_anti_patterns.py](detect_anti_patterns.py) | [`detect_anti_patterns.md`](../tools/detect_anti_patterns.md) | Scans DDR tags for structural and content anti-patterns |
| [directory_tree.py](directory_tree.py) | — | Generates filtered directory tree with labels and reporting |
| [extract_citations.py](extract_citations.py) | [`tag_extract_citations.md`](../tools/tag_extract_citations.md) | Extracts cited parent tags from `:links:` directives |
| [find_tags_citing.py](find_tags_citing.py) | [`tag_find_citing.md`](../tools/tag_find_citing.md) | Finds all DDR tags citing a given parent tag |
| [generate_class_stub.py](generate_class_stub.py) | [`isp_generate_class_stub.md`](../tools/isp_generate_class_stub.md) | Generates Python class stub from TDD with Numpy docstring |
| [generate_llm_context.py](generate_llm_context.py) | — | Transforms `needs.json` into flattened Markdown for LLM context |
| [generate_method_stub.py](generate_method_stub.py) | [`isp_generate_method_stub.md`](../tools/isp_generate_method_stub.md) | Generates Python method stub with traceability links |
| [generate_traceability_report.py](generate_traceability_report.py) | [`trace_generate_report.md`](../tools/trace_generate_report.md) | Analyzes citation chains and generates violation reports |
| [generate_uuid.py](generate_uuid.py) | [`generate_uuid.md`](../tools/generate_uuid.md) | Generates Version 4 UUID for sandbox concurrency paths |
| [route_to_specialist.py](route_to_specialist.py) | [`ddr_route_to_specialist.md`](../tools/ddr_route_to_specialist.md) | Returns specialist persona handle for a given DDR tier |
| [scoring_matrix.py](scoring_matrix.py) | [`ddr_scoring_matrix.md`](../tools/ddr_scoring_matrix.md) | Resolves ambiguous tier classification via weighted scoring |
| [update_tag.py](update_tag.py) | [`tag_update.md`](../tools/tag_update.md) | Updates existing DDR tag; marks children for reconciliation |
| [validate_tier_compliance.py](validate_tier_compliance.py) | [`validate_tier_compliance.md`](../tools/validate_tier_compliance.md) | Validates DDR tag content against tier-specific constraints |
| [visualize_traceability.py](visualize_traceability.py) | [`trace_visualize.md`](../tools/trace_visualize.md) | Generates Mermaid flowchart of DDR traceability graph |

---

## By Category

### Classification & Routing (3)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [classify_information.py](classify_information.py) | [`ddr_classify_information.md`](../tools/ddr_classify_information.md) | Tier assignment via decision tree |
| [scoring_matrix.py](scoring_matrix.py) | [`ddr_scoring_matrix.md`](../tools/ddr_scoring_matrix.md) | Ambiguity resolution via weighted scoring |
| [route_to_specialist.py](route_to_specialist.py) | [`ddr_route_to_specialist.md`](../tools/ddr_route_to_specialist.md) | Tier-to-persona delegation |

---

### Tag Lifecycle (3)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [create_tag.py](create_tag.py) | [`tag_create.md`](../tools/tag_create.md) | Tag creation with UUID and parent validation |
| [update_tag.py](update_tag.py) | [`tag_update.md`](../tools/tag_update.md) | Tag field update with reconciliation triggers |
| [deprecate_tag.py](deprecate_tag.py) | [`tag_deprecate.md`](../tools/tag_deprecate.md) | Tag deprecation with migration instructions |

---

### Traceability & Impact (5)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [find_tags_citing.py](find_tags_citing.py) | [`tag_find_citing.md`](../tools/tag_find_citing.md) | Downstream citation discovery |
| [extract_citations.py](extract_citations.py) | [`tag_extract_citations.md`](../tools/tag_extract_citations.md) | Upstream parent extraction and orphan detection |
| [build_dependency_graph.py](build_dependency_graph.py) | [`trace_build_dependency_graph.md`](../tools/trace_build_dependency_graph.md) | Full graph construction with cycle detection |
| [visualize_traceability.py](visualize_traceability.py) | [`trace_visualize.md`](../tools/trace_visualize.md) | Mermaid flowchart generation |
| [generate_traceability_report.py](generate_traceability_report.py) | [`trace_generate_report.md`](../tools/trace_generate_report.md) | Violation reports with severity filtering |

---

### Validation & Compliance (3)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [validate_tier_compliance.py](validate_tier_compliance.py) | [`validate_tier_compliance.md`](../tools/validate_tier_compliance.md) | Tier-specific constraint enforcement |
| [check_manifest_integrity.py](check_manifest_integrity.py) | [`check_manifest_integrity.md`](../tools/check_manifest_integrity.md) | Reconciliation manifest validation |
| [detect_anti_patterns.py](detect_anti_patterns.py) | [`detect_anti_patterns.md`](../tools/detect_anti_patterns.md) | Structural and content anti-pattern scanning |

---

### BRD Tier Support (2)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [abstract_to_business.py](abstract_to_business.py) | [`brd_abstract_to_business_value.md`](../tools/brd_abstract_to_business_value.md) | Technology term → business language conversion |
| [derive_success_metrics.py](derive_success_metrics.py) | [`brd_derive_success_metrics.md`](../tools/brd_derive_success_metrics.md) | Vague objectives → quantifiable KPIs |

---

### ISP Tier Support (3)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [generate_class_stub.py](generate_class_stub.py) | [`isp_generate_class_stub.md`](../tools/isp_generate_class_stub.md) | Python class stub from TDD with Numpy docstring |
| [generate_method_stub.py](generate_method_stub.py) | [`isp_generate_method_stub.md`](../tools/isp_generate_method_stub.md) | Python method stub with traceability links |
| [add_implementation_hints.py](add_implementation_hints.py) | [`isp_add_implementation_hints.md`](../tools/isp_add_implementation_hints.md) | Hint injection from TDD/ICD references |

---

### Utility & Infrastructure (5)

| File | Tool Definition | Purpose |
|:-----|:----------------|:--------|
| [clean_source.py](clean_source.py) | [`clean_source.md`](../tools/clean_source.md) | **DESTRUCTIVE.** Docstring/comment stripping |
| [ast_compare.py](ast_compare.py) | [`ast_compare.md`](../tools/ast_compare.md) | **SAFETY GATE.** AST-level code integrity verification |
| [generate_uuid.py](generate_uuid.py) | [`generate_uuid.md`](../tools/generate_uuid.md) | UUID generation for sandbox concurrency paths |
| [directory_tree.py](directory_tree.py) | — | Directory structure visualization with filtering and labeling |
| [generate_llm_context.py](generate_llm_context.py) | — | Sphinx-Needs JSON → flattened LLM context Markdown |

---

## Summary

| Category | Count |
|:---------|------:|
| Classification & Routing | 3 |
| Tag Lifecycle | 3 |
| Traceability & Impact | 5 |
| Validation & Compliance | 3 |
| BRD Tier Support | 2 |
| ISP Tier Support | 3 |
| Utility & Infrastructure | 5 |
| **Total** | **24** |
