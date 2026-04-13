---
task: "Produce DDR System v7.0 by closing all source-visible v6.3 contract gaps, hardening governance authority, adding profile-driven capability scaling, completing production contracts, bridging the specification-to-implementation gap, and accelerating adoption — without expanding core topology."
model: "gemini-3-pro-preview"
version: "6.0.2"
output_path: ".agent/plans/20260413-054500-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260413-054500-IMPLEMENTATION_PLAN.md"
---

<objective>
Transform DDR System v6.3 into DDR System v7.0 — a comprehensive, complete, stable, dynamic, and production-ready software application design framework — by executing 48 atomic modifications organized across 6 phases. The modifications close all source-visible contract gaps in the v6.3 YAML pair, harden governance and SSOT authority, introduce a profile-driven capability governance system enabling use cases from custom scripts to enterprise-scale regulated applications, complete production contract coverage, bridge the gap between finalized specification and implementable runtime, and deliver adoption tooling and documentation. The core topology (9 tiers, 4 edge types, 7 axioms) remains frozen; all scaling is achieved through profiles and extension scope expansion.
</objective>

<phases>
- phase_id: "PHASE_1_CONTRACT_GAP_CLOSURE"
  objectives:
    - "Close all 14 source-visible contract gaps in the v6.3 YAML pair"
    - "Achieve schema self-consistency: every rule, invariant, and lifecycle row the system YAML describes must be structurally enforceable by the node schema"
  task_references: ["M-01", "M-02", "M-03", "M-04", "M-05", "M-06", "M-07", "M-08", "M-09", "M-10", "M-11", "M-12", "M-13", "M-14"]
  entry_criteria:
    - "v6.3 YAML pair (`ddr_system_v6.3.yaml`, `ddr_node_schema_v6.3.yaml`) available and schema-validates successfully"
    - "All three review documents (`review.gemini.md`, `review.codex.md`, `review.opus.md`) read and synthesized"
  exit_criteria:
    - "v7.0 node schema validates the v7.0 system YAML with zero errors"
    - "All 14 modifications are individually schema-testable and pass"
    - "No new section or property is introduced that was not identified as a source-visible gap"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_2_AUTHORITY_HARDENING"
  objectives:
    - "Freeze the core kernel with an enforceable complexity budget"
    - "Establish the YAML pair as the sole normative authority with machine-generated derivative surfaces"
    - "Add deprecation and removal governance"
  task_references: ["M-15", "M-16", "M-17", "M-18", "M-19", "M-20", "M-21"]
  entry_criteria:
    - "PHASE_1 complete: v7.0 YAML pair passes self-validation"
  exit_criteria:
    - "Authority hierarchy section present and machine-parseable"
    - "Complexity budget principle codified in design philosophy"
    - "Express Mode generation contract declared"
    - "Errata governance and deprecation policy formalized"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_3_PROFILE_SYSTEM"
  objectives:
    - "Add system_class and operational_maturity profile dimensions"
    - "Add hardware-profile schema to CL"
    - "Add validation gate separation (design_complete vs production_ready)"
    - "Add optional tags field to DdrNode"
  task_references: ["M-22", "M-23", "M-24", "M-25", "M-26"]
  entry_criteria:
    - "PHASE_2 complete: authority hierarchy and complexity budget in place"
  exit_criteria:
    - "Profile taxonomy schema-validated"
    - "At least 3 system_class × operational_maturity combinations have enumerated minimum obligations"
    - "Hardware-profile sub-schema validates structured CL hardware declarations"
    - "Both validation gates (design_complete, production_ready) have distinct checklist items"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_4_PRODUCTION_CONTRACTS"
  objectives:
    - "Expand extension scope to cover security, deployment, resilience, operational readiness, online systems, event/queue, data governance, and supply chain"
    - "All contract expansions profile-gated via M-22/M-23"
  task_references: ["M-27", "M-28", "M-29", "M-30", "M-31", "M-32", "M-33", "M-34"]
  entry_criteria:
    - "PHASE_3 complete: profile system schema-validated"
  exit_criteria:
    - "Each expanded extension contract passes schema validation"
    - "Each new contract is bound to specific system_class + operational_maturity minimums"
    - "No new Core tier, edge type, or invariant introduced"
  assigned_model: "gemini-3-flash-preview"

- phase_id: "PHASE_5_IMPLEMENTATION_BRIDGE"
  objectives:
    - "Add structured preconditions/postconditions to all 8 core operations"
    - "Add a normative runtime_contract section"
    - "Add validation metadata fields to DdrNode"
    - "Define reference validator and conformance corpus requirements"
    - "Define round-trip conformance tests"
  task_references: ["M-35", "M-36", "M-37", "M-38", "M-39"]
  entry_criteria:
    - "PHASE_4 complete: production contracts schema-validated"
  exit_criteria:
    - "Every core operation has machine-parseable preconditions and postconditions"
    - "Runtime contract covers concurrency, persistence, eventing, API, and transaction semantics"
    - "Conformance corpus requirements are documented with exemplar counts"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_6_DOCUMENTATION_AND_ADOPTION"
  objectives:
    - "Expand glossary to cover all undefined terms"
    - "Add profile-aware compliance checklist"
    - "Add quick-start examples to tier definitions"
    - "Add migration contract for v6.3→v7.0"
    - "Add reference generator and starter template requirements"
    - "Resolve meta-governance gaps (project block, mode consistency, inline commentary)"
  task_references: ["M-40", "M-41", "M-42", "M-43", "M-44", "M-45", "M-46", "M-47", "M-48"]
  entry_criteria:
    - "PHASE_5 complete: implementation bridge schema-validated"
  exit_criteria:
    - "Glossary covers all terms used in the specification that lack definitions"
    - "Compliance checklist maps items to profiles"
    - "Migration contract specifies all breaking changes from v6.3 to v7.0"
    - "No issue-specific audit commentary remains in the authority file"
    - "v7.0 YAML pair self-validates as the final deliverable"
  assigned_model: "gemini-3-flash-preview"
</phases>

<atomic_steps>

#### Group 1 — SIL Parent Enforcement and Node Content Mandate (PHASE_1)

- [ ] 1. **SIL parent_ids per-node enforcement.** MODIFY `ddr/ddr_node_schema_v6.3.yaml` → `ddr/ddr_node_schema_v7.0.yaml`: In the `DdrNode.allOf` SIL conditional block (current lines 1548–1555), add `parent_ids: {minItems: 1}` to the `then.properties` alongside the existing `id` pattern constraint. **Intent:** Close the gap where standalone SIL node validation admits orphaned SIL nodes when XPD is contextually active. **Outcome:** Per-node SIL validation rejects nodes with empty `parent_ids`, matching the document-level enforcement already present in the root `allOf`.

- [ ] 2. **Mandate `content` as required.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Move `content` into the `DdrNode.required` array (current line 1420–1427), changing it from `[id, tier, title, status, version, created, modified]` to `[id, tier, title, content, status, version, created, modified]`. **Intent:** Prevent schema-valid nodes from existing as structurally hollow shells that bypass the entire 70+ atomic tier inclusion/exclusion ruleset. **Outcome:** Any `DdrNode` without a `content` field fails schema validation. Cross-reviewer consensus: Gemini recommendation 1, Opus M-05, Codex item 2.

#### Group 2 — Score Band Determinism and Edge Type Cleanup (PHASE_1)

- [ ] 3. **ARE score band boundary determinism.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: In the `ScoringProfile.score_bands` definition (current lines 1193–1215), add schema-level constraints: (a) items must be ordered by ascending `range[0]`; (b) each item's `range[1]` must equal the next item's `range[0]` (contiguous coverage); (c) the first band must begin at `0.0` and the last must end at `1.0`; (d) boundaries follow half-open `[low, high)` convention with the final band closed at `[low, 1.0]`. Add a `boundary_convention` annotation field with const `"half_open_final_closed"` to make the convention machine-explicit. **Intent:** Resolve the AX-3 determinism violation where a score of exactly 0.4 falls in two bands. **Outcome:** Non-conformant scoring profiles fail schema validation.

- [ ] 4. **Remove `extends` from `TierRelationship.edge_type`.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: In the `TierRelationship` definition (current line 885), change the `edge_type` enum from `[derives, constrains, implements, extends]` to `[derives, constrains, implements]`. **Intent:** Core topology fields should not express extension-only semantics; verified that all 22 tier relationships in the system YAML use only `derives`, `constrains`, or `implements`. **Outcome:** Schema rejects `extends` in `parent_relationships` and `child_relationships`.

#### Group 3 — Lifecycle Corrections (PHASE_1)

- [ ] 5. **Add guards to `DEPRECATED → ACTIVE` transition.** MODIFY `ddr/ddr_system_v6.3.yaml` → `ddr/ddr_system_v7.0.yaml`: In the `lifecycle.status_transitions` table, locate the `DEPRECATED → ACTIVE` row (current lines 2684–2687) and append `gc-001` (structural validation) and `gc-005` (review closure) to the existing guard list `[gc-002, gc-003, gc-004]`, yielding `[gc-001, gc-002, gc-003, gc-004, gc-005]`. **Intent:** Close the lifecycle safety gap where a deprecated node can be reactivated without passing structural validation or review closure. **Outcome:** Reactivation of deprecated nodes requires the same vetting as dirty-to-active transitions.

- [ ] 6. **Add `DEPRECATED → DIRTY` transition.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a new row to `lifecycle.status_transitions`: `{from: DEPRECATED, to: DIRTY, operation: MODIFY, side_effect: propagation, guards: []}`. **Intent:** Enable dirty propagation to reach deprecated nodes lawfully when a parent is modified, eliminating the awkward `DEPRECATED → ACTIVE → DIRTY` path. **Outcome:** Deprecated nodes can re-enter the validation workflow via standard dirty propagation.

- [ ] 7. **Add DELETE lifecycle semantics.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: (a) In the node schema, add `DELETED` to `StatusEnum` (current line 1667). (b) Extend `StatusTransition` to permit `to: DELETED` as a terminal state. (c) In the system YAML, add DELETE transition rows for DRAFT, ACTIVE, DIRTY, and DEPRECATED source states, each transitioning `to: DELETED` with appropriate guards (orphan-cascade acknowledgment for ACTIVE/DIRTY; deprecation-first preference for ACTIVE). **Intent:** Close the INV-8 completeness gap where DELETE is modeled as an operation sink with no lifecycle rows. **Outcome:** DELETE has explicit lifecycle semantics; INV-8 is fully satisfied.

#### Group 4 — System Metadata and Guard Extensibility (PHASE_1)

- [ ] 8. **Require `system_metadata` fields.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Add `required: [status, date, scope, authority, lineage, single_source_of_truth]` to the `system_metadata` definition (after current line 235). **Intent:** Prevent a `system_definition` document from carrying empty `system_metadata: {}`. **Outcome:** System-definition documents must declare all essential authority descriptors.

- [ ] 9. **Convert `GuardIdRef` to pattern-based.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Replace the `GuardIdRef` definition (current lines 1669–1671) from `enum: [gc-001, ..., gc-009]` to `type: string, pattern: "^gc-[0-9]{3}$"`. **Intent:** Eliminate schema-breaking changes when adding or retiring guard conditions; guard definitions in the system YAML remain the authoritative registry. **Outcome:** Guard IDs are format-validated, not enum-locked.

#### Group 5 — Citation Freshness and Manifest Typing (PHASE_1)

- [ ] 10. **Add `validated_parent_version` to `ParentCitation`.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: In the `ParentCitation` definition (current lines 1627–1663), add an optional property: `validated_parent_version: {type: string, pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$"}`. Add a description documenting write-once semantics: set on VALIDATE success, cleared on parent MODIFY/SUPERSEDE to trigger DIRTY propagation. **Intent:** Enable mechanical enforcement of CIT-R7 parent-version freshness. **Outcome:** VERIFY can detect stale citations by comparing `validated_parent_version` against the current parent `version`. Cross-reviewer consensus: Gemini recommendation 7, Codex item 3.

- [ ] 11. **Expand reconciliation manifest types.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: (a) In the schema, expand `ManifestItemType.item_type` enum from `[MISSING_MEDIATOR, SUPERSEDE_FAILED, SUPERSEDE_PENDING_DETECTED]` to include `REVIEW_REQUIRED`, `CONFLICT_RESOLUTION`, `OVERRIDE_APPROVAL`, `EXTENSION_ADVISORY`, `DEFERRED_FRAGMENT`. Expand `SemanticGapClassification.allowed_types` to include all applicable types. (b) In the system YAML, add corresponding `manifest_item_types` entries with typed `fields` arrays, descriptions, and appropriate `severity` levels. **Intent:** Close the gap where 5+ manifest interactions described by the specification lack typed entries. **Outcome:** The reconciliation manifest is fully typed; "zero pending items" is mechanically unambiguous.

#### Group 6 — Version History, Topology Requirements, and Rule ID Uniqueness (PHASE_1)

- [ ] 12. **Fix v1.0 date.** MODIFY `ddr/ddr_system_v7.0.yaml`: Change the v1.0 entry's `date` field (current line 2094) from `""` to `"unknown"`. Add a `format_note` or inline comment explaining the date is not recoverable from historical records. **Intent:** Eliminate vacant metadata from the semantic authority's own historical record. **Outcome:** No empty-string date values in `version_history`.

- [ ] 13. **Require topology fields in `TierDefinition`.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: In the `TierDefinition` definition (current line 892), add `parent_relationships` and `child_relationships` to the `required` array. The requirement enforces field presence, not non-empty content (ISL legitimately has `child_relationships: []`). **Intent:** Prevent tier definitions from passing validation without declaring their position in the DAG topology. **Outcome:** All tier definitions must declare both parent and child relationships.

- [ ] 14. **Enforce global rule_id uniqueness.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: (a) In the schema, restrict `ExtensionRuleId` pattern to exclude tier-name prefixes via negative lookahead or naming convention (e.g., require extension prefixes to differ from `[XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]`). (b) In the system YAML, add a `rule_id_uniqueness` invariant or annotation requiring global uniqueness across all rule families (`AtomicTierRuleId`, `BridgeRuleId`, `ExtensionRuleId`, `CitationRuleId`, `InvariantId`). **Intent:** Prevent ambiguous rule references in tooling and logs. **Outcome:** Rule IDs are globally resolvable without tier context.

#### Group 7 — Authority Hierarchy and Complexity Budget (PHASE_2)

- [ ] 15. **Add authority hierarchy section.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a top-level `authority_hierarchy` section declaring: (1) the system YAML is the sole normative semantic authority; (2) the node schema is the sole normative structural authority; (3) all Markdown renderings, crosswalks, and reference tables are derived surfaces with no normative weight; (4) generated surfaces must carry a machine-generated provenance header citing source artifacts and generation timestamp. Add corresponding schema support in `ddr/ddr_node_schema_v7.0.yaml`. **Intent:** Generalize the lifecycle-block precedent (current lines 2623–2626) to eliminate dual-authority ambiguity. **Outcome:** Authority model is machine-explicit; derivative surfaces are formally subordinated.

- [ ] 16. **Codify complexity budget rule.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a new `DesignPrinciple` entry under `system_metadata.design_philosophy`: `{principle: "Enforce Complexity Budget", description: "Every proposed Core addition must retire existing machinery of equal or greater complexity, or demonstrate it closes a defect not addressable by an Extension, profile, or tooling."}`. **Intent:** Create auditable selection pressure against monotonic surface growth. Cross-reviewer consensus: all four review documents. **Outcome:** New Core additions are formally gated by a subtraction rule.

#### Group 8 — Content Validation, Express Mode, and Governance (PHASE_2)

- [ ] 17. **Add content validation contract field.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Add an optional `content_validation_contract` property to `DdrNode` (type: object) with sub-fields: `evaluated_rules` (array of objects: `{rule_id, disposition: pass|fail|review_required}`), `evaluated_at` (ISO 8601), `evaluated_by` (string). **Intent:** Make content compliance auditable without requiring the schema to evaluate prose semantics; the 70+ atomic rules operate outside the schema boundary but their evaluation should be recorded. **Outcome:** Compliance audit trails are machine-parseable.

- [ ] 18. **Declare Express Mode generation contract.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add an `express_mode_generation_contract` annotation within the `express_mode` section declaring that Express Mode group definitions, unbundle rules, and deferred fragment handling are derived from the full tier definitions and must maintain guaranteed round-trip fidelity. **Intent:** Prevent Express Mode from drifting into a parallel manually maintained surface. **Outcome:** Express Mode is formally subordinated to the full model.

- [ ] 19. **Specify UNBUNDLE_EXECUTE behavior with inactive tiers.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add normative text to `unbundle_determinism_rule` specifying: when a constituent tier is inactive (e.g., CL inactive in G2=[FCL, CL]), UNBUNDLE_EXECUTE allocates all group content to remaining active tiers only; no content is invented for inactive tiers; inactive-tier annotations are treated as classification errors with confidence `none`. **Intent:** Close the indeterminate reduced-topology unbundling behavior. **Outcome:** UNBUNDLE_EXECUTE behavior is fully specified for all topology variants.

- [ ] 20. **Add errata governance.** MODIFY `ddr/ddr_system_v7.0.yaml` and `ddr/ddr_node_schema_v7.0.yaml`: Add governance text specifying when errata entries are required (post-release corrections only), retirement procedure (moved to `version_history` on next version increment), and release-blocking status (unresolved errata with severity `BLOCKING` must be resolved before next version finalization). Add optional `severity` field to `ErrataEntry`. **Intent:** Give the errata log operational governance. **Outcome:** Errata lifecycle is deterministic.

- [ ] 21. **Add deprecation and removal policy.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a normative `deprecation_policy` section specifying sunset periods and migration obligations for rules, profiles, extensions, and generated artifacts. Include a `deprecated_artifacts` array tracking items scheduled for removal with their sunset version. Add corresponding schema support. **Intent:** Enable intentional simplification by formalizing the removal mechanism. **Outcome:** The subtraction rule (M-16) has an operational counterpart.

#### Group 9 — Profile System (PHASE_3)

- [ ] 22. **Add `system_class` taxonomy.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: Add a top-level `profiles` section with a `system_class` taxonomy containing at minimum: `script_tool`, `library_sdk`, `batch_job`, `service_api`, `web_app`, `data_pipeline`, `edge_device`, `regulated_system`. Bind each to: minimum required tiers (e.g., `script_tool` → SIL+FCL+CDL+ISL; `regulated_system` → all 9 + XPD), minimum rules, required extensions, evidence gates, and delivery obligations. **Intent:** Enable AX-4 Universality through profile-driven scaling instead of core topology expansion. **Outcome:** Small tools are not over-burdened; enterprise systems cannot under-specify.

- [ ] 23. **Add `operational_maturity` dimension.** MODIFY the `profiles` section: Add an orthogonal `operational_maturity` dimension with levels: `local`, `internal`, `internet_facing`, `high_availability`, `regulated`. Bind each level to explicit gates for observability, security, resilience, rollout, and compliance evidence. **Intent:** Separate scale from operational exposure. **Outcome:** A `script_tool` at `regulated` maturity gets different obligations than a `web_app` at `local`.

- [ ] 24. **Separate validation gates.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add `design_complete` and `production_ready` as distinct validation gates with separate checklist items. `design_complete` = all tiers structurally valid per declared profile; `production_ready` = operational contracts also satisfied per `system_class` + `operational_maturity`. **Intent:** Prevent conflating "spec is finished" with "system is deployable." **Outcome:** Both local tools and enterprise production systems have appropriate completion criteria.

- [ ] 25. **Add hardware-profile schema to CL.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: Add a `hardware_profile_schema` sub-section to CL's `node_schema` defining structured hardware envelope fields: `cpu_class`, `ram_floor_gb`, `storage_class`, `gpu_requirement`, `network_bandwidth_class`, `power_envelope_watts`. **Intent:** Enable HRE (E1) to validate mechanically rather than parsing prose. Essential for edge-device and hardware-constrained use cases. **Outcome:** Hardware declarations are machine-shaped.

- [ ] 26. **Add optional `tags` field to `DdrNode`.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Add `tags: {type: array, items: {type: string}, uniqueItems: true}` as an optional property. **Intent:** Enable cross-concern traceability (e.g., "security", "performance", "accessibility") without new tiers or edges. Tags carry no normative weight and do not participate in VERIFY traversals. **Outcome:** Lightweight cross-cutting categorization is available.

#### Group 10 — Production Contract Expansions (PHASE_4)

- [ ] 27. **Expand security contracts (SCE).** MODIFY `ddr/ddr_system_v7.0.yaml`: Expand SCE's contract scope to cover identity, authentication, authorization, secret management, and key management — structured as profile-gated obligations. **Intent:** Current SCE covers RBAC on ICL contracts only (SCE-R3). Production systems need broader security governance. **Outcome:** SCE rules cover the full security lifecycle, gated by `system_class` + `operational_maturity`.

- [ ] 28. **Expand deployment contracts (DCP).** MODIFY `ddr/ddr_system_v7.0.yaml`: Extend DCP to cover migration sequencing, deployment rollback, compatibility windows, feature flags, canary/blue-green release policies — profile-gated. **Intent:** Current DCP defines minimum pipeline stages only. **Outcome:** Enterprise deployments have explicit rollout/rollback semantics.

- [ ] 29. **Add resilience contracts.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add explicit backup, restore, failover, disaster-recovery, and degraded-operation contracts tied back to GPCL RTO/RPO targets as proof obligations — profile-gated. **Intent:** v6.3 names RTO/RPO targets but does not require operational proof. **Outcome:** Resilience is a machine-checkable obligation for appropriate profiles.

- [ ] 30. **Expand operational readiness (ORE).** MODIFY `ddr/ddr_system_v7.0.yaml`: Expand ORE beyond telemetry points and vendor-agnostic alerts to cover SLIs, SLOs, alert ownership, dashboards, runbooks, and on-call escalation — profile-gated. **Intent:** Current ORE-R3 requires "≥1 telemetry point." Production systems need complete observability contracts. **Outcome:** Observability contracts match production reality.

- [ ] 31. **Add online system contracts.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add first-class rate-limit, timeout, retry, backpressure, and idempotency contracts for online and event-driven systems — profile-gated to `service_api`, `web_app`, and `data_pipeline`. **Intent:** Missing entirely from the current specification. **Outcome:** Online system operational semantics are formally specified.

- [ ] 32. **Add event/queue contracts.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add first-class cache, queue, stream, and event-schema contracts including ordering, replay, dead-letter, and durability semantics — profile-gated. **Intent:** Missing from the current specification; essential for event-driven architectures. **Outcome:** Event infrastructure is governed by typed contracts.

- [ ] 33. **Expand data governance (DDE).** MODIFY `ddr/ddr_system_v7.0.yaml`: Expand DDE beyond residency, retention, and ICL-schema consistency to include classification, privacy, consent, deletion/right-to-erasure, lineage, schema evolution, and backfill/reconciliation — profile-gated. **Intent:** Current DDE covers ER model consistency but not the full data governance lifecycle. **Outcome:** Regulated-sector data obligations are formally specified.

- [ ] 34. **Expand supply chain (DGA).** MODIFY `ddr/ddr_system_v7.0.yaml`: Expand DGA to cover SBOM generation, artifact provenance and signing, dependency update policy, vulnerability response SLA, and license gating — profile-gated. **Intent:** Current DGA covers dependency graph and copyleft analysis only. **Outcome:** Supply-chain governance matches production requirements.

#### Group 11 — Operation Contracts and Runtime Specification (PHASE_5)

- [ ] 35. **Add structured preconditions/postconditions.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: For each of the 8 core operations, add structured `preconditions` (array of machine-evaluable expression objects) and `postconditions` (array of state assertion objects) alongside the existing prose `description` and `validation_trigger` fields. Add corresponding schema definitions for precondition and postcondition types. **Intent:** Make operations implementable without parsing natural language. **Outcome:** Every operation has machine-shaped pre/post contracts.

- [ ] 36. **Add normative `runtime_contract` section.** MODIFY `ddr/ddr_system_v7.0.yaml` and `ddr/ddr_node_schema_v7.0.yaml`: Add a top-level `runtime_contract` section specifying: concurrency model (serialized vs. concurrent operations); persistence model (in-memory, file-backed, database-backed); event/notification model (synchronous propagation vs. queued); API surface contract (function-call, CLI, REST, or language-native); and transaction/rollback semantics. **Intent:** The specification describes 8 atomic operations but provides no runtime execution contract. **Outcome:** Implementers have unambiguous runtime behavior guidance.

- [ ] 37. **Add validation metadata to `DdrNode`.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Add optional fields: `last_validated_by: {type: string, enum: [VALIDATE, VERIFY]}` and `last_validated_at: {type: string, format: date-time}`. **Intent:** Enable mechanical confirmation of graph validation state against a known timestamp. **Outcome:** CLEAN claims are tied to actual evaluation points.

- [ ] 38. **Define reference validator and conformance corpus.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a `conformance_suite` section defining: (a) reference validator requirements (language, input/output contract, error reporting format); (b) golden conformance corpus structure (valid and invalid exemplars for all three document profiles and all lifecycle transitions); (c) release-blocking status: both validator and corpus pass are required for every version increment. **Intent:** Close the gap between "the spec says X" and "a validator enforces X." **Outcome:** Conformance testing is formalized as a release gate.

- [ ] 39. **Define round-trip conformance tests.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add round-trip test requirements for: `project_instance ↔ VALIDATE`, `project_instance_express ↔ UNBUNDLE_SCAN/EXECUTE ↔ project_instance`, and `system_definition ↔ schema self-validation`. **Intent:** Ensure Express Mode maintains round-trip fidelity and self-hosting is machine-verified. **Outcome:** Round-trip invariants are documented and testable.

#### Group 12 — Documentation, Glossary, and Adoption (PHASE_6)

- [ ] 40. **Expand glossary.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add glossary entries for at minimum: `Consumption Mode Profile`, `System Class`, `Operational Maturity`, `Manifest Item`, `Bridge Rule`, `Dirty Classification`, `Guard Condition`, `Content Validation Contract`, `Hardware Envelope`, `Scoring Profile`, `Document Profile`, `Constraint Origin`. **Intent:** Close the gap where 12+ terms used throughout the specification lack definitions. **Outcome:** All normative terms have formal definitions.

- [ ] 41. **Add profile-aware compliance checklist.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a `profile_aware_validation` sub-section to `compliance_checklist` mapping each checklist item to the `system_class` + `operational_maturity` profiles where it applies. **Intent:** Prevent false-negative CLEAN declarations for small projects and under-specification of enterprise systems. **Outcome:** Compliance is profile-calibrated.

- [ ] 42. **Add quick-start examples to tier definitions.** MODIFY `ddr/ddr_system_v7.0.yaml` and `ddr/ddr_node_schema_v7.0.yaml`: Add a `quick_start_example` field (type: string) to each `TierDefinition` containing a concise example of compliant tier content for a representative use case. **Intent:** Bridge the gap between abstract rules and concrete authoring. **Outcome:** Every tier has a concrete content example.

- [ ] 43. **Add v6.3→v7.0 migration contract.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a `migration_contract` section specifying: mandatory field additions for v6.3 → v7.0 upgrades, automated migration rules (field additions, enum expansions, structural renames), manual review requirements, and breaking-change classification. **Intent:** Make version upgrades deterministic for existing DDR instances. **Outcome:** Migration is formally specified.

- [ ] 44. **Add reference generator requirements.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add a `reference_generators` section defining: starter template requirements for the main `system_class` variants, generated Markdown rendering contract, and crosswalk artifact specification. **Intent:** Ensure realistic onboarding paths for all system classes. **Outcome:** Generator requirements are formally captured.

- [ ] 45. **Formalize `project` block under `system_definition`.** MODIFY `ddr/ddr_node_schema_v7.0.yaml` and `ddr/ddr_system_v7.0.yaml`: Add a normative note clarifying the `project` block's role under `system_definition` — either make it explicitly required with documented normative purpose, or clarify it is metadata-only with no enforcement implications. **Intent:** Resolve the role ambiguity where the canonical system YAML uses `project` but the role is undefined. **Outcome:** The `project` block has clear semantics for all document profiles.

- [ ] 46. **Enforce `system_definition` mode consistency.** MODIFY `ddr/ddr_node_schema_v7.0.yaml`: Add a schema conditional ensuring `project.mode: full` is required (or defaulted) when `document_profile: system_definition`, preventing a system-definition artifact from declaring `mode: express`. **Intent:** Close the gap where a `system_definition` with `mode: express` is technically schema-valid. **Outcome:** System-definition documents cannot declare express mode.

- [ ] 47. **Add testing strategy contracts.** MODIFY `ddr/ddr_system_v7.0.yaml`: Add or extend DCP to include a `testing_contract` covering unit, integration, contract, end-to-end, performance, security, resilience, and migration testing requirements — profile-gated with minimum coverage expectations per `system_class` + `operational_maturity`. **Intent:** Current DCP includes "test" as a pipeline stage but defines no test categories or profile-based minimums. **Outcome:** Testing strategy is governed by profile obligations.

- [ ] 48. **Remove issue-specific audit commentary.** MODIFY `ddr/ddr_system_v7.0.yaml`: Remove issue-specific inline comments (e.g., current lines 280–281: "ISSUE-007 Change") and migrate the historical context to `errata_log` entries or `version_history` notes. **Intent:** The authority file should contain only timeless explanatory notes, not version-specific audit residue. **Outcome:** No issue-specific commentary remains in normative comments.

</atomic_steps>

<verification>

1. Parse `ddr/ddr_node_schema_v7.0.yaml` SIL conditional block; confirm `parent_ids: {minItems: 1}` is present. Test: submit a `{tier: SIL, parent_ids: []}` node — must fail validation.
2. Parse `ddr/ddr_node_schema_v7.0.yaml` `DdrNode.required`; confirm `content` is listed. Test: submit a node without `content` — must fail validation.
3. Parse `ScoringProfile.score_bands`; confirm `boundary_convention` field exists. Test: submit overlapping bands `[0.0, 0.5]` and `[0.4, 1.0]` — must fail validation.
4. Parse `TierRelationship.edge_type` enum; confirm `extends` is absent. Test: submit a tier relationship with `edge_type: extends` — must fail.
5. Parse `lifecycle.status_transitions` `DEPRECATED → ACTIVE` row; confirm guards include `gc-001` and `gc-005`.
6. Parse `lifecycle.status_transitions`; confirm a `DEPRECATED → DIRTY` row exists with `operation: MODIFY`.
7. Parse `StatusEnum`; confirm `DELETED` is present. Parse `status_transitions`; confirm DELETE rows exist for DRAFT, ACTIVE, DIRTY, and DEPRECATED.
8. Parse `system_metadata`; confirm `required` array contains `[status, date, scope, authority, lineage, single_source_of_truth]`.
9. Parse `GuardIdRef`; confirm it uses `pattern: "^gc-[0-9]{3}$"` instead of a closed enum. Test: `gc-010` passes; `gc-abc` fails.
10. Parse `ParentCitation`; confirm `validated_parent_version` optional field exists with SemVer pattern.
11. Parse `ManifestItemType.item_type` enum; confirm `REVIEW_REQUIRED`, `CONFLICT_RESOLUTION`, `OVERRIDE_APPROVAL`, `EXTENSION_ADVISORY`, `DEFERRED_FRAGMENT` are present. Parse `SemanticGapClassification.allowed_types`; confirm expansion.
12. Parse `version_history` v1.0 entry; confirm `date` is non-empty.
13. Parse `TierDefinition.required`; confirm `parent_relationships` and `child_relationships` are listed.
14. Parse `ExtensionRuleId` pattern; confirm it excludes tier-name prefixes. Parse system YAML for `rule_id_uniqueness` annotation.
15. Parse system YAML top level; confirm `authority_hierarchy` section exists with all 4 declarations.
16. Parse `system_metadata.design_philosophy`; confirm complexity budget principle is present.
17. Parse `DdrNode`; confirm `content_validation_contract` optional field exists with `evaluated_rules`, `evaluated_at`, `evaluated_by` sub-fields.
18. Parse `express_mode` section; confirm `express_mode_generation_contract` annotation is present.
19. Parse `unbundle_determinism_rule`; confirm inactive-tier allocation behavior is specified.
20. Parse `errata_log` schema description; confirm governance text covers creation, retirement, and release-blocking conditions. Confirm `ErrataEntry` has optional `severity` field.
21. Parse system YAML; confirm `deprecation_policy` section exists with sunset period and `deprecated_artifacts` array definitions.
22. Parse system YAML `profiles` section; confirm `system_class` taxonomy with ≥8 classes, each with minimum required tiers, rules, and extensions.
23. Within `profiles`, confirm `operational_maturity` dimension with ≥5 levels, each with explicit gates.
24. Confirm both `design_complete` and `production_ready` validation gates exist with distinct checklist items.
25. Parse CL `node_schema`; confirm `hardware_profile_schema` with structured fields (`cpu_class`, `ram_floor_gb`, etc.).
26. Parse `DdrNode`; confirm optional `tags` array field with `uniqueItems: true`.
27. Parse SCE extension rules; confirm rules covering identity, authentication, authorization, secret management, key management — each with profile-gate reference.
28. Parse DCP extension rules; confirm rollback, canary/blue-green, feature flag rules with profile-gate references.
29. Parse system YAML; confirm resilience contracts are tied to GPCL RTO/RPO targets with proof obligation language.
30. Parse ORE rules; confirm SLI/SLO/runbook/on-call requirements with profile-gate references.
31. Parse system YAML; confirm online system contracts (rate-limit, timeout, retry, backpressure, idempotency) are present with profile-gate.
32. Parse system YAML; confirm event/queue contracts with ordering, replay, dead-letter, durability semantics.
33. Parse DDE rules; confirm classification, privacy, consent, deletion, lineage, schema evolution coverage.
34. Parse DGA rules; confirm SBOM, provenance, signing, vulnerability response, license gating coverage.
35. Parse `Operation` schema; confirm `preconditions` and `postconditions` array fields exist. Verify all 8 operations in system YAML have structured pre/post entries.
36. Parse system YAML top level; confirm `runtime_contract` section covers concurrency, persistence, eventing, API surface, and transaction semantics.
37. Parse `DdrNode`; confirm `last_validated_by` and `last_validated_at` optional fields.
38. Parse system YAML; confirm `conformance_suite` section with validator requirements, corpus structure, and release-blocking declaration.
39. Parse system YAML; confirm round-trip test requirements for all three document profiles.
40. Parse `glossary`; confirm ≥26 entries (14 existing + 12 new).
41. Parse `compliance_checklist`; confirm `profile_aware_validation` sub-section mapping items to profiles.
42. Parse `TierDefinition` schema; confirm `quick_start_example` field. Verify all 9 tier definitions in system YAML include a non-empty example.
43. Parse system YAML; confirm `migration_contract` section with v6.3→v7.0 field additions, breaking-change classification, and review requirements.
44. Parse system YAML; confirm `reference_generators` section with template and rendering requirements.
45. Parse system YAML or schema; confirm normative note or requirement for `project` under `system_definition`.
46. Test: a `system_definition` document with `project.mode: express` — must fail schema validation.
47. Parse DCP rules; confirm `testing_contract` with test categories and profile-based minimums.
48. Grep `ddr/ddr_system_v7.0.yaml` for `ISSUE-` patterns in comments; confirm zero matches.

**Final integration verification:** Run `jsonschema.validate(ddr_system_v7.0, ddr_node_schema_v7.0)` — must pass with zero errors.

</verification>

<risks_and_mitigations>

- **Risk:** Phase 1 modifications change the `StatusEnum` (adding `DELETED`) and `DdrNode.required` array (adding `content`), which are breaking changes for existing v6.3 project-instance files.
  **Mitigation:** These are captured in the v6.3→v7.0 migration contract (M-43). Phase 6 must complete before any external migration guidance is issued. Projects upgrading from v6.3 must add `content` to all nodes and handle `DELETED` status awareness.

- **Risk:** Expanding `ManifestItemType` (M-11) and `SemanticGapClassification` (M-11) could introduce items that existing manifest implementations do not handle.
  **Mitigation:** New manifest types are additive; existing implementations that do not recognize them will produce schema validation errors, which is the desired failure mode.

- **Risk:** The profile system (M-22/M-23) introduces significant new schema surface area, which contradicts the subtraction-rule spirit (M-16).
  **Mitigation:** Profiles are a scaling mechanism, not a core topology expansion. The complexity budget rule (M-16) applies to tiers, edge types, invariants, and operations — not to the classification system that gates their applicability. Profiles reduce effective complexity for small projects even as they add schema surface.

- **Risk:** Converting `GuardIdRef` from enum to pattern (M-09) relaxes validation strictness; any string matching `^gc-[0-9]{3}$` passes schema validation whether or not a corresponding `GuardDefinition` exists.
  **Mitigation:** Guard definitions in the system YAML remain the authoritative registry. Runtime validators must check guard references against the resolution list. The schema validates format conformance; the system YAML validates semantic existence.

- **Risk:** Adding `DELETED` to `StatusEnum` (M-07) requires updating the `prior_status` enum, the SUPERSEDE_PENDING conditional, and potentially the lifecycle guard references.
  **Mitigation:** `prior_status` restricts to `[ACTIVE, DEPRECATED, DIRTY]` — `DELETED` nodes cannot enter SUPERSEDE_PENDING (they are terminal), so no `prior_status` change is needed. SUPERSEDE_PENDING conditional remains unchanged because DELETED is a terminal state.

- **Risk:** Phase 4 (production contracts) adds significant rule count to extensions, which could be perceived as bloat.
  **Mitigation:** All Phase 4 rules are profile-gated. A `script_tool` at `local` maturity encounters zero additional obligations from Phase 4. The rules activate only for system classes and maturity levels where they are production-relevant.

- **Risk:** Self-hosting property: the v7.0 system YAML must itself validate against the v7.0 node schema, which now has more requirements.
  **Mitigation:** Every Phase exit criterion includes self-validation. The system YAML is updated in lockstep with every schema change to maintain self-hosting validity.

</risks_and_mitigations>
