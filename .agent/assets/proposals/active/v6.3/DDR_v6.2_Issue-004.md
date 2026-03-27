---
document:
  id:              DDR_v6.2_Issue-004
  title:           "Resolution Report for ISSUE-004: Harden ARE Operational Contracts in the Schema"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  updated:         "2026-03-27"
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
tier_refs:   ["Extension System", "Extension Catalog"]
section_ref: "§8.2, §9 E5"
rule_refs:   []
updated:     2026-03-27
```

### 1. Validation Audit of ISSUE-004

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:330-360`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:416-445`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:929-1002`, and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:1437-1498` was conducted to investigate the claims of "ISSUE-004: Harden ARE Operational Contracts in the Schema."

The schema types `candidate_pool.activation_states` only as a generic object at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:345-360`, while the authoritative system file defines concrete `active`, `paused`, and `disabled` semantics plus transition rules at `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:1437-1498`. `ExtensionEntry.scoring_profile` remains an unconstrained string with descriptive prose saying it is required for `E5` at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:929-945`, and `ScoringProfile` accepts any two-number `range` plus any numeric `minimum_surfacing_threshold` at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:963-1002`. Local `jsonschema` probes all passed for `activation_states: {banana: {disabled_to_paused: true}}`, an `E5` extension entry without `scoring_profile`, an `E5` entry with `scoring_profile: does_not_exist`, and a scoring profile with reversed or out-of-band ranges plus `minimum_surfacing_threshold: -0.25`.

**Findings:**

1. **ARE Safety Semantics Are Mostly Descriptive:** The system file defines concrete pool lifecycle and scoring rules, but the schema only enforces shallow structure for several of the most important safety boundaries.
2. **Invalid Promotion and Lifecycle States Remain Schema-Valid:** Impossible activation states, dangling scoring-profile references, and mathematically invalid scoring bands can all cross the schema boundary without early rejection.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-004

The resolution goal is to make ARE operational safety contracts enforceable in a way that validators and downstream tooling can rely on consistently.

#### Option A: Promote ARE Contracts into JSON Schema

Strengthen the schema directly by typing `activation_states` as a closed object with explicit `active`, `paused`, and `disabled` members; add conditional enforcement so `id: E5` requires `scoring_profile`; and add the numeric bounds and structural constraints that JSON Schema can express for scoring thresholds and band ranges. This catches more invalid data at the schema boundary and keeps validation centralized in one contract. Its main limitation is that same-document reference integrity and full range-overlap semantics are awkward to express completely in plain JSON Schema.

* **Supporting Insights:** The current schema can already enforce much more than it does today for ARE, especially fixed keys, required fields, enum-like branches, and basic numeric bounds. That makes Option A a meaningful hardening step even if some cross-reference and semantic checks would still remain out of reach.
* **Citations:** [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals)

#### Option B: Pair the Current Schema with a Required ARE Contract Validator

Declare the unresolved ARE semantics runtime-authoritative and ship a deterministic validator that checks activation-state topology, `E5` scoring-profile presence, scoring-profile existence, threshold bounds, and range sanity as a mandatory companion to schema validation. This explicitly treats the JSON Schema as a structural front door rather than the whole contract. It adds one more validation stage, but it can fully enforce the semantic rules that the current schema shape does not capture well.

* **Supporting Insights:** The hardest defects in the current ARE contract are not just about missing fields; they are about referential integrity and domain semantics. A dedicated validator can enforce those rules directly instead of encoding them indirectly or incompletely in schema syntax.
* **Citations:** No authoritative external reference identified for this specific claim.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Boundary Strictness vs Semantic Reach:** Option A improves structural rejection at the schema boundary, while Option B can validate the full ARE semantics that matter operationally.
2. **Validation Simplicity:** Option A preserves a single validation surface, but risks awkward or partial encodings for same-document references and score-band semantics. Option B adds a companion validator, but makes responsibilities explicit.
3. **Operational Reliability:** Option A catches more malformed documents early, but Option B is the more complete way to guarantee pool lifecycle, scoring-profile integrity, and promotion-threshold correctness.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

The validated defect is broader than simple schema looseness: it includes referential integrity and scoring semantics that the current schema shape does not express completely. A required ARE validator is the most honest way to make those rules deterministic today, while still leaving room to harden the schema itself where pure structural checks are sufficient.

**Option B** is recommended because:

* **Covers the Full Contract:** It can enforce activation-state logic, profile existence, and score-band sanity without relying on partial schema approximations.
* **Makes Validation Authority Explicit:** Tooling can treat the JSON Schema as structural validation and the ARE validator as semantic validation, rather than assuming the schema alone is complete.
* **Supports Incremental Hardening:** The project can still move obvious structural checks into the schema later without weakening the validator-based semantic backstop.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
