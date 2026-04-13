---
task: "Produce a review-gated DDR System v7.0 release package centered on a self-validating YAML authority pair, governed release tooling, generated derivative surfaces, and profile-driven production contracts while preserving the frozen v6.x core topology."
model: "gemini-3-pro-preview"
version: "6.0.3"
output_path: ".agent/plans/20260413-054500-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260413-054500-IMPLEMENTATION_PLAN.md"
---

<objective>
Produce DDR System v7.0 as a self-validating authority pair (`ddr/ddr_node_schema_v7.0.yaml`, `ddr/ddr_system_v7.0.yaml`) plus governed release tooling, conformance assets, and generated release surfaces that resolve source-visible v6.3 gaps before profile-gated scope expansion. If local repo evidence is missing or conflicts with `ddr/ddr_node_schema_v6.3.yaml` or `ddr/ddr_system_v6.3.yaml`, halt for review instead of inferring.
</objective>

<phases>
- phase_id: "PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS"
  objectives:
    - "Create isolated v7.0 copies of the YAML SSOT pair."
    - "Close source-visible v6.3 blockers with local evidence only."
    - "Keep rejected review prescriptions out of scope."
  task_references: ["source-visible-gap-closure", "release-blocking-defects"]
  entry_criteria:
    - "The v6.3 YAML SSOT pair is readable."
    - "review.gemini.md, review.codex.md, and review.opus.md have been synthesized against the YAML pair."
  exit_criteria:
    - "The v7.0 YAML pair self-validates after blocker edits."
    - "DELETE semantics and rule-family separation are reviewed before PHASE_2."
    - "No change demotes Full mode, removes semantic review, or de-normativizes ARE against the v6.3 SSOT."
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_2_AUTHORITY_AND_GENERATION_GOVERNANCE"
  objectives:
    - "Declare the YAML pair as the v7.0 normative authority."
    - "Encode generated-surface ownership and governance controls."
    - "Lock complexity-budget, errata, and deprecation rules before expansion."
  task_references: ["authority-hardening", "generated-surfaces"]
  entry_criteria:
    - "PHASE_1 exit criteria are satisfied."
  exit_criteria:
    - "Authority hierarchy and generated-surface precedence are encoded in the v7.0 pair."
    - "Governance additions validate without reopening core-topology drift."
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_3_PROFILE_RUNTIME_AND_CONFORMANCE_FOUNDATION"
  objectives:
    - "Add distinct profile axes for shape, maturity, and assurance."
    - "Make runtime and operation behavior machine-shaped."
    - "Define conformance, migration, and release-tool ownership before bulk expansion."
  task_references: ["profile-model", "runtime-contract", "conformance"]
  entry_criteria:
    - "PHASE_2 exit criteria are satisfied."
  exit_criteria:
    - "Profiles, runtime contracts, validation-ledger semantics, and release-tool contracts validate in the v7.0 pair."
    - "Profile-axis and readiness-gate decisions are reviewed before PHASE_4."
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_4_PROFILE_GATED_PRODUCTION_CONTRACTS"
  objectives:
    - "Expand production obligations through profiles and existing extension surfaces."
    - "Cover security, deployment, resilience, observability, online, data, and supply-chain contracts."
    - "Bind target use cases to explicit minimum obligations."
  task_references: ["production-contract-expansion"]
  entry_criteria:
    - "PHASE_3 exit criteria are satisfied."
  exit_criteria:
    - "Target use cases map to explicit tiers, extensions, evidence, and readiness gates through declared profile axes."
    - "No new core tiers, edge types, or operations are introduced unless an approved defect closure requires them."
  assigned_model: "gemini-3-flash-preview"

- phase_id: "PHASE_5_ADOPTION_AND_EXECUTABLE_RELEASE_SURFACES"
  objectives:
    - "Complete adoption surfaces and governed release tooling for v7.0."
    - "Stand up the owned generator and validator under existing `.agent/` conventions."
    - "Finish with tool-driven validation of the v7.0 release package."
  task_references: ["migration", "derived-release-surfaces", "release-tooling"]
  entry_criteria:
    - "PHASE_4 exit criteria are satisfied."
  exit_criteria:
    - "Governed release tooling exists under `.agent/` with current indexes and passing targeted tests."
    - "Generated v7.0 markdown surfaces and the conformance corpus exist with provenance headers."
    - "The v7.0 YAML pair and release corpus validate through the owned release tool."
  assigned_model: "gemini-3-flash-preview"
</phases>

<atomic_steps>
#### Group 1 - V7 Baseline Copies (PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS)

- [X] 1. Intent: isolate schema work. Action: CREATE `ddr/ddr_node_schema_v7.0.yaml` from `ddr/ddr_node_schema_v6.3.yaml` and change only root version identifiers. Outcome: later schema edits land on a new v7.0 file.
- [X] 2. Intent: isolate semantic-authority work. Action: CREATE `ddr/ddr_system_v7.0.yaml` from `ddr/ddr_system_v6.3.yaml` and change only root version metadata. Outcome: later authority edits land on a new v7.0 file.

#### Group 2 - Structural Admission and Metadata Closures (PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS)

- [X] 3. Intent: close the observed admission gaps. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `DdrNode.required` includes `content` and the per-node `SIL` conditional enforces `parent_ids.minItems: 1`. Outcome: hollow nodes and orphan `SIL` nodes fail validation.
- [X] 4. Intent: align semantic text with schema admission rules. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `node_schema_fields`, `ICL-6.1`, `CDL-7.1`, and scaffold text to require node `content` and non-root `SIL` parents. Outcome: semantic authority matches schema admission rules.
- [X] 5. Intent: reject incomplete authority metadata. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `system_metadata` requires essential authority fields and `TierDefinition.required` includes `parent_relationships` and `child_relationships`. Outcome: empty authority metadata and topology-less tier definitions fail validation.
- [X] 6. Intent: keep semantic authority self-hosting under stricter metadata rules. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `system_metadata`, tier-definition narrative, and scaffold text to require authority fields and explicit parent/child topology. Outcome: semantic authority remains consistent with step 5.
- [X] 7. Intent: remove `system_definition` profile ambiguity. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `system_definition` rejects `project.mode: express` and documents the allowed `project` contract. Outcome: `system_definition` profile branching is unambiguous.

#### Group 3 - Semantic-Authority Release Blockers (PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS)

- [X] 8. Intent: make the `project` block explicit in the authority. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to define `project` semantics for `document_profile: system_definition` and align profile/mode prose with step 7. Outcome: readers no longer infer the `project` contract.
- [X] 9. Intent: remove a historical metadata defect. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `version_history` so the v1.0 entry does not contain an empty `date`. Outcome: version history contains explicit values.
- [X] 10. Intent: remove transient audit residue from the normative file. Action: MODIFY `ddr/ddr_system_v7.0.yaml` inline comments to delete issue-tracker commentary or rewrite commentary as timeless explanation. Outcome: the normative file contains enduring semantics only.
- [X] 11. Intent: close deprecated-node lifecycle gaps. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `lifecycle.status_transitions` so `DEPRECATED -> ACTIVE` requires structural and review closure and `DEPRECATED -> DIRTY` exists as a propagation path. Outcome: deprecated nodes cannot bypass re-validation.
- [X] 12. Intent: make DELETE a defined contract. Action: MODIFY `ddr/ddr_system_v7.0.yaml` lifecycle and operation narratives to encode allowed DELETE source states, terminal behavior, child handling, manifest effects, and rollback notes. Outcome: DELETE is machine-auditable. Stop if: local evidence leaves DELETE behavior ambiguous or conflicts with the v6.3 SSOT.
- [X] 13. Intent: align the schema with the chosen DELETE contract. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` lifecycle and status definitions to admit only the DELETE model encoded in step 12. Outcome: schema and semantic authority agree on DELETE handling.
- [X] 14. Intent: make `CIT-R7` baseline-aware. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` `ParentCitation` to add `validated_parent_version` with write-on-validate semantics. Outcome: child freshness can be checked against persisted parent checkpoints.
- [X] 15. Intent: align semantic freshness rules with stored checkpoints. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `citation_rules`, validation prose, and scaffold text so `CIT-R7` relies on `validated_parent_version`. Outcome: parent freshness is described consistently.
- [X] 16. Intent: type the full reconciliation manifest. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` manifest definitions to admit `REVIEW_REQUIRED`, extension advisories, conflict-resolution records, override approvals, and deferred fragments. Outcome: the schema admits the full manifest item set.
- [X] 17. Intent: define the manifest taxonomy semantically. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `reconciliation_manifest_schema` and related text to define every manifest family admitted in step 16. Outcome: manifest state is semantically closed.
- [X] 18. Intent: separate core topology from extension-only semantics. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `TierRelationship.edge_type` excludes `extends` and extension rule-family typing stays distinct from core families. Outcome: core topology fields cannot carry extension-only semantics. Stop if: rule-family separation requires unreviewed changes to approved v6.3 semantics.
- [X] 19. Intent: state rule-family and edge invariants explicitly. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to declare global rule-family uniqueness and reserve `extends` for extension interaction instead of core tier relationships. Outcome: rule IDs and edge semantics resolve without hidden assumptions.

#### Review Gate - Approve DELETE and rule-family decisions before PHASE_2

#### Group 4 - Authority and Generated-Surface Governance (PHASE_2_AUTHORITY_AND_GENERATION_GOVERNANCE)

- [X] 20. Intent: declare the formal v7.0 authority model. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add `authority_hierarchy` for semantic authority, structural authority, and derived human-readable surfaces. Outcome: the YAML pair is the declared normative source.
- [X] 21. Intent: keep the schema aligned with `authority_hierarchy`. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to admit and shape the `authority_hierarchy` section. Outcome: the v7.0 system-definition artifact remains self-validating.
- [X] 22. Intent: encode anti-drift governance. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add a complexity-budget rule, errata governance, and a deprecation/removal policy for rules, profiles, extensions, and generated artifacts. Outcome: v7.0 gains explicit growth controls.
- [X] 23. Intent: type the new governance structures. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support errata severity, deprecation, removal, and related governance fields from step 22. Outcome: governance additions are schema-shaped.
- [X] 24. Intent: keep Express subordinate to the full kernel. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `express_mode` to declare generated-surface ownership and close the inactive-tier `UNBUNDLE_EXECUTE` gap without demoting Full mode. Outcome: Express remains supported but non-normative.
- [X] 25. Intent: keep the schema aligned with the Express contract. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to admit Express-generation metadata from step 24 while preserving current project-instance express branching rules. Outcome: Express support remains structurally closed.

#### Group 5 - Profiles, Runtime, and Conformance Foundations (PHASE_3_PROFILE_RUNTIME_AND_CONFORMANCE_FOUNDATION)

- [X] 26. Intent: scale obligations without reopening core topology. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add `system_class`, `operational_maturity`, `assurance_profile`, `design_complete`, and `production_ready`. Outcome: v7.0 separates shape, maturity, assurance, and readiness. Stop if: local evidence requires a different profile-axis model than the declared three-axis contract.
- [X] 27. Intent: make the profile model enforceable. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to define the profile structures, readiness-gate fields, and profile-aware checklist branches from step 26. Outcome: profile declarations are structurally typed.
- [X] 28. Intent: make hardware-aware design machine-shaped. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `CL` surfaces to add structured hardware-envelope and target-platform vocabulary for local tools, games, servers, and edge deployments. Outcome: hardware constraints become explicit contract fields.
- [X] 29. Intent: align the schema with hardware vocabulary. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support the hardware-envelope fields from step 28. Outcome: hardware declarations become machine-validated.
- [X] 30. Intent: stop runtime inference from prose alone. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add structured `preconditions`, `postconditions`, and a top-level `runtime_contract` covering concurrency, persistence, eventing, API shape, and rollback semantics. Outcome: runtime behavior becomes structured.
- [X] 31. Intent: keep the schema aligned with runtime contracts. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support operation preconditions, postconditions, and `runtime_contract`. Outcome: the system definition remains self-validating after runtime hardening.
- [X] 32. Intent: persist semantic-validation evidence. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` `DdrNode` to add `content_validation_contract`, `last_validated_by`, and `last_validated_at`. Outcome: content validation outcomes and timestamps are durable.
- [X] 33. Intent: define validation-ledger effects on readiness. Action: MODIFY `ddr/ddr_system_v7.0.yaml` so validation-ledger semantics cover pass, fail, review-required, reconciliation, activation, and readiness claims. Outcome: the structural and semantic split stays auditable.
- [X] 34. Intent: attach executable proof to the specification. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add `conformance_suite` for the validator contract, golden corpus expectations, and round-trip requirements across all document profiles. Outcome: conformance ownership becomes normative.
- [X] 35. Intent: make migration and release ownership explicit. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add `migration_contract` for v6.3 -> v7.0 and `reference_generators` for owned markdown and validation outputs. Outcome: migration and release ownership become first-class surfaces.
- [X] 36. Intent: keep the schema aligned with conformance and migration. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support `conformance_suite`, `migration_contract`, and `reference_generators`. Outcome: release-oriented additions remain structurally valid.

#### Review Gate - Approve profile axes and runtime foundation before PHASE_4

#### Group 6 - Profile-Gated Production Contracts (PHASE_4_PROFILE_GATED_PRODUCTION_CONTRACTS)

- [X] 37. Intent: cover missing production operations. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add profile-gated contracts for identity, authentication, authorization, secrets, rollout/rollback, backup/restore, failover, observability, runbooks, and on-call ownership. Outcome: security and operations obligations become explicit.
- [X] 38. Intent: cover online, data, and supply-chain runtime concerns. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add profile-gated contracts for rate limits, retry/backpressure, queues/events/streams, multi-tenancy, data governance, and supply-chain controls. Outcome: online and enterprise runtime concerns become explicit.
- [X] 39. Intent: bind target use cases to concrete obligations. Action: MODIFY `ddr/ddr_system_v7.0.yaml` profile matrices so developer tools, games, enterprise platforms, hardware-aware deployments, and medical/government/banking objectives map to minimum tiers, extensions, evidence, and readiness gates. Outcome: the requested breadth is grounded in profile obligations.

#### Group 7 - Adoption and Executable Release Surfaces (PHASE_5_ADOPTION_AND_EXECUTABLE_RELEASE_SURFACES)

- [X] 40. Intent: improve adoption without side documentation. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to expand the glossary, add profile-aware compliance guidance, and add concise tier `quick_start_example` content. Outcome: v7.0 becomes easier to author and audit.
- [X] 41. Intent: own markdown generation in one entrypoint. Action: CREATE `.agent/scripts/generate_ddr_release_docs.py` to read `ddr/ddr_system_v7.0.yaml` and `ddr/ddr_node_schema_v7.0.yaml` and emit the v7.0 markdown artifacts with provenance headers. Outcome: release-doc generation becomes a governed local surface. Stop if: one owned script cannot deterministically generate both markdown artifacts from the v7.0 YAML pair alone.
- [X] 42. Intent: keep the generator regression-safe. Action: CREATE `.agent/scripts/tests/test_generate_ddr_release_docs.py` to cover provenance headers, output-path selection, and fail-fast handling for missing or malformed v7.0 YAML files. Outcome: the generator gains a repeatable local test boundary.
- [X] 43. Intent: make generator invocation explicit. Action: CREATE `.agent/tools/generate_ddr_release_docs.md` with exact command wiring to `.agent/scripts/generate_ddr_release_docs.py`, declared inputs, declared outputs, provenance rules, and halt-on-failure behavior. Outcome: later agents can invoke the generator safely.
- [X] 44. Intent: own the release gate in one validator. Action: CREATE `.agent/scripts/validate_ddr_release.py` to validate the v7.0 YAML pair against the schema, check markdown provenance headers, and execute the v7.0 corpus. Outcome: release validation becomes a governed local surface. Stop if: local validation depends on undeclared external services or unowned commands.
- [X] 45. Intent: keep the validator regression-safe. Action: CREATE `.agent/scripts/tests/test_validate_ddr_release.py` to cover YAML self-validation, corpus manifest loading, expected pass/fail handling, and provenance checks. Outcome: the validator gains a repeatable local test boundary.
- [X] 46. Intent: make validator invocation explicit. Action: CREATE `.agent/tools/validate_ddr_release.md` with exact command wiring to `.agent/scripts/validate_ddr_release.py`, declared corpus layout, expected outputs, and halt-on-failure behavior. Outcome: later agents can invoke the release gate safely.
- [X] 47. Intent: keep governed script indexes current. Action: EXECUTE `python .agent/scripts/update_index.py` after steps 41 through 46. Outcome: `.agent/scripts/index.md` and `.agent/scripts/tests/index.md` reflect the owned release scripts and tests.
- [X] 48. Intent: back conformance with local proof data. Action: CREATE `ddr/conformance/v7.0/` with a manifest plus valid and invalid exemplars for `system_definition`, `project_instance`, and `project_instance_express`. Outcome: v7.0 gains an owned proof corpus for earlier structural and lifecycle closures.
- [X] 49. Intent: keep the governed tool index current. Action: MODIFY `.agent/tools/index.md` to inventory `generate_ddr_release_docs` and `validate_ddr_release` with correct paths, outputs, side effects, and safety notes. Outcome: later agents can discover the release tools reliably.
- [X] 50. Intent: ship the canonical markdown rendering through owned tooling. Action: CREATE `ddr/DDR System(v7.0).md` with the generator from steps 41 through 43 and include a provenance header without normative escalation. Outcome: v7.0 gains a generated canonical markdown rendering.
- [X] 51. Intent: ship the explanatory reference surface through owned tooling. Action: CREATE `ddr/ddr_ref_manual_v7.0.md` with the generator from steps 41 through 43 and include an explanatory provenance header. Outcome: v7.0 gains a generated reference manual aligned to the YAML pair.
- [X] 52. Intent: close the release with one owned validation boundary. Action: EXECUTE the validator from steps 44 through 46 against `ddr/ddr_system_v7.0.yaml`, `ddr/ddr_node_schema_v7.0.yaml`, `ddr/DDR System(v7.0).md`, `ddr/ddr_ref_manual_v7.0.md`, and `ddr/conformance/v7.0/`. Outcome: the v7.0 package is complete only after the owned release gate passes. Stop if: any valid case fails, any invalid case passes, or any provenance mismatch remains.
</atomic_steps>

<verification>
1. Confirm `ddr/ddr_node_schema_v7.0.yaml` exists and root schema identifiers mark a v7.0 contract.
2. Confirm `ddr/ddr_system_v7.0.yaml` exists and root version metadata marks a v7.0 semantic authority file.
3. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm `DdrNode.required` includes `content`, the per-node `SIL` conditional enforces `parent_ids.minItems: 1`, and minimal violating samples fail validation.
4. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `node_schema_fields`, `ICL-6.1`, `CDL-7.1`, and scaffold text require node `content` and non-root `SIL` parents.
5. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm `system_metadata` requires authority fields and `TierDefinition.required` includes `parent_relationships` and `child_relationships`.
6. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `system_metadata` and tier-definition surfaces remain populated and consistent with step 5.
7. Confirm `ddr/ddr_node_schema_v7.0.yaml` rejects `system_definition` with `project.mode: express` and documents the allowed `project` contract.
8. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `document_profile: system_definition` explicitly defines `project` semantics.
9. Inspect `ddr/ddr_system_v7.0.yaml`; confirm the v1.0 `version_history` entry no longer contains an empty `date`.
10. Inspect `ddr/ddr_system_v7.0.yaml`; confirm issue-tracker audit markers are absent from the normative file.
11. Inspect `ddr/ddr_system_v7.0.yaml` `lifecycle.status_transitions`; confirm `DEPRECATED -> ACTIVE` requires closure guards and `DEPRECATED -> DIRTY` exists.
12. Inspect `ddr/ddr_system_v7.0.yaml`; confirm DELETE semantics explicitly cover source states, terminal behavior, child handling, manifest effects, and rollback notes.
13. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm lifecycle and status structures admit only the DELETE model encoded in `ddr/ddr_system_v7.0.yaml`.
14. Inspect `ddr/ddr_node_schema_v7.0.yaml` `ParentCitation`; confirm `validated_parent_version` exists with the intended typing.
15. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `CIT-R7` and related validation text rely on `validated_parent_version`.
16. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm manifest definitions admit every typed family added in step 16.
17. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `reconciliation_manifest_schema` defines every manifest family admitted by the schema.
18. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm `TierRelationship.edge_type` excludes `extends` and extension rule-family typing remains distinct from core families.
19. Inspect `ddr/ddr_system_v7.0.yaml`; confirm rule-family uniqueness is explicit and `extends` is reserved for extension interaction.
20. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `authority_hierarchy` distinguishes semantic authority, structural authority, and derived surfaces.
21. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the schema supports `authority_hierarchy`.
22. Inspect `ddr/ddr_system_v7.0.yaml`; confirm the file contains a complexity-budget rule, errata governance, and a deprecation/removal policy for rules, profiles, extensions, and generated artifacts.
23. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm governance structures from step 22 are structurally typed.
24. Inspect `ddr/ddr_system_v7.0.yaml` `express_mode`; confirm generated-surface ownership and inactive-tier unbundle semantics are explicit without demoting Full mode.
25. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm Express-generation metadata is supported without changing current project-instance express branching rules.
26. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `system_class`, `operational_maturity`, `assurance_profile`, `design_complete`, and `production_ready` exist as distinct fields.
27. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the profile axes and readiness-gate fields are structurally typed.
28. Inspect `ddr/ddr_system_v7.0.yaml` `CL` surfaces; confirm hardware-envelope and target-platform vocabulary is explicit and structured.
29. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm hardware-envelope fields from step 28 are schema-shaped.
30. Inspect `ddr/ddr_system_v7.0.yaml`; confirm core operations have structured `preconditions` and `postconditions` and `runtime_contract` covers concurrency, persistence, eventing, API shape, and rollback semantics.
31. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm operation contract structures and `runtime_contract` are supported.
32. Inspect `ddr/ddr_node_schema_v7.0.yaml` `DdrNode`; confirm `content_validation_contract`, `last_validated_by`, and `last_validated_at` exist with the intended typing.
33. Inspect `ddr/ddr_system_v7.0.yaml`; confirm validation-ledger semantics cover pass, fail, review-required, reconciliation, activation, and readiness claims.
34. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `conformance_suite` names the validator contract, corpus ownership, and round-trip requirements for all supported document profiles.
35. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `migration_contract` and `reference_generators` are scoped to the v6.3 -> v7.0 release path and owned release outputs.
36. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm `conformance_suite`, `migration_contract`, and `reference_generators` are supported structurally.
37. Inspect `ddr/ddr_system_v7.0.yaml`; confirm profile-gated contracts cover identity, authn, authz, secrets, rollout/rollback, backup/restore, failover, observability, runbooks, and on-call ownership.
38. Inspect `ddr/ddr_system_v7.0.yaml`; confirm profile-gated contracts cover rate limits, retry/backpressure, queues/events/streams, multi-tenancy, data governance, and supply-chain controls.
39. Inspect `ddr/ddr_system_v7.0.yaml` profile matrices; confirm each target use case maps through `system_class`, `operational_maturity`, and `assurance_profile` to minimum obligations.
40. Inspect `ddr/ddr_system_v7.0.yaml`; confirm the glossary, profile-aware compliance guidance, and tier `quick_start_example` content exist.
41. Confirm `.agent/scripts/generate_ddr_release_docs.py` exists and names the v7.0 YAML pair plus both v7.0 markdown outputs.
42. Run `pytest .agent/scripts/tests/test_generate_ddr_release_docs.py -q` and confirm the test covers provenance headers, output-path selection, and missing-input failure behavior.
43. Inspect `.agent/tools/generate_ddr_release_docs.md`; confirm the frontmatter command targets `.agent/scripts/generate_ddr_release_docs.py` and the body names exact inputs, outputs, provenance rules, and halt-on-failure behavior.
44. Confirm `.agent/scripts/validate_ddr_release.py` exists and names YAML self-validation, markdown provenance checks, and corpus execution.
45. Run `pytest .agent/scripts/tests/test_validate_ddr_release.py -q` and confirm the test covers YAML self-validation, corpus manifest loading, expected pass/fail handling, and provenance checks.
46. Inspect `.agent/tools/validate_ddr_release.md`; confirm the frontmatter command targets `.agent/scripts/validate_ddr_release.py` and the body names corpus layout, outputs, and halt-on-failure behavior.
47. Inspect `.agent/scripts/index.md` and `.agent/scripts/tests/index.md`; confirm both regenerated indexes list the owned release scripts and tests accurately.
48. Inspect `ddr/conformance/v7.0/`; confirm the corpus contains a manifest plus valid and invalid exemplars for `system_definition`, `project_instance`, and `project_instance_express`.
49. Inspect `.agent/tools/index.md`; confirm the file inventories `generate_ddr_release_docs` and `validate_ddr_release` with correct paths, outputs, side effects, and safety notes.
50. Confirm `ddr/DDR System(v7.0).md` exists, carries a provenance header tied to the v7.0 YAML pair, and does not claim stronger authority than the YAML pair.
51. Confirm `ddr/ddr_ref_manual_v7.0.md` exists, carries a provenance header tied to the v7.0 YAML pair, and remains explanatory rather than normative.
52. Run the owned release validator and confirm zero self-validation errors, passing valid corpus cases, failing invalid corpus cases for the expected reasons, and matching provenance headers across generated markdown outputs.
</verification>

<risks_and_mitigations>
- **Risk:** Scope creep or inference pressure expands the release beyond the reviewed v7.0 work.
  **Mitigation:** Keep the same 5 phases, 52 atomic steps, and 52 verification items, and halt on missing or conflicting repo evidence instead of broadening scope.

- **Risk:** Compat-first plan optimization drifts into unsupported contract retargeting.
  **Mitigation:** Do not modify `.agent/config/runtime-target.yaml`, `.agent/schemas/implementation-plan/*`, or `.agent/skills/artifact-implementation-plan/SKILL.md` during the optimization pass.

- **Risk:** DELETE, rule-family, or profile-axis decisions proceed without explicit review.
  **Mitigation:** Treat the review gates before PHASE_2 and PHASE_4 as hard stop/go boundaries and honor the step-level halt clauses in steps 12, 18, and 26.

- **Risk:** Generator, validator, index, or corpus surfaces drift from the YAML authority pair.
  **Mitigation:** Land owned scripts, tests, tool docs, indexes, corpus data, generated markdown, and the final release-validation run in the order declared by steps 41 through 52.

- **Risk:** Rejected recommendations re-enter through convenience edits.
  **Mitigation:** Preserve three exclusions across all phases: Express does not become the only canonical authoring surface, semantic review remains in the normative model, and ARE remains normative unless schema and semantic authority change together under explicit review.
</risks_and_mitigations>
