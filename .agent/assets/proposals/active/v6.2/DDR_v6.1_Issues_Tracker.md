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
| [ISSUE-011](#issue-011-node-id-prefix-is-not-bound-to-declared-tier) | `CRITICAL` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | Node ID prefix is not bound to declared tier |
| [ISSUE-003](#issue-003-parentcitation-permits-forbidden-extends-edges-in-parent_ids) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | ParentCitation permits forbidden `extends` edges in `parent_ids` |
| [ISSUE-004](#issue-004-derivation_mode-rule-is-declared-but-not-enforced) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | `derivation_mode` rule is declared but not enforced |
| [ISSUE-006](#issue-006-prior_status-can-be-set-outside-supersede_pending) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | `prior_status` can be set outside `SUPERSEDE_PENDING` |
| [ISSUE-012](#issue-012-parent_ids-empty-array-default-allows-orphaned-non-root-nodes) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | All (schema) | `parent_ids` empty array default allows orphaned non-root nodes |
| [ISSUE-005](#issue-005-reserved-extension-annotation-shadow-keys-are-not-schema-blocked) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | All Extensions (schema) | Reserved extension annotation shadow keys are not schema-blocked |
| [ISSUE-013](#issue-013-node_schema_fields-is-documentation-only-not-machine-enforced) | `MODERATE` | `DESIGN_INADEQUACY` | `OPEN` | System-definition files | `node_schema_fields` is documentation-only, not machine-enforced |
| [ISSUE-007](#issue-007-lifecycle-object-accepts-arbitrary-keys) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | All lifecycle blocks | `lifecycle` object accepts arbitrary keys |
| [ISSUE-008](#issue-008-constraint_origin-is-not-restricted-to-cl-nodes) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | Non-CL nodes (schema) | `constraint_origin` is not restricted to CL nodes |
| [ISSUE-009](#issue-009-express_mode_group-is-not-required-in-express-mode) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | Express-mode project instances | `express_mode_group` is not required in express mode |
| [ISSUE-010](#issue-010-lifecycle-guard-references-accept-undefined-guard-ids) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | All lifecycle definitions | Lifecycle guard references accept undefined guard IDs |

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

### ISSUE-006: `prior_status` Can Be Set Outside `SUPERSEDE_PENDING`

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All (schema)` | **Spec Section:** `§3.1, §3.8`

#### Problem Statement-006

The schema defines `prior_status` and documents that it "must not be set on any node that is not in SUPERSEDE_PENDING status," but it does not actually enforce that condition. As a result, settled nodes can carry rollback metadata even when no supersede operation is in progress.

#### Evidence & Justification-006

- `ddr_node_schema.yaml` lines 1116-1126 define `prior_status` as optional with enum `[ACTIVE, DEPRECATED, DIRTY]` and state that it must not be set outside `SUPERSEDE_PENDING`.
- `ddr_system_v6.1.yaml` lines 199-208 repeat the same semantic rule in the system definition.
- The `DdrNode` schema block at `ddr_node_schema.yaml` lines 1072-1202 contains no `if/then`, `oneOf`, or equivalent status-gated conditional around `prior_status`.
- A direct `jsonschema` validation probe accepted a node with `status: ACTIVE` and `prior_status: DIRTY`.

#### Impact Assessment-006

The rollback anchor for `SUPERSEDE` can appear on nodes that are not actually in the transient supersede state. That weakens `gc-007` through `gc-009`, makes rollback metadata less trustworthy, and allows tools to misinterpret stale or fabricated `prior_status` values as live supersede context.

#### Resolution-006: Option A — Gate `prior_status` by Node Status

Add a `DdrNode`-level conditional that allows `prior_status` only when `status == SUPERSEDE_PENDING` and otherwise requires the field to be absent. This is the narrowest schema repair and directly encodes the prose rule already stated in both the schema and the system definition. The condition can be expressed with `if`/`then`/`else` or an equivalent `oneOf` arrangement. It preserves the existing node shape while finally making the rollback-anchor rule machine-enforceable.

#### Resolution-006: Option B — Split Transient and Settled Node Variants

Refactor `DdrNode` into explicit lifecycle-state variants, with a dedicated `SupersedePendingNode` variant that carries `prior_status` and a settled-node variant that omits it entirely. This is a broader type-system change than Option A, but it makes transient rollback state a structural property rather than a conditional footnote. It also creates a clearer place to attach any future supersede-only fields without stretching the base node definition. The tradeoff is higher refactor cost across any tooling that currently assumes a single node shape.

#### Notes-006

This issue is tightly coupled to ISSUE-002 because rollback semantics depend on `prior_status` being both valid and appropriately scoped. Resolving both together yields a more trustworthy supersede state machine.

---

### ISSUE-007: `lifecycle` Object Accepts Arbitrary Keys

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All lifecycle blocks` | **Spec Section:** `Schema Root, §3.8`

#### Problem Statement-007

The root `lifecycle` object requires `status_transitions` and enumerates the known lifecycle sections, but it is not closed with `additionalProperties: false`. This leaves the lifecycle authority surface open to arbitrary undeclared keys.

#### Evidence & Justification-007

- `ddr_node_schema.yaml` lines 401-421 define `lifecycle` as an object with `required: [status_transitions]` and explicit `properties` for `status_transitions`, `prohibited_transitions`, and `guard_definitions`.
- Unlike nearby major objects such as the root schema (`line 31`), `project` (`line 67`), `system_metadata` (`line 93`), `DdrNode` (`line 1087`), and `ParentCitation` (`line 1179`), the `lifecycle` block contains no `additionalProperties: false`.
- A direct `jsonschema` validation probe accepted `lifecycle: {status_transitions: [], rogue_key: true}`.

#### Impact Assessment-007

The most authority-sensitive block in the schema can silently accumulate unreviewed extension keys that validators will not reject. That undermines the otherwise closed-contract design of the document and makes lifecycle behavior easier to fragment across tools.

#### Resolution-007: Option A — Close the Existing `lifecycle` Object

Add `additionalProperties: false` to the current `lifecycle` object definition. This is the smallest and clearest fix because it matches the pattern already used across the rest of the schema's major object surfaces. It preserves the current structure exactly while preventing undeclared lifecycle fields from being treated as valid contract data. If future lifecycle expansion is needed, new keys can be added intentionally through versioned schema edits.

#### Resolution-007: Option B — Close the Core Surface but Add an Explicit Lifecycle Extension Channel

Refactor `lifecycle` so the core object is closed, but if extensibility is intentionally desired, add a clearly named subordinate extension bag such as `extension_annotations` or `vendor_extensions` with its own namespacing rules. This keeps the normative lifecycle contract strict while still allowing controlled out-of-band metadata. It is broader than Option A because it introduces a new contract surface and naming policy. The benefit is that any extensibility becomes explicit instead of leaking through accidental openness.

#### Notes-007

This issue complements ISSUE-001 and ISSUE-002: if `lifecycle` remains a core authority block, its surface should be both present where appropriate and closed to undeclared keys.

---

### ISSUE-008: `constraint_origin` Is Not Restricted to CL Nodes

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Non-CL nodes (schema)` | **Spec Section:** `§3.1, §5`

#### Problem Statement-008

The schema defines `constraint_origin` with the description "for CL tier," but it does not restrict the field to nodes whose `tier` is `CL`. Non-CL nodes can therefore carry CL-specific semantics without structural rejection.

#### Evidence & Justification-008

- `ddr_node_schema.yaml` lines 1109-1115 define `constraint_origin` as enum `[derived, imposed]` and describe it as "for CL tier."
- `ddr_system_v6.1.yaml` lines 743-753 define `constraint_origin` inside the CL tier schema and explain its CL-specific meaning.
- The `DdrNode` schema block at `ddr_node_schema.yaml` lines 1072-1202 contains no conditional tying `constraint_origin` to `tier == CL`.
- A direct `jsonschema` validation probe accepted a `SIL` node carrying `constraint_origin: imposed`.

#### Impact Assessment-008

Tier-specific semantics can bleed into unrelated node types while still passing schema validation. That weakens tier discipline, makes `constraint_origin` less trustworthy as a CL-only signal, and creates room for tooling to infer false constraint semantics from non-CL nodes.

#### Resolution-008: Option A — Prohibit `constraint_origin` Unless `tier == CL`

Add a `DdrNode`-level conditional that permits `constraint_origin` only when the node's tier is `CL` and otherwise requires it to be absent. This is the narrowest schema fix and directly aligns the machine contract with the current field description. It preserves the single-node schema while making the tier restriction enforceable. The change is low blast radius because the field is already documented as CL-specific.

#### Resolution-008: Option B — Introduce Tier-Specific Node Variants

Refactor `DdrNode` into tier-aware schema variants, with a dedicated CL node variant that includes `constraint_origin` and non-CL variants that do not. This is a broader type redesign, but it makes tier-specific fields structurally explicit and creates a cleaner foundation for any future tier-only properties. The tradeoff is more schema volume and a larger update surface for generators and typed consumers. The benefit is stronger alignment between the type system and the tier model the spec already describes.

#### Notes-008

This issue is conceptually independent of ISSUE-004, but both expose places where tier- or role-specific semantics are currently only documented rather than structurally enforced.

---

### ISSUE-009: `express_mode_group` Is Not Required in Express Mode

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Express-mode project instances` | **Spec Section:** `§4`

#### Problem Statement-009

The schema documents `express_mode_group` as "Required when mode=express," but it does not actually require that field when the project is authored in express mode. Express-mode files can therefore validate without the per-node grouping metadata that UNBUNDLE depends on.

#### Evidence & Justification-009

- `ddr_node_schema.yaml` lines 75-78 define `project.mode` as `full | express`.
- `ddr_node_schema.yaml` lines 1153-1158 define `express_mode_group` and say it is "Required when mode=express."
- `ddr_system_v6.1.yaml` lines 360-390 define Express Mode groups and describe deterministic UNBUNDLE behavior in terms of those groups.
- The schema contains no root-level conditional that, when `project.mode == express`, requires each node item to include `express_mode_group`.
- A direct `jsonschema` validation probe accepted a document with `project.mode: express` and nodes lacking `express_mode_group`.

#### Impact Assessment-009

Express-mode project instances can pass validation while omitting the grouping metadata needed for deterministic UNBUNDLE behavior. That shifts a foundational express-mode invariant out of the schema and into late runtime failure or ambiguous tool behavior.

#### Resolution-009: Option A — Require `express_mode_group` When `project.mode == express`

Add a root-level conditional so that when `project.mode` equals `express`, the node-item schema requires `express_mode_group` on every node. This is the smallest repair because it preserves the current document shape and simply makes the existing prose rule enforceable. It keeps full-mode documents lean while hardening the express-mode contract. The change is also directly aligned with how the schema already describes the field.

#### Resolution-009: Option B — Split Full-Mode and Express-Mode Root Profiles

Refactor the root into explicit full-mode and express-mode document profiles, with the express profile requiring nodes to carry `express_mode_group` and the full profile omitting that obligation. This is a larger design change than Option A, but it gives mode-specific requirements a clearer structural home and can pair naturally with any broader document-profile work from ISSUE-001. The downside is added root complexity and a larger migration surface. The upside is that mode becomes a first-class contract boundary instead of a trigger for scattered conditional rules.

#### Notes-009

This issue shares architectural themes with ISSUE-001 because both concern root-level document profiles whose requirements currently differ in prose more clearly than they do in the machine contract.

---

### ISSUE-010: Lifecycle Guard References Accept Undefined Guard IDs

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All lifecycle definitions` | **Spec Section:** `§3.8`

#### Problem Statement-010

Lifecycle transitions can cite guard IDs that are not actually declared in `guard_definitions`, and the schema does not reject them. This leaves lifecycle preconditions vulnerable to silent typos or nonexistent references.

#### Evidence & Justification-010

- `ddr_node_schema.yaml` lines 1035-1038 define `StatusTransition.guards` as an array of unconstrained strings.
- `ddr_node_schema.yaml` lines 1056-1068 define `GuardDefinition.id` with the pattern `^gc-[0-9]+$`, but that typing is not reused by `StatusTransition.guards`.
- `ddr_system_v6.1.yaml` lines 2623-2660 enumerate the concrete guard IDs `gc-001` through `gc-009` used by the current lifecycle authority.
- A direct `jsonschema` validation probe accepted a transition with `guards: ['gc-999']`.

#### Impact Assessment-010

Lifecycle transitions can reference missing or misspelled guard IDs and still validate structurally. That weakens the integrity of the lifecycle safety model because tooling cannot rely on the schema to catch broken precondition references before runtime or review.

#### Resolution-010: Option A — Constrain Guard References to the Versioned Guard Set

Define a reusable guard-reference type for `StatusTransition.guards` that matches the actual lifecycle authority of v6.1, ideally by enumerating the declared guard IDs `gc-001` through `gc-009` or by reusing a single authoritative guard-ID definition. This is the strongest contract because the allowed reference set is versioned and closed just like the guard definitions themselves. It lets validators reject misspellings and phantom guards immediately. The tradeoff is that schema updates are required when the versioned guard set changes.

#### Resolution-010: Option B — Enforce a Lexical Guard-ID Pattern as a Minimum Floor

If the project does not want to close the reference set to exact IDs, at minimum constrain `StatusTransition.guards` to the established lexical format, such as `^gc-[0-9]{3}$`. This is weaker than exact-set validation because `gc-999` would still be structurally valid, but it at least blocks malformed identifiers like `gc-07` or `guard-seven`. It is a modest improvement with low implementation cost. The tradeoff is that real referential integrity remains partly outside the schema.

#### Notes-010

This issue is adjacent to ISSUE-002 because both concern the integrity of the machine-authoritative lifecycle block. If lifecycle transitions are meant to be trusted as normative data, both their endpoints and their guard references need stronger typing.

---

### ISSUE-011: Node ID Prefix Is Not Bound to Declared Tier

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All (schema)` | **Spec Section:** `§3.1, §3.6`

#### Problem Statement-011

The schema validates `id` and `tier` independently, but it does not enforce that the tier prefix embedded in `id` matches the declared `tier` enum value. A node can therefore be structurally valid with `tier: FCL` and `id: SAL-5.1`, producing a semantically contradictory identity.

#### Evidence & Justification-011

- `ddr_node_schema.yaml` lines 1089-1098 define `id` with the broad pattern `^(XPD-0\\.[0-9]+|[A-Z]{2,5}-[0-9]+\\.[0-9]+)$` and `tier` as a separate enum, but no conditional ties the two together.
- The enclosing `DdrNode` schema at `ddr_node_schema.yaml` lines 1079-1202 contains no `if/then`, `allOf`, `oneOf`, or tier-specific variant that constrains the `id` prefix by `tier`.
- `ddr_system_v6.1.yaml` lines 2363-2366 describe the node contract and parent edge IDs with the `TIER-N.M` format, reinforcing that the identifier prefix is intended to be semantically meaningful rather than decorative.
- A direct Draft 2020-12 validation probe accepted an otherwise valid node with `tier: FCL` and `id: SAL-5.1`.

#### Impact Assessment-011

Tier-aware tooling cannot safely trust the node identifier as a routing signal if schema-valid documents may embed mismatched prefixes. Visualization, traversal, and rule-resolution logic can disagree about whether a node belongs to `SAL` or `FCL`, creating inconsistent behavior from a single structurally valid artifact.

#### Resolution-011: Option A — Bind `id` Pattern to `tier`

Keep the current single `DdrNode` shape, but add tier-aware schema constraints so each `tier` value activates the corresponding `id` regex. This can be implemented with `if/then` branches or a compact `allOf` map that enforces `^SIL-[0-9]+\\.[0-9]+$` for `tier: SIL`, `^FCL-[0-9]+\\.[0-9]+$` for `tier: FCL`, and so on, while preserving the special `XPD-0.N` rule. This is the smallest repair because it closes the integrity gap without changing the rest of the node contract.

#### Resolution-011: Option B — Introduce Tier-Specific Node Variants

Refactor `DdrNode` into explicit tier-specific variants so each variant fixes both `tier` and the corresponding `id` pattern at the type level. This is a broader redesign, but it yields stronger typed consumers and can absorb other tier-specific fields such as the `constraint_origin` leak tracked in ISSUE-008. The tradeoff is a larger schema and a wider migration surface for generators, validators, and downstream models.

#### Notes-011

This issue is closely related to ISSUE-008. If the project adopts tier-specific node variants to solve CL-only field leakage, the same refactor can also make prefix-to-tier alignment structurally exact.

---


---

### ISSUE-012: `parent_ids` Empty Array Default Allows Orphaned Non-Root Nodes

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All (schema)` | **Spec Section:** `§3.1, §3.5, §3.7`

#### Problem Statement-012

The `DdrNode.parent_ids` array is documented as empty only for root nodes, but the schema sets `default: []` and does not enforce a minimum cardinality for non-root nodes. This allows orphaned non-root nodes to validate even though both axioms and citation rules require parent linkage.

#### Evidence & Justification-012

- `ddr_node_schema.yaml` describes `parent_ids` as empty only for root nodes and requiring `≥1` for non-root nodes, but no `minItems` or root-aware conditional is present.
- `ddr_system_v6.1.yaml` defines `INV-5` and `CIT-R1` with the same non-root parent requirement.
- The current `ParentCitation` contract is applied only when entries exist; therefore an empty `parent_ids` array bypasses citation-level structural checks entirely.

#### Impact Assessment-012

Schema-valid documents can violate core traceability guarantees by admitting orphaned non-root nodes. This weakens deterministic DAG validation and forces runtime tools to compensate for a contract gap that should be blocked at schema level.

#### Resolution-012: Option A — Enforce Non-Root Parent Cardinality with Root-Aware Conditionals

Add an explicit root-aware conditional to `DdrNode` that requires `parent_ids` to have `minItems: 1` for all non-root nodes. Preserve current root semantics: XPD root nodes may remain empty when XPD is active, and SIL root nodes may remain empty only when XPD is inactive. This directly aligns machine validation with `INV-5` and `CIT-R1` without redesigning node identity.

#### Resolution-012: Option B — Introduce Explicit Root Node Variant(s)

Split node typing to make root status structural (for example, `RootNode` vs `NonRootNode`, or tier-specific variants that encode root behavior). In this model, root variants allow empty `parent_ids`, while non-root variants require at least one citation. This yields clearer typing and error messages but introduces broader schema refactor cost.

#### Notes-012

This issue is adjacent to ISSUE-011 because tier-specific variants could absorb root/non-root cardinality as part of a broader structural model.

---

### ISSUE-013: `node_schema_fields` Is Documentation-Only, Not Machine-Enforced

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `System-definition files` | **Spec Section:** `§3.1`

#### Problem Statement-013

The system definition publishes `node_schema_fields` as a canonical list of node properties, but no machine constraint links this list to the actual `$defs.DdrNode` schema. As a result, schema and documentation can drift independently while still validating.

#### Evidence & Justification-013

- `ddr_system_v6.1.yaml` includes a rich `node_schema_fields` section describing node properties and semantics.
- `ddr_node_schema.yaml` separately defines the enforceable `DdrNode` contract.
- No synchronization rule, validation hook, or schema-level assertion ensures that field names or semantics remain aligned between these artifacts.

#### Impact Assessment-013

Specification consumers may rely on stale or divergent documentation metadata for generation, linting, or governance workflows. Over time, this increases maintenance risk and can produce tooling behavior that conflicts with the true schema contract.

#### Resolution-013: Option A — Add Automated Synchronization Validation

Introduce a deterministic CI check that compares `node_schema_fields` entries against the actual `DdrNode` properties and fails on drift. This preserves current document structure while creating a machine-enforced consistency guard. It is process-oriented, minimally invasive, and independently deployable.

#### Resolution-013: Option B — Consolidate Documentation into the Enforceable Schema

Retire the parallel `node_schema_fields` list and encode authoritative field documentation directly inside `DdrNode` metadata (`title`, `description`, deprecation tags, and related annotations). This reduces duplication and drift risk at the source, but requires migration for any tools currently consuming `node_schema_fields`.

#### Notes-013

This issue is independent of runtime DAG correctness and focuses on long-term specification maintainability.

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
| ISSUE-006 | ISSUE-002 | Rollback semantics are only trustworthy if `prior_status` is both correctly typed in the lifecycle machine and absent outside `SUPERSEDE_PENDING`. |
| ISSUE-007 | ISSUE-002 | If the lifecycle block remains normative authority, its property surface should be closed while transition semantics are being repaired. |
| ISSUE-009 | ISSUE-001 | A future root-profile split is a natural place to encode express-mode-only requirements such as mandatory `express_mode_group`. |
| ISSUE-010 | ISSUE-002 | Lifecycle integrity depends on both valid state targets and valid guard references inside the same authority block. |
| ISSUE-011 | ISSUE-008 | A tier-specific node-variant refactor would allow both CL-only field scoping and ID-prefix enforcement to be solved in one coordinated schema redesign. |
| ISSUE-012 | ISSUE-011 | If tier-specific variants are adopted, root/non-root parent cardinality can be encoded structurally within those variants. |
| ISSUE-013 | (none) | Documentation/synchronization concern; can be resolved independently through process checks or schema-doc consolidation. |

---

*DDR System v6.1 Issues Tracker — IT-1.0*
*13 issues identified | 0 resolved | Last updated: 2026-03-27*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*
