<!--
  AGENT PARSING HEADER — DO NOT MODIFY
  =====================================
  skill:                DDR-v4-Issues-Tracker
  version:              1.0.0
  target_agent:         Gemini 3.1 Pro
  platform:             Google Antigravity >=1.18
  context_mode:         progressive_disclosure
  schema_version:       IT-1.0
  document_type:        issues_tracker
  subject_system:       DDR System Specification v4.0
  subject_file:         DDR_System_Opus_v4_.md
  last_updated:         2026-02-28
  total_issues:         13
  open_issues:          13
  resolved_issues:      0
  load_trigger:         "DDR issue", "track issue", "DDR problem", "DDR review", "DDR assessment"

  ANTIGRAVITY 1.18 DEPLOYMENT NOTES
  ===================================
  recommended_path:     <workspace-root>/.agents/skills/DDR-Issues-Tracker/SKILL.md
  global_path:          ~/.gemini/antigravity/skills/DDR-Issues-Tracker/SKILL.md
  plan_mode_hint:       Use Antigravity Plan Mode before executing resolution options.
                        Plan Mode maps the full change set (spec sections + YAML fields)
                        before any file is touched. Enables pre-flight impact review.
  context_budget:       Gemini 3.1 Pro supports 1M token context / 64K output tokens.
                        This document uses progressive_disclosure to stay within
                        a single skill load. The ISSUE REGISTRY table is the primary
                        context gate — parse it before loading individual issue blocks.
  artifact_integration: Issue entries are structured for Antigravity Artifact output.
                        Each ISSUE-NNN block can be rendered as a standalone Artifact
                        for Google-Doc-style comment feedback from human reviewers.
  workflow_path:        .agent/workflows/ddr-issue-resolution.md
                        Create a numbered-step Workflow to chain: identify → add entry
                        → update registry → update header metadata.
  gemini_md_hook:       Add to ~/.gemini/GEMINI.md or .antigravity/rules.md:
                        "When working on DDR System issues, load the skill at
                        .agents/skills/DDR-Issues-Tracker/SKILL.md before proceeding."
  deep_think_mode:      Recommended ON for CRITICAL and MAJOR severity issues.
                        Toggle in Antigravity model settings before issuing resolution
                        prompts to force extended chain-of-thought on logic-heavy changes.
-->

# DDR System v4.0 — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the DDR System Specification v4.0. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read only the `<!-- AGENT_CONTEXT -->` blocks within each issue before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              DDR-IT-001
  title:           "DDR System v4.0 — Issues Tracker"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-02-28"
  last_modified:   "2026-02-28"
  author:          "Anthony Formosa"
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT      # Specification makes contradictory claims
    - DESIGN_INADEQUACY     # Feature is absent, underspecified, or insufficient
    - UNNECESSARY_COMPLEXITY # System is more complex than the problem demands
    - AXIOM_VIOLATION       # A rule or behavior contradicts a stated axiom
    - SCHEMA_DEFECT         # Machine-readable schema is incorrect or incomplete
    - MIGRATION_GAP         # Version migration is incomplete or unresolved
    - LIFECYCLE_GAP         # A state, transition, or lifecycle path is undefined
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every new issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

<!-- AGENT_CONTEXT
id:          ISSUE-[NNN]
status:      OPEN | IN_REVIEW | RESOLVED | WONT_FIX | DEFERRED
severity:    CRITICAL | MAJOR | MODERATE | MINOR
type:        [TYPE_VALUE]
tier_refs:   [list of DDR tiers affected, e.g. FCL, CL, SAL]
section_ref: [§ reference in DDR_System_Opus_v4_.md]
rule_refs:   [list of specific rule IDs affected, e.g. CIT-R2, AX-3]
created:     YYYY-MM-DD
updated:     YYYY-MM-DD
resolved:    null | YYYY-MM-DD
-->

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the specific issue. 2–4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the spec, plus the logical chain that makes this a problem.
Use inline code formatting for rule IDs and tier names.]

#### Impact Assessment-[NNN]
[What breaks, is ambiguous, or fails if this issue is not resolved.
State the concrete failure mode.]

#### Resolution-[NNN]: Option A — [Short Label]
[Detailed description of first resolution approach. Include specific rule/section changes
required, draft replacement language where applicable, and any trade-offs.]

#### Resolution-[NNN]: Option B — [Short Label]
[Detailed description of second, distinctly different resolution approach. Must not be
a minor variant of Option A — must represent a meaningfully different design decision.]

#### Notes-[NNN]
[Any cross-references, dependencies on other issues, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID                                                                                            | Severity   | Type                | Status | Tiers Affected | Title                                                               |
| --------------------------------------------------------------------------------------------- | ---------- | ------------------- | ------ | -------------- | ------------------------------------------------------------------- |
| \[ISSUE-001\](#issue-001-derives-absorbs-cites-destroying-audit-trail-precision)              | `CRITICAL` | `LOGICAL_CONFLICT`  | `OPEN` | All            | `derives` absorbs `cites`, destroying audit trail precision         |
| \[ISSUE-002\](#issue-002-fcl-cl-edge-direction-is-semantically-inverted)                      | `CRITICAL` | `LOGICAL_CONFLICT`  | `OPEN` | FCL, CL, SAL   | FCL→CL edge direction is semantically inverted                      |
| \[ISSUE-003\](#issue-003-dag-invariant-text-contradicts-the-merge-node-topology)              | `MAJOR`    | `LOGICAL_CONFLICT`  | `OPEN` | SAL            | DAG invariant text contradicts the merge-node topology              |
| \[ISSUE-004\](#issue-004-ax-3-determinism-is-violated-by-non-automatable-atomic-rules)        | `MAJOR`    | `AXIOM_VIOLATION`   | `OPEN` | All            | AX-3 determinism violated by non-automatable atomic rules           |
| \[ISSUE-005\](#issue-005-gpcl-overloading-creates-an-implicit-fcl-tier-skip)                  | `MAJOR`    | `DESIGN_INADEQUACY` | `OPEN` | GPCL, FCL, SAL | GPCL overloading creates an implicit FCL tier skip                  |
| \[ISSUE-006\](#issue-006-node-status-lifecycle-lacks-a-formal-state-machine)                  | `MAJOR`    | `LIFECYCLE_GAP`     | `OPEN` | All            | Node status lifecycle lacks a formal state machine                  |
| \[ISSUE-007\](#issue-007-supersede-atomicity-and-rollback-are-underspecified)                 | `MAJOR`    | `DESIGN_INADEQUACY` | `OPEN` | All            | SUPERSEDE atomicity and rollback are underspecified                 |
| \[ISSUE-008\](#issue-008-unbundle-rejection-behaviour-is-underspecified)                      | `MODERATE` | `DESIGN_INADEQUACY` | `OPEN` | Express Mode   | UNBUNDLE rejection behaviour is underspecified                      |
| \[ISSUE-009\](#issue-009-are-confidence-score-has-no-normative-rubric)                        | `MODERATE` | `DESIGN_INADEQUACY` | `OPEN` | ARE (E5)       | ARE confidence score has no normative rubric                        |
| \[ISSUE-010\](#issue-010-extension_annotations-namespace-enforcement-is-schema-level-absent)  | `MODERATE` | `SCHEMA_DEFECT`     | `OPEN` | All (schema)   | `extension_annotations` namespace unenforced at schema level        |
| \[ISSUE-011\](#issue-011-orl-r7-migration-is-unresolved-in-a-finalized-specification)         | `MODERATE` | `MIGRATION_GAP`     | `OPEN` | GPCL           | ORL-R7 migration is unresolved in a "Finalized" specification       |
| \[ISSUE-012\](#issue-012-candidate-pool-has-no-pause-state)                                   | `MINOR`    | `LIFECYCLE_GAP`     | `OPEN` | ARE (E5)       | Candidate Pool has no pause state                                   |
| \[ISSUE-013\](#issue-013-dde-upward-fcl-annotation-creates-a-backwards-validation-dependency) | `MINOR`    | `DESIGN_INADEQUACY` | `OPEN` | FCL, DDE (E7)  | DDE upward FCL annotation creates a backwards validation dependency |

---

## ISSUES

---

### ISSUE-001: `derives` Absorbs `cites`, Destroying Audit Trail Precision

<!-- AGENT_CONTEXT
id:          ISSUE-001
status:      OPEN
severity:    CRITICAL
type:        LOGICAL_CONFLICT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.2
rule_refs:   [CIT-R2, AX-3, AX-7]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** All | **Spec Section:** §3.2 Edge Types

#### Problem Statement-001

The v4.0 design decision to merge the `cites` edge type into `derives` collapses two semantically distinct relationships into one undifferentiated type. The stated justification — "a citation for traceability *is* a derivation relationship" — is philosophically imprecise. Content generation from parent content (semantic derivation) and authority grounding without content derivation (traceability citation) are not the same relationship class.

#### Evidence & Justification-001

The spec states: *"`cites` merged into `derives` (a citation for traceability is a derivation relationship)."*

Consider two real DDR relationships:

- `GPCL` derives from `SIL` — the governance constraints are *logically entailed by* the strategic objectives. Content is generated downward. This is genuine derivation.
- A `SAL` node citing an `FCL` node to justify an architectural pattern — the FCL node did not *generate* the SAL content; it merely *authorises* it. This is traceability, not derivation.

When VERIFY traverses the graph, a compliance auditor using only `derives` cannot answer: "Was this component *generated from* that requirement, or merely *traceable to* it?" For regulated domains (ISO 9001, IEC 62443, SOC 2), this distinction is a formal audit requirement. The collapsed vocabulary removes a dimension of information permanently.

#### Impact Assessment-001

- Compliance audits in regulated industries cannot distinguish authorship lineage from traceability citation using the exported DAG alone.
- Graph analytics on the DAG (e.g., cluster analysis of derivation chains vs. authority chains) become impossible.
- VERIFY cannot report whether a downstream node was derived from, or merely grounded in, its parent — both appear identical.

#### Resolution-001: Option A — Reintroduce `cites` as a Distinct Edge Type

Restore `cites` to the 4-type vocabulary, yielding 5 edge types total:
`derives`, `cites`, `constrains`, `implements`, `extends`.

Define `cites` as: *"Establishes a traceability anchor between a child node and a parent node whose content provided authority or justification, without the child's content being semantically derived from the parent's content."*

Update `CIT-R2` to specify which inter-tier transitions are `derives` (vertical content-generation paths: SIL→GPCL, GPCL→FCL, FCL→SAL when CL is inactive) versus `cites` (lateral authority chains: SAL architectural decisions referencing FCL capabilities for justification). This is a breaking schema change requiring a version bump from `4.0` to `5.0` in `ddr_version`. Update `ddr_node_schema.yaml` to add `"cites"` to the `EdgeTypeDefinition` enum and to the `ParentCitation.edge_type` enum.

#### Resolution-001: Option B — Add Derivation Subtype Annotation to `derives`

Retain 4 edge types but add an optional `derivation_mode` property to `ParentCitation`:

```yaml
ParentCitation:
  id: string           # parent node ID
  edge_type: derives | constrains | implements | extends
  derivation_mode:     # Optional; only valid when edge_type = derives
    type: string
    enum: [semantic, traceability]
    description: >
      semantic    — child content was generated from or entailed by parent content.
      traceability — child cites parent for authority grounding only; no content derivation.
```

This is a non-breaking addition (field is optional; default is `semantic` for backwards compatibility). Existing YAML files remain valid. `VERIFY` gains the ability to distinguish derivation modes. Compliance reports can filter by `derivation_mode: traceability` to produce audit trails. No version bump required — schema minor version increment suffices.

#### Notes-001

Option A is semantically cleaner but introduces a breaking change requiring migration tooling. Option B is immediately deployable without breaking existing project files. The two options represent a fundamental design philosophy choice: vocabulary minimalism (Option B) versus semantic precision (Option A). Recommend board decision before proceeding to implementation of either path.

---

### ISSUE-002: FCL→CL Edge Direction Is Semantically Inverted

<!-- AGENT_CONTEXT
id:          ISSUE-002
status:      OPEN
severity:    CRITICAL
type:        LOGICAL_CONFLICT
tier_refs:   [FCL, CL, SAL]
section_ref: §3.4, §5 (Tier 4 CL)
rule_refs:   [CL-R9, AX-2, CIT-R2]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `FCL`, `CL`, `SAL` | **Spec Section:** §3.4, §5 Tier 4

#### Problem Statement-002

The spec defines `CL` as deriving from `FCL`. However, the `CL` tier is defined as containing *externally imposed*, non-negotiable technology and hardware constraints — constraints that exist prior to and independent of any functional capability authoring. Modelling these constraints as *children* of functional capabilities inverts the causal direction for the majority of real-world projects.

#### Evidence & Justification-002

The spec's `CL` activation condition: *"Activate when specific technology, hardware, or infrastructure constraints are non-negotiable."* The word *non-negotiable* implies pre-existing facts — an inherited hardware budget, a mandated OS, a contractual framework obligation. These do not *derive from* a user workflow specification. They *precede and constrain* it.

`CL-R9` compounds the problem by requiring: *"Must cite FCL IDs for each constraint."* This forces authors to construct post-hoc functional justifications for hardware and technology mandates that were imposed by external authority (procurement, legal, legacy infrastructure) before a single FCL node was authored.

Concrete example: An organization mandates Python 3.11+ due to a corporate security policy. Under the current model, the author must identify an `FCL` node that this constraint "derives from" — which is fabricated, because the constraint precedes and is independent of any functional capability.

#### Impact Assessment-002

- Authors are systematically required to invent false derivation chains for externally-imposed `CL` constraints, directly violating `AX-1` (complete audit trails must not be manufactured).
- Any project where hardware/technology selections are dictated by procurement, legacy infrastructure, or security policy — which is the majority of enterprise projects — will have structurally dishonest `CL→FCL` citations.
- The `AX-2` abstraction ordering principle (technology specificity deferred until logically necessary) is violated because `CL` must logically precede `FCL` authoring in projects where constraints are given, not chosen.

#### Resolution-002: Option A — Elevate CL to Derive from GPCL or SIL

Reposition `CL` as a peer of `FCL` rather than its child. Both `FCL` and `CL` derive from `GPCL` (or optionally `SIL` when the constraint is purely strategic, such as a vendor commitment). Both then feed `SAL` as a merge node:

```markdown
GPCL → FCL → SAL
GPCL → CL  ╌constrains╌▶ SAL
```

Update `CL-R9` to: *"Must cite the GPCL or SIL ID that establishes the organizational or governance context for each constraint."* This accurately models the authorship reality: governance mandates drive both what the system must do (FCL) and what it must be built with (CL). SAL's merge-node role is unchanged; it still absorbs both. This is a breaking topological change requiring a version bump.

#### Resolution-002: Option B — Make CL Direction Context-Dependent via an `origin` Tag

Retain the FCL→CL edge but add an `origin` field to `CL` nodes that explicitly records whether the constraint was internally derived or externally imposed:

```yaml
CL Node properties (addition):
  constraint_origin:
    type: string
    enum: [derived, imposed]
    description: >
      derived  — constraint selected by the design team based on FCL requirements.
      imposed  — constraint pre-exists and is externally mandated (legal, procurement, legacy).
```

When `constraint_origin: imposed`, `CL-R9` is replaced by `CL-R9-imposed`: *"Must cite the external authority source (regulatory framework, contract reference, or procurement policy) that mandates the constraint. FCL citation is not required."*

This is a non-breaking addition. Existing files work unchanged. The `imposed` path creates an honest audit trail without requiring fabricated FCL citations. VERIFY checks that `derived` nodes have FCL citations and `imposed` nodes have authority references.

#### Notes-002

Option A is the structurally correct solution but requires topology changes. Option B is immediately implementable and accurately reflects the dual nature of technology constraints (sometimes chosen, sometimes given) without breaking the existing DAG model. This issue is co-dependent with `ISSUE-001` — any topology changes in this issue must be reflected in edge type vocabulary updates.

---

### ISSUE-003: DAG Invariant Text Contradicts the Merge-Node Topology

<!-- AGENT_CONTEXT
id:          ISSUE-003
status:      OPEN
severity:    MAJOR
type:        LOGICAL_CONFLICT
tier_refs:   [SAL]
section_ref: §3.5
rule_refs:   [INV-2, SAL-R6, CIT-R2]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `SAL` | **Spec Section:** §3.5 DAG Invariants

#### Problem Statement-003

The normative text in §3.5 bullet 2 states: *"No tier-skipping: each citation references exactly one active tier above in the derivation path."* This is directly contradicted by the SAL merge-node design, where SAL is explicitly required to cite *both* FCL and CL (when active) — two parent tiers simultaneously. The YAML corrects this with an `INV-2` annotation, but the Markdown specification, which is the human-readable normative document, contains no such exception.

#### Evidence & Justification-003

- §3.5 Invariant bullet 2 (Markdown): *"No tier-skipping: each citation references exactly one active tier above in the derivation path."*
- §3.4 Topology diagram (Markdown): SAL is labelled "Constraint merge point" and explicitly shows two incoming edges: FCL (derives) and CL (constrains).
- `SAL-R6` (Markdown): *"Must cite all active parent IDs (FCL + CL if active) for each major architectural decision."*
- `ddr_system_v4_0.yaml`, `INV-2`: *"Exception: FCL→SAL derives edge is always valid regardless of CL activation state (SAL merge-node design; see §3.4, Audit C-2)."*

The YAML is internally consistent; the Markdown is not. In a system declared as "Single Source of Truth," having the two canonical formats produce contradictory normative rules on a structural invariant is a specification integrity failure by the system's own standards.

#### Impact Assessment-003

- Any validator implementing the Markdown-stated invariant verbatim will reject valid SAL nodes that correctly cite both FCL and CL parents, producing false VERIFY failures.
- A practitioner reading only the Markdown spec (the primary human-readable format) will incorrectly model SAL as having a single parent, authoring non-compliant nodes.
- The inconsistency undermines the Single Source of Truth claim in the document header.

#### Resolution-003: Option A — Correct §3.5 Invariant Language with Explicit Exception

Replace the §3.5 bullet 2 text with:

> *"No tier-skipping: each citation references the immediately preceding active tier(s) in the derivation path. Exception: `SAL` is a merge node (§3.4) that simultaneously derives from `FCL` and is constrained by `CL` when active. `SAL` is therefore the only node that validly carries parent citations from two distinct tiers. This exception is exhaustive; no other tier may carry citations from more than one immediately preceding tier."*

Remove the exception note from `INV-2` in the YAML (it becomes redundant once the Markdown is authoritative). Designate Markdown as the normative source; YAML as the machine-parseable encoding.

#### Resolution-003: Option B — Establish a Single Authoritative Source Policy

Define a formal `§0 Document Authority Policy` section that specifies: *"In the event of any conflict between the Markdown specification and the YAML encoding, the YAML encoding is authoritative. The Markdown is a human-readable rendering."* Then update `INV-2` in the YAML with the complete exception text (currently only a note), making the YAML the canonical source for all invariant definitions.

Under Option B, the Markdown §3.5 bullet is updated to a simplified cross-reference: *"See `dag_invariants.INV-2` in `ddr_system_v4_0.yaml` for the complete invariant definition including the SAL merge-node exception."* This eliminates the risk of future divergence by making YAML the single truth for machine-verifiable rules.

#### Notes-003

Option B is the stronger long-term choice for an agentic workflow where the YAML is parsed by tools and the Markdown is read by humans. However, it requires a cultural shift from human-readable Markdown as the "real" spec. Both options require a minor version bump (`4.0` → `4.1`).

---

### ISSUE-004: AX-3 Determinism Is Violated by Non-Automatable Atomic Rules

<!-- AGENT_CONTEXT
id:          ISSUE-004
status:      OPEN
severity:    MAJOR
type:        AXIOM_VIOLATION
tier_refs:   [XPD, SIL, GPCL, FCL, SAL]
section_ref: §2 (AX-3, AX-6), §5, §7.1
rule_refs:   [AX-3, AX-6, FCL-R1, FCL-R2, XPD-R3, SAL-R1, GPCL-R2]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `AXIOM_VIOLATION`
**Tiers Affected:** `XPD`, `SIL`, `GPCL`, `FCL`, `SAL` | **Spec Section:** §2, §5, §7.1

#### Problem Statement-004

`AX-3` (Determinism) states: *"Identical inputs produce unambiguous, mechanically verifiable outputs. Implication: Automated validation and compliance checking are possible."* The `VALIDATE` operation promises *"pass/fail with specific violated rule IDs"* against the full atomic ruleset. However, a significant subset of atomic inclusion rules require semantic judgment that cannot be mechanically evaluated — violating `AX-3`. Evaluating those rules via LLM inference would violate `AX-6` (Core is strictly declarative; inference is Extension-only).

#### Evidence & Justification-004

Rules that cannot be mechanically verified include:

| Rule      | Non-Automatable Requirement                                                                      |
| --------- | ------------------------------------------------------------------------------------------------ |
| `FCL-R1`  | *"from the perspective of a user or external system"* — requires audience modeling               |
| `FCL-R2`  | *"without naming components, classes, or modules"* — requires semantic intent parsing            |
| `XPD-R3`  | *"comprehensible to non-technical stakeholders without a glossary"* — requires audience modeling |
| `SAL-R1`  | *"with rationale"* — requires adequacy judgment                                                  |
| `GPCL-R2` | *"enforceable, testable constraints — not aspirational targets"* — requires semantic distinction |

`VALIDATE` cannot evaluate these rules without LLM inference, which is explicitly prohibited in Core by `AX-6`. The system therefore either: (a) silently skips unevaluable rules — meaning `VALIDATE` is incomplete without stating so, or (b) invokes inference inside Core — which violates `AX-6`.

#### Impact Assessment-004

- The `VALIDATE` operation's `pass` result is not trustworthy: it may indicate "passed all automatable rules" rather than "passed all rules," without distinguishing the two cases.
- The CLEAN state declaration in §11 may be false: a project can reach `CLEAN` while containing nodes that violate semantic rules that VALIDATE never evaluated.
- `AX-3` and `AX-6` are mutually contradictory as currently stated — they cannot both be satisfied by a Core VALIDATE that evaluates the full ruleset.

#### Resolution-004: Option A — Formally Classify Rules as Structural vs. Semantic

Add a `verification_mode` property to every atomic rule:

```yaml
AtomicInclusionRule:
  rule_id: string
  statement: string
  violation_consequence: string
  verification_mode:   # NEW REQUIRED FIELD
    type: string
    enum: [structural, semantic]
    description: >
      structural — evaluable by pattern matching, schema validation, keyword detection,
                   or citation graph traversal. Core VALIDATE handles this automatically.
      semantic   — requires human judgment or LLM inference. Core VALIDATE flags these
                   as REVIEW_REQUIRED; human sign-off required before DRAFT→ACTIVE transition.
```

Update `VALIDATE` to: *"Evaluates all `structural` rules automatically. For each `semantic` rule, emits a `REVIEW_REQUIRED` item in the reconciliation manifest pending_items. A node may not transition from `DRAFT` to `ACTIVE` while any `REVIEW_REQUIRED` items remain unresolved."* This preserves `AX-3` for the automatable subset and `AX-6` throughout.

#### Resolution-004: Option B — Create a Semantic Validation Extension (SVE)

Extract all semantic rule evaluation into a new optional Extension `E10 — Semantic Validation Engine (SVE)`. Core `VALIDATE` evaluates only structural rules and emits a `validation_mode: structural_only` flag in its output. `SVE` reads Core node content and evaluates semantic rules via LLM inference, producing `SVE::semantic_compliance` annotations in `extension_annotations`. The CLEAN checklist gains an entry: *"If SVE is active, all `SVE::semantic_compliance` annotations must be `PASS` or carry a human-disposition note."*

This cleanly separates structural (Core) from semantic (Extension) validation, satisfying both `AX-3` and `AX-6` without modifying Core atomic rule definitions. The trade-off: semantic compliance is optional by default and requires SVE activation.

#### Notes

Option A (classification at rule definition level) is more transparent and guarantees semantic rules are always flagged even without an Extension active. Option B separates concerns more cleanly but makes semantic validation opt-in. Both options should be combined in an ideal implementation: classify rules (Option A) AND create SVE (Option B) to handle evaluation of `semantic` rules when LLM capability is desired.

---

### ISSUE-005: GPCL Overloading Creates an Implicit FCL Tier Skip

<!-- AGENT_CONTEXT
id:          ISSUE-005
status:      OPEN
severity:    MAJOR
type:        DESIGN_INADEQUACY
tier_refs:   [GPCL, FCL, SAL]
section_ref: §5 (Tier 2 GPCL, Tier 3 FCL)
rule_refs:   [GPCL-R6, GPCL-E2, FCL-R6, SAL-R6]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `GPCL`, `FCL`, `SAL` | **Spec Section:** §5 Tiers 2–3, §3.5 INV-2

#### Problem Statement-005

By absorbing `ORL` (operational requirements), `GPCL` now specifies quantifiable performance targets — latency, throughput, availability — that directly drive architectural decisions at `SAL`. This creates an implicit authority path from `GPCL` → `SAL` that bypasses `FCL`, the tier whose role is to mediate between governance constraints and architecture decisions. Simultaneously, the `GPCL`/`FCL` tier boundary is undefined for requirements (like throughput under load) that are simultaneously a governance threshold and a functional capability.

#### Evidence & Justification-005

- `GPCL-R6`: *"Must specify quantifiable performance targets: latency, throughput, concurrency ceilings."*
- `GPCL-E2`: *"Must not describe functional system behaviors (→ FCL)."*
- `SAL-R6`: *"Must cite all active parent IDs (FCL + CL if active) for each major architectural decision."*

A `GPCL` node stating *"p99 API response < 50ms"* directly determines SAL decomposition choices (caching layer, async patterns, edge deployment). By `SAL-R6`, the SAL node must cite its FCL parent — but if the architectural driver is the GPCL threshold, the FCL node becomes a structural formality with no independent semantic content. `GPCL-E2` prevents GPCL from describing the capability, but a requirement like *"the system must handle 10,000 concurrent authentication requests"* describes observable system behaviour (capability) and a governance threshold simultaneously — the tier assignment is ambiguous by definition.

#### Impact Assessment-005

- Authors will routinely face tier-assignment ambiguity between GPCL and FCL for performance-sensitive requirements, generating inconsistent documentation across projects.
- VERIFY will detect tier contamination violations (`GPCL-E2` breaches) for requirements that cannot be cleanly assigned to either tier.
- The FCL tier becomes a structural pass-through for performance-driven projects, undermining the tier's semantic value as a mediating layer.

#### Resolution-005: Option A — Add a GPCL/FCL Disambiguation Rule

Add a normative rule `GPCL-FCL-BR1` (boundary rule) to §5:

> *"GPCL specifies the threshold (the measurable target). FCL specifies the capability (the user-observable behaviour) that must satisfy that threshold. These are complementary, not competing, assignments. For any quantitative GPCL target, there must exist a corresponding FCL node describing the observable interaction whose performance is being governed. SAL citations for performance-driven architectural decisions must cite the FCL capability node, not the GPCL threshold node directly, unless no corresponding FCL interaction can be identified — in which case, a MISSING_PARENT item must be logged to the reconciliation manifest."*

This forces FCL to remain a genuine mediating layer and gives VERIFY a deterministic rule to enforce.

#### Resolution-005: Option B — Split GPCL into Regulatory-GPCL and Quality-ORL as Distinct Sections with Cross-Tier Citation Rules

Retain GPCL as a single tier but formally define two mandatory content sections within every GPCL node: `regulatory` (external mandates, compliance frameworks, data residency) and `quality` (performance, availability, scalability targets). Define that `regulatory` content has authority over SAL directly, while `quality` content authority must route through FCL:

```markdown
## GPCL Node Content Structure

### [regulatory]
<!-- Directly citable by SAL nodes (external mandates are architecture-constraining) -->
- ...

### [quality]
<!-- Must be mediated by a corresponding FCL node before SAL citation -->
- ...
```

Update `SAL-R6` to distinguish: *"For each major architectural decision driven by regulatory GPCL content, cite the GPCL node directly. For each decision driven by quality GPCL content, cite the mediating FCL node."* This eliminates FCL bypass for regulatory mandates (which legitimately constrain architecture directly) while preserving FCL as a mandatory mediator for quality targets.

#### Notes-005

Option B is more architecturally precise but requires authors to understand the `regulatory`/`quality` distinction within GPCL — adding cognitive overhead. Option A is simpler to apply and enforce. Both options reduce but do not eliminate the tier boundary ambiguity for requirements that are genuinely dual-nature.

---

### ISSUE-006: Node Status Lifecycle Lacks a Formal State Machine

<!-- AGENT_CONTEXT
id:          ISSUE-006
status:      OPEN
severity:    MAJOR
type:        LIFECYCLE_GAP
tier_refs:   [ALL]
section_ref: §3.1, §7.1, §7.2
rule_refs:   [AX-3]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** All | **Spec Section:** §3.1, §7.1

#### Problem Statement-006

The `status` enum defines five values (`DRAFT`, `ACTIVE`, `DIRTY`, `DEPRECATED`, `SUPERSEDED`) but the specification contains no formal state transition table. Valid transitions, guard conditions, and prohibited transitions are scattered across narrative text in §7.1 and §7.2. The schema comment references "Audit H-1" which does not exist in the specification. At least one transition (`DEPRECATED→ACTIVE`) is entirely absent.

#### Evidence & Justification-006

- The `ddr_node_schema.yaml` `status` field description references: *"Valid transitions (§7.1, Audit H-1)"* — but §7.1 contains no "Audit H-1" section and no complete transition table.
- `DIRTY→ACTIVE` transition: requires `VERIFY+VALIDATE` per schema, but no guard conditions are specified (does full-graph VERIFY suffice, or per-node VALIDATE? what if some descendants are still DRAFT?).
- `DEPRECATED→ACTIVE`: the reversal of a deprecation decision is entirely undefined. No transition path, no operation, no guard condition.
- `SUPERSEDED→ACTIVE`: the schema comment lists this path implicitly absent, but never formally prohibits it.

#### Impact Assessment-006

- Any implementation of the status lifecycle will be based on inference from narrative text rather than a formal machine, producing divergent implementations.
- The undefined `DIRTY→ACTIVE` guard conditions mean that implementations will disagree on when a DIRTY node is clean enough to become ACTIVE.
- The missing `DEPRECATED→ACTIVE` path means reversed deprecation decisions have no spec-compliant resolution path, forcing authors to use SUPERSEDE (which is semantically incorrect — SUPERSEDE implies replacement exists).

#### Resolution-006: Option A — Add §3.8 "Node Status Lifecycle" with a Formal Transition Table

Insert a new section §3.8 before the citation rules, containing:

| From         | To           | Triggering Operation        | Guard Conditions                                                     | Notes                      |
| ------------ | ------------ | --------------------------- | -------------------------------------------------------------------- | -------------------------- |
| `DRAFT`      | `ACTIVE`     | `VALIDATE`                  | All tier rules pass (structural + semantic REVIEW_REQUIRED resolved) | —                          |
| `DRAFT`      | `DELETED`    | `DELETE`                    | No children; or cascade confirmed                                    | —                          |
| `ACTIVE`     | `DIRTY`      | `MODIFY` / propagation      | Always (no guard; automatic)                                         | —                          |
| `ACTIVE`     | `DEPRECATED` | `MODIFY` (set status field) | `LVE-R3`: sunset date + migration path required                      | —                          |
| `ACTIVE`     | `SUPERSEDED` | `SUPERSEDE`                 | Replacement spec validates; atomically                               | —                          |
| `DIRTY`      | `ACTIVE`     | `VALIDATE` (re-validation)  | Node's own tier rules pass; all REVIEW_REQUIRED resolved             | Grandchildren not affected |
| `DIRTY`      | `DEPRECATED` | `MODIFY`                    | Same as `ACTIVE→DEPRECATED`                                          | —                          |
| `DIRTY`      | `SUPERSEDED` | `SUPERSEDE`                 | Same as `ACTIVE→SUPERSEDED`                                          | —                          |
| `DEPRECATED` | `SUPERSEDED` | `SUPERSEDE`                 | Replacement validates                                                | —                          |
| `DEPRECATED` | `DELETED`    | `DELETE`                    | No active children dependent                                         | —                          |
| `DEPRECATED` | `ACTIVE`     | `MODIFY` (revert)           | Deprecation rationale documented; sunset date cleared                | Reversal must be logged    |
| `SUPERSEDED` | *(none)*     | *(terminal)*                | Node ID is immutable; no further transitions permitted               | ID retained permanently    |

Also explicitly state: *"SUPERSEDED is a terminal status. No operation may transition a node out of SUPERSEDED status. New content requires INSERT of a new node."*

#### Resolution-006: Option B — Express the State Machine in the YAML Schema as a Machine-Verifiable Contract

Add a `status_transitions` block to `ddr_system_v4_0.yaml` under a new `lifecycle` key:

```yaml
lifecycle:
  status_transitions:
    - from: DRAFT
      to: ACTIVE
      operation: VALIDATE
      guards: ["all_structural_rules_pass", "all_semantic_review_required_resolved"]
    - from: ACTIVE
      to: DIRTY
      operation: MODIFY
      guards: []  # automatic; no guard
    # ... etc.
  prohibited_transitions:
    - from: SUPERSEDED
      to: [DRAFT, ACTIVE, DIRTY, DEPRECATED]
      reason: "SUPERSEDED is terminal. INSERT a new node."
```

This makes the state machine machine-parseable and directly validatable by VERIFY, rather than requiring a reader to infer rules from narrative text. The human-readable §3.8 in Markdown becomes a rendered view of this YAML definition.

#### Notes-006

Option B is superior for agentic validation workflows because the state machine is directly consumable by Antigravity agents without natural language parsing. Both options should be implemented together: YAML as source of truth (Option B), Markdown table as human-readable rendering (Option A). Resolve "Audit H-1" reference in `ddr_node_schema.yaml` simultaneously.

---

### ISSUE-007: SUPERSEDE Atomicity and Rollback Are Underspecified

<!-- AGENT_CONTEXT
id:          ISSUE-007
status:      OPEN
severity:    MAJOR
type:        DESIGN_INADEQUACY
tier_refs:   [ALL]
section_ref: §7.1
rule_refs:   [AX-3, INV-6]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** All | **Spec Section:** §7.1 (SUPERSEDE operation)

#### Problem Statement-007

The `SUPERSEDE` operation is described as a three-step sequence: (1) mark old node `SUPERSEDED`, (2) validate and create replacement node, (3) auto-update children's `parent_ids`. The spec states that INSERT *"fails atomically"* if the replacement spec is invalid. However, it does not define whether step 1 (marking old node SUPERSEDED) is committed before or after step 2's success is confirmed. If step 1 is committed and step 2 fails, the original node is `SUPERSEDED` with no valid replacement — a structural corruption state.

#### Evidence & Justification-007

Spec text: *"Mark node SUPERSEDED; create replacement with new ID... Old node retains ID; new node validated; children's parent_ids auto-updated..."*

The sequence *"Mark... create... auto-update"* implies serial execution. If the replacement INSERT fails validation after step 1 has been applied, children now point to a `SUPERSEDED` parent with no successor. This is an orphan-creation scenario that no existing operation resolves (INSERT of the replacement would be a new, separate action — not a rollback). `INV-6` requires atomic XPD SUPERSEDE, but no equivalent atomicity guarantee exists for non-XPD nodes.

#### Impact Assessment-007

A failed SUPERSEDE mid-operation could leave the DAG in a structurally corrupt state: original node in `SUPERSEDED` status, no replacement node, children with a parent pointing to a `SUPERSEDED` node — triggering orphan detection on the next VERIFY run. This is unrecoverable without a manual repair operation not defined in the spec.

#### Resolution-007: Option A — Define SUPERSEDE as a Single Atomic Transaction with Guaranteed Rollback

Add to the SUPERSEDE operation definition:

> *"SUPERSEDE is a single atomic transaction. All three steps — (1) transition source node to `SUPERSEDED`, (2) INSERT and validate replacement node, (3) re-wire child `parent_ids` — must succeed or the entire operation rolls back atomically. Rollback returns the source node to its pre-SUPERSEDE status (`ACTIVE` or `DEPRECATED`) and leaves no replacement node or re-wired parent_ids in the DAG. A SUPERSEDE operation that fails validation leaves the DAG in an unchanged state. The reconciliation manifest must record failed SUPERSEDE attempts with the validation error that triggered rollback."*

Extend `INV-6` to apply to all tiers: *"SUPERSEDE of any node must be atomic; partial application constitutes a structural violation detectable by VERIFY."*

#### Resolution-007: Option B — Introduce a SUPERSEDE_PENDING Intermediate Status

Add `SUPERSEDE_PENDING` as a sixth status value representing the in-progress state of a SUPERSEDE operation:

```yaml
status: DRAFT | ACTIVE | DIRTY | DEPRECATED | SUPERSEDED | SUPERSEDE_PENDING
```

The operation proceeds: (1) source node → `SUPERSEDE_PENDING`; (2) attempt INSERT of replacement; (3a) on success: source → `SUPERSEDED`, children re-wired; (3b) on failure: source → reverted to prior status, no children modified. VERIFY detects any node stuck in `SUPERSEDE_PENDING` and treats it as a structural violation requiring manual resolution. This makes the intermediate state visible and recoverable without requiring true transactional rollback semantics from the implementation.

#### Notes-007

Option A requires transactional semantics from the storage layer (e.g., copy-on-write or journal). Option B is implementable without transactional infrastructure by making the intermediate state explicit. Option B's `SUPERSEDE_PENDING` status also provides operational visibility into long-running replacements — useful in agentic workflows where SUPERSEDE may be triggered asynchronously across a large DAG.

---

### ISSUE-008: UNBUNDLE Rejection Behaviour Is Underspecified

<!-- AGENT_CONTEXT
id:          ISSUE-008
status:      OPEN
severity:    MODERATE
type:        DESIGN_INADEQUACY
tier_refs:   [FCL, CL, XPD, SIL, GPCL]
section_ref: §4, §7.1
rule_refs:   [AX-3]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** Express Mode Groups | **Spec Section:** §4, §7.1

#### Problem Statement-008

The UNBUNDLE Determinism Rule states that UNBUNDLE *"must reject content that cannot be unambiguously assigned to a constituent tier."* The specification does not define: (a) the rejection payload format, (b) whether partial UNBUNDLE is permitted, (c) the status of a rejected Express Mode node after a failed UNBUNDLE attempt, or (d) what constitutes sufficient tier annotation coverage to permit UNBUNDLE to proceed.

#### Evidence & Justification-008

The only disambiguation mechanism is *"explicit tier annotations (e.g., `[FCL]` or `[CL]` inline prefixes)."* However, no minimum annotation coverage threshold is specified. An LLM authoring in Express Mode will frequently omit tier prefixes for content it considers contextually obvious. The rejection error message format is undefined — an agent receiving a rejection has no structured payload to parse and retry.

#### Impact Assessment-008

- Workflow-blocking failure mode with no recovery path specified.
- Agents cannot programmatically identify which content fragment caused rejection, preventing autonomous retry.
- The status of a rejected Express Mode node is undefined — it could remain in DRAFT, revert to unannotated, or enter an unspecified error state.

#### Resolution-008: Option A — Define UNBUNDLE as a Two-Phase Operation with Pre-Flight Scan

Split UNBUNDLE into two invokable phases:

**Phase 1 (UNBUNDLE_SCAN):** Traverses the Express Mode group content, identifies all content fragments, and emits a structured `scan_result` for each:

```json
{
  "fragment_id": "G2-3",
  "content_preview": "Mandatory framework: Django 4.2+",
  "detected_annotation": "[CL]",
  "allocation_confidence": "high | ambiguous | none",
  "ambiguity_reason": "null | 'No [TIER] annotation found; could be FCL or CL'"
}
```

**Phase 2 (UNBUNDLE_EXECUTE):** Only proceeds if zero `ambiguous` or `none` fragments remain. Rejects otherwise, returning the Phase 1 scan result as the error payload.

Phase 1 is independently invokable as a pre-flight check. This gives agents structured error payloads to process and retry. Specify: partial UNBUNDLE is prohibited — it is all-or-nothing per group.

#### Resolution-008: Option B — Require Structured Front Matter in Express Mode Nodes

Mandate that Express Mode group nodes contain a structured preamble listing their constituent tier allocations before content:

```markdown
<!-- EXPRESS_MODE_ALLOCATIONS
G2-FCL: [line numbers or content IDs allocated to FCL]
G2-CL:  [line numbers or content IDs allocated to CL]
-->
[Content with optional inline [TIER] annotations]
```

UNBUNDLE uses the structured `EXPRESS_MODE_ALLOCATIONS` front matter as the authoritative allocation map, requiring no per-line annotation parsing. If the front matter is absent or incomplete, UNBUNDLE rejects with a structured error: `MISSING_EXPRESS_ALLOCATION_HEADER`. This makes UNBUNDLE deterministic (it reads a map, not heuristically scans annotations) and eliminates ambiguity in tier assignment.

#### Notes-008

Option B is more robust and deterministic but adds authoring overhead. Option A preserves the current inline annotation convention while adding operational clarity. Recommend combining both: Option B for precise allocation when desired, Option A scan as fallback for content authored without structured front matter.

---

### ISSUE-009: ARE Confidence Score Has No Normative Rubric

<!-- AGENT_CONTEXT
id:          ISSUE-009
status:      OPEN
severity:    MODERATE
type:        DESIGN_INADEQUACY
tier_refs:   [ARE_E5]
section_ref: §9 (E5 ARE)
rule_refs:   [AX-3, ARE-R2]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** ARE (E5) | **Spec Section:** §9 Extension E5

#### Problem Statement-009

`ARE-R2` requires every Candidate Pool node to carry `ARE::confidence_score (0.0–1.0)` derived from "source evidence quality." Neither the input signals for score derivation, nor band definitions, nor a minimum promotion threshold are specified. The score is therefore non-deterministic across ARE implementations, violating `AX-3`.

#### Evidence & Justification-009

- `ARE-R2`: *"Each candidate carries `ARE::confidence_score (0.0–1.0)` derived from source evidence quality."*
- "Source evidence quality" is undefined: no rubric, no list of signals, no band definitions.
- Two ARE implementations can produce scores of 0.9 and 0.2 for identical input DAGs with no mechanism to adjudicate which is correct.
- Practitioners reviewing Candidate Pool nodes have no framework to interpret a score of 0.67 — is this high confidence? Should it be promoted or discarded?

#### Impact Assessment-009

- ARE is specified as an optional Extension but is the highest-value capability for maintenance workflows. An opaque confidence score reduces its practical utility for promotion decisions.
- Non-determinism directly violates `AX-3`, the system's foundational determinism axiom.
- Without a minimum promotion threshold, the CLEAN checklist entry for ARE (*"candidates reviewed and either promoted or discarded"*) provides no quality gate — a low-confidence candidate can be promoted via INSERT without any systemic check.

#### Resolution-009: Option A — Define a Normative ARE Confidence Scoring Schema in §9

Extend `ARE-R2` with a normative scoring appendix:

```yaml
ARE_confidence_score:
  range: [0.0, 1.0]
  input_signals:
    - signal: direct_source_node_count
      description: "Number of ISL/CDL nodes whose content directly implies the inferred content."
      weight: high
    - signal: icl_contract_corroboration
      description: "Whether an ICL contract schema corroborates the inferred interface."
      weight: medium
    - signal: sal_pattern_alignment
      description: "Whether the inferred node aligns with an existing SAL architectural pattern."
      weight: medium
    - signal: cross_tier_consistency
      description: "Whether inferences from ≥3 tiers independently converge on the same content."
      weight: high
  score_bands:
    - range: [0.0, 0.4]
      label: speculative
      recommendation: "Surface only if ARE::low_confidence_override flag is set. Require human rationale on promotion."
    - range: [0.4, 0.7]
      label: probable
      recommendation: "Surface. Require peer review before promotion via INSERT."
    - range: [0.7, 1.0]
      label: high_confidence
      recommendation: "Surface. Single human review sufficient for promotion."
  minimum_surfacing_threshold: 0.35
  low_confidence_override_flag: "ARE::low_confidence_override: true"
```

#### Resolution-009: Option B — Delegate Confidence Scoring to a Configurable Scoring Profile

Define `ARE-R2` as requiring a declared `scoring_profile` in the ARE Extension contract rather than a fixed rubric. Standard profiles are defined in an appendix; custom profiles must declare their signals and bands:

```yaml
ARE_contract:
  scoring_profile: standard_v1 | conservative_v1 | custom
  custom_scoring_profile:  # required when scoring_profile = custom
    signals: [...]
    bands: [...]
    minimum_surfacing_threshold: float
```

The standard `standard_v1` profile contains the rubric from Option A. `conservative_v1` uses a higher minimum threshold (0.55) for regulated environments. `custom` requires explicit declaration. This allows ARE implementations to adapt to domain-specific evidence quality norms while maintaining determinism within any given profile.

#### Notes-009

Option B provides flexibility for enterprise customization. Option A provides a universal baseline. Recommend implementing Option A as the `standard_v1` profile within Option B's framework — combining both into one spec-compatible solution.

---

### ISSUE-010: `extension_annotations` Namespace Enforcement Is Absent at Schema Level

<!-- AGENT_CONTEXT
id:          ISSUE-010
status:      OPEN
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   [ALL]
section_ref: §8, §8.3
rule_refs:   [EXT-R3, AX-6]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All (schema-level) | **Spec Section:** §8, §8.3

#### Problem Statement-010

`EXT-R3` mandates that Extension annotations be namespaced by Extension ID (`HRE::min_hardware_profile`). However, `ddr_node_schema.yaml` defines `extension_annotations` as `type: object; additionalProperties: true` — accepting any key-value structure without namespace pattern enforcement. Schema validation passes for non-compliant or adversarial annotation keys.

#### Evidence & Justification-010

Current schema definition:

```yaml
extension_annotations:
  type: object
  additionalProperties: true  # ANY key accepted — no pattern enforcement
```

A non-conforming Extension writing `content: "overwrite"` or `parent_ids: []` as annotation keys would pass JSON Schema 2020-12 validation despite being explicitly prohibited by `AX-6` (Extensions must not modify Core content). While runtime checks could prevent this, relying solely on runtime enforcement leaves the schema contract incomplete.

#### Impact Assessment-010

- A buggy or adversarial Extension can write namespace-less keys that shadow or conflict with Core node fields without triggering schema validation errors.
- The JSON Schema contract advertised in `ICL-6.1` as *"machine-parseable"* is not complete: it validates structure but not namespace compliance.
- `EXT-R3` becomes a runtime-only convention rather than a contract-level guarantee.

#### Resolution-010: Option A — Add JSON Schema 2020-12 Pattern Properties Constraint

Replace the `extension_annotations` schema with:

```yaml
extension_annotations:
  type: object
  description: >
    Namespaced Extension metadata. Keys MUST follow format: EXTENSION_ID::annotation_key
    (EXT-R3). EXTENSION_ID must be uppercase alphanumeric. annotation_key must be
    lowercase snake_case.
  patternProperties:
    "^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$":
      description: "Valid namespaced annotation. Format: EXTENSION_ID::annotation_key"
  additionalProperties: false
  default: {}
```

This enforces `EXT-R3` at schema validation time via JSON Schema 2020-12's `patternProperties` + `additionalProperties: false` combination. Any key not matching `^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$` fails validation. Non-breaking for compliant Extensions; immediately catches non-compliant ones.

#### Resolution-010: Option B — Introduce a Dedicated ExtensionAnnotation Schema Type

Instead of pattern validation on keys, define a structured `ExtensionAnnotation` object type:

```yaml
ExtensionAnnotation:
  type: object
  required: [extension_id, annotation_key, value]
  additionalProperties: false
  properties:
    extension_id:
      type: string
      pattern: "^[A-Z][A-Z0-9_]+$"    # e.g., HRE, DGA, ARE
    annotation_key:
      type: string
      pattern: "^[a-z][a-z0-9_]+$"    # e.g., min_hardware_profile
    value:
      description: "Annotation value. Any JSON-serializable type."

# Then in DdrNode:
extension_annotations:
  type: array
  items:
    $ref: "#/$defs/ExtensionAnnotation"
  default: []
```

This is a breaking schema change (changes from Map to Array) but produces richer validation and enables querying annotations by `extension_id` without key parsing. Each annotation is a first-class typed object rather than a key-value pair.

#### Notes-010

Option A is non-breaking and immediately deployable. Option B is a superior data model but requires a schema migration. Recommend Option A for v4.1 and Option B as a v5.0 schema evolution target.

---

### ISSUE-011: ORL-R7 Migration Is Unresolved in a "Finalized" Specification

<!-- AGENT_CONTEXT
id:          ISSUE-011
status:      OPEN
severity:    MODERATE
type:        MIGRATION_GAP
tier_refs:   [GPCL]
section_ref: Appendix B
rule_refs:   []
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `MIGRATION_GAP`
**Tiers Affected:** `GPCL` | **Spec Section:** Appendix B, Rule Migration Table

#### Problem Statement-011

The YAML migration record for `ORL-R7` explicitly notes: *"NOTE — Audit C-3: mapping marked TBD in source doc; assigned here pending board confirmation."* An unconfirmed rule migration in a specification carrying `system_metadata.status: Finalized` means the v3.1.1→v4.0 migration traceability chain is broken for any project that had `ORL-R7` content.

#### Evidence & Justification-011

`ddr_system_v4_0.yaml` rule_map entry:

```yaml
- from_rule_ids: "ORL-R7"
  to_rule_ids: "GPCL-R10"
  consolidation_status: "1:1"
  notes: >
    NOTE — Audit C-3: mapping marked TBD in source doc;
    assigned here pending board confirmation.
```

A `TBD` migration assignment in a `Finalized` document is a specification integrity violation by the system's own `AX-3` standard (determinism). The `Finalized` status signal tells practitioners that the document is complete and safe to use as an authoritative reference — which is false while an unresolved migration mapping exists.

#### Impact Assessment-011

- Any v3.1.1 project with `ORL-R7` content has no authoritative guidance on where that content migrates in v4.0.
- The `Finalized` status creates false confidence in specification completeness.
- If `Audit C-3` refers to an unresolved architectural board decision, proceeding with implementation risks building against an unconfirmed rule — requiring a retroactive fix.

#### Resolution-011: Option A — Resolve the ORL-R7 Mapping and Update Status

Confirm the correct `ORL-R7` → `GPCL-RN` destination with the DDR Architecture Board. Update the YAML `rule_map` entry with the confirmed mapping and remove the TBD note. Update `system_metadata.status` from `"Finalized"` to `"Active"` (a less absolute status claim) or keep `"Finalized"` only after all TBD items are resolved. Add a changelog entry documenting the resolution.

#### Resolution-011: Option B — Introduce a `"Finalized-Pending-[AUDIT-ID]"` Status Value

Add `"Finalized-Pending"` as a valid `system_metadata.status` value to indicate: *"The specification is complete and authoritative except for explicitly enumerated open items listed in the `pending_finalization` field."* This allows the specification to be used as a working reference without falsely claiming complete finalization:

```yaml
system_metadata:
  status: "Finalized-Pending"
  pending_finalization:
    - audit_id: "Audit C-3"
      description: "ORL-R7 → GPCL-RN mapping requires board confirmation."
      impact: "Projects with ORL-R7 content cannot migrate until resolved."
      target_resolution: "2026-03-15"
```

Validators can check `pending_finalization` list length before declaring a project based on this spec as CLEAN.

#### Notes-011

Option A is the correct long-term resolution. Option B provides an honest intermediate state while board confirmation is pending. Both should be implemented: Option B now (honest status signal), Option A when the board decision is made. "Audit C-3" reference should be resolved or documented as an internal architecture review identifier.

---

### ISSUE-012: Candidate Pool Has No Pause State

<!-- AGENT_CONTEXT
id:          ISSUE-012
status:      OPEN
severity:    MINOR
type:        LIFECYCLE_GAP
tier_refs:   [ARE_E5]
section_ref: §8.2
rule_refs:   []
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MINOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** ARE (E5) | **Spec Section:** §8.2

#### Problem Statement-012

The Candidate Pool lifecycle defines only two states for ARE activation: active (generating candidates) and disabled (Pool discarded). There is no intermediate state that preserves an existing Candidate Pool while halting new candidate generation — forcing practitioners to either complete Pool reviews before disabling ARE or lose all pending candidates.

#### Evidence & Justification-012

§8.2: *"Candidate nodes... are automatically discarded when ARE is disabled."* No partial deactivation, pause, or hold state is defined. In agentic workflows where ARE may be resource-intensive, temporarily disabling inference while retaining review candidates is a natural operational need.

#### Impact Assessment-012

Mid-review Pool loss in large projects (50+ candidates) forces a complete re-inference cycle on ARE re-activation. In cost-sensitive environments, this is a meaningful operational inefficiency.

#### Resolution-012: Option A — Add `paused` to ARE Activation States

Define three ARE activation states: `active | paused | disabled`. When `paused`: ARE generates no new candidates; existing Candidate Pool is retained and fully browsable; promotion via INSERT and discards remain available. When set from `paused` to `disabled`: Pool is discarded. When set from `paused` to `active`: inference resumes, adding to the existing Pool.

#### Resolution-012: Option B — Add an Explicit Pool Snapshot Operation

Define a `SNAPSHOT_POOL` operation within the ARE Extension (not Core): *"Serialises the current Candidate Pool to a named file in `.agent/are_snapshots/`. The Pool can subsequently be restored via `RESTORE_POOL [snapshot_name]` after ARE is re-enabled."* This provides Pool persistence without requiring a new activation state, and snapshot files are human-readable for manual review.

#### Notes-012

Option A is simpler and more intuitive for users. Option B is more flexible and enables persistent Pool archival for audit purposes. This is a Minor issue with no impact on Core validity.

---

### ISSUE-013: DDE Upward FCL Annotation Creates a Backwards Validation Dependency

<!-- AGENT_CONTEXT
id:          ISSUE-013
status:      OPEN
severity:    MINOR
type:        DESIGN_INADEQUACY
tier_refs:   [FCL, DDE_E7]
section_ref: §9 (E7 DDE)
rule_refs:   [FCL-R1, DDE-R1, DDE-R3]
created:     2026-02-28
updated:     2026-02-28
resolved:    null
-->

**Status:** `OPEN` | **Severity:** `MINOR` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `FCL`, DDE (E7) | **Spec Section:** §9 Extension E7

#### Problem Statement-013

`DDE` (Data Domain Extension) annotates `FCL` nodes to flag functional capabilities that imply data domain schemas not yet formally specified in `ICL`. This creates a backwards validation dependency: FCL completeness is assessed only *after* ICL content exists for DDE to read — inverting the intended top-down authoring flow. Additionally, if DDE consistently flags FCL for missing schema implications, it suggests FCL has a missing inclusion rule that should be in Core.

#### Evidence & Justification-013

DDE contract: *"Reads: FCL, GPCL, SAL, ICL, CDL. Annotates: ICL, SAL, FCL."* The FCL annotation purpose: *"flag functional capabilities that imply data domain schemas not yet formally specified in ICL."*

If DDE reliably detects data schema implications in FCL nodes that were not captured in FCL content, the FCL tier is structurally incomplete for data-heavy applications. The Extension is doing discovery work that should have been done at FCL authoring time. An Extension that reliably discovers FCL deficiencies is evidence of a missing Core rule.

#### Impact Assessment-013

- FCL nodes authored without DDE active will silently lack data schema implications, creating ICL gaps discoverable only if DDE is later activated — making FCL completeness DDE-dependent.
- The backwards validation pattern (ICL content needed before FCL gaps visible) conflicts with the top-down authoring mandate of the DAG hierarchy.

#### Resolution-013: Option A — Add FCL-R7 to Mandate Data Entity Enumeration in FCL

Add a Core inclusion rule to the FCL tier: *"`FCL-R7`: For capabilities that create, read, update, or delete persistent data entities, must enumerate the data entities involved by logical name. Technology-neutral (no schema, no field types — just entity names and their relationship to the capability)."* This shifts data entity discovery from DDE advisory (downstream, reactive) to FCL authorship (upstream, proactive), making DDE's FCL annotations confirmatory rather than discovery-mode.

#### Resolution-013: Option B — Restrict DDE's FCL Annotation Contract

Remove FCL from DDE's `annotates` list and instead surface FCL gap discoveries only via the reconciliation manifest's `extension_advisories` section with `advisory_type: UPSTREAM_GAP`. The advisory would state: *"FCL-N.M implies data entity [EntityName] but no ICL schema is defined. Consider inserting FCL-R7-equivalent content into FCL-N.M."* This preserves DDE's discovery capability while keeping FCL annotation semantics clean — FCL nodes receive annotations only from Extensions that validate them, not from Extensions reading their downstream implications.

#### Notes-013

Option A is the architecturally superior choice — it resolves the root cause (missing Core rule) rather than adjusting the Extension. Option B is acceptable if the FCL-R7 addition is considered out of scope for v4.x. This is a Minor issue that becomes Major for data-intensive projects where FCL completeness is critical.

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue RESOLVED until all steps are confirmed.

```plaintext
1. IDENTIFY issue ID and selected Resolution Option (A or B)
2. DRAFT the specific changes to DDR_System_Opus_v4_.md and/or ddr_system_v4_0.yaml
3. VERIFY draft changes do not introduce new issues (check cross-references in Notes fields)
4. UPDATE the issue entry:
   - Set status: IN_REVIEW
   - Set updated: [date]
5. HUMAN REVIEW of draft changes
6. On approval:
   - Set status: RESOLVED
   - Set resolved: [date]
   - Record resolution: "Option [A|B]: [one-line summary]"
7. UPDATE ISSUE REGISTRY table
8. UPDATE document header metadata (open_issues, resolved_issues)
```

---

## APPENDIX: CROSS-ISSUE DEPENDENCY MAP

> Issues that share a dependency — resolving one may affect the other.

| Issue     | Depends On | Nature of Dependency                                                               |
| --------- | ---------- | ---------------------------------------------------------------------------------- |
| ISSUE-002 | ISSUE-001  | CL topology changes require edge type vocabulary decision first                    |
| ISSUE-004 | ISSUE-001  | `cites` vs `derives` decision affects which rules are "structural"                 |
| ISSUE-005 | ISSUE-004  | GPCL/FCL boundary rule depends on VALIDATE classification outcome                  |
| ISSUE-006 | ISSUE-007  | Status machine must define SUPERSEDE_PENDING if Option B chosen                    |
| ISSUE-009 | ISSUE-004  | ARE scoring rubric references AX-3; outcome depends on AX-3 resolution             |
| ISSUE-010 | ISSUE-001  | Schema `edge_type` enum must be updated if new edge types added                    |
| ISSUE-013 | ISSUE-005  | FCL-R7 (Option A) addresses the same GPCL/FCL mediation gap from a different angle |

---

*DDR System v4.0 Issues Tracker — IT-1.0*
*13 issues identified | 0 resolved | Last updated: 2026-02-28*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*
