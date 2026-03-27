---
document:
  id:              DDR_v4_Issue-007
  title:           "Resolution Report for ISSUE-007: SUPERSEDE Atomicity and Rollback Are Underspecified"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "DESIGN_INADEQUACY"
---

## Optimized Resolution Strategy for "ISSUE-007"

### Agent Context

```yaml
id:          ISSUE-007
status:      RESOLVED
severity:    MAJOR
type:        DESIGN_INADEQUACY
tier_refs:   [ALL]
section_ref: §7.1
rule_refs:   [AX-3, INV-6]
```

### 1. Validation Audit of ISSUE-007

An evaluation of `.agent/assets/proposals/active/DDR System(Opus_v4).md` and `.agent/assets/proposals/active/DDR_v4_Issues_Tracker.md` was conducted to investigate the claims of "ISSUE-007: SUPERSEDE Atomicity and Rollback Are Underspecified."

The §7.1 Core Operations table (line 513) defines SUPERSEDE as: *"Mark node `SUPERSEDED`; create replacement with new ID"* with a validation trigger of: *"Old node retains ID; new node validated; children's `parent_ids` auto-updated to replacement ID then set `DIRTY` for content re-validation; this auto-update does not cascade DIRTY to grandchildren."* This description prescribes a three-step sequence — (1) mark the source node `SUPERSEDED`, (2) create and validate a replacement node via INSERT, (3) auto-update children's `parent_ids` to the replacement node — but provides no atomicity guarantee, no rollback specification, and no definition of the DAG's state if step 2 fails after step 1 has been applied.

The §3.5 DAG Invariants (line 169) states: *"At most one XPD node may carry `status: ACTIVE` at any time. SUPERSEDE of an XPD node must atomically set the predecessor to `SUPERSEDED` before the replacement node can be set to `ACTIVE`."* This invariant — which the issue tracker labels `INV-6` — explicitly guarantees atomicity for XPD SUPERSEDE operations. However, no equivalent atomicity guarantee exists for any other tier. The XPD invariant is scoped exclusively to the single-active-XPD constraint and does not generalize to SUPERSEDE operations on GPCL, FCL, SAL, or any other tier.

The §7.2 Dirty Flag Triggers section (lines 526, 533–534) describes the SUPERSEDE auto-update as a *"structural re-wiring operation"* and notes that *"grandchild's inherited content remains valid pending the child's own re-validation."* The *"Supersede-to-MODIFY Interaction"* note (line 534) describes a consequence chain — if a DIRTY child's re-validation results in a content MODIFY, standard cascade rules apply — but this note assumes the SUPERSEDE operation completed successfully. No text addresses the failure path where the replacement INSERT fails validation. The *"Deprecation Lifecycle"* note (line 535) distinguishes `DEPRECATED` (*"scheduled for replacement, no replacement yet exists"*) from `SUPERSEDED` (*"replacement exists and children have been re-wired"*), confirming that `SUPERSEDED` status semantically implies a valid replacement is present. A node in `SUPERSEDED` status with no replacement violates this semantic contract.

The §7.1 INSERT operation description (line 510) states that INSERT *"supports both forward (parent→child) and reverse (child→inferred parent) direction"* with validation triggers including *"full atomic ruleset; parent existence; DAG cycle detection."* The word *"atomically"* appears only in the §3.5 XPD invariant. The INSERT description does not state that INSERT *"fails atomically"* — the Issues Tracker's claim that INSERT *"fails atomically"* (Issue-007 Evidence & Justification, line 617) is a reasonable inference from the validation trigger description but is not a verbatim normative claim in the specification. This distinction matters: if INSERT failure semantics are also underspecified, the SUPERSEDE atomicity gap is compounded by an INSERT failure semantics gap.

The `AX-3` axiom (§2, line 47) states: *"Identical inputs produce unambiguous, mechanically verifiable outputs."* A SUPERSEDE operation whose intermediate failure state is undefined produces ambiguous outcomes — two implementations may handle a failed SUPERSEDE differently (one rolling back, another leaving the source node in `SUPERSEDED` status) — directly violating `AX-3`.

**Findings:**

1. **XPD-Only Atomicity Guarantee:** The DDR v4.0 specification provides an explicit atomicity guarantee for SUPERSEDE exclusively on XPD nodes (§3.5, line 169). No equivalent guarantee exists for any other tier. The SUPERSEDE operation description in §7.1 (line 513) prescribes a multi-step sequence without specifying whether the steps constitute an atomic transaction, are independently committable, or have defined rollback semantics on partial failure. Two compliant implementations may diverge on whether a failed replacement INSERT leaves the source node in its pre-SUPERSEDE status or in `SUPERSEDED` status with no replacement — an `AX-3` violation.

2. **Semantic Contract Violation on Partial Failure:** The specification defines `SUPERSEDED` as semantically meaning *"replacement exists and children have been re-wired"* (§7.2, line 535). If step 1 (mark source `SUPERSEDED`) is committed and step 2 (INSERT replacement) fails validation, the source node carries `SUPERSEDED` status while no replacement exists — a state that violates the specification's own semantic definition. This inconsistent state is not addressed by any operation: no recovery operation restores a `SUPERSEDED` node to its prior status, and the node status lifecycle (as documented in ISSUE-006) does not define an outbound transition from `SUPERSEDED`.

3. **Orphan-Creation Failure Mode:** If step 1 and step 2 succeed but step 3 (auto-update children's `parent_ids`) partially fails — for example, if some children are updated but a system failure interrupts the process — the DAG enters a state where some children reference the superseded node and others reference the replacement. VERIFY would detect structural violations (children citing a `SUPERSEDED` parent with `CIT-R1`/`CIT-R2` implications), but no operation is defined to complete or reverse a partially applied SUPERSEDE. The reconciliation manifest has no entry type for "incomplete SUPERSEDE" — repair requires manual intervention not specified in the protocol.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-007

The resolution must define the atomicity contract for SUPERSEDE operations across all tiers, specify the DAG's state on partial failure, and provide either rollback semantics or an explicit intermediate state that enables recovery — satisfying `AX-3` by ensuring identical SUPERSEDE inputs produce unambiguous, mechanically verifiable outcomes regardless of success or failure.

#### Option A: Define SUPERSEDE as a Strict Atomic Transaction with Guaranteed Rollback

Extend the §7.1 SUPERSEDE operation description with a normative atomicity clause applicable to all tiers (not only XPD). The clause specifies that SUPERSEDE is a single atomic transaction encompassing all three steps: (1) transition source node to `SUPERSEDED`, (2) INSERT and validate replacement node, (3) re-wire children's `parent_ids` to the replacement ID and set children `DIRTY`. All three steps must succeed for any step to be committed. If step 2 (replacement INSERT) fails validation, the entire operation rolls back: the source node reverts to its pre-SUPERSEDE status (`ACTIVE` or `DEPRECATED`), no replacement node is created, and no child `parent_ids` are modified. If step 3 (child re-wiring) fails after step 2 succeeds, the rollback removes the replacement node and reverts the source node to its prior status. The reconciliation manifest records failed SUPERSEDE attempts as a new entry type: `SUPERSEDE_FAILED` with fields for the source node ID, the attempted replacement content, the validation error or failure reason, and a timestamp. The §3.5 XPD atomicity invariant is generalized: the existing XPD-specific language is replaced with a universal statement — *"SUPERSEDE of any node must be atomic; partial application constitutes a structural violation detectable by VERIFY"* — and the XPD single-active constraint is preserved as an additional guard condition specific to XPD SUPERSEDE operations.

* **Supporting Insights:** This approach aligns with the DDR specification's existing all-or-nothing semantics for INSERT (§7.1, line 510), which validates against the "full atomic ruleset; parent existence; DAG cycle detection" before committing a node. Extending the same transactional boundary to encompass the full SUPERSEDE sequence ensures consistency across mutation operations. The `SUPERSEDE_FAILED` manifest entry type gives VERIFY and the reconciliation workflow explicit visibility into failed replacement attempts, enabling agents to diagnose and retry without manual DAG inspection. The generalization of `INV-6` from XPD-only to all tiers eliminates the asymmetric atomicity guarantee that currently treats XPD nodes as structurally privileged — a distinction with no justified basis given that partial SUPERSEDE failure produces identical structural corruption regardless of the source node's tier.

* **Citations:** ISO/IEC 10026-1:1998 (Information technology — Open Systems Interconnection — Distributed Transaction Processing) defines the atomic commitment protocol requiring that all participants in a distributed operation either commit or abort, with no intermediate states visible to external observers. The ACID atomicity property as formalized in Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques* (Morgan Kaufmann, 1993), establishes that an atomic operation is indivisible — it either completes in its entirety or has no effect on the system state. The Two-Phase Commit protocol (2PC) specified in ISO/IEC 14834:1996 (The XA Specification) provides a proven coordination mechanism for ensuring all-or-nothing semantics across multi-step operations involving multiple resources.

#### Option B: Introduce a `SUPERSEDE_PENDING` Intermediate Status with Explicit Recovery Semantics

Add `SUPERSEDE_PENDING` as a sixth value to the `status` enum, representing the in-progress state of a SUPERSEDE operation. The operation proceeds: (1) transition source node from its current status to `SUPERSEDE_PENDING`, recording the prior status in a new `prior_status` field on the node; (2) attempt INSERT of the replacement node with full validation; (3a) on success: transition source node from `SUPERSEDE_PENDING` to `SUPERSEDED`, re-wire children's `parent_ids`, set children `DIRTY`; (3b) on failure: transition source node from `SUPERSEDE_PENDING` back to its `prior_status` value, discard the failed replacement, leave children unmodified. VERIFY treats any node found in `SUPERSEDE_PENDING` status as a structural violation requiring resolution — either by completing the SUPERSEDE (retrying the replacement INSERT) or by reverting to the prior status. The `SUPERSEDE_PENDING` state has a maximum duration (configurable, default: indefinite with VERIFY advisory) beyond which VERIFY escalates the advisory from informational to blocking. The `prior_status` field is write-once during the `SUPERSEDE_PENDING` transition and cleared when the node exits `SUPERSEDE_PENDING`. The schema addition is non-breaking: existing YAML files with only five status values remain valid, and `SUPERSEDE_PENDING` is only entered programmatically during an active SUPERSEDE operation.

* **Supporting Insights:** This approach makes the transient state explicitly visible in the DAG rather than hiding it behind a transactional boundary — a design choice that is advantageous in agentic workflows where SUPERSEDE operations may span multiple agent invocations or require asynchronous validation. A node in `SUPERSEDE_PENDING` is a clear signal to both automated tools and human operators that an in-flight operation requires attention, unlike the implicit corruption state that a failed atomic transaction might silently produce if the rollback mechanism itself fails. The `prior_status` field provides a deterministic revert target without requiring the implementation to maintain a separate transaction journal or undo log, reducing infrastructure requirements for DDR implementations. The approach parallels the saga pattern used in distributed systems, where long-running operations are decomposed into individually committable steps with compensating actions — each step (mark pending, attempt replacement, finalize or revert) is independently observable and recoverable.

* **Citations:** The Saga pattern, originally formalized by Hector Garcia-Molina and Kenneth Salem in "Sagas" (*ACM SIGMOD Record*, Vol. 16, No. 3, 1987), defines a sequence of local transactions with compensating transactions for each step, providing atomicity guarantees for long-running operations without requiring global locking — directly applicable to the multi-step SUPERSEDE operation where each step can be independently compensated. The Outbox Pattern described in Chris Richardson, *Microservices Patterns* (Manning Publications, 2018), Chapter 4, establishes precedent for making intermediate operational states explicitly persistent and observable rather than relying on implicit transactional boundaries, ensuring recoverability in systems where operations may span multiple service invocations.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **Atomicity Model:** Option A provides classical ACID atomicity — the SUPERSEDE operation is invisible to external observers in any intermediate state. The DAG is either in its pre-SUPERSEDE or post-SUPERSEDE state, never in between. Option B makes the intermediate state explicitly visible via `SUPERSEDE_PENDING`, trading strict atomicity for operational transparency. In single-agent, synchronous execution environments, Option A's invisible intermediate state is cleaner. In multi-agent, asynchronous, or long-running execution environments — which are the DDR's primary deployment context — Option B's visible intermediate state provides superior observability and recoverability.

2. **Schema Impact:** Option A requires no schema changes to the `status` enum — the five existing values are sufficient, and the atomicity guarantee is a behavioural specification, not a structural one. Option B adds `SUPERSEDE_PENDING` as a sixth status value and introduces a `prior_status` field, requiring a minor schema version increment and updates to all validation logic that consumes the `status` enum. The ISSUE-006 resolution (if Option B from ISSUE-006 is adopted) would need to incorporate `SUPERSEDE_PENDING` into the formal `lifecycle.status_transitions` block.

3. **Infrastructure Requirements:** Option A requires the storage layer to support transactional semantics — either copy-on-write, journaling, or an undo log mechanism — to guarantee rollback on failure. This is a non-trivial infrastructure requirement that may not be satisfied by all DDR implementation environments (e.g., a file-system-based YAML store without transactional semantics). Option B is implementable without transactional infrastructure: each step writes a single observable state change, and recovery is achieved by reading the `prior_status` field and reverting — no journal or undo log is required.

4. **ISSUE-006 Interaction:** Both options require updates to the node status lifecycle state machine. Option A adds no new states but requires the lifecycle specification to formally document that `SUPERSEDED` is unreachable as a partial state — all transitions into `SUPERSEDED` are guarded by the SUPERSEDE atomicity contract. Option B adds `SUPERSEDE_PENDING` as a new state with defined inbound transitions (`ACTIVE→SUPERSEDE_PENDING`, `DEPRECATED→SUPERSEDE_PENDING`) and outbound transitions (`SUPERSEDE_PENDING→SUPERSEDED` on success, `SUPERSEDE_PENDING→{prior_status}` on failure), requiring corresponding entries in the §3.8 transition table and/or `lifecycle.status_transitions` YAML block.

5. **Failure Observability:** Option A's rollback is silent — a failed SUPERSEDE leaves no trace in the DAG itself (only in the reconciliation manifest's `SUPERSEDE_FAILED` entry). An operator inspecting the DAG sees no evidence of the attempt. Option B's `SUPERSEDE_PENDING` status is immediately visible to any DAG observer, including VERIFY, human reviewers, and other agents — providing a built-in diagnostic signal without requiring manifest inspection. For debugging and operational monitoring in agentic workflows, Option B's visible intermediate state is materially more useful.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A + Option B Combined (Recommended Strategy)**.

The two options are complementary rather than competing: Option A defines the normative atomicity contract (SUPERSEDE must be all-or-nothing — no partial application is permitted), while Option B provides the implementation mechanism that makes that contract achievable without requiring transactional storage infrastructure. The `SUPERSEDE_PENDING` intermediate status (Option B) is the mechanism through which the atomicity guarantee (Option A) is realized in practice: the pending state makes rollback deterministic (`prior_status` → revert) and success confirmable (`SUPERSEDE_PENDING` → `SUPERSEDED` only after replacement validation and child re-wiring complete). The `SUPERSEDE_FAILED` manifest entry (Option A) records the attempt for audit trail purposes, while the `SUPERSEDE_PENDING` detection by VERIFY (Option B) provides real-time operational visibility.

**Option A + B Combined** is recommended because:

* **AX-3 Satisfaction:** The combined approach produces unambiguous, mechanically verifiable outcomes for every SUPERSEDE execution path — success transitions through `SUPERSEDE_PENDING` to `SUPERSEDED` with child re-wiring, failure reverts from `SUPERSEDE_PENDING` to `prior_status` with no replacement created. No intermediate state is undefined or implementation-dependent, satisfying `AX-3` determinism across all DDR implementations.
* **Universal Atomicity Without Infrastructure Assumptions:** Option A's strict atomicity contract is normatively correct but requires transactional storage semantics that not all DDR implementations can provide. Option B's saga-style decomposition makes the same guarantee achievable using only single-field status writes and a `prior_status` revert path — eliminating the infrastructure dependency while preserving the all-or-nothing semantic contract.
* **Agentic Workflow Compatibility:** In Antigravity-powered workflows where SUPERSEDE operations may span multiple agent invocations, the `SUPERSEDE_PENDING` state provides a checkpoint from which any agent can resume or compensate — unlike Option A alone, where a failed rollback in a stateless agent session could leave the DAG in an unrecoverable state with no visible diagnostic signal.
* **ISSUE-006 Coherence:** The combined approach feeds directly into the ISSUE-006 lifecycle state machine resolution by adding `SUPERSEDE_PENDING` as a formally defined state with explicit transitions and guard conditions, strengthening the overall lifecycle contract rather than creating an isolated fix.

### 4. Concluding Notation

**Reviewer Determination (Maximal Optimization Check): APPROVED.**

After re-evaluating the issue framing, option set, tradeoff analysis, and endorsement rationale, I concur that the endorsed **Option A + Option B Combined** strategy is the maximally optimized resolution for ISSUE-007 under DDR v4.0 constraints. It uniquely delivers deterministic all-tier SUPERSEDE semantics, operational recoverability in non-transactional environments, and direct lifecycle harmonization with ISSUE-006 while preserving AX-3 conformance.