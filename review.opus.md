# DDR System v6.3 — Observation Report Review

> **Reviewer:** Antigravity (Claude Opus 4.6)
> **Date:** 2026-04-13 (Final Revision)
> **Sources of Truth:** `ddr/ddr_node_schema_v6.3.yaml`, `ddr/ddr_system_v6.3.yaml`
> **Reports Under Review:** `observations.codex.md`, `observations.opus.md`
> **Cross-Reference:** `review.codex.md`

---

## Table of Contents

- [1. Review Methodology](#1-review-methodology)
- [2. Epistemological Framework](#2-epistemological-framework)
- [3. Comparative Assessment of the Observation Reports](#3-comparative-assessment-of-the-observation-reports)
- [4. Feedback on observations.codex.md](#4-feedback-on-observationscodexmd)
- [5. Feedback on observations.opus.md](#5-feedback-on-observationsopusmd)
- [6. Cross-Report Synthesis](#6-cross-report-synthesis)
- [7. Maximally Optimized Atomic Modification List](#7-maximally-optimized-atomic-modification-list)
- [8. Prioritized Implementation Sequence](#8-prioritized-implementation-sequence)

---

## 1. Review Methodology

Both observation reports were evaluated against the two canonical v6.3 YAML files — the system definition (`ddr_system_v6.3.yaml`, 2728 lines, ~126 KB) and the node schema (`ddr_node_schema_v6.3.yaml`, 1672 lines, ~46 KB). The YAML pair validates successfully: the system-definition artifact conforms to its own declared JSON Schema contract. Every factual claim made by each report was cross-referenced against the source-of-truth artifacts. Structural and conceptual recommendations were evaluated for feasibility, risk, and alignment with the DDR's declared axioms and design philosophy.

This revision incorporates validated findings from `review.codex.md`, which independently identified several source-visible contract gaps confirmed against the YAML pair.

---

## 2. Epistemological Framework

For precision, this review distinguishes three classes of claims:

- **Source-verified facts**: directly stated or mechanically confirmable in the v6.3 YAML pair.
- **Source-visible gaps**: omissions, ambiguities, or under-constrained areas directly observable in the v6.3 YAML pair without relying on external documentation or issue trackers.
- **Forward recommendations**: proposed modifications inferred from the SSOT and the stated production-readiness objective; not claims that v6.3 already provides them.

This distinction matters because both observation reports and the prior Codex review occasionally conflate "the spec does not currently say X" with "the spec is broken because X is missing." Some absences are gaps; others are deliberate scope boundaries. Each modification in §7 is tagged with its classification.

---

## 3. Comparative Assessment of the Observation Reports

The two reports arrive at the same diagnosis from opposite therapeutic directions. Understanding this divergence is essential before acting on either.

### 3.1 Concordance

Both reports agree on all of the following:

1. The DDR architecture (9 tiers, 4 edge types, 7 axioms) is **structurally complete and stable**.
2. The primary growth vector since v5 is **schema tightening, not structural expansion**.
3. The **self-hosting property** (the spec is its own DDR artifact) creates recursive governance pressure.
4. The **dual-surface governance** (YAML pair + Markdown rendering) is a permanent synchronization cost.
5. The **Extension complexity firewall** is the system's most important architectural success.
6. The **ARE extension** is approaching complexity levels that strain the Core extension model.
7. **Express Mode** consumes disproportionate specification space relative to its conceptual simplicity.

### 3.2 Divergence

| Dimension | observations.codex.md | observations.opus.md |
| --- | --- | --- |
| **Framing** | The system is *failing* as an application design framework unless radically simplified | The system has reached *conditional equilibrium*; complexity is bounded and decelerating |
| **Recommendation** | Freeze Express Mode as the primary authoring surface; demote 9-tier model to internal/expert mode | Maintain current trajectory; the tightening phase is working |
| **Root cause analysis** | Over-governance and additive-only evolution | Inherent cost of determinism; irreducible |
| **Posture toward complexity** | Complexity is the disease | Complexity is the treatment, and the dose is stabilizing |
| **Actionability** | Provides a 6-phase concrete repair program | Provides risk identification without a concrete remediation plan |

### 3.3 Which Report Is More Accurate?

**Neither report is wrong. Both are incomplete.** The Codex report correctly identifies the symptom (cognitive load on authors) but prescribes a treatment (demoting the 9-tier model) that would violate AX-4 (Universality) and undermine the framework's value for regulated and enterprise use cases. The Opus report correctly identifies the stabilization trend but underestimates the practical barrier the current specification size presents to adoption and offers no concrete path to reduce it.

**The actionable truth lies between them:** the 9-tier model must remain canonical, but the authoring experience must be stratified so that complexity is encountered only when needed. The correct next move — as `review.codex.md` independently concludes — is neither "collapse DDR into Express Mode" nor "declare DDR production-complete." It is to keep the current kernel, close source-visible contract gaps, generate derivative authority surfaces, and add profile-driven production contracts that make operational readiness explicit and scalable.

---

## 4. Feedback on observations.codex.md

### 4.1 Strengths

- **The quantitative signals section is excellent.** Tracking spec line counts and issue-tracker volumes across versions is the right methodology. The observation that issue character shifted from modeling choices to schema-closure defects is precisely correct and verified against the v6.3 source material.
- **The additive-only evolution diagnosis is accurate.** Examining `ddr_system_v6.3.yaml`, I count 8 DAG invariants, 8 core operations, 9 guard definitions, 3 manifest item types, 7 extension integration rules (EXT-R1 through EXT-R7), and a 12-row status transition table — none of which existed in v1. Every one was added to solve a real problem, but none replaced an existing mechanism.
- **The "one true normative source" recommendation is the single highest-leverage suggestion in either report.** The current authority model (see `ddr_system_v6.3.yaml` lines 2623–2626) explicitly acknowledges that the YAML lifecycle block governs over the Markdown §3.8 table. This precedent should be generalized: the YAML pair governs everything; all other surfaces are generated.

### 4.2 Factual Errors and Overstatements

1. **"v6.0 appears largely to relabel and carry forward v5.0 concepts"** — This understates v6.0's contributions. The system definition shows that v6.0 introduced INV-7 (semantic gap governance, line 289), constraint precedence classes (logical/physical distinction, line 1148), `MISSING_MEDIATOR` gap classification (line 1383), and the conflict resolution protocol (line 1357). These are not relabeling; they are semantic completeness mechanisms.

2. **"The least stable DDR idea is the assumption that every nuance must be represented as a first-class normative artifact"** — This is directionally correct but imprecise. Examining the schema, the DDR already practises selective escalation: `verification_mode: semantic` rules explicitly defer to human judgment rather than encoding every nuance as machine-checkable structure. The `REVIEW_REQUIRED` output pathway (see VALIDATE operation, line 1229) and the reconciliation manifest's `pending_items` queue are evidence that the system already distinguishes between structural gates and semantic reviews. The report's recommendation to "keep semantic judgment review-based" therefore describes the current design, not a reform.

3. **"Treat the existing 4-group Express Mode as the primary design-system surface"** — This recommendation conflicts with the DDR's own axioms. AX-4 (Universality) requires that the Core applies to all software systems regardless of domain, scale, or technology. Express Mode groups (G1–G4) are a presentation convenience with fixed tier compositions (see schema lines 803–835). Promoting them to the primary authoring surface would force all DDR instances through a 4-group model that cannot represent the CL activation decision, the SAL merge-node semantics, or the GPCL-FCL-BR1 bridge rule without immediately requiring unbundling. For regulated programs where CL is mandatory and every tier must be independently auditable, Express Mode is not a simplification — it is an obstacle that must be expanded through before useful work begins.

4. **"The v5 issue tracker header reports `open_issues: 1` while the visible registry entries are resolved"** — This is described as "a concrete metadata-synchronization smell." While potentially valid as an observation of the archived file, it is not evidence of a structural flaw in DDR v6.3. The v6.3 source-of-truth files have a clean `errata_log: []` (line 101) with no pending errata, and the lifecycle block is internally consistent with the status transition table.

### 4.3 What the Codex Report Understates

As `review.codex.md` correctly observes, the Codex report understates how much production-relevant design content already exists in v6.3. The specification is not merely "bookkeeping":

- **GPCL** already requires measurable quality thresholds, security requirements, reliability targets, residency, retention, scalability, and accessibility (GPCL-R6 through GPCL-R10).
- **CL** already requires runtime constraints, hardware envelopes, infrastructure ceilings, and deployment topology (CL-R1 through CL-R8).
- **SAL** already requires concurrency rules, data ownership, and resilience boundaries (SAL-R1 through SAL-R5).
- **ICL** already requires machine-parseable contracts, validation rules, error contracts, and versioning (ICL-R1 through ICL-R5).
- The **extension catalog** already includes hardware/resource intelligence (E1), dependency analysis (E2), lifecycle/versioning (E3), observability/runtime (E4), AI inference (E5), security/compliance (E6), data-domain modeling (E7), deployment/CI-CD (E8), and ethics/human-centered design (E9).

This is a substantial cross-scale design vocabulary that the Codex report's "over-governance" framing partially obscures.

### 4.4 Recommendations I Endorse

- **Enforce a subtraction rule for new core changes.** This is the most important governance recommendation. Every v6.x addition passed a necessity test, but no addition was paired with a mechanism retirement. The result is monotonic surface growth. A formal complexity budget requiring a retirement for every addition would create the selection pressure the system needs.

- **Generate derivative surfaces rather than co-maintaining them.** This directly addresses the dominant defect source (schema/spec misalignment) identified by both reports and by the v6.3 issue tracker.

- **Treat metadata drift as a release-blocking defect.** The self-hosting property means that metadata inconsistency is not cosmetic — it is a structural violation of the DDR's own axioms.

### 4.5 Recommendations I Reject

- **"Demote the 9-tier surface to internal normalization or expert mode."** This would bifurcate the DDR into two systems with different authority surfaces, creating exactly the dual-authority drift the report warns against elsewhere. The better answer — as both this review and `review.codex.md` conclude — is to keep the full semantic kernel canonical, freeze it, and make Express Mode a generated or tool-assisted facade with guaranteed round-trip behavior.

---

## 5. Feedback on observations.opus.md

### 5.1 Strengths

- **The phase analysis is the finest structural account of the DDR's evolution I have seen.** The v4 table (§4.3) correctly identifies every major structural addition and its complexity cost. The edge type design consolidation narrative (6 → 4 with `derivation_mode` recovery in v5) is verified against the source material and accurately describes the within-version consolidation that the Codex report partially mischaracterizes.

- **The "Complexity Paradox" framing (§5.3) is the most useful conceptual contribution in either report.** The stepped example showing how a single edge type's specification grew from one sentence to a multi-field contract with conditional semantics, backward-compatibility defaults, and cross-referenced citation constraints is precisely right. This is verified: `ParentCitation` in the schema (lines 1627–1663) has `id`, `edge_type`, `derivation_mode` (conditional on `edge_type: derives`), backward-compatibility notes in `node_schema_fields` (line 203), and cross-references to CIT-R2 and CIT-R6. That is indeed an order of magnitude more specification for the same concept.

- **The "Zero structural issues in the last four audit cycles" metric (§7.1) is the single most important datum in either report.** It concretely demonstrates that the architecture is finished and only enforcement is catching up.

- **The Stabilization Evidence section (§7) is methodologically rigorous and directly verified against source material.** Tier count, axiom stability, extension non-contamination, and specification growth rate deceleration are all confirmed by the v6.3 YAML artifacts.

### 5.2 Where the Opus Report Is Too Optimistic

As `review.codex.md` correctly observes, this report treats architectural stabilization too closely as a proxy for production readiness. A schema-valid system is not the same as a deployment-ready framework with clear production obligations.

The v6.3 YAML pair still exposes multiple source-visible contract gaps that neither the Opus report nor my original review fully catalogued:

1. **SIL parent_ids enforcement gap.** When `active_tiers` contains `XPD`, the *document-level* allOf (schema lines 78–95) enforces `SIL.parent_ids.minItems: 1`. But the *per-node* SIL conditional (schema lines 1548–1555) does not enforce `minItems: 1` — it only constrains the `id` pattern. This means standalone node validation (without document-level `active_tiers` context) can admit orphaned SIL nodes when XPD is active, creating a schema/specification semantic mismatch.

2. **DEPRECATED → ACTIVE guard weakness.** The `DIRTY → ACTIVE` transition requires guards `[gc-001, gc-005, gc-006]` (structural rules pass, review items resolved, validation scope confirmed). The `DEPRECATED → ACTIVE` transition requires only `[gc-002, gc-003, gc-004]` (deprecation rationale documented, sunset date cleared, status reversal logged). This means a deprecated node can be reactivated *without passing structural validation or review closure* — a genuine lifecycle safety gap.

3. **Missing DEPRECATED → DIRTY transition.** If a parent of a DEPRECATED node is modified, dirty propagation should set descendants DIRTY. But the lifecycle `status_transitions` table contains no `DEPRECATED → DIRTY` row. DEPRECATED nodes cannot lawfully re-enter the validation workflow via dirty propagation, forcing them into an awkward `DEPRECATED → ACTIVE → DIRTY` path that requires reactivation before re-validation.

4. **`system_metadata` has no required fields.** The schema (lines 232–258) defines `system_metadata` as a typed object with named properties (`status`, `date`, `scope`, `authority`, `lineage`, etc.) but no `required` key. A `system_definition` document can carry an empty `system_metadata: {}` and pass schema validation, even though every property is semantically essential for a normative specification.

5. **UNBUNDLE_EXECUTE behavior with inactive tiers is unspecified.** Express Mode group G2 contains `[FCL, CL]`. When CL is inactive, UNBUNDLE_EXECUTE must allocate G2 content to FCL only. But neither the system YAML's `unbundle_determinism_rule` (lines 384–396) nor the UNBUNDLE_EXECUTE operation description specifies this behavior explicitly, leaving reduced-topology unbundling indeterminate.

6. **`TierDefinition` topology fields are not required.** The schema (lines 890–972) lists `parent_relationships` and `child_relationships` as optional properties. A tier definition can pass validation without declaring its structural position in the DAG, breaking the topology completeness guarantee.

7. **`errata_log` has no operational governance.** The schema defines the `errata_log` structure (lines 222–228) and the system YAML carries `errata_log: []` (line 101), but no normative text governs when entries are required, how they are retired, or whether unresolved errata are release-blocking.

### 5.3 Factual Notes

1. **"9 lifecycle guards" (§3 table, Lifecycle Guards row, v6.3 column)** — Confirmed correct: `guard_definitions` in the system YAML contains exactly 9 entries (gc-001 through gc-009).

2. **"~170KB" combined spec size** — The actual combined size of the v6.3 YAML pair is approximately 172 KB (125,586 + 46,178 bytes), so this estimate is accurate.

3. **"No future version should need to add tiers, edge types, or fundamental operations. The structural design is complete." (§9.1)** — This is stated too categorically. The system definition's own `extension_catalog` (9 extensions, E1–E9) is fixed by convention, not by invariant. There is no DAG invariant or schema constraint preventing a 10th extension. More importantly, the `SemanticGapClassification.allowed_types` (schema line 1046) is currently restricted to `enum: [MISSING_MEDIATOR]`. If new gap types are needed (and the GPCL→SAL indirect dependency pattern suggests they will be), the "structural design is complete" claim will require revision. The claim should be qualified as: the *topology and edge vocabulary* are complete; the *governance vocabulary* may still evolve.

4. **The report does not identify any concrete modifications.** For a document titled "Observations," this is acceptable. But the absence of an actionable remediation plan is a significant gap when measured against the Codex report's 6-phase program.

### 5.4 Insights Unique to This Report

- **The self-hosting recursion risk** (§6) is identified exclusively by this report and is the most structurally important long-term risk. The observation that "each specification change must also be a valid schema change" is precisely correct: the `ddr_system_v6.3.yaml` file is itself validated against `ddr_node_schema_v6.3.yaml`, which it defines. This circularity is elegant but creates an engineering constraint that neither report fully resolves.

- **The "specification growth rate deceleration" metric** (§7.5) showing monotonically declining growth (10× → 25% → 20% → 15%) is the strongest quantitative evidence for convergence in either report.

---

## 6. Cross-Report Synthesis

### 6.1 Where Both Reports Should Have Gone Deeper

1. **The `content` field problem.** The DDR node schema defines `content` as `type: string` (schema line 1487) with no structural constraints beyond "tier-level atomic inclusion/exclusion rules are enforced at runtime, not by this schema." Furthermore, `content` is not in the `required` array of `DdrNode` — a schema-valid node can exist with no content at all. This means the entire tier-level compliance apparatus — the 70+ atomic inclusion and exclusion rules distributed across 9 tier definitions — operates outside the schema boundary. The schema can validate that a node *exists* with the right shape, but it cannot validate that the node's *content* satisfies its tier's rules or even that content exists. Neither report identifies this as the single largest unenforceable surface in the DDR.

2. **The DELETE operation is under-specified.** The system YAML defines DELETE as "Remove node; cascade orphan detection to children" (line 1188) but the lifecycle `status_transitions` table (lines 2628–2688) contains no row with operation `DELETE`. DELETE is modeled as an "operation sink" (per the v6.2 version history, line 2148), but neither report examines the implications: a DELETEd node has no final status, no transition guard, and no rollback mechanism. This is a genuine lifecycle gap.

3. **Guard ID rigidity.** The schema types `GuardIdRef` as a fixed enum: `[gc-001, gc-002, gc-003, gc-004, gc-005, gc-006, gc-007, gc-008, gc-009]` (schema lines 1669–1671). This is a closed-world assumption that makes adding a new guard condition a schema-breaking change requiring a version increment.

4. **The score band boundary ambiguity.** Both scoring profiles (`standard_v1` and `conservative_v1`) define score bands with boundary values like `[0.0, 0.4]` and `[0.4, 0.7]`. The schema validates that each range element is a number between 0 and 1 (schema lines 1203–1211), but there is no constraint enforcing non-overlap, ordering, or boundary exclusivity. A score of exactly 0.4 is valid in both the "speculative" band `[0.0, 0.4]` and the "probable" band `[0.4, 0.7]`. This is exactly the kind of determinism gap that AX-3 was written to prevent.

5. **Global rule_id uniqueness is not enforced.** The schema defines separate patterns for `AtomicTierRuleId`, `BridgeRuleId`, `ExtensionRuleId`, `CitationRuleId`, and `InvariantId` — but there is no cross-family uniqueness requirement. A string like `GPCL-R1` is valid under both `AtomicTierRuleId` and `ExtensionRuleId`. While the enum-based `AtomicTierRuleId` pattern prevents collision in practice, the absence of a formal uniqueness invariant means rule references in tooling, logs, and advisory outputs cannot be resolved unambiguously without tier context.

6. **The `project` block role under `system_definition` is ambiguous.** The schema permits `project` on all document profiles, and the canonical `ddr_system_v6.3.yaml` includes `project: {name: "DDR System v6.3 Semantic Authority", created: "2026-02-26", mode: full}` (lines 14–17). But it is unclear whether this block carries normative weight for system-definition documents, whether it is required, or whether its `mode` field has enforcement implications for a system-definition artifact that is inherently full-mode.

### 6.2 The Central Question Neither Report Answers

**Can the DDR System v6.3 actually be implemented as described?**

Both reports evaluate the specification as a specification. Neither evaluates it as an implementation blueprint. The ISL-8.1 node (system YAML lines 2500–2621) provides a Python scaffold, but it is a ~122-line stub with `...` bodies. The specification describes 8 atomic operations with complex pre/post-conditions, a 12-row status transition table with 9 guards, a 3-step SUPERSEDE atomicity protocol with rollback semantics, an UNBUNDLE two-phase protocol with deferred fragment handling, and 9 extensions with independent contracts — all of which must be implemented in a runtime that handles concurrent mutations, maintains a reconciliation manifest, and supports the full lifecycle state machine.

The gap between specification and implementability is not a flaw in either report — it is a flaw in the DDR's own self-assessment. The specification claims to be "production-ready" (system metadata status: `Finalized`), but the distance from finalized specification to working runtime is substantial. The modification list below addresses this gap directly.

### 6.3 Insights Not Surfaced by Either Observation Report

#### 6.3.1 The Extension System Has an Identity Crisis

The 9 extensions in the catalog fall into three distinct categories that the current model does not distinguish:

| Category | Extensions | Characteristic |
| --- | --- | --- |
| **Analytical overlays** | HRE (E1), DGA (E2), ORE (E4), SCE (E6), EHD (E9) | Pure read-only analysis; produce advisories or external artifacts |
| **Data model extensions** | DDE (E7) | Reads FCL+GPCL+SAL+ICL+CDL, validates ER model consistency; performs data-domain governance |
| **Inference engines** | ARE (E5) | Creates candidate nodes, manages a stateful pool, has a tri-state lifecycle with checkpoint persistence |
| **Tooling integrations** | LVE (E3), DCP (E8) | Map DDR artifacts to external systems (VCS, CI/CD) |

The Extension System (§8) treats all 9 uniformly under the "read-only overlay" model. But ARE's Candidate Pool is not a read-only overlay — it is a stateful staging area with its own lifecycle, persistence contract, and promotion mechanism. The `extension_system.candidate_pool` block (system YAML lines 1439–1536) is specific to ARE but lives in the generic Extension System section, creating a structural coupling that conflicts with the "orthogonal overlay" architecture description.

#### 6.3.2 The Reconciliation Manifest Is Under-Typed

The manifest schema (system YAML lines 1381–1420) defines only 3 `manifest_item_types`: `MISSING_MEDIATOR`, `SUPERSEDE_FAILED`, and `SUPERSEDE_PENDING_DETECTED`. But the specification describes at least 5 additional manifest interactions:

1. VALIDATE emits `REVIEW_REQUIRED` items to `pending_items` (line 1234)
2. VERIFY emits `REVIEW_REQUIRED` items for semantic consistency (line 1225)
3. Conflict resolutions must be recorded in the manifest (line 1364)
4. Extension advisories are tracked in the manifest (line 1380)
5. Override approvals for below-threshold ARE candidates must be recorded (line 1529)

None of these have typed `manifest_item_types` entries. This means the reconciliation manifest — which the compliance checklist requires to show "zero pending items" for CLEAN status (line 1971) — has a machine-typed subset and an untyped superset, violating the schema's own closure aspiration.

#### 6.3.3 The CIT-R7 Freshness Rule Has No Enforcement Mechanism

CIT-R7 (system YAML line 345) states: "A child node may remain ACTIVE only while each cited parent remains at the version last validated against." But the node schema has no field to record the parent version that was validated against. The `ParentCitation` object (schema lines 1627–1663) has `id`, `edge_type`, and `derivation_mode` — no `validated_parent_version` field. Without this field, CIT-R7 is an unenforceable aspiration: VERIFY cannot mechanically detect stale parent citations because there is no recorded baseline version to compare against.

#### 6.3.4 Missing Operational Completeness

As `review.codex.md` correctly identifies, the SSOT does not currently define explicit contracts for several concerns that matter in production systems. These are not Core structural gaps — they are scope gaps that must be addressed via extensions, profiles, or adjacent contracts:

- Secrets and key management beyond the current ICL RBAC requirement
- Authentication/session architecture
- Multi-tenancy and tenant isolation strategy
- Deployment rollback, canary, and blue-green policies beyond DCP's current minimum pipeline
- Backup, restore, and disaster recovery beyond GPCL's RTO/RPO targets
- Runbooks and on-call ownership beyond ORE's telemetry point requirement
- Rate limits, idempotency, retry, and backpressure for online systems
- Event-driven and queue-based system semantics
- SBOM, artifact provenance, and supply-chain controls beyond DGA's dependency graph
- Profile-driven obligation scaling by system class

The architecture may be stable, but the framework is not yet production-complete for the full range of stated use cases.

---

## 7. Maximally Optimized Atomic Modification List

The following modifications are organized by priority and designed to move DDR v6.3 from "finalized specification" to "production-ready implementation blueprint" suitable for use cases ranging from custom scripts and developer tools to enterprise-scale online applications with hardware considerations.

Each modification is atomic: it can be applied independently without requiring other modifications as prerequisites, unless explicitly noted. Each is tagged with its classification per §2.

### Tier 1 — Release-Blocking v6.3 Corrections (Source-Visible Gaps)

These close genuine contract gaps directly observable in the v6.3 YAML pair.

| # | Target | Modification | Rationale |
| --- | --- | --- | --- |
| M-01 | `DdrNode` SIL conditional | Add `parent_ids: {minItems: 1}` to the per-node SIL conditional (schema lines 1548–1555) so that standalone node validation enforces parent citation when XPD is contextually active. | Currently, SIL parent_ids enforcement depends on the document-level `active_tiers` allOf (lines 78–95), which is invisible to per-node validators. Per-node validation of SIL nodes can silently admit orphans. |
| M-02 | `ScoringProfile.score_bands` | Add schema-level constraints: (a) `score_bands` items ordered by ascending `range[0]`; (b) each `range[1]` equals next band's `range[0]` (contiguous coverage); (c) first band begins at `0.0`, last ends at `1.0`; (d) boundaries follow half-open `[low, high)` with final band closed `[low, 1.0]`. | A score of exactly 0.4 currently falls in two bands. AX-3 requires deterministic assignment. |
| M-03 | `TierRelationship.edge_type` | Remove `extends` from the enum (schema line 885). | No tier relationship in the system YAML uses `extends`. The edge type is Extension-to-Core only (§3.2), stored in `extension_annotations`, never in `parent_relationships`/`child_relationships`. |
| M-04 | `lifecycle.status_transitions` | Add `DEPRECATED → ACTIVE` guards: append `gc-001` and `gc-005` to the existing guard list `[gc-002, gc-003, gc-004]`. | Currently, `DEPRECATED → ACTIVE` does not require structural validation (gc-001) or review closure (gc-005). A deprecated node can be reactivated without passing the same gates required for `DIRTY → ACTIVE`. |
| M-05 | `DdrNode.content` | Move `content` from optional to `required` in the `DdrNode` schema (line 1420). | A schema-valid node with no content is structurally hollow. Every tier's atomic inclusion rules presuppose content exists. An empty-content node should fail `VALIDATE`, but currently it passes schema validation silently. |
| M-06 | `lifecycle.status_transitions` | Add a `DEPRECATED → DIRTY` transition row: `{from: DEPRECATED, to: DIRTY, operation: MODIFY, side_effect: propagation, guards: []}`. | Dirty propagation from a parent MODIFY must be able to set DEPRECATED descendants DIRTY. Without this row, dirty propagation hitting a DEPRECATED node has no lawful path. |
| M-07 | `lifecycle.status_transitions` | Add `DELETE` transition rows for DRAFT, ACTIVE, DIRTY, and DEPRECATED, each with `to: null` (terminal sink) and appropriate guards. | DELETE is the only core operation without lifecycle rows. INV-8 requires every non-terminal status to have at least one valid outbound transition, but DELETE's removal semantics are not lifecycle-modeled. |
| M-08 | `system_metadata` | Add `required: [status, date, scope, authority, lineage, single_source_of_truth]` to the schema definition (after line 235). | A `system_definition` document can currently carry `system_metadata: {}` and pass validation. Every listed field is semantically essential for a normative specification artifact. |
| M-09 | `GuardIdRef` ($defs) | Convert from `enum: [gc-001, ..., gc-009]` to `type: string, pattern: "^gc-[0-9]{3}$"`. | Eliminates schema-breaking changes when adding guard conditions. Guard definitions in the system YAML remain the authoritative registry; the schema validates format conformance. |
| M-10 | `ParentCitation` ($defs) | Add `validated_parent_version: {type: string, pattern: semver}` optional field. | Enables enforcement of CIT-R7 (parent-version freshness). Without this, VERIFY cannot detect stale citations. Write-once: set on VALIDATE success, cleared on parent MODIFY/SUPERSEDE. |
| M-11 | `SemanticGapClassification.allowed_types` | Expand from `[MISSING_MEDIATOR]` to include `REVIEW_REQUIRED`, `CONFLICT_RESOLUTION`, `OVERRIDE_APPROVAL`, `EXTENSION_ADVISORY`. Add corresponding `manifest_item_types` entries with required fields. | The reconciliation manifest is referenced by 5+ mechanisms that produce items not covered by the current 3 typed entries. Typing them makes "zero pending items" mechanically unambiguous. |
| M-12 | Version history | Set the v1.0 entry's `date` field to a non-empty value (system YAML line 2094). | An empty date in the semantic authority violates the specification's own completeness standards. |
| M-13 | `TierDefinition` | Add `parent_relationships` and `child_relationships` to the `required` array (schema line 892). | A tier definition can currently pass validation without declaring its position in the DAG topology. |
| M-14 | `ExtensionRuleId` / global uniqueness | Add a disambiguating convention to prevent `ExtensionRuleId` pattern overlap with `AtomicTierRuleId`. Options: (a) negative lookahead excluding tier name prefixes, or (b) naming convention requiring exactly 3-letter extension prefixes (current extensions already comply). Add a `rule_id_uniqueness` invariant to the system YAML requiring global uniqueness across all rule families. | `GPCL-R1` is valid under both patterns. Without global uniqueness, tooling cannot resolve rule references without tier context. |

### Tier 2 — Governance and Authority Hardening (Source-Verified + Forward)

These reduce maintenance burden and prevent governance drift.

| # | Target | Modification | Rationale |
| --- | --- | --- | --- |
| M-15 | Authority model (meta-level) | Add a top-level `authority_hierarchy` section declaring: (1) the system YAML is the sole normative semantic authority; (2) the node schema is the sole normative structural authority; (3) all Markdown renderings, crosswalks, and reference tables are *derived* surfaces with no normative weight. | Currently, only the lifecycle block (lines 2623–2626) declares this precedence. Generalizing eliminates the dual-authority ambiguity both reports identify. |
| M-16 | Complexity budget rule | Add a design philosophy principle: "Every proposed Core addition must retire existing machinery of equal or greater complexity, or demonstrate it closes a defect not addressable by an Extension or profile." | Codifies the subtraction rule. Makes the "no new tiers, no new edge types" policy auditable. |
| M-17 | `node_schema_fields` | Add a `content_validation_contract` field to `DdrNode` (type: object, optional) declaring which atomic rule IDs have been evaluated and their pass/fail/review_required disposition. | The `content` field is unvalidated at the schema level. Recording evaluation disposition makes compliance auditable without requiring the schema to evaluate prose semantics. |
| M-18 | Express Mode | Make Express Mode a generated or tool-assisted facade: add an `express_mode_generation_contract` section or annotation declaring that Express Mode group definitions, unbundle rules, and deferred fragment handling are derived from the full tier definitions and must maintain guaranteed round-trip fidelity. | Eliminates the risk of Express Mode drifting into a parallel manually maintained surface. |
| M-19 | Express Mode / inactive tiers | Add normative text to `unbundle_determinism_rule` specifying: when a constituent tier is inactive, UNBUNDLE_EXECUTE allocates all group content to remaining active tiers only; no content invention for inactive tiers. | G2 = `[FCL, CL]`. When CL is inactive, UNBUNDLE_EXECUTE behavior is currently unspecified. |
| M-20 | `errata_log` | Add governance text: when entries are required (post-release corrections only), retirement procedure (moved to `version_history` on next version increment), release-blocking status (unresolved errata with severity BLOCKING must be resolved before next version finalization). | The errata log structure exists but has no operational governance. |
| M-21 | Deprecation/removal policy | Add a normative deprecation-and-removal policy for rules, profiles, extensions, and generated artifacts specifying sunset periods and migration obligations. | Simplification cannot happen intentionally without a formal removal mechanism. |

### Tier 3 — Expressiveness and Scalability (Forward Recommendations)

These extend the DDR's reach across the full project-scale spectrum without adding structural complexity.

| # | Target | Modification | Rationale |
| --- | --- | --- | --- |
| M-22 | `profiles` section | Add a `system_class` taxonomy: `script_tool`, `library_sdk`, `batch_job`, `service_api`, `web_app`, `data_pipeline`, `edge_device`, `regulated_system`. Bind each to minimum required tiers, rules, extensions, evidence, and delivery obligations. | Small tools should not be over-burdened; enterprise systems cannot under-specify themselves. AX-4 (Universality) is preserved because the full model remains canonical; profiles select subsets. |
| M-23 | `profiles` section | Add an orthogonal `operational_maturity` dimension: `local`, `internal`, `internet_facing`, `high_availability`, `regulated`. Bind each level to explicit gates for observability, security, resilience, rollout, and compliance evidence. | Separates scale from operational exposure. A `script_tool` at `regulated` maturity gets different obligations than a `web_app` at `local`. |
| M-24 | Validation gates | Separate `design_complete` from `production_ready` as distinct validation gates. `design_complete` means all tiers are structurally valid; `production_ready` means operational contracts are also satisfied per the declared `system_class` + `operational_maturity` profile. | Prevents conflating "spec is finished" with "system is deployable." Supports both small local tools and enterprise production systems without flattening them. |
| M-25 | `tier_definitions[CL]` | Add a `hardware_profile_schema` sub-section to CL's `node_schema` defining structured hardware envelope fields: `cpu_class`, `ram_floor_gb`, `storage_class`, `gpu_requirement`, `network_bandwidth_class`. | CL-R6 requires hardware envelopes but gives no schema guidance. Structured fields enable HRE (E1) to validate mechanically rather than parsing prose. |
| M-26 | `DdrNode` | Add `tags: {type: array, items: {type: string}, uniqueItems: true}` as an optional field. | Enables cross-concern traceability without new tiers or edges. Tags carry no normative weight and do not participate in VERIFY traversals. |

### Tier 4 — Production Contract Completions (Forward Recommendations)

These address the operational completeness gaps identified by `review.codex.md` without expanding the Core.

| # | Target | Modification | Rationale |
| --- | --- | --- | --- |
| M-27 | Security contracts (SCE) | Expand SCE's contract scope to cover identity, authentication, authorization, secret management, and key management — structured as profile-gated obligations (not required for `script_tool` at `local` maturity, mandatory for `service_api` at `internet_facing`+). | Current SCE covers RBAC on ICL contracts only. Production systems need broader security governance. |
| M-28 | Deployment contracts (DCP) | Extend DCP to cover migration sequencing, deployment rollback, compatibility windows, feature flags, canary/blue-green release policies — profile-gated. | Current DCP defines minimum lint/test/build/deploy pipeline stages. Enterprise deployments require explicit rollout/rollback semantics. |
| M-29 | Resilience contracts (ORE/GPCL) | Add explicit backup, restore, failover, disaster-recovery, and degraded-operation contracts tied back to GPCL RTO/RPO targets as proof obligations, not just naming the targets. | v6.3 names RTO/RPO targets (GPCL-R7) but does not require operational proof that they can be met. |
| M-30 | Operational readiness (ORE) | Expand ORE beyond telemetry points and vendor-agnostic alerts to cover SLIs, SLOs, alert ownership, dashboards, runbooks, and on-call escalation — profile-gated. | Current ORE-R3 requires "≥1 telemetry point." Production systems need complete observability contracts. |
| M-31 | Online system contracts | Add first-class rate-limit, timeout, retry, backpressure, and idempotency contracts for online and event-driven systems — profile-gated to `service_api`, `web_app`, and `data_pipeline` system classes. | These are missing entirely from the current specification and extension catalog. |
| M-32 | Event/queue contracts | Add first-class cache, queue, stream, and event-schema contracts including ordering, replay, dead-letter, and durability semantics — profile-gated. | Missing from the current specification; essential for event-driven architectures. |
| M-33 | Data governance (DDE) | Expand DDE beyond residency, retention, and ICL-schema consistency to include classification, privacy, consent, deletion, lineage, schema evolution, and backfill/reconciliation — profile-gated. | Current DDE covers ER model consistency but not the full data governance lifecycle required by regulated systems. |
| M-34 | Supply chain (DGA) | Expand DGA to cover SBOM generation, artifact provenance, signing, dependency update policy, vulnerability response SLA, and license gating — profile-gated. | Current DGA covers dependency graph and copyleft analysis only. Production supply-chain governance is broader. |

### Tier 5 — Implementation Readiness (Forward Recommendations)

These close the gap between finalized specification and implementable runtime.

| # | Target | Modification | Rationale |
| --- | --- | --- | --- |
| M-35 | `operations.core_operations` | For each operation, add structured `preconditions` and `postconditions` arrays with machine-evaluable expressions. | Operation semantics are currently embedded in prose `description` and `validation_trigger` fields. Structured contracts make operations implementable without parsing natural language. |
| M-36 | Top-level | Add a `runtime_contract` section specifying: concurrency model, persistence model, event model, and API surface. | The specification describes 8 atomic operations but provides no runtime execution contract. Implementers cannot determine whether DIRTY propagation is synchronous or queued. |
| M-37 | `DdrNode` | Add `last_validated_by: {type: string, enum: [VALIDATE, VERIFY]}` and `last_validated_at: {format: date-time}` optional fields. | Without validation timestamps, "zero pending items" cannot be mechanically confirmed against a known graph state. |
| M-38 | Top-level | Publish a reference validator plus a golden conformance corpus (valid and invalid exemplars for all three document profiles and all lifecycle transitions). Make both release-blocking for every version increment. | Closes the gap between "the spec says X" and "a validator enforces X." |
| M-39 | Top-level | Add round-trip conformance tests for: `project_instance ↔ VALIDATE`, `project_instance_express ↔ UNBUNDLE_SCAN/EXECUTE ↔ project_instance`, and `system_definition ↔ schema self-validation`. | Ensures that Express Mode maintains round-trip fidelity and that the self-hosting property is machine-verified, not assumed. |

### Tier 6 — Documentation and Adoption (Forward Recommendations)

These improve usability without changing semantics.

| # | Target | Modification | Rationale |
| --- | --- | --- | --- |
| M-40 | `glossary` | Add entries for: `Consumption Mode Profile`, `System Class`, `Operational Maturity`, `Manifest Item`, `Bridge Rule`, `Dirty Classification`, `Guard Condition`, `Content Validation Contract`, `Hardware Envelope`, `Scoring Profile`, `Document Profile`, `Constraint Origin`. | The glossary currently has 14 entries. At least 12 terms used throughout the specification have no definitions. |
| M-41 | `compliance_checklist` | Add a `profile_aware_validation` sub-section that maps each of the 32 checklist items to the `system_class` + `operational_maturity` profiles where it applies. | Prevents false-negative CLEAN declarations for small projects and under-specification of enterprise systems. |
| M-42 | `tier_definitions` | Add a `quick_start_example` field (type: string) to each `TierDefinition` containing a 3–5 sentence example of compliant tier content. | Tier rules describe *what* content must contain but never show *what compliant content looks like*. The gap between abstract rules and concrete authoring is the primary adoption barrier. |
| M-43 | Top-level | Add a `migration_contract` section specifying: mandatory fields for v6.2 → v6.3 upgrades, automated migration rules, and manual review requirements. | Enterprise deployments with hundreds of nodes cannot manually audit every field addition. Formal migration contracts make version upgrades deterministic. |
| M-44 | Top-level | Add reference generators and starter templates for the main `system_class` variants so scripts, libraries, and small tools can adopt DDR without manual tier-by-tier boilerplate. | Addresses the Codex report's legitimate cognitive-load concern through tooling rather than spec reduction. |

---

## 8. Prioritized Implementation Sequence

If the goal is maximum leverage with minimum destabilization:

| Phase | Items | Effect |
| --- | --- | --- |
| **Phase 1: Contract Gap Closure** | M-01 through M-14 | Closes all source-visible v6.3 contract gaps. No new concepts; pure defect remediation. |
| **Phase 2: Authority Hardening** | M-15 through M-21 | Freezes the kernel, establishes generated surfaces, prevents governance drift. |
| **Phase 3: Profile System** | M-22 through M-24 | Adds `system_class` and `operational_maturity` dimensions. Makes scaling explicit. |
| **Phase 4: Production Contracts** | M-25 through M-34 | Fills operational gaps through extension scope expansion and profile-gated obligations. No Core tier changes. |
| **Phase 5: Implementation Bridge** | M-35 through M-39 | Provides structured operation contracts, runtime specification, and conformance tooling. |
| **Phase 6: Adoption** | M-40 through M-44 | Documentation, templates, generators, and migration contracts for onboarding. |

---

> **Summary:** 44 atomic modifications organized in 6 tiers. Tier 1 (M-01 through M-14) closes all source-visible contract gaps in the v6.3 YAML pair — these are release-blocking corrections. Tier 2 (M-15 through M-21) hardens governance and freezes the kernel. Tier 3 (M-22 through M-24) adds profile-driven scaling without Core expansion. Tier 4 (M-25 through M-34) fills production contract gaps through extension scope expansion and profile-gated obligations. Tier 5 (M-35 through M-39) bridges specification to implementation. Tier 6 (M-40 through M-44) accelerates adoption.
>
> **Applied together, these modifications transform DDR v6.3 from a finalized specification into a production-ready application design framework capable of governing projects from single-file developer tools to multi-region enterprise platforms with hardware-aware constraint management and profile-driven operational readiness.**
