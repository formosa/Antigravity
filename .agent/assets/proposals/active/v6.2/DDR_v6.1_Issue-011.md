---
document:
  id:              DDR_v6.1_Issue-011
  title:           "Resolution Report for ISSUE-011: Node ID Prefix Is Not Bound to Declared Tier"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  status:          "OPEN"
  severity:        "CRITICAL"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-011"

### Agent Context

```yaml
id:          ISSUE-011
status:      OPEN
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   ["All (schema)"]
section_ref: "§3.1, §3.6"
rule_refs:   []
```

### 1. Validation Audit of ISSUE-011

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` was conducted to investigate the claims of "ISSUE-011: Node ID Prefix Is Not Bound to Declared Tier."

The core node schema defines `id` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1089-1094` with the pattern `^(XPD-0\.[0-9]+|[A-Z]{2,5}-[0-9]+\.[0-9]+)$`, while `tier` is defined independently at `:1095-1098` as the enum `[XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]`. The enclosing `DdrNode` block at `:1079-1202` contains no conditional, variant, or cross-field assertion that ties the `id` prefix to the declared `tier`. The system definition's contract summary at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:2363-2366` reinforces that identifiers are semantically tiered by the `TIER-N.M` pattern rather than free-form labels. A local Draft 2020-12 validation probe accepted an otherwise valid node with `tier: FCL` and `id: SAL-5.1`, confirming that prefix-to-tier alignment is not enforced today.

**Findings:**

1. **Identifier Semantics Are Not Structurally Bound:** The schema treats `id` and `tier` as independently valid fields even though the identifier format embeds tier meaning. That lets a single node claim two different tiers at once, depending on which field a consumer trusts.
2. **Tier-Routed Tooling Can Diverge on the Same Document:** Downstream validators, DAG visualizers, and routing logic often key behavior from tier identity. If one consumer trusts `tier` and another trusts the `id` prefix, the same schema-valid document can produce contradictory traversal, grouping, or rule-application results.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-011

The resolution goal is to make node identity unambiguous so that the schema cannot admit documents whose identifier and declared tier disagree.

#### Option A: Bind `id` Patterns to `tier` with Conditionals

Keep the current `DdrNode` shape, but add tier-aware constraints so each `tier` value activates the corresponding `id` regex. In practice, `tier: SAL` would require `^SAL-[0-9]+\.[0-9]+$`, `tier: FCL` would require `^FCL-[0-9]+\.[0-9]+$`, and `tier: XPD` would retain its special `^XPD-0\.[0-9]+$` rule. This is the narrowest fix because it closes the integrity gap without redesigning the rest of the node schema. It also preserves backward compatibility for consumers that already depend on a single `DdrNode` contract.

* **Supporting Insights:** The current defect is a missing cross-field invariant, not a failure of the entire node model. A conditional repair fits the present schema architecture and can be introduced with low blast radius while still making tier identity structurally reliable.
* **Citations:** [JSON Schema string reference (`pattern`)](https://json-schema.org/understanding-json-schema/reference/string), [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals)

#### Option B: Introduce Tier-Specific Node Variants

Refactor `DdrNode` into tier-specific variants so each variant fixes both `tier` and the matching `id` pattern at the type level. This is a broader redesign, but it makes tier identity explicit to typed consumers and creates a cleaner home for tier-only fields such as `constraint_origin`. The approach also pairs naturally with a future resolution of ISSUE-008, where CL-specific data should be structurally unavailable to non-CL nodes. The tradeoff is a larger schema and a wider update surface for validators, code generators, and any tooling that currently assumes one generic node shape.

* **Supporting Insights:** Variant modeling becomes more attractive when multiple tier-sensitive constraints need to be enforced together. If the project expects more tier-specific rules over time, this option reduces the accumulation of scattered conditionals in a single monolithic node schema.
* **Citations:** [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Repair Scope:** Option A repairs the exact prefix-mismatch defect with a focused cross-field constraint. Option B yields stronger structural typing, but it broadens the change into a full node-schema redesign.
2. **Long-Term Tier Modeling:** Option A preserves the current single-node contract and is easier to adopt immediately. Option B creates a cleaner foundation for future tier-only constraints, especially if ISSUE-008 or similar tier-partitioned fields are expected to grow.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a missing identity invariant inside an otherwise coherent node contract. DDR v6.1 can close that gap directly without forcing every consumer into a larger tier-variant migration immediately.

**Option A** is recommended because:

* **Direct Integrity Repair:** It makes the schema reject semantically contradictory `id` and `tier` combinations as soon as they appear.
* **Low Migration Cost:** Existing tooling can keep the current `DdrNode` shape while gaining a stronger guarantee about tier identity.
* **Future-Compatible:** A focused conditional repair does not prevent a later move to tier-specific variants if broader tier partitioning becomes desirable.
