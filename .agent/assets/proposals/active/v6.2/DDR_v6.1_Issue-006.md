---
document:
  id:              DDR_v6.1_Issue-006
  title:           "Resolution Report for ISSUE-006: `prior_status` Can Be Set Outside `SUPERSEDE_PENDING`"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  resolved:        "2026-03-27"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-006"

### Agent Context

```yaml
id:          ISSUE-006
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   ["All (schema)"]
section_ref: "§3.1, §3.8"
rule_refs:   [gc-007, gc-008, gc-009]
updated:     2026-03-27
resolved:    2026-03-27
```

> **Resolution (2026-03-27):** Option A — Restricted `prior_status` to nodes in `SUPERSEDE_PENDING`.

### 1. Validation Audit of ISSUE-006

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` was conducted to investigate the claims of "ISSUE-006: `prior_status` Can Be Set Outside `SUPERSEDE_PENDING`."

The node schema defines `prior_status` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1116-1126` and explicitly states that the field "Must not be set on any node that is not in SUPERSEDE_PENDING status." The system definition repeats the same semantic rule at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:199-208`, and the lifecycle guard text at `:2642-2660` makes `prior_status` the rollback anchor for `gc-007` through `gc-009`. However, the enclosing `DdrNode` schema at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1072-1202` contains no conditional linking `prior_status` to `status == SUPERSEDE_PENDING`. A direct `jsonschema` validation probe accepted a node with `status: ACTIVE` and `prior_status: DIRTY`, confirming that the prohibition is documentary only.

**Findings:**

1. **Rollback Metadata Is Not Status-Scoped:** The schema exposes `prior_status` as a generally optional field even though the prose restricts it to a transient supersede state. That means settled nodes can carry rollback anchors with no machine-level rejection.
2. **The Supersede Safety Chain Is Weaker Than Advertised:** `gc-007` through `gc-009` assume `prior_status` reflects a live supersede operation. If the field can appear arbitrarily on non-pending nodes, tools cannot safely treat its presence as authoritative rollback context.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-006

The resolution goal is to make `prior_status` mechanically valid only in the transient state where the supersede lifecycle actually needs it.

#### Option A: Gate `prior_status` by `status`

Add a `DdrNode`-level conditional so that when `status == SUPERSEDE_PENDING`, `prior_status` may be present with its current enum, and when `status != SUPERSEDE_PENDING`, `prior_status` must be absent. This is the narrowest schema repair because it preserves the current node shape and simply converts the existing prose rule into an enforceable contract. It also aligns directly with the current lifecycle text, which already treats `prior_status` as a temporary rollback anchor rather than general node metadata. The change has low blast radius for consumers that already follow the documented rule.

* **Supporting Insights:** The field's intended lifecycle is already well specified; what is missing is only the structural guard. Using a conditional here keeps the schema aligned with the current runtime model without redesigning the whole node type.
* **Citations:** [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object).

#### Option B: Split Pending and Settled Node Variants

Refactor `DdrNode` into explicit variants, such as a `SupersedePendingNode` that includes `prior_status` and a settled-node variant that omits it entirely. This is a broader redesign, but it makes transient rollback state a first-class type distinction instead of a conditional rule buried inside one large object. It also creates a cleaner structural home for any future supersede-only fields or invariants. The tradeoff is higher migration cost across validators, generators, and typed client models that currently assume a single node schema.

* **Supporting Insights:** Variant modeling is stronger when transient lifecycle states are expected to carry specialized metadata. It trades some schema verbosity for clearer semantics and less per-consumer branching logic.
* **Citations:** [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Repair Scope:** Option A localizes the fix to one documented rule and preserves the current `DdrNode` shape. Option B is structurally cleaner, but it pushes a broader node-type refactor into every downstream consumer.
2. **Lifecycle Clarity:** Option A makes the current prose enforceable with minimal blast radius. Option B makes the transient-versus-settled distinction more explicit, but that extra clarity comes with a larger migration surface.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

DDR v6.1 already describes `prior_status` as transient rollback metadata rather than general-purpose node state. Encoding that rule directly is enough to close the defect without forcing a broader node-model redesign.

**Option A** is recommended because:

* **Direct Spec Alignment:** It makes the schema enforce the same `prior_status` scope rule already stated in both the schema and system definition.
* **Low Consumer Disruption:** Existing tooling that already treats `prior_status` as supersede-only can remain structurally unchanged.
* **Stronger Rollback Trust:** The presence of `prior_status` becomes a more reliable signal that a node is actually in supersede-pending state.

### 4. Implementation Note

Implemented in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.2\ddr_node_schema_v6.2.yaml` with a `DdrNode` conditional that requires `prior_status` only when `status == SUPERSEDE_PENDING` and rejects it otherwise. Post-change validation confirmed that settled nodes carrying `prior_status` now fail while the system-definition lifecycle semantics remain intact.