---
document:
  id:              DDR_v5_Issue-002
  title:           "Resolution Report for ISSUE-002: Schema Missing derivation_mode Field on ParentCitation"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v5.0"
  created:         "2026-03-25"
  status:          "RESOLVED"
  severity:        "CRITICAL"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-002"

### Agent Context

```yaml
id:          ISSUE-002
status:      RESOLVED
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.1 (node_schema_fields), §3.2, §3.7, ParentCitation def
rule_refs:   [CIT-R2, CIT-R6, AX-3]
```

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §3.1, §3.2, §3.7

### 1. Validation Audit of ISSUE-002

An evaluation of `ddr_node_schema.yaml` and `ddr_system_v5.0.yaml` was conducted to investigate the claims of "ISSUE-002: Schema Missing derivation_mode Field on ParentCitation."

The audit confirms the schema defect. In `ddr_node_schema.yaml`'s `ParentCitation` definition, only `id` and `edge_type` are declared with `additionalProperties: false`. Conversely, `ddr_system_v5.0.yaml` specifies `derivation_mode` as an optional field and uses it in 5 canonical DAG nodes.

**Findings:**

1. **Validation Failure:** 5 canonical DAG nodes will fail schema validation. The system file cannot validate against its own schema, breaking the self-validation loop.
2. **CIT-R6 Unenforceable:** The rule requiring derivation_mode for authority linkages cannot be structurally validated, threatening audit precision.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-002

To resolve the schema omission of the derivation_mode field required by the specification, two distinct strategies are proposed.

#### Option A: Add derivation_mode to ParentCitation Schema

Extend the `ParentCitation` definition in `ddr_node_schema.yaml` to include the optional `derivation_mode` field with enum values `semantic` and `traceability`.

* **Supporting Insights:** Aligns the schema with the already documented specification behaviors and preserves the resolution for v4.0 ISSUE-001, restoring audit trail precision seamlessly.
* **Citations:** SOC 2 compliance (Trust Services Criteria) regarding SDLC traceability.

#### Option B: Remove derivation_mode from Specification and Canonical Nodes

Remove all references to `derivation_mode` from the specification and canonical nodes, and revert to the v4.0 ISSUE-001 Option A approach by reintroducing `cites` as a distinct edge type.

* **Supporting Insights:** Keeps the schema structure extremely minimal and removes optional fields in favor of explicit structural graph edges for distinct citation purposes.
* **Citations:** ISO/IEC/IEEE 29148:2018 - Systems and software engineering — Life cycle processes.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v5.0 invariants:

1. **Backwards Compatibility vs Minimalism:** Option A preserves the v4.0 design decisions and is minimally invasive. Option B forces a major structural rollback and breaks backward compatibility.
2. **Rule Enforcement:** Option A makes CIT-R6 enforceable immediately via schema validation. Option B replaces the rule entirely with new edge topologies.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A is the most balanced and non-destructive strategy to reconcile the schema and specification.

**Option A** is recommended because:

* **Preserves Decisions:** It honors the design choice made to resolve v4.0 ISSUE-001 without undoing progress.
* **Fixes Validation:** It allows the system file to validate against its own schema.
* **Low Overhead:** It requires minimal modification to the existing structure.
