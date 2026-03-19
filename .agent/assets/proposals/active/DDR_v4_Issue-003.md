---
document:
  id:              DDR_v4_Issue-003
  title:           "Resolution Report for ISSUE-003: DAG Invariant Text Contradicts the Merge-Node Topology"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "OPEN"
  severity:        "MAJOR"
  type:            "LOGICAL_CONFLICT"
---

## Optimized Resolution Strategy for "ISSUE-003"

### Agent Context

```yaml
id:          ISSUE-003
status:      OPEN
severity:    MAJOR
type:        LOGICAL_CONFLICT
tier_refs:   [SAL]
section_ref: §3.5
rule_refs:   [INV-2, SAL-R6, CIT-R2]
```

### 1. Validation Audit of ISSUE-003

An evaluation of `.agent/assets/proposals/active/DDR System(Opus_v4).md` was conducted to investigate the claims of "ISSUE-003: DAG Invariant Text Contradicts the Merge-Node Topology."

The §3.5 DAG Invariants section (line 165) contains the normative bullet: *"No tier-skipping: each citation references exactly one active tier above in the derivation path."* The phrase "exactly one active tier above" is unambiguous — it permits a single parent tier per citation chain, with no provision for exceptions.

The §3.4 Core DAG Topology diagram (lines 96–160) explicitly labels SAL as a "Constraint merge point" (line 135) and models two incoming edges: `derives` from FCL (line 123: "derives (always)") and `constrains` from CL (line 131). The SAL tier specification at line 373 confirms: *"Merge node. SAL must satisfy all incoming constraints simultaneously."* The parent declaration at line 375 reads: *"Parents: `derives` ← FCL (always); `constrains` ← CL (if active)."* This unambiguously establishes SAL as receiving citations from two distinct tiers simultaneously.

`SAL-R6` (line 386) states: *"Must cite all active parent IDs (FCL + CL if active) for each major architectural decision."* This rule normatively requires SAL nodes to carry parent citations from both FCL and CL when the Constraint Layer is active — directly contradicting the "exactly one active tier above" invariant in §3.5.

`CIT-R2` (line 185) states: *"`parent_ids` must reference node(s) from the immediately preceding active tier(s) in the DAG topology."* The plural "tier(s)" in `CIT-R2` implicitly accommodates the SAL merge-node design, but §3.5's invariant uses the singular "one active tier," creating a normative conflict within the same specification.

The Issues Tracker references a YAML-side correction via `INV-2`: *"Exception: FCL→SAL derives edge is always valid regardless of CL activation state (SAL merge-node design; see §3.4, Audit C-2)."* However, the Markdown specification — which the document header declares as the "exclusive normative specification" (line 14) — contains no such exception text. The `.agent/assets/proposals/active/report-conversion-fidelity.md` (line 92) independently confirms: *"C-2: FCL→SAL tier-skip exception undocumented"* and notes that the YAML `dag_invariants[id=INV-2]` encodes the exception, but the Markdown does not.

The `.agent/assets/proposals/active/DDR_v4_Adversarial_Audit.md` (line 99–105) independently flagged this same contradiction, noting: *"The invariant states: 'No tier-skipping: each citation references exactly one active tier above in the derivation path'"* and recommending an update to §3.5 bullet 2.

**Findings:**

1. **Normative Self-Contradiction:** The §3.5 invariant ("exactly one active tier above") and the §3.4/SAL-R6 merge-node design ("cite all active parent IDs: FCL + CL") are mutually exclusive statements within the same normative document. A validator implementing §3.5 verbatim will reject every compliant SAL node that correctly cites both FCL and CL parents, producing false structural violations. This is not an ambiguity — it is a direct logical contradiction between two normative requirements.

2. **Markdown–YAML Normative Divergence:** The YAML encoding resolves the contradiction via `INV-2`, but the Markdown specification — declared as the "exclusive normative specification" in its own header — contains no corresponding exception. In a system that claims Single Source of Truth status, having two canonical formats produce contradictory normative rules on a structural invariant constitutes a specification integrity failure by the system's own declared standards.

3. **Independent Corroboration:** Both the `report-conversion-fidelity.md` audit (Audit C-2) and the `DDR_v4_Adversarial_Audit.md` analysis independently identified and flagged this same contradiction, confirming the issue is reproducible and not an artifact of interpretive ambiguity. The convergence of three independent analyses on the same defect establishes high confidence in the finding.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-003

The resolution must eliminate the normative contradiction between §3.5 and the SAL merge-node design while establishing a clear authority hierarchy for cases where the Markdown specification and YAML encoding diverge.

#### Option A: Correct §3.5 Invariant Language with an Explicit, Exhaustive Exception

Amend the §3.5 DAG Invariants section by replacing bullet 2 with language that explicitly encodes the SAL merge-node exception:

> *"No tier-skipping: each citation references the immediately preceding active tier(s) in the derivation path. Exception: SAL is a merge node (§3.4) that simultaneously derives from FCL and is constrained by CL when active. SAL is therefore the only tier that validly carries parent citations from two distinct tiers. This exception is exhaustive; no other tier may carry citations from more than one immediately preceding tier."*

Following the amendment, the `INV-2` exception annotation in the YAML becomes redundant and should be removed or converted to a cross-reference to §3.5. The Markdown remains the authoritative normative source, and the YAML serves as its machine-parseable encoding. `CIT-R2` requires no change — its existing "tier(s)" plural already accommodates the corrected §3.5 language. This constitutes a minor version increment (`4.0` → `4.1`).

* **Supporting Insights:** This approach resolves the contradiction at its source — the Markdown normative text — preserving the specification's declared authority model where the Markdown document is the "exclusive normative specification." By making the exception exhaustive and explicitly scoped to SAL, it prevents future over-generalization while providing implementors with unambiguous guidance. The corrected invariant text aligns with the existing `CIT-R2` language and the §3.4 topology diagram, creating internal consistency across all three representations of the same structural rule.

* **Citations:** ISO/IEC/IEEE 42010:2022 (Systems and software engineering — Architecture description) specifies "correspondence rules" as the mechanism for expressing and enforcing architectural relationships, including consistency constraints between different views of the same architecture. The standard mandates that conflicts between normative figures and normative text be resolved in favour of the text (Clause 4). This principle directly supports correcting the §3.5 normative text to align with the established topology diagram and tier rules, rather than relying on a YAML-side annotation to override prose invariants. Additionally, IETF RFC 2119 (Key words for use in RFCs to Indicate Requirement Levels) establishes that normative language must be precise and unambiguous; the current §3.5 bullet's use of "exactly one" when the system requires "one or two" constitutes a normative precision failure by RFC 2119 standards.

#### Option B: Establish a Formal Document Authority Policy with YAML as the Canonical Source for Machine-Verifiable Rules

Introduce a new `§0 Document Authority Policy` section at the beginning of the specification that formally declares: *"In the event of any conflict between the Markdown specification and the YAML encoding, the YAML encoding is authoritative for all machine-verifiable structural rules. The Markdown is a human-readable rendering."* Under this policy, `INV-2` in the YAML becomes the canonical definition of the tier-skipping invariant, including the SAL merge-node exception. The §3.5 bullet 2 in the Markdown is replaced with a simplified cross-reference: *"See `dag_invariants.INV-2` in ddr_system_v4_0.yaml for the complete invariant definition including the SAL merge-node exception."*

This approach eliminates the possibility of future Markdown–YAML divergence for all machine-verifiable rules by design, not just for this specific invariant. Validators parse the YAML directly; human readers consult the Markdown for narrative context but defer to the YAML for structural definitions. This requires a minor version increment (`4.0` → `4.1`) and an update to the document header to replace the "exclusive normative specification" claim with a nuanced authority policy.

* **Supporting Insights:** The DDR System is designed for agentic workflows where automated validators (VERIFY, VALIDATE) parse machine-readable schemas, not Markdown prose. Making the YAML authoritative for structural rules aligns the authority model with the actual consumption pattern: agents read YAML, humans read Markdown. This eliminates an entire class of potential future contradictions — any Markdown–YAML divergence for machine-verifiable rules is resolved by definition, rather than requiring per-case amendments like Option A. The trade-off is a philosophical shift: the Markdown ceases to be the "real" specification for structural invariants and becomes a rendering layer.

* **Citations:** The IETF's approach to dual-format specifications provides relevant precedent. RFC 9512 (YAML Media Type) establishes YAML as a standardised machine-readable format suitable for encoding normative content alongside human-readable prose. The FedRAMP program's RFC for machine-readable authorization packages (using OSCAL format) explicitly establishes a dual-authority model where machine-readable formats carry normative weight for automated compliance checking, while human-readable versions serve interpretive and review purposes. This model directly maps to the Markdown (human) / YAML (machine) dual-format architecture of the DDR specification.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **Scope of Fix:** Option A surgically corrects a single invariant statement in §3.5, resolving this specific contradiction without altering the specification's broader authority model. Option B resolves this specific contradiction as a consequence of a systemic authority policy change that prevents all future Markdown–YAML divergences for machine-verifiable rules. Option A is a local fix; Option B is a structural reform.

2. **Consistency with the Declared Authority Model:** The specification header declares the Markdown as the "exclusive normative specification" (line 14). Option A preserves this declaration by correcting the Markdown text. Option B contradicts and replaces this declaration by elevating the YAML to co-normative (or primary-normative) status for structural rules, requiring removal of the "exclusive" claim from the header.

3. **Future Divergence Risk:** Option A resolves only this invariant. If the Markdown and YAML diverge on other structural rules in the future, each divergence requires its own correction — the same class of error can recur. Option B eliminates future divergence for all machine-verifiable rules by design, but introduces a new risk: the Markdown may drift from the YAML as a human-readable rendering without normative checks, potentially creating confusion for human readers who treat the Markdown as authoritative.

4. **Implementation Complexity:** Option A requires editing one bullet point in §3.5 and optionally simplifying the `INV-2` YAML annotation. Option B requires: a new §0 section, updates to the document header, a policy framework for classifying which rules are "machine-verifiable," and a cultural shift in how stakeholders interact with the specification.

5. **Agentic Workflow Alignment:** Option B is better aligned with the DDR's target deployment in Antigravity-based agentic workflows, where automated validators consume the YAML directly. Option A maintains a model where agents must parse Markdown prose to extract invariant definitions, which is less deterministic than YAML parsing.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

While Option B offers a compelling long-term architectural advantage for agentic workflows, it requires replacing the specification's foundational authority claim — a decision with governance implications that extend well beyond the scope of this single issue. The DDR System's own design philosophy prioritises minimising design complexity (§1, constraint 1) and avoiding premature optimisation (§1, constraint 2). Introducing a systemic authority policy to resolve a single invariant contradiction would be a disproportionate structural change. Option A resolves the contradiction completely, immediately, and without altering the specification's approved authority model.

**Option A** is recommended because:

* **Minimal Disruption:** The fix requires editing a single bullet point in §3.5. No new sections, no policy frameworks, no changes to the document header's authority declaration. Existing validators and tools that parse the Markdown are corrected by the text change alone.
* **Internal Consistency:** The corrected §3.5 text aligns with the existing `CIT-R2` plural "tier(s)", the §3.4 topology diagram's merge-node label, the SAL tier specification's parent declaration (line 375), and `SAL-R6`'s citation requirement — establishing consistency across all four representations of the same structural rule within the Markdown itself.
* **Exhaustive Scoping:** The exception is explicitly declared as exhaustive and limited to SAL. This prevents future implementors from inferring that other tiers might also carry multi-tier citations, preserving the strength of the no-tier-skipping invariant for all non-merge-node tiers.
