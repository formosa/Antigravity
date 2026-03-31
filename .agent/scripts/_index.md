# Agent Scripts Index

> Master registry of durable automation script implementations.
>
> **Total Scripts**: 6
>
> **Package Init**: [`__init__.py`](__init__.py) (not counted — infrastructure only)
>
> **Parent**: [`.agent/`](..)

## Quick Lookup

| File                                                     | Tool Definition                                                               | Purpose                                                           |
| :------------------------------------------------------- | :---------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| [add_implementation_hints.py](add_implementation_hints.py) | —                                                                             | Enriches ISP stubs with implementation guidance from TDD/ICD      |
| [audit_ddr_v6_3_markdown.py](audit_ddr_v6_3_markdown.py) | —                                                                             | Audits DDR v6.3 Markdown parity against authoritative YAML inputs |
| [build_dependency_graph.py](build_dependency_graph.py)   | —                                                                             | Constructs DDR citation dependency graph with cycle detection     |
| [cleanup_temp_assets.py](cleanup_temp_assets.py)         | [`cleanup_temp_assets.md`](../tools/cleanup_temp_assets.md)                   | Audits and optionally removes stale temp run directories          |
| [directory_tree.py](directory_tree.py)                   | —                                                                             | Generates filtered directory tree with labels and reporting       |
| [generate_uuid.py](generate_uuid.py)                     | [`generate_uuid.md`](../tools/generate_uuid.md)                               | Generates UUID strings for temp run-directory construction        |

---

## By Category

### Traceability & Analysis (2)

| File                                                   | Tool Definition                                                               | Purpose                                         |
| :----------------------------------------------------- | :---------------------------------------------------------------------------- | :---------------------------------------------- |
| [build_dependency_graph.py](build_dependency_graph.py) | —                                                                             | Full graph construction with cycle detection    |
| [directory_tree.py](directory_tree.py)                 | —                                                                             | Directory structure visualization with labeling |

---

### Validation & Compliance (1)

| File                                                     | Tool Definition | Purpose                                      |
| :------------------------------------------------------- | :-------------- | :------------------------------------------- |
| [audit_ddr_v6_3_markdown.py](audit_ddr_v6_3_markdown.py) | —               | Canonical Markdown parity audit for DDR v6.3 |

---

### ISP Tier Support (1)

| File                                                         | Tool Definition                                                               | Purpose                                |
| :----------------------------------------------------------- | :---------------------------------------------------------------------------- | :------------------------------------- |
| [add_implementation_hints.py](add_implementation_hints.py)   | —                                                                             | Hint injection from TDD/ICD references |

---

### Utility & Infrastructure (2)

| File                                               | Tool Definition                                                     | Purpose                                            |
| :------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------- |
| [cleanup_temp_assets.py](cleanup_temp_assets.py)   | [`cleanup_temp_assets.md`](../tools/cleanup_temp_assets.md)         | Temp workspace audit and cleanup                   |
| [generate_uuid.py](generate_uuid.py)               | [`generate_uuid.md`](../tools/generate_uuid.md)                     | UUID generation for temp run-directory construction |

---

## Summary

| Category                 | Count   |
| :----------------------- | ------: |
| Traceability & Analysis  | 2       |
| Validation & Compliance  | 1       |
| ISP Tier Support         | 1       |
| Utility & Infrastructure | 2       |
| **Total**                | **6**   |
