---
document:
  id:              DDR_v4_Issue-012
  title:           "Resolution Report for ISSUE-012: Candidate Pool Has No Pause State"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "OPEN"
  severity:        "MINOR"
  type:            "LIFECYCLE_GAP"
---

## Optimized Resolution Strategy for "ISSUE-012"

### Agent Context

```yaml
id:          ISSUE-012
status:      OPEN
severity:    MINOR
type:        LIFECYCLE_GAP
tier_refs:   [ARE_E5]
section_ref: §8.2
rule_refs:   []
```

### 1. Validation Audit of ISSUE-012

An evaluation of `DDR System(Opus_v4).md` (§8.1, §8.2, §8.3, §9 E5), `ddr_system_v4.0.yaml` (extension_system, extension_catalog), `ddr_node_schema.yaml` (extension_system schema), and `DDR_v4_Adversarial_Audit.md` (Finding-12) was conducted to investigate the claims of "ISSUE-012: Candidate Pool Has No Pause State."

The Extension Candidate Pool is defined in `DDR System(Opus_v4).md` §8.2 (lines 571–579) as a staging area outside the Core DAG for ARE-inferred nodes. Five properties are enumerated:

1. *"Carry `status: CANDIDATE` (not a Core status value)"*
2. *"Are visible only when the ARE extension is active"*
3. *"Have no effect on Core DIRTY/CLEAN status"*
4. *"Must be promoted into the Core DAG via INSERT (triggering full validation) to become Core nodes"*
5. *"Are automatically discarded when ARE is disabled"*

The fifth property — `"Are automatically discarded when ARE is disabled"` — is the operative constraint. The YAML encoding at `ddr_system_v4.0.yaml` lines 1063–1075 repeats this as `discard_trigger: "Automatically discarded when ARE is disabled."` No intermediate activation state (pause, hold, suspend) is defined in either source. The visibility rule (`"Visible only when the ARE extension is active"`) implies a binary state model: active → visible and generating; disabled → invisible and discarded.

`EXT-R5` (`DDR System(Opus_v4).md`, line 589) states: *"Disabling an Extension leaves Core CLEAN/DIRTY status unchanged."* This rule governs the Core-facing side-effects of Extension deactivation but does not address Extension-internal state preservation. The Candidate Pool is explicitly outside the Core DAG, meaning `EXT-R5` does not normatively prevent Pool retention during deactivation — it simply does not address the question.

The ARE Extension contract (§9 E5, `DDR System(Opus_v4).md`, lines 642–653) defines four rules (`ARE-R1` through `ARE-R4`) governing candidate placement, scoring, promotion, and authorship restrictions. None of these rules address ARE activation lifecycle or Pool persistence across state transitions.

`DDR_v4_Adversarial_Audit.md` Finding-12 (lines 244–251) independently identifies this gap: *"A practitioner mid-way through reviewing a batch of 20 ARE-generated candidates must either complete the review or lose all candidates."* The audit recommends adding a `paused` state: `active | paused | disabled`.

The `ddr_node_schema.yaml` Extension System schema (lines 253–293) defines `candidate_pool` as a nested object with five string properties (`description`, `candidate_status_value`, `visibility_rule`, `effect_on_core_status`, `promotion_mechanism`, `discard_trigger`). No `activation_states` field or lifecycle state machine exists in the schema.

**Findings:**

1. **Binary Activation Lifecycle:** The ARE Extension operates on a strict two-state model — `active` or `disabled` — with no intermediate state. The transition from `active` to `disabled` unconditionally discards the entire Candidate Pool. This is a data-loss transition with no recovery path: all pending, partially-reviewed, or queued candidates are destroyed. There is no mechanism to preserve review progress.

2. **Operational Inefficiency in Agentic Workflows:** In cost-sensitive or resource-constrained environments, ARE inference may be computationally expensive. Practitioners may need to temporarily halt inference to manage API costs, computational budgets, or workload capacity — while retaining candidates already generated for ongoing review. The binary model forces an all-or-nothing choice: continue inference (active) or lose everything (disabled). This creates an operational penalty disproportionate to the intent of the deactivation.

3. **No Conflict with Core Invariants:** Introducing a pause state creates no Core DAG integrity concerns. The Candidate Pool is explicitly outside the Core DAG (§8.2), carries a non-Core status value (`CANDIDATE`), and has no effect on Core DIRTY/CLEAN status. `EXT-R5` confirms that Extension state changes do not affect Core status. A `paused` state that retains candidates without generating new ones is structurally invisible to the Core.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-012

The resolution must provide a mechanism for practitioners to halt ARE inference while preserving the existing Candidate Pool for continued review, without introducing Core DAG side-effects or conflicting with existing Extension integration rules.

#### Option A: Add a Tri-State Activation Model to ARE

Extend the ARE Extension lifecycle with a three-state activation model: `active | paused | disabled`. Define the semantics of each state and the permitted transitions:

| State      | Inference | Pool Visibility | Pool Preserved | Promotion Allowed | Discard Allowed |
|------------|-----------|-----------------|----------------|-------------------|-----------------|
| `active`   | Running   | Yes             | Yes            | Yes               | Yes             |
| `paused`   | Halted    | Yes             | Yes            | Yes               | Yes             |
| `disabled` | Halted    | No              | No             | No                | N/A (auto-discarded) |

**Transition rules:**
- `active → paused`: Inference halts immediately. Existing Candidate Pool is retained and browsable. INSERT promotion and manual discards remain available. No new candidates are generated.
- `paused → active`: Inference resumes, adding new candidates to the existing Pool. Previously reviewed or annotated candidates retain their state.
- `paused → disabled`: Pool is discarded (identical to `active → disabled`).
- `active → disabled`: Pool is discarded (existing behavior, unchanged).
- `disabled → active`: ARE starts fresh with an empty Candidate Pool (existing behavior, unchanged).
- `disabled → paused`: Not permitted (no Pool exists to pause over).

This requires adding a `paused` state to the §8.2 Candidate Pool definition and an `activation_states` field to the ARE Extension contract. The `ddr_node_schema.yaml` extension_system schema gains an optional `activation_states` property on the `candidate_pool` object.

* **Supporting Insights:** The DDR specification already models multi-state lifecycles for nodes (`DRAFT`, `ACTIVE`, `DIRTY`, `DEPRECATED`, `SUPERSEDED`), and the design philosophy emphasizes that optional capabilities should not compromise Core stability. The `paused` state is the Extension-level analogue of `DIRTY` — a named state indicating "temporarily not progressing, but data is preserved." The specification's own `CL` and `XPD` tiers demonstrate that optional activation (`is_optional: true`) does not require binary presence/absence — tiers can be inactive without data loss.

* **Citations:** ISO/IEC 42001:2023 ("AI Management System Standard") §6.1.4 requires organizations to manage AI system resources responsibly, including computational cost management and the ability to pause AI processing without data loss. The concept of graceful degradation in AI system lifecycle management is documented in NIST AI RMF 1.0 (AI-600-1, "Artificial Intelligence Risk Management Framework"), which emphasizes that AI systems should support controlled deactivation states that preserve work-in-progress artifacts.

#### Option B: Introduce a SNAPSHOT_POOL / RESTORE_POOL Operation Pair

Rather than modifying the ARE activation model, define two new Extension-level operations (not Core operations) that provide explicit Pool persistence:

- **`SNAPSHOT_POOL [snapshot_name]`:** Serializes the current Candidate Pool — including all candidate nodes, their `ARE::confidence_score` annotations, review status, and any practitioner notes — to a named, human-readable file (e.g., `.agent/are_snapshots/snapshot_name.yaml`). The snapshot includes a metadata header with the timestamp, ARE configuration state, and candidate count. Multiple snapshots can coexist.

- **`RESTORE_POOL [snapshot_name]`:** Loads a previously saved snapshot into the active Candidate Pool. Requires ARE to be in `active` state. Validates that restored candidates do not conflict with any candidates currently in the Pool (duplicate candidate IDs are rejected). Restores all metadata and annotations from the snapshot.

This approach uses the existing binary activation model (active/disabled) but adds explicit persistence operations. Before disabling ARE, the practitioner snapshots the Pool. After re-enabling ARE, they restore the snapshot. The Pool persistence becomes an explicit, auditable action rather than an implicit lifecycle state.

* **Supporting Insights:** The DDR specification's §7 Operations protocol establishes a pattern of named, atomic operations with defined pre/post-conditions (INSERT, MODIFY, SUPERSEDE, etc.). `SNAPSHOT_POOL` and `RESTORE_POOL` follow this same pattern — they are atomic, have clear triggers, and produce deterministic outcomes. The reconciliation manifest (§7 dirty flag model) already demonstrates the concept of serializing DAG state for audit purposes. Pool snapshots extend this pattern to Extension-internal state.

* **Citations:** The Git version control model provides precedent: `git stash` (analogous to `SNAPSHOT_POOL`) preserves work-in-progress without committing, and `git stash pop` (analogous to `RESTORE_POOL`) restores it. This pattern is well-understood by practitioners and maps naturally to the Pool preservation use case. The OpenAPI Specification v3.1 documents Extension state management patterns where auxiliary data structures are persisted independently of the primary artifact lifecycle.

#### Option C: Tri-State Lifecycle + Mandatory Persisted Pool Checkpoint (New)

Introduce a composite lifecycle strategy that preserves Option A ergonomics while closing its restart/session durability gap:

1. Keep `active | paused | disabled` activation states.
2. Define `paused` as **durable** (Pool retained in-memory and persisted to a canonical Extension checkpoint file).
3. Require automatic checkpoint writes on `active → paused`, periodic checkpointing while paused, and checkpoint load on process restart when state is `paused`.
4. Keep `disabled` semantics unchanged (Pool discarded on `→ disabled`).

| State      | Inference | Pool Visibility | Pool Preserved (Runtime) | Pool Preserved (Restart) | Promotion Allowed |
|------------|-----------|-----------------|---------------------------|--------------------------|-------------------|
| `active`   | Running   | Yes             | Yes                       | Optional                 | Yes               |
| `paused`   | Halted    | Yes             | Yes                       | **Yes (required)**       | Yes               |
| `disabled` | Halted    | No              | No                        | No                       | No                |

**Operational semantics:**
- `active → paused`: stop inference and atomically persist the current Pool to `.agent/state/are_candidate_pool.checkpoint.yaml`.
- `paused` steady state: allow review/promotion/discard; persist after each mutating action or at bounded intervals.
- system restart while `paused`: restore checkpoint automatically and keep state as `paused`.
- `paused → active`: resume inference without data loss; keep checkpointing policy optional.
- `paused → disabled` or `active → disabled`: delete checkpoint and discard Pool (explicit destruction preserved).

* **Supporting Insights:** This retains the low cognitive load of Option A (single pause control), while providing the durability and audit continuity benefits of Option B without relying on manual snapshot discipline. It also preserves the documented intentional destruction semantics of `disabled` as a clear lifecycle boundary.

* **Citations:** ISO/IEC 42001 and NIST AI RMF controls emphasize resilient operational controls and traceability for AI-assisted workflows; Option C best satisfies both by combining human factors optimization and durable state management.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **User Experience and Cognitive Load:** Option A and Option C are both low-friction, single-control workflows. Option B has higher cognitive load because it requires explicit save/restore discipline.

2. **Audit and Reproducibility:** Option B and Option C provide persistent artifacts; Option A by itself is weakest unless paired with additional persistence requirements.

3. **Implementation Complexity:** Option A has the lowest implementation scope. Option B has the largest API/operation footprint. Option C is moderate: it extends Option A with one canonical checkpoint mechanism, avoiding the multi-snapshot UX and restore conflict surface of Option B.

4. **Multi-Session Persistence:** Option C and Option B support restart/session continuity. Option A does not guarantee this unless further extended.

5. **Data-Loss Risk:** Option C is strongest: no manual snapshot prerequisite plus mandatory persistence on pause. Option A avoids immediate loss during temporary halts but still risks loss on restart. Option B is only safe when the user remembers to snapshot.

6. **Specification Precedent Alignment:** Option A aligns with lifecycle states. Option B aligns with explicit operations. Option C cleanly composes both paradigms while keeping the Core DAG isolation constraints unchanged.

#### Updated Endorsement and Justification

I do **not** agree that Option A alone is the maximally optimized strategy.

The maximally optimized resolution is **Option C (Updated Recommended Strategy)**, because it preserves the strongest properties of Option A (intuitive pause control, no manual save steps) and adds the durability guarantees identified as a meaningful weakness in the original endorsement.

**Option C** is newly endorsed because:

* **Best Safety/Ergonomics Balance:** Practitioners get one-step pause behavior with automatic durability, eliminating both immediate discard risk and restart-loss risk.
* **Controlled Specification Expansion:** The added surface area is bounded to one checkpoint convention and deterministic transition behavior, avoiding the broader command lifecycle and naming semantics required by Option B.
* **Preserved Existing Semantics:** `disabled` continues to mean destructive teardown; no ambiguity is introduced.
* **Future-Compatible:** If explicit snapshots are later desired for branching review scenarios, Option B-style named snapshots can be layered on top of Option C without changing core lifecycle semantics.

### 4. Concluding Notation

**Reviewer Conclusion:** I have provided an updated endorsement. The recommended strategy for ISSUE-012 is now **Option C: Tri-State Lifecycle + Mandatory Persisted Pool Checkpoint** as the maximally optimized resolution approach.
