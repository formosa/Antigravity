# DDR System v6.1 — Issue Report Review & Audit

## ISSUE-001 — `lifecycle` Required Despite Lean Project-Instance Contract

**Endorsement of Option C: CONFIRMED — with a material implementation clarification.**

The analysis and logic chain are sound. Option C is architecturally superior to A and B. However, the reports repeatedly suggest introducing a *new* discriminator field (`definition_kind`, `document_class`) to drive the `oneOf` split, and that recommendation is suboptimal. A new required discriminator field adds authoring burden to project-instance files and creates a new schema surface that itself can drift. The correct implementation of Option C uses the **already-present structural marker** — `system_metadata` — as the implicit discriminator. The `oneOf` branches would be:

- Profile 1 (system-definition): `system_metadata` present → `lifecycle` required
- Profile 2 (project-instance): `system_metadata` absent → `lifecycle` optional

This requires zero new fields, preserves the lean project-instance contract literally, and makes `system_metadata` do double duty as both a metadata carrier and a document-class selector, which is already its de-facto role. Any implementation of Option C that introduces a new discriminator field is less optimized than one that doesn't.

---

## ISSUE-002 — Lifecycle Machine Authority Accepts Undefined States

**Endorsement of Option A: CONFIRMED — with a critical implementation gap.**

The direction is correct. However, the report's treatment of `{prior_status}` is insufficient. It says to "model rollback explicitly through allowed target statuses" without specifying the mechanism. The `{prior_status}` placeholder is a *dynamic* reference — the real rollback target is the node's `prior_status` field at the time of the operation, which is already typed as `enum: [ACTIVE, DEPRECATED, DIRTY]` at schema line 1117. The lifecycle table cannot express this as a static `to` value at all. The correct structural fix is to **extend `StatusTransition` with an alternative field**, e.g.:

```yaml
StatusTransition:
  properties:
    to:
      # omit when rollback; mutually exclusive with to_node_field
    to_node_field:
      type: string
      const: "prior_status"
      description: "Used when the target state is determined by the node's own field value."
```

A `oneOf` between `{to: <StatusEnum>}` and `{to_node_field: "prior_status"}` is the machine-verifiable representation. Without this, any "fix" to the transition table still requires either accepting `{prior_status}` as a literal string (wrong) or omitting the rollback row entirely (information loss).

**A secondary defect the report missed:** The `ProhibitedTransition.to` field (schema line 1050-1052, `type: array, items: type: string`) has the same unconstrained-string problem. The prohibited transitions block at lines 2584–2607 includes `DELETED` as a prohibited target (e.g., `ACTIVE → [DRAFT, ACTIVE, DELETED]`), which is also outside the status enum. The ISSUE-002 fix must cover `ProhibitedTransition.to` symmetrically, not only `StatusTransition.to`.

---

## ISSUE-003 — ParentCitation Permits Forbidden `extends` Edges in `parent_ids`

**Endorsement of Option B: CONFIRMED.**

The coordinated `ParentCitation` split is the correct long-term strategy. One implementation detail the report underspecifies: when `parent_ids.items` becomes a `oneOf`, JSON Schema 2020-12 discriminates variants via field presence. The clean approach is:

- `DerivesCitation`: `required: [id, edge_type]`, `edge_type: const: derives`, `derivation_mode` optional
- `CoreCitation`: `required: [id, edge_type]`, `edge_type: enum: [constrains, implements]`, `derivation_mode` prohibited (`not: required: [derivation_mode]` or simply omit it with `unevaluatedProperties: false`)

Using `edge_type` as the discriminating `const`/`enum` within each branch avoids any need for an explicit `discriminator` field and is idiomatic 2020-12. The report should specify this.

---

## ISSUE-004 — `derivation_mode` Rule Declared but Not Enforced

**Endorsement of Option B: CONFIRMED — with one unaddressed enforcement ceiling.**

The variant split resolves the structural defect. However, **CIT-R6 cannot be fully enforced by schema alone.** CIT-R6 requires that any derives edge used as an "authority linkage" *must* set `derivation_mode: traceability`. The schema can enforce that `derivation_mode` is absent outside derives edges, but it cannot distinguish *why* a particular derives edge exists — that is intent, not structure. The report should explicitly note that CIT-R6 enforcement remains a runtime/review-time obligation even after the schema fix. Leaving this implicit creates a future expectation gap.

**Additionally:** The canonical `ParentCitation` scaffold at system YAML lines 2451–2456 retains `EdgeTypeEnum.EXTENDS` and `derivation_mode: Optional[DerivationModeEnum] = None` universally. The scaffold must be updated as part of the same remediation window. The report acknowledges the scaffold reinforces the defect but does not enumerate the scaffold changes required.

---

## ISSUE-005 — Reserved Extension Annotation Shadow Keys Not Schema-Blocked

**Endorsement of Option A: CONFIRMED — with an implementation precision note.**

The `propertyNames` approach is correct. The optimal implementation in 2020-12 combines both constraints (positive namespace format AND negative reserved-suffix exclusion) as an `allOf` on `propertyNames` rather than relying on a negative lookahead in a single regex, which is not supported in ECMA-262:

```yaml
propertyNames:
  allOf:
    - pattern: "^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$"
    - not:
        pattern: "^[A-Z][A-Z0-9_]+::(content|parent_ids|status|tier|id)$"
```

This is more readable, more maintainable, and avoids validator-specific lookahead support variations.

---

## New Issues of Concern — Requiring Dedicated Issue Reports

### ISSUE-006 (Proposed): `prior_status` Settable on Any Node Regardless of `status`

**Severity: MAJOR | Type: SCHEMA_DEFECT | Section: §3.1, §3.8 | Rule: gc-007**

Schema lines 1116–1126 define `prior_status` as optional with `enum: [ACTIVE, DEPRECATED, DIRTY]` and a prose rule: *"Must not be set on any node that is not in SUPERSEDE_PENDING status."* However, the schema has no conditional guard enforcing this. A node with `status: ACTIVE, prior_status: DIRTY` validates today. Since `prior_status` is the rollback anchor for SUPERSEDE atomicity (gc-007 through gc-009), allowing it to be set arbitrarily on non-SUPERSEDE_PENDING nodes undermines that anchor entirely. The fix is a root-level `if/then` conditional on `DdrNode`: when `status ≠ SUPERSEDE_PENDING`, `prior_status` must be absent or null. This is a `unevaluatedProperties`-level or `dependentSchemas` constraint.

---

### ISSUE-007 (Proposed): `lifecycle` Object Lacks `additionalProperties: false`

**Severity: MODERATE | Type: SCHEMA_DEFECT | Section: §3.8**

Schema lines 401–421 define the `lifecycle` property as `type: object` with `required: [status_transitions]` and explicit `properties`, but there is no `additionalProperties: false`. Every other major object in the schema (e.g., `project`, `system_metadata`, `node_id_format`, `DdrNode`, `ParentCitation`) explicitly closes its property surface. The `lifecycle` omission means arbitrary keys are structurally valid inside the lifecycle block, violating the closed-contract design intent and creating a silent extension surface on the most authority-sensitive section of the schema.

---

### ISSUE-008 (Proposed): `constraint_origin` Not Schema-Restricted to CL-Tier Nodes

**Severity: MODERATE | Type: SCHEMA_DEFECT | Section: §3.1, §5 | Rule: AX-4**

Schema lines 1109–1115 define `constraint_origin: enum: [derived, imposed]` with the description "for CL tier." No conditional guard restricts this field to nodes whose `tier` equals `CL`. A SIL or ICL node with `constraint_origin: imposed` passes schema validation today. This violates the intended semantics and, more critically, violates AX-4 (Universality) by allowing CL-tier-specific semantics to appear on any tier node without detection. The fix mirrors the ISSUE-004 pattern: a `DdrNode`-level conditional requiring `constraint_origin` to be absent when `tier ≠ CL`.

---

### ISSUE-009 (Proposed): `express_mode_group` Not Conditionally Required in Express Mode

**Severity: MODERATE | Type: SCHEMA_DEFECT | Section: §4**

Schema lines 1153–1158 define `express_mode_group` with the description "Required when mode=express." However, there is no schema conditional linking `project.mode = express` to the requirement of `express_mode_group` on each node. An entire express-mode project-instance file can be schema-valid with no `express_mode_group` fields set on any node. Since the UNBUNDLE operation depends on group membership (per the system YAML scaffold), this enforcement gap means the schema cannot catch files that would cause UNBUNDLE to fail or behave non-deterministically at runtime.

---

### ISSUE-010 (Proposed): Lifecycle Guard References Are Not Validated Against `guard_definitions`

**Severity: MODERATE | Type: SCHEMA_DEFECT | Section: §3.8**

`StatusTransition.guards` is defined as `type: array, items: type: string` (schema line 1036–1038) with no constraint linking guard ID strings to the `guard_definitions` array. A transition referencing `gc-999` or a misspelled `gc-07` would pass schema validation even if that guard is not defined. Since guards encode the safety preconditions for lifecycle transitions (gc-001 through gc-009), an unresolvable guard reference is a silent atomicity gap. The fix requires either a custom `$defs/GuardRef` type constrained to the defined guard ID set (which requires knowing the set at schema-authoring time, appropriate for a versioned spec), or a pattern constraint enforcing at minimum `^gc-[0-9]{3}$` matching the established three-digit padding convention.

---

## Summary Table

| Issue | Recommended Strategy | Endorsement | Action |
|---|---|---|---|
| ISSUE-001 | Option C | ✅ Confirmed | Clarify: use `system_metadata` as discriminator, not a new field |
| ISSUE-002 | Option A | ✅ Confirmed | Extend: add `to_node_field` for rollback; fix `ProhibitedTransition.to` |
| ISSUE-003 | Option B | ✅ Confirmed | Specify: discriminate via `edge_type: const` in each variant branch |
| ISSUE-004 | Option B | ✅ Confirmed | Note: CIT-R6 traceability enforcement remains runtime-only; update scaffold |
| ISSUE-005 | Option A | ✅ Confirmed | Specify: use `allOf + not` on `propertyNames`, not single-regex negative lookahead |
| ISSUE-006 (new) | — | 🆕 Open | `prior_status` settable regardless of node status — MAJOR |
| ISSUE-007 (new) | — | 🆕 Open | `lifecycle` object open to arbitrary keys — MODERATE |
| ISSUE-008 (new) | — | 🆕 Open | `constraint_origin` unguarded outside CL tier — MODERATE |
| ISSUE-009 (new) | — | 🆕 Open | `express_mode_group` not conditionally required in express mode — MODERATE |
| ISSUE-010 (new) | — | 🆕 Open | Guard references not validated against `guard_definitions` — MODERATE |

All five existing recommendations are directionally correct and worth proceeding on. The primary value-adds above are the implementation precision on ISSUE-001 through ISSUE-005 and the five newly surfaced schema enforcement gaps that will need dedicated resolution reports before v6.1 can be declared structurally clean.
