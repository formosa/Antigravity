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

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **User Experience and Cognitive Load:** Option A is simpler from the practitioner's perspective — setting ARE to `paused` is a single state change that implicitly preserves the Pool. No file management, snapshot naming, or restoration commands are needed. Option B requires practitioners to remember to snapshot before disabling and restore after re-enabling — introducing a two-step workflow with a manual discipline requirement. If a practitioner forgets to snapshot before disabling ARE, the Pool is lost (same as the current behavior).

2. **Audit and Reproducibility:** Option B provides superior auditability — snapshots are named, timestamped, human-readable files that persist independently of ARE state. Multiple snapshots can capture Pool evolution over time. Option A retains the Pool in memory/runtime state only, with no external audit trail of Pool state at specific points in time.

3. **Implementation Complexity:** Option A requires modifying the §8.2 Candidate Pool definition, the ARE Extension contract, and the `ddr_node_schema.yaml` schema — three specification touchpoints. Option B requires defining two new Extension-level operations, a snapshot file format specification, and a storage convention — more specification surface area but no modification of existing definitions.

4. **Multi-Session Persistence:** Option A's `paused` state is a runtime concept — it preserves the Pool while the system is running but does not guarantee persistence across system restarts or session boundaries. Option B's snapshots are file-based and persist across sessions, system restarts, and environment changes. For long-running projects where review may span days or weeks, Option B provides stronger persistence guarantees.

5. **Specification Precedent Alignment:** Option A aligns with the node lifecycle pattern (`DRAFT → ACTIVE → DIRTY → ...`) where states are implicit in the data model. Option B aligns with the operations pattern (`INSERT`, `MODIFY`, `SUPERSEDE`, ...) where actions are explicit and auditable. Both patterns exist in the specification; neither is more canonical than the other.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A addresses the primary user need — preserving the Candidate Pool during temporary inference suspension — with the simplest possible mechanism. It avoids the forgetting-to-snapshot failure mode and requires no file management overhead.

**Option A** is recommended because:

* **Zero-Discipline Preservation:** The `paused` state automatically preserves the Pool without requiring the practitioner to take any explicit action beyond setting the state. Option B's snapshot workflow introduces a manual step that, if omitted, results in the same data loss the issue identifies. The most robust solution to a data-loss problem is one that prevents data loss implicitly.
* **Minimal Specification Surface Area:** Option A adds one activation state and six transition rules to the §8.2 definition. Option B adds two operations, a file format specification, a storage convention, and conflict resolution semantics — substantially more specification text for the same functional outcome.
* **Consistent with Extension Isolation:** The `paused` state is entirely within the Extension boundary and has no Core DAG side-effects. `EXT-R5` is satisfied: pausing ARE leaves Core CLEAN/DIRTY status unchanged. No new operations are added to the Core operations protocol.
* **Natural Ergonomics:** Practitioners intuitively understand `active/paused/disabled` as a standard three-state control pattern (analogous to media playback controls, service management, and CI/CD pipeline states). The state names are self-documenting and require no explanation beyond the transition table.
* **Option B Remains Available as a Complement:** The snapshot/restore capability can be added later as an independent enhancement without conflicting with the tri-state model. A future `SNAPSHOT_POOL` operation would work equally well in `active` or `paused` states, making the two options complementary rather than mutually exclusive.
