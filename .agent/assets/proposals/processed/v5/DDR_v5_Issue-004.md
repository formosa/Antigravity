---
document:
  id:              DDR_v5_Issue-004
  title:           "Resolution Report for ISSUE-004: lifecycle Block Not Covered by ddr_node_schema"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v5.0"
  created:         "2026-03-25"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-004"

### Agent Context

```yaml
id:          ISSUE-004
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.8, lifecycle
rule_refs:   [AX-3]
```

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. lifecycle (§3.8)

### 1. Validation Audit of ISSUE-004

An evaluation of `ddr_node_schema.yaml` and `ddr_system_v5.0.yaml` was conducted to investigate the claims of "ISSUE-004: lifecycle Block Not Covered by ddr_node_schema."

The audit confirms the defect. The system file contains a top-level `lifecycle` block detailing status transition state machines. However, `ddr_node_schema.yaml` does not list `lifecycle` as a permitted top-level property and enforces `additionalProperties: false` at the root.

**Findings:**

1. **System Validation Failure:** The machine-parseable lifecycle state machine causes the master system specification file to fail its own schema validation.
2. **Previous Resolution Broken:** The lifecycle block is the resolution artifact for earlier v4.0 issues. Its exclusion from the schema undermines those resolved issues and limits structural automation.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-004

To structurally integrate the authoritative lifecycle machine, two distinct strategies are proposed.

#### Option A: Add lifecycle Property to the Root Schema

Add `lifecycle` as an optional top-level property in `ddr_node_schema.yaml`, alongside structured `$defs` for `StatusTransition`, `ProhibitedTransition`, and `GuardDefinition`.

* **Supporting Insights:** Incorporates all declarative node and core operational semantics into a single, unified authoritative schema.
* **Citations:** OpenAPI Specification v3.1.0 standards for monolithic state machine schemas.

#### Option B: Extract Lifecycle to a Separate Schema File

Create a new `ddr_lifecycle_schema.yaml` that validates only the lifecycle block, referencing both schemas from the system file. This isolates structural node validation from state transition logic.

* **Supporting Insights:** Enforces strict separation of concerns, keeping the node schema strictly focused on data payload validation while sequestering state machine validation rules.
* **Citations:** Separation of Concerns software engineering principles (Dijkstra, 1974).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v5.0 invariants:

1. **Cohesion vs Separation of Concerns:** Option A keeps all definitions together in a single source of truth matrix. Option B isolates state machine validation from node structural validation, enforcing modularity.
2. **Schema Complexity:** Option A bloats the primary schema. Option B introduces multi-schema orchestration complexities across the toolchain.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A offers the most pragmatically integrated solution for a unified schema model.

**Option A** is recommended because:

* **Tooling Simplicity:** It directly addresses the gap without introducing multi-schema file resolution complexity.
* **Completeness:** It natively enables validation of all aspects of the DDR system file simultaneously.
* **Precedent:** Other operational directives already reside in the central node schema.