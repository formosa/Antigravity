---
task: "Resolve DDR System v7.0 concerns A-D by updating the authority pair, aligning affected system-definition conformance fixtures, and revalidating the governed release package without changing the corpus case count or expected pass/fail outcomes."
model: "gemini-3-pro-preview"
version: "6.0.2"
output_path: ".agent/plans/20260413-235035-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260413-235035-IMPLEMENTATION_PLAN.md"
---

<objective>
Resolve the four live DDR System v7.0 defects labeled A-D by hardening the authority schema and system artifacts, propagating the approved fixes to the affected conformance system-definition fixtures, and re-running the owned release boundary so the package remains release-valid with 10 corpus cases.
</objective>

<phases>
- phase_id: "PHASE_1_AUTHORITY_PAIR_HARDENING"
  objectives:
    - "Resolve live concerns A-D in the normative schema and system authority artifacts."
    - "Hold schema and scaffold changes behind an explicit review boundary before downstream propagation."
  task_references: ["Concern A", "Concern B", "Concern C", "Concern D"]
  entry_criteria:
    - "Workspace review confirms concern 10 is already closed by the existing `ddr/conformance/v7.0/` corpus and concern 11 is already closed by the owned validator plus `test_validate_ddr_release.py` coverage."
    - "No additional DDR v7.0 scope is introduced beyond files that currently carry concerns A-D."
  exit_criteria:
    - "`ddr/ddr_node_schema_v7.0.yaml` explicitly reserves `CL` in `ExtensionRuleId`."
    - "`ddr/ddr_system_v7.0.yaml` resolves the validation-note prose defect and hardens the CDL-7.1 scaffold with an ergonomic `detected_annotation` default plus explicit pickle-safe `UnbundleRejectionError` reconstruction semantics."
    - "Human review approves the authority-pair contract edits before any conformance-fixture propagation begins."
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_2_RELEASE_ALIGNMENT_AND_VALIDATION"
  objectives:
    - "Propagate the approved authority edits to the affected system-definition corpus fixtures without changing each case's intentional validity state."
    - "Refresh governed release surfaces and re-run the owned DDR v7.0 release gate."
  task_references: ["Concern B", "Concern C", "Concern D"]
  entry_criteria:
    - "PHASE_1_AUTHORITY_PAIR_HARDENING exit criteria are met."
    - "Human review gate on the schema and authority-file edits is complete."
  exit_criteria:
    - "Affected conformance system-definition fixtures match the approved authority wording for concerns B-D while preserving each fixture's expected pass/fail reason."
    - "Governed markdown release surfaces are regenerated from the updated YAML authority pair."
    - "`.venv/Scripts/python.exe .agent/scripts/validate_ddr_release.py` passes and still reports 10 validated corpus cases."
  assigned_model: "gemini-3-flash-preview"
</phases>

<atomic_steps>

#### Group 1 - Authority Schema and System Corrections (PHASE_1_AUTHORITY_PAIR_HARDENING)

- [X] 1. Intent: make the closed Core-tier exclusion explicit in the extension rule-ID contract. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `ExtensionRuleId` adds `CL` to the negative-lookahead reserved-prefix set without changing any other rule-ID semantics. Outcome: the schema self-documents the full forbidden Core vocabulary while remaining behaviorally stable for existing valid and invalid inputs.
- [X] 2. Intent: remove the remaining normative prose defect in the custom ARE profile contract. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `custom.validation_note` so it states profile-reference resolution, score-band ordering, non-overlap checks, and per-band `[0.0, 1.0]` bound enforcement in one grammatically correct sentence. Outcome: the authority prose matches the validator's runtime responsibilities without duplicated conjunctions or ambiguous wording.
- [X] 3. Intent: harden the CDL-7.1/SAL-5.1 Express-mode scaffold without degrading current raise/except ergonomics. Action: MODIFY `ddr/ddr_system_v7.0.yaml` so `FragmentDiagnostic.detected_annotation` defaults to `None`, `UnbundleRejectionError` declares an explicit pickle-safe reconstruction path that preserves the structured `scan_result` payload, and the `unbundle_execute` docstring states the resulting contract. Outcome: the scaffold becomes ergonomic for no-annotation cases and defensible for cross-process error transport.

#### Group 2 - Conformance Fixture Alignment (PHASE_2_RELEASE_ALIGNMENT_AND_VALIDATION)

- [X] 4. Intent: keep conformance fixtures aligned to the approved ARE prose contract without repairing their intentional invalid mutations. Action: MODIFY `ddr/conformance/v7.0/valid/system_definition.yaml`, `ddr/conformance/v7.0/valid/system_definition_custom_profile.yaml`, `ddr/conformance/v7.0/invalid/system_definition_invalid_bridge_rule.yaml`, `ddr/conformance/v7.0/invalid/system_definition_invalid_mixed_rollback_transition.yaml`, `ddr/conformance/v7.0/invalid/system_definition_invalid_overlapping_score_bands.yaml`, and `ddr/conformance/v7.0/invalid/system_definition_missing_authority.yaml` so each mirrored `validation_note` matches the updated authority wording only. Outcome: the corpus reflects the corrected normative prose while preserving each case's intended validity classification.
- [X] 5. Intent: keep the mirrored CDL-7.1/SAL-5.1 scaffold synchronized across release-fixture surfaces. Action: MODIFY the five conformance system-definition fixtures that carry the scaffold block so the `FragmentDiagnostic` default, `UnbundleRejectionError` reconstruction behavior, and `unbundle_execute` contract text match the approved authority-file changes only. Outcome: the corpus mirrors the corrected runtime scaffold semantics without changing the deliberate invalid trigger in any negative case.

#### Group 3 - Generated Surface Refresh and Release Validation (PHASE_2_RELEASE_ALIGNMENT_AND_VALIDATION)

- [X] 6. Intent: keep governed markdown outputs current with the updated YAML authority pair. Action: EXECUTE `.venv/Scripts/python.exe .agent/scripts/generate_ddr_release_docs.py`. Outcome: `ddr/DDR System(v7.0).md` and `ddr/ddr_ref_manual_v7.0.md` are refreshed under the owned provenance contract after the authority edits land.
- [X] 7. Intent: prove the release package still satisfies its owned stop/go boundary after concerns A-D are resolved. Action: EXECUTE `.venv/Scripts/python.exe .agent/scripts/validate_ddr_release.py`. Outcome: the authority pair, generated markdown provenance, and all 10 conformance corpus cases validate successfully with unchanged expected pass/fail behavior.

</atomic_steps>

<verification>

1. Inspect `ddr/ddr_node_schema_v7.0.yaml` and confirm the `ExtensionRuleId` pattern explicitly includes `CL` in the reserved-prefix lookahead while the surrounding rule-ID definitions remain unchanged.
2. Inspect `ddr/ddr_system_v7.0.yaml` and confirm `custom.validation_note` is grammatically clean and explicitly names profile-reference resolution, score-band ordering, non-overlap checks, and per-band `[0.0, 1.0]` bound checks.
3. Inspect `ddr/ddr_system_v7.0.yaml` and confirm `FragmentDiagnostic.detected_annotation` defaults to `None`, `UnbundleRejectionError` exposes an explicit pickle-safe reconstruction path that retains both `message` and `scan_result`, and the `unbundle_execute` docstring reflects that contract.
4. Inspect the six listed conformance system-definition fixtures and confirm each `validation_note` block matches the updated authority wording while the fixture-specific invalid mutation remains intact.
5. Inspect the five conformance fixtures that carry the scaffold block and confirm the CDL-7.1/SAL-5.1 scaffold text matches the updated authority file for the `detected_annotation` default, exception reconstruction behavior, and `unbundle_execute` wording.
6. Run `.venv/Scripts/python.exe .agent/scripts/generate_ddr_release_docs.py` and confirm it completes without error while rewriting `ddr/DDR System(v7.0).md` and `ddr/ddr_ref_manual_v7.0.md`.
7. Run `.venv/Scripts/python.exe .agent/scripts/validate_ddr_release.py` and confirm it reports authority-pair validation, markdown provenance verification, and `10` validated corpus cases.

</verification>

<risks_and_mitigations>

- **Risk:** `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml` are normative release-authority surfaces, so even low-churn edits carry contract risk. **Mitigation:** keep PHASE_1 limited to the exact concern lines, require explicit human review before PHASE_2, and avoid any unrelated schema or readiness-gate changes.
- **Risk:** fixing `UnbundleRejectionError` by changing `Exception.args` semantics could degrade current human-readable exception behavior while solving pickling. **Mitigation:** prefer an explicit reconstruction method such as `__reduce__` or `__reduce_ex__` that preserves the structured `scan_result` payload without broadening user-facing exception-string behavior.
- **Risk:** conformance invalid fixtures could be accidentally repaired while syncing shared text from the authority artifact. **Mitigation:** patch only the mirrored prose/scaffold lines listed in steps 4 and 5, leave each fixture's intentional invalid trigger untouched, and treat the release validator's expected pass/fail outcomes as the stop/go boundary before completion.

</risks_and_mitigations>
