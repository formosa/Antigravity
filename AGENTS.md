# DDR System — Codex Agent Constraints

## Framework Identity

- PRIMARY TARGET: `ddr_system_v4_0.yaml`
- REFERENCE SPEC: `DDR_System_Opus_v4_.md`
- SPECIFICATION VERSION: DDR System v4.0

## Immutable Structural Invariants (NEVER violate)

- §3.5 DAG Invariant: No tier-skipping. Every citation must reference
  exactly one active tier above in the derivation chain.
- AX-7: The DAG must remain acyclic. Do not introduce cycles.
- AX-3: All outputs must be mechanically verifiable. No ambiguous
  or probabilistic structures.
- INV-1: Every non-root node must have at least one parent_id.
- INV-2: SAL is the only permitted merge-node exception (exhaustive).
  Do not introduce additional merge-node exceptions.
- Tier derivation chain: XPD → SIL → GPCL → FCL → [CL →] SAL

## Modification Policy

- ADDITIVE CHANGES ONLY unless the Issue Report explicitly authorizes
  modification of existing rule IDs, tier definitions, or schema fields.
- Do NOT reassign existing rule_id values.
- Do NOT change node IDs, tier_ids, or edge_type definitions.
- Do NOT introduce new edge types.
- Preserve all existing content unless the Issue Report requires removal.

## Validation Requirements (run after EVERY modification)

- Confirm DAG acyclicity (AX-7) is preserved.
- Confirm tier adjacency (CIT-R2) is satisfied for all parent_ids.
- Confirm no existing rule_id has been removed or reassigned.
- Confirm the GPCL→FCL→SAL derivation path remains uniform.
- Confirm no new topology exceptions (beyond INV-2) have been introduced.

## Output Format

- All YAML diffs must be minimal — change only what the Issue Report requires.
- PR commit messages must follow the format:
  "[ISSUE-XXX Resolution]: <brief description>"
