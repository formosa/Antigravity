---
document:
  id:              DDR_v6.2_Issue-009
  title:           "Resolution Report for ISSUE-009: Close the Operation Identifier Surface Machine-Readably"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  resolved:        "2026-03-28"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "LOGICAL_CONFLICT"
---

## Optimized Resolution Strategy for "ISSUE-009"

### Agent Context

```yaml
id:          ISSUE-009
status:      RESOLVED
severity:    MAJOR
type:        LOGICAL_CONFLICT
tier_refs:   ["Operations", "lifecycle authority", "ISL scaffold"]
section_ref: "\u00a77, \u00a73.8, SAL-5.1, ICL-6.1"
rule_refs:   ["AX-3"]
updated:     2026-03-28
resolved:    2026-03-28
```

### 1. Validation Audit of ISSUE-009

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:864-870`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:1062-1075`, `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:1168-1256`, and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2557-2607` was conducted to investigate the claims of "ISSUE-009: Close the Operation Identifier Surface Machine-Readably".

DDR presents a closed set of core operations, but the schema types operation names as free strings and the broader operational surface uses several overlapping naming dialects. Lifecycle rows, scaffold helpers, and operations-table tokens are therefore not normalized to one canonical vocabulary.

**Findings:**

1. **Operation Identity Is Not Structurally Closed:** The schema does not define a canonical operation enum for operations or lifecycle transitions.
2. **Extra Token Families Leak Across Surfaces:** Composite, subphase, and alias-like tokens coexist without one normalization authority.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-009

The resolution goal is to make operation identity deterministic enough that validators and tooling can distinguish canonical operations from phases and aliases without guesswork.

#### Option A: Split Canonical Operation, Phase, and Effect

Introduce a closed `OperationNameEnum` for the true public operation set, then model lifecycle-specific detail separately using fields such as `phase`, `transition_kind`, or `side_effect`. For example, `SUPERSEDE_COMPLETE` and `SUPERSEDE_ROLLBACK` become `operation: SUPERSEDE` plus explicit phase metadata, while `MODIFY|PROPAGATION` becomes `operation: MODIFY` plus a propagation side-effect annotation.

* **Supporting Insights:** Separating canonical operation identity from phase or side-effect metadata removes the ambiguity rather than normalizing around it.
* **Citations:** [W3C SCXML](https://www.w3.org/TR/scxml/), [JSON Schema enum](https://json-schema.org/understanding-json-schema/reference/enum)

#### Option B: Add an Authoritative Alias/Taxonomy Layer

Keep the current strings, but add a machine-readable alias map and operation taxonomy that classifies each token as canonical, composite, lifecycle-subphase, or scaffold alias. Validators must normalize all operation identifiers through that authority before comparison. This is less disruptive, but it preserves more conceptual complexity than Option A.

* **Supporting Insights:** An alias or taxonomy layer can work, but it preserves more conceptual overlap and string normalization burden.
* **Citations:** [JSON Schema enum](https://json-schema.org/understanding-json-schema/reference/enum)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Model Decomposition:** Option A clarifies what an operation is; Option B adds a normalization layer over the current strings.
2. **Compatibility:** Option B is less disruptive initially, but Option A yields a cleaner long-term contract.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The updated tracker now treats decomposition as the stronger fix because DDR does not just have a typo problem. It has multiple overlapping concepts currently all encoded as raw operation strings.

**Option A** is recommended because:

* **Removes the Core Ambiguity:** Canonical operation identity no longer competes with subphase or alias tokens.
* **Improves Tooling Determinism:** Validators, logs, tests, and APIs can compare one normalized operation surface.
* **Absorbs the Narrower Naming Drift:** The UNBUNDLE naming problem fits naturally inside this broader cleanup.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` and `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml`.

The v6.3 schema now closes the operation surface around `OperationNameEnum` and decomposes lifecycle transitions into canonical `operation` plus `phase`, `side_effect`, and `prerequisite_operations` metadata. The v6.3 system file now uses that normalized surface in `operations`, `lifecycle.status_transitions`, and the ISL scaffold so raw composite identifiers no longer act as authoritative operation tokens.

Validation evidence:
- `.venv\Scripts\python.exe` YAML-parse check succeeded for both v6.3 YAML artifacts.
- Draft 2020-12 validation of `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` against `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` succeeded with the normalized operation identifier surface.
