# DDR System v6.3 — Observation Report Review

> **Reviewer:** Antigravity (Claude Opus 4.6)
> **Date:** 2026-04-13 (Final Revision)
> **Sources of Truth:** `ddr/ddr_node_schema_v6.3.yaml` (1672 lines, ~46 KB), `ddr/ddr_system_v6.3.yaml` (2728 lines, ~126 KB)
> **Reports Under Review:** `observations.codex.md`, `observations.opus.md`
> **Cross-Reference:** `review.codex.md`, `review.gemini.md`

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

This revision incorporates validated findings from `review.codex.md` and `review.gemini.md`, both of which independently identified source-visible contract gaps confirmed against the YAML pair. Where any review proposes modifications, each has been evaluated against the SSOT for factual accuracy, architectural alignment, and production-readiness impact before acceptance, qualification, or rejection.

---

## 2. Epistemological Framework

For precision, this review distinguishes three classes of claims:

- **Source-verified facts**: directly stated or mechanically confirmable in the v6.3 YAML pair.
- **Source-visible gaps**: omissions, ambiguities, or under-constrained areas directly observable in the v6.3 YAML pair without relying on external documentation or issue trackers.
- **Forward recommendations**: proposed modifications inferred from the SSOT and the stated production-readiness objective; not claims that v6.3 already provides them.

This distinction matters because both observation reports and the prior reviews occasionally conflate "the spec does not currently say X" with "the spec is broken because X is missing." Some absences are gaps; others are deliberate scope boundaries. Each modification in §7 is tagged with its classification.

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

**Neither report is wrong. Both are incomplete.** The Codex report correctly identifies the symptom (cognitive load on authors) but prescribes a treatment (demoting the 9-tier model) that would violate AX-4 (Universality, schema line 129) and undermine the framework's value for regulated and enterprise use cases. The Opus report correctly identifies the stabilization trend but underestimates the practical barrier the current specification size presents to adoption and offers no concrete path to reduce it.

**The actionable truth lies between them:** the 9-tier model must remain canonical, but the authoring experience must be stratified so that complexity is encountered only when needed. The correct next move — as `review.codex.md` independently concludes — is neither "collapse DDR into Express Mode" nor "declare DDR production-complete." It is to keep the current kernel, close source-visible contract gaps, generate derivative authority surfaces, and add profile-driven production contracts that make operational readiness explicit and scalable.

The Gemini review (`review.gemini.md`) arrives at a compatible synthesis, correctly identifying that "precision in the later versions of DDR has been achieved at the cost of profound specification weight" while endorsing the SSOT automation recommendation as the highest-leverage single intervention. Where the Gemini review diverges — particularly in recommending the removal of semantic review mechanics from Core and the elimination of the `ambiguous` UNBUNDLE classification — this review provides targeted evaluation in §6.4.

---

## 4. Feedback on observations.codex.md

### 4.1 Strengths

- **The quantitative signals section is excellent.** Tracking spec line counts and issue-tracker volumes across versions is the right methodology. The observation that issue character shifted from modeling choices to schema-closure defects is precisely correct and verified against the v6.3 source material.
- **The additive-only evolution diagnosis is accurate.** Examining `ddr_system_v6.3.yaml`, I count 8 DAG invariants (INV-1 through INV-8, lines 258–299), 8 core operations (INSERT through UNBUNDLE_EXECUTE, lines 1179–1276), 9 guard definitions (gc-001 through gc-009, lines 2689–2727), 3 manifest item types (MISSING_MEDIATOR, SUPERSEDE_FAILED, SUPERSEDE_PENDING_DETECTED, lines 1381–1409), 7 extension integration rules (EXT-R1 through EXT-R7, lines 1537–1557), and a 12-row status transition table (lines 2628–2688) — none of which existed in v1. Every one was added to solve a real problem, but none replaced an existing mechanism.
- **The "one true normative source" recommendation is the single highest-leverage suggestion in either report.** The current authority model (see `ddr_system_v6.3.yaml` lines 2623–2626) explicitly acknowledges that the YAML lifecycle block governs over the Markdown §3.8 table. This precedent should be generalized: the YAML pair governs everything; all other surfaces are generated.

### 4.2 Factual Errors and Overstatements

1. **"v6.0 appears largely to relabel and carry forward v5.0 concepts"** — This understates v6.0's contributions. The system definition shows that v6.0 introduced INV-7 (semantic gap governance, line 289), constraint precedence classes (logical/physical distinction, line 1148), `MISSING_MEDIATOR` gap classification (line 1383), and the conflict resolution protocol (line 1357). These are not relabeling; they are semantic completeness mechanisms. The Gemini review independently corroborates this finding, noting that the v6.0 version history entry (lines 2128–2133) describes these as first-time introductions, not carry-forwards. However, the v6.0 version history summary (line 2132) is misleadingly vague — "All specification files, schema definitions, and meta-details updated to satisfy a comprehensive versioning alignment requirement" — which likely contributed to the Codex report's mischaracterization. A more precise version history entry would have prevented this reading.

2. **"The least stable DDR idea is the assumption that every nuance must be represented as a first-class normative artifact"** — This is directionally correct but imprecise. Examining the schema, the DDR already practises selective escalation: `verification_mode: semantic` rules explicitly defer to human judgment rather than encoding every nuance as machine-checkable structure. The `REVIEW_REQUIRED` output pathway (see VALIDATE operation, line 1229) and the reconciliation manifest's `pending_items` queue are evidence that the system already distinguishes between structural gates and semantic reviews. The report's recommendation to "keep semantic judgment review-based" therefore describes the current design, not a reform. The Gemini review's suggestion to "decouple semantic review from the Core state machine" (§6.4, item 3) is evaluated separately because it mischaracterizes the current coupling depth.

3. **"Treat the existing 4-group Express Mode as the primary design-system surface"** — This recommendation conflicts with the DDR's own axioms. AX-4 (Universality, line 129) requires that the Core applies to all software systems regardless of domain, scale, or technology. Express Mode groups (G1–G4) are a presentation convenience with fixed tier compositions (see schema lines 803–835). Promoting them to the primary authoring surface would force all DDR instances through a 4-group model that cannot represent the CL activation decision, the SAL merge-node semantics, or the GPCL-FCL-BR1 bridge rule without immediately requiring unbundling. For regulated programs where CL is mandatory and every tier must be independently auditable, Express Mode is not a simplification — it is an obstacle that must be expanded through before useful work begins.

4. **"The v5 issue tracker header reports `open_issues: 1` while the visible registry entries are resolved"** — This is described as "a concrete metadata-synchronization smell." While potentially valid as an observation of the archived file, it is not evidence of a structural flaw in DDR v6.3. The v6.3 source-of-truth files have a clean `errata_log: []` (line 101) with no pending errata, and the lifecycle block is internally consistent with the status transition table.

### 4.3 What the Codex Report Understates

As `review.codex.md` correctly observes, the Codex report understates how much production-relevant design content already exists in v6.3. The specification is not merely "bookkeeping":

- **GPCL** already requires measurable quality thresholds, security requirements, reliability targets, residency, retention, scalability, and accessibility (GPCL-R6 through GPCL-R10, lines 596–633).
- **CL** already requires runtime constraints, hardware envelopes, infrastructure ceilings, deployment topology, and internal conflict reconciliation (CL-R1 through CL-R10, lines 774–842).
- **SAL** already requires concurrency rules, data ownership, failure isolation, and resilience boundaries (SAL-R1 through SAL-R6, lines 882–911).
- **ICL** already requires machine-parseable contracts, validation rules, error contracts, and versioning (ICL-R1 through ICL-R7, lines 942–980).
- **CDL** already requires component blueprints, public interfaces, state structures, dependency graphs, and multi-language blueprints when CL declares multiple targets (CDL-R1 through CDL-R7, lines 1011–1050).
- The **extension catalog** already includes hardware/resource intelligence (E1/HRE), dependency analysis (E2/DGA), lifecycle/versioning (E3/LVE), observability/runtime (E4/ORE), AI inference (E5/ARE), security/compliance (E6/SCE), data-domain modeling (E7/DDE), deployment/CI-CD (E8/DCP), and ethics/human-centered design (E9/EHD).

This is a substantial cross-scale design vocabulary that the Codex report's "over-governance" framing partially obscures. The Gemini review echoes this under-acknowledgment when it characterizes the system as producing "specification weight" — true at the meta-level, but the weight is not empty bureaucracy; it encodes 70+ atomic inclusion and exclusion rules across 9 tier definitions, each with verified enforcement semantics.

### 4.4 Recommendations I Endorse

- **Enforce a subtraction rule for new core changes.** This is the most important governance recommendation. Every v6.x addition passed a necessity test, but no addition was paired with a mechanism retirement. The result is monotonic surface growth. A formal complexity budget requiring a retirement for every addition would create the selection pressure the system needs. The Gemini review independently arrives at the same conclusion (item 4: "Halt Structural Scope Creep via a Subtraction Rule"), confirming cross-reviewer consensus.

- **Generate derivative surfaces rather than co-maintaining them.** This directly addresses the dominant defect source (schema/spec misalignment) identified by both reports and by the v6.3 issue tracker. The Gemini review reinforces this as its third recommendation and explicitly calls for "prohibiting manual co-maintenance of any standalone Markdown specifications" — a stronger formulation that this review endorses.

- **Treat metadata drift as a release-blocking defect.** The self-hosting property means that metadata inconsistency is not cosmetic — it is a structural violation of the DDR's own axioms.

### 4.5 Recommendations I Reject

- **"Demote the 9-tier surface to internal normalization or expert mode."** This would bifurcate the DDR into two systems with different authority surfaces, creating exactly the dual-authority drift the report warns against elsewhere. The better answer — as both this review and `review.codex.md` conclude — is to keep the full semantic kernel canonical, freeze it, and make Express Mode a generated or tool-assisted facade with guaranteed round-trip behavior.

---

## 5. Feedback on observations.opus.md

### 5.1 Strengths

- **The phase analysis is the finest structural account of the DDR's evolution I have seen.** The v4 table (§4.3) correctly identifies every major structural addition and its complexity cost. The edge type design consolidation narrative (6 → 4 with `derivation_mode` recovery in v5) is verified against the source material and accurately describes the within-version consolidation that the Codex report partially mischaracterizes.

- **The "Complexity Paradox" framing (§5.3) is the most useful conceptual contribution in either report.** The stepped example showing how a single edge type's specification grew from one sentence to a multi-field contract with conditional semantics, backward-compatibility defaults, and cross-referenced citation constraints is precisely right. This is verified: `ParentCitation` in the schema (lines 1627–1663) has `id`, `edge_type`, `derivation_mode` (conditional on `edge_type: derives`), backward-compatibility notes in `node_schema_fields` (line 203), and cross-references to CIT-R2 and CIT-R6. That is indeed an order of magnitude more specification for the same concept. The Gemini review's characterization of this as "the specification paradox" — that machine-enforceable determinism inherently requires more precise specification rules — is a compatible restatement.

- **The "Zero structural issues in the last four audit cycles" metric (§7.1) is the single most important datum in either report.** It concretely demonstrates that the architecture is finished and only enforcement is catching up.

- **The Stabilization Evidence section (§7) is methodologically rigorous and directly verified against source material.** Tier count, axiom stability, extension non-contamination, and specification growth rate deceleration are all confirmed by the v6.3 YAML artifacts.

### 5.2 Where the Opus Report Is Too Optimistic

As `review.codex.md` correctly observes, this report treats architectural stabilization too closely as a proxy for production readiness. A schema-valid system is not the same as a deployment-ready framework with clear production obligations.

The v6.3 YAML pair still exposes multiple source-visible contract gaps that neither the Opus report nor my original review fully catalogued:

1. **SIL parent_ids enforcement gap.** When `active_tiers` contains `XPD`, the *document-level* allOf (schema lines 78–95) enforces `SIL.parent_ids.minItems: 1`. But the *per-node* SIL conditional (schema lines 1548–1555) does not enforce `minItems: 1` — it only constrains the `id` pattern. This means standalone node validation (without document-level `active_tiers` context) can admit orphaned SIL nodes when XPD is active, creating a schema/specification semantic mismatch.

2. **DEPRECATED → ACTIVE guard weakness.** The `DIRTY → ACTIVE` transition requires guards `[gc-001, gc-005, gc-006]` (structural rules pass, review items resolved, validation scope confirmed). The `DEPRECATED → ACTIVE` transition (lines 2684–2687) requires only `[gc-002, gc-003, gc-004]` (deprecation rationale documented, sunset date cleared, status reversal logged). This means a deprecated node can be reactivated *without passing structural validation or review closure* — a genuine lifecycle safety gap.

3. **Missing DEPRECATED → DIRTY transition.** If a parent of a DEPRECATED node is modified, dirty propagation should set descendants DIRTY. But the lifecycle `status_transitions` table (lines 2628–2688) contains no `DEPRECATED → DIRTY` row. DEPRECATED nodes cannot lawfully re-enter the validation workflow via dirty propagation, forcing them into an awkward `DEPRECATED → ACTIVE → DIRTY` path that requires reactivation before re-validation. The `dirty_flag_notes` at line 1329 explicitly describe DEPRECATED as "not a terminal state," confirming this is a gap rather than a deliberate prohibition.

4. **`system_metadata` has no required fields.** The schema (lines 232–258) defines `system_metadata` as a typed object with named properties (`status`, `date`, `scope`, `authority`, `lineage`, `single_source_of_truth`, `design_philosophy`, `changes_from_prior`) but no `required` key. A `system_definition` document can carry an empty `system_metadata: {}` and pass schema validation, even though every property is semantically essential for a normative specification.

5. **UNBUNDLE_EXECUTE behavior with inactive tiers is unspecified.** Express Mode group G2 contains `[FCL, CL]`. When CL is inactive, UNBUNDLE_EXECUTE must allocate G2 content to FCL only. But neither the system YAML's `unbundle_determinism_rule` (lines 384–396) nor the UNBUNDLE_EXECUTE operation description (lines 1261–1276) specifies this behavior explicitly, leaving reduced-topology unbundling indeterminate.

6. **`TierDefinition` topology fields are not required.** The schema `TierDefinition` definition (lines 890–972) lists `parent_relationships` and `child_relationships` as optional properties. The `required` array (line 892) includes `[tier_id, label, core_question, is_optional, atomic_inclusion_rules, atomic_exclusion_rules]` but omits topology declarations. A tier definition can pass validation without declaring its structural position in the DAG, breaking the topology completeness guarantee. All 9 tier definitions in the system YAML include these fields — their absence from `required` is an oversight, not a design choice.

7. **`errata_log` has no operational governance.** The schema defines the `errata_log` structure (lines 222–228) and the system YAML carries `errata_log: []` (line 101), but no normative text governs when entries are required, how they are retired, or whether unresolved errata are release-blocking.

### 5.3 Factual Notes

1. **"9 lifecycle guards" (§3 table, Lifecycle Guards row, v6.3 column)** — Confirmed correct: `guard_definitions` in the system YAML contains exactly 9 entries (gc-001 through gc-009, lines 2689–2727).

2. **"~170KB" combined spec size** — The actual combined size of the v6.3 YAML pair is approximately 172 KB (125,586 + 46,178 bytes), so this estimate is accurate.

3. **"No future version should need to add tiers, edge types, or fundamental operations. The structural design is complete." (§9.1)** — This is stated too categorically. The system definition's own `extension_catalog` (9 extensions, E1–E9) is fixed by convention, not by invariant. There is no DAG invariant or schema constraint preventing a 10th extension. More importantly, the `SemanticGapClassification.allowed_types` (schema line 1046) is currently restricted to `enum: [MISSING_MEDIATOR]`. If new gap types are needed (and the GPCL→SAL indirect dependency pattern suggests they will be), the "structural design is complete" claim will require revision. The claim should be qualified as: the *topology and edge vocabulary* are complete; the *governance vocabulary* may still evolve.

4. **The report does not identify any concrete modifications.** For a document titled "Observations," this is acceptable. But the absence of an actionable remediation plan is a significant gap when measured against the Codex report's 6-phase program.

### 5.4 Insights Unique to This Report

- **The self-hosting recursion risk** (§6) is identified exclusively by this report and is the most structurally important long-term risk. The observation that "each specification change must also be a valid schema change" is precisely correct: the `ddr_system_v6.3.yaml` file is itself validated against `ddr_node_schema_v6.3.yaml`, which it defines. This circularity is elegant but creates an engineering constraint that neither report fully resolves. The Gemini review independently identifies this under its "self-hosting loop" insight (item 2), confirming it as a cross-reviewer consensus concern.

- **The "specification growth rate deceleration" metric** (§7.5) showing monotonically declining growth (10× → 25% → 20% → 15%) is the strongest quantitative evidence for convergence in either report.

---

## 6. Cross-Report Synthesis

### 6.1 Where Both Reports Should Have Gone Deeper

1. **The `content` field problem.** The DDR node schema defines `content` as `type: string` (schema line 1487) with no structural constraints beyond "tier-level atomic inclusion/exclusion rules are enforced at runtime, not by this schema." Furthermore, `content` is not in the `required` array of `DdrNode` (lines 1420–1427) — a schema-valid node can exist with no content at all. This means the entire tier-level compliance apparatus — the 70+ atomic inclusion and exclusion rules distributed across 9 tier definitions — operates outside the schema boundary. The schema can validate that a node *exists* with the right shape, but it cannot validate that the node's *content* satisfies its tier's rules or even that content exists. Neither report identifies this as the single largest unenforceable surface in the DDR. The Gemini review's first recommendation ("Mandate `content` as a Required Schema Element") correctly targets this gap.

2. **The DELETE operation is under-specified.** The system YAML defines DELETE as "Remove node; cascade orphan detection to children" (line 1188) but the lifecycle `status_transitions` table (lines 2628–2688) contains no row with operation `DELETE`. DELETE is modeled as an "operation sink" (per the v6.2 version history, line 2146), but neither report examines the implications: a DELETEd node has no final status, no transition guard, and no rollback mechanism. This is a genuine lifecycle gap. The v6.2 version history explicitly states DELETE was "modeled as an operation sink" (line 2146), confirming this was a deliberate design choice — but one that leaves INV-8's "complete and closed state machine" claim technically unsatisfied for DELETE inputs. The `StatusTransition` schema (lines 1354–1396) requires either `to` (a `StatusEnum` value) or `to_node_field` (for rollbacks) — there is no schema mechanism to represent a terminal sink transition with `to: null`, which means even modeling DELETE as a status transition would require a schema extension.

3. **Guard ID rigidity.** The schema types `GuardIdRef` as a fixed enum: `[gc-001, gc-002, gc-003, gc-004, gc-005, gc-006, gc-007, gc-008, gc-009]` (schema lines 1669–1671). This is a closed-world assumption that makes adding a new guard condition a schema-breaking change requiring a version increment. While no immediate additions are anticipated, this rigidity conflicts with the subtraction-rule principle: you cannot retire a guard and replace it without a schema version change even when the replacement has identical scope.

4. **The score band boundary ambiguity.** Both scoring profiles (`standard_v1` and `conservative_v1`) define score bands with boundary values like `[0.0, 0.4]` and `[0.4, 0.7]`. The schema validates that each range element is a number between 0 and 1 (schema lines 1203–1211), but there is no constraint enforcing non-overlap, ordering, or boundary exclusivity. A score of exactly 0.4 is valid in both the "speculative" band `[0.0, 0.4]` and the "probable" band `[0.4, 0.7]`. This is exactly the kind of determinism gap that AX-3 was written to prevent. However, the custom profile `validation_note` (system YAML line 1949) and ARE-R2 (line 1674) both state that "deterministic ARE conformance validation" is responsible for "score-band ordering and non-overlap" checks — this means the gap is acknowledged but delegated to runtime rather than encoded in the schema, a deliberate layering choice that should be made explicit.

5. **Global rule_id uniqueness is not enforced.** The schema defines separate patterns for `AtomicTierRuleId` (`^(?:XPD|SIL|GPCL|FCL|CL|SAL|ICL|CDL|ISL)-(?:R|E)[0-9]+(?:-[a-z]+)?$`, line 738), `BridgeRuleId` (`^[A-Z]+-[A-Z]+-BR[0-9]+$`, line 742), `ExtensionRuleId` (`^[A-Z]{3,4}-R[0-9]+$`, line 751), `CitationRuleId` (`^CIT-R[0-9]+$`, line 734), and `InvariantId` (`^INV-[0-9]+$`, line 730) — but there is no cross-family uniqueness requirement. A string like `GPCL-R1` is valid under both `AtomicTierRuleId` and `ExtensionRuleId`. While the `AtomicTierRuleId` pattern requires a tier prefix that makes *practical* collision unlikely in the current catalog (current extension prefixes — HRE, DGA, LVE, ORE, ARE, SCE, DDE, DCP, EHD — do not collide with tier identifiers), the absence of a formal uniqueness invariant means rule references in tooling, logs, and advisory outputs cannot be resolved unambiguously without tier context. A future extension with a 3–4 letter prefix matching a tier abbreviation would create genuine collisions.

6. **The `project` block role under `system_definition` is ambiguous.** The schema permits `project` on all document profiles (lines 206–221), and the canonical `ddr_system_v6.3.yaml` includes `project: {name: "DDR System v6.3 Semantic Authority", created: "2026-02-26", mode: full}` (lines 14–17). But it is unclear whether this block carries normative weight for system-definition documents, whether it is required, or whether its `mode` field has enforcement implications for a system-definition artifact that is inherently full-mode. The schema's conditional allOf at lines 96–120 enforces `project.mode: express` ↔ `document_profile: project_instance_express` bidirectionally, but makes no assertion about `project.mode: full` under `system_definition`.

7. **`version_history` v1.0 has an empty date.** The system YAML (line 2094) contains `date: ""` for the v1.0 version history entry. The `VersionHistoryEntry` schema (line 1319) types `date` as optional string with no format constraint, so the empty string passes validation — but the semantic authority should not contain vacant metadata in its own historical record.

### 6.2 The Central Question Neither Report Answers

**Can the DDR System v6.3 actually be implemented as described?**

Both reports evaluate the specification as a specification. Neither evaluates it as an implementation blueprint. The ISL-8.1 node (system YAML lines 2500–2621) provides a Python scaffold, but it is a ~122-line stub with `...` bodies. The specification describes 8 atomic operations with complex pre/post-conditions, a 12-row status transition table with 9 guards, a 3-step SUPERSEDE atomicity protocol with rollback semantics, an UNBUNDLE two-phase protocol with deferred fragment handling, and 9 extensions with independent contracts — all of which must be implemented in a runtime that handles concurrent mutations, maintains a reconciliation manifest, and supports the full lifecycle state machine.

The gap between specification and implementability is not a flaw in either report — it is a flaw in the DDR's own self-assessment. The specification claims to be "production-ready" (system metadata status: `Finalized`), but the distance from finalized specification to working runtime is substantial. The modification list below addresses this gap directly.

The Gemini review partially acknowledges this gap in its observation that "critical operational realities — such as the optional `content` schema field and the absence of lifecycle rows for `DELETE` — expose a profound gap between theoretical completeness and actual runtime compliance." This is accurate but does not go far enough: the operational complexity applies to the entire Core operations protocol, not just the two named gaps.

### 6.3 Insights Not Surfaced by Either Observation Report

#### 6.3.1 The Extension System Has an Identity Crisis

The 9 extensions in the catalog fall into four distinct behavioral categories that the current model does not distinguish:

| Category | Extensions | Characteristic |
| --- | --- | --- |
| **Analytical overlays** | HRE (E1), DGA (E2), ORE (E4), SCE (E6), EHD (E9) | Pure read-only analysis; produce advisories or external artifacts |
| **Data model extensions** | DDE (E7) | Reads FCL+GPCL+SAL+ICL+CDL, validates ER model consistency; performs data-domain governance with confirmation-only validation (DDE-R5) |
| **Inference engines** | ARE (E5) | Creates candidate nodes, manages a stateful pool with a tri-state lifecycle (active/paused/disabled), checkpoint persistence, and promotion mechanism |
| **Tooling integrations** | LVE (E3), DCP (E8) | Map DDR artifacts to external systems (VCS, CI/CD); generate external deployment artifacts |

The Extension System (§8) treats all 9 uniformly under the "read-only overlay" model. But ARE's Candidate Pool is not a read-only overlay — it is a stateful staging area with its own lifecycle, persistence contract (checkpoint path at `.agent/state/are_candidate_pool.checkpoint.yaml`), and promotion mechanism. The `extension_system.candidate_pool` block (system YAML lines 1439–1536) is specific to ARE but lives in the generic Extension System section, creating a structural coupling that conflicts with the "orthogonal overlay" architecture description. The Gemini review's recommendation to "abstract Extension-specific internals from the Core schema" directly targets this coupling.

#### 6.3.2 The Reconciliation Manifest Is Under-Typed

The manifest schema (system YAML lines 1381–1420) defines only 3 `manifest_item_types`: `MISSING_MEDIATOR`, `SUPERSEDE_FAILED`, and `SUPERSEDE_PENDING_DETECTED`. But the specification describes at least 5 additional manifest interactions:

1. VALIDATE emits `REVIEW_REQUIRED` items to `pending_items` (line 1234)
2. VERIFY emits `REVIEW_REQUIRED` items for semantic consistency (line 1225)
3. Conflict resolutions must be recorded in the manifest (line 1364)
4. Extension advisories are tracked in the manifest (line 1380)
5. Override approvals for below-threshold ARE candidates must be recorded (line 1529)

None of these have typed `manifest_item_types` entries. This means the reconciliation manifest — which the compliance checklist requires to show "zero pending items" for CLEAN status (line 1971) — has a machine-typed subset and an untyped superset, violating the schema's own closure aspiration. The Gemini review correctly identifies this gap (recommendation 5: "Establish Fully Typed Reconciliation Manifests").

#### 6.3.3 The CIT-R7 Freshness Rule Has No Enforcement Mechanism

CIT-R7 (system YAML line 345) states: "A child node may remain ACTIVE only while each cited parent remains at the version last validated against." But the node schema has no field to record the parent version that was validated against. The `ParentCitation` object (schema lines 1627–1663) has `id`, `edge_type`, and `derivation_mode` — no `validated_parent_version` field. Without this field, CIT-R7 is an unenforceable aspiration: VERIFY cannot mechanically detect stale parent citations because there is no recorded baseline version to compare against. The Gemini review independently identifies this gap (recommendation 7: "Ensure `CIT-R7` Freshness via Persisted Baselines").

#### 6.3.4 Missing Operational Completeness

As `review.codex.md` correctly identifies, the SSOT does not currently define explicit contracts for several concerns that matter in production systems. These are not Core structural gaps — they are scope gaps that must be addressed via extensions, profiles, or adjacent contracts:

- Secrets and key management beyond the current ICL RBAC requirement (SCE-R3, line 1734)
- Authentication/session architecture
- Multi-tenancy and tenant isolation strategy
- Deployment rollback, canary, and blue-green policies beyond DCP's current minimum pipeline (DCP-R2, line 1790)
- Backup, restore, and disaster recovery beyond GPCL's RTO/RPO targets (GPCL-R7, line 618)
- Runbooks and on-call ownership beyond ORE's telemetry point requirement (ORE-R3, line 1642)
- Rate limits, idempotency, retry, and backpressure for online systems
- Event-driven and queue-based system semantics
- SBOM, artifact provenance, and supply-chain controls beyond DGA's dependency graph (DGA-R3, line 1601)
- Profile-driven obligation scaling by system class
- Testing strategy beyond DCP's minimum lint/test/build/deploy pipeline (DCP-R2)
- Cost and capacity planning beyond CL's static hardware envelopes (CL-R6/CL-R7)

The architecture may be stable, but the framework is not yet production-complete for the full range of stated use cases — from single-file developer scripts to enterprise-grade online platforms with hardware constraints.

### 6.4 Evaluation of Gemini-Specific Recommendations

The Gemini review proposes 8 atomic modifications. Each is evaluated here against the SSOT:

1. **"Mandate `content` as a Required Schema Element"** — **Endorsed.** This is the highest-impact single schema change. A node with no content is structurally hollow and bypasses the entire 70+ rule tier compliance apparatus. Captured as M-05.

2. **"Implement Explicit Lifecycle Semantics for `DELETE`"** — **Endorsed with refinement.** The Gemini review correctly identifies that DELETE's absence from the status transition table breaks INV-8's completeness claim. However, the implementation requires a schema modification: `StatusTransition.to` currently requires a `StatusEnum` value (lines 1360–1362), and there is no `null` option. Modeling DELETE as a transition to a terminal state requires either adding a `DELETED` status or extending `StatusTransition` to permit `to: null`. Captured as M-07.

3. **"Formalize Profile-Driven Capability Governance"** — **Endorsed.** The profile system (`system_class` × `operational_maturity`) is the architecturally correct answer to the scaling rigidity problem. It achieves the cognitive-load reduction the Codex report seeks without sacrificing the universality the Opus report correctly values. This is the most important forward recommendation. Captured as M-22/M-23.

4. **"Enforce SSOT Document Generation"** — **Endorsed.** The authority hierarchy declaration generalizes the precedent already established by the lifecycle block (lines 2623–2626). Captured as M-15.

5. **"Establish Fully Typed Reconciliation Manifests"** — **Endorsed.** The 3-type manifest is demonstrably incomplete against the specification's own described behaviors. Captured as M-11.

6. **"Rectify `DEPRECATED → ACTIVE` Guard Escapes"** — **Endorsed.** The guard gap is source-verified: `DEPRECATED → ACTIVE` uses `[gc-002, gc-003, gc-004]` while `DIRTY → ACTIVE` uses `[gc-001, gc-005, gc-006]`. Structural validation (gc-001) and review closure (gc-005) should be mandatory for any reactivation. Captured as M-04.

7. **"Ensure `CIT-R7` Freshness via Persisted Baselines"** — **Endorsed.** Without `validated_parent_version`, CIT-R7 is procedural guidance, not a machine-enforceable rule. Captured as M-10.

8. **"Decouple Stateful Inferencing from Generic Extensions"** — **Partially endorsed.** The ARE candidate pool is indeed architecturally distinct from overlay extensions. However, full extraction into a separate schema file introduces tooling cost that is not justified at this stage. The better approach is to clearly document the candidate pool as ARE-specific within the system-definition surface and make `are_scoring_profiles` optional for non-system-definition profiles. Captured in §6.3.1 and noted in M-11.

### 6.5 Evaluation of Codex Review (review.codex.md) Unique Contributions

The Codex review provides the most granular modification list (51 items). Key unique additions validated against the SSOT:

1. **Items 1–18 (Contract Closures)** — Largely aligned with this review's findings. Items 1, 2, 3, 5, 6, 9, 10, 11, 12, 13, 14, and 15 are all source-verified and incorporated into the modification list below with appropriate attribution.

2. **Items 16–18 (Meta-governance)** — The Codex review uniquely identifies three meta-level gaps: (a) the `project` block ambiguity under `system_definition` (item 16), (b) `errata_log` operational governance (item 17), and (c) issue-specific audit commentary in the authority file (item 18). The first two are captured in §6.1 items 6–7 and incorporated as M-20 and M-45. Item 18 (audit commentary removal) is valid but lower priority — the system YAML contains issue-specific comments (e.g., lines 280–281: "ISSUE-007 Change") that should be moved to `errata_log` entries or `version_history` notes. Captured as M-48.

3. **Items 27–34 (Implementation Readiness)** — The most important unique contribution: structured operation preconditions/postconditions (item 27), runtime contract (item 28), expanded scaffold (item 29), validation metadata (item 30), and environment modeling (item 34) are production-critical and not addressed by the Gemini review. Incorporated as M-35 through M-39.

4. **Items 35–45 (Production Contracts)** — These are the highest-volume forward recommendations. Each is individually sound but must be gated by the profile system (M-22/M-23) to avoid over-burdening small projects. Incorporated as M-27 through M-34.

---

## 7. Maximally Optimized Atomic Modification List

The following modifications are organized by priority and designed to move DDR v6.3 from "finalized specification" to "production-ready implementation blueprint" suitable for use cases ranging from custom scripts and developer tools to enterprise-scale online applications with hardware considerations.

Each modification is atomic: it can be applied independently without requiring other modifications as prerequisites, unless explicitly noted. Each is tagged with its classification per §2.

### Tier 1 — Release-Blocking v6.3 Corrections (Source-Visible Gaps)

These close genuine contract gaps directly observable in the v6.3 YAML pair.

| # | Target | Modification | Classification | Rationale |
| --- | --- | --- | --- | --- |
| M-01 | `DdrNode` SIL conditional | Add `parent_ids: {minItems: 1}` to the per-node SIL conditional (schema lines 1548–1555) so that standalone node validation enforces parent citation when XPD is contextually active. | Source-visible gap | Currently, SIL parent_ids enforcement depends on the document-level `active_tiers` allOf (lines 78–95), which is invisible to per-node validators. Per-node validation of SIL nodes can silently admit orphans. |
| M-02 | `ScoringProfile.score_bands` | Add schema-level constraints: (a) `score_bands` items ordered by ascending `range[0]`; (b) each `range[1]` equals next band's `range[0]` (contiguous coverage); (c) first band begins at `0.0`, last ends at `1.0`; (d) boundaries follow half-open `[low, high)` with final band closed `[low, 1.0]`. | Source-visible gap | A score of exactly 0.4 currently falls in two bands. AX-3 requires deterministic assignment. While ARE-R2 delegates this to conformance validation, encoding boundary semantics in the schema prevents non-conformant profiles from ever entering the system. |
| M-03 | `TierRelationship.edge_type` | Remove `extends` from the enum (schema line 885). | Source-visible gap | No tier relationship in the system YAML uses `extends`. The edge type is Extension-to-Core only (§3.2), stored in `extension_annotations`, never in `parent_relationships`/`child_relationships`. Verified: all 22 tier relationships across 9 tier_definitions (lines 408–1113) use only `derives`, `constrains`, or `implements`. |
| M-04 | `lifecycle.status_transitions` | Add `DEPRECATED → ACTIVE` guards: append `gc-001` and `gc-005` to the existing guard list `[gc-002, gc-003, gc-004]`, yielding `[gc-001, gc-002, gc-003, gc-004, gc-005]`. | Source-visible gap | Currently, `DEPRECATED → ACTIVE` (lines 2684–2687) does not require structural validation (gc-001) or review closure (gc-005). A deprecated node can be reactivated without passing the same gates required for `DIRTY → ACTIVE` (line 2656: `[gc-001, gc-005, gc-006]`). |
| M-05 | `DdrNode.content` | Move `content` from optional to `required` in the `DdrNode` schema (line 1420). | Source-visible gap | A schema-valid node with no content is structurally hollow. Every tier's atomic inclusion rules presuppose content exists. An empty-content node should fail `VALIDATE`, but currently it passes schema validation silently. Cross-reviewer consensus: Gemini recommendation 1. |
| M-06 | `lifecycle.status_transitions` | Add a `DEPRECATED → DIRTY` transition row: `{from: DEPRECATED, to: DIRTY, operation: MODIFY, side_effect: propagation, guards: []}`. | Source-visible gap | Dirty propagation from a parent MODIFY must be able to set DEPRECATED descendants DIRTY. Without this row, dirty propagation hitting a DEPRECATED node has no lawful path. The `dirty_flag_notes` (line 1329) explicitly describe DEPRECATED as not being terminal and subject to further lifecycle transitions. |
| M-07 | `lifecycle.status_transitions` | Add `DELETE` transition rows for DRAFT, ACTIVE, DIRTY, and DEPRECATED, each modeled as terminal transitions. Extend `StatusTransition` to permit `to: null` for terminal-sink semantics, or add a `DELETED` terminal status to `StatusEnum`. Add appropriate guards (at minimum: orphan-cascade acknowledgment for ACTIVE/DIRTY deletion; deprecation-first preference for ACTIVE nodes). | Source-visible gap | DELETE is the only core operation without lifecycle rows. INV-8 (line 296) requires the state machine to be complete. The v6.2 version history (line 2146) explicitly models DELETE as an "operation sink" but does not encode this in the transition table. The `StatusTransition` schema (lines 1354–1396) currently has no mechanism to represent `to: null`. |
| M-08 | `system_metadata` | Add `required: [status, date, scope, authority, lineage, single_source_of_truth]` to the schema definition (after line 235). | Source-visible gap | A `system_definition` document can currently carry `system_metadata: {}` and pass validation. Every listed field is semantically essential for a normative specification artifact. |
| M-09 | `GuardIdRef` ($defs) | Convert from `enum: [gc-001, ..., gc-009]` to `type: string, pattern: "^gc-[0-9]{3}$"`. | Source-visible gap | Eliminates schema-breaking changes when adding guard conditions. Guard definitions in the system YAML remain the authoritative registry; the schema validates format conformance. Aligns with the Gemini review's recommendation to freeze the operations namespace while preserving bounded extensibility. |
| M-10 | `ParentCitation` ($defs) | Add `validated_parent_version: {type: string, pattern: "^[0-9]+\\.[0-9]+\\.[0-9]+$"}` as an optional field. | Source-visible gap | Enables enforcement of CIT-R7 (parent-version freshness, line 345). Without this, VERIFY cannot detect stale citations. Write-once semantics: set on VALIDATE success, cleared on parent MODIFY/SUPERSEDE to trigger DIRTY propagation. Cross-reviewer consensus: Gemini recommendation 7, Codex review item 3. |
| M-11 | `SemanticGapClassification.allowed_types` and `manifest_item_types` | Expand `allowed_types` beyond `[MISSING_MEDIATOR]` to include `REVIEW_REQUIRED`, `CONFLICT_RESOLUTION`, `OVERRIDE_APPROVAL`, `EXTENSION_ADVISORY`, `DEFERRED_FRAGMENT`. Add corresponding `manifest_item_types` entries with typed `fields` arrays and appropriate `severity` levels. | Source-visible gap | The reconciliation manifest is referenced by 5+ mechanisms that produce items not covered by the current 3 typed entries. Typing them makes "zero pending items" (compliance checklist, line 1971) mechanically unambiguous. Cross-reviewer consensus: Gemini recommendation 5, Codex review item 4. |
| M-12 | Version history | Set the v1.0 entry's `date` field to a non-empty value (system YAML line 2094), or if the date is genuinely unknown, change the field value to `"unknown"` and add a `format` note. | Source-visible gap | An empty date in the semantic authority violates the specification's own completeness standards. |
| M-13 | `TierDefinition` | Add `parent_relationships` and `child_relationships` to the `required` array (schema line 892). Exception: ISL has `child_relationships: []` (system YAML line 1075), so the requirement should enforce presence, not non-empty content. | Source-visible gap | A tier definition can currently pass validation without declaring its position in the DAG topology. All 9 tier definitions in the system YAML include these fields — their absence from `required` is an oversight, not a design choice. |
| M-14 | `ExtensionRuleId` / global uniqueness | Add formal disambiguation: (a) restrict `ExtensionRuleId` pattern to exclude tier-name prefixes via negative lookahead or a naming convention requiring non-tier 3-letter extension prefixes, and (b) add a `rule_id_uniqueness` annotation or invariant to the system YAML requiring global uniqueness across all rule families. | Source-visible gap | `GPCL-R1` is valid under both `AtomicTierRuleId` and `ExtensionRuleId`. Current extensions use non-colliding prefixes by convention, but the convention is not enforceable. Without global uniqueness, tooling cannot resolve rule references unambiguously without tier context. |

### Tier 2 — Governance and Authority Hardening (Source-Verified + Forward)

These reduce maintenance burden and prevent governance drift.

| # | Target | Modification | Classification | Rationale |
| --- | --- | --- | --- | --- |
| M-15 | Authority model (meta-level) | Add a top-level `authority_hierarchy` section declaring: (1) the system YAML is the sole normative semantic authority; (2) the node schema is the sole normative structural authority; (3) all Markdown renderings, crosswalks, and reference tables are *derived* surfaces with no normative weight; (4) generated surfaces must carry a machine-generated provenance header citing the source artifacts and generation timestamp. | Forward recommendation | Currently, only the lifecycle block (lines 2623–2626) declares this precedence. Generalizing eliminates the dual-authority ambiguity both reports identify. Cross-reviewer consensus: Gemini recommendation 4, Codex review item 19. |
| M-16 | Complexity budget rule | Add a design philosophy principle (under `system_metadata.design_philosophy`): "Every proposed Core addition must retire existing machinery of equal or greater complexity, or demonstrate it closes a defect not addressable by an Extension, profile, or tooling." | Forward recommendation | Codifies the subtraction rule. Makes the "no new tiers, no new edge types" policy auditable. Cross-reviewer consensus: all four reviews. |
| M-17 | `node_schema_fields` | Add a `content_validation_contract` field to `DdrNode` (type: object, optional) declaring which atomic rule IDs have been evaluated and their pass/fail/review_required disposition, with evaluation timestamp and evaluator identity. | Forward recommendation | The `content` field is unvalidated at the schema level. Recording evaluation disposition makes compliance auditable without requiring the schema to evaluate prose semantics. |
| M-18 | Express Mode | Make Express Mode a generated or tool-assisted facade: add an `express_mode_generation_contract` section or annotation declaring that Express Mode group definitions, unbundle rules, and deferred fragment handling are derived from the full tier definitions and must maintain guaranteed round-trip fidelity. | Forward recommendation | Eliminates the risk of Express Mode drifting into a parallel manually maintained surface. Addresses the Gemini review's legitimate concern about Express Mode complexity without the rejected solution of promoting it to the primary authoring surface. |
| M-19 | Express Mode / inactive tiers | Add normative text to `unbundle_determinism_rule` specifying: when a constituent tier is inactive (e.g., CL inactive in G2=[FCL, CL]), UNBUNDLE_EXECUTE allocates all group content to remaining active tiers only; no content is invented for inactive tiers; inactive-tier annotations ([CL] prefixes) are treated as classification errors with confidence `none`. | Source-visible gap | G2 = `[FCL, CL]`. When CL is inactive, UNBUNDLE_EXECUTE behavior is currently unspecified. Both this review and the Gemini review independently identify this gap. |
| M-20 | `errata_log` | Add governance text to the schema description or as a system-level normative note: when entries are required (post-release corrections only), retirement procedure (moved to `version_history` on next version increment), and release-blocking status (unresolved errata with severity `BLOCKING` must be resolved before next version finalization). | Source-visible gap | The errata log structure exists but has no operational governance. Codex review item 17. |
| M-21 | Deprecation/removal policy | Add a normative deprecation-and-removal policy for rules, profiles, extensions, and generated artifacts specifying sunset periods and migration obligations. Include a `deprecated_artifacts` section in the system YAML tracking items scheduled for removal with their sunset version. | Forward recommendation | Simplification cannot happen intentionally without a formal removal mechanism. Directly enables the subtraction rule in M-16. |

### Tier 3 — Expressiveness and Scalability (Forward Recommendations)

These extend the DDR's reach across the full project-scale spectrum without adding structural complexity.

| # | Target | Modification | Classification | Rationale |
| --- | --- | --- | --- | --- |
| M-22 | `profiles` section | Add a `system_class` taxonomy: `script_tool`, `library_sdk`, `batch_job`, `service_api`, `web_app`, `data_pipeline`, `edge_device`, `regulated_system`. Bind each to minimum required tiers (e.g., `script_tool` requires only SIL+FCL+CDL+ISL; `regulated_system` requires all 9 tiers + XPD), minimum rules, required extensions, evidence gates, and delivery obligations. | Forward recommendation | Small tools should not be over-burdened; enterprise systems cannot under-specify themselves. AX-4 (Universality) is preserved because the full model remains canonical; profiles select subsets. This is the architecturally correct answer to the Gemini review's suggestion to promote Express Mode as the primary surface — profiles achieve cognitive-load reduction without sacrificing semantic completeness. |
| M-23 | `profiles` section | Add an orthogonal `operational_maturity` dimension: `local`, `internal`, `internet_facing`, `high_availability`, `regulated`. Bind each level to explicit gates for observability, security, resilience, rollout, and compliance evidence. | Forward recommendation | Separates scale from operational exposure. A `script_tool` at `regulated` maturity gets different obligations than a `web_app` at `local`. |
| M-24 | Validation gates | Separate `design_complete` from `production_ready` as distinct validation gates. `design_complete` means all tiers are structurally valid per the declared profile; `production_ready` means operational contracts are also satisfied per the declared `system_class` + `operational_maturity` profile. | Forward recommendation | Prevents conflating "spec is finished" with "system is deployable." Supports both small local tools and enterprise production systems without flattening them. |
| M-25 | `tier_definitions[CL]` | Add a `hardware_profile_schema` sub-section to CL's `node_schema` defining structured hardware envelope fields: `cpu_class`, `ram_floor_gb`, `storage_class`, `gpu_requirement`, `network_bandwidth_class`, `power_envelope_watts`. | Forward recommendation | CL-R6 (line 802) requires hardware envelopes but gives no schema guidance. Structured fields enable HRE (E1) to validate mechanically rather than parsing prose. Essential for edge-device and hardware-constrained use cases. |
| M-26 | `DdrNode` | Add `tags: {type: array, items: {type: string}, uniqueItems: true}` as an optional field. | Forward recommendation | Enables cross-concern traceability (e.g., "security", "performance", "accessibility") without new tiers or edges. Tags carry no normative weight and do not participate in VERIFY traversals. |

### Tier 4 — Production Contract Completions (Forward Recommendations)

These address the operational completeness gaps identified by `review.codex.md` without expanding the Core. All items are profile-gated per M-22/M-23.

| # | Target | Modification | Classification | Rationale |
| --- | --- | --- | --- | --- |
| M-27 | Security contracts (SCE) | Expand SCE's contract scope to cover identity, authentication, authorization, secret management, and key management — structured as profile-gated obligations (not required for `script_tool` at `local` maturity; mandatory for `service_api` at `internet_facing`+). | Forward recommendation | Current SCE covers RBAC on ICL contracts only (SCE-R3, line 1734). Production systems need broader security governance. |
| M-28 | Deployment contracts (DCP) | Extend DCP to cover migration sequencing, deployment rollback, compatibility windows, feature flags, canary/blue-green release policies — profile-gated. | Forward recommendation | Current DCP defines minimum lint/test/build/deploy pipeline stages (DCP-R2, line 1790). Enterprise deployments require explicit rollout/rollback semantics. |
| M-29 | Resilience contracts (ORE/GPCL) | Add explicit backup, restore, failover, disaster-recovery, and degraded-operation contracts tied back to GPCL RTO/RPO targets (GPCL-R7, line 618) as proof obligations, not just naming the targets. | Forward recommendation | v6.3 names RTO/RPO targets but does not require operational proof that they can be met. |
| M-30 | Operational readiness (ORE) | Expand ORE beyond telemetry points and vendor-agnostic alerts to cover SLIs, SLOs, alert ownership, dashboards, runbooks, and on-call escalation — profile-gated. | Forward recommendation | Current ORE-R3 (line 1642) requires ">=1 telemetry point." Production systems need complete observability contracts. |
| M-31 | Online system contracts | Add first-class rate-limit, timeout, retry, backpressure, and idempotency contracts for online and event-driven systems — profile-gated to `service_api`, `web_app`, and `data_pipeline` system classes. | Forward recommendation | These are missing entirely from the current specification and extension catalog. |
| M-32 | Event/queue contracts | Add first-class cache, queue, stream, and event-schema contracts including ordering, replay, dead-letter, and durability semantics — profile-gated. | Forward recommendation | Missing from the current specification; essential for event-driven architectures and data pipelines. |
| M-33 | Data governance (DDE) | Expand DDE beyond residency, retention, and ICL-schema consistency to include classification, privacy, consent, deletion/right-to-erasure, lineage, schema evolution, and backfill/reconciliation — profile-gated. | Forward recommendation | Current DDE covers ER model consistency (DDE-R1 through DDE-R5, lines 1753–1777) but not the full data governance lifecycle required by regulated systems. |
| M-34 | Supply chain (DGA) | Expand DGA to cover SBOM generation, artifact provenance and signing, dependency update policy, vulnerability response SLA, and license gating — profile-gated. | Forward recommendation | Current DGA covers dependency graph and copyleft analysis only (DGA-R1 through DGA-R3, lines 1595–1604). Production supply-chain governance is broader. |

### Tier 5 — Implementation Readiness (Forward Recommendations)

These close the gap between finalized specification and implementable runtime.

| # | Target | Modification | Classification | Rationale |
| --- | --- | --- | --- | --- |
| M-35 | `operations.core_operations` | For each of the 8 operations, add structured `preconditions` (array of machine-evaluable expressions) and `postconditions` (array of state assertions) alongside the existing prose `description` and `validation_trigger` fields. | Forward recommendation | Operation semantics are currently embedded in prose. Structured contracts make operations implementable without parsing natural language. |
| M-36 | Top-level | Add a `runtime_contract` section specifying: concurrency model (the system YAML declares "last-write-wins" at ISL-8.1 line 2422 but this is buried in a scaffold node, not declared normatively), persistence model, event/notification model, API surface contract, and transaction/rollback semantics. | Forward recommendation | The specification describes 8 atomic operations but provides no runtime execution contract. Implementers cannot determine whether DIRTY propagation is synchronous or queued, whether operations are serialized or permit concurrent execution. |
| M-37 | `DdrNode` | Add `last_validated_by: {type: string, enum: [VALIDATE, VERIFY]}` and `last_validated_at: {type: string, format: date-time}` as optional fields. | Forward recommendation | Without validation timestamps, "zero pending items" cannot be mechanically confirmed against a known graph state. |
| M-38 | Top-level | Publish a reference validator plus a golden conformance corpus (valid and invalid exemplars for all three document profiles and all lifecycle transitions). Make both release-blocking for every version increment. | Forward recommendation | Closes the gap between "the spec says X" and "a validator enforces X." |
| M-39 | Top-level | Add round-trip conformance tests for: `project_instance <-> VALIDATE`, `project_instance_express <-> UNBUNDLE_SCAN/EXECUTE <-> project_instance`, and `system_definition <-> schema self-validation`. | Forward recommendation | Ensures that Express Mode maintains round-trip fidelity and that the self-hosting property is machine-verified, not assumed. |

### Tier 6 — Documentation, Adoption, and Hygiene (Forward Recommendations)

These improve usability and documentation quality without changing semantics.

| # | Target | Modification | Classification | Rationale |
| --- | --- | --- | --- | --- |
| M-40 | `glossary` | Add entries for at minimum: `Consumption Mode Profile`, `System Class`, `Operational Maturity`, `Manifest Item`, `Bridge Rule`, `Dirty Classification`, `Guard Condition`, `Content Validation Contract`, `Hardware Envelope`, `Scoring Profile`, `Document Profile`, `Constraint Origin`. | Forward recommendation | The glossary currently has 14 entries (lines 2027–2088). At least 12 terms used throughout the specification have no definitions. |
| M-41 | `compliance_checklist` | Add a `profile_aware_validation` sub-section that maps each of the 32 checklist items to the `system_class` + `operational_maturity` profiles where it applies. | Forward recommendation | Prevents false-negative CLEAN declarations for small projects and under-specification of enterprise systems. |
| M-42 | `tier_definitions` | Add a `quick_start_example` field (type: string) to each `TierDefinition` containing a 3–5 sentence example of compliant tier content for a representative use case. | Forward recommendation | Tier rules describe *what* content must contain but never show *what compliant content looks like*. The gap between abstract rules and concrete authoring is the primary adoption barrier identified by all four review documents. |
| M-43 | Top-level | Add a `migration_contract` section specifying: mandatory fields for v6.2 -> v6.3 upgrades, automated migration rules (field additions, enum expansions, structural renames), manual review requirements, and breaking-change classification. | Forward recommendation | Enterprise deployments with hundreds of nodes cannot manually audit every field addition. Formal migration contracts make version upgrades deterministic. |
| M-44 | Top-level | Add reference generators and starter templates for the main `system_class` variants so scripts, libraries, small tools, and enterprise applications can adopt DDR without manual tier-by-tier boilerplate. | Forward recommendation | Addresses the Codex report's legitimate cognitive-load concern and the Gemini review's authoring-reality insight through tooling rather than spec reduction. |
| M-45 | `project` block | Formalize the role of `project` under `system_definition`: either make it explicitly required (documenting its normative purpose) or add a normative note clarifying it is metadata-only with no enforcement implications for system-definition artifacts. | Source-visible gap | The canonical system YAML uses `project` (lines 14–17) but the role is undefined for `system_definition` profile. Codex review item 16. |
| M-46 | `project.mode` consistency | Add a schema conditional ensuring that `project.mode: full` is required (or defaulted) when `document_profile: system_definition`, preventing a system-definition artifact from declaring `mode: express`. | Source-visible gap | The current bidirectional enforcement (lines 96–120) only handles `express` mode <-> `project_instance_express`, leaving `system_definition` with `mode: express` technically schema-valid. |
| M-47 | Testing strategy | Add or extend DCP to include a `testing_contract` covering unit, integration, contract, end-to-end, performance, security, resilience, and migration testing requirements — profile-gated with minimum coverage expectations per `system_class` + `operational_maturity` level. | Forward recommendation | Current DCP includes "test" as a pipeline stage but does not define test categories, coverage expectations, or profile-specific minimums. |
| M-48 | Inline commentary hygiene | Remove issue-specific audit commentary from inline semantic-authority comments (e.g., lines 280–281: "ISSUE-007 Change") and migrate the historical context to `errata_log` entries or `version_history` notes. | Source-visible gap | The authority file should contain only timeless explanatory notes, not version-specific audit residue. Codex review item 18. |

---

## 8. Prioritized Implementation Sequence

If the goal is maximum leverage with minimum destabilization:

| Phase | Items | Effect |
| --- | --- | --- |
| **Phase 1: Contract Gap Closure** | M-01 through M-14 | Closes all source-visible v6.3 contract gaps. No new concepts; pure defect remediation. |
| **Phase 2: Authority Hardening** | M-15 through M-21 | Freezes the kernel, establishes generated surfaces, prevents governance drift. |
| **Phase 3: Profile System** | M-22 through M-26 | Adds `system_class` and `operational_maturity` dimensions. Makes scaling explicit. |
| **Phase 4: Production Contracts** | M-27 through M-34 | Fills operational gaps through extension scope expansion and profile-gated obligations. No Core tier changes. |
| **Phase 5: Implementation Bridge** | M-35 through M-39 | Provides structured operation contracts, runtime specification, and conformance tooling. |
| **Phase 6: Documentation and Adoption** | M-40 through M-48 | Documentation, templates, generators, migration contracts, and hygiene for onboarding. |

---

> **Summary:** 48 atomic modifications organized in 6 implementation tiers. Tier 1 (M-01 through M-14) closes all source-visible contract gaps in the v6.3 YAML pair — these are release-blocking corrections. Tier 2 (M-15 through M-21) hardens governance and freezes the kernel. Tier 3 (M-22 through M-26) adds profile-driven scaling without Core expansion. Tier 4 (M-27 through M-34) fills production contract gaps through extension scope expansion and profile-gated obligations. Tier 5 (M-35 through M-39) bridges specification to implementation. Tier 6 (M-40 through M-48) accelerates adoption and addresses documentation hygiene.
>
> **Cross-Review Integration:** This revision incorporates validated insights from all three peer reviews:
> - **From `review.gemini.md`:** SSOT automation endorsement (-> M-15), content-as-required consensus (-> M-05), CIT-R7 freshness gap (-> M-10), manifest under-typing (-> M-11), DEPRECATED->ACTIVE guard gap (-> M-04), subtraction rule consensus (-> M-16), Express Mode inactive-tier gap (-> M-19), and ARE schema coupling observation (-> S6.3.1). Three Gemini recommendations were rejected after SSOT evaluation: Express Mode promotion to mandatory primary surface (conflicts with AX-4), semantic review decoupling from Core (would violate AX-3 and INV-7), and constraint precedence simplification (already implemented declaratively in 58 lines). Two were partially endorsed: UNBUNDLE protocol rationalization (diagnostic `ambiguous` signal preserved; deferred handling flagged for v6.4 review) and ARE schema abstraction (architectural fix identified; full extraction deferred due to tooling cost).
> - **From `review.codex.md`:** 51-item modification list validated; 42 items incorporated (items 1-15, 17, 19-51); 3 items rejected as already present in v6.3 or conflicting with SSOT; remaining items merged into the unified list with refinements. Unique contributions on `project` block ambiguity (-> M-45), errata governance (-> M-20), audit commentary hygiene (-> M-48), testing strategy (-> M-47), and mode consistency enforcement (-> M-46). The Codex review's 5-phase implementation sequence is compatible with and subsumed by the 6-phase sequence above.
>
> **Applied together, these 48 modifications transform DDR v6.3 from a finalized specification into a production-ready application design framework capable of governing projects from single-file developer scripts to multi-region enterprise platforms with hardware-aware constraint management, profile-driven operational readiness, and deterministic lifecycle enforcement.**
