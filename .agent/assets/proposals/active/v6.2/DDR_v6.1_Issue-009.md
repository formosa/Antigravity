---
document:
  id:              DDR_v6.1_Issue-009
  title:           "Resolution Report for ISSUE-009: `express_mode_group` Is Not Required in Express Mode"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  resolved:        "2026-03-27"
  status:          "RESOLVED"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-009"

### Agent Context

```yaml
id:          ISSUE-009
status:      RESOLVED
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["Express-mode project instances"]
section_ref: "§4"
rule_refs:   []
updated:     2026-03-27
resolved:    2026-03-27
```

> **Resolution (2026-03-27):** Option A — Required `express_mode_group` whenever `project.mode` is `express`.

### 1. Validation Audit of ISSUE-009

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` was conducted to investigate the claims of "ISSUE-009: `express_mode_group` Is Not Required in Express Mode."

The project schema defines `project.mode` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:75-78` and allows `full` or `express`. The node schema defines `express_mode_group` at `:1153-1158` and explicitly says it is "Required when mode=express." The system definition at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:360-390` then defines Express Mode groups and deterministic UNBUNDLE behavior in terms of those groups. However, the schema contains no root-level conditional that, when `project.mode == express`, requires each node item to include `express_mode_group`. A direct `jsonschema` validation probe accepted an express-mode document whose nodes omitted the field entirely.

**Findings:**

1. **The Express-Mode Requirement Exists Only in Prose:** The schema documents the rule but does not enforce it. Express-mode documents therefore validate without the grouping metadata the same schema says they require.
2. **UNBUNDLE Preconditions Can Be Missing at Validation Time:** The system definition ties deterministic UNBUNDLE behavior to express-mode groups. If those groups are absent from a schema-valid express document, failure is deferred to runtime or to manual review.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-009

The resolution goal is to make express-mode documents structurally carry the per-node grouping metadata that their downstream operations depend on.

#### Option A: Require `express_mode_group` When `project.mode == express`

Add a root-level conditional so that when `project.mode` equals `express`, the node-item schema requires `express_mode_group` on every node. This is the smallest repair because it preserves the current document structure and simply enforces the rule the schema already states in prose. It also keeps full-mode documents lean by leaving the field optional outside express mode. The change directly aligns the validation contract with the current operational model.

* **Supporting Insights:** The defect is not that the field is missing from the schema, but that its requirement is disconnected from the mode selector that is already present. A conditional closes that gap with minimal redesign.
* **Citations:** [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema array reference (`items`)](https://json-schema.org/understanding-json-schema/reference/array).

#### Option B: Split Full-Mode and Express-Mode Root Profiles

Refactor the schema root into explicit full-mode and express-mode profiles, with the express profile requiring nodes to carry `express_mode_group` and the full profile omitting that obligation. This is a larger design change than Option A, but it gives mode-specific rules a clearer structural home and pairs naturally with any broader root-profile work undertaken for ISSUE-001. The tradeoff is added root complexity and a wider migration surface for producers and validators. The advantage is that mode becomes a first-class contract boundary instead of a trigger for scattered conditionals.

* **Supporting Insights:** Mode-specific document requirements often age better when they are attached to explicit profiles instead of hidden behind many local conditionals. That said, the current evidence only proves one missing requirement, not the need for a broader profile redesign.
* **Citations:** [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Implementation Scope:** Option A repairs the exact missing rule with a focused conditional. Option B can create a cleaner long-term mode model, but it introduces a broader root-contract redesign.
2. **Architectural Leverage:** Option A is the faster way to restore express-mode correctness. Option B becomes more attractive only if the project is already planning explicit root profiles for other reasons, such as ISSUE-001.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a missing express-mode requirement, not a broken mode system overall. A targeted conditional closes the enforcement gap without expanding the root contract more than necessary.

**Option A** is recommended because:

* **Directness:** It enforces the exact rule the schema already claims.
* **Preserved Lean Full Mode:** Full-mode documents do not inherit extra mandatory fields.
* **Earlier Failure Detection:** Express-mode documents missing group data fail at schema validation instead of at UNBUNDLE time.

### 4. Implementation Note

Implemented in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.2\ddr_node_schema_v6.2.yaml` with a root conditional that requires `express_mode_group` on every node when `project.mode == express`. Post-change validation confirmed that express-mode documents missing the field now fail while full-mode documents remain unaffected.