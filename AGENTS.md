# DDR System — Codex Agent Constraints

## Project Identity

- Primary specification target: `ddr_system_v4.0.yaml`
- Reference document: `DDR System(Opus_v4).md`
- Active issue: `DDR_v4_Issue-005.md`

## Inviolable DDR Structural Constraints

The following rules govern ALL modifications to `ddr_system_v4.0.yaml`.
Violation of any constraint below is a CRITICAL ERROR.

1. **No rule ID mutation.** Existing rule IDs (GPCL-R1 through GPCL-R10, FCL-R1
   through FCL-R6, SAL-R1 through SAL-R6, etc.) must NOT be modified, renamed,
   renumbered, or have their `statement` fields altered in any way.

2. **No tier topology changes.** The derivation chain GPCL → FCL → SAL is
   invariant (§3.5 INV-2). No modification may introduce a direct GPCL → SAL
   citation path. No new `dag_invariants` entries may be added.

3. **Additive-only modification profile.** ISSUE-005 Option A is strictly
   additive. The ONLY permitted changes to the file are:
   a) Insertion of rule `GPCL-FCL-BR1` into GPCL tier `atomic_inclusion_rules`
   b) Update of `FCL-R6` statement to reference `GPCL-FCL-BR1`
   c) Addition of a `verify_citation_logic` block to the FCL tier
   d) Addition of a `MISSING_MEDIATOR` item type to the reconciliation manifest

4. **No schema field additions.** Do NOT add new properties to `node_schema_fields`
   or `edge_type_definitions`.

5. **Preserve all existing node content.** `ddr_system_v4.0.yaml` contains DAG
   nodes (e.g., GPCL-2.1, FCL-3.1, SAL-5.1). Their `content`, `parent_ids`,
   `status`, and `version` fields must not be altered.

6. **YAML validity.** All edits must produce valid YAML. Indentation must
   conform to the existing file's 2-space standard.

## Validation Protocol

After each modification step, run:
  python -c "import yaml; yaml.safe_load(open('ddr_system_v4.0.yaml'))"
to confirm YAML structural integrity before proceeding.
