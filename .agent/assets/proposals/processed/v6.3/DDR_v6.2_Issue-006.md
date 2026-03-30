---
document:
  id:              DDR_v6.2_Issue-006
  title:           "Resolution Report for ISSUE-006: Type Remaining Normative Rule Identifiers"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  resolved:        "2026-03-28"
  status:          "RESOLVED"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-006"

### Agent Context

```yaml
id:          ISSUE-006
status:      RESOLVED
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["DAG invariants", "tier rules", "extension rules"]
section_ref: "\u00a73.5, \u00a75, \u00a79"
rule_refs:   ["INV-2", "EXT-R1"]
updated:     2026-03-28
resolved:    2026-03-28
```

### 1. Validation Audit of ISSUE-006

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:595-603`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:649-655`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:676-683`, and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:919-926` was conducted to investigate the claims of "ISSUE-006: Type Remaining Normative Rule Identifiers".

Several normative identifier families remain free strings even though sibling schema families already use explicit patterns. The gap now spans DAG invariants, both atomic rule families, and extension rules.

**Findings:**

1. **Multiple Rule Families Lack Structural Guards:** Invariant IDs, atomic rule IDs, and extension rule IDs are looser than peer families such as `AX-*` and `CIT-R*`.
2. **Malformed IDs Pass Validation:** Local probes accepted clearly invalid identifiers in authoritative rule positions.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-006

The resolution goal is to make syntactic rule identity consistently machine-checkable without scattering rule-pattern logic across the schema.

#### Option A: Add Pattern Constraints Per Rule Family

Add explicit regex patterns for each currently untyped rule-ID family, such as `^INV-[0-9]+$` for `DagInvariant.id`, a permissive but structured pattern for atomic rule families that preserves bridge and suffix forms such as `GPCL-FCL-BR1` and `CL-R9-imposed`, and either a unified `^[A-Z]{2,3}-R[0-9]+$` pattern or per-extension prefixes for extension rules. This is the lowest-blast-radius fix and aligns these families with the stricter rule-ID typing already used elsewhere.

* **Supporting Insights:** Per-field patterns close the current gap quickly, but they duplicate logic across several schema locations.
* **Citations:** [JSON Schema regular expressions](https://json-schema.org/understanding-json-schema/reference/regular_expressions)

#### Option B: Centralize Rule-ID Definitions

Create reusable `$defs` for each rule-ID family and reference them wherever those IDs appear. This is a larger cleanup, but it reduces drift, keeps rule-ID logic in one place, and makes future additions or alias handling easier to maintain.

* **Supporting Insights:** Centralized `$defs` keep recurring rule-ID families maintainable as DDR evolves.
* **Citations:** [JSON Schema structuring](https://json-schema.org/understanding-json-schema/structuring), [JSON Schema regular expressions](https://json-schema.org/understanding-json-schema/reference/regular_expressions)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Maintainability:** Option B consolidates shared logic; Option A repeats it at each field.
2. **Repair Speed:** Option A is faster to patch in place, but Option B lowers future drift risk.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

The tracker now favors centralized rule-ID definitions because the issue spans multiple families and has already expanded beyond the original narrow scope. Once several related identifier families need tightening, duplication becomes the larger maintenance risk.

**Option B** is recommended because:

* **Shared Logic in One Place:** Identifier-family rules remain consistent across consumers.
* **Lower Drift Risk:** Later edits touch one central definition instead of several duplicated patterns.
* **Easier Extension:** Future alias or family changes do not require reopening every field.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml`.

The v6.3 schema now centralizes normative identifier typing in reusable `$defs` including `InvariantId`, `CitationRuleId`, `AtomicTierRuleId`, `BridgeRuleId`, `AtomicRuleId`, and `ExtensionRuleId`, and it repoints the relevant consumers to those shared definitions. The final rule-ID contract also admits both atomic inclusion and exclusion rule families, so exclusion identifiers such as `XPD-E1` now validate under the same centralized authority.

Validation evidence:
- `.venv\Scripts\python.exe` YAML-parse check succeeded for both v6.3 YAML artifacts.
- Draft 2020-12 validation of `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` against `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` succeeded with the centralized rule-ID definitions in place.
