
# DDR System v4.0 — Logic Audit Report

---

## ⛔ CRITICAL — Specification Correctness Failures

These issues contradict normative text elsewhere in the document or produce mechanically unresolvable conflicts.

---

### C-1 · §1.1 Change Table — Incorrect Description of HIL Absorption

**Location:** Section 1.1, "Tier count" row, Rationale column.

**The defect:** The rationale states *"HIL absorbed into TDL as a unified Constraint Layer."* This is factually incorrect. Appendix B explicitly shows both HIL and TDL as **independent source tiers** that were each absorbed into the new CL. HIL was not absorbed into TDL; both were absorbed into CL in parallel. The phrasing implies a two-step merger (HIL→TDL, then TDL→CL) that never occurred and is directly contradicted by the migration table.

**Why it matters:** This is the specification's own rationale for one of its structural changes. A reader implementing or validating the migration would mis-trace the HIL rules and potentially conclude that TDL-level rules take precedence over HIL-level rules within CL, since TDL was the "absorbing" tier in the stated sequence.

**Recommendations:**

1. Correct the Rationale cell to read: *"HIL and TDL unified into the new CL; HIL hardware constraints and TDL technology constraints become CL-R6–CL-R8 and CL-R1–CL-R5 respectively."*
2. Add a footnote cross-referencing Appendix B directly from this cell, so the change table and migration table are always read in conjunction and any future discrepancy is immediately visible.

---

### C-2 · §3.5 No-Tier-Skipping Invariant Conflicts with FCL→SAL "Always" Edge

**Location:** Section 3.5 (DAG Invariants), Section 3.4 (topology diagram), FCL Tier specification, SAL-R6.

**The defect:** §3.5 states *"No tier-skipping: each citation references exactly one active tier above in the derivation path."* However, when CL is active, the tier sequence is FCL → CL → SAL. The topology diagram and FCL's tier spec both mandate that FCL **always** derives directly to SAL. This means SAL holds a `parent_id` reference to FCL even when CL occupies the intermediate tier, making FCL two tiers above SAL in the active topology — a tier-skip by the spec's own definition.

SAL-R6 ("Must cite all active parent IDs: FCL + CL if active") enshrines this two-parent pattern as a mandatory rule, but never reconciles it with the no-tier-skipping invariant. The invariant and the rule directly contradict each other.

**Why it matters:** An automated VERIFY implementation would have to choose whether to flag FCL→SAL (when CL is active) as a tier-skip violation. AX-3 (Determinism) demands this be unambiguous. Currently it is not.

**Recommendations:**

1. Add an explicit numbered exception to the no-tier-skipping invariant in §3.5: *"Exception: The FCL→SAL derives edge is always valid regardless of CL activation state, because FCL provides the functional derivation lineage independently of CL's constraint lineage. This dual-parent pattern at SAL is the intended design, not a tier-skip."*
2. Add a normative note in the SAL tier specification and the VERIFY operation description stating that a SAL node carrying both FCL and CL as `parent_ids` is structurally valid and must not trigger a tier-skip violation.

---

### C-3 · Appendix B — ORL Rule Count Mismatch Labeled "1:1" with Unresolved "TBD" in a Finalized Document

**Location:** Appendix B, Rule-Level Cross-Reference table, first row.

**The defect:** The row maps "ORL-R1 through ORL-R4, ORL-R7" (five rules) to "GPCL-R6, GPCL-R7, GPCL-R8, GPCL-R10" (four destinations) with a Consolidation Status of **"1:1 / TBD."** Three compounding issues are present simultaneously:

- **Arithmetic failure:** Five source rules cannot have a 1:1 mapping to four destinations without at least one consolidation. The "1:1" label is arithmetically false.
- **Unresolved TBD:** The document's Status field is **"Finalized."** A Finalized normative specification must not contain unresolved TBD items, particularly in a migration table that is the authoritative record of rule lineage.
- **Missing ORL-R7 destination clarity:** ORL-R7 is grouped with R1–R4 but is not individually listed in the migration table the way ORL-R5 and ORL-R6 are. Its individual mapping is unconfirmed.

**Why it matters:** Appendix B is the authoritative migration record per the "Migration Policy" note. An incomplete or incorrect cross-reference breaks the traceability chain that AX-1 mandates for the entire system — ironically, in the document that governs traceability.

**Recommendations:**

1. Expand the first row into individual entries for ORL-R1, R2, R3, R4, and R7 separately, with explicit destination GPCL rule IDs and a resolved (not TBD) consolidation status for each, matching the level of detail given to ORL-R5 and ORL-R6.
2. Establish a gating policy stating that the document Status field may not be set to "Finalized" while any cell in Appendix B contains "TBD." Add this as a line item in the §11 Compliance Checklist under a new "Migration Integrity" category.

---

## 🔴 HIGH — Missing Mechanisms and Semantic Gaps

These issues do not break the spec's stated invariants but leave normatively required behaviors undefined or under-specified, making deterministic implementation impossible in the affected areas.

---

### H-1 · No Formal Status State Transition Model

**Location:** §3.1 (Node Schema), §7.1 (Operations), §7.2 (Dirty Flag footnotes).

**The defect:** The spec defines five status values (DRAFT, ACTIVE, DIRTY, DEPRECATED, SUPERSEDED) but never provides a formal state transition model. Allowed transitions are scattered across operation descriptions and footnotes:

- The only place DEPRECATED is set is in a §7.2 footnote ("A node is set to DEPRECATED via MODIFY").
- MODIFY's formal definition says only "Update content; version incremented" — status mutation is not part of its formal contract.
- Whether DIRTY → DEPRECATED is allowed (a DIRTY node scheduled for removal), or whether DRAFT → DEPRECATED is allowed, is never addressed.
- Whether a SUPERSEDED node can be set to DEPRECATED (e.g., for audit purposes) is undefined.

AX-3 (Determinism) requires unambiguous, mechanically verifiable behavior. A status field without a formal transition table is non-deterministic by omission.

**Recommendations:**

1. Add a §3.1.1 "Status Transition Model" table enumerating all valid (From → To) status transitions, the operation that triggers each, and any preconditions (e.g., "DIRTY → DEPRECATED requires that all children have a valid alternative parent before DEPRECATED is set").
2. Update the MODIFY operation's formal description in §7.1 to explicitly list status transitions it can perform, so that MODIFY's contract is self-contained and does not depend on a footnote for completeness.

---

### H-2 · UNBUNDLE "Reject" Behavior is Undefined

**Location:** §4, UNBUNDLE Determinism Rule.

**The defect:** The rule states: *"The UNBUNDLE operation must reject content that cannot be unambiguously assigned to a constituent tier."* But "reject" is never defined. Critical questions left open:

- Does rejection abort the entire UNBUNDLE operation (atomic failure), or does it perform a partial UNBUNDLE and flag the ambiguous content?
- What status does the group node carry after a rejection — does it remain in Express Mode as-is, or does it enter DIRTY?
- Is the rejection surfaced as a VERIFY violation, an operation error, or a manifest advisory?
- Does rejected content require manual resolution before UNBUNDLE can be re-attempted?

Given that UNBUNDLE auto-wires `parent_ids` (a structural mutation), a partial-failure mode could leave the DAG in an inconsistent intermediate state, directly violating AX-3.

**Recommendations:**

1. Define UNBUNDLE as **atomically all-or-nothing**: if any content cannot be unambiguously assigned, the entire UNBUNDLE fails with no state changes applied, the group node remains in its pre-UNBUNDLE state, and the operation returns an itemized list of unassignable content blocks. Add this to the §7.1 operation table's Validation Trigger column.
2. Add an explicit precondition to UNBUNDLE: all Express Mode content within the target group must carry valid tier-prefix annotations before UNBUNDLE may be invoked. Make annotation completeness a VALIDATE-checkable condition for Express Mode group nodes.

---

### H-3 · DRAFT Node Behavior Under DIRTY Propagation is Unspecified

**Location:** §7.2 (Dirty Flag Triggers), §7.2 footnote "Node Insertion."

**The defect:** §7.2 states that MODIFY of a parent sets the modified node plus **all descendants** to DIRTY. §7.2's footnote establishes that DRAFT nodes are "structurally present in the DAG but excluded from CLEAN compliance checks." The spec does not resolve whether DRAFT descendants receive DIRTY propagation from a parent MODIFY. Two incompatible interpretations are possible:

- **Interpretation A:** DRAFT nodes receive DIRTY (consistent with "all descendants"), but since they're excluded from CLEAN checks, the DIRTY status has no observable effect until they transition to ACTIVE.
- **Interpretation B:** DIRTY propagation stops at DRAFT nodes (since they're not subject to CLEAN checks, flagging them DIRTY is meaningless overhead).

These interpretations produce different behavior when a DRAFT node's parent is modified and the DRAFT node is then independently validated and set to ACTIVE: under Interpretation A the node is already DIRTY and requires re-validation; under Interpretation B it is not.

**Recommendations:**

1. Add a line to the §7.2 Dirty Flag Triggers table: "DRAFT nodes: DIRTY propagation applies. A DRAFT node set to DIRTY must be re-validated (VALIDATE operation) before it may transition to ACTIVE." This eliminates ambiguity and aligns with the principle that validation at ACTIVE transition must reflect the current state of all parents.
2. Alternatively, add DRAFT as an explicit exclusion from propagation and add a precondition to the DRAFT → ACTIVE transition: *"The VALIDATE operation performed to promote DRAFT → ACTIVE must be performed after the most recent MODIFY of any ancestor node."*

---

### H-4 · CIT-R4 Enforcement Post-DELETE Leaves Stale Inline Citations Unaddressed

**Location:** §3.7 (CIT-R4), §7.1 (DELETE operation).

**The defect:** CIT-R4 states: *"An inline [TIER-N.M] citation in node content must have a matching entry in parent_ids."* The DELETE operation cascades orphan detection to children and removes the deleted node's ID from valid `parent_ids`. However, no rule requires that inline [TIER-N.M] text citations within the content body of surviving child nodes be reconciled. A child node whose parent was deleted will have its `parent_id` entry removed (satisfying the DELETE cascade), but the inline text citation `[PARENT-N.M]` may persist in the content body, creating a CIT-R4 violation that the VERIFY operation's orphan detection may not surface separately from structural orphan checks.

**Recommendations:**

1. Amend the DELETE operation's validation trigger in §7.1 to explicitly include: *"Scan surviving children's content bodies for inline citations referencing the deleted node ID; flag each as a CIT-R4 violation in the reconciliation manifest's pending items list."*
2. Amend the VERIFY operation to distinguish between two violation types in its output: **structural orphan** (missing `parent_id`) and **content citation orphan** (inline `[TIER-N.M]` citation with no matching `parent_id`), with separate rule IDs reported, so remediation actions can be targeted correctly.

---

## 🟡 MODERATE — Logical Inconsistencies and Missing Rules

These issues represent internal inconsistencies in policy or missing normative coverage for scenarios the spec implicitly allows.

---

### M-1 · Extension Annotation Scope Policy is Inconsistently Applied: DDE Annotates FCL Without Stated Rationale While ARE is Explicitly Restricted

**Location:** §8.5 ARE note; §9 E5 (ARE), §9 E7 (DDE).

**The defect:** The ARE extension carries an explicit normative restriction: *"ARE annotation is restricted to tiers at or below SAL (SAL, ICL, CDL, ISL)."* The rationale is clear — AI-inferred annotations must not influence intent, governance, ethical, or functional tiers. However, E7 (DDE) declares it annotates FCL (Tier 3, above SAL) without any stated rationale for why this exception is acceptable. No general policy governing which Extensions may or may not annotate above-SAL tiers is ever stated. A reader implementing a new Extension has no principled basis for determining whether annotating FCL, GPCL, SIL, or XPD is permissible for their Extension.

**Recommendations:**

1. Add a general Extension annotation policy rule in §8.1 (or §8.3 as EXT-R8): *"Extensions that perform automated inference or generation (ARE, HRE, DDE) must declare the highest-tier annotation target and provide rationale. Annotation of XPD, SIL, GPCL, or FCL requires explicit justification in the Extension's contract declaration."*
2. Add a sentence to DDE's §9 entry explaining why FCL annotation is appropriate (e.g., "DDE annotates FCL to flag functional capabilities that imply data domain schemas not yet formally specified in ICL — this is a forward-reference advisory, not inference about intent") so the reasoning is auditable.

---

### M-2 · Architecture Diagram (§10) Conflates "reads" and "annotates" in `extends` Edges, Making EXT-R2 Compliance Unverifiable from the Diagram

**Location:** §10 (Mermaid diagram), §8.3 EXT-R2.

**The defect:** EXT-R2 requires Extensions to declare which tiers they **read** and which they **annotate** separately. The Mermaid diagram renders all Extension-to-Core relationships as a single `extends` edge type with no visual distinction between read-only and annotation relationships. For example, ORE reads GPCL, ICL, CDL but annotates only ISL and SAL — but the diagram only shows `extends` edges to ISL and SAL, making it appear ORE does not read the other tiers at all. A user consulting the diagram alone cannot verify EXT-R2 compliance for any Extension.

**Recommendations:**

1. Use two distinct edge styles in the Mermaid diagram: `-.reads.->` (dotted, no fill arrowhead) and `-..annotates..->` (dotted, filled arrowhead), with a legend entry for each. This makes EXT-R2's read vs. annotate distinction visually auditable from the diagram.
2. Add a tabular summary of all Extensions' read and annotate tier sets in §8.3 or §9 (e.g., a matrix: Extensions × Tiers with R/A/— per cell), making EXT-R2 compliance checkable without parsing nine individual Extension contracts.

---

### M-3 · No FCL-Level Rule Governs the Conditions or Content of the FCL→CL Derivation Edge

**Location:** FCL Tier specification (§5, Tier 3), CL Tier specification (§5, Tier 4).

**The defect:** The FCL tier spec declares *"Edge to children: derives → SAL (always); derives → CL (if CL active)."* But no FCL inclusion or exclusion rule governs what content within an FCL node triggers or characterizes the FCL→CL derivation. All six FCL-R rules address user-observable behavior description; none addresses the condition under which FCL content necessitates CL activation or how to document within an FCL node that a capability has technology/hardware implications. This leaves CL activation criteria entirely implicit.

**Recommendations:**

1. Add FCL-R7: *"FCL nodes that directly imply non-negotiable technology, hardware, or infrastructure constraints (e.g., a capability that requires GPU processing, real-time streaming, or specific OS features) must be explicitly annotated to indicate CL activation necessity. This annotation must appear in the FCL node's content body as a structured note, not as implementation detail."*
2. Add a corresponding FCL exclusion rule FCL-E4: *"FCL nodes must not specify the constraint values themselves (→ CL); they may only flag that constraints exist."* This creates a clean handoff between FCL and CL with unambiguous authoring guidance.

---

### M-4 · SUPERSEDE Operation Behavior on DRAFT, DIRTY, and DEPRECATED Nodes is Unspecified

**Location:** §7.1 (SUPERSEDE), §7.2 (footnote on Deprecation Lifecycle).

**The defect:** The SUPERSEDE operation's description addresses the common case (an ACTIVE node being replaced) but leaves the following cases open: Can a DIRTY node be SUPERSEDED directly without first resolving it to ACTIVE or DEPRECATED? Can a DRAFT node be SUPERSEDED (it has never been ACTIVE — what is the semantic meaning of superseding an unvalidated draft)? Can a DEPRECATED node be SUPERSEDED (the footnote says it can, but §7.1 does not formalize this)? Each case produces structurally different outcomes for `parent_id` auto-wiring in children.

**Recommendations:**

1. Add a "Valid Source States" column to the §7.1 operations table for each operation. For SUPERSEDE: *"Valid source states: ACTIVE, DIRTY, DEPRECATED. DRAFT nodes may not be SUPERSEDED; a DRAFT must be explicitly DELETEd. Rationale: SUPERSEDE implies the node reached production, which a DRAFT never did."*
2. Enumerate the pre-conditions for each SUPERSEDE case (DIRTY → SUPERSEDED, DEPRECATED → SUPERSEDED) in the §7.2 notes section, mirroring the detail already given to the DEPRECATED lifecycle description.

---

## 🟢 LOW — Documentation Clarity and Minor Omissions

---

### L-1 · UNBUNDLE Determinism Rule Exemplifies Only G2 Tier Annotations, Not G1

**Location:** §4, UNBUNDLE Determinism Rule note.

**The defect:** The rule references both G1 (XPD + SIL + GPCL) and G2 (FCL + CL) as groups containing optional tiers requiring inline annotation, but its examples — `[FCL]` and `[CL]` — reference only G2 prefixes. A practitioner authoring G1 content in Express Mode receives no guidance on whether to use `[XPD]`, `[SIL]`, `[GPCL]`, or some other prefix convention.

**Recommendations:**

1. Extend the example to include G1: *"e.g., [XPD], [SIL], [GPCL] for G1 content; [FCL], [CL] for G2 content."*
2. Add a normative sub-rule clarifying that when XPD is inactive but G1 content exists, all content is implicitly `[SIL]` or `[GPCL]` — no `[XPD]` annotation should appear, and UNBUNDLE must treat `[XPD]`-annotated content in an XPD-inactive project as a validation error.

---

### L-2 · §6 Physical Constraint Escalation References an "Authoring Authority" Without Defining It or Requiring Escalation to be Documented

**Location:** §6, Physical Constraint Escalation paragraph.

**The defect:** *"...the conflict must be escalated to the authoring authority for resolution."* "Authoring authority" is not defined anywhere in the spec (it does not appear in the Glossary). Additionally, the spec does not state whether the escalation event and its resolution must be recorded in the reconciliation manifest, nor whether the escalation itself temporarily blocks the conflicting nodes from achieving CLEAN status.

**Recommendations:**

1. Add "Authoring Authority" to the Glossary: *"The human or organizational role accountable for resolving conflicts that cannot be resolved by constraint precedence alone (§6). Must be identified per-project before the first VERIFY cycle."*
2. Add a normative rule in §6 (or as a §7 operation note) stating that physical constraint escalations must produce a disposition record in the reconciliation manifest before the affected nodes may transition to ACTIVE, treating unresolved escalations as a DIRTY condition.

---

### L-3 · Overlap Between GPCL-R6 Performance Targets and CL-E3 Cost Model Exclusion is Underspecified

**Location:** GPCL-R6, CL-E3, CL-R7.

**The defect:** GPCL-R6 requires specifying "quantifiable performance targets: latency, throughput, concurrency ceilings." CL-R7 requires specifying "infrastructure ceilings (compute budget, storage cap, bandwidth cap)." CL-E3 prohibits "cost models or TCO calculations" from CL. The boundary between a "bandwidth cap" (CL-R7, allowed) and a "cost model" (CL-E3, prohibited) is not defined — bandwidth caps are often expressed as cost-derived constraints (e.g., "egress ≤ $X/month → ≤ Y TB/month"). Similarly, CL-R7's "compute budget" language is adjacent to TCO. A practitioner cannot determine without additional guidance whether budget-derived infrastructure ceilings belong in CL or are disqualified by CL-E3.

**Recommendations:**

1. Amend CL-E3 with a clarifying sentence: *"CL nodes may express the resulting infrastructure ceiling (e.g., 'maximum 10 TB/month egress') but must not include the financial derivation, vendor pricing tables, or cost optimization logic that produced that ceiling (→ Extensions, e.g., HRE)."*
2. Add a cross-reference note in GPCL-R6 and CL-R7 pointing to each other, making explicit that performance thresholds established in GPCL flow into CL as physical ceiling declarations, and that the financial rationale behind those ceilings is Extension territory only.

---

## Summary Table

| ID | Severity | Section(s) | Issue |
|----|----------|------------|-------|
| C-1 | ⛔ Critical | §1.1 | HIL absorption misstatement in change rationale |
| C-2 | ⛔ Critical | §3.5, §3.4, FCL, SAL-R6 | No-tier-skipping invariant conflicts with FCL→SAL always-edge |
| C-3 | ⛔ Critical | Appendix B | ORL rule count mismatch + TBD in a Finalized document |
| H-1 | 🔴 High | §3.1, §7.1, §7.2 | No formal status state transition model |
| H-2 | 🔴 High | §4, §7.1 | UNBUNDLE "reject" behavior undefined |
| H-3 | 🔴 High | §7.2 | DRAFT node DIRTY propagation unspecified |
| H-4 | 🔴 High | §3.7, §7.1 | CIT-R4 stale inline citations post-DELETE unaddressed |
| M-1 | 🟡 Moderate | §8.1, §8.3, §9 E5/E7 | Inconsistent Extension annotation scope policy (ARE vs. DDE) |
| M-2 | 🟡 Moderate | §10, §8.3 EXT-R2 | Mermaid diagram conflates reads/annotates in extends edges |
| M-3 | 🟡 Moderate | §5 FCL, §5 CL | No FCL rule governs FCL→CL derivation conditions |
| M-4 | 🟡 Moderate | §7.1, §7.2 | SUPERSEDE on DRAFT/DIRTY/DEPRECATED nodes unspecified |
| L-1 | 🟢 Low | §4 | UNBUNDLE examples omit G1 tier annotation guidance |
| L-2 | 🟢 Low | §6 | "Authoring authority" undefined; escalation not manifest-tracked |
| L-3 | 🟢 Low | GPCL-R6, CL-E3, CL-R7 | Ambiguous boundary between performance ceiling and cost model |

---

The three Critical issues (C-1, C-2, C-3) collectively challenge the document's "Finalized" status designation and should be resolved before the specification is used as a binding reference — C-2 in particular has direct implications for any VERIFY engine implementation.
