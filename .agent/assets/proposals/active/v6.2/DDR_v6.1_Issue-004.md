---
document:
  id:              DDR_v6.1_Issue-004
  title:           "Resolution Report for ISSUE-004: `derivation_mode` Rule Is Declared but Not Enforced"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
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
tier_refs:   ["All (schema)"]
section_ref: "§3.2, §3.7"
rule_refs:   [CIT-R2, CIT-R6]
```

### 1. Validation Audit of ISSUE-004

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` was conducted to investigate the claims of "ISSUE-004: `derivation_mode` Rule Is Declared but Not Enforced."

The rule text in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:315-319` states that for `edge_type='derives'`, `derivation_mode` may be provided as `semantic|traceability`, and `:332-335` adds that authority-linkage derives edges must set `derivation_mode` to `traceability`. The schema mirrors that intent only in prose: `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1194-1202` says `derivation_mode` is "Valid only when edge_type is 'derives'." However, the same schema block has no conditional guard, and the canonical scaffold in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:2451-2456` gives every `ParentCitation` an optional `derivation_mode` field. A local `jsonschema` validation probe using `{edge_type: "implements", derivation_mode: "traceability"}` inside `parent_ids` returned `VALID`. The evidence also shows an enforcement ceiling: the schema can restrict `derivation_mode` to derives edges, but it cannot tell whether a particular derives edge is being used specifically as an "authority linkage," so `CIT-R6` can only be partially mechanized.

**Findings:**

1. **The Constraint Exists Only as Documentation:** The schema text states the restriction, but the machine-readable contract does not encode it. That means structurally invalid citation shapes currently pass validation even though the spec says they should not exist.
2. **`CIT-R6` Cannot Be Fully Solved by Schema Alone:** The schema can enforce that `derivation_mode` is absent on non-derives edges, but it cannot infer whether a derives citation is serving as an "authority linkage" rather than ordinary semantic lineage. The requirement that authority-linkage derives edges use `traceability` therefore remains partly a runtime or review-time obligation.
3. **The Canonical Implementation Scaffold Reinforces the Defect:** The published dataclass model treats `derivation_mode` as universally optional across all edge types. Tool authors who follow that scaffold will reproduce the same invalid state space in code, not just in data.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-004

The resolution goal is to make `derivation_mode` structurally legal only on derives edges, while preserving a citation model that is easy for validators and tooling to reason about.

#### Option A: Add a Conditional Guard to the Existing `ParentCitation`

Keep the current `ParentCitation` shape but add JSON Schema conditional logic so `derivation_mode` is allowed only when `edge_type` equals `derives`. In practice, that means the schema must say "if `edge_type` is derives, then `derivation_mode` may be present with the documented enum; else `derivation_mode` must be absent." This is the smallest targeted patch and it preserves the existing object shape for downstream consumers. Its limitation is that the citation type still has to be mentally parsed as "one object with embedded behavioral branches" rather than as explicit structural variants.

* **Supporting Insights:** If the project wants the narrowest schema edit, conditionals express the rule directly without changing field names or citation object identity. That keeps backwards compatibility high while still making the prose restriction enforceable.
* **Citations:** [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object).

#### Option B: Split `ParentCitation` into Explicit Citation Variants

Replace the single all-purpose `ParentCitation` definition with explicit variants such as `DerivesCitation` and `NonDerivesCitation`, combined with `oneOf`. The derives variant carries the optional `derivation_mode`, while the non-derives variant omits it entirely and can simultaneously enforce ISSUE-003's exclusion of `extends` from `parent_ids`; the canonical scaffold at `ddr_system_v6.1.yaml:2451-2456` should be updated in the same remediation window so the published dataclass model matches the revised schema. This is a broader schema refactor than Option A, but it makes the citation model self-documenting and structurally unambiguous. It also aligns the schema type system with how the spec already talks about derives edges as semantically special, while still acknowledging that `CIT-R6` intent cannot be fully derived from structure alone.

* **Supporting Insights:** ISSUE-003 and ISSUE-004 both point to the same design smell: the current `ParentCitation` object is modeling too many distinct cases in one loose shape. Variant schemas let the project solve both defects with one coherent redesign instead of layering more conditional exceptions onto an already overloaded type, but the project should document that "authority linkage" still requires semantic intent checking beyond pure schema validation.
* **Citations:** [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Immediate Patch Size:** Option A is smaller and fully addresses the validated defect because it preserves the current `ParentCitation` shape and adds the missing field-placement rule. Option B broadens the change into a type redesign even though the evidence shows a single missing conditional.
2. **Cross-Issue Alignment:** Option A can still be coordinated with ISSUE-003 in the same `ParentCitation` patch window by tightening the enum and the `derivation_mode` condition together. Option B solves both issues through a larger refactor, but that larger refactor is not required to make either rule enforceable.
3. **Enforcement Ceiling:** Neither option can make `CIT-R6` fully self-enforcing because the schema cannot infer authorial intent for a derives edge. Option A therefore fixes the exact structural leak without implying a broader architectural rewrite is necessary.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a missing conditional on one optional field, not a demonstrated failure of the entire citation model. Adding the `derivation_mode` guard to the existing `ParentCitation` shape closes the schema gap directly, and it can still be paired with ISSUE-003 in the same edit without introducing new citation variants.

**Option A** is recommended because:

* **Exact Rule Enforcement:** It makes the schema reject `derivation_mode` everywhere the spec already says it is invalid.
* **Low Migration Cost:** Existing tooling keeps the same citation object shape and only gains the missing constraint.
* **Coordinated Repair Window:** ISSUE-003 and ISSUE-004 can still be fixed together on the same schema type without turning both defects into a larger redesign.
* **Future-Compatible:** If a later version accumulates more tiered citation rules, a variant model can still be introduced then, based on demonstrated need rather than on this one conditional gap.
