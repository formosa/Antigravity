---
document:
  id:              DDR_v6.2_Issue-003
  title:           "Resolution Report for ISSUE-003: Close `SUPERSEDE_PENDING` Exit Semantics Machine-Readably"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  resolved:        "2026-03-28"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "LIFECYCLE_GAP"
---

## Optimized Resolution Strategy for "ISSUE-003"

### Agent Context

```yaml
id:          ISSUE-003
status:      RESOLVED
severity:    MAJOR
type:        LIFECYCLE_GAP
tier_refs:   ["Lifecycle authority"]
section_ref: "\u00a73.8"
rule_refs:   ["INV-8", "gc-007", "gc-008", "gc-009"]
updated:     2026-03-28
resolved:    2026-03-28
```

### 1. Validation Audit of ISSUE-003

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2557-2646` and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:1096-1107` was conducted to investigate the claims of "ISSUE-003: Close `SUPERSEDE_PENDING` Exit Semantics Machine-Readably".

The lifecycle graph names allowed transitions, but the companion prohibition table is not exhaustive and cannot express “all other targets are forbidden.” The defect is visible at `SUPERSEDE_PENDING`, but the same incompleteness appears across other non-terminal statuses as well.

**Findings:**

1. **Lifecycle Authority Is Split:** Allowed transitions and prohibited transitions are both treated as authoritative even though they drift.
2. **The Gap Is Systemic:** The incompleteness affects multiple statuses, not just `SUPERSEDE_PENDING`.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-003

The resolution goal is to restore one closed lifecycle authority so implementations cannot disagree about undefined edges.

#### Option A: Add Explicit Closed Transition Metadata

Augment the lifecycle contract with machine-readable fields such as `allowed_targets`, `allows_prior_status_rollback`, or `closed_transition_set` for any status whose blacklist is meant to be exhaustive. At minimum this must close `SUPERSEDE_PENDING`; ideally it should eliminate the current ambiguity for `DRAFT`, `ACTIVE`, `DIRTY`, and `DEPRECATED` at the same time.

* **Supporting Insights:** Extra closed-transition metadata can patch the current model, but it still preserves dual authority.
* **Citations:** [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema enum](https://json-schema.org/understanding-json-schema/reference/enum)

#### Option B: Make Allowed Transitions the Sole Authority

Refactor lifecycle validation so `status_transitions` is the only authoritative transition graph and `prohibited_transitions` becomes derived documentation rather than a parallel blacklist. This is a bigger model change, but it removes the need to maintain two partially redundant views of the same state machine.

* **Supporting Insights:** One authoritative transition graph is easier to validate and harder to let drift.
* **Citations:** [W3C SCXML](https://www.w3.org/TR/scxml/), [JSON Schema enum](https://json-schema.org/understanding-json-schema/reference/enum)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Single Authority:** Option B collapses lifecycle semantics into one graph; Option A retains a parallel prohibition surface.
2. **Patch vs Cleanup:** Option A is more localized, but Option B fixes the model that caused the drift.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

The defect is deeper than one missing prohibition row. The tracker now favors a single authoritative transition graph because DDR already has evidence that parallel lifecycle surfaces drift under maintenance.

**Option B** is recommended because:

* **Eliminates Drift:** One graph removes manual alignment between two lifecycle authorities.
* **Improves Determinism:** Implementations validate against one closed state machine.
* **Scales Better:** Future lifecycle refinements do not reopen the same dual-surface problem.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` and `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml`.

The v6.3 lifecycle contract now treats `status_transitions` as the sole machine-authoritative state graph. `prohibited_transitions` was removed from both the schema and the system file, the lifecycle authority text now states that any transition not enumerated in `status_transitions` is invalid, and the system lifecycle table was normalized onto that single authoritative surface.

Validation evidence:
- `.venv\Scripts\python.exe` YAML-parse check succeeded for both v6.3 YAML artifacts.
- Draft 2020-12 validation of `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` against `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` succeeded after removal of the parallel `prohibited_transitions` surface.
