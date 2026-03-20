# DDR System — Codex Agent Standing Constraints

## MANDATORY PRE-EXECUTION READING

Before modifying any file in this repository, read and internalize the
following invariants. Do not proceed if any constraint cannot be satisfied.

## DDR Invariants (Non-Negotiable)

- AX-7 / INV-1: No cycles may exist in any citation path at any path length.
- INV-2: No tier-skipping. All parent_ids must reference the immediately
  preceding active tier.
- INV-5: All non-root nodes must carry at least one parent_id citation.
- CIT-R2: parent_ids must reference the immediately preceding active tier(s).
- AX-3 (amended by ISSUE-004): Determinism applies to structural rules only.
  Semantic rules emit REVIEW_REQUIRED, not pass/fail.
- AX-6: Core is strictly declarative. No inference logic may be embedded in
  Core definitions.

## Semantic Rule Ground Truth (ISSUE-004, Option A)

The following five atomic inclusion rules are classified as `semantic` and
MUST receive `verification_mode: semantic` in all YAML mutations:

- XPD-R3
- FCL-R1
- FCL-R2
- GPCL-R2
- SAL-R1
All other atomic inclusion rules receive `verification_mode: structural`.

## Modification Policy

- Do NOT modify node_ids, tier definitions, edge_type_definitions, or
  parent_ids during ISSUE-004 resolution. All changes are additive only.
- Do NOT introduce new edge types or Extensions.
- Do NOT break JSON Schema 2020-12 compliance (validate after every change).
- All changes must target: ddr_system_v4.0.yaml ONLY.
