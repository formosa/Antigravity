# DDR v6.1 Implementation Plan

**Date:** 2026-03-27  
**Driver:** `.agent\assets\proposals\active\AGENTS.md`  
**Primary targets:** `.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml`, `.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml`

## Objective

Validate DDR System v6.1 against the inherited v4/v5 issue history plus the active
v6 audit notes, resolve any remaining gaps in the targeted YAML artifacts, and
leave a traceable task record with final status for each identified issue of
concern.

## Status Key

- `VERIFIED_FORWARD`: previously resolved issue confirmed to be correctly carried
  forward into v6.1.
- `COMPLETED`: v6.1 required direct edits in the targeted YAML artifacts and the
  repair has been applied.

## Task List

### Carryforward Verification — v4 Tracker

- [x] `VERIFIED_FORWARD` — v4 ISSUE-001: `derives` Absorbs `cites`, Destroying Audit Trail Precision
- [x] `VERIFIED_FORWARD` — v4 ISSUE-002: FCL→CL Edge Direction Is Semantically Inverted
- [x] `VERIFIED_FORWARD` — v4 ISSUE-003: DAG Invariant Text Contradicts the Merge-Node Topology
- [x] `VERIFIED_FORWARD` — v4 ISSUE-004: AX-3 Determinism Is Violated by Non-Automatable Atomic Rules
- [x] `VERIFIED_FORWARD` — v4 ISSUE-005: GPCL Overloading Creates an Implicit FCL Tier Skip
- [x] `VERIFIED_FORWARD` — v4 ISSUE-006: Node Status Lifecycle Lacks a Formal State Machine
- [x] `VERIFIED_FORWARD` — v4 ISSUE-007: SUPERSEDE Atomicity and Rollback Are Underspecified
- [x] `VERIFIED_FORWARD` — v4 ISSUE-008: UNBUNDLE Rejection Behaviour Is Underspecified
- [x] `VERIFIED_FORWARD` — v4 ISSUE-009: ARE Confidence Score Has No Normative Rubric
- [x] `VERIFIED_FORWARD` — v4 ISSUE-010: `extension_annotations` Namespace Enforcement Is Absent at Schema Level
- [x] `VERIFIED_FORWARD` — v4 ISSUE-011: ORL-R7 Migration Is Unresolved in a "Finalized" Specification
- [x] `VERIFIED_FORWARD` — v4 ISSUE-012: Candidate Pool Has No Pause State
- [x] `VERIFIED_FORWARD` — v4 ISSUE-013: DDE Upward FCL Annotation Creates a Backwards Validation Dependency

### Carryforward Verification — v5 Tracker

- [x] `VERIFIED_FORWARD` — v5 ISSUE-001: Schema Omits SUPERSEDE_PENDING from DdrNode Status Enum
- [x] `VERIFIED_FORWARD` — v5 ISSUE-002: Schema Missing `derivation_mode` Field on ParentCitation
- [x] `VERIFIED_FORWARD` — v5 ISSUE-003: CL `node_schema` Property Not Permitted by TierDefinition Schema
- [x] `VERIFIED_FORWARD` — v5 ISSUE-004: `lifecycle` Block Not Covered by ddr_node_schema
- [x] `VERIFIED_FORWARD` — v5 ISSUE-005: `are_scoring_profiles` Not Covered by ddr_node_schema
- [x] `VERIFIED_FORWARD` — v5 ISSUE-006: `errata_log` Not Covered by ddr_node_schema
- [x] `VERIFIED_FORWARD` — v5 ISSUE-007: `reconciliation_manifest_schema` Not Covered by ddr_node_schema
- [x] `VERIFIED_FORWARD` — v5 ISSUE-008: `verify_citation_logic` Not Permitted by TierDefinition Schema
- [x] `VERIFIED_FORWARD` — v5 ISSUE-009: `errata_log` References v4 Versions in a v5 Specification
- [x] `VERIFIED_FORWARD` — v5 ISSUE-010: AtomicInclusionRule Schema Missing `verification_mode` and `applies_when` Fields
- [x] `VERIFIED_FORWARD` — v5 ISSUE-011: ExtensionEntry Schema Missing `scoring_profile` Property
- [x] `VERIFIED_FORWARD` — v5 ISSUE-012: `candidate_pool` Schema Missing `activation_states` and `checkpoint_path`

### v6.1 Remediation Tasks

- [x] `COMPLETED` — PATCH-1: GPCL ↔ FCL Mediation Gap Formalization
  Applied `semantic_gap_classification`, added `INV-7`, and required rationale-bearing `MISSING_MEDIATOR` manifest fields.
- [x] `COMPLETED` — PATCH-2: Physical Constraint Dual Authority Formalization
  Added `constraint_classes` and `physical_constraint_rule` to formalize non-silent escalation of imposed constraints.
- [x] `COMPLETED` — PATCH-3: Dirty Propagation Model Unification
  Added `dirty_classification` and `supersede_dirty_behavior` to distinguish structural versus semantic DIRTY conditions.
- [x] `COMPLETED` — PATCH-4: Cross-Node Semantic Validation Gap
  Extended `VERIFY` semantics and added `semantic_consistency_rules` as a non-blocking review hook.
- [x] `COMPLETED` — PATCH-5: UNBUNDLE Usability Stabilization
  Added deterministic deferred-fragment handling via explicit `[DEFER]` annotation semantics.
- [x] `COMPLETED` — PATCH-6: Extension Philosophy Consistency
  Refined AX-5 wording to match the existing explicit, non-mutating Extension interface model.
- [x] `COMPLETED` — PATCH-7: Conflict Resolution Process Definition
  Added `conflict_resolution_protocol` with auditable escalation and disposition steps.
- [x] `COMPLETED` — PATCH-8: Lifecycle Completeness Safeguard
  Added `INV-8` to require a complete, closed lifecycle state machine.
- [x] `COMPLETED` — PATCH-9: Version Consistency Rule
  Added `CIT-R7` to formalize child re-validation after cited parent version changes.

### Version Alignment

- [x] `COMPLETED` — Promoted the active system artifact from internally mislabeled v6.0 content to explicit v6.1 metadata.
- [x] `COMPLETED` — Updated the schema identity and `ddr_version` lock from `6.0` to `6.1`.
- [x] `COMPLETED` — Added a v6.1 version-history entry and refreshed the targeted ICL versioning note.

## Direct Edit Summary

- Updated `.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` to express true
  v6.1 metadata, carry the missing v6 audit refinements, and preserve alignment
  with inherited v4/v5 fixes.
- Updated `.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` so the new
  v6.1 structures are schema-representable and the definition remains
  self-validating.
- Limited direct repairs to the YAML artifacts named by the task brief. The
  companion Markdown document was reviewed for context but not synchronized as
  part of this pass.

## Verification

- [x] Parsed both YAML files successfully with `.venv\Scripts\python.exe` and `yaml`.
- [x] Validated `ddr_system_v6.1.yaml` against `ddr_node_schema.yaml` with `jsonschema_rs`.
- [x] Confirmed the updated system file now validates successfully (`VALID`).

## Remaining Follow-Up

- No unresolved issues were identified inside the targeted YAML surfaces after
  the v6.1 repair pass.
- If the human-readable `DDR System(v6).md` document must remain textually in
  lockstep with the authoritative YAML, a separate Markdown synchronization pass
  should be scheduled.
