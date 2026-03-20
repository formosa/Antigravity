# DDR System — Codex Agent Configuration

## Project Overview

This repository contains the DDR System Specification v4.0. The primary
specification file is `ddr_system_v4.0.yaml`. The canonical reference is
`DDR_System_Opus_v4.md`. Issue reports are in `.agent/assets/proposals/active/`.

## Invariants — Codex MUST enforce these at all times

- AX-3: All SUPERSEDE operations must produce unambiguous, mechanically
  verifiable outcomes with no implementation-dependent intermediate states.
- INV-6 (generalized): SUPERSEDE of ANY node (not only XPD) must be atomic
  across all three steps: (1) status transition, (2) replacement INSERT,
  (3) child re-wiring. Partial application is a structural violation.
- CIT-R1: All non-root nodes must have at least one valid, non-superseded parent_id.
- CIT-R2: Parent_ids must respect tier adjacency rules.
- AX-7: The DAG must remain acyclic at all times. No modification may introduce a cycle.
- Status enum changes must be backward-compatible: existing five-value YAML
  files must remain valid after any enum extension.

## Programmatic Checks — Run AFTER every modification

1. `python .agent/scripts/validate_yaml_schema.py ddr_system_v4.0.yaml`
2. `python .agent/scripts/check_dag_acyclicity.py ddr_system_v4.0.yaml`
3. `python .agent/scripts/check_lifecycle_completeness.py ddr_system_v4.0.yaml`
4. `python .agent/scripts/check_backward_compat.py ddr_system_v4.0.yaml`

## Output Format

- All YAML modifications must be presented as unified diffs.
- Each diff must include a `# ISSUE-007 Change` header comment citing the
  specific section modified and the rule it satisfies.
- Do NOT modify any section not listed in the active issue report.
