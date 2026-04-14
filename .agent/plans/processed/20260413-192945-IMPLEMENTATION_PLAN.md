---
task: "Resolve the currently valid DDR System v7.0 schema, scaffold, and release-validation concerns by aligning the YAML authority pair, hardening runtime validation, and expanding the conformance proof set."
model: "gemini-3-pro-preview"
version: 6.0.2
output_path: ".agent/plans/20260413-192945-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260413-192945-IMPLEMENTATION_PLAN.md"
status: "completed"
completed_at: "2026-04-13"
---

<objective>
Correct the still-valid DDR System v7.0 defects and gaps identified in concerns 1, 2, 3, 4, 5, 6, 7, and 9 while leaving already-resolved concerns 10 and 11 untouched and keeping concern 8 out of scope unless new local evidence proves it defective.
</objective>

<phases>
- phase_id: "PHASE_1_SCHEMA_AND_AUTHORITY_ALIGNMENT"
  status: "completed"
  outcome: "Schema and semantic authority were aligned on scoring-profile shape, rollback exclusivity, bridge-rule typing, and unbundle interface declarations."

- phase_id: "PHASE_2_VALIDATOR_AND_CORPUS_ENFORCEMENT"
  status: "completed"
  outcome: "Runtime ARE score-band checks were added to the owned release validator and exercised through regression tests plus expanded conformance fixtures."

- phase_id: "PHASE_3_RELEASE_SURFACES_AND_FINAL_GATE"
  status: "completed"
  outcome: "Derived markdown surfaces were regenerated and the owned validator passed against the corrected authority pair and expanded corpus."
</phases>

<atomic_steps>
- [x] 1. Modified `ddr/ddr_node_schema_v7.0.yaml` `$defs.ScoringProfile` to admit `profile_id` while preserving `additionalProperties: false`.
- [x] 2. Modified `ddr/ddr_node_schema_v7.0.yaml` `$defs.StatusTransition.allOf` so rollback entries forbid `to` and non-rollback entries forbid `to_node_field`.
- [x] 3. Modified `ddr/ddr_node_schema_v7.0.yaml` `$defs.BridgeRuleId` to enumerate canonical DDR tier identifiers.
- [x] 4. Added schema `$comment` guidance for `ScoringProfile.score_bands`, fixed G2 `[FCL, CL]` behavior, and `GuardIdRef` dual-update requirements.
- [x] 5. Modified `ddr/ddr_system_v7.0.yaml` `are_scoring_profiles.custom` and ARE conformance wording to include `profile_id` and bind runtime band checks to `.agent/scripts/validate_ddr_release.py`.
- [x] 6. Modified `ddr/ddr_system_v7.0.yaml` `CDL-7.1` to declare `FragmentDiagnostic`, `UnbundleScanResult`, and `UnbundleRejectionError`.
- [x] 7. Modified `ddr/ddr_system_v7.0.yaml` `ISL-8.1` to reorder `ParentCitation`, import `Literal`, and add scaffold definitions for unbundle result/error types.
- [x] 8. Modified `.agent/scripts/validate_ddr_release.py` to enforce ordered, non-overlapping, bounded ARE score bands during authority validation and corpus validation.
- [x] 9. Modified `.agent/scripts/tests/test_validate_ddr_release.py` to cover overlapping score bands, mixed rollback transition fields, and self-validation-first sequencing.
- [x] 10. Modified `ddr/conformance/v7.0/manifest.yaml` and fixtures to add a valid custom-profile case, invalid mixed rollback transition case, invalid bridge-rule case, invalid overlapping score-band case, and a refreshed valid system-definition fixture.
- [x] 11. Executed `python .agent/scripts/generate_ddr_release_docs.py`.
- [x] 12. Executed `pytest .agent/scripts/tests/test_validate_ddr_release.py -q` and `python .agent/scripts/validate_ddr_release.py`.
</atomic_steps>

<verification_results>
1. `pytest .agent/scripts/tests/test_validate_ddr_release.py -q` passed with `7 passed`.
2. `python .agent/scripts/generate_ddr_release_docs.py` regenerated `ddr/DDR System(v7.0).md` and `ddr/ddr_ref_manual_v7.0.md`.
3. `python .agent/scripts/validate_ddr_release.py` passed with authority-pair validation, markdown provenance validation, and `10` conformance corpus cases succeeding as expected.
</verification_results>

<deliverables>
- `ddr/ddr_node_schema_v7.0.yaml`
- `ddr/ddr_system_v7.0.yaml`
- `.agent/scripts/validate_ddr_release.py`
- `.agent/scripts/tests/test_validate_ddr_release.py`
- `ddr/conformance/v7.0/manifest.yaml`
- `ddr/conformance/v7.0/valid/system_definition.yaml`
- `ddr/conformance/v7.0/valid/system_definition_custom_profile.yaml`
- `ddr/conformance/v7.0/invalid/system_definition_invalid_bridge_rule.yaml`
- `ddr/conformance/v7.0/invalid/system_definition_invalid_mixed_rollback_transition.yaml`
- `ddr/conformance/v7.0/invalid/system_definition_invalid_overlapping_score_bands.yaml`
- `ddr/DDR System(v7.0).md`
- `ddr/ddr_ref_manual_v7.0.md`
</deliverables>
