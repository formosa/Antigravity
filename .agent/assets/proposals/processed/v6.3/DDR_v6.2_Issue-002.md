---
document:
  id:              DDR_v6.2_Issue-002
  title:           "Resolution Report for ISSUE-002: Enforce the Mandatory Active Tier Set"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  resolved:        "2026-03-28"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-002"

### Agent Context

```yaml
id:          ISSUE-002
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   ["All files (root topology)"]
section_ref: "\u00a73.5"
rule_refs:   ["INV-3"]
updated:     2026-03-28
resolved:    2026-03-28
```

### 1. Validation Audit of ISSUE-002

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:79-88` was conducted to investigate the claims of "ISSUE-002: Enforce the Mandatory Active Tier Set".

The schema text names seven mandatory tiers, but the actual `active_tiers` contract only checks enum membership, uniqueness, and a minimum length of seven. That leaves the mandatory set itself unenforced.

**Findings:**

1. **Mandatory Membership Is Prose-Only:** No schema rule requires any specific mandatory tier to appear.
2. **The Wrong Seven Tiers Can Pass:** Validation can succeed while omitting mandatory `CDL` and `ISL`.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-002

The resolution goal is to encode the mandatory tier set directly without dragging this narrow defect into broader topology redesign work.

#### Option A: Add Mandatory `contains` Constraints

Add one `contains: {const: <TIER>}` constraint per mandatory tier inside an `allOf` block for `active_tiers`. This is the smallest repair because it preserves the current array shape while making the existing prose requirement machine-enforceable.

* **Supporting Insights:** Per-tier `contains` constraints encode the stated obligation directly.
* **Citations:** [JSON Schema array reference](https://json-schema.org/understanding-json-schema/reference/array)

#### Option B: Encode Tier Sets as Profile-Specific Contracts

Replace the current loose array rule with profile-aware tier-set contracts that distinguish the mandatory base set from the optional `XPD` and `CL` expansions. This creates a clearer topology contract, but it is a wider root-schema redesign than Option A.

* **Supporting Insights:** Profile-aware tier-set rules are cleaner architecturally, but they broaden the change significantly.
* **Citations:** [JSON Schema array reference](https://json-schema.org/understanding-json-schema/reference/array), [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Repair Scope:** Option A fixes the exact missing guarantee; Option B folds it into wider root-schema redesign.
2. **Compatibility:** Option A preserves the current array shape; Option B introduces broader profile semantics.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The current defect is mechanical and well-bounded. DDR says seven specific tiers are mandatory, so the lowest-risk repair is the one that machine-requires those exact tiers and stops there.

**Option A** is recommended because:

* **Directness:** The fix mirrors the published mandatory-tier rule exactly.
* **Low Blast Radius:** Existing valid documents keep the same data shape.
* **Scope Control:** Ordering and node-membership concerns remain isolated to ISSUE-008.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` and reflected in `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml`.

The v6.3 schema now closes `active_tiers` to canonical ordered variants that always include the mandatory base tier set. That stricter contract subsumes the recommended mandatory-member enforcement by making any omission of `SIL`, `GPCL`, `FCL`, `SAL`, `ICL`, `CDL`, or `ISL` schema-invalid. The v6.3 system file now declares an `active_tiers` array that conforms to that closed topology.

Validation evidence:
- `.venv\Scripts\python.exe` YAML-parse check succeeded for both v6.3 YAML artifacts.
- Draft 2020-12 validation of `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` against `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` succeeded with the canonical `active_tiers` contract in place.
