# Agent Tools Index

> Master lookup for all agent tool definitions.
>
> **Total Tools**: 23
>
> **Parent**: [`.agent/`](..)

## Quick Lookup

| File | Tool Name | Purpose | Confirmation |
| :----- | :---------- | :-------- | :------------- |
| [ddr_classify_information.md](ddr_classify_information.md) | `classify_information` | Classifies information fragments into DDR tiers using the decision tree algorithm | `never` |
| [ddr_scoring_matrix.md](ddr_scoring_matrix.md) | `scoring_matrix` | Resolves ambiguous tier classification using weighted scoring factors | `never` |
| [ddr_route_to_specialist.md](ddr_route_to_specialist.md) | `route_to_specialist` | Returns the specialist persona handle for a given DDR tier | `never` |
| [tag_create.md](tag_create.md) | `create_tag` | Generates a new DDR tag with UUID, validates tier, and enforces parent citation | `ask` |
| [tag_update.md](tag_update.md) | `update_tag` | Updates an existing DDR tag and marks affected children for reconciliation | `ask` |
| [tag_deprecate.md](tag_deprecate.md) | `deprecate_tag` | Marks a DDR tag as deprecated and optionally specifies a replacement | `ask` |
| [tag_find_citing.md](tag_find_citing.md) | `find_tags_citing` | Finds all DDR tags that cite a given tag as a parent | `never` |
| [tag_extract_citations.md](tag_extract_citations.md) | `extract_citations` | Extracts cited parent tags from a DDR tag's :links: directive | `never` |
| [trace_build_dependency_graph.md](trace_build_dependency_graph.md) | `build_dependency_graph` | Constructs DDR citation dependency graph with orphan and cycle detection | `never` |
| [trace_visualize.md](trace_visualize.md) | `visualize_traceability` | Generates Mermaid flowchart diagram of DDR traceability graph | `never` |
| [trace_generate_report.md](trace_generate_report.md) | `generate_traceability_report` | Analyzes DDR citation chains and generates violation reports | `never` |
| [validate_tier_compliance.md](validate_tier_compliance.md) | `validate_tier_compliance` | Validates DDR tag content against tier-specific constraints | `never` |
| [check_manifest_integrity.md](check_manifest_integrity.md) | `check_manifest_integrity` | Validates reconciliation manifest blocks against DDR structure requirements | `never` |
| [detect_anti_patterns.md](detect_anti_patterns.md) | `detect_anti_patterns` | Scans DDR tags for structural and content anti-patterns | `never` |
| [brd_abstract_to_business_value.md](brd_abstract_to_business_value.md) | `abstract_to_business_value` | Converts technology-specific terminology to business-appropriate language | `never` |
| [brd_derive_success_metrics.md](brd_derive_success_metrics.md) | `derive_success_metrics` | Generates quantifiable success metrics from business objectives | `never` |
| [isp_generate_class_stub.md](isp_generate_class_stub.md) | `generate_class_stub` | Generates Python class stub from TDD specification with Numpy-style docstring | `never` |
| [isp_generate_method_stub.md](isp_generate_method_stub.md) | `generate_method_stub` | Generates Python method stub with Numpy-style docstring and traceability | `never` |
| [isp_add_implementation_hints.md](isp_add_implementation_hints.md) | `add_implementation_hints` | Enriches ISP stub files with implementation guidance from TDD/ICD references | `never` |
| [rebuild_docs.md](rebuild_docs.md) | `rebuild_docs` | Rebuilds Sphinx documentation (HTML, needs.json) and logs all warnings | `never` |
| [generate_uuid.md](generate_uuid.md) | `generate_uuid` | Generates a Version 4 UUID string for sandbox concurrency paths | `never` |
| [clean_source.md](clean_source.md) | `clean_source` | **DESTRUCTIVE.** Surgically removes all docstrings and comments from a Python file | `always` |
| [ast_compare.md](ast_compare.md) | `ast_compare` | **SAFETY GATE.** Verifies no functional code logic changed between two file versions | `always` |

---

## By Category

### Classification & Routing (3)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [ddr_classify_information.md](ddr_classify_information.md) | `classify_information` | `never` | Tier assignment via decision tree |
| [ddr_scoring_matrix.md](ddr_scoring_matrix.md) | `scoring_matrix` | `never` | Ambiguity resolution via weighted scoring |
| [ddr_route_to_specialist.md](ddr_route_to_specialist.md) | `route_to_specialist` | `never` | Tier-to-persona delegation |

---

### Tag Lifecycle (3)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [tag_create.md](tag_create.md) | `create_tag` | `ask` | Tag creation with UUID and parent validation |
| [tag_update.md](tag_update.md) | `update_tag` | `ask` | Tag field update with reconciliation triggers |
| [tag_deprecate.md](tag_deprecate.md) | `deprecate_tag` | `ask` | Tag deprecation with migration instructions |

---

### Traceability & Impact (5)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [tag_find_citing.md](tag_find_citing.md) | `find_tags_citing` | `never` | Downstream citation discovery |
| [tag_extract_citations.md](tag_extract_citations.md) | `extract_citations` | `never` | Upstream parent extraction and orphan detection |
| [trace_build_dependency_graph.md](trace_build_dependency_graph.md) | `build_dependency_graph` | `never` | Full graph construction with cycle detection |
| [trace_visualize.md](trace_visualize.md) | `visualize_traceability` | `never` | Mermaid flowchart generation |
| [trace_generate_report.md](trace_generate_report.md) | `generate_traceability_report` | `never` | Violation reports with severity filtering |

---

### Validation & Compliance (3)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [validate_tier_compliance.md](validate_tier_compliance.md) | `validate_tier_compliance` | `never` | Tier-specific constraint enforcement |
| [check_manifest_integrity.md](check_manifest_integrity.md) | `check_manifest_integrity` | `never` | Reconciliation manifest validation |
| [detect_anti_patterns.md](detect_anti_patterns.md) | `detect_anti_patterns` | `never` | Structural and content anti-pattern scanning |

---

### BRD Tier Tools (2)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [brd_abstract_to_business_value.md](brd_abstract_to_business_value.md) | `abstract_to_business_value` | `never` | Technology term → business language conversion |
| [brd_derive_success_metrics.md](brd_derive_success_metrics.md) | `derive_success_metrics` | `never` | Vague objectives → quantifiable KPIs |

---

### ISP Tier Tools (3)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [isp_generate_class_stub.md](isp_generate_class_stub.md) | `generate_class_stub` | `never` | Python class stub from TDD with Numpy docstring |
| [isp_generate_method_stub.md](isp_generate_method_stub.md) | `generate_method_stub` | `never` | Python method stub with traceability links |
| [isp_add_implementation_hints.md](isp_add_implementation_hints.md) | `add_implementation_hints` | `never` | Hint injection from TDD/ICD references |

---

### Utility & Infrastructure (4)

| File | Tool Name | Confirmation | Purpose |
| :----- | :---------- | :------------- | :-------- |
| [rebuild_docs.md](rebuild_docs.md) | `rebuild_docs` | `never` | Sphinx rebuild (needs.json + HTML) — prerequisite for analysis tools |
| [generate_uuid.md](generate_uuid.md) | `generate_uuid` | `never` | UUID generation for sandbox concurrency paths |
| [clean_source.md](clean_source.md) | `clean_source` | `always` | **DESTRUCTIVE.** Docstring/comment stripping |
| [ast_compare.md](ast_compare.md) | `ast_compare` | `always` | **SAFETY GATE.** AST-level code integrity verification |

---

## Summary

| Category | Count |
| :--------- | ------: |
| Classification & Routing | 3 |
| Tag Lifecycle | 3 |
| Traceability & Impact | 5 |
| Validation & Compliance | 3 |
| BRD Tier Tools | 2 |
| ISP Tier Tools | 3 |
| Utility & Infrastructure | 4 |
| **Total** | **23** |
