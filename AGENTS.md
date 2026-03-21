# AGENTS.md

# DDR System v4.0 — Codex Agent Contract

# Scope: ISSUE-012 Resolution Only

## Project Files

- Primary target : `.agent/assets/proposals/active/ddr_system_v4.0.yaml`
- Reference spec : `.agent/assets/proposals/active/DDR System(Opus_v4).md`
- Issue report   : `.agent/assets/proposals/active/DDR_v4_Issue-012.md`

## Resolution Directive

Implement Option C from `DDR_v4_Issue-012.md` exactly as endorsed in §3.
Do not implement Option A or Option B. Do not blend strategies.

## Immutable Constraints

Any edit violating the following rules MUST be rejected and reversed before proceeding.

1. Do not modify any key outside `extension_system.candidate_pool`
   and `extension_catalog.E5.rules`.
2. Do not alter `extension_system.integration_rules` entries EXT-R1 through EXT-R7.
3. Do not alter `extension_catalog` entries E1, E2, E3, E4, E6,
   or any entry beyond E5.
4. Do not modify `are_scoring_profiles`, `axioms`, `tier_definitions`,
   `atomic_rules`, `operations`, `lifecycle_model`, `dirty_propagation`,
   or `reconciliation_manifest`.
5. Do not add, rename, or remove any top-level YAML key.
6. Do not modify `extension_catalog.E5.rules` entries ARE-R1 through ARE-R5.
7. Do not introduce any mechanism by which ARE state transitions affect
   Core CLEAN/DIRTY status. EXT-R5 must hold unconditionally across all
   ARE activation state transitions.
8. The canonical checkpoint path is `.agent/state/are_candidate_pool.checkpoint.yaml`.
   Do not substitute an alternative path.

## Permitted Modification Scope

Exactly the following keys may be changed — no others.

- `extension_system.candidate_pool.visibility_rule`  — update value
- `extension_system.candidate_pool.activation_states` — add (new key)
- `extension_system.candidate_pool.checkpoint_path`  — add (new key)
- `extension_system.candidate_pool.discard_trigger`  — update value
- `extension_catalog.E5.rules`                       — append ARE-R6 and ARE-R7 only

## Validation Command

Run after every YAML edit. The command MUST exit 0 with no output before
any changes are staged or committed.

```bash
python -c "import yaml; yaml.safe_load(open('.agent/assets/proposals/active/ddr_system_v4.0.yaml'))"
```

## Pre-Commit Verification Checklist

Confirm each item manually before generating the commit.

- [ ] `extension_system.candidate_pool` contains exactly 8 top-level keys,
      in this order: `description`, `candidate_status_value`, `visibility_rule`,
      `activation_states`, `checkpoint_path`, `effect_on_core_status`,
      `promotion_mechanism`, `discard_trigger`.
- [ ] `extension_catalog.E5.rules` contains exactly 7 entries,
      in order: ARE-R1, ARE-R2, ARE-R3, ARE-R4, ARE-R5, ARE-R6, ARE-R7.
- [ ] Git diff touches only `extension_system.candidate_pool`
      and `extension_catalog.E5`.
- [ ] No top-level key count change relative to the original file.

## YAML Style

- Multi-line scalars: `>` folded style only, consistent with existing spec formatting.
- Rule statements: present-tense normative prose (e.g., "ARE MUST...").
- New rule IDs: ARE-Rn namespace, incrementing from the highest existing index (ARE-R5).

## PR Format

Title:
  fix(ddr-spec): ISSUE-012 — Introduce tri-state ARE lifecycle with mandatory checkpoint (Option C)

Body must include:

- Problem statement (binary lifecycle, data-loss transition)
- Option C justification and comparative rationale over Options A and B
- DDR invariant verification results (EXT-R5, AX-6, ARE-R1, ARE-R3)
- Enumerated list of modified YAML keys
