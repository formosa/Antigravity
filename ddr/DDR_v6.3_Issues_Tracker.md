# DDR System v6.3 — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the DDR System v6.3. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read the issue heading plus the `Status`, `Severity`, and `Type` metadata lines before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              ITR-7C9FFB6E-5639-4276-BEE3-C17206360828
  title:           "DDR System v6.3 — Issues Tracker"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.3"
  created:         "2026-04-01"
  last_modified:   "2026-04-01"
  author:          "Anthony Formosa"
  open_issues:     17
  resolved_issues: 0
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT
    - DESIGN_INADEQUACY
    - UNNECESSARY_COMPLEXITY
    - AXIOM_VIOLATION
    - SCHEMA_DEFECT
    - MIGRATION_GAP
    - LIFECYCLE_GAP
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every updated issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.
> If an issue later becomes `RESOLVED`, a one-line blockquote resolution note may be
> inserted above `#### Problem Statement-[NNN]`.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the issue. 2-4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the local spec plus the logic that makes this a problem.]

#### Impact Assessment-[NNN]
[Concrete failure mode if the issue is not resolved.]

#### Resolution-[NNN]: Option A - [Short Label]
[First resolution approach.]

#### Resolution-[NNN]: Option B - [Short Label]
[Second, materially different approach.]

#### Resolution-[NNN]: Option C - [Short Label]
[Third, materially different approach.]

#### Comparative Analysis-[NNN]
[Direct comparison of Options A, B, and C.]

#### Recommendation-[NNN]
**Endorsed Option:** `Option A|B|C`
[Precise technical justification for the endorsed option.]

#### Supporting Citations-[NNN]
- [Source Name](https://example.com): One-line explanation of why the source supports the endorsed option.

#### Notes-[NNN]
[Cross-references, dependencies, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID | Severity | Type | Status | Tiers Affected | Title |
| --- | --- | --- | --- | --- | --- |
| [ISSUE-001](#issue-001-enforce-sil-parent_ids-minitems-in-ddrnode-conditional) | `CRITICAL` | `SCHEMA_DEFECT` | `OPEN` | `SIL, XPD` | Enforce SIL `parent_ids` minItems in DdrNode conditional |
| [ISSUE-002](#issue-002-resolve-score-band-boundary-ambiguity) | `CRITICAL` | `LOGICAL_CONFLICT` | `OPEN` | `ARE scoring` | Resolve score band boundary ambiguity |
| [ISSUE-006](#issue-006-add-deprecated--dirty-lifecycle-transition) | `CRITICAL` | `LIFECYCLE_GAP` | `OPEN` | `All tiers` | Add DEPRECATED → DIRTY lifecycle transition |
| [ISSUE-003](#issue-003-remove-extends-from-tierrelationship-edge_type) | `MAJOR` | `AXIOM_VIOLATION` | `OPEN` | `All tiers` | Remove `extends` from TierRelationship edge_type |
| [ISSUE-004](#issue-004-add-validation-guards-to-deprecated--active-transition) | `MAJOR` | `LIFECYCLE_GAP` | `OPEN` | `All tiers` | Add validation guards to DEPRECATED → ACTIVE transition |
| [ISSUE-005](#issue-005-require-content-field-in-ddrnode-schema) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | `All tiers` | Require `content` field in DdrNode schema |
| [ISSUE-008](#issue-008-add-required-fields-to-system_metadata) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | `System metadata` | Add required fields to `system_metadata` |
| [ISSUE-009](#issue-009-document-delete-operation-lifecycle-semantics) | `MAJOR` | `LIFECYCLE_GAP` | `OPEN` | `All tiers` | Document DELETE operation lifecycle semantics |
| [ISSUE-012](#issue-012-specify-unbundle-behavior-for-inactive-tier-fragments) | `MAJOR` | `DESIGN_INADEQUACY` | `OPEN` | `Express Mode G1, G2` | Specify UNBUNDLE behavior for inactive-tier fragments |
| [ISSUE-007](#issue-007-remove-issue-007-commentary-from-normative-text) | `MODERATE` | `UNNECESSARY_COMPLEXITY` | `OPEN` | `DAG invariants` | Remove ISSUE-007 commentary from normative text |
| [ISSUE-010](#issue-010-replace-guardidref-closed-enum-with-pattern) | `MODERATE` | `DESIGN_INADEQUACY` | `OPEN` | `Lifecycle guards` | Replace GuardIdRef closed enum with pattern |
| [ISSUE-011](#issue-011-constrain-project-object-in-system_definition-profile) | `MODERATE` | `LOGICAL_CONFLICT` | `OPEN` | `System definition` | Constrain `project` object in system_definition profile |
| [ISSUE-013](#issue-013-prevent-extensionruleid-pattern-overlap-with-tier-ids) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | `Extension rules` | Prevent ExtensionRuleId pattern overlap with tier IDs |
| [ISSUE-014](#issue-014-add-global-rule_id-uniqueness-requirement) | `MODERATE` | `DESIGN_INADEQUACY` | `OPEN` | `Tier definitions` | Add global rule_id uniqueness requirement |
| [ISSUE-015](#issue-015-fix-version_history-v10-empty-date-field) | `MINOR` | `SCHEMA_DEFECT` | `OPEN` | `Version history` | Fix version_history v1.0 empty date field |
| [ISSUE-016](#issue-016-require-topology-fields-in-tierdefinition) | `MINOR` | `SCHEMA_DEFECT` | `OPEN` | `Tier definitions` | Require topology fields in TierDefinition |
| [ISSUE-017](#issue-017-define-errata_log-operational-guidance) | `MINOR` | `DESIGN_INADEQUACY` | `OPEN` | `Errata system` | Define errata_log operational guidance |

---

## ISSUES

---

### ISSUE-001: Enforce SIL `parent_ids` minItems in DdrNode Conditional

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `SIL, XPD` | **Spec Section:** `§3.1 DdrNode, §3.5 INV-5, §3.7 CIT-R1`

#### Problem Statement-001

The `DdrNode` allOf block (schema lines 1548–1555) enforces only an ID-pattern constraint for SIL nodes but does not set `parent_ids.minItems: 1`. Every other non-root-eligible tier (GPCL, FCL, CL, SAL, ICL, CDL, ISL) includes `parent_ids: { minItems: 1 }` in its DdrNode conditional. The document-level allOf (lines 78–95) correctly enforces SIL `minItems: 1` when XPD is in `active_tiers`, but this enforcement is invisible to validators operating on `DdrNode` in isolation.

#### Evidence & Justification-001

- Schema lines 1548–1555: SIL conditional sets only `id: pattern: "^SIL-[0-9]+\\.[0-9]+$"` — no `parent_ids` constraint.
- Schema lines 1559–1565 (GPCL), 1566–1575 (FCL), 1576–1585 (CL), 1586–1595 (SAL), 1596–1605 (ICL), 1606–1615 (CDL), 1616–1625 (ISL): all include `parent_ids: { minItems: 1 }`.
- Schema lines 78–95: document-level conditional enforces SIL `parent_ids.minItems: 1` only when `active_tiers` contains XPD.
- `CIT-R1` (Semantic Authority line 320): "Every non-root node must have ≥1 parent_id."
- SIL `parent_relationships` (line 488–494): derives from XPD when active, root when XPD inactive.

#### Impact Assessment-001

A `DdrNode` validator operating on isolated node payloads (e.g., an API context) would accept a SIL node with `parent_ids: []` in a project where XPD is active. The orphaned SIL node enters the DAG, violating AX-1 and CIT-R1. VERIFY catches the violation later, but by then the node may have downstream dependents, and removal cascades DIRTY across the graph.

#### Resolution-001: Option A - Add SIL minItems to DdrNode Conditional

Add `parent_ids: { minItems: 1 }` to the SIL tier conditional in `DdrNode.allOf`, matching the treatment of all other non-root-eligible tiers. The document-level allOf would need no changes since it already handles the XPD-conditional case.

#### Resolution-001: Option B - Add Root-Eligibility Conditional for SIL in DdrNode

Add a two-branch conditional to `DdrNode.allOf`: if XPD is in `active_tiers`, require `parent_ids.minItems: 1` for SIL; if XPD is absent, permit `parent_ids.minItems: 0`. This models SIL dual root/non-root semantics within the node definition itself.

#### Resolution-001: Option C - Enforce via Secondary Validator Only

Leave the `DdrNode` schema unchanged. Add a normative statement requiring that secondary validators (VERIFY, conformance tools) enforce SIL `parent_ids.minItems: 1` when XPD is active. Document the gap as an intentional schema design decision: DdrNode-level validation is intentionally relaxed for SIL to accommodate both root and non-root semantics.

#### Comparative Analysis-001

Option A is the smallest structural fix, bringing SIL into alignment with every other non-root tier. It defaults to rejecting orphans, with the document-level allOf overriding for root-SIL cases. Option B precisely models dual semantics but requires DdrNode-level access to `active_tiers` (a document-level field), which JSON Schema cannot natively provide without restructuring. Option C preserves the current schema but defers enforcement to runtime, weakening the schema's fail-fast guarantee and violating AX-3's demand for mechanically verifiable determinism at the schema level.

#### Recommendation-001

**Endorsed Option:** `Option A`

Option A is endorsed because it aligns SIL with every other non-root tier's DdrNode conditional, making standalone node validation fail-safe by rejecting orphans by default. The document-level allOf (lines 78–95) already handles the XPD-conditional relaxation where `active_tiers` context is available. This is the smallest correct patch with no schema restructuring required.

#### Supporting Citations-001

- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance on if/then/else patterns for tier-conditional enforcement in JSON Schema 2020-12.
- [JSON Schema Applying Subschemas](https://json-schema.org/understanding-json-schema/reference/combining): Guidance on allOf composition used for layered document-level and node-level constraints.

#### Notes-001

The document-level allOf at lines 78–95 currently only handles the "XPD active → SIL must have parents" case. If Option A is adopted, no additional document-level change is needed since adding `minItems: 1` to SIL's DdrNode conditional and then relaxing via document-level allOf for root-SIL is consistent with the existing pattern.

---

### ISSUE-002: Resolve Score Band Boundary Ambiguity

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `ARE scoring` | **Spec Section:** `§9 E5 ARE, are_scoring_profiles`

#### Problem Statement-002

The `score_bands` arrays in both scoring profiles use two-element ranges with overlapping boundary values (e.g., `[0.0, 0.4]`, `[0.4, 0.7]`, `[0.7, 1.0]`). Neither the Semantic Authority nor the Machine Contract specifies whether these are closed `[a, b]` or half-open `[a, b)` intervals. A score of exactly `0.4` or `0.7` matches two adjacent bands simultaneously, making classification non-deterministic.

#### Evidence & Justification-002

- Semantic Authority lines 1850–1862 (`standard_v1.score_bands`): speculative `[0.0, 0.4]`, probable `[0.4, 0.7]`, high_confidence `[0.7, 1.0]`.
- Semantic Authority lines 1889–1901 (`conservative_v1.score_bands`): identical boundary values.
- `validation_note` (line 1949): mentions "score-band ordering and non-overlap checks" as a requirement, but the normative bands themselves overlap at boundary values.
- `AX-3` (line 119): "Identical inputs produce unambiguous, mechanically verifiable outputs."

#### Impact Assessment-002

Two ARE implementations scoring a candidate at exactly `0.7` would classify it differently — one as "probable", the other as "high_confidence" — producing different promotion guidance for the same score under the same profile. This directly violates AX-3 determinism.

#### Resolution-002: Option A - Adopt Half-Open Interval Convention

Define all score bands as `[lower, upper)` with the final band using `[lower, upper]`. Add a normative statement to the `are_scoring_profiles` section.

#### Resolution-002: Option B - Shift Boundaries to Eliminate Overlap

Redefine standard profiles to use non-overlapping boundaries: `[0.0, 0.39]`, `[0.40, 0.69]`, `[0.70, 1.0]`.

#### Resolution-002: Option C - Add Explicit Interval Type Field to ScoringProfile

Add an `interval_convention` field to the `ScoringProfile` schema (e.g., `enum: [half_open_lower, closed]`) that machine-readably declares the boundary interpretation. Standard profiles set `interval_convention: half_open_lower`; custom profiles must declare their convention explicitly.

#### Comparative Analysis-002

Option A is the simplest: one normative sentence, no boundary value changes, no schema changes. Option B eliminates ambiguity but changes normative numeric values and introduces precision constraints that may not suit all scoring implementations. Option C provides maximum machine-readability by making the convention a schema-level field, but adds structural complexity for a problem that can be resolved with a single prose convention.

#### Recommendation-002

**Endorsed Option:** `Option A`

Option A is endorsed because the half-open interval convention `[lower, upper)` is the mathematical standard for partitioning continuous ranges. It preserves current boundary values unchanged and requires only a single normative sentence. AX-3 demands determinism; a convention-based fix achieves determinism with minimal specification churn.

#### Supporting Citations-002

- [IEEE 754-2019 Floating-Point Arithmetic](https://standards.ieee.org/ieee/754/6210/): The foundational standard for floating-point representation and comparison, establishing precision semantics for boundary value comparisons.
- [JSON Schema Numeric Validation](https://json-schema.org/understanding-json-schema/reference/numeric): Official guidance on numeric range constraints, supporting the minimum/maximum pattern used by score_bands.

#### Notes-002

The custom profile `validation_note` already references "non-overlap checks" — adopting Option A makes this requirement mechanically achievable. No dependency on other issues.

---

### ISSUE-003: Remove `extends` from TierRelationship edge_type

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `AXIOM_VIOLATION`
**Tiers Affected:** `All tiers` | **Spec Section:** `§3.2, §3.7 CIT-R5, §5 TierRelationship`

#### Problem Statement-003

`TierRelationship.edge_type` (schema line 885) allows `[derives, constrains, implements, extends]`, but `ParentCitation.edge_type` (line 1640) correctly restricts to `[derives, constrains, implements]` per CIT-R5. No tier definition in the Semantic Authority uses `extends` in any `parent_relationships` or `child_relationships` entry. Allowing `extends` in `TierRelationship` contradicts CIT-R5 and AX-6, since these are Core structural fields.

#### Evidence & Justification-003

- Schema line 885: `TierRelationship.edge_type` enum includes `extends`.
- Schema line 1640: `ParentCitation.edge_type` enum excludes `extends`.
- `CIT-R5` (Semantic Authority line 336): "Extension extends edges are stored in extension_annotations only — never in parent_ids."
- No tier definition in lines 408–1112 uses `extends` in any relationship array.

#### Impact Assessment-003

An author defining a custom tier with `child_relationships: [{tier: SAL, edge_type: extends}]` would produce a schema-valid but semantically invalid topology, implying Extension edges exist in Core structural hierarchy. This undermines AX-5/AX-6 Extension isolation.

#### Resolution-003: Option A - Remove extends from TierRelationship Enum

Restrict `TierRelationship.edge_type` to `[derives, constrains, implements]`.

#### Resolution-003: Option B - Add Normative Note Prohibiting extends Usage

Keep `extends` in the enum but add a validation rule prohibiting its use in `parent_relationships` and `child_relationships`.

#### Resolution-003: Option C - Split TierRelationship into Core and Extension Variants

Create `CoreTierRelationship` (without `extends`) for use in `parent_relationships`/`child_relationships`, and `ExtendedTierRelationship` (with `extends`) for Extension-specific contexts only.

#### Comparative Analysis-003

Option A is the smallest change and eliminates the contradiction at its source. Option B leaves a valid-but-prohibited value in the enum — an anti-pattern for deterministic validation. Option C provides schema-level type safety but introduces new definitions for a problem that affects exactly one unused enum value.

#### Recommendation-003

**Endorsed Option:** `Option A`

Option A is endorsed because `extends` has no legitimate use case in `TierRelationship`. Removing it eliminates a hallucination surface where schema-valid but semantically invalid tier definitions could be produced. The DDR design philosophy demands that every element earn its existence.

#### Supporting Citations-003

- [JSON Schema Enum Validation](https://json-schema.org/understanding-json-schema/reference/string#enum): Official guidance on restricting string values to a closed set, supporting the principle that enums should contain only valid values.

#### Notes-003

Non-breaking change. No existing tier definition uses `extends` in relationships.

---

### ISSUE-004: Add Validation Guards to DEPRECATED → ACTIVE Transition

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `All tiers` | **Spec Section:** `§3.8 lifecycle.status_transitions`

#### Problem Statement-004

The `DEPRECATED → ACTIVE` transition (Semantic Authority lines 2684–2687) uses operation `MODIFY` with guards `[gc-002, gc-003, gc-004]`. These guards are all manual checks (deprecation rationale, sunset date clearance, manifest logging). No validation guard (`gc-001`: structural rules pass) or review guard (`gc-005`: review items resolved) is required. A node returning from DEPRECATED to ACTIVE via MODIFY is never required to pass re-validation, even though its content may have been substantially modified.

#### Evidence & Justification-004

- Semantic Authority lines 2684–2687: `{from: DEPRECATED, to: ACTIVE, operation: MODIFY, guards: [gc-002, gc-003, gc-004]}`.
- `gc-001` (line 2691): "All structural rules for the node pass validation."
- `gc-005` (line 2703): "All review items are resolved."
- `DIRTY → ACTIVE` transition (lines 2652–2656): requires `[gc-001, gc-005, gc-006]` — includes validation.
- `DRAFT → ACTIVE` transition (lines 2629–2632): requires `[gc-001, gc-005]`.

#### Impact Assessment-004

A CDL node deprecated due to outdated content is revived via MODIFY with substantial content rewrite. The DEPRECATED → ACTIVE transition succeeds without structural validation. The node enters ACTIVE with potentially non-conforming content that violates CDL-R1 through CDL-R7.

#### Resolution-004: Option A - Add gc-001 and gc-005 to DEPRECATED → ACTIVE Guards

Add guards `gc-001` and `gc-005` to the existing transition, requiring structural validation and review-item resolution before reactivation.

#### Resolution-004: Option B - Route Through DIRTY as Intermediate

Remove direct DEPRECATED → ACTIVE. Model as DEPRECATED → DIRTY (via MODIFY) then DIRTY → ACTIVE (via VALIDATE).

#### Resolution-004: Option C - Change Operation from MODIFY to VALIDATE

Change the DEPRECATED → ACTIVE transition's operation from `MODIFY` to `VALIDATE`, inheriting VALIDATE's built-in validation semantics. Keep guards `[gc-001, gc-002, gc-003, gc-004, gc-005]`.

#### Comparative Analysis-004

Option A is the smallest correct patch — it adds validation guards to the existing single-step transition. Option B is architecturally cleaner (reuses the existing DIRTY → ACTIVE validated path) but introduces a two-step workflow that increases practitioner burden. Option C changes the triggering operation, which may conflict with the semantic intent that reactivation involves content modification (MODIFY), not just validation.

#### Recommendation-004

**Endorsed Option:** `Option A`

Option A is endorsed because adding validation guards preserves the single-step reactivation workflow while closing the validation gap. It is consistent with the principle that ACTIVE status implies validated content, and mirrors the guard patterns used by DRAFT → ACTIVE and DIRTY → ACTIVE.

#### Supporting Citations-004

- [State Machine Design Patterns](https://statecharts.dev/): Guidance on ensuring state transitions carry appropriate guard conditions, supporting the principle that lifecycle transitions to ACTIVE should require validation.

#### Notes-004

Depends on ISSUE-006: if DEPRECATED → DIRTY is added (for propagation), this issue's resolution must remain compatible with both the propagation path and the reactivation path.

---

### ISSUE-005: Require `content` Field in DdrNode Schema

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All tiers` | **Spec Section:** `§3.1 DdrNode, §5 Tier Definitions`

#### Problem Statement-005

The `DdrNode` required array (schema lines 1420–1427) lists `[id, tier, title, status, version, created, modified]` but omits `content`. A schema-valid DDR node can exist with no content field whatsoever, yet every tier's atomic inclusion rules (e.g., XPD-R1, SIL-R1) presuppose content exists. This creates ambiguity for validators evaluating tier rules against nodes with missing content.

#### Evidence & Justification-005

- Schema lines 1420–1427: `required: [id, tier, title, status, version, created, modified]` — `content` absent.
- Schema lines 1487–1492: `content` defined as `type: string` but not required.
- Semantic Authority line 436: `XPD-R1`: "Must articulate a fundamental human or societal need."
- Semantic Authority line 501: `SIL-R1`: "Must define the core business problem."

#### Impact Assessment-005

A validator processing a node with `status: ACTIVE` and content omitted entirely must determine whether tier rules apply. Different implementations may treat missing content as implicitly empty or as inapplicable, producing inconsistent validation outcomes that violate AX-3.

#### Resolution-005: Option A - Make content Required with Empty String Default

Add `content` to the `DdrNode` required array. The minimum valid value would be `""`. Add a normative note that ACTIVE nodes with empty content are structural violations detectable by VALIDATE.

#### Resolution-005: Option B - Add Lifecycle-Conditional content Requirement

Add a conditional in `DdrNode.allOf` requiring `content` (with `minLength: 1`) when `status` is `ACTIVE`. Leave it optional for DRAFT nodes.

#### Resolution-005: Option C - Add content to required and Set Schema Default

Add `content` to the `DdrNode` required array and add `default: ""` to the content property definition. This ensures backward compatibility — existing documents without content get an implicit empty string during validation rather than failing.

#### Comparative Analysis-005

Option A is the simplest structural fix: content is always present, tier-rule validators always have a defined value to inspect. Option B over-engineers the schema to enforce lifecycle semantics that belong in the operations protocol. Option C extends Option A with a schema-level default that improves backward compatibility for existing documents.

#### Recommendation-005

**Endorsed Option:** `Option A`

Option A is endorsed because requiring `content` as a field ensures tier-rule validators always have a defined value. The semantic content-quality check is the responsibility of tier atomic rules and VALIDATE, not the schema. Making content required with `""` as minimum is a backward-compatible structural clarification.

#### Supporting Citations-005

- [JSON Schema Required Properties](https://json-schema.org/understanding-json-schema/reference/object#required): Official guidance on declaring required object properties in JSON Schema 2020-12.

#### Notes-005

Systems currently omitting `content` from DRAFT nodes would need to provide `content: ""`. This is a non-breaking behavioral change.

---

### ISSUE-006: Add DEPRECATED → DIRTY Lifecycle Transition

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `All tiers` | **Spec Section:** `§3.8 lifecycle.status_transitions, §7 dirty_flag_triggers`

#### Problem Statement-006

The lifecycle `status_transitions` define transitions from DEPRECATED to `SUPERSEDE_PENDING` (via SUPERSEDE) and `ACTIVE` (via MODIFY), but no `DEPRECATED → DIRTY` transition exists. Dirty flag triggers (Semantic Authority lines 1284–1296) affect "all descendants" including DEPRECATED nodes. INV-8 requires the lifecycle to be a complete and closed state machine, and the dirty_flag_notes explicitly state "DEPRECATED is not a terminal state" (line 1332). Yet the lifecycle cannot model DIRTY propagation to a DEPRECATED node.

#### Evidence & Justification-006

- Semantic Authority lines 2665–2687: DEPRECATED transitions only to `SUPERSEDE_PENDING` and `ACTIVE`.
- Lines 1284–1296: dirty_flag_triggers affect "all descendants" — includes DEPRECATED nodes.
- Lines 1329–1335: "DEPRECATED is not a terminal state."
- `INV-8` (line 296): lifecycle must form "a complete and closed state machine."

#### Impact Assessment-006

A project has SIL-1.1 (ACTIVE) → GPCL-2.1 (DEPRECATED). MODIFY on SIL-1.1 should cascade DIRTY to GPCL-2.1 as a descendant, but no valid DEPRECATED → DIRTY transition exists. Implementations must either skip propagation (losing audit trail), apply DIRTY in violation of the state machine, or block the parent MODIFY — all incorrect outcomes.

#### Resolution-006: Option A - Add DEPRECATED → DIRTY Transition with Propagation Side-Effect

Add: `{from: DEPRECATED, to: DIRTY, operation: MODIFY, side_effect: propagation, guards: []}`. This mirrors the existing ACTIVE → DIRTY propagation row.

#### Resolution-006: Option B - Exclude DEPRECATED Nodes from DIRTY Propagation

Add a normative statement excluding DEPRECATED nodes from propagation cascades. Update dirty_flag_triggers to explicitly exclude DEPRECATED nodes.

#### Resolution-006: Option C - Add DEPRECATED → DIRTY and DIRTY → DEPRECATED Bidirectional Path

Add both DEPRECATED → DIRTY (propagation) and DIRTY → DEPRECATED (recovery without reactivation), allowing a DEPRECATED node that was made dirty to return to DEPRECATED after re-validation rather than being forced through ACTIVE.

#### Comparative Analysis-006

Option A is the smallest change that closes the lifecycle gap and preserves CIT-R7 enforcement. The existing DIRTY → ACTIVE path handles recovery. Option B creates a CIT-R7 compliance gap: a DEPRECATED node reinstated to ACTIVE could reference stale parent content without any DIRTY signal. Option C adds a DIRTY → DEPRECATED path that is semantically questionable — why would a re-validated node return to DEPRECATED rather than ACTIVE?

#### Recommendation-006

**Endorsed Option:** `Option A`

Option A is endorsed because the lifecycle state machine must be complete (INV-8). DEPRECATED nodes are non-terminal and may return to ACTIVE — excluding them from propagation creates a CIT-R7 stale-citation gap. The DIRTY → ACTIVE path already exists as recovery, requiring no additional transitions.

#### Supporting Citations-006

- [Finite-State Machine Completeness](https://en.wikipedia.org/wiki/Finite-state_machine): Reference definition for complete state machines where every non-terminal state has defined transitions for all applicable events.

#### Notes-006

ISSUE-004 resolution must be compatible with this issue's resolution. Both affect DEPRECATED node lifecycle paths.

---

### ISSUE-007: Remove ISSUE-007 Commentary from Normative Text

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `UNNECESSARY_COMPLEXITY`
**Tiers Affected:** `DAG invariants` | **Spec Section:** `§3.5 dag_invariants`

#### Problem Statement-007

The Semantic Authority contains inline YAML comments at lines 280–281 referencing a prior issue tracking artifact ("ISSUE-007") directly in the normative `dag_invariants` section. These comments reference an editorial process artifact not part of the DDR specification, violating the `single_source_of_truth` declaration.

#### Evidence & Justification-007

- Semantic Authority lines 280–281: `# ISSUE-007 Change (§3.5 INV-6; satisfies AX-3 determinism and generalized INV-6 atomicity)` and `# ISSUE-007 §3 (Option A + B Combined)`.
- `single_source_of_truth` (line 38): "No conversation record, partial specification, or derivative document carries normative weight."
- `version_history` v5.0 entry (lines 2116–2127): already documents "SUPERSEDE atomicity with SUPERSEDE_PENDING transient state."

#### Impact Assessment-007

New team members reviewing the specification may interpret the ISSUE-007 references as indicating the change is provisional or subject to revision. The historical context is already captured in `version_history`.

#### Resolution-007: Option A - Remove the Comments Entirely

Delete lines 280–281 from the Semantic Authority.

#### Resolution-007: Option B - Move to errata_log or version_history

Remove inline comments and add a corresponding `errata_log` entry.

#### Resolution-007: Option C - Replace with Neutral Design Rationale Comment

Replace the ISSUE-007 references with a neutral design rationale comment: `# INV-6 generalizes SUPERSEDE atomicity across all tiers (v5.0+)` — preserving contextual value without referencing an external artifact.

#### Comparative Analysis-007

Option A is the cleanest — the `version_history` v5.0 entry already captures the change context, making the inline comments redundant. Option B adds the first `errata_log` entry for what is essentially a comment-cleanup task — disproportionate. Option C preserves local context without external references but adds a new comment where deletion would suffice.

#### Recommendation-007

**Endorsed Option:** `Option A`

Option A is endorsed because the version_history already documents the INV-6 change. The inline comments are redundant and add no information not already present. Removing them follows the optimization priority of eliminating dead structure.

#### Supporting Citations-007

- [YAML Specification - Comments](https://yaml.org/spec/1.2.2/#3231-node-properties): Official YAML specification confirming comments carry no semantic value and are excluded from serialization.

#### Notes-007

No dependency on other issues. This is a standalone cleanup.

---

### ISSUE-008: Add Required Fields to `system_metadata`

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `System metadata` | **Spec Section:** `§1 system_metadata`

#### Problem Statement-008

The `system_metadata` object (schema lines 232–258) defines properties `status`, `date`, `scope`, `authority`, `lineage`, `single_source_of_truth`, `design_philosophy`, and `changes_from_prior` with `additionalProperties: false`, but declares no `required` array. A system-definition file could contain `system_metadata: {}` and pass schema validation, producing a normative specification with no declared authority, status, or design philosophy.

#### Evidence & Justification-008

- Schema lines 232–258: `system_metadata` has `additionalProperties: false` but no `required` field.
- Schema lines 59–60: `system_definition` profile requires `system_metadata` to be present, but not its sub-fields.
- Semantic Authority lines 32–58: the actual system_metadata populates `status`, `date`, `scope`, `authority`, `lineage`, `single_source_of_truth`, `design_philosophy`, `changes_from_prior`.

#### Impact Assessment-008

A practitioner forking DDR v6.3 creates a system-definition file with `system_metadata: {}`. It passes schema validation. The document is a normative DDR specification with no declared authority, status, or design philosophy — undermining system-level governance.

#### Resolution-008: Option A - Add required Array to system_metadata

Add `required: [status, date, scope, authority]` to `system_metadata`. Fields like `lineage`, `design_philosophy`, and `changes_from_prior` remain optional (applicable only to non-initial versions).

#### Resolution-008: Option B - Add Profile-Conditional Requirement

In the root `allOf`, when `document_profile: system_definition`, require specific `system_metadata` sub-fields via a conditional nested schema.

#### Resolution-008: Option C - Make All Fields Required

Add `required: [status, date, scope, authority, lineage, single_source_of_truth, design_philosophy, changes_from_prior]` — requiring the full set for any system_metadata object.

#### Comparative Analysis-008

Option A identifies the irreducible minimum (status, date, scope, authority) and requires only those. Option B adds profile-conditional logic for a system with only one system_definition profile — premature generality. Option C requires all fields including `changes_from_prior` and `lineage`, which may not apply to an initial version (v1.0 had no prior version to reference).

#### Recommendation-008

**Endorsed Option:** `Option A`

Option A is endorsed because the four fields represent the irreducible minimum for a normative specification. Strategy B introduces conditional logic for a hypothetical future need. Strategy C forces fields that are meaningless for initial versions.

#### Supporting Citations-008

- [JSON Schema Required Properties](https://json-schema.org/understanding-json-schema/reference/object#required): Official guidance on constraining required object properties.

#### Notes-008

No dependency on other issues. Backward-compatible with the existing Semantic Authority file which already populates all candidate required fields.

---

### ISSUE-009: Document DELETE Operation Lifecycle Semantics

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `All tiers` | **Spec Section:** `§7 operations, §3.8 lifecycle`

#### Problem Statement-009

The `core_operations` section defines DELETE (Semantic Authority line 1187): "Remove node; cascade orphan detection to children." However, `status_transitions` contains zero rows with `operation: DELETE`. The version_history v6.2 entry (line 2146) mentions "DELETE modeled as an operation sink," but this design decision is not documented in the lifecycle section itself. There is no normative statement explaining which statuses permit DELETE or what guards apply.

#### Evidence & Justification-009

- Semantic Authority line 1187: DELETE defined as a core operation.
- Lines 2628–2687: `status_transitions` array — no rows with `operation: DELETE`.
- Line 2146: v6.2 summary mentions "DELETE modeled as an operation sink."
- Lines 2623–2626: lifecycle block is "the machine-parseable authority for DDR node status lifecycle semantics."
- `INV-8` (line 296): lifecycle must be "complete and closed."

#### Impact Assessment-009

An implementer using `status_transitions` as the complete lifecycle authority finds no DELETE transitions and must guess which statuses permit DELETE. They may incorrectly conclude DELETE is prohibited from all statuses, or apply it without guards.

#### Resolution-009: Option A - Add Normative Note with Explicit Status-Eligibility

Add a normative note to the lifecycle section: "DELETE removes the node from the DAG rather than transitioning it to a new status. DELETE may be invoked on nodes in status DRAFT, ACTIVE, DIRTY, or DEPRECATED. DELETE on SUPERSEDED or SUPERSEDE_PENDING nodes is prohibited."

#### Resolution-009: Option B - Document DELETE as Out-of-Lifecycle-Scope

Add a normative note: "DELETE does not produce a status transition; it removes the node. The lifecycle governs status transitions only; node removal is orthogonal."

#### Resolution-009: Option C - Add DELETE Transition Rows with Synthetic Terminal Status

Add transition rows for DELETE from each eligible status to a synthetic `DELETED` terminal status. Add `DELETED` to the `StatusEnum`.

#### Comparative Analysis-009

Option A provides a clear, enumerated status-eligibility list without schema changes, making DELETE deterministic. Option B's "non-terminal, non-transient" phrasing requires interpretation — is SUPERSEDED terminal? Is SUPERSEDE_PENDING transient? Option C adds a new status value to the enum, which is a breaking schema change affecting all implementations and expanding the status surface unnecessarily.

#### Recommendation-009

**Endorsed Option:** `Option A`

Option A is endorsed because it makes DELETE deterministic by explicitly enumerating eligible statuses. The lifecycle block is the authoritative source, and an operation with side-effects (orphan detection, DIRTY propagation) but no lifecycle representation creates an authority gap. Option A closes this gap without schema changes.

#### Supporting Citations-009

- [State Machine Design Best Practices](https://statecharts.dev/): Guidance on modeling destructive operations within state machines, supporting the principle that all operations should have defined lifecycle semantics.

#### Notes-009

No dependency on other issues. The normative note should be placed adjacent to the `status_transitions` array or as a new `lifecycle_notes` field.

---

### ISSUE-010: Replace GuardIdRef Closed Enum with Pattern

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `Lifecycle guards` | **Spec Section:** `§3.8 lifecycle, $defs/GuardIdRef`

#### Problem Statement-010

`GuardIdRef` (schema line 1669–1672) is a closed enum: `[gc-001, gc-002, ..., gc-009]`. Adding a new guard (e.g., `gc-010` for a future lifecycle transition) requires modifying the enum in the Machine Contract. This creates a hard coupling between guard definitions and the schema's type system, making the guard namespace non-extensible without schema version changes.

#### Evidence & Justification-010

- Schema lines 1669–1672: `GuardIdRef: { type: string, enum: [gc-001, gc-002, gc-003, gc-004, gc-005, gc-006, gc-007, gc-008, gc-009] }`.
- `guard_definitions` (Semantic Authority lines 2689–2727): nine definitions, each with `id` matching the enum.
- The enum creates a structural bottleneck: any new guard requires both a `guard_definitions` entry and a schema enum expansion.

#### Impact Assessment-010

Resolving ISSUE-004 or ISSUE-006 may require new guard conditions. Each new guard forces a schema version increment solely to add an enum value, creating churn disproportionate to the change.

#### Resolution-010: Option A - Replace Enum with Pattern

Replace the `GuardIdRef` enum with `type: string, pattern: "^gc-[0-9]+$"`. Guard definitions remain in the Semantic Authority as the normative registry of valid guards. The schema enforces naming convention; the specification governs the actual set.

#### Resolution-010: Option B - Keep Enum with Explicit Version Policy

Keep the closed enum. Add a normative note: "Any new guard definition requires updating the GuardIdRef enum and incrementing the schema version."

#### Resolution-010: Option C - Use Dual Enforcement: Pattern + Enum

Add `pattern: "^gc-[0-9]+$"` to `GuardIdRef` while keeping the enum. The enum serves as a structural whitelist for the current version; the pattern ensures consistency if the enum is expanded.

#### Comparative Analysis-010

Option A decouples guard namespace growth from schema versioning, matching how rule IDs are managed (pattern-based). Option B is correct but maximizes schema churn for minor lifecycle refinements. Option C adds redundant constraints — pattern and enum together — without meaningful benefit since the pattern subsumes the enum's structural role.

#### Recommendation-010

**Endorsed Option:** `Option A`

Option A is endorsed because guard definitions are a semantic concern (specified in the Semantic Authority), not a structural one. Pattern-based enforcement ensures naming consistency while allowing the guard namespace to grow without schema version churn. This matches the treatment of tier rule IDs (e.g., `^[A-Z]+-[RE][0-9]+$`), which use patterns and not closed enums.

#### Supporting Citations-010

- [JSON Schema Pattern Validation](https://json-schema.org/understanding-json-schema/reference/string#regexp): Official guidance on string pattern constraints as an alternative to closed enums.

#### Notes-010

If adopted, the `guard_definitions` array in the Semantic Authority becomes the sole registry of valid guards. Validators should cross-reference `guards` entries against `guard_definitions` at runtime, not at schema level.

---

### ISSUE-011: Constrain `project` Object in system_definition Profile

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `System definition` | **Spec Section:** `§1 document_profile, project`

#### Problem Statement-011

The `project` object schema (lines 116–140) defines fields `name`, `created`, `mode`, and `express_mode_authority` with profile-conditional enforcement for express instances. However, no conditional restricts what a `system_definition` profile may carry in its `project` object. A system-definition file could include `mode: express` and an `express_mode_authority` block — meaningless for a system definition but schema-valid.

#### Evidence & Justification-011

- Schema lines 116–140: `project` defined with `mode` and `express_mode_authority` properties.
- Schema lines 55–78: `system_definition` profile requires `system_metadata`, `axioms`, etc., but imposes no constraints on `project` sub-fields.
- Semantic Authority lines 14–17: actual project for system_definition has `mode: full` — but this is not enforced by schema.

#### Impact Assessment-011

A system-definition file with `project: {name: "DDR v6.3", mode: express}` passes schema validation. An agent or tool parsing the file might attempt to apply express mode semantics to a system definition, producing incorrect behavior.

#### Resolution-011: Option A - Add system_definition Conditional to project

In the root `allOf`, when `document_profile: system_definition`, add a conditional requiring `project.mode: full` (or prohibiting `mode: express` and `express_mode_authority`).

#### Resolution-011: Option B - Add mode to project required and Default to full

Make `mode` required in `project` and enforce `const: full` for system_definition profiles via allOf conditional.

#### Resolution-011: Option C - Remove mode from project for system_definition

Add a `not: { required: [mode] }` constraint to the system_definition conditional, forbidding `mode` entirely in system-definition documents and reserving it exclusively for project instances.

#### Comparative Analysis-011

Option A is the most precise: it constrains `mode` to `full` for system definitions while allowing the field to remain optional. Option B forces `mode` to be required in all profiles, which may impact project instance documents that don't currently declare `mode`. Option C is too restrictive — removing `mode` from system definitions eliminates a potentially useful documentation signal ("this is Full Mode").

#### Recommendation-011

**Endorsed Option:** `Option A`

Option A is endorsed because it narrows the valid `project` configuration for system definitions without altering the project schema for other profiles. The current Semantic Authority already uses `mode: full`, so the constraint merely formalizes existing practice.

#### Supporting Citations-011

- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance on applying profile-specific constraints via if/then/else.

#### Notes-011

No dependency on other issues. The existing Semantic Authority file already satisfies the constraint.

---

### ISSUE-012: Specify UNBUNDLE Behavior for Inactive-Tier Fragments

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `Express Mode G1, G2` | **Spec Section:** `§4 express_mode, UNBUNDLE_SCAN/EXECUTE`

#### Problem Statement-012

Express Mode groups G1 (`[XPD, SIL, GPCL]`) and G2 (`[FCL, CL]`) contain conditionally active tiers (XPD in G1, CL in G2). The `unbundle_determinism_rule` (Semantic Authority lines 384–404) states content must be authored with explicit tier annotations for "deterministic UNBUNDLE allocation," but does not specify what happens when a fragment is annotated with an inactive tier (e.g., `[CL]` annotation in a project where CL is not in `active_tiers`).

#### Evidence & Justification-012

- Semantic Authority lines 384–404: `unbundle_determinism_rule` requires explicit tier annotations but does not address inactive-tier annotations.
- Lines 371–383: Express Mode groups defined with conditionally active tiers.
- UNBUNDLE_SCAN diagnostic (Semantic Authority lines 1244–1260): reports confidence `high|ambiguous|none` — but no classification for "annotated with inactive tier."
- `active_tiers` constraint (schema lines 19–29): defines which tiers are active.

#### Impact Assessment-012

An author in an Express Mode project without CL active annotates content with `[CL]`. UNBUNDLE_SCAN assigns confidence `high` (the annotation maps unambiguously to one tier), but UNBUNDLE_EXECUTE would attempt to allocate content to a non-existent tier. The behavior is undefined: reject? discard? force CL activation?

#### Resolution-012: Option A - Add Inactive-Tier Fragment Handling Rule

Add a normative statement: "A fragment annotated with a tier not present in `active_tiers` must be classified by UNBUNDLE_SCAN as confidence `ambiguous` with `ambiguity_reason: 'annotated_tier_not_in_active_tiers'`. UNBUNDLE_EXECUTE must reject the fragment unless explicitly deferred."

#### Resolution-012: Option B - Validate Annotations Against active_tiers Pre-Scan

Add a pre-validation step before UNBUNDLE_SCAN that rejects any fragment annotated with a tier not in `active_tiers`.

#### Resolution-012: Option C - Auto-Activate Tier on Valid Annotation

Add a normative rule: if a fragment is annotated with a conditionally active tier not currently in `active_tiers`, UNBUNDLE_EXECUTE may activate the tier (adding it to `active_tiers`) as part of its atomic expansion, provided the resulting `active_tiers` set is one of the four canonical configurations in INV-3.

#### Comparative Analysis-012

Option A uses the existing diagnostic system (confidence + ambiguity_reason) and requires no schema changes. Option B adds a new pre-validation step that duplicates UNBUNDLE_SCAN's classification responsibility. Option C introduces implicit tier activation — a structural mutation outside the operation protocol's explicit design, violating AX-3 determinism (the practitioner didn't request tier activation).

#### Recommendation-012

**Endorsed Option:** `Option A`

Option A is endorsed because it extends the existing UNBUNDLE_SCAN diagnostic vocabulary to cover a real authoring scenario without introducing new operations or implicit structural mutations. The `ambiguity_reason` field already exists in the diagnostic schema; adding a new reason value is a non-breaking extension.

#### Supporting Citations-012

- [YAML Specification - Tags and Types](https://yaml.org/spec/1.2.2/): Supports the principle that annotations should be validated against their applicable context (active tiers) before allocation.

#### Notes-012

No dependency on other issues. The UNBUNDLE_SCAN diagnostic schema should add `annotated_tier_not_in_active_tiers` as a documented `ambiguity_reason` value.

---

### ISSUE-013: Prevent ExtensionRuleId Pattern Overlap with Tier IDs

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Extension rules` | **Spec Section:** `§9 ExtensionRuleId, §5 AtomicInclusionRule`

#### Problem Statement-013

`ExtensionRuleId` (schema lines 909–911) uses pattern `^[A-Z]+-R[0-9]+$`. This pattern matches both Extension rule IDs (e.g., `HRE-R1`, `DGA-R3`) and tier atomic rule IDs (e.g., `XPD-R1`, `SIL-R6`, `GPCL-R10`). The overlap allows an Extension rule to shadow a Core tier rule ID, creating citation ambiguity.

#### Evidence & Justification-013

- Schema lines 909–911: `ExtensionRuleId: { type: string, pattern: "^[A-Z]+-R[0-9]+$" }`.
- Schema lines 897–903: `AtomicInclusionRule.rule_id` uses pattern `^[A-Z]+-R[0-9]+$` (identical).
- Semantic Authority: Extension rules use multi-character prefixes (HRE-R1, DGA-R1, SCE-R1), tier rules use tier abbreviations (XPD-R1, SIL-R1).
- No schema-level constraint prevents `ExtensionRuleId` from accepting `XPD-R1`.

#### Impact Assessment-013

An Extension declaring `rule_id: FCL-R7` passes schema validation. Two different rules with the same ID exist — one in the Core tier definitions, one in the Extension catalog. Validators or reports referencing `FCL-R7` cannot determine which is intended.

#### Resolution-013: Option A - Add Negative Lookahead to ExtensionRuleId Pattern

Modify the pattern to exclude known tier prefixes: `^(?!XPD|SIL|GPCL|FCL|CL|SAL|ICL|CDL|ISL)[A-Z]+-R[0-9]+$`.

#### Resolution-013: Option B - Use Minimum Prefix Length to Separate Namespaces

Change `ExtensionRuleId` pattern to require at least 3 uppercase characters before the hyphen: `^[A-Z]{3,}-R[0-9]+$`. This excludes `CL-R*` (2 chars) while permitting all current Extension prefixes (HRE, DGA, etc.). Note: this would exclude `XPD`, `SIL`, `FCL`, `SAL`, `ICL`, `CDL`, `ISL` (all 3 chars) — those match, so GPCL (4 chars) also matches. The tier IDs `CL` (2 chars) would be excluded, but `XPD`, `SIL`, etc. (3 chars) would still overlap.

#### Resolution-013: Option C - Add Normative Uniqueness Requirement

Keep the pattern unchanged. Add a normative statement: "Extension rule_id prefixes must not collide with any tier abbreviation defined in active_tiers. Uniqueness is enforced by secondary validation, not by the JSON Schema pattern."

#### Comparative Analysis-013

Option A provides the tightest schema-level guarantee using negative lookahead, which is supported in ECMA-262 regex (the regex dialect used by JSON Schema). Option B is simpler but doesn't fully separate namespaces since 3-char tier IDs (XPD, SIL, FCL, SAL, ICL, CDL, ISL) match the `{3,}` constraint. Option C defers to secondary validation, weakening the schema's fail-fast guarantee, but is the most flexible for future tier additions.

#### Recommendation-013

**Endorsed Option:** `Option C`

Option C is endorsed because the tier name set may expand in future versions (v7.x). A negative lookahead hardcodes the current tier list into the machine contract, creating a maintenance obligation to update two locations whenever tiers change. A normative uniqueness requirement + secondary validation is the lighter-weight solution with lower maintenance burden. This parallels ISSUE-014's recommendation for global rule_id uniqueness.

#### Supporting Citations-013

- [ECMA-262 Regular Expressions](https://tc39.es/ecma262/multipage/text-processing.html#sec-regexp-regular-expression-objects): JSON Schema 2020-12 references ECMA-262 regex for pattern validation, confirming negative lookahead is supported but adds regex complexity.

#### Notes-013

Depends on ISSUE-014 (global rule_id uniqueness). If ISSUE-014 is adopted, the uniqueness enforcement for Extension rule IDs becomes a subset of the global uniqueness requirement.

---

### ISSUE-014: Add Global `rule_id` Uniqueness Requirement

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `Tier definitions` | **Spec Section:** `§5, §9`

#### Problem Statement-014

Neither the Machine Contract nor the Semantic Authority declares a global uniqueness constraint on `rule_id` values across tier definitions and extensions. The schema patterns (`^[A-Z]+-R[0-9]+$` for inclusion, `^[A-Z]+-E[0-9]+$` for exclusion) enforce naming convention but not uniqueness. Two different tier definitions could theoretically define a rule with the same ID.

#### Evidence & Justification-014

- Schema lines 897–903: `AtomicInclusionRule.rule_id` pattern `^[A-Z]+-R[0-9]+$`.
- Schema lines 918–924: `AtomicExclusionRule.rule_id` pattern `^[A-Z]+-E[0-9]+$`.
- Schema lines 909–911: `ExtensionRuleId` pattern `^[A-Z]+-R[0-9]+$`.
- No `uniqueItems` or cross-definition uniqueness constraint in the schema.
- VALIDATE output references `rule_id` in violation results — ambiguity if IDs are not globally unique.

#### Impact Assessment-014

A VALIDATE result containing `violated_rules: ["FCL-R7"]` is unambiguous today because naming conventions prevent collisions. However, if a custom extension or future tier reuses a rule_id prefix, the result becomes ambiguous. The absence of normative uniqueness leaves this gap open.

#### Resolution-014: Option A - Add Normative Uniqueness Statement

Add to the Semantic Authority: "All rule_id values across tier_definitions and extension_catalog must be globally unique within a single DDR System specification. Duplicate rule_ids constitute a structural violation detectable by VERIFY."

#### Resolution-014: Option B - Add JSON Schema uniqueItems Constraint

Add `uniqueItems: true` to arrays containing rule objects. Note: JSON Schema `uniqueItems` compares entire objects, not individual properties — it cannot enforce property-level uniqueness across different arrays.

#### Resolution-014: Option C - Enforce via Naming Convention Only

Document that rule_id prefixes must match tier_id or Extension abbreviation, and that uniqueness follows from the naming convention. No normative uniqueness statement needed.

#### Comparative Analysis-014

Option A provides a clear normative guarantee enforceable by secondary validation. Option B is technically non-functional for property-level uniqueness across separate arrays in JSON Schema. Option C relies on naming convention discipline without a normative backstop — fragile for a system that demands AX-3 determinism.

#### Recommendation-014

**Endorsed Option:** `Option A`

Option A is endorsed because JSON Schema cannot enforce cross-array property uniqueness (ruling out Option B). Naming conventions (Option C) are a best-effort measure, not a structural guarantee. A normative statement + VERIFY enforcement provides deterministic uniqueness verification.

#### Supporting Citations-014

- [JSON Schema uniqueItems](https://json-schema.org/understanding-json-schema/reference/array#uniqueItems): Official guidance confirming uniqueItems compares whole objects, not individual fields — insufficient for cross-array property uniqueness.

#### Notes-014

ISSUE-013 depends on this issue. Global rule_id uniqueness subsumes the Extension rule_id collision concern.

---

### ISSUE-015: Fix version_history v1.0 Empty Date Field

**Status:** `OPEN` | **Severity:** `MINOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Version history` | **Spec Section:** `Appendix A version_history`

#### Problem Statement-015

The `version_history` entry for v1.0 (Semantic Authority lines 2093–2096) has `date: ""`. The `VersionHistoryEntry` schema (lines 1312–1322) allows `date` as an optional string but imposes no format or minimum length. An empty date violates the v6.3 philosophy of explicit, complete metadata.

#### Evidence & Justification-015

- Semantic Authority lines 2093–2096: `{version: "1.0", date: "", summary: "Initial DDR System concept..."}`.
- Schema lines 1312–1322: `VersionHistoryEntry` — `date: { type: string }` with no `minLength` or format constraint.
- All other version_history entries have populated dates.

#### Impact Assessment-015

An automated changelog generator iterating `version_history` encounters an entry with no date and must decide whether to display "unknown," skip the entry, or raise an error. The inconsistency creates a minor but unnecessary exception case.

#### Resolution-015: Option A - Add minLength to date and Populate v1.0

Add `minLength: 1` to `VersionHistoryEntry.date`. Populate the v1.0 entry with the earliest known date (e.g., `"2026-02-26"` to match v2.1, or `"unknown"` if truly unavailable).

#### Resolution-015: Option B - Make date Optional with Normative Note

Keep `date` optional. Add a normative note: "Empty date fields indicate unknown historical dates. Tooling should treat empty dates as 'unknown.'"

#### Resolution-015: Option C - Add date to required for VersionHistoryEntry

Add `date` to the `required` array in `VersionHistoryEntry`. All entries must have a non-empty date.

#### Comparative Analysis-015

Option A is the most practical: it closes the schema gap and fixes the single offending entry. Option B codifies the problem rather than fixing it. Option C makes `date` required but without `minLength`, an empty string would still pass — it needs to be combined with `minLength: 1` anyway, making it equivalent to Option A.

#### Recommendation-015

**Endorsed Option:** `Option A`

Option A is endorsed because it fixes both the schema gap (missing `minLength`) and the data gap (empty v1.0 date). A single entry with a placeholder date is preferable to codifying "unknown" as a valid field value.

#### Supporting Citations-015

- [JSON Schema String Constraints](https://json-schema.org/understanding-json-schema/reference/string#length): Official guidance on minLength constraints for string properties.

#### Notes-015

No dependency on other issues. The v1.0 date can be set to match v2.1 (`"2026-02-26"`) or a best-estimate date.

---

### ISSUE-016: Require Topology Fields in TierDefinition

**Status:** `OPEN` | **Severity:** `MINOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Tier definitions` | **Spec Section:** `§5 TierDefinition`

#### Problem Statement-016

The `TierDefinition` schema (lines 814–869) declares `required: [tier_id, label, layer_label, core_question, is_optional, is_terminal_leaf, is_merge_node]` but omits topology-critical fields `parent_relationships` and `child_relationships`. A schema-valid tier definition can exist with no declared topology, making it impossible to validate DAG structure from tier definitions alone.

#### Evidence & Justification-016

- Schema lines 814–822: `TierDefinition.required` omits `parent_relationships` and `child_relationships`.
- Schema lines 848–864: `parent_relationships` and `child_relationships` defined as arrays of `TierRelationship` objects.
- Semantic Authority: every tier definition includes both `parent_relationships` and `child_relationships`.
- INV-2 (line 261): "No tier-skipping: citations must reference the immediately preceding active tier(s)."

#### Impact Assessment-016

A tier definition without `parent_relationships` passes schema validation. INV-2 enforcement relies on these relationships to determine which tiers are "immediately preceding." Without them, INV-2 becomes unverifiable from tier definitions alone, forcing implementers to hardcode tier ordering separately.

#### Resolution-016: Option A - Add to required Array

Add `parent_relationships` and `child_relationships` to `TierDefinition.required`.

#### Resolution-016: Option B - Add minItems Constraint

Keep topology fields optional but add `minItems: 1` when they are present. This allows tier definitions without topology (for informational contexts) but ensures that if topology is declared, at least one relationship exists.

#### Resolution-016: Option C - Add Conditional Requirement Based on is_optional

Require `parent_relationships` and `child_relationships` only when `is_optional: false`. Optional tiers (XPD, CL) may omit topology in certain configurations.

#### Comparative Analysis-016

Option A is the simplest and matches actual usage — every tier definition in the Semantic Authority includes both fields. Option B allows topology-free tier definitions to exist, which undermines the schema's role as a structural authority. Option C adds conditional logic for a scenario (topology-free optional tiers) that doesn't exist in practice.

#### Recommendation-016

**Endorsed Option:** `Option A`

Option A is endorsed because topology relationships are definitionally part of a tier definition. A tier without parent/child relationships is not a tier in the DDR topology. The current Semantic Authority demonstrates 100% population, making this a formalization of existing practice.

#### Supporting Citations-016

- [JSON Schema Required Properties](https://json-schema.org/understanding-json-schema/reference/object#required): Official guidance on declaring required properties.

#### Notes-016

No dependency on other issues. Backward compatible with all existing tier definitions.

---

### ISSUE-017: Define `errata_log` Operational Guidance

**Status:** `OPEN` | **Severity:** `MINOR` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `Errata system` | **Spec Section:** `§1 errata_log`

#### Problem Statement-017

The `errata_log` field (Semantic Authority line 101) is declared as `errata_log: []` with no accompanying documentation of its purpose, entry schema, or operational lifecycle. The `ErrataEntry` schema (schema lines 292–299) defines `date`, `description`, and optional `affected_sections`, but no normative guidance explains when entries should be added, who adds them, or how they relate to `version_history`.

#### Evidence & Justification-017

- Semantic Authority line 101: `errata_log: []`.
- Schema lines 292–299: `ErrataEntry` schema with `required: [date, description]`.
- No normative section defines errata_log purpose or lifecycle.
- `version_history` exists as a separate change tracking mechanism — relationship to errata_log is undefined.

#### Impact Assessment-017

A practitioner discovers a non-breaking factual error in the specification. Should they: add an errata entry? Modify the content and add a version_history entry? Both? The undefined relationship creates editorial ambiguity.

#### Resolution-017: Option A - Add Normative Section with Operational Guidance

Add a normative section to the Semantic Authority: "errata_log records factual corrections, typographical fixes, and clarifications that do not change normative behavior. Each entry must specify the affected sections. Entries that change normative behavior must be documented in version_history instead and trigger a version increment."

#### Resolution-017: Option B - Remove errata_log Entirely

Remove `errata_log` from the specification and schema. All changes, including minor corrections, are tracked through `version_history`.

#### Resolution-017: Option C - Merge errata_log into version_history as Entry Type

Add an `entry_type` field to `VersionHistoryEntry` (e.g., `enum: [release, errata]`). Remove the standalone `errata_log`. All corrections are tracked in a single chronological log.

#### Comparative Analysis-017

Option A preserves the separation between normative changes (version_history) and non-normative corrections (errata_log), which is a standard practice in specification engineering (e.g., W3C errata). Option B simplifies but loses the normative/non-normative distinction. Option C merges the two but adds schema complexity for minimal benefit.

#### Recommendation-017

**Endorsed Option:** `Option A`

Option A is endorsed because the errata_log/version_history separation reflects a real semantic distinction: errata correct errors without changing behavior; version history tracks behavioral changes. This matches established specification engineering practice (W3C, IETF). The field already exists and is schema-valid; it simply needs operational guidance.

#### Supporting Citations-017

- [W3C Errata Management](https://www.w3.org/2003/01/errata): W3C's established practice for managing specification errata separately from versioned specification releases.
- [IETF RFC Errata System](https://www.rfc-editor.org/errata.php): IETF's approach to errata, supporting the principle that non-normative corrections should be tracked separately from normative revisions.

#### Notes-017

No dependency on other issues. ISSUE-007 references errata_log as a potential destination for inline comments — if ISSUE-007 adopts Option B (errata_log placement), this issue's guidance would inform that entry.

---

## DEPENDENCY MAP

> **AGENT INSTRUCTION:** Use this map to determine resolution order.
> Issues with no dependencies can be resolved independently.
> Issues with dependencies should be resolved after their dependencies.

| Issue | Depends On | Depended On By |
| --- | --- | --- |
| ISSUE-001 | — | — |
| ISSUE-002 | — | — |
| ISSUE-003 | — | — |
| ISSUE-004 | ISSUE-006 | — |
| ISSUE-005 | — | — |
| ISSUE-006 | — | ISSUE-004 |
| ISSUE-007 | — | ISSUE-017 (weak) |
| ISSUE-008 | — | — |
| ISSUE-009 | — | — |
| ISSUE-010 | — | — |
| ISSUE-011 | — | — |
| ISSUE-012 | — | — |
| ISSUE-013 | ISSUE-014 | — |
| ISSUE-014 | — | ISSUE-013 |
| ISSUE-015 | — | — |
| ISSUE-016 | — | — |
| ISSUE-017 | — | ISSUE-007 (weak) |

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** Follow this workflow when resolving any issue.

1. Select an `OPEN` issue with no unresolved dependencies.
2. Set status to `IN_REVIEW`.
3. Apply the endorsed resolution to the target files.
4. Validate the target files against the Machine Contract schema.
5. Verify no new contradictions or orphaned rules are introduced.
6. Update the issue status to `RESOLVED` and add a blockquote resolution note.
7. Update the `## ISSUE REGISTRY` table.
8. Update `## DOCUMENT METADATA` counts.

---

## TARGET FILES

> These files form the Single Source of Truth for DDR System v6.3.
> All issue resolutions must be applied to one or both of these files.

- **DDR System v6.3 Machine Contract:** `ddr/ddr_node_schema_v6.3.yaml`
- **DDR System v6.3 Semantic Authority:** `ddr/ddr_system_v6.3.yaml`
