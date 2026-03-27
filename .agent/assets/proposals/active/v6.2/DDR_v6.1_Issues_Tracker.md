# DDR System v6.1 — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the DDR System v6.1. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read only the `` blocks within each issue before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              ITR-827b62af-ae8f-4764-85cd-ec7061fd9669
  title:           "DDR System v6.1 — Issues Tracker"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  last_modified:   "2026-03-27"
  author:          "Anthony Formosa"
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT      # Specification makes contradictory claims
    - DESIGN_INADEQUACY     # Feature is absent, under-specified, or insufficient
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

| ID | Severity | Type | Status | Tiers Affected | Title |
| --- | --- | --- | --- | --- | --- |
| [ISSUE-001](#issue-001-lifecycle-required-despite-lean-project-instance-contract) | `CRITICAL` | `SCHEMA_DEFECT` | `OPEN` | All project-instance files | `lifecycle` required despite lean project-instance contract |
| [ISSUE-002](#issue-002-lifecycle-machine-authority-accepts-undefined-states) | `CRITICAL` | `LIFECYCLE_GAP` | `OPEN` | All | Lifecycle machine authority accepts undefined states |
| [ISSUE-003](#issue-003-parentcitation-permits-forbidden-extends-edges-in-parent_ids) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | ParentCitation permits forbidden `extends` edges in `parent_ids` |
| [ISSUE-004](#issue-004-derivation_mode-rule-is-declared-but-not-enforced) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | `derivation_mode` rule is declared but not enforced |
| [ISSUE-005](#issue-005-reserved-extension-annotation-shadow-keys-are-not-schema-blocked) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | All Extensions (schema) | Reserved extension annotation shadow keys are not schema-blocked |

---

## ISSUES

---

### ISSUE-001: `lifecycle` Required Despite Lean Project-Instance Contract

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All project-instance files` | **Spec Section:** `Schema Root`

#### Problem Statement-001
The schema advertises support for lean project-instance files whose minimum shape is `ddr_version`, `active_tiers`, and `nodes`, but the root `required` list also mandates `lifecycle`. This makes the published project-instance contract false in the machine-readable schema itself.

#### Evidence & Justification-001
- `ddr_node_schema.yaml` lines 19-23 state that all sections beyond `ddr_version`, `active_tiers`, and `nodes` are optional for project-instance files.
- `ddr_node_schema.yaml` lines 26-30 require `lifecycle` at the root.
- A direct `jsonschema_rs` probe using only `ddr_version`, `active_tiers`, and `nodes` fails with: `"lifecycle" is a required property`.
- Because the schema is presented as certifying both system-definition files and project-instance files, the root contract must not contradict its own published minimum shape.

#### Impact Assessment-001
Lean project-instance DDR files cannot validate even when they satisfy the documented minimum contract. Any client that trusts the schema description will generate invalid files, and every project instance is forced to embed specification-level lifecycle metadata that should be optional or inherited.

#### Resolution-001: Option A — Make `lifecycle` Conditional
Remove `lifecycle` from the unconditional root `required` list and require it only for system-definition files. Implement that distinction with a root-level conditional such as presence of `system_metadata`, `tier_definitions`, or another explicit `definition_kind` discriminator. This preserves the published lean project-instance contract while keeping lifecycle mandatory for the authoritative system spec.

#### Resolution-001: Option B — Rewrite the Project-Instance Contract
Keep `lifecycle` universally required, but revise the schema header, top-level description, and any related contract text so project-instance files are explicitly documented as requiring an embedded lifecycle block. This avoids schema changes, but it expands every project-instance artifact and weakens the original "lean file" design goal.

#### Notes-001
This issue is independent of lifecycle-state correctness. Even if ISSUE-002 is resolved, the root project-instance contract remains contradictory until this required-field mismatch is addressed.

---

### ISSUE-002: Lifecycle Machine Authority Accepts Undefined States

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `All` | **Spec Section:** `§3.1, §3.8`

#### Problem Statement-002
The machine-authoritative lifecycle block uses transition targets that are not members of the declared node status set, and the schema does not constrain lifecycle transition state names to valid statuses. As written, the lifecycle authority can encode undefined states without structural rejection.

#### Evidence & Justification-002
- `ddr_system_v6.1.yaml` lines 189-198 define valid node statuses as `DRAFT | ACTIVE | DIRTY | DEPRECATED | SUPERSEDED | SUPERSEDE_PENDING`.
- `ddr_node_schema.yaml` lines 1103-1108 define the same `DdrNode.status` enum.
- `ddr_system_v6.1.yaml` lines 2530-2532 and 2575-2578 define transitions to `DELETED`, which is not present in the status enum.
- `ddr_system_v6.1.yaml` lines 2567-2570 use `"{prior_status}"` as another transition target, but `ddr_node_schema.yaml` lines 1024-1054 model transition `from` and `to` as unconstrained strings rather than status references.
- A direct evaluation of the current lifecycle block shows transition targets not in `StatusEnum`: `DELETED` and `{prior_status}`.

#### Impact Assessment-002
`INV-8` cannot actually be machine-validated, because the schema accepts arbitrary lifecycle state names and the current authoritative lifecycle already depends on undefined ones. Tooling cannot tell whether `DELETE` removes a node immediately, transitions it into a terminal persisted status, or both, so lifecycle enforcement can diverge across implementations.

#### Resolution-002: Option A — Constrain Lifecycle to Typed Status References
Introduce typed lifecycle references in the schema: `from` and `to` must resolve to `StatusEnum`, with a narrowly defined symbolic rollback token if needed for `SUPERSEDE_ROLLBACK`. Model `DELETE` as an operation sink that removes a node without pretending it becomes a persisted `DELETED` status. This keeps the runtime state model small and restores machine-verifiable lifecycle closure.

#### Resolution-002: Option B — Formalize `DELETED` as a Real Lifecycle State
Expand the status model to include `DELETED` as an explicit terminal status and define the rollback placeholder as a typed lifecycle construct rather than an untyped string literal. This preserves the existing transition table shape, but it broadens the core status model and requires every status consumer to understand one more persisted state.

#### Notes-002
This issue interacts with ISSUE-001 because the current root schema already forces `lifecycle` into every project-instance file. If lifecycle remains globally required, its state machine must be structurally self-consistent.

---

### ISSUE-003: ParentCitation Permits Forbidden `extends` Edges in `parent_ids`

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All (schema)` | **Spec Section:** `§3.7, §8.1`

#### Problem Statement-003
The `ParentCitation` schema allows `edge_type: extends`, even though the citation rules explicitly forbid `extends` edges from appearing in `parent_ids`. This lets Core node parent links encode Extension semantics in the wrong channel.

#### Evidence & Justification-003
- `ddr_system_v6.1.yaml` lines 328-331 define `CIT-R5`: Extension `extends` edges are stored in `extension_annotations` only and never in `parent_ids`.
- `ddr_node_schema.yaml` lines 1159-1167 reinforce that Extension metadata belongs in `extension_annotations`, not in `parent_ids`.
- `ddr_node_schema.yaml` lines 1185-1193 still declare `ParentCitation.edge_type` as `[derives, constrains, implements, extends]`.
- A direct `jsonschema_rs` probe validated a node whose `parent_ids` contained `{id: "SIL-1.1", edge_type: "extends"}`.

#### Impact Assessment-003
Invalid Core DAGs can pass structural validation while violating `CIT-R5`. Downstream tooling cannot trust `parent_ids` to contain only Core derivation, constraint, or implementation edges, and Extension relationships can be smuggled into the authoritative DAG.

#### Resolution-003: Option A — Remove `extends` from ParentCitation
Restrict `ParentCitation.edge_type` to `[derives, constrains, implements]`. Keep `extends` in the global edge vocabulary text for Extension architecture documentation, but do not permit it in `parent_ids`. This is the smallest fix and directly aligns the schema with `CIT-R5`.

#### Resolution-003: Option B — Split Core and Global Edge Enums
Define a Core-only `ParentCitationEdgeType` enum for `parent_ids` and a separate broader edge vocabulary type for explanatory or extension-layer modeling. This is slightly larger than Option A, but it cleanly separates "all conceptual edge types" from "edge types that may appear in Core node citations."

#### Notes-003
This issue shares the same schema surface as ISSUE-004. If `ParentCitation` is refactored, both constraints should be applied in the same patch to avoid repeated churn.

---

### ISSUE-004: `derivation_mode` Rule Is Declared but Not Enforced

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All (schema)` | **Spec Section:** `§3.2, §3.7`

#### Problem Statement-004
The spec states that `derivation_mode` is valid only for `edge_type='derives'`, but the schema does not enforce that conditional rule. As a result, non-derives edges can carry `derivation_mode` and still validate.

#### Evidence & Justification-004
- `ddr_system_v6.1.yaml` lines 315-319 define `CIT-R2` so that `derivation_mode` applies to `derives` edges.
- `ddr_system_v6.1.yaml` lines 332-335 define `CIT-R6`, which depends on the ability to structurally distinguish derives-edge traceability.
- `ddr_node_schema.yaml` lines 1194-1202 state that `derivation_mode` is "Valid only when edge_type is 'derives'."
- The same schema block contains no `if/then`, `oneOf`, or other conditional guard, and a direct `jsonschema_rs` probe validated `{edge_type: "implements", derivation_mode: "traceability"}` inside `parent_ids`.
- `ddr_system_v6.1.yaml` lines 2451-2456 show the canonical scaffold `ParentCitation` dataclass also accepts `derivation_mode` for every edge instance.

#### Impact Assessment-004
Semantically nonsensical citations can pass schema validation, which makes `CIT-R6` only partially enforceable. Tooling may incorrectly treat `implements` or `constrains` edges as if they carried derives-edge lineage semantics, degrading audit precision.

#### Resolution-004: Option A — Add a Conditional Constraint
Keep the current `ParentCitation` shape, but add JSON Schema conditional logic: if `edge_type == "derives"`, `derivation_mode` may be omitted or must be one of `semantic|traceability`; otherwise `derivation_mode` must be absent. This is the smallest change and preserves backward compatibility.

#### Resolution-004: Option B — Split Citation Variants
Replace the current single `ParentCitation` definition with explicit schema variants such as `DerivesCitation` and `NonDerivesCitation`, combined via `oneOf`. This is structurally cleaner and makes the rule self-documenting, but it introduces a broader schema refactor than Option A.

#### Notes-004
This issue is adjacent to ISSUE-003 because both arise from the same `ParentCitation` schema type. A single coordinated edit can fix both invalid edge-type acceptance and invalid `derivation_mode` placement.

---

### ISSUE-005: Reserved Extension Annotation Shadow Keys Are Not Schema-Blocked

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All Extensions (schema)` | **Spec Section:** `§3.1, §8.1`

#### Problem Statement-005
The schema text says that namespaced annotation keys ending in core field names such as `content` or `status` are never valid, but the actual regex permits them. This leaves a documented prohibition unenforced at the machine-contract level.

#### Evidence & Justification-005
- `ddr_node_schema.yaml` lines 1162-1167 say keys named `content`, `parent_ids`, `status`, `tier`, or `id` are never valid in `extension_annotations`.
- `ddr_node_schema.yaml` lines 1168-1171 permit any key matching `^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$`, which allows values such as `HRE::content`.
- A direct `jsonschema_rs` probe validated `extension_annotations: {HRE::content: "shadow"}`.
- Because `extension_annotations` is the sanctioned channel for Extension/Core interaction, its reserved-key guarantees need to be enforceable rather than documentary only.

#### Impact Assessment-005
Extensions can publish namespaced keys that shadow core field names while still passing schema validation. Consumers that flatten, normalize, or partially strip namespaces can mis-handle annotation payloads, and the schema contradicts its own stated safety rule.

#### Resolution-005: Option A — Explicitly Block Reserved Suffixes
Add a `propertyNames` or negative-pattern constraint that rejects keys whose annotation segment after `::` is `content`, `parent_ids`, `status`, `tier`, or `id`. This preserves the existing namespacing model while making the reserved-word rule enforceable.

#### Resolution-005: Option B — Relax the Normative Text
Remove the "never valid" language from the `extension_annotations` description and treat namespacing alone as sufficient separation, with collision handling delegated to extension-specific contracts and tooling. This avoids schema complexity, but it weakens the current AX-6/CIT-R5 safety posture.

#### Notes-005
This issue reinforces the same Core/Extension boundary defended by ISSUE-003. If both are addressed together, the schema can tighten Extension isolation in a single compatibility review.

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue RESOLVED until all steps are confirmed.

```plaintext
1. IDENTIFY issue ID and selected Resolution Option (A or B)
2. DRAFT the specific changes to .agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml and .agent\assets\proposals\active\v6.1\ddr_node_schema.yaml and/or associated schemas
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

| Issue | Depends On | Nature of Dependency |
| --- | --- | --- |
| ISSUE-002 | ISSUE-001 | If `lifecycle` remains globally required, its machine-authoritative state model must be fully self-consistent across both system-definition and project-instance files. |
| ISSUE-004 | ISSUE-003 | Both issues require changes to `ParentCitation`; resolving them together avoids repeated schema churn and inconsistent citation semantics. |
| ISSUE-005 | ISSUE-003 | Both tighten the Core/Extension boundary and should be regression-tested together against existing annotation consumers. |

---

*DDR System v6.1 Issues Tracker — IT-1.0*
*5 issues identified | 0 resolved | Last updated: 2026-03-27*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*
