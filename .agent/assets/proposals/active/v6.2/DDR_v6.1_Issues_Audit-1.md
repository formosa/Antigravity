# DDR System v6.1 Issues Review — Comprehensive Analysis

## Executive Summary

After reviewing all 11 issues in the tracker, I've identified that **most recommended solutions are sound but suboptimal**. Several issues warrant **Option B** (broader redesign) over the conservative Option A fixes, particularly where structural debt accumulates. I've also identified **2 validated new issues** requiring dedicated issue reports, plus **1 candidate issue that does not hold after file-level verification**.

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
| **My Assessment**      | **Option A is correct but incomplete** — While removing `extends` from the enum is the minimal fix, this issue reveals a deeper architectural concern: the edge type vocabulary is overloaded.                                        |
| **Optimization Notes** | The schema should explicitly document that `extends` is valid ONLY in `extension_annotations` context. Consider adding a `$comment` or description annotation to the global edge type definition clarifying this channel restriction. |

---

### **ISSUE-004: `derivation_mode` Rule Is Declared but Not Enforced**

| Field              | Assessment                                                                                                                                                                                                                                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Severity**       | MAJOR ✓                                                                                                                                                                                                                                                                                                                                                            |
| **Recommended**    | Option A (Add Conditional Constraint)                                                                                                                                                                                                                                                                                                                              |
| **My Assessment**  | **Option B (Split Citation Variants) is actually superior** — Here's my first major divergence. While Option A is "smaller," it creates a conditional schema that's harder to reason about and maintain. The `oneOf` approach with explicit `DerivesCitation` and `NonDerivesCitation` variants is self-documenting and enables stronger typing in generated code. |
| **Recommendation** | **Adopt Option B** — The refactor cost is justified by improved clarity and the precedent set by ISSUE-011 (tier-specific variants).                                                                                                                                                                                                                               |

---

### **ISSUE-005: Reserved Extension Annotation Shadow Keys Not Schema-Blocked**

| Field                  | Assessment                                                                                                                                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**           | MODERATE ✓                                                                                                                                                                                                                         |
| **Recommended**        | Option A (Explicitly Block Reserved Suffixes)                                                                                                                                                                                      |
| **My Assessment**      | **Option A is correct** — Use `propertyNames` with a negative pattern (regex lookahead/negative match) to reject `.*::(content|parent_ids|status|tier|id)$`. This preserves the namespacing model while enforcing the safety rule. |
| **Optimization Notes** | The regex `^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$` should be updated to: `^[A-Z][A-Z0-9_]+::(?!(content|parent_ids|status|tier|id)$)[a-z][a-z0-9_]+$`                                                                                  |

---

### **ISSUE-006: `prior_status` Can Be Set Outside `SUPERSEDE_PENDING`**

| Field              | Assessment                                                                                                                                                                                                                                                                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Severity**       | MAJOR ✓                                                                                                                                                                                                                                                                                                                                         |
| **Recommended**    | Option A (Gate by Node Status)                                                                                                                                                                                                                                                                                                                  |
| **My Assessment**  | **Option B (Split Node Variants) is superior** — This is my second major divergence. The `SUPERSEDE_PENDING` state carries unique semantics (rollback anchor, transient lifecycle). Making this a distinct structural variant rather than a conditional field creates a cleaner type system and prevents an entire class of state-machine bugs. |
| **Recommendation** | **Adopt Option B** — The `SupersedePendingNode` variant can carry `prior_status` as a required field, while settled nodes simply don't have the field. This eliminates the need for runtime conditional checks.                                                                                                                                 |

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
| **My Assessment**  | **Option B (Tier-Specific Variants) is superior** — Third major divergence. This field is CL-specific by design. If the schema adopts tier-specific node variants (as recommended for ISSUE-011), the CL variant naturally includes this field while other variants exclude it. |
| **Recommendation** | **Coordinate with ISSUE-011** — If tier-specific variants are adopted, this becomes a non-issue. If not, Option A is the fallback.                                                                                                                                              |

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
| **My Assessment**  | **Option B (Tier-Specific Node Variants) is strongly superior** — This is the fourth and most important divergence. The current schema attempts to validate a semantic relationship (ID prefix indicates tier) through regex alone. Tier-specific variants make this relationship structural and self-evident. |
| **Recommendation** | **Adopt Option B** — The variant approach enables: (1) tier-specific ID patterns, (2) tier-specific fields (absorbing ISSUE-008), (3) clearer generated code, (4) better error messages. The refactor cost is high but the architectural clarity is worth it.                                                  |

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

- `ddr_node_schema.yaml` lines 1152-1158 define `parent_ids` with `default: []` and `minItems` is not specified.
- `ddr_system_v6.1.yaml` lines 328-331 define `CIT-R1`: "Every non-root node must have ≥1 parent_id."
- AX-1 (Traceability) states: "Every non-root node must cite at least one parent via a typed edge."
- A direct `jsonschema` validation probe accepted a node with `tier: SIL`, `id: SIL-1.2`, and `parent_ids: []`.

#### Impact Assessment-012

Orphaned non-root nodes can exist in structurally valid documents while violating the foundational traceability axiom. Downstream tooling cannot distinguish between a valid root node (XPD/SIL with empty parents) and an invalid orphaned node.

#### Resolution-012: Option A — Conditional Minimum Items

Add a conditional constraint to `DdrNode`: if `tier` is not `XPD` (and not `SIL` when XPD is active), then `parent_ids` must have `minItems: 1`. This preserves the root-node exception while closing the orphan loophole.

#### Resolution-012: Option B — Explicit Root Node Typing

Introduce a `is_root_node` boolean or derive root status from context, then use `dependentRequired` to enforce `minItems: 1` on non-root nodes. This makes root status explicit rather than inferred from tier.

#### Notes-012

Related to ISSUE-011 (tier-specific variants would naturally resolve this by making root nodes a distinct variant).

---

### **NEW ISSUE-013: `node_schema_fields` Documentation-Only, Not Machine-Enforced**

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `DESIGN_INADEQUACY`
**Tiers Affected:** `System-definition files` | **Spec Section:** `§3.1`

**Validation Verdict:** ✅ Confirmed as a maintainability/design gap.

#### Problem Statement-013

The `node_schema_fields` array in the system definition provides human-readable documentation of node properties, but there is no machine-enforced linkage between these field definitions and the actual `DdrNode` schema. The schema and its documentation can drift independently.

#### Evidence & Justification-013

- `ddr_system_v6.1.yaml` lines 189-208 enumerate `node_schema_fields` with properties like `id`, `tier`, `title`, etc.
- `ddr_node_schema.yaml` lines 1079-1202 define the actual `DdrNode` structure.
- No schema constraint ensures that every field in `node_schema_fields` has a corresponding property in `DdrNode`, or vice versa.
- The `node_schema_fields` entries include metadata (cardinality, semantics, backward_compatibility) that is not machine-verifiable against the actual schema.

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

The schema tracks which tiers are *defined* in `active_tiers`, but project-instance files have no explicit field tracking which optional tiers (XPD, CL) are actually *activated* for the current project. This forces tooling to infer activation from node presence or context, creating ambiguity.

#### Evidence & Justification-014

- `ddr_system_v6.1.yaml` lines 253-255 define `INV-3`: "XPD and CL are conditionally activatable."
- `ddr_system_v6.1.yaml` lines 256-258 define `INV-4`: "When CL is inactive, SAL derives directly from FCL."
- `ddr_node_schema.yaml` lines 19-23 define `active_tiers` as the ordered list of tier identifiers, but this appears to be the *available* tiers, not the *activated* tiers.
- The `project` object (lines 63-79) has no `activated_tiers` or `tier_states` field.
- A project with `active_tiers: [XPD, SIL, ...]` and no XPD nodes could be interpreted as either "XPD active but empty" or "XPD present but inactive."

#### Impact Assessment-014

DAG traversal logic cannot deterministically apply INV-4 (SAL→FCL direct derivation when CL inactive) without knowing CL's activation state. This creates ambiguity in parent edge validation and tier-skip detection.

#### Resolution-014: Option A — Add `tier_activation` Map

Add an optional `tier_activation` object to the `project` metadata with boolean flags for optional tiers (XPD, CL). Default to `true` if present in `active_tiers` and nodes exist, but allow explicit `false` to indicate "present in schema but inactive."

#### Resolution-014: Option B — Infer from Node Presence with Explicit Empty-Tier Marker

Define that tier activation is inferred from node presence, but require an explicit empty-tier marker node (e.g., `XPD-0.0` with status `INACTIVE`) to indicate "tier considered but explicitly skipped." This preserves the lean file principle while making the decision auditable.

#### Notes-014

This issue affects the deterministic application of DAG invariants and should be resolved before tooling assumes ambiguous behavior.

---

## Cross-Issue Coordination Recommendations

The dependency map in the tracker is accurate, but I recommend **re-prioritizing the resolution order**:

| Priority   | Issue                                           | Rationale                                             |
| ---------- | ----------------------------------------------- | ----------------------------------------------------- |
| 1          | **ISSUE-011** (Tier-specific variants)          | Foundation for ISSUE-008 and NEW ISSUE-012            |
| 2          | **ISSUE-008**                                   | Absorbed into ISSUE-011 if variants adopted           |
| 3          | **ISSUE-006**                                   | Absorbed into ISSUE-011 if variants adopted           |
| 4          | **ISSUE-004**                                   | Coordinate with citation variant refactoring          |
| 5          | **ISSUE-003**                                   | Same schema surface as ISSUE-004                      |
| 6          | **ISSUE-001**                                   | Root-level discriminator depends on variant approach  |
| 7          | **ISSUE-009**                                   | Root-level conditional, depends on ISSUE-001 approach |
| 8          | **ISSUE-002, ISSUE-007, ISSUE-010**             | Lifecycle integrity (can proceed in parallel)         |
| 9          | **ISSUE-005**                                   | Extension isolation (independent)                     |
| 10         | **NEW ISSUE-012, NEW ISSUE-013**                 | Newly identified and validated                         |

---

## Summary of Recommendations

| Issue     | Tracker Recommended   | My Recommendation   | Rationale                            |
| --------- | --------------------- | ------------------- | ------------------------------------ |
| ISSUE-001 | Option A              | **Option A** ✓      | Minimal fix for dual-use schema      |
| ISSUE-002 | Option A              | **Option A** ✓      | Preserve minimal state model         |
| ISSUE-003 | Option A              | **Option A** ✓      | Surgical enum fix                    |
| ISSUE-004 | Option A              | **Option B** ⚠️     | Self-documenting variant structure   |
| ISSUE-005 | Option A              | **Option A** ✓      | Regex negative lookahead             |
| ISSUE-006 | Option A              | **Option B** ⚠️     | Transient state as distinct variant  |
| ISSUE-007 | Option A              | **Option A** ✓      | Match existing closed-object pattern |
| ISSUE-008 | Option A              | **Option B** ⚠️     | Coordinate with ISSUE-011            |
| ISSUE-009 | Option A              | **Option A** ✓      | Root-level conditional is clean      |
| ISSUE-010 | Option A              | **Option A** ✓      | Closed guard set is correct          |
| ISSUE-011 | Option A              | **Option B** ⚠️     | Structural alignment of ID→tier      |

**Key Theme:** Issues 004, 006, 008, and 011 all benefit from a **tier-specific node variant** approach. While this represents higher initial refactor cost, it creates a more maintainable, self-documenting schema that prevents entire classes of cross-field validation errors. If the project can absorb this cost, the long-term maintainability gains are substantial.

Validated conclusion: **ISSUE-012** and **ISSUE-013** are genuine gaps that should be tracked. **Candidate ISSUE-014** should not be promoted because current `active_tiers` semantics already encode active/ inactive optional tiers.
