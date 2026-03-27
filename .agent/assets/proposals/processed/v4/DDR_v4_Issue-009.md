---
document:
  id:              DDR_v4_Issue-009
  title:           "Resolution Report for ISSUE-009: ARE Confidence Score Has No Normative Rubric"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "RESOLVED"
  severity:        "MODERATE"
  type:            "DESIGN_INADEQUACY"
---

## Optimized Resolution Strategy for "ISSUE-009"

### Agent Context

```yaml
id:          ISSUE-009
status:      RESOLVED
severity:    MODERATE
type:        DESIGN_INADEQUACY
tier_refs:   [ARE_E5]
section_ref: §9 (E5 ARE)
rule_refs:   [AX-3, ARE-R2]
```

### 1. Validation Audit of ISSUE-009

An evaluation of `DDR System(Opus_v4).md` (§2, §8.2, §9, §11) and `ddr_system_v4.0.yaml` (§9 extension_catalog, §8 candidate_pool, §11 compliance_checklist) was conducted to investigate the claims of "ISSUE-009: ARE Confidence Score Has No Normative Rubric."

The specification defines `ARE-R2` in §9 Extension E5 as: *"Each candidate carries `ARE::confidence_score` (0.0–1.0) derived from source evidence quality"* (`DDR System(Opus_v4).md`, line 649; `ddr_system_v4.0.yaml`, lines 1205–1208). The phrase "source evidence quality" is the sole derivation instruction — no further elaboration exists in either the Markdown specification or the YAML encoding. A full-text search for `confidence_score`, `score_band`, `scoring_rubric`, `minimum_threshold`, and `promotion_threshold` across both source files yields zero additional definitions beyond the single `ARE-R2` statement.

The Candidate Pool mechanism (§8.2, `DDR System(Opus_v4).md`, lines 571–579; `ddr_system_v4.0.yaml`, lines 1063–1075) defines staging semantics — `status: CANDIDATE`, visibility rules, promotion via INSERT — but specifies no quality gate that references the confidence score. The §11 CLEAN compliance checklist entry for ARE (`DDR System(Opus_v4).md`, line 810; `ddr_system_v4.0.yaml`, lines 1351–1353) states only: *"ARE-generated candidates reviewed and either promoted via INSERT or discarded."* No minimum confidence threshold conditions this review.

`AX-3` (§2, `DDR System(Opus_v4).md`, line 47) requires: *"Identical inputs produce unambiguous, mechanically verifiable outputs."* A confidence score derived from an undefined rubric cannot satisfy this axiom — two conforming ARE implementations processing identical input DAGs will produce non-comparable scores with no mechanism for adjudication.

**Findings:**

1. **Absent Scoring Rubric:** `ARE-R2` mandates a confidence score in the range `[0.0, 1.0]` but provides no normative definition of input signals, weighting, or aggregation method. The phrase "source evidence quality" is semantically opaque — it does not enumerate which properties of source nodes (count, tier diversity, content specificity, corroboration across tiers) constitute "quality." This renders the score non-reproducible across implementations, directly violating `AX-3`.

2. **Missing Score Interpretation Framework:** No score band definitions exist anywhere in the specification. A practitioner reviewing a Candidate Pool node with `ARE::confidence_score: 0.52` has no normative guidance on whether this represents adequate evidence for promotion, marginal evidence requiring additional review, or speculative inference that should be discarded. The absence of band labels and threshold values makes the score operationally meaningless for promotion decisions.

3. **No Quality Gate at Promotion Boundary:** The §11 compliance checklist and the Candidate Pool promotion mechanism (§8.2) require only that candidates are "reviewed and either promoted or discarded." No structural check links the confidence score to the promotion decision. A candidate with `ARE::confidence_score: 0.05` can be promoted via INSERT to become a Core node with the same procedural pathway as one scored at `0.95`, undermining the score's intended purpose as a quality signal.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-009

The resolution must define a normative scoring framework that makes `ARE::confidence_score` deterministic, interpretable, and structurally integrated into the Candidate Pool promotion pathway — without over-constraining domain-specific ARE implementations.

#### Option A: Define a Fixed Normative Scoring Schema in §9

Extend `ARE-R2` with a mandatory scoring appendix specifying: (1) enumerated input signals with categorical weights, (2) score band definitions with action labels, and (3) a minimum surfacing threshold. The rubric would define concrete signals — such as direct source node count, cross-tier convergence, ICL contract corroboration, and SAL pattern alignment — each assigned a weight category (`high`, `medium`, `low`). Score bands would partition the `[0.0, 1.0]` range into labelled zones (e.g., `speculative` for `[0.0, 0.4)`, `probable` for `[0.4, 0.7)`, `high_confidence` for `[0.7, 1.0]`) with normative promotion guidance per band. A fixed minimum surfacing threshold (e.g., `0.35`) would prevent extremely low-confidence candidates from entering the review queue without an explicit override flag.

This approach makes every ARE implementation produce scores on a common scale with shared interpretation semantics. VERIFY can structurally validate that promoted candidates met the minimum threshold or carried an explicit override. The rubric becomes part of the specification itself, ensuring universal baseline consistency.

* **Supporting Insights:** The DDR System's foundational axiom `AX-3` (Determinism) explicitly requires that identical inputs produce mechanically verifiable outputs. A fixed rubric is the most direct satisfaction of this axiom for confidence scoring — it eliminates implementation-specific interpretation entirely. The specification's existing pattern of normative rule tables (e.g., atomic inclusion rules per tier) demonstrates that DDR favors explicit enumeration over delegated interpretation.

* **Citations:** ISO/IEC 23053:2022 ("Framework for Artificial Intelligence Systems Using Machine Learning") establishes that AI system outputs require defined evaluation criteria to be trustworthy and auditable. ISO/IEC 25010:2023 ("Software Product Quality — Quality Model") provides a framework for defining measurable quality characteristics with explicit sub-characteristics and measurement methods, supporting the approach of decomposing "source evidence quality" into enumerated, measurable signals.

#### Option B: Delegate Scoring to Configurable, Declared Scoring Profiles

Rather than embedding a fixed rubric, define `ARE-R2` as requiring each ARE deployment to declare a `scoring_profile` in its Extension contract. The specification would ship standard profiles (e.g., `standard_v1` with a moderate threshold, `conservative_v1` with stricter thresholds for regulated environments) while permitting `custom` profiles that must explicitly declare their signals, bands, and minimum surfacing threshold. Any ARE implementation must declare which profile it uses; the profile definition becomes part of the machine-readable Extension contract, making it auditable by VERIFY.

The `standard_v1` profile would contain the same rubric content as Option A, serving as the default baseline. The `conservative_v1` profile would raise the minimum surfacing threshold and tighten band boundaries for environments with lower risk tolerance. Custom profiles must declare all constituent fields — signals, weights, bands, and thresholds — or fail contract validation. This approach preserves `AX-3` determinism within any given profile while allowing domain-specific adaptation.

* **Supporting Insights:** The DDR Extension System architecture (§8) already establishes a pattern of contract-based integration — each Extension declares its contract version, read tiers, and annotated tiers via `EXT-R1` and `EXT-R2`. Extending this contract pattern to include a scoring profile is architecturally consistent. The specification's own precedent with configurable activation (XPD and CL are conditionally activatable; Express Mode groups are selectable) demonstrates that DDR supports parameterized behavior within normative boundaries.

* **Citations:** ISO/IEC 25010:2023 explicitly permits tailoring of quality models, stating that conforming evaluations may "tailor the quality model, giving the rationale for any changes and providing a mapping between the tailored model and the standard model." This directly validates the profile-based approach where standard and custom profiles coexist within a normative framework. ISO/IEC 42001 ("AI Management System Standard") requires documented monitoring processes for AI systems with context-appropriate evaluation criteria, supporting the principle that scoring parameters should be declared and auditable rather than hardcoded universally.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **AX-3 Determinism Compliance:** Option A achieves universal determinism — all ARE implementations produce scores on an identical scale using identical signals. Option B achieves determinism within a declared profile but permits cross-implementation divergence when different profiles are selected. Both satisfy the axiom's letter; Option A satisfies its spirit more completely by eliminating the profile-selection variable.

2. **Domain Adaptability:** Option A imposes a single rubric that may not align with all deployment contexts — a safety-critical system may require stricter thresholds than a prototyping environment, while a domain with sparse lower-tier documentation may weight signals differently. Option B accommodates these variations through profile selection without specification amendments. For the DDR System's stated universality goal (`AX-4`), Option B provides broader applicability.

3. **Specification Maintenance Cost:** Option A embeds scoring logic directly in the specification, meaning any refinement to signal weights or band boundaries requires a specification version change. Option B isolates scoring parameters in profile definitions — standard profiles can be updated as appendix revisions without modifying the core rule text, reducing long-term maintenance overhead.

4. **Implementation Complexity:** Option A is simpler to implement — every ARE reads one fixed rubric. Option B requires profile resolution logic, profile validation against a schema, and contract-level enforcement of profile completeness. However, this additional complexity is consistent with the existing Extension contract validation pattern already required by `EXT-R1` through `EXT-R7`.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

Option B subsumes Option A by shipping the fixed rubric as the `standard_v1` profile while preserving the flexibility demanded by `AX-4` (Universality) and the Extension System's contract-based architecture. It aligns with the specification's existing parameterization patterns and minimizes long-term maintenance cost.

**Option B** is recommended because:

* **Subsumption of Option A:** The `standard_v1` profile contains the identical rubric proposed in Option A, ensuring that the universal baseline exists as a concrete, usable default. No functionality is lost.
* **Architectural Consistency:** The profile declaration extends the existing Extension contract pattern (`EXT-R1`, `EXT-R2`), requiring no new structural concepts. VERIFY can validate profile completeness using the same contract-checking logic already required for Extension integration.
* **AX-4 Universality Alignment:** A fixed rubric optimized for one domain (e.g., enterprise software) may produce systematically misleading scores in another (e.g., embedded systems with sparse ICL contracts). Profile-based scoring allows each deployment to declare context-appropriate evaluation criteria while remaining normatively auditable.
* **Reduced Specification Churn:** Profile definitions are appendix-level content that can be versioned independently of the core `ARE-R2` rule text, reducing the frequency of specification version bumps for scoring refinements.
* **Regulatory Readiness:** The `conservative_v1` profile provides a pre-built option for regulated environments (ISO 9001, IEC 62443, SOC 2) where higher confidence thresholds and stricter band definitions are expected, without requiring custom profile authoring.

### 4. Final Reviewer Notation

**Reviewer Conclusion (2026-03-19): APPROVED.**  
After review of ISSUE-009, the proposed strategies, and the endorsed recommendation, I confirm that **Option B remains the maximally optimized resolution strategy** for this issue under DDR v4.0 constraints. The recommendation is approved without modification.