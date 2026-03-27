# DDR System v6.1 Issues Review — Comprehensive Analysis

## Executive Summary

After reviewing the original 11 tracked issues against the v6.1 normative files, I've validated that the tracker's current Option A recommendations are the strongest fit for the demonstrated defects under the repository's `AGENTS.md` heuristics. I also identified **2 validated new issues** requiring dedicated issue reports, plus **1 candidate issue that does not hold after file-level verification**.

---

## Issue-by-Issue Assessment

### **ISSUE-001: `lifecycle` Required Despite Lean Project-Instance Contract**

| Field                  | Assessment                                                                                                                                                                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | CRITICAL ✓                                                                                                                                                                                                                                              |
| **Recommended**        | Option A (Make `lifecycle` Conditional)                                                                                                                                                                                                                 |
| **My Assessment**      | **Option A is optimal here** — The dual-use nature of this schema (certifying both system-definition and project-instance files) demands a discriminator-based approach. Option A preserves backward compatibility while fixing the contract violation. |
| **Optimization Notes** | Consider using `dependentRequired` (Draft 2020-12)  rather than complex `if/then` for cleaner expression: if `system_metadata` is present, require `lifecycle`.                                                                                         |

---

### **ISSUE-002: Lifecycle Machine Authority Accepts Undefined States**

| Field                  | Assessment                                                                                                                                                                                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | CRITICAL ✓                                                                                                                                                                                                                                                                         |
| **Recommended**        | Option A (Constrain to Typed Status References)                                                                                                                                                                                                                                    |
| **My Assessment**      | **Option A is strongly preferred** — The `DELETED` transition target is an operation sink, not a persisted state. Modeling it as a terminal operation rather than a status preserves the minimal state model. However, the `{prior_status}` symbolic token needs careful handling. |
| **Optimization Notes** | Use JSON Schema `enum` with a single special token value like `"__PRIOR_STATUS__"` rather than a string template pattern. This makes the reference explicit and machine-resolvable.                                                                                                |

---

### **ISSUE-003: ParentCitation Permits Forbidden `extends` Edges**

| Field                  | Assessment                                                                                                                                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | MAJOR ✓                                                                                                                                                                                                                               |
| **Recommended**        | Option A (Remove `extends` from ParentCitation)                                                                                                                                                                                       |
| **My Assessment**      | **Option A is preferred** — The validated defect is a single illegal enum member on a schema type used only for `parent_ids`. Removing `extends` restores `CIT-R5` with the smallest correct patch and no new abstraction.            |
| **Optimization Notes** | If extra clarity is desired, add a short description or `$comment` noting that `extends` remains valid only in `extension_annotations` contexts.                                                                              |

---

### **ISSUE-004: `derivation_mode` Rule Is Declared but Not Enforced**

| Field              | Assessment                                                                                                                                                                                                                                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Severity**       | MAJOR ✓                                                                                                                                                                                                                                                                                                                                                            |
| **Recommended**    | Option A (Add Conditional Constraint)                                                                                                                                                                                                                                                                                                                              |
| **My Assessment**  | **Option A is preferred** — The validated defect is a missing conditional on one optional field. An explicit conditional closes the gap directly and can be coordinated with ISSUE-003 on the same schema surface without introducing citation variants.                                                                                                      |
| **Recommendation** | **Retain Option A** — Use `if/then` or equivalent `allOf` logic to permit `derivation_mode` only on `derives` edges.                                                                                                                                                                                                                                |

---

### **ISSUE-005: Reserved Extension Annotation Shadow Keys Not Schema-Blocked**

| Field                  | Assessment                                                                                                                                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | MODERATE ✓                                                                                                                                                                                                                         |
| **Recommended**        | Option A (Explicitly Block Reserved Suffixes)                                                                                                                                                                                      |
| **My Assessment**      | **Option A is correct** — Use `propertyNames` plus a `not`-based reserved-suffix check to reject keys whose annotation segment is `content`, `parent_ids`, `status`, `tier`, or `id`. This preserves the namespacing model while enforcing the safety rule. |
| **Optimization Notes** | Prefer a portable two-part constraint: keep the existing positive namespace pattern and add a second `propertyNames` rule that blocks the reserved suffix set.                                                                                                                                      |

---

### **ISSUE-006: `prior_status` Can Be Set Outside `SUPERSEDE_PENDING`**

| Field              | Assessment                                                                                                                                                                                                                                                                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**       | MAJOR ✓                                                                                                                                                                                                                                                                                                                                         |
| **Recommended**    | Option A (Gate by Node Status)                                                                                                                                                                                                                                                                                                                  |
| **My Assessment**  | **Option A is preferred** — `prior_status` is transient rollback metadata scoped to a single lifecycle state. A status-gated conditional restores the contract without broadening node taxonomy.                                                                                                                                                           |
| **Recommendation** | **Retain Option A** — Permit `prior_status` only when `status == SUPERSEDE_PENDING` and require its absence otherwise.                                                                                                                                                                                                                                |

---

### **ISSUE-007: `lifecycle` Object Accepts Arbitrary Keys**

| Field                  | Assessment                                                                                                                                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | MODERATE ✓                                                                                                                                                                                                  |
| **Recommended**        | Option A (Close with `additionalProperties: false`)                                                                                                                                                         |
| **My Assessment**      | **Option A is correct and sufficient** — The lifecycle block is machine-authoritative; extensibility here is dangerous. The pattern of closed major objects is already established elsewhere in the schema. |
| **Optimization Notes** | Ensure this applies recursively to nested objects within `lifecycle` (transitions, guards, etc.).                                                                                                           |

---

### **ISSUE-008: `constraint_origin` Is Not Restricted to CL Nodes**

| Field              | Assessment                                                                                                                                                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**       | MODERATE ✓                                                                                                                                                                                                                                                                      |
| **Recommended**    | Option A (Prohibit unless `tier == CL`)                                                                                                                                                                                                                                         |
| **My Assessment**  | **Option A is preferred** — The validated defect is a CL-only field leaking across tiers, not proof that tier-specific variants are required. A tier gate repairs the documented contract directly.                                                                                                                                                     |
| **Recommendation** | **Retain Option A** — Allow `constraint_origin` only when `tier == CL`.                                                                                                                                                                                                                                                                            |

---

### **ISSUE-009: `express_mode_group` Is Not Required in Express Mode**

| Field                  | Assessment                                                                                                                                                                        |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | MODERATE ✓                                                                                                                                                                        |
| **Recommended**        | Option A (Require when `project.mode == express`)                                                                                                                                 |
| **My Assessment**      | **Option A is correct** — Use root-level `if/then` conditional: if `project.mode == "express"`, then require `express_mode_group` on all nodes. This is the minimal surgical fix. |
| **Optimization Notes** | Consider using `dependentSchemas` (Draft 2020-12)  for cleaner expression of this cross-object dependency.                                                                        |

---

### **ISSUE-010: Lifecycle Guard References Accept Undefined Guard IDs**

| Field                  | Assessment                                                                                                                                                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | MODERATE ✓                                                                                                                                                                                                            |
| **Recommended**        | Option A (Constrain to Versioned Guard Set)                                                                                                                                                                           |
| **My Assessment**      | **Option A is correct** — The guard set is versioned and closed. Enumerating `gc-001` through `gc-009` as a strict enum provides the strongest contract. Option B's lexical pattern would still allow phantom guards. |
| **Optimization Notes** | Define a reusable `$defs/GuardId` type with the exact enumeration, then reference it from both `GuardDefinition.id` and `StatusTransition.guards`.                                                                    |

---

### **ISSUE-011: Node ID Prefix Is Not Bound to Declared Tier**

| Field              | Assessment                                                                                                                                                                                                                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**       | CRITICAL ✓                                                                                                                                                                                                                                                                                                     |
| **Recommended**    | Option A (Bind `id` pattern to `tier`)                                                                                                                                                                                                                                                                         |
| **My Assessment**  | **Option A is preferred** — The validated defect is a missing cross-field invariant between `id` and `tier`. Binding the regex by tier closes it directly while preserving the current node shape and compatibility profile.                                                                                                                            |
| **Recommendation** | **Retain Option A** — Add tier-aware `id` constraints and keep the current `DdrNode` contract.                                                                                                                                                                                                                                                   |

---

## New Issues Identified

After comprehensive analysis and file-level validation, I identified **2 additional issues** that should be tracked, plus one candidate that should be rejected:

---

### **NEW ISSUE-012: `parent_ids` Empty Array Default Allows Orphaned Non-Root Nodes**

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All` | **Spec Section:** `§3.1, §3.7`

**Validation Verdict:** ✅ Confirmed against schema and spec files.

#### Problem Statement-012

The `DdrNode.parent_ids` field has `default: []`, which allows non-root nodes to validate with an empty parent array. While the description states "Empty only for root nodes," the schema does not enforce this constraint. This creates a structural loophole where orphaned nodes (violating AX-1) can pass validation.

#### Evidence & Justification-012

- `ddr_node_schema.yaml` lines 1139-1146 define `parent_ids` with `default: []`, while no `minItems` or root-aware conditional is present.
- `ddr_system_v6.1.yaml` lines 271-272 define `INV-5`: "All non-root nodes must carry at least one parent_id citation."
- `ddr_system_v6.1.yaml` lines 312-313 define `CIT-R1`: "Every non-root node must have ≥1 parent_id."
- `ddr_system_v6.1.yaml` lines 116-121 define `AX-1` traceability: every non-root node must cite at least one parent via a typed edge.
- A direct `jsonschema` validation probe accepted a node with `tier: SAL`, `id: SAL-9.9`, and `parent_ids: []`.

#### Impact Assessment-012

Orphaned non-root nodes can exist in structurally valid documents while violating the foundational traceability axiom. Downstream tooling cannot distinguish between a valid root node (XPD/SIL with empty parents) and an invalid orphaned node.

#### Resolution-012: Option A — Conditional Minimum Items

Add a conditional constraint to `DdrNode`: if `tier` is not `XPD` (and not `SIL` when XPD is active), then `parent_ids` must have `minItems: 1`. This preserves the root-node exception while closing the orphan loophole.

#### Resolution-012: Option B — Explicit Root Node Typing

Introduce a `is_root_node` boolean or derive root status from context, then use `dependentRequired` to enforce `minItems: 1` on non-root nodes. This makes root status explicit rather than inferred from tier.

#### Notes-012

Adjacent to ISSUE-011 only in the sense that a future variant refactor could absorb it; the defect is independently valid today.

---

### **NEW ISSUE-013: `node_schema_fields` Documentation-Only, Not Machine-Enforced**

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `System-definition files` | **Spec Section:** `§3.1`

**Validation Verdict:** ✅ Confirmed as a maintainability/design gap.

#### Problem Statement-013

The `node_schema_fields` array in the system definition provides human-readable documentation of node properties, but there is no machine-enforced linkage between these field definitions and the actual `DdrNode` schema. The schema and its documentation can drift independently.

#### Evidence & Justification-013

- `ddr_system_v6.1.yaml` lines 169-220 enumerate `node_schema_fields` with properties like `id`, `tier`, `title`, `content`, `parent_ids`, and `status`.
- `ddr_node_schema.yaml` lines 519-538 define the free-form `NodeSchemaField` documentation object, while lines 1072-1202 define the actual `DdrNode` structure.
- No schema constraint ensures that every field in `node_schema_fields` has a corresponding property in `DdrNode`, or vice versa.
- A direct validation probe accepted a mutated `node_schema_fields` entry for an `imaginary_field`, demonstrating that documentation drift is not blocked by the schema.

#### Impact Assessment-013

Documentation drift creates a maintenance hazard where the human-readable specification becomes misleading. Tooling cannot rely on `node_schema_fields` for code generation or validation logic because the contract is not machine-enforced.

#### Resolution-013: Option A — Schema Synchronization Check

Add a CI/CD validation step that compares `node_schema_fields` against the actual `DdrNode` schema properties and fails on mismatch. This is a process solution rather than a schema change.

#### Resolution-013: Option B — Unify Schema and Documentation

Refactor to use JSON Schema's built-in metadata keywords (`title`, `description`, `deprecated`) within the actual `DdrNode` definition, eliminating the parallel `node_schema_fields` array. The schema becomes self-documenting.

#### Notes-013

This is a meta-level issue about the specification's own maintainability.

---

### **CANDIDATE ISSUE-014: Missing `tier_activation_state` Tracking in Project Instances**

**Status:** `REJECTED` | **Severity:** `N/A` | **Type:** `NOT_AN_ISSUE`
**Tiers Affected:** `Project-instance files` | **Spec Section:** `§3.5, INV-3, INV-4`

**Validation Verdict:** ❌ Not confirmed. `active_tiers` already models activation in the current contract.

#### Problem Statement-014

A candidate concern was raised that project-instance files might need a second field to track activation state for optional tiers. The validation question is whether the current contract already encodes that information through `active_tiers`.

#### Evidence & Justification-014

- `ddr_node_schema.yaml` lines 42-50 define `active_tiers` as the "Ordered list of active tier identifiers."
- `ddr_system_v6.1.yaml` lines 17-26 use `active_tiers` to enumerate the active tiers in the authoritative v6.1 system definition.
- `ddr_system_v6.1.yaml` lines 265-270 define `INV-3` and `INV-4` in terms of conditional activation semantics, not a separate activation-state structure.
- The `project` object at `ddr_node_schema.yaml` lines 64-78 has no `activated_tiers` field because activation is already represented by membership in `active_tiers`.
- A project that omits `CL` from `active_tiers` already expresses "CL inactive" in the current contract.

#### Impact Assessment-014

No additional tracker issue is warranted on the current evidence. The remaining implementation challenge is runtime enforcement of topology against `active_tiers`, not absence of an activation-state field in the schema contract.

#### Resolution-014: Option A — Keep the Current Contract

Do not promote this candidate into the tracker. Treat `active_tiers` as the canonical activation signal, and focus future validation work on ensuring runtime topology checks respect it consistently.

#### Resolution-014: Option B — Re-open Only on Contrary Evidence

If a concrete consumer ambiguity is demonstrated even when `active_tiers` is handled correctly, capture that as a new issue with a reproducer showing why membership in `active_tiers` is insufficient.

#### Notes-014

Do not promote this candidate absent evidence that `active_tiers` is insufficient in the current contract.

---

## Cross-Issue Coordination Recommendations

The dependency map in the tracker is accurate. After validation, the most efficient implementation order is to group fixes by shared schema surface while retaining the tracker's current Option A resolutions:

| Priority | Issue Bundle                        | Rationale                                                                 |
| -------- | ----------------------------------- | ------------------------------------------------------------------------- |
| 1        | **ISSUE-003 + ISSUE-004**           | Same `ParentCitation` surface; tighten enum and `derivation_mode` together. |
| 2        | **ISSUE-002 + ISSUE-007 + ISSUE-010** | Same lifecycle authority surface; type transitions, close the object, and constrain guard refs together. |
| 3        | **ISSUE-001 + ISSUE-009**           | Same root-level conditional surface; coordinate project-instance and express-mode requirements. |
| 4        | **ISSUE-006**                       | Follow lifecycle cleanup so `prior_status` gating matches the repaired state model. |
| 5        | **ISSUE-011 + ISSUE-008**           | Same `DdrNode` conditional surface; bind tier/id and restrict the CL-only field. |
| 6        | **ISSUE-005**                       | Independent extension-annotation hardening.                               |
| 7        | **NEW ISSUE-012**                   | Independent root/non-root parent-cardinality repair.                      |
| 8        | **NEW ISSUE-013**                   | Independent documentation/synchronization gap.                            |

---

## Summary of Recommendations

| Issue     | Tracker Recommended   | My Recommendation   | Rationale                            |
| --------- | --------------------- | ------------------- | ------------------------------------ |
| ISSUE-001 | Option A              | **Option A** ✓      | Minimal fix for dual-use schema      |
| ISSUE-002 | Option A              | **Option A** ✓      | Preserve minimal state model         |
| ISSUE-003 | Option A              | **Option A** ✓      | Surgical enum fix                    |
| ISSUE-004 | Option A              | **Option A** ✓      | Exact conditional repair             |
| ISSUE-005 | Option A              | **Option A** ✓      | Portable reserved-suffix blocking    |
| ISSUE-006 | Option A              | **Option A** ✓      | Gate transient rollback metadata     |
| ISSUE-007 | Option A              | **Option A** ✓      | Match existing closed-object pattern |
| ISSUE-008 | Option A              | **Option A** ✓      | Direct tier gate                     |
| ISSUE-009 | Option A              | **Option A** ✓      | Root-level conditional is clean      |
| ISSUE-010 | Option A              | **Option A** ✓      | Closed guard set is correct          |
| ISSUE-011 | Option A              | **Option A** ✓      | Direct cross-field invariant binding |

**Key Theme:** The validated defects are real, but the evidence supports targeted contract-enforcement repairs rather than a mandatory polymorphic refactor. Under `AGENTS.md`, the smallest correct patch that restores correctness, determinism, and explicitness is the preferred resolution for each currently tracked issue.

Validated conclusion: **ISSUE-012** and **ISSUE-013** are genuine gaps that should be tracked. **Candidate ISSUE-014** should not be promoted because current `active_tiers` semantics already encode active/ inactive optional tiers.

---

## Third Party Review

This is a strong file-level validation pass, especially in how it confirms the existing tracker issues and surfaces two genuine additional gaps. Where the analysis overreaches is in treating several localized schema-enforcement defects as proof that DDR v6.1 must immediately move to a polymorphic node model.

The authoritative `AGENTS.md` guidance for this proposal set explicitly prefers the smallest correct patch that preserves determinism, simplicity, explicitness, and backward-compatible stability. On the current evidence, the tracked defects are better understood as missing conditionals and missing cross-field constraints on otherwise coherent existing schema surfaces.

Here is the validated review of the divergences and the newly identified gaps.

### 1. Where the Audit Holds

- **NEW ISSUE-012 (Orphaned Non-Root Nodes):** Confirmed. Non-root parent cardinality is documented in `AX-1`, `INV-5`, and `CIT-R1`, but not enforced by the schema.
- **NEW ISSUE-013 (`node_schema_fields` drift):** Confirmed. The documentation list and the enforceable `DdrNode` schema can drift independently with no machine check.
- **Candidate ISSUE-014:** Correctly rejected after validation. `active_tiers` already names active tiers in the current contract.

### 2. Where the Audit Overreaches

For ISSUE-004, ISSUE-006, ISSUE-008, and ISSUE-011, the validated defects are missing conditionals or cross-field constraints on the existing schema, not demonstrated failures of the entire node model. Option A resolves each defect directly, preserves the current contract surface, and better matches the repository's preference for the smallest correct patch set.

A polymorphic schema may become appropriate in a future version if multiple new constraints accumulate and cannot be expressed cleanly inside the present structure. That threshold is not demonstrated by the current evidence set.

### 3. Strategic Next Step

Proceed with grouped Option A repairs by shared schema surface: `ParentCitation`, `lifecycle`, root conditionals, and `DdrNode` conditionals. That sequence resolves the validated defects end-to-end while preserving backward-compatible stability and minimizing churn.
