# Rules Index

> Master lookup for all agent enforcement rules.
>
> **Total Rules**: 21 (post-optimization)
>
> **Schema**: [`antigravity_types.d.ts`](../assets/antigravity_types.d.ts)
>
> **Parent**: [`.agent/`](..)

## Priority Bands

| Band | Range | Meaning |
| :----- | :------ | :-------- |
| Critical | 90–100 | Safety, immutability, data integrity |
| Standard | 60–89 | Tier enforcement, traceability |
| Advisory | 30–59 | Classification, maintenance, planning |

## Activation Summary

| Mode | Count | Purpose |
| :----- | ------: | :-------- |
| Always On | 4 | Safety constraints, ID immutability, Execution protocols |
| Glob | 15 | Tier-scoped doc enforcement |
| Model Decision | 2 | Contextual application during doc work |

## By Category

### System Rules (2) — Always On, Priority 100

| File | Purpose |
| :----- | :-------- |
| [sys_protected_files.md](sys_protected_files.md) | `.agent/assets/` write protection |
| [sys_antigravity_types.md](sys_antigravity_types.md) | Schema compliance enforcement |

---

### Execution Rules (1) — Always On, Priority 100

| File | Purpose |
| :----- | :-------- |
| [execution_protocol.md](execution_protocol.md) | Shell & Python execution constraints |

---

### DDR Core Rules (3) — Mixed Activation

| File | Activation | Priority | Purpose |
| :----- | :----------- | :--------- | :-------- |
| [ddr_id_immutability.md](ddr_id_immutability.md) | Always On | 100 | Tag ID immutability |
| [ddr_tier_classification.md](ddr_tier_classification.md) | Model Decision | 50 | Classification decision tree |
| [ddr_manifest_integrity.md](ddr_manifest_integrity.md) | Model Decision | 50 | Reconciliation manifest sync |

---

### Traceability Rules (4) — Glob, Priority 85–90

| File | Priority | Purpose |
| :----- | :--------- | :-------- |
| [trace_complete_chain.md](trace_complete_chain.md) | 90 | Complete chain to BRD root |
| [trace_no_forward_references.md](trace_no_forward_references.md) | 85 | No downward citations |
| [trace_no_sibling_citations.md](trace_no_sibling_citations.md) | 85 | No peer citations |
| [ddr_traceability_mandate.md](ddr_traceability_mandate.md) | 85 | Parent citation required |

---

### BRD Tier Rules (3) — Glob, Priority 70–80

| File | Severity | Priority | Purpose |
| :----- | :--------- | :--------- | :-------- |
| [brd_technology_agnostic.md](brd_technology_agnostic.md) | Mandatory | 80 | No tech terms in BRD |
| [brd_measurable_metrics.md](brd_measurable_metrics.md) | Mandatory | 80 | Quantifiable success criteria |
| [brd_stakeholder_focus.md](brd_stakeholder_focus.md) | Guideline | 70 | Stakeholder identification |

---

### NFR Tier Rules (1) — Glob, Priority 80

| File | Purpose |
| :----- | :-------- |
| [nfr_numeric_targets.md](nfr_numeric_targets.md) | Numeric targets with RFC 2119 |

---

### FSD / SAD / ICD Tier Rules (3) — Glob, Priority 80

| File | Purpose |
| :----- | :-------- |
| [fsd_behavioral_specs.md](fsd_behavioral_specs.md) | User-perspective behavioral specs |
| [sad_architecture_topology.md](sad_architecture_topology.md) | Architecture pattern + ASCII diagram |
| [icd_interface_contracts.md](icd_interface_contracts.md) | Language-agnostic data shapes |

---

### TDD / ISP Tier Rules (4) — Glob, Priority 80

| File | Purpose |
| :----- | :-------- |
| [tdd_structural_blueprints.md](tdd_structural_blueprints.md) | Structure without implementation logic |
| [isp_stub_only.md](isp_stub_only.md) | Pass-only method bodies |
| [isp_numpy_docstring.md](isp_numpy_docstring.md) | Numpy-style docstring format |
| [isp_traceability_required.md](isp_traceability_required.md) | Implements/Requirements citations |

---
