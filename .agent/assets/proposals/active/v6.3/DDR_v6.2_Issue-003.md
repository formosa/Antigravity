---
document:
  id:              DDR_v6.2_Issue-003
  title:           "Resolution Report for ISSUE-003: Close `SUPERSEDE_PENDING` Exit Semantics Machine-Readably"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  status:          "OPEN"
  severity:        "MAJOR"
  type:            "LIFECYCLE_GAP"
---

## Optimized Resolution Strategy for "ISSUE-003"

### Agent Context

```yaml
id:          ISSUE-003
status:      OPEN
severity:    MAJOR
type:        LIFECYCLE_GAP
tier_refs:   ["Lifecycle authority"]
section_ref: "§3.8"
rule_refs:   []
updated:     2026-03-27
```

### 1. Validation Audit of ISSUE-003

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2591-2603`, `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2640-2646`, and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:1062-1107` was conducted to investigate the claims of "ISSUE-003: Close `SUPERSEDE_PENDING` Exit Semantics Machine-Readably."

The lifecycle authority defines exactly two legal exits from `SUPERSEDE_PENDING`: `SUPERSEDE_COMPLETE -> SUPERSEDED` and `SUPERSEDE_ROLLBACK -> prior_status`, as shown at `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2591-2603`. The parallel `prohibited_transitions` table names only `DRAFT` at `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2640-2646`, even though its reason text says that all other exits are prohibited. The schema explains why this drift exists: `StatusTransition` can model the special rollback case via `to_node_field: prior_status` at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:1062-1094`, but `ProhibitedTransition.to` is only an explicit array of status enums at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:1096-1107`.

**Findings:**

1. **Two Lifecycle Authorities Can Drift:** The allowed-transition graph and the prohibited-transition blacklist do not currently encode the same state space. That makes the machine-readable lifecycle contract less deterministic than the prose suggests.
2. **The Blacklist Shape Cannot Express the Intended Closure:** The schema can represent the special rollback edge in `status_transitions`, but it cannot express "all remaining targets except that rollback form" inside the current `prohibited_transitions` model.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-003

The resolution goal is to make the `SUPERSEDE_PENDING` exit space fully deterministic for validators and other lifecycle consumers.

#### Option A: Add Explicit Closed Exit Metadata

Augment the lifecycle contract with a machine-readable field such as `allowed_targets`, `allows_prior_status_rollback`, or `closed_exit_set` for `SUPERSEDE_PENDING`. This keeps the current two-table structure intact while giving validators an explicit source of truth for the full exit set. It is the smaller patch because it addresses the specific closure gap without changing the broader lifecycle model.

* **Supporting Insights:** The schema already has the information needed to express the intended rollback special case; what is missing is a field that closes the rest of the state space. A targeted metadata addition would let existing consumers evolve without abandoning the current lifecycle document structure.
* **Citations:** No authoritative external reference identified for this specific claim.

#### Option B: Make Allowed Transitions the Sole Authority

Refactor lifecycle validation so `status_transitions` becomes the only authoritative transition graph and `prohibited_transitions` is treated as derived documentation or removed from machine evaluation. This is a wider model change, but it eliminates the need to keep two partially redundant lifecycle views in sync. The special rollback form already lives naturally in the allowed-transition structure, so consolidating authority there removes the exact source of the current defect.

* **Supporting Insights:** The present inconsistency exists because the lifecycle contract duplicates the same semantic space in two different representations. Making the allowed transition graph authoritative gives validators one place to resolve normal targets and rollback indirection together.
* **Citations:** No authoritative external reference identified for this specific claim.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Authority Model:** Option A patches the closure gap while preserving dual lifecycle representations; Option B removes the duplicated machine authority that caused the drift.
2. **Implementation Scope:** Option A is a smaller schema and validator update focused on one state; Option B is a broader lifecycle refactor with a larger migration surface.
3. **Long-Term Consistency:** Option A improves the current model, but future lifecycle edits must still keep multiple views aligned. Option B makes the transition graph single-source and therefore harder to desynchronize.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

Although Option B is the broader change, the validated defect exists because lifecycle authority is split across parallel representations that cannot express the same semantics cleanly. Consolidating machine authority in `status_transitions` resolves the `SUPERSEDE_PENDING` ambiguity and reduces the chance of future state-machine drift.

**Option B** is recommended because:

* **Eliminates Duplicate Authority:** Validators no longer have to reconcile a partially redundant blacklist against the real transition graph.
* **Keeps Rollback Semantics Native:** The existing `to_node_field: prior_status` shape already fits naturally in the allowed-transition model.
* **Improves Future Maintainability:** New lifecycle states and rollback-like patterns can be added in one authoritative graph instead of multiple synchronized tables.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
