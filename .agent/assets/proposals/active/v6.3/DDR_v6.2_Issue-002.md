---
document:
  id:              DDR_v6.2_Issue-002
  title:           "Resolution Report for ISSUE-002: Enforce the Mandatory Active Tier Set"
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

## Optimized Resolution Strategy for "ISSUE-002"

### Agent Context

```yaml
id:          ISSUE-002
status:      OPEN
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   ["All files (root topology)"]
section_ref: "§3.5"
rule_refs:   []
updated:     2026-03-27
```

### 1. Validation Audit of ISSUE-002

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:79-88` was conducted to investigate the claims of "ISSUE-002: Enforce the Mandatory Active Tier Set."

The `active_tiers` description names `SIL`, `GPCL`, `FCL`, `SAL`, `ICL`, `CDL`, and `ISL` as mandatory, with only `XPD` and `CL` marked optional, at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:79-83`. The machine contract immediately below it enforces only enum membership, `minItems: 7`, and `uniqueItems: true` at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:84-88`. A local `jsonschema` probe accepted `active_tiers: [SIL, GPCL, FCL, CL, SAL, ICL, CDL]`, which satisfies the current size rule while still omitting mandatory `ISL`.

**Findings:**

1. **Topology Prose Is Stronger Than Validation:** The schema text states a mandatory seven-tier base topology, but the validator only checks array size and membership. That means the canonical DDR tier set is not actually enforced at the schema boundary.
2. **Schema-Valid Files Can Drop Required Tiers:** A document can pass validation while omitting a required tier and substituting an optional one. Downstream tooling must therefore reconstruct a topology guarantee the root schema claims to provide.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-002

The resolution goal is to make the `active_tiers` contract machine-enforce the mandatory DDR base topology instead of only approximating it by count.

#### Option A: Add Mandatory `contains` Constraints

Keep the current array shape, but add one `contains: {const: <TIER>}` assertion per mandatory tier inside an `allOf` block for `active_tiers`. This is the narrowest repair because it preserves the existing list representation while making each mandatory member structurally required. Optional `XPD` and `CL` remain expressible as additive members rather than substitutes for the base set.

* **Supporting Insights:** The current defect is not about array ordering or duplication, both of which are already handled well enough. It is specifically about missing mandatory members, which `contains` addresses directly without redesigning the rest of the root topology model.
* **Citations:** [JSON Schema array reference](https://json-schema.org/understanding-json-schema/reference/array)

#### Option B: Encode Tier Sets as Profile-Specific Contracts

Replace the current loose array rule with profile-aware tier-set contracts that distinguish the mandatory base set from optional topology expansions such as `XPD` and `CL`. This creates a clearer topology model and could be paired with a broader document-profile cleanup, but it expands the scope of the fix from one array contract to a wider root-schema redesign. It is more explicit, but heavier than the specific defect requires.

* **Supporting Insights:** Profile-aware tier contracts make the topology easier to read and reason about, especially if the schema eventually formalizes multiple document classes. The cost is that a simple membership gap becomes entangled with larger root modeling decisions.
* **Citations:** [JSON Schema array reference](https://json-schema.org/understanding-json-schema/reference/array), [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Defect Precision:** Option A targets the exact gap by requiring each mandatory tier directly, while Option B folds the fix into a broader topology and profile redesign.
2. **Blast Radius:** Option A preserves the current array contract and downstream expectations; Option B changes the conceptual shape of root topology validation.
3. **Future Modeling:** Option A is the cleaner immediate repair, whereas Option B offers more room for future profile-aware topology rules if the project later decides they are necessary.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated problem is that the schema already knows the full set of mandatory tiers in prose but fails to require those members structurally. Adding explicit membership checks repairs the published topology contract at the lowest cost and keeps root validation aligned with the current document model.

**Option A** is recommended because:

* **Repairs the Actual Gap:** The problem is missing mandatory members, and `contains` constraints address that directly.
* **Preserves Existing Shape:** The project keeps the current `active_tiers` array model instead of widening this issue into a larger root-schema redesign.
* **Strengthens Early Validation:** Validators can reject topology defects immediately rather than relying on later runtime checks to recover the invariant.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
