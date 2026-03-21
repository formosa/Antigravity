# AGENTS.md — DDR System v4.0

## Project Overview

This repository contains the DDR (Document-Driven Requirements) System
specification v4.0. The task assigned to this agent is the resolution of
**ISSUE-008: UNBUNDLE Rejection Behaviour Is Underspecified**, as documented
in `.agent\assets\proposals\active\DDR_v4_Issue-008.md`.

---

## Authoritative Files

| File | Role | Editable |
|---|---|---|
| `.agent\assets\proposals\active\ddr_system_v4.0.yaml` | Normative specification — PRIMARY TARGET | ✅ Yes |
| `.agent\assets\proposals\active\DDR System(Opus_v4).md` | Human-readable reference rendering | ❌ No |
| `.agent\assets\proposals\active\DDR_v4_Issue-008.md` | Issue report and endorsed resolution strategy | ❌ No |

In all cases of divergence between `ddr_system_v4.0.yaml` and
`DDR System(Opus_v4).mdd`, the YAML governs. Do not modify
`DDR System(Opus_v4).md` for any reason.

---

## Modification Scope — ISSUE-008

Edits are restricted to **exactly three sections** of `ddr_system_v4.0.yaml`.
Do NOT modify any content outside these sections.

1. `express_mode.unbundle_determinism_rule` — extend with annotation coverage
   threshold and post-rejection node status clause.

2. `operations.core_operations` — update the existing `UNBUNDLE` entry's
   `validation_trigger`; insert a new `UNBUNDLE_SCAN` operation entry
   immediately before it.

3. The `unbundle()` pseudocode stub tagged `[SAL-5.1]` — replace with two
   stubs: `unbundle_scan()` (read-only pre-flight) and `unbundle_execute()`
   (atomic commit phase).

If a proposed change falls outside these three sections, do NOT apply it.
Report the out-of-scope change and await instruction.

---

## DDR Invariants — Must Not Be Violated

The following invariants must be preserved across every edit. If any change
would violate an invariant, halt and report the conflict before applying it.

- **AX-3 (Determinism):** Every operation entry in `core_operations` must
  specify both a success path and a failure path in its `validation_trigger`.
  Failure path must include: rejection payload format, atomicity guarantee,
  and post-failure node status. This is the core deficiency ISSUE-008 corrects.

- **AX-7 (DAG Acyclicity):** No edit may alter `parent_ids` wiring rules in
  a way that could introduce cycles into the node dependency graph.

- **CIT-R2 (Tier Adjacency):** `parent_ids` must reference only nodes in the
  immediately superior tier. No edit may relax or redefine this constraint.

- **INV-1 / INV-2:** No edit may introduce orphan nodes or broken parent
  chains.

---

## ISSUE-008 Resolution — Enforced Constraints

The endorsed strategy is **Option A: Two-Phase UNBUNDLE with Structured
Pre-Flight Scan and Atomic Execution**. No other strategy may be implemented.

### What Option A requires

- Two operation semantics must be specified:
  - `UNBUNDLE_SCAN`: read-only, independently invokable, no DAG state changes.
    Traverses all content fragments in the target Express Mode group and emits
    a per-fragment diagnostic for each, covering: fragment identity, detected
    tier annotation, allocation confidence, and ambiguity reason where
    confidence is not high. Confidence levels are: `high`, `ambiguous`, `none`.
  - `UNBUNDLE_EXECUTE`: atomic commit phase. Proceeds only when all fragments
    reach `high` confidence. On rejection: no structural mutations are applied;
    the Express Mode group node retains its pre-attempt status; the rejection
    payload is the complete `UNBUNDLE_SCAN` result.

- The existing inline `[TIER]` annotation convention must remain the allocation
  mechanism. No new mandatory authoring requirement may be added to existing
  Express Mode group node content.

- All existing Express Mode G1 and G2 group nodes using inline `[TIER]`
  annotations must remain fully processable without any migration step.

### What Option A prohibits

- **Do not implement Option B.** Do not introduce an `EXPRESS_ALLOCATION` front
  matter block, an `EXPR-R1` rule, or any equivalent mandatory pre-authoring
  structure requirement.

- Do not introduce new mandatory content-level requirements on any existing
  Express Mode group node.

- Do not increase the number of edge types or tier definitions.

---

## General Editing Rules

- Do not reformat, reorder, or rewrite YAML sections outside the modification
  scope, even if style improvements appear warranted.
- Do not change any node IDs, tier identifiers, axiom statements, or citation
  rules.
- Do not alter any `core_operations` entry other than `UNBUNDLE` (update only)
  and `UNBUNDLE_SCAN` (new insertion). All other operations are read-only.
- Preserve existing YAML scalar styles (`>` block scalars) and indentation
  conventions consistent with adjacent entries.
- Produce minimal diffs — change only what ISSUE-008 requires.

---

## Git Workflow

- Branch: `issue-008-unbundle-failure-semantics`
- All changes must be committed to this branch only. Do not commit to `main`.
- Commit message prefix: `[ISSUE-008]`
- Preserve per-phase commit history. Do not squash intermediate commits.
