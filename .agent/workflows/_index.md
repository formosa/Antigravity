# Agent Workflows Index

> Master registry of all multi-step agent workflows.
>
> **Total Workflows**: 14
>
> **Parent**: [`.agent/`](..)

## Quick Lookup

| File                                                                 | Slug                         | Name                             | Mode          | Description                                                                                   |
| :------------------------------------------------------------------- | :--------------------------- | :------------------------------- | :------------ | :-------------------------------------------------------------------------------------------- |
| [brd_create_tag.md](brd_create_tag.md)                               | `/create_brd`                | Create BRD Tag                   | `autonomous`  | Author BRD tag with validation                                                                |
| [ddr_new_feature_documentation.md](ddr_new_feature_documentation.md) | `/document_feature`          | Document Feature (BRD→ISP)       | `autonomous`  | Complete seven-tier documentation workflow from Business Requirements to Implementation Stubs |
| [ddr_orphan_resolution.md](ddr_orphan_resolution.md)                 | `/resolve_orphan`            | Resolve Orphan Tag               | `autonomous`  | Synthesize missing parent or child tags to complete traceability chains                       |
| [document_script.md](document_script.md)                             | `/document_script`           | Document Script (Numpy-style)    | `autonomous`  | Orchestrator. Applies comprehensive Numpy-style docstrings                                    |
| [feature_documentation.md](feature_documentation.md)                 | `/complete_feature`          | Complete Feature Documentation   | `autonomous`  | Full 9-stage DDR workflow: Classify → BRD → NFR → FSD → SAD → ICD → TDD → ISP → Validate      |
| [fsd_create_tag.md](fsd_create_tag.md)                               | `/create_fsd`                | Create FSD Tag                   | `autonomous`  | Author FSD tag with validation                                                                |
| [icd_create_tag.md](icd_create_tag.md)                               | `/create_icd`                | Create ICD Tag                   | `autonomous`  | Author ICD tag with validation                                                                |
| [isp_create_from_tdd.md](isp_create_from_tdd.md)                     | `/create_isp`                | Create ISP from TDD              | `autonomous`  | Generate Python stub from Technical Design                                                    |
| [nfr_create_tag.md](nfr_create_tag.md)                               | `/create_nfr`                | Create NFR Tag                   | `autonomous`  | Author NFR tag with validation                                                                |
| [sad_create_tag.md](sad_create_tag.md)                               | `/create_sad`                | Create SAD Tag                   | `autonomous`  | Author SAD tag with validation                                                                |
| [tdd_create_tag.md](tdd_create_tag.md)                               | `/create_tdd`                | Create TDD Tag                   | `autonomous`  | Author TDD tag with validation                                                                |
| [trace_comprehensive_audit.md](trace_comprehensive_audit.md)         | `/audit_traceability`        | Comprehensive Traceability Audit | `autonomous`  | Full DDR tag validation for completeness, integrity, and chain validity                       |
| [trace_tag_to_root.md](trace_tag_to_root.md)                         | `/trace_tag`                 | Trace Tag to Root                | `autonomous`  | Display citation chain from tag to BRD root                                                   |
| [update_documentation_spec.md](update_documentation_spec.md)         | `/update_documentation_spec` | Update Documentation Spec        | `interactive` | Process for updating the Maggie Design Specifications (Sphinx-Needs)                          |

---

## By Category

### End-to-End Documentation Flows (3)

| File                                                                 | Slug                         | Mode          | Purpose                            |
| :------------------------------------------------------------------- | :--------------------------- | :------------ | :--------------------------------- |
| [feature_documentation.md](feature_documentation.md)                 | `/complete_feature`          | `autonomous`  | Full 9-stage DDR cascade           |
| [ddr_new_feature_documentation.md](ddr_new_feature_documentation.md) | `/document_feature`          | `autonomous`  | 7-tier BRD→ISP documentation       |
| [update_documentation_spec.md](update_documentation_spec.md)         | `/update_documentation_spec` | `interactive` | Sphinx-Needs specification updates |

---

### Tag Authorship (6)

| File                                   | Slug          | Tier   | Purpose                     |
| :------------------------------------- | :------------ | :----- | :-------------------------- |
| [brd_create_tag.md](brd_create_tag.md) | `/create_brd` | BRD    | Business Requirements       |
| [nfr_create_tag.md](nfr_create_tag.md) | `/create_nfr` | NFR    | Non-Functional Requirements |
| [fsd_create_tag.md](fsd_create_tag.md) | `/create_fsd` | FSD    | Functional Specifications   |
| [sad_create_tag.md](sad_create_tag.md) | `/create_sad` | SAD    | System Architecture         |
| [icd_create_tag.md](icd_create_tag.md) | `/create_icd` | ICD    | Interface Contracts         |
| [tdd_create_tag.md](tdd_create_tag.md) | `/create_tdd` | TDD    | Technical Design            |

---

### Code Generation & Documentation (2)

| File                                             | Slug               | Purpose                           |
| :----------------------------------------------- | :----------------- | :-------------------------------- |
| [isp_create_from_tdd.md](isp_create_from_tdd.md) | `/create_isp`      | Python stub generation from TDD   |
| [document_script.md](document_script.md)         | `/document_script` | Numpy-style docstring application |

---

### Traceability & Validation (3)

| File                                                         | Slug                  | Purpose                                      |
| :----------------------------------------------------------- | :-------------------- | :------------------------------------------- |
| [trace_comprehensive_audit.md](trace_comprehensive_audit.md) | `/audit_traceability` | Full chain audit with anti-pattern detection |
| [trace_tag_to_root.md](trace_tag_to_root.md)                 | `/trace_tag`          | Upstream citation lineage                    |
| [ddr_orphan_resolution.md](ddr_orphan_resolution.md)         | `/resolve_orphan`     | Missing link synthesis                       |

---

## Summary

| Category                        | Count   |
| :------------------------------ | ------: |
| End-to-End Documentation Flows  | 3       |
| Tag Authorship                  | 6       |
| Code Generation & Documentation | 2       |
| Traceability & Validation       | 3       |
| **Total**                       | **14**  |