# Rules Index

> Master lookup for all agent enforcement rules.
>
> **Total Rules**: 21 (post-optimization)
>
> **Schema**: [`rule.d.ts`](../assets/schemas/rule/rule.d.ts)
>
> **Parent**: [`.agent/`](..)

## Priority Bands

| Band     | Range   | Meaning                               |
| :------- | :------ | :------------------------------------ |
| Critical | 90–100  | Safety, immutability, data integrity  |
| Standard | 60–89   | Tier enforcement, traceability        |
| Advisory | 30–59   | Classification, maintenance, planning |

## Activation Summary

| Mode           | Count   | Purpose                                                  |
| :------------- | ------: | :------------------------------------------------------- |
| Always On      | 4       | Safety constraints, ID immutability, Execution protocols |
| Glob           | 15      | Tier-scoped doc enforcement                              |
| Model Decision | 2       | Contextual application during doc work                   |

## By Category

### System Rules (2) — Always On, Priority 100

| File                                                 | Purpose                           |
| :--------------------------------------------------- | :-------------------------------- |
| [dev-protected-files.md](dev-protected-files.md)     | `.agent/assets/` write protection |
| [dev-antigravity-types.md](dev-antigravity-types.md) | Schema compliance enforcement     |

---

### Execution Rules (1) — Always On, Priority 100

| File                                           | Purpose                              |
| :--------------------------------------------- | :----------------------------------- |
| [execution-protocol.md](execution-protocol.md) | Shell & Python execution constraints |

---

### DDR Core Rules (3) — Mixed Activation

| File                                                     | Activation     | Priority   | Purpose                      |
| :------------------------------------------------------- | :------------- | :--------- | :--------------------------- |
| [ddr-id-immutability.md](ddr-id-immutability.md)         | Always On      | 100        | Tag ID immutability          |
| [ddr-tier-classification.md](ddr-tier-classification.md) | Model Decision | 50         | Classification decision tree |
| [ddr-manifest-integrity.md](ddr-manifest-integrity.md)   | Model Decision | 50         | Reconciliation manifest sync |

---

### Traceability Rules (4) — Glob, Priority 85–90

| File                                                             | Priority   | Purpose                    |
| :--------------------------------------------------------------- | :--------- | :------------------------- |
| [trace-complete-chain.md](trace-complete-chain.md)               | 90         | Complete chain to BRD root |
| [trace-no-forward-references.md](trace-no-forward-references.md) | 85         | No downward citations      |
| [trace-no-sibling-citations.md](trace-no-sibling-citations.md)   | 85         | No peer citations          |
| [ddr-traceability-mandate.md](ddr-traceability-mandate.md)       | 85         | Parent citation required   |

---

### BRD Tier Rules (3) — Glob, Priority 70–80

| File                                                     | Severity   | Priority   | Purpose                       |
| :------------------------------------------------------- | :--------- | :--------- | :---------------------------- |
| [brd-technology-agnostic.md](brd-technology-agnostic.md) | Mandatory  | 80         | No tech terms in BRD          |
| [brd-measurable-metrics.md](brd-measurable-metrics.md)   | Mandatory  | 80         | Quantifiable success criteria |
| [brd-stakeholder-focus.md](brd-stakeholder-focus.md)     | Guideline  | 70         | Stakeholder identification    |

---

### NFR Tier Rules (1) — Glob, Priority 80

| File                                             | Purpose                       |
| :----------------------------------------------- | :---------------------------- |
| [nfr-numeric-targets.md](nfr-numeric-targets.md) | Numeric targets with RFC 2119 |

---

### FSD / SAD / ICD Tier Rules (3) — Glob, Priority 80

| File                                                         | Purpose                              |
| :----------------------------------------------------------- | :----------------------------------- |
| [fsd-behavioral-specs.md](fsd-behavioral-specs.md)           | User-perspective behavioral specs    |
| [sad-architecture-topology.md](sad-architecture-topology.md) | Architecture pattern + ASCII diagram |
| [icd-interface-contracts.md](icd-interface-contracts.md)     | Language-agnostic data shapes        |

---

### TDD / ISP Tier Rules (4) — Glob, Priority 80

| File                                                         | Purpose                                |
| :----------------------------------------------------------- | :------------------------------------- |
| [tdd-structural-blueprints.md](tdd-structural-blueprints.md) | Structure without implementation logic |
| [isp-stub-only.md](isp-stub-only.md)                         | Pass-only method bodies                |
| [isp-numpy-docstring.md](isp-numpy-docstring.md)             | Numpy-style docstring format           |
| [isp-traceability-required.md](isp-traceability-required.md) | Implements/Requirements citations      |

---
