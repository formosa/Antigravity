---
task: "Produce a review-gated DDR System v7.0 release package centered on a self-validating YAML authority pair, generated derivative surfaces, and profile-driven production contracts while preserving the frozen v6.x core topology."
model: "gemini-3-pro-preview"
version: "6.0.2"
output_path: ".agent/plans/20260413-054500-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260413-054500-IMPLEMENTATION_PLAN.md"
---

<objective>
Produce DDR System v7.0 as a self-validating authority pair (`ddr/ddr_node_schema_v7.0.yaml`, `ddr/ddr_system_v7.0.yaml`) plus generated human-readable release surfaces that first resolve the source-visible v6.3 contract gaps verified in the YAML SSOT, then harden authority and conformance ownership, and only then add profile-gated runtime and production contracts for use cases spanning scripts, developer tools, games, enterprise systems, hardware-aware deployments, and regulated-sector objectives without changing the core 9-tier topology or stripping semantic review from the model.
</objective>

<phases>
- phase_id: "PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS"
  objectives:
    - "Create isolated v7.0 working copies of the YAML SSOT pair"
    - "Close the source-visible v6.3 contract defects with direct local evidence"
    - "Keep rejected review prescriptions out of the v7.0 baseline"
  task_references: ["source-visible-gap-closure", "release-blocking-defects"]
  entry_criteria:
    - "The v6.3 YAML SSOT pair is readable and schema-validates successfully"
    - "review.gemini.md, review.codex.md, and review.opus.md have been synthesized against the YAML pair"
  exit_criteria:
    - "The v7.0 YAML pair self-validates after all release-blocking edits"
    - "DELETE semantics and rule-family changes are explicitly reviewed before authority hardening proceeds"
    - "No step demotes Full mode, removes semantic review, or de-normativizes ARE contrary to the v6.3 SSOT"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_2_AUTHORITY_AND_GENERATION_GOVERNANCE"
  objectives:
    - "Freeze the kernel around the YAML pair as the normative authority"
    - "Formalize generated-surface ownership and governance"
    - "Encode complexity-budget, errata, and deprecation controls before scope expansion"
  task_references: ["authority-hardening", "generated-surfaces"]
  entry_criteria:
    - "PHASE_1 exit criteria are satisfied"
  exit_criteria:
    - "Authority hierarchy, generated-surface precedence, and express-generation semantics are encoded in the v7.0 pair"
    - "Governance additions validate without reopening core-topology drift"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_3_PROFILE_RUNTIME_AND_CONFORMANCE_FOUNDATION"
  objectives:
    - "Add the profile model and separate design-complete from production-ready gating"
    - "Make runtime behavior and operation contracts machine-shaped"
    - "Define migration, conformance, and generator ownership before bulk contract expansion"
  task_references: ["profile-model", "runtime-contract", "conformance"]
  entry_criteria:
    - "PHASE_2 exit criteria are satisfied"
  exit_criteria:
    - "Profiles, runtime contract, validation ledger semantics, and conformance surfaces validate in the v7.0 pair"
    - "The profile model is explicitly reviewed before profile-gated production obligations are expanded"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_4_PROFILE_GATED_PRODUCTION_CONTRACTS"
  objectives:
    - "Expand production obligations through profiles and existing extension surfaces rather than new core topology"
    - "Cover security, deployment, resilience, observability, online/event, data, and supply-chain contracts"
    - "Bind broad use cases to explicit minimum obligations"
  task_references: ["production-contract-expansion"]
  entry_criteria:
    - "PHASE_3 exit criteria are satisfied"
  exit_criteria:
    - "Target use cases map to explicit tiers, extensions, evidence, and readiness gates"
    - "No new core tiers, edge types, or operations are introduced unless required by an already-approved defect closure"
  assigned_model: "gemini-3-flash-preview"

- phase_id: "PHASE_5_ADOPTION_AND_DERIVED_RELEASE_SURFACES"
  objectives:
    - "Complete the adoption surfaces needed to make v7.0 usable"
    - "Stand up the generator-owned v7.0 markdown outputs"
    - "Finish with self-hosting validation of the final v7.0 release package"
  task_references: ["migration", "derived-release-surfaces"]
  entry_criteria:
    - "PHASE_4 exit criteria are satisfied"
  exit_criteria:
    - "The generated v7.0 markdown surfaces exist with provenance headers"
    - "The v7.0 YAML pair validates through the standard JSON Schema workflow"
  assigned_model: "gemini-3-flash-preview"
</phases>

<atomic_steps>
#### Group 1 - V7 Baseline Copies (PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS)

- [ ] 1. Intent: establish an isolated structural baseline for v7.0. Action: CREATE `ddr/ddr_node_schema_v7.0.yaml` by cloning `ddr/ddr_node_schema_v6.3.yaml` and updating only the root schema identifiers needed to mark it as the v7.0 machine contract. Outcome: all later schema edits land on a new versioned file while the v6.3 SSOT remains untouched.
- [ ] 2. Intent: establish an isolated semantic-authority baseline for v7.0. Action: CREATE `ddr/ddr_system_v7.0.yaml` by cloning `ddr/ddr_system_v6.3.yaml` and updating only the root version metadata needed to mark it as the v7.0 semantic authority. Outcome: all later system-definition edits land on a new versioned file while the v6.3 SSOT remains untouched.

#### Group 2 - Structural Admission and Metadata Closures (PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS)

- [ ] 3. Intent: close the two directly observed schema admission gaps called out across the reviews. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `DdrNode.content` is required and the per-node `SIL` conditional enforces `parent_ids.minItems: 1` instead of relying only on the document-level `active_tiers` branch. Outcome: hollow nodes and orphan `SIL` nodes fail structural validation.
- [ ] 4. Intent: keep the semantic authority self-consistent with the tightened schema front door. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `node_schema_fields`, `ICL-6.1`, `CDL-7.1`, and any scaffold text that still describe `content` as optional or leave the `SIL` root rule under-specified. Outcome: the v7.0 semantic-authority text matches the v7.0 schema on required node content and `SIL` parent requirements.
- [ ] 5. Intent: prevent structurally incomplete system-definition records from passing validation. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `system_metadata` requires the essential authority fields and `TierDefinition` requires `parent_relationships` and `child_relationships`. Outcome: empty authority metadata and topology-less tier definitions are rejected structurally.
- [ ] 6. Intent: mirror the tightened metadata and topology expectations in the semantic authority itself. Action: MODIFY `ddr/ddr_system_v7.0.yaml` so system metadata and tier-definition narrative/scaffold surfaces explicitly assume the required authority fields and explicit parent/child topology declarations. Outcome: the v7.0 system definition remains self-hosting under the stricter schema.
- [ ] 7. Intent: close the unresolved `project` and `mode` ambiguity on `system_definition` artifacts. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `system_definition` documents cannot declare `project.mode: express`, and document the intended contract for the `project` block under that profile in schema descriptions and conditionals. Outcome: profile/mode branching is structurally unambiguous for the authoritative artifact.

#### Group 3 - Semantic-Authority Release Blockers (PHASE_1_V7_BASELINE_AND_RELEASE_BLOCKERS)

- [ ] 8. Intent: make the semantic authority explicit about the `project` block now that the schema no longer leaves it implicit. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to define the role of `project` for `document_profile: system_definition` and align any profile/mode prose with the v7.0 schema branch. Outcome: the v7.0 authority no longer relies on reader inference for the `project` block.
- [ ] 9. Intent: remove an obvious self-inconsistency from the historical authority surface. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `version_history` so the v1.0 entry no longer carries an empty `date` field. Outcome: the semantic authority does not contain blank historical metadata where v7.0 expects explicit values.
- [ ] 10. Intent: remove version-specific audit residue from the normative authority file. Action: MODIFY `ddr/ddr_system_v7.0.yaml` inline comments so issue-tracker style commentary is migrated out of the normative surface or rewritten as timeless explanatory notes. Outcome: the v7.0 authority file contains enduring semantics rather than transient audit chatter.
- [ ] 11. Intent: close the lifecycle gaps around deprecated nodes before any forward expansion begins. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `lifecycle.status_transitions` so `DEPRECATED -> ACTIVE` requires the same structural/review closure expected for re-activation and `DEPRECATED -> DIRTY` is explicitly represented for propagation-driven re-entry. Outcome: deprecated nodes can be re-validated lawfully and cannot bypass validation/review gates.
- [ ] 12. Intent: stop treating DELETE as an implicit sink that the reviews identified as semantically incomplete. Action: MODIFY `ddr/ddr_system_v7.0.yaml` lifecycle and operation narratives to encode the approved v7.0 DELETE semantics, including allowed source states, terminal behavior, child handling, manifest effects, and rollback notes. Outcome: DELETE becomes a machine-auditable semantic contract rather than an unstated assumption.
- [ ] 13. Intent: make the structural contract admit exactly the DELETE semantics chosen in step 12. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` lifecycle/status definitions to match the approved DELETE model from the semantic authority, adding only the transition or terminal-token support that model requires. Outcome: the schema and semantic authority agree on DELETE handling.
- [ ] 14. Intent: make `CIT-R7` mechanically enforceable instead of baseline-free. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` `ParentCitation` to add `validated_parent_version` with write-on-validate semantics. Outcome: child freshness can be evaluated against persisted parent-version checkpoints.
- [ ] 15. Intent: align the semantic authority with the persisted parent-version freshness model. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `citation_rules`, validation prose, and related scaffold text so `CIT-R7` explicitly relies on the stored validated parent version. Outcome: parent freshness is described consistently across the v7.0 authority surfaces.
- [ ] 16. Intent: close the under-typed reconciliation-manifest surface identified by the reviews. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` manifest-related definitions so the schema admits the additional typed item families already described in the semantic system, including `REVIEW_REQUIRED`, extension advisories, conflict-resolution records, override approvals, and deferred fragments. Outcome: the v7.0 schema can structurally represent the full manifest behavior the authority describes.
- [ ] 17. Intent: make the semantic authority enumerate the full manifest taxonomy instead of relying on implied categories. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `reconciliation_manifest_schema` and related semantic-gap language so every manifest item family admitted by step 16 is explicitly defined with fields and usage semantics. Outcome: manifest state is typed and auditably closed at the semantic-authority layer.
- [ ] 18. Intent: separate core topology identifiers from extension-only semantics at the schema level. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` so `TierRelationship.edge_type` no longer admits `extends`, and tighten extension rule-family typing so extension rule IDs remain distinguishable from core rule families. Outcome: the schema stops allowing extension-only semantics in core topology fields and reduces rule-family ambiguity.
- [ ] 19. Intent: make rule-family uniqueness and edge separation explicit in the semantic authority. Action: MODIFY `ddr/ddr_system_v7.0.yaml` so rule-family uniqueness is stated as an invariant or equivalent governance rule, and core-topology prose clearly reserves `extends` for extension interaction rather than tier relationships. Outcome: tooling and human review can resolve rule IDs and edge semantics without hidden assumptions.

#### Group 4 - Authority and Generated-Surface Governance (PHASE_2_AUTHORITY_AND_GENERATION_GOVERNANCE)

- [ ] 20. Intent: generalize the v6.3 lifecycle-authority precedent into a full v7.0 authority model. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add an explicit `authority_hierarchy` section that distinguishes semantic authority, structural authority, and derived human-readable surfaces. Outcome: the YAML pair becomes the formally declared normative source for v7.0.
- [ ] 21. Intent: keep the structural contract aligned with the new authority model. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to admit and shape the `authority_hierarchy` section introduced in step 20. Outcome: the v7.0 system-definition artifact remains self-validating with its explicit authority hierarchy.
- [ ] 22. Intent: encode the governance controls that all three reviews treated as necessary to avoid further additive drift. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add a complexity-budget rule, formal errata governance, and a deprecation/removal policy that covers rules, profiles, extensions, and generated artifacts. Outcome: v7.0 has explicit governance pressure against uncontrolled core growth and drift.
- [ ] 23. Intent: make the schema support the new governance fields instead of leaving them prose-only. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support the errata severity, deprecation, removal, and related governance structures introduced in step 22. Outcome: governance additions are structurally typed.
- [ ] 24. Intent: keep Express Mode in the system while preventing it from becoming a rival authority surface. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `express_mode` semantics so v7.0 explicitly declares generated-surface ownership for Express renderings and closes the inactive-tier `UNBUNDLE_EXECUTE` gap without promoting Express to the only authoring mode. Outcome: Express remains supported, subordinate to the full kernel, and deterministic under reduced topology.
- [ ] 25. Intent: keep the v7.0 schema aligned with the hardened Express contract. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to admit any new Express-generation metadata introduced in step 24 while preserving the existing project-instance express branching rules. Outcome: Express-mode authority remains structurally closed without altering the canonical consumption-mode contract.

#### Group 5 - Profiles, Runtime, and Conformance Foundations (PHASE_3_PROFILE_RUNTIME_AND_CONFORMANCE_FOUNDATION)

- [ ] 26. Intent: add scaling without reopening core topology. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to introduce a profile model centered on `system_class` and `operational_maturity`, and separate `design_complete` from `production_ready` as distinct readiness gates. Outcome: v7.0 can scale obligations by profile instead of by new tiers or new core topology.
- [ ] 27. Intent: make the profile model structurally enforceable. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to define the profile structures, readiness-gate fields, and any profile-aware checklist branches introduced in step 26. Outcome: profile declarations and readiness gates become schema-shaped rather than prose-only.
- [ ] 28. Intent: make hardware-aware design machine-shaped for the use cases the user explicitly named. Action: MODIFY `ddr/ddr_system_v7.0.yaml` `CL` surfaces to add a structured hardware-envelope and target-platform vocabulary that can cover local tools, games, servers, edge devices, and other hardware-aware deployments. Outcome: v7.0 expresses hardware constraints as explicit contract fields rather than prose-only declarations.
- [ ] 29. Intent: align the structural contract with the v7.0 hardware vocabulary. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support the structured hardware-envelope fields introduced in step 28. Outcome: CL hardware declarations are structurally typed and machine-validated.
- [ ] 30. Intent: stop forcing runtime implementations to infer critical behavior from prose alone. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add machine-shaped `preconditions` and `postconditions` to core operations and a top-level `runtime_contract` covering concurrency, persistence, eventing, API shape, and transaction/rollback semantics. Outcome: v7.0 expresses executable runtime behavior as structured contracts.
- [ ] 31. Intent: keep the schema aligned with the machine-shaped operation/runtime surfaces. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support the operation precondition/postcondition structures and the new `runtime_contract` section introduced in step 30. Outcome: the v7.0 system definition remains self-validating after runtime-contract hardening.
- [ ] 32. Intent: make content-rule evaluation and validation recency auditable without collapsing semantic review into pure schema checks. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` `DdrNode` to add a `content_validation_contract` plus validation metadata fields such as `last_validated_by` and `last_validated_at`. Outcome: v7.0 can persist semantic-evaluation outcomes and validation timestamps without pretending the schema alone proves semantic completeness.
- [ ] 33. Intent: define how the new validation ledger participates in CLEAN and review-required semantics. Action: MODIFY `ddr/ddr_system_v7.0.yaml` so validation-ledger semantics explicitly describe pass/fail/review-required outcomes and their effect on reconciliation, activation, and readiness claims. Outcome: the structural/semantic split remains intact but auditable.
- [ ] 34. Intent: back the v7.0 specification with executable proof surfaces rather than prose promises. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add a `conformance_suite` that defines the reference validator contract, golden corpus expectations, and round-trip requirements for `project_instance`, `project_instance_express`, and `system_definition` flows. Outcome: conformance ownership is part of the v7.0 semantic authority.
- [ ] 35. Intent: make upgrading and generated-surface ownership explicit before bulk rollout. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add a `migration_contract` for v6.3 -> v7.0 and a `reference_generators` contract for derived documentation, starter outputs, and other owned generated surfaces. Outcome: migration and generated-surface ownership are first-class release surfaces rather than afterthoughts.
- [ ] 36. Intent: keep the schema aligned with the new conformance, migration, and generator contracts. Action: MODIFY `ddr/ddr_node_schema_v7.0.yaml` to support `conformance_suite`, `migration_contract`, and `reference_generators`. Outcome: the v7.0 system-definition artifact remains structurally valid after these release-oriented additions.

#### Group 6 - Profile-Gated Production Contract Expansion (PHASE_4_PROFILE_GATED_PRODUCTION_CONTRACTS)

- [ ] 37. Intent: cover the operational areas the reviews identified as missing from production-ready use. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to expand profile-gated contract coverage for identity, authentication, authorization, secret/key management, rollout/rollback policy, backup/restore, failover, observability, runbooks, and on-call ownership through existing core and extension surfaces rather than new tiers. Outcome: v7.0 gains explicit security, deployment, resilience, and observability obligations without reopening the kernel.
- [ ] 38. Intent: cover the remaining production-readiness surfaces needed for online, data-heavy, and enterprise use cases. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to add profile-gated contracts for rate limits, retry/backpressure, queues/events/streams, multi-tenancy, data governance, supply-chain controls, and related delivery/runtime semantics. Outcome: v7.0 explicitly models the online/event/data/supply-chain concerns the reviews identified as absent or under-modeled.
- [ ] 39. Intent: bind the broad target use cases to concrete obligations instead of leaving them aspirational. Action: MODIFY `ddr/ddr_system_v7.0.yaml` profile matrices so developer tools, games, enterprise platforms, hardware-aware deployments, and medical/government/banking objectives each map to explicit minimum tiers, extensions, evidence, and readiness gates. Outcome: the user-requested breadth is grounded in profile obligations rather than broad marketing language.

#### Group 7 - Adoption and Derived Release Surfaces (PHASE_5_ADOPTION_AND_DERIVED_RELEASE_SURFACES)

- [ ] 40. Intent: make v7.0 authorable and auditable by humans once the contracts are stable. Action: MODIFY `ddr/ddr_system_v7.0.yaml` to expand the glossary, add profile-aware compliance guidance, and add concise tier `quick_start_example` content where the reviews identified an adoption gap. Outcome: the v7.0 authority contains the adoption scaffolding required to use the stronger model without informal side docs.
- [ ] 41. Intent: eliminate manual drift between the v7.0 YAML pair and its human-readable renderings. Action: CREATE the reproducible v7.0 documentation-generation workflow in the existing `ddr/` surface so one owned workflow reads the v7.0 YAML pair and emits the derived markdown artifacts with provenance headers. Outcome: v7.0 human-readable surfaces become generator-owned rather than manually co-maintained.
- [ ] 42. Intent: ship the canonical human-readable rendering for the new release. Action: CREATE `ddr/DDR System(v7.0).md` from the workflow introduced in step 41 so it renders the finalized v7.0 YAML authority pair without claiming independent normative weight. Outcome: v7.0 has a generated canonical markdown rendering aligned to the YAML pair.
- [ ] 43. Intent: ship the reference-manual surface needed for practical adoption and audit. Action: CREATE `ddr/ddr_ref_manual_v7.0.md` from the workflow introduced in step 41 so the final v7.0 authority pair has a generated explanatory companion with explicit provenance. Outcome: v7.0 includes a derived reference manual aligned to the finalized YAML authorities.
</atomic_steps>

<verification>
1. Confirm `ddr/ddr_node_schema_v7.0.yaml` exists and its root schema identifiers mark it as a v7.0 contract rather than a second v6.3 file.
2. Confirm `ddr/ddr_system_v7.0.yaml` exists and its root version metadata marks it as the v7.0 semantic authority rather than a second v6.3 file.
3. Inspect `ddr/ddr_node_schema_v7.0.yaml` and confirm `DdrNode.required` now includes `content` and the per-node `SIL` conditional enforces `parent_ids.minItems: 1`; a minimal missing-content node and a minimal orphan `SIL` node must both fail validation.
4. Inspect `ddr/ddr_system_v7.0.yaml` `node_schema_fields`, `ICL-6.1`, `CDL-7.1`, and related scaffold text; confirm none of those surfaces still describe `content` as optional or leave the `SIL` parent rule weaker than the schema.
5. Inspect `ddr/ddr_node_schema_v7.0.yaml` and confirm `system_metadata` requires the essential authority fields and `TierDefinition.required` includes `parent_relationships` and `child_relationships`.
6. Inspect `ddr/ddr_system_v7.0.yaml` and confirm its system metadata and tier-definition surfaces remain populated and consistent with the stricter schema from step 5.
7. Confirm the v7.0 schema rejects a `system_definition` artifact with `project.mode: express` and explicitly documents the intended `project` contract for that profile.
8. Inspect `ddr/ddr_system_v7.0.yaml` and confirm the `project` block semantics for `document_profile: system_definition` are explicitly described rather than implied.
9. Inspect the v1.0 `version_history` entry in `ddr/ddr_system_v7.0.yaml` and confirm the `date` field is no longer empty.
10. Search `ddr/ddr_system_v7.0.yaml` for issue-tracker style inline audit markers such as `ISSUE-`; confirm the normative file no longer contains version-specific audit residue.
11. Inspect `lifecycle.status_transitions` in `ddr/ddr_system_v7.0.yaml`; confirm `DEPRECATED -> ACTIVE` includes structural/review closure guards and `DEPRECATED -> DIRTY` exists as an explicit propagation path.
12. Inspect DELETE semantics in `ddr/ddr_system_v7.0.yaml`; confirm allowed source states, terminal behavior, child handling, manifest impact, and rollback notes are explicitly encoded rather than implied.
13. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the lifecycle/status structures admit the DELETE model chosen in step 12 and the v7.0 pair remains internally consistent after that choice.
14. Inspect `ParentCitation` in `ddr/ddr_node_schema_v7.0.yaml`; confirm `validated_parent_version` exists with the intended v7.0 typing.
15. Inspect `CIT-R7` and related validation text in `ddr/ddr_system_v7.0.yaml`; confirm the rule now relies on the persisted validated parent version rather than an unstated baseline.
16. Inspect manifest-related definitions in `ddr/ddr_node_schema_v7.0.yaml`; confirm the expanded manifest item families are structurally admitted.
17. Inspect `reconciliation_manifest_schema` in `ddr/ddr_system_v7.0.yaml`; confirm every manifest family admitted by the schema is explicitly defined semantically.
18. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm `TierRelationship.edge_type` no longer admits `extends` and extension rule-family typing no longer overlaps the core families implicitly.
19. Inspect `ddr/ddr_system_v7.0.yaml`; confirm it explicitly states global rule-family uniqueness and keeps `extends` reserved for extension interaction rather than core tier relationships.
20. Inspect `ddr/ddr_system_v7.0.yaml`; confirm an `authority_hierarchy` section explicitly distinguishes semantic authority, structural authority, and derived surfaces.
21. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm it supports the `authority_hierarchy` section present in the v7.0 system file.
22. Inspect `ddr/ddr_system_v7.0.yaml`; confirm it contains a complexity-budget rule, explicit errata governance, and a deprecation/removal policy covering rules, profiles, extensions, and generated artifacts.
23. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the schema supports the governance structures introduced in step 22, including any errata severity or deprecation/removal fields required by the v7.0 authority.
24. Inspect `ddr/ddr_system_v7.0.yaml` `express_mode`; confirm it now includes generated-surface ownership and inactive-tier unbundle semantics without demoting Full mode or deleting deferred semantic review behavior.
25. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm it supports any new Express-generation metadata while preserving the existing express profile branching rules.
26. Inspect `ddr/ddr_system_v7.0.yaml`; confirm the profile model includes `system_class`, `operational_maturity`, and distinct `design_complete` / `production_ready` readiness gates.
27. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the profile structures and readiness-gate fields introduced in step 26 are structurally typed.
28. Inspect the `CL` surfaces in `ddr/ddr_system_v7.0.yaml`; confirm the v7.0 hardware-envelope and target-platform vocabulary is explicit and not prose-only.
29. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the hardware-envelope structure introduced in step 28 is schema-shaped.
30. Inspect `operations` and the top-level runtime section in `ddr/ddr_system_v7.0.yaml`; confirm core operations have structured preconditions/postconditions and `runtime_contract` covers concurrency, persistence, eventing, API shape, and rollback semantics.
31. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the schema supports the new operation contract structures and `runtime_contract`.
32. Inspect `DdrNode` in `ddr/ddr_node_schema_v7.0.yaml`; confirm `content_validation_contract`, `last_validated_by`, and `last_validated_at` are present with the intended typing.
33. Inspect `ddr/ddr_system_v7.0.yaml`; confirm validation-ledger semantics explicitly describe pass/fail/review-required outcomes and their effect on CLEAN/readiness claims.
34. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `conformance_suite` exists and names the validator contract, corpus ownership, and round-trip requirements for all supported document profiles.
35. Inspect `ddr/ddr_system_v7.0.yaml`; confirm `migration_contract` and `reference_generators` exist and are scoped to the v6.3 -> v7.0 release path and generator-owned outputs.
36. Inspect `ddr/ddr_node_schema_v7.0.yaml`; confirm the schema supports `conformance_suite`, `migration_contract`, and `reference_generators`.
37. Inspect `ddr/ddr_system_v7.0.yaml`; confirm profile-gated contracts now cover identity/authn/authz, secret/key management, rollout/rollback, backup/restore, failover, observability, runbooks, and on-call ownership.
38. Inspect `ddr/ddr_system_v7.0.yaml`; confirm profile-gated contracts now cover online runtime controls, queues/events/streams, multi-tenancy, data governance, and supply-chain controls.
39. Inspect the profile matrices in `ddr/ddr_system_v7.0.yaml`; confirm developer tools, games, enterprise platforms, hardware-aware deployments, and medical/government/banking objectives each map to explicit minimum obligations.
40. Inspect `ddr/ddr_system_v7.0.yaml`; confirm the glossary is expanded, compliance guidance is profile-aware, and tier quick-start examples exist for the intended adoption surfaces.
41. Confirm the v7.0 documentation-generation workflow exists under `ddr/` and explicitly names the v7.0 YAML pair as its input and the two v7.0 markdown artifacts as its generator-owned outputs.
42. Confirm `ddr/DDR System(v7.0).md` exists, carries a provenance header tying it back to the v7.0 YAML pair, and does not claim stronger authority than the YAML surfaces.
43. Confirm `ddr/ddr_ref_manual_v7.0.md` exists, carries a provenance header tying it back to the v7.0 YAML pair, and run the standard YAML-against-schema validation flow already documented in the schema header using `.\.venv\Scripts\python.exe` against `ddr/ddr_system_v7.0.yaml` and `ddr/ddr_node_schema_v7.0.yaml`; require zero validation errors.
</verification>

<risks_and_mitigations>
- **Risk:** The release-blocking v7.0 changes create breaking differences from v6.3, especially around required `content`, stronger lifecycle semantics, and validation baselines.
  **Mitigation:** Keep v6.3 files untouched, land all breaking changes only in the v7.0 pair, and complete the explicit `migration_contract` in PHASE_3 before treating the release package as ready.

- **Risk:** DELETE modeling and rule-family changes can destabilize the frozen core if they are implemented without review.
  **Mitigation:** Treat PHASE_1 exit as a hard review gate for the DELETE model and rule-family diffs before authority hardening or profile expansion continues.

- **Risk:** Generated-surface governance regresses into another hand-maintained authority layer.
  **Mitigation:** Make the generation workflow a first-class owned surface, require provenance headers on both v7.0 markdown outputs, and keep the YAML pair as the only normative authority.

- **Risk:** The profile model turns into hidden topology expansion.
  **Mitigation:** Enforce the complexity-budget rule and explicitly keep scaling in `system_class`, `operational_maturity`, and profile-gated contracts rather than new tiers, edge types, or informal side systems.

- **Risk:** Recommendations rejected by the review synthesis creep back into implementation through convenience edits.
  **Mitigation:** Preserve three explicit exclusions across all phases: do not make Express the only canonical authoring surface, do not remove semantic review from the normative model, and do not remove ARE normative authority unless the schema and semantic contract are revised together under explicit review.

- **Risk:** The conformance and generation surfaces lag behind late v7.0 YAML changes and leave the release package internally inconsistent.
  **Mitigation:** Do not complete PHASE_5 until the generation workflow has emitted both v7.0 markdown artifacts from the finalized YAML pair and the final YAML-against-schema validation passes cleanly.
</risks_and_mitigations>
