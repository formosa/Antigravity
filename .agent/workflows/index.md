# Agent Workflows Index

> Master registry of all multi-step agent workflows.
>
> **Total Workflows**: 14
>
> **Parent**: [`.agent/`](..)

## Quick Lookup

| File                                                                 | Slug                         | Name                             | Mode          | Description                                                                                   |
| :------------------------------------------------------------------- | :--------------------------- | :------------------------------- | :------------ | :-------------------------------------------------------------------------------------------- |
| [brd-create-tag.md](brd-create-tag.md)                               | `/create_brd`                | Create BRD Tag                   | `autonomous`  | Author BRD tag with validation                                                                |
| [ddr-new-feature-documentation.md](ddr-new-feature-documentation.md) | `/document_feature`          | Document Feature (BRD→ISP)       | `autonomous`  | Complete seven-tier documentation workflow from Business Requirements to Implementation Stubs |
| [ddr-orphan-resolution.md](ddr-orphan-resolution.md)                 | `/resolve_orphan`            | Resolve Orphan Tag               | `autonomous`  | Synthesize missing parent or child tags to complete traceability chains                       |
| [document-script.md](document-script.md)                             | `/document_script`           | Document Script (Numpy-style)    | `autonomous`  | Orchestrator. Applies comprehensive Numpy-style docstrings                                    |
| [feature-documentation.md](feature-documentation.md)                 | `/complete_feature`          | Complete Feature Documentation   | `autonomous`  | Full 9-stage DDR workflow: Classify → BRD → NFR → FSD → SAD → ICD → TDD → ISP → Validate      |
| [fsd-create-tag.md](fsd-create-tag.md)                               | `/create_fsd`                | Create FSD Tag                   | `autonomous`  | Author FSD tag with validation                                                                |
| [icd-create-tag.md](icd-create-tag.md)                               | `/create_icd`                | Create ICD Tag                   | `autonomous`  | Author ICD tag with validation                                                                |
| [isp-create-from-tdd.md](isp-create-from-tdd.md)                     | `/create_isp`                | Create ISP from TDD              | `autonomous`  | Generate Python stub from Technical Design                                                    |
| [nfr-create-tag.md](nfr-create-tag.md)                               | `/create_nfr`                | Create NFR Tag                   | `autonomous`  | Author NFR tag with validation                                                                |
| [sad-create-tag.md](sad-create-tag.md)                               | `/create_sad`                | Create SAD Tag                   | `autonomous`  | Author SAD tag with validation                                                                |
| [tdd-create-tag.md](tdd-create-tag.md)                               | `/create_tdd`                | Create TDD Tag                   | `autonomous`  | Author TDD tag with validation                                                                |
| [trace-comprehensive-audit.md](trace-comprehensive-audit.md)         | `/audit_traceability`        | Comprehensive Traceability Audit | `autonomous`  | Full DDR tag validation for completeness, integrity, and chain validity                       |
| [trace-tag-to-root.md](trace-tag-to-root.md)                         | `/trace_tag`                 | Trace Tag to Root                | `autonomous`  | Display citation chain from tag to BRD root                                                   |
| [update-documentation-spec.md](update-documentation-spec.md)         | `/update_documentation_spec` | Update Documentation Spec        | `interactive` | Process for updating the Maggie Design Specifications (Sphinx-Needs)                          |

---

## By Category

### End-to-End Documentation Flows (3)

| File                                                                 | Slug                         | Mode          | Purpose                            |
| :------------------------------------------------------------------- | :--------------------------- | :------------ | :--------------------------------- |
| [feature-documentation.md](feature-documentation.md)                 | `/complete_feature`          | `autonomous`  | Full 9-stage DDR cascade           |
| [ddr-new-feature-documentation.md](ddr-new-feature-documentation.md) | `/document_feature`          | `autonomous`  | 7-tier BRD→ISP documentation       |
| [update-documentation-spec.md](update-documentation-spec.md)         | `/update_documentation_spec` | `interactive` | Sphinx-Needs specification updates |

---

### Tag Authorship (6)

| File                                   | Slug          | Tier   | Purpose                     |
| :------------------------------------- | :------------ | :----- | :-------------------------- |
| [brd-create-tag.md](brd-create-tag.md) | `/create_brd` | BRD    | Business Requirements       |
| [nfr-create-tag.md](nfr-create-tag.md) | `/create_nfr` | NFR    | Non-Functional Requirements |
| [fsd-create-tag.md](fsd-create-tag.md) | `/create_fsd` | FSD    | Functional Specifications   |
| [sad-create-tag.md](sad-create-tag.md) | `/create_sad` | SAD    | System Architecture         |
| [icd-create-tag.md](icd-create-tag.md) | `/create_icd` | ICD    | Interface Contracts         |
| [tdd-create-tag.md](tdd-create-tag.md) | `/create_tdd` | TDD    | Technical Design            |

---

### Code Generation & Documentation (2)

| File                                             | Slug               | Purpose                           |
| :----------------------------------------------- | :----------------- | :-------------------------------- |
| [isp-create-from-tdd.md](isp-create-from-tdd.md) | `/create_isp`      | Python stub generation from TDD   |
| [document-script.md](document-script.md)         | `/document_script` | Numpy-style docstring application |

---

### Traceability & Validation (3)

| File                                                         | Slug                  | Purpose                                      |
| :----------------------------------------------------------- | :-------------------- | :------------------------------------------- |
| [trace-comprehensive-audit.md](trace-comprehensive-audit.md) | `/audit_traceability` | Full chain audit with anti-pattern detection |
| [trace-tag-to-root.md](trace-tag-to-root.md)                 | `/trace_tag`          | Upstream citation lineage                    |
| [ddr-orphan-resolution.md](ddr-orphan-resolution.md)         | `/resolve_orphan`     | Missing link synthesis                       |

---

## Summary

| Category                        | Count   |
| :------------------------------ | ------: |
| End-to-End Documentation Flows  | 3       |
| Tag Authorship                  | 6       |
| Code Generation & Documentation | 2       |
| Traceability & Validation       | 3       |
| **Total**                       | **14**  |