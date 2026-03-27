---
document:
  id:              DDR_v6.1_Issue-002
  title:           "Resolution Report for ISSUE-002: Lifecycle Machine Authority Accepts Undefined States"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  status:          "OPEN"
  severity:        "CRITICAL"
  type:            "LIFECYCLE_GAP"
---

## Optimized Resolution Strategy for "ISSUE-002"

### Agent Context

```yaml
id:          ISSUE-002
status:      OPEN
severity:    CRITICAL
type:        LIFECYCLE_GAP
tier_refs:   ["All"]
section_ref: "§3.1, §3.8"
rule_refs:   [INV-8]
```

### 1. Validation Audit of ISSUE-002

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` was conducted to investigate the claims of "ISSUE-002: Lifecycle Machine Authority Accepts Undefined States."

The authoritative status vocabulary in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:189-198` defines valid node statuses as `DRAFT | ACTIVE | DIRTY | DEPRECATED | SUPERSEDED | SUPERSEDE_PENDING`, and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1103-1108` repeats the same enum in `DdrNode.status`. However, the machine-authoritative lifecycle table in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:2529-2532` and `:2575-2578` transitions to `DELETED`, while `:2567-2570` transitions to `"{prior_status}"`. The schema does not constrain those transition endpoints back to the declared status set: `StatusTransition.from` and `StatusTransition.to` are both plain `type: string` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1029-1032`, and `ProhibitedTransition.to` is likewise an unconstrained array of strings at `:1049-1052`. A local validation probe confirmed that both `{'from': 'SUPERSEDE_PENDING', 'to': '{prior_status}', 'operation': 'SUPERSEDE_ROLLBACK'}` and `{'from': 'ACTIVE', 'to': ['DELETED'], 'reason': 'test'}` are schema-valid today.

**Findings:**

1. **The Closed-State Machine Claim Is Not True Today:** The authoritative transition table references targets that are not members of the declared status enum. That means `INV-8` is currently violated by the same lifecycle block that is supposed to embody it.
2. **Rollback Is Dynamic, Not a Literal Status:** The system spec already defines `prior_status` as a node field with enum-restricted values at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1116-1126` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:199-210`. Treating `"{prior_status}"` as a plain string therefore fails to model the actual rollback mechanism the spec describes.
3. **The Schema Cannot Prevent Further Lifecycle Drift:** Because both allowed and prohibited transition endpoints are unconstrained strings, future undefined states, typos, or placeholders will continue to validate structurally. Implementations are therefore free to disagree about what `DELETE` and rollback actually do.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-002

The resolution goal is to re-establish a closed, machine-verifiable lifecycle model whose transition table and status vocabulary cannot diverge silently.

#### Option A: Constrain Transitions to Typed Status References

Refactor the lifecycle schema so every persisted transition endpoint is validated against the declared status enum, ideally by reusing a single `StatusEnum` definition or a dedicated `StatusRef` schema. Under this approach, `DELETE` is treated as an operation sink that removes a node from the graph rather than as a transition into a persisted `DELETED` status, and rollback is modeled explicitly with a mutually exclusive field such as `to_node_field: "prior_status"` instead of an untyped placeholder string. The same typing discipline should be applied symmetrically to `ProhibitedTransition.to` so prohibited targets cannot escape the enum either. This preserves the current six-state runtime model while making the lifecycle table structurally closed and machine-verifiable.

* **Supporting Insights:** The current spec already distinguishes operations from statuses, and `SUPERSEDE_PENDING` is described as transient rather than stable. Modeling rollback as "read the node's recorded `prior_status` field" is also truer to the current semantics than pretending that `"{prior_status}"` is itself a valid status token.
* **Citations:** [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum), [W3C SCXML Recommendation](https://www.w3.org/TR/scxml/).

#### Option B: Formalize `DELETED` and Rollback as First-Class Lifecycle States

Expand the core status vocabulary to include `DELETED` and replace `"{prior_status}"` with a typed lifecycle construct that validators and tooling can understand directly. This preserves the overall shape of the existing transition table and may feel more intuitive to implementers who want every operation to land on an explicit persisted state. The downside is that every consumer of `StatusEnum` must now recognize a broader state model, and the system must decide whether `DELETED` is a true stored node state or just a tombstone marker. That is a materially larger semantic commitment than the current six-state design implies.

* **Supporting Insights:** This strategy favors table continuity over model minimalism. It can work, but it changes the meaning of status across the whole DDR surface area rather than only repairing the transition contract.
* **Citations:** [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum), [W3C SCXML Recommendation](https://www.w3.org/TR/scxml/).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **State-Model Scope:** Option A keeps the persisted status model at six states and treats delete as an operation-level terminal effect. Option B broadens the core lifecycle vocabulary, which increases status-handling obligations across validators, serializers, and downstream tooling.
2. **Semantic Repair Cost:** Option A localizes the repair to lifecycle typing and transition expression, including a dynamic rollback reference and symmetric typing for prohibited transitions. Option B is more invasive because it requires a system-wide decision on what `DELETED` means as a stored status and how rollback placeholders become first-class lifecycle constructs.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

DDR v6.1 already has a compact status model and describes `SUPERSEDE_PENDING` as an operationally transient state. Preserving that smaller persisted vocabulary while typing the transition table is the clearest way to restore lifecycle closure without expanding the meaning of status across the entire system.

**Option A** is recommended because:

* **Closed-State Compliance:** It directly repairs the `INV-8` defect by forcing lifecycle endpoints back into the declared status set.
* **Lower Consumer Disruption:** Existing status-aware tooling can keep the current six-state model instead of being upgraded for a new global `DELETED` state.
* **Clearer Operational Semantics:** Delete and rollback remain operations with explicit handling rules rather than ambiguous pseudo-states embedded in the authoritative transition table.
* **Symmetric Lifecycle Closure:** The same typed boundary can be enforced for both allowed transitions and prohibited-transition lists, which eliminates the current `DELETED` leak from both schema surfaces.

### 4. GPT-5.4 Endorsement

GPT-5.4 endorses the current Recommended Strategy, **Option A**, as the maximally optimized solution for ISSUE-002.

This endorsement is based on the current DDR v6.1 evidence: the authoritative status vocabulary in the system definition and schema is six-state, while the defect is specifically that the lifecycle transition table is allowed to escape that vocabulary through unconstrained string endpoints. Option A repairs that exact break at the smallest semantic surface, restores `INV-8` closure, models rollback as a reference to the node's recorded `prior_status`, and avoids promoting operational effects such as delete into broader persisted-status obligations that the rest of the spec does not support.
