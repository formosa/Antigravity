---
document:
  id:              DDR_v6.2_Issue-004
  title:           "Resolution Report for ISSUE-004: Harden ARE Operational Contracts in the Schema"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  status:          "OPEN"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-004"

### Agent Context

```yaml
id:          ISSUE-004
status:      OPEN
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   ["Extension System", "Extension Catalog", "ARE Scoring Profiles"]
section_ref: "\u00a78.2, \u00a79 E5"
rule_refs:   ["ARE-R2", "ARE-R5", "EXT-R1"]
updated:     2026-03-28
```

### 1. Validation Audit of ISSUE-004

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:345-360`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:423-434`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:941-945`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:963-1002`, `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:1437-1498`, and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:1650-1672` was conducted to investigate the claims of "ISSUE-004: Harden ARE Operational Contracts in the Schema".

ARE has several safety-sensitive contracts in the authoritative system file, but the schema front door is weak where those contracts should be easiest to enforce. Activation states are structurally open, `E5` scoring-profile requirements are under-enforced, the custom profile path is under-typed, and numeric score bounds are loose.

**Findings:**

1. **ARE Structural Contracts Are Under-Typed:** Key activation-state and scoring-profile guarantees remain documentary at the schema boundary.
2. **Invalid Scoring Shapes Can Validate:** Malformed thresholds and profile structures can still pass structural validation.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-004

The resolution goal is to harden the ARE boundary without forcing every higher-order ARE guarantee into plain JSON Schema.

#### Option A: Use a Hybrid Structural Schema plus ARE Conformance Validator

Use JSON Schema to close the structural rules that it expresses well: typed activation states, `E5`-conditional `scoring_profile` presence, machine-typed profile objects, and basic numeric bounds. Then make a deterministic ARE-specific validator authoritative for cross-reference existence, score-band ordering and non-overlap, and any semantic checks that span multiple objects. This intentionally splits enforcement by concern without leaving the schema front door weak.

* **Supporting Insights:** A hybrid split lets the schema reject malformed structures early while a deterministic validator owns cross-object guarantees.
* **Citations:** [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema numeric reference](https://json-schema.org/understanding-json-schema/reference/numeric)

#### Option B: Promote ARE Contracts into JSON Schema

Add a typed `activation_states` object with explicit `active`, `paused`, and `disabled` members; add conditional enforcement so `id: E5` requires `scoring_profile`; constrain `scoring_profile` to known or structurally declared profile identifiers; type the custom profile path against `ScoringProfile`; and add numeric bounds for thresholds and range items, with a runtime ordering check if the two-element array form is retained.

* **Supporting Insights:** A schema-only push strengthens early rejection, but some ARE guarantees fit poorly as pure schema rules.
* **Citations:** [JSON Schema numeric reference](https://json-schema.org/understanding-json-schema/reference/numeric), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Coverage vs Fit:** Option A matches enforcement method to rule type; Option B tries to keep more of the contract in schema.
2. **Early Failure:** Both options improve front-door validation, but Option A avoids overloading JSON Schema with awkward cross-object logic.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The tracker now prefers the hybrid strategy because ARE has two different classes of obligations: obvious structural rules and higher-order conformance rules. DDR benefits from enforcing both, but not with the same mechanism.

**Option A** is recommended because:

* **Closes Front-Door Gaps:** Malformed activation states and invalid numeric bounds can fail immediately.
* **Preserves Deterministic Higher-Order Checks:** Profile resolution and score semantics can stay in a dedicated validator.
* **Matches the Contract Boundary:** Each ARE guarantee is enforced by the mechanism that fits it best.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
