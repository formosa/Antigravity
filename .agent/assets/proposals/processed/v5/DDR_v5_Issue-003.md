---
document:
  id:              DDR_v5_Issue-003
  title:           "Resolution Report for ISSUE-003: CL node_schema Property Not Permitted by TierDefinition Schema"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v5.0"
  created:         "2026-03-25"
  status:          "RESOLVED"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-003"

### Agent Context

```yaml
id:          ISSUE-003
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [CL]
section_ref: §5 (Tier 4 CL)
rule_refs:   [CL-R9, CL-R9-imposed]
```

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §5 Tier 4

### 1. Validation Audit of ISSUE-003

An evaluation of `ddr_node_schema.yaml` and `ddr_system_v5.0.yaml` was conducted to investigate the claims of "ISSUE-003: CL node_schema Property Not Permitted by TierDefinition Schema."

The audit confirms the schema defect. The system file's CL tier declares `node_schema.constraint_origin`, but `ddr_node_schema.yaml`'s `TierDefinition` does not permit `node_schema`, causing the system file to fail its own schema.

**Findings:**

1. **Schema Rejection:** Tooling validating the system file against the schema will report a false violation on the CL tier definition.
2. **Verification Gap:** `constraint_origin` cannot be validated as part of the tier definition, breaking the determinism of CL node validation logic.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-003

To resolve the unrecognized property in the CL tier definition, two distinct strategies are proposed.

#### Option A: Add node_schema Property to TierDefinition

Extend the `TierDefinition` schema to include an optional `node_schema` property, allowing tiers to define additional fields like `constraint_origin`. Also add `constraint_origin` as an optional property on `DdrNode` itself.

* **Supporting Insights:** Directly supports the CL tier's need for custom properties and aligns the schema with current specification usage without undermining existing requirements.
* **Citations:** JSON Schema Specification Context Metadata implementations.

#### Option B: Encode constraint_origin as a CL Atomic Inclusion Rule Instead

Remove the `node_schema` block from the CL tier and encode the requirement as an atomic inclusion rule (`CL-R11`) enforced as a structural pattern match on the content header.

* **Supporting Insights:** Keeps the `TierDefinition` schema simpler by moving runtime enforcement from a schema-level field to a content-level convention, avoiding schema bloat for a single tier's needs.
* **Citations:** No authoritative external reference identified for this specific claim.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v5.0 invariants:

1. **Determinism vs Schema Simplicity:** Option A provides strictly deterministic schema-enforced validation. Option B simplifies the schema but relies on content rules.
2. **Blast Radius:** Option A alters the core TierDefinition schema, affecting all potential tier definitions. Option B alters only the CL tier content.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A is the preferred approach because it preserves rule enforcement mechanics.

**Option A** is recommended because:

* **Rule Dependencies:** `constraint_origin` is referenced by rules as a machine-evaluable branching condition.
* **Strict Evaluation:** Making it a content convention (Option B) weakens the deterministic enforcement required by v5.0.
* **Extensibility:** It paves the way for future tier definitions to specify custom properties cleanly.
