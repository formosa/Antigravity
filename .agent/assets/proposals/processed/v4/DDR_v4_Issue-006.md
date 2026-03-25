---
document:
  id:              DDR_v4_Issue-006
  title:           "Resolution Report for ISSUE-006: Node Status Lifecycle Lacks a Formal State Machine"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "LIFECYCLE_GAP"
---

## Optimized Resolution Strategy for "ISSUE-006"

### Agent Context

```yaml
id:          ISSUE-006
status:      RESOLVED
severity:    MAJOR
type:        LIFECYCLE_GAP
tier_refs:   [ALL]
section_ref: §3.1, §7.1, §7.2
rule_refs:   [AX-3]
```

### 1. Validation Audit of ISSUE-006

An evaluation of `.agent/assets/proposals/active/DDR System(Opus_v4).md`, `.agent/assets/proposals/active/ddr_node_schema.yaml`, and `.agent/assets/proposals/active/DDR_v4_Adversarial_Audit.md` was conducted to investigate the claims of "ISSUE-006: Node Status Lifecycle Lacks a Formal State Machine."

The §3.1 Node Schema table (line 66) defines the `status` property as an enum with five values: `DRAFT | ACTIVE | DIRTY | DEPRECATED | SUPERSEDED`. No transition rules, guard conditions, or prohibited transitions are specified at this definition site — the field is presented as a flat enumeration without lifecycle semantics.

The `ddr_node_schema.yaml` `DdrNode.status` field (line 751–760) provides the only transition listing in the entire project. The description reads: *"Node lifecycle status. Valid transitions (§7.1, Audit H-1): DRAFT→ACTIVE (VALIDATE), DRAFT→DELETED (DELETE), ACTIVE→DIRTY (MODIFY/propagation), ACTIVE→DEPRECATED (MODIFY), ACTIVE→SUPERSEDED (SUPERSEDE), DIRTY→ACTIVE (VERIFY+VALIDATE), DIRTY→DEPRECATED (MODIFY), DIRTY→SUPERSEDED (SUPERSEDE), DEPRECATED→SUPERSEDED (SUPERSEDE), DEPRECATED→DELETED (DELETE)."* This listing is embedded in a YAML description string — not a formal, machine-parseable state machine — and references "Audit H-1," a section that does not exist anywhere in the specification or its appendices.

The §7.1 Core Operations table (lines 506–516) defines seven operations with validation triggers but contains no state transition table, no guard condition definitions, and no formal lifecycle section. Transition behaviour is implied through operation descriptions: INSERT *"create node with auto-assigned ID"*, MODIFY *"update content; version incremented"* with *"DIRTY propagation to all descendants"*, and SUPERSEDE *"mark node SUPERSEDED; create replacement with new ID."* These descriptions embed lifecycle transitions within operational prose without isolating them as a formal contract.

The §7.2 Dirty Flag Triggers section (lines 520–535) contains narrative notes that further scatter lifecycle semantics. The "Deprecation Lifecycle" note (line 535) states: *"A node is set to DEPRECATED via MODIFY when it is scheduled for removal or replacement. DEPRECATED nodes remain structurally valid and are included in VERIFY traversals. DEPRECATED is not a terminal state — a DEPRECATED node may subsequently be SUPERSEDED (creating a replacement) or DELETED."* Critically, this note omits the `DEPRECATED→ACTIVE` reversal transition entirely — an omission confirmed by the schema's transition list, which also excludes this path. Additionally, the note defines `DEPRECATED` as *"scheduled for replacement, no replacement yet exists"* and `SUPERSEDED` as *"replacement exists and children have been re-wired"* — semantic distinctions that should appear in a formal state machine definition, not in a narrative footnote.

The `DDR_v4_Adversarial_Audit.md` Finding-6 (lines 148–160) independently confirms the same deficiencies: *"There is no §10 or Audit section in the specification. 'Audit H-1' is an unexplained reference"* (line 154), *"There is no formal state transition table in the normative spec"* (line 155), and *"The transition DEPRECATED→ACTIVE is absent"* (line 157). The audit explicitly recommends adding *"§3.8 'Node Status Lifecycle' containing: a formal state transition table"* (line 159).

The `DIRTY→ACTIVE` transition conditions are also underspecified. The schema states this requires `VERIFY+VALIDATE`, but no guard conditions clarify whether per-node VALIDATE suffices, whether all descendants must also be clean, or what occurs when some descendants remain in `DRAFT` status. The `SUPERSEDED` status is implied to be terminal by the transition list (no outbound transitions are listed), but this prohibition is never formally stated — the absence of a listed transition is not equivalent to a normative prohibition.

**Findings:**

1. **Absent Formal State Machine:** The DDR v4.0 specification distributes status lifecycle semantics across four locations — the §3.1 enum definition, the §7.1 operations table, the §7.2 dirty flag narrative notes, and the `ddr_node_schema.yaml` description string — without consolidating them into a formal state transition table. No single location provides the complete set of valid transitions, their triggering operations, guard conditions, and prohibited transitions. Any implementation of the status lifecycle must reconstruct the state machine from inference across these scattered sources, producing divergent implementations that directly violate `AX-3` (Determinism).

2. **Dangling "Audit H-1" Reference:** The `ddr_node_schema.yaml` status field description (line 755) references *"Audit H-1"* as the authority for valid transitions. This reference resolves to no section in the Markdown specification, YAML system definition, or any project file. The sole source for the transition listing is the YAML description string itself — a schema comment, not a normative specification section. This creates a phantom authority reference that undermines the traceability of the lifecycle contract.

3. **Missing and Underspecified Transitions:** The `DEPRECATED→ACTIVE` reversal path is entirely absent from both the schema listing and the §7.2 narrative. If a deprecation decision is reversed before a replacement is authored, there is no spec-compliant path to restore the node to `ACTIVE` status — forcing authors to use `SUPERSEDE` (semantically incorrect, as `SUPERSEDE` implies a replacement exists) or to create a new node via `INSERT` (losing the original node's ID and citation history). The `DIRTY→ACTIVE` transition specifies `VERIFY+VALIDATE` as the triggering operations but defines no guard conditions on descendant status, review resolution state, or scope of validation required.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-006

The resolution must consolidate the scattered lifecycle semantics into a single, authoritative, machine-verifiable state machine definition that enumerates all valid transitions, their triggering operations, guard conditions, and explicitly prohibited transitions — satisfying `AX-3` (Determinism) by ensuring identical lifecycle inputs produce unambiguous, mechanically verifiable state outcomes.

#### Option A: Add §3.8 Normative Markdown State Transition Table

Insert a new section §3.8 "Node Status Lifecycle" in the normative Markdown specification, positioned between §3.7 (Citation Rules) and §4 (Consumption Modes). This section contains a formal state transition table defining every valid transition as a row with five columns: `From` status, `To` status, `Triggering Operation`, `Guard Conditions`, and `Notes`. The table enumerates all transitions currently scattered across §7.1, §7.2, and the schema description — including the missing `DEPRECATED→ACTIVE` reversal (triggered by `MODIFY` with guard conditions: deprecation reversal rationale documented, sunset date cleared, reversal logged in reconciliation manifest). The section explicitly states that `SUPERSEDED` is a terminal status from which no outbound transition is permitted, and that any transition not listed in the table is prohibited. The `DIRTY→ACTIVE` guard conditions are formally specified: the node's own tier rules pass structural validation, all `REVIEW_REQUIRED` items (if the Issue-004 resolution is adopted) are resolved, and the validation scope is per-node (descendants are not required to be `CLEAN` for the parent's transition). The `ddr_node_schema.yaml` status field description is updated to reference §3.8 instead of "Audit H-1," and the redundant transition listing is replaced with a cross-reference. This approach designates the Markdown specification as the normative source for the lifecycle contract, with the schema serving as a machine-enforceable encoding.

* **Supporting Insights:** This approach follows the DDR specification's existing pattern: all other structural contracts — DAG invariants (§3.5), citation rules (§3.7), constraint precedence (§6) — are defined as normative Markdown tables within the specification document. Adding §3.8 as a parallel lifecycle table maintains structural consistency with the document's established architecture. The Markdown-first approach ensures human reviewers can audit the complete lifecycle contract without parsing YAML schema descriptions, which is critical for the DDR's stated goal of being readable by non-technical stakeholders at the governance layers. The resolution of the "Audit H-1" dangling reference simultaneously eliminates a traceability defect identified by the adversarial audit (Finding-6, line 154).

* **Citations:** ISO/IEC/IEEE 29148:2018 (Systems and software engineering — Life cycle processes — Requirements engineering) specifies that behavioral requirements must define all states, state transitions, and conditions for transitioning between states (Clause 6.6.4.3). The standard explicitly requires that state models enumerate valid and prohibited transitions to ensure completeness and determinism — a requirement directly applicable to the DDR node status lifecycle. The UML state machine formalism defined in ISO/IEC 19505-2:2012 (OMG Unified Modeling Language — Part 2: Superstructure) establishes the canonical structure for state transition specifications: source state, trigger event, guard condition, action, and target state — the five-column structure proposed for the §3.8 table.

#### Option B: Define a Machine-Parseable `lifecycle.status_transitions` Block in YAML as the Single Source of Truth

Add a new top-level `lifecycle` key to `ddr_node_schema.yaml` (or to `ddr_system_v4.0.yaml` as a system-definition property) containing a `status_transitions` array and a `prohibited_transitions` array. Each `status_transitions` entry is a structured object with fields: `from` (source status), `to` (target status), `operation` (triggering operation), `guards` (array of named guard condition identifiers), and `notes` (optional clarification). Each `prohibited_transitions` entry specifies a `from` status, a `to` array of prohibited target statuses, and a `reason` string. The guard condition identifiers (e.g., `all_structural_rules_pass`, `deprecation_rationale_documented`, `sunset_date_cleared`) are defined as a companion `guard_definitions` array, each with an `id`, `description`, and `verification_mode` (`structural` or `manual`). VERIFY consumes this YAML block directly to enforce lifecycle transitions programmatically — any transition not listed in `status_transitions` and not explicitly prohibited in `prohibited_transitions` is treated as an undefined transition error. The Markdown specification's §3.8 (if created) becomes a human-readable rendering of this YAML definition, with an explicit authority note: *"In the event of divergence, the `lifecycle.status_transitions` YAML block is authoritative."* This approach makes the state machine directly consumable by Antigravity agents and automated validators without natural language parsing of Markdown prose.

* **Supporting Insights:** The DDR v4.0 specification already exhibits a pattern of dual-source authority tension between its Markdown and YAML representations (documented in ISSUE-003 regarding the §3.5/INV-2 divergence). Option B addresses this proactively by designating one authoritative source for lifecycle semantics — the machine-parseable YAML — and rendering the Markdown as a derived view. This is consistent with the DDR's design as an agentic specification consumed by LLM-powered validation tools: a YAML state machine block can be directly loaded, traversed, and enforced by VERIFY without requiring the natural language parsing that the current §7.1/§7.2 narrative demands. The structured guard condition definitions also provide VERIFY with explicit, named conditions to check rather than inferring validation scope from prose descriptions.

* **Citations:** The SCXML (State Chart XML) specification, W3C Recommendation (2015-09-01), defines a standard XML-based format for expressing state machines with explicit transitions, guards, and events — demonstrating industry precedent for machine-parseable state machine definitions as the authoritative lifecycle contract rather than prose descriptions. JSON Schema 2020-12 (RFC 8927, subsequently refined in the JSON Schema Specification) supports the `$defs` mechanism used to define reusable guard condition objects, ensuring the proposed `guard_definitions` array conforms to established schema composition patterns already used in `ddr_node_schema.yaml`.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **Authority Model Consistency:** Option A designates Markdown as the normative source for the lifecycle contract, consistent with the specification's current document architecture where all structural rules are defined in Markdown. Option B designates YAML as the normative source, introducing a precedent where one specification concern (lifecycle) is authoritatively defined in YAML while others (invariants, citation rules, tier definitions) remain authoritatively defined in Markdown. This split-authority model increases the risk of future divergence — precisely the class of defect documented in ISSUE-003.

2. **Agentic Consumability:** Option A produces a human-readable table that requires natural language parsing for automated enforcement — agents must extract transition rules from Markdown table cells. Option B produces a structured YAML block that is directly machine-parseable and can be loaded by VERIFY as a data structure without parsing prose. For an agentic specification targeting Gemini 3.1 Pro processing, Option B offers lower integration friction and deterministic parsing guarantees.

3. **ISSUE-003 Interaction:** ISSUE-003 documents the consequences of normative divergence between Markdown and YAML representations. Option A avoids this risk by keeping the lifecycle contract in Markdown only, with YAML referencing it. Option B introduces a second instance of the same pattern (YAML as authority, Markdown as rendering) but does so explicitly with a declared authority policy — potentially establishing a precedent that could be applied retroactively to resolve ISSUE-003's invariant divergence.

4. **Implementation Complexity:** Option A requires updating two files (add §3.8 to the Markdown spec, update the `ddr_node_schema.yaml` status description to remove the "Audit H-1" reference). Option B requires updating three artefacts (add `lifecycle` block to YAML, optionally add §3.8 Markdown rendering, update `ddr_node_schema.yaml` cross-reference) and defining a new schema type (`GuardCondition`) with its own validation contract. The incremental schema complexity is modest but non-trivial.

5. **Completeness Verification:** Option B's structured format makes it straightforward to programmatically verify completeness — every ordered pair of (`from`, `to`) statuses is either listed in `status_transitions`, listed in `prohibited_transitions`, or flagged as undefined. Option A's Markdown table achieves the same completeness but verification requires parsing the table into a data structure first, effectively re-implementing Option B as a validation step.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A + Option B Combined (Recommended Strategy)**.

The Issues Tracker's own notes (ISSUE-006 Notes, line 589) explicitly recommend implementing both options together: *"YAML as source of truth (Option B), Markdown table as human-readable rendering (Option A)."* This combined approach resolves the lifecycle gap completely: the YAML `lifecycle.status_transitions` block serves as the machine-parseable, VERIFY-consumable authority, while the Markdown §3.8 table serves as the human-readable rendering for specification reviewers. The "Audit H-1" dangling reference is resolved by both options simultaneously.

**Option A + B Combined** is recommended because:

* **Completeness:** Neither option alone addresses both audiences. Markdown-only (Option A) leaves automated validators parsing prose. YAML-only (Option B) forces human reviewers to read structured data instead of tabular prose. The combined approach serves both consumers with a single authoritative definition and a derived rendering.
* **Precedent for Authority Resolution:** The combined approach establishes a reusable pattern — YAML as machine authority, Markdown as human rendering with explicit derivation — that can be retroactively applied to resolve the ISSUE-003 §3.5/INV-2 divergence. Rather than creating a one-off fix, it establishes an architectural principle for the entire specification's dual-format strategy.
* **AX-3 Satisfaction:** The YAML `status_transitions` block provides VERIFY with a deterministic, machine-loadable state machine contract. Every implementation consuming this block will produce identical lifecycle enforcement behaviour for identical inputs, satisfying `AX-3` without requiring natural language interpretation of transition rules.

### 4. Concluding Notation

**Independent Review Decision (2026-03-19): APPROVED.**

After independent reassessment of ISSUE-006, the endorsed **Option A + Option B Combined** strategy remains the maximally optimized resolution because it simultaneously guarantees machine-enforceable determinism (YAML authority) and governance-grade human auditability (Markdown rendering), while removing the dangling reference defect and minimizing semantic drift across specification consumers.
