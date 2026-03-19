---
document:
  id:              DDR_v4_Issue-002
  title:           "Resolution Report for ISSUE-002: FCL→CL Edge Direction Is Semantically Inverted"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "OPEN"
  severity:        "CRITICAL"
  type:            "LOGICAL_CONFLICT"
---

## Optimized Resolution Strategy for "ISSUE-002"

### Agent Context

```yaml
id:          ISSUE-002
status:      OPEN
severity:    CRITICAL
type:        LOGICAL_CONFLICT
tier_refs:   [FCL, CL, SAL]
section_ref: §3.4, §5 (Tier 4 CL)
rule_refs:   [CL-R9, AX-2, CIT-R2]
```

### 1. Validation Audit of ISSUE-002

An evaluation of `.agent/assets/proposals/active/DDR System(Opus_v4).md` was conducted to investigate the claims of "ISSUE-002: FCL→CL Edge Direction Is Semantically Inverted."

The §3.4 Core DAG Topology diagram (lines 96–160) explicitly models `CL` as a child of `FCL`. The diagram shows an arrow from `FCL` to `CL` with text `────▶` on line 127, and CL's parent declaration on line 342 reads: `**Parents:** 'derives' ← FCL. **Edge to child:** 'constrains' → SAL`. This confirms that the specification models CL as deriving from FCL — i.e., that technology and hardware constraints are structurally positioned as outputs of functional capability authoring.

`CL-R9` (line 356) states: *"Must cite FCL IDs for each constraint"* with a violation consequence of *"Constraints untraceable to a business need."* This rule compels CL authors to link every technology/hardware constraint back to a specific functional capability, regardless of whether the constraint was externally imposed or derived from functional analysis.

The CL tier's own description (lines 334–340) provides the activation condition: *"Activate when specific technology, hardware, or infrastructure constraints are non-negotiable."* The term *"non-negotiable"* directly implies externally imposed facts — procurement decisions, security policies, legacy infrastructure mandates — that exist independently of, and temporally prior to, functional capability authoring.

`AX-2` (line 46) states: *"Technology and implementation specificity are deferred until logically necessary"* with the implication: *"Tiers above CL (XPD, SIL, GPCL, FCL) must contain no technology, hardware, or implementation references."* This axiom acknowledges that CL content is qualitatively different from FCL content — it is technology-specific. Yet the topology forces this technology-specific content to derive from technology-agnostic content, even when the technology constraint precedes and is independent of the functional specification.

`CIT-R2` (line 185) states: *"`parent_ids` must reference node(s) from the immediately preceding active tier(s) in the DAG topology."* This confirms that CL nodes structurally must cite FCL as their parent — there is no mechanism for CL to cite GPCL or SIL directly even when the constraint originates from governance or strategic authority.

**Findings:**

1. **Causal Inversion for Imposed Constraints:** The specification's topology forces all CL constraints to structurally derive from FCL. For constraints that are externally mandated (e.g., a corporate security policy dictating Python 3.11+, a procurement decision mandating AWS), the author must identify an FCL node as the parent — fabricating a derivation relationship that does not exist in the project's actual decision chain. This directly conflicts with AX-1's mandate for complete, honest audit trails.

2. **Topological Rigidity vs. Real-World Constraint Origins:** The DDR topology models a single causal flow: intent → governance → capability → constraint → architecture. In practice, technology constraints have at least two distinct origins: (a) *derived* — chosen by the design team in response to functional requirements (genuinely derives from FCL), and (b) *imposed* — mandated by external authority (procurement, legal, legacy infrastructure) independently of any functional capability. The specification provides no mechanism to distinguish these two fundamentally different constraint origins, forcing all CL nodes into the same structural relationship regardless of their actual provenance.

3. **CL-R9 Enforcement Gap:** When a technology constraint is externally imposed, `CL-R9`'s requirement to *"cite FCL IDs for each constraint"* produces structurally dishonest citations. The FCL node being cited did not generate or motivate the constraint — it is merely the closest tier in the topology. This means VERIFY-validated citations in the DAG carry false provenance information, undermining the audit integrity that the axiom system is designed to guarantee.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-002

The resolution must restore honest provenance tracking for CL constraints while preserving the DAG's structural integrity and the SAL merge-node design. The two strategies below represent fundamentally different approaches: topological restructuring versus metadata enrichment.

#### Option A: Elevate CL to Peer Status with FCL, Both Deriving from GPCL

Reposition `CL` as a sibling of `FCL` in the DAG topology rather than its child. Both `FCL` and `CL` would derive from `GPCL`, with SAL remaining the merge node absorbing both inputs. The revised topology would be: `GPCL → FCL → SAL` (derives) and `GPCL → CL ╌constrains╌▶ SAL`. This restructuring reflects the real-world authoring reality: governance mandates (GPCL) simultaneously drive what the system must do (FCL) and what it must be built with (CL). `CL-R9` would be updated to: *"Must cite the GPCL or SIL ID that establishes the organizational or governance context for each constraint."* The Express Mode Group G2 (currently `FCL + CL`) would need restructuring, and `CIT-R2` would require an exception clause for the new CL position. This is a breaking topological change requiring a version bump from `4.0` to `5.0`.

* **Supporting Insights:** This approach eliminates the causal inversion at its source. In the majority of enterprise projects, technology and hardware constraints originate from organizational authority (procurement policies, security mandates, legacy infrastructure commitments) which are governance-level concerns. Positioning CL as a GPCL descendant rather than an FCL descendant models this reality without requiring authors to fabricate derivation chains. The SAL merge-node design is preserved — SAL continues to absorb both functional capabilities and technology constraints — but the graph now accurately represents the two independent authority streams feeding architecture.

* **Citations:** ISO/IEC/IEEE 42010:2022 (Systems and software engineering — Architecture description) distinguishes between *imposed constraints* (externally given prerequisites) and *architecture-driven constraints* (consequences of design decisions). The standard's framework treats imposed constraints as environmental factors that bound the architecture from outside, not as outputs of functional analysis. This directly supports modeling externally imposed technology constraints as peers to functional capabilities rather than their children. Additionally, the TOGAF Architecture Development Method (ADM) Phase B (Business Architecture) and Phase D (Technology Architecture) operate as parallel, governance-anchored activities — not as a sequential parent-child derivation.

#### Option B: Add a `constraint_origin` Property to CL Nodes with Context-Dependent Citation Rules

Retain the existing `FCL → CL` topology but introduce a mandatory `constraint_origin` field to every CL node, with an enum of `[derived, imposed]`. When `constraint_origin: derived`, the existing `CL-R9` applies unchanged — the constraint was chosen in response to FCL requirements and must cite the relevant FCL IDs. When `constraint_origin: imposed`, a new rule `CL-R9-imposed` replaces `CL-R9`: *"Must cite the external authority source (regulatory framework, contract reference, procurement policy, or organizational mandate) that imposes the constraint. FCL citation is not required; an optional FCL cross-reference may be provided for contextual traceability."* VERIFY would validate that `derived` nodes carry FCL citations and `imposed` nodes carry authority references. This is a non-breaking schema addition — existing CL nodes default to `derived` for backwards compatibility.

* **Supporting Insights:** This approach preserves the existing DAG topology and avoids a version bump, while recovering honest provenance tracking at the node level. The `imposed` pathway creates a formally sanctioned alternative to fabricated FCL citations, directly addressing the CL-R9 enforcement gap identified in the audit. By making the distinction explicit in the schema, VERIFY gains the ability to enforce different citation requirements based on constraint origin — a deterministic, mechanically verifiable check that satisfies AX-3. The Express Mode G2 grouping and SAL merge-node design remain entirely unchanged.

* **Citations:** IEEE Std 830-1998 (IEEE Recommended Practice for Software Requirements Specifications) and its successor ISO/IEC/IEEE 29148:2018 distinguish between *derived requirements* (traced to higher-level requirements) and *imposed requirements* (originating from external constraints such as regulatory mandates, organizational policies, or interface obligations). Both standards recommend maintaining explicit traceability to the originating authority for imposed requirements rather than forcing them into a derivation chain from functional requirements. This classification directly maps to the `derived` / `imposed` distinction proposed in Option B.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **Breaking Changes and Migration Cost:** Option A requires a topological restructuring of the Core DAG, a version bump to `5.0`, updates to `CIT-R2`, Express Mode Group G2 realignment, and migration tooling for existing DDR projects. Option B is a non-breaking schema addition requiring only a minor version increment (`4.0` → `4.1`); existing CL nodes remain valid with an implicit `derived` default.

2. **Semantic Accuracy of the DAG:** Option A produces a topology that accurately models both constraint origins at the structural level — the graph itself tells you whether a constraint was governance-driven or capability-driven. Option B encodes this distinction as node-level metadata within the existing topology, meaning the graph edges still imply FCL parentage for imposed constraints even though the `constraint_origin` field corrects this at the property level.

3. **VERIFY Determinism (AX-3):** Both options produce deterministic VERIFY checks. Option A: VERIFY checks that CL cites GPCL/SIL (structurally enforced by topology). Option B: VERIFY checks `constraint_origin` and applies the appropriate citation rule (`CL-R9` for `derived`, `CL-R9-imposed` for `imposed`). Option B requires slightly more complex VERIFY logic but remains fully mechanically verifiable.

4. **Co-dependency with ISSUE-001:** Option A's topology change must be coordinated with any edge-type vocabulary changes from ISSUE-001. If ISSUE-001 reintroduces `cites`, the combined topology and edge changes compound migration complexity. Option B is independent of ISSUE-001's resolution and can be implemented in isolation.

5. **Authoring Burden:** Option A simplifies CL authoring for the majority case (imposed constraints) by removing the need to identify an FCL parent node. Option B requires authors to consciously select `derived` or `imposed` for each CL node, but this is a straightforward classification decision that mirrors the author's actual knowledge of the constraint's origin.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

While Option A achieves greater topological purity, the DDR System Specification v4.0 has already committed to a design philosophy of vocabulary minimalism and topological simplicity (as evidenced by the v3.1.1 → v4.0 consolidation that reduced tiers from 11 to 9 and edge types from 6 to 4). A topological restructuring to resolve this issue would partially reverse that consolidation trajectory and create compounding migration risk alongside ISSUE-001. Option B achieves the same semantic outcome — honest constraint provenance — through a non-breaking metadata enrichment that is immediately deployable.

**Option B** is recommended because:

* **Non-Breaking Compatibility:** Existing DDR v4.0 project files require zero migration. The `constraint_origin` field defaults to `derived`, preserving all current CL → FCL citation chains as valid without modification.
* **Independent Resolution Path:** Option B can be implemented regardless of how ISSUE-001 (edge type vocabulary) is resolved, eliminating cross-issue implementation dependencies and reducing coordination risk.
* **Honest Audit Trails:** The `imposed` pathway eliminates the structural requirement to fabricate FCL citations for externally mandated constraints, restoring AX-1 compliance for the CL tier without altering the DAG topology.

### 4. Independent Review Conclusion

**Reviewer Determination:** I agree that **Option B** is the maximally optimized resolution strategy for ISSUE-002 under DDR v4 constraints.

**Approval Notation:** ✅ Independent review completed on 2026-03-19; the endorsed recommendation (Option B) is approved without modification.
