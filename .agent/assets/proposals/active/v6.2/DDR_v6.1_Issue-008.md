---
document:
  id:              DDR_v6.1_Issue-008
  title:           "Resolution Report for ISSUE-008: `constraint_origin` Is Not Restricted to CL Nodes"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  status:          "OPEN"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-008"

### Agent Context

```yaml
id:          ISSUE-008
status:      OPEN
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["Non-CL nodes (schema)"]
section_ref: "§3.1, §5"
rule_refs:   [AX-4]
```

### 1. Validation Audit of ISSUE-008

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` was conducted to investigate the claims of "ISSUE-008: `constraint_origin` Is Not Restricted to CL Nodes."

The node schema defines `constraint_origin` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1109-1115` and describes it as "Causal origin of the constraint (v6.1 §5, for CL tier)." The system definition places the same field inside the CL tier schema at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:743-753`, where the surrounding context is explicitly CL-specific. However, the enclosing `DdrNode` schema at `ddr_node_schema.yaml:1072-1202` contains no conditional limiting `constraint_origin` to `tier == CL`. A direct `jsonschema` validation probe accepted a `SIL` node carrying `constraint_origin: imposed`, confirming that the CL-only semantics are not structurally enforced.

**Findings:**

1. **A CL-Scoped Field Is Exposed Globally:** The schema describes `constraint_origin` as CL-specific, but structurally it is available to any tier. That creates a gap between the published tier model and the actual validation surface.
2. **Tier Semantics Can Leak Across the DAG:** Non-CL nodes can carry CL-only meaning while still validating. This makes the field less trustworthy as a CL signal and increases the chance of false inference in tooling.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-008

The resolution goal is to ensure `constraint_origin` is legal only on nodes whose tier semantics actually support it.

#### Option A: Prohibit `constraint_origin` Unless `tier == CL`

Add a `DdrNode`-level conditional that permits `constraint_origin` only when the node's `tier` equals `CL` and otherwise requires the field to be absent. This is the narrowest schema repair because it preserves the current single-node shape while making the documented tier restriction enforceable. It directly aligns the machine contract with both the field description and the CL tier schema in the system definition. The change is also low-risk because the field is already advertised as CL-specific.

* **Supporting Insights:** The spec already knows which tier owns the field. The missing piece is only the structural gate that keeps the field from appearing elsewhere.
* **Citations:** [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object).

#### Option B: Introduce Tier-Specific Node Variants

Refactor `DdrNode` into tier-aware variants so that CL nodes include `constraint_origin` and non-CL variants do not. This is a broader redesign, but it makes tier-specific fields structurally explicit and creates a cleaner base for future tier-only properties. The downside is a larger schema and a wider change surface for generators and typed consumers. The upside is stronger fidelity between the schema type system and the tier model described throughout the spec.

* **Supporting Insights:** Variant modeling is most compelling when a schema starts accumulating multiple tier-only fields. It can prevent repeated one-off conditionals from cluttering a single monolithic node definition.
* **Citations:** [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Repair Size:** Option A fixes the exact leak with a small conditional and minimal consumer impact. Option B offers cleaner long-term tier typing, but it requires a larger schema refactor immediately.
2. **Type-System Explicitness:** Option A keeps tier scoping implicit inside one node type. Option B makes the CL-versus-non-CL distinction more explicit, but that clarity may be more than the current schema needs for a single leaked field.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a missing tier gate, not a failure of the entire node model. DDR v6.1 can recover the intended semantics with a focused conditional instead of a full node-variant redesign.

**Option A** is recommended because:

* **Exactness:** It repairs the specific tier leak the evidence demonstrates.
* **Low Migration Cost:** Existing consumers can keep the current `DdrNode` shape.
* **Better Tier Discipline:** `constraint_origin` becomes a reliable CL-only signal instead of a globally available hint.
