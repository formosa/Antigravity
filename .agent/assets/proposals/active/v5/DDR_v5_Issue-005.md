---
document:
  id:              DDR_v5_Issue-005
  title:           "Resolution Report for ISSUE-005: are_scoring_profiles Not Covered by ddr_node_schema"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v5.0"
  created:         "2026-03-25"
  status:          "OPEN"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-005"

### Agent Context

```yaml
id:          ISSUE-005
status:      OPEN
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [ARE_E5]
section_ref: §9 (E5 ARE), are_scoring_profiles
rule_refs:   [ARE-R2, ARE-R5]
```

### 1. Validation Audit of ISSUE-005

An evaluation of `ddr_node_schema.yaml` and `ddr_system_v5.0.yaml` was conducted to investigate the claims of "ISSUE-005: are_scoring_profiles Not Covered by ddr_node_schema."

The audit confirms the schema gap. The `ddr_system_v5.0.yaml` contains `are_scoring_profiles`. Still, `ddr_node_schema.yaml` does not list it, which will trigger schema rejection under `additionalProperties: false`.

**Findings:**

1. **Schema Rejection:** Schema validation rejects the system file wholesale due to the unrecognized `are_scoring_profiles` property, halting toolchain ingestion.
2. **ARE-R5 Broken:** Compliance mechanisms cannot be structurally validated because the scoring profiles referenced are not schema-representable.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-005

To define normative scoring rubrics for ARE deployments correctly within the structural schema, two distinct strategies are proposed.

#### Option A: Add are_scoring_profiles to Root Schema

Add `are_scoring_profiles` as an optional top-level property with structured definitions for scoring profiles, signals, bands, and custom profile requirements in the core `ddr_node_schema.yaml`.

* **Supporting Insights:** It represents a simple, lower-risk fix, resolving the immediate validation error gracefully without dramatically reshaping the specification hierarchy.
* **Citations:** No authoritative external reference identified for this specific claim.

#### Option B: Subsume Under extension_system or extension_catalog

Move `are_scoring_profiles` to be a child of the existing `extension_system` block (or the E5 entry in `extension_catalog`), nesting it under the extension schema definition instead.

* **Supporting Insights:** Scoring profiles are an ARE-specific concern and logically belong under the extension system's schema umbrella instead of indiscriminately cluttering the root tree.
* **Citations:** Domain-Driven Design (Evans, 2003) regarding Context Boundaries and bounded model scopes.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v5.0 invariants:

1. **Structural Coherence:** Option B ensures higher architectural cohesion by grouping ARE extensions closely together contextually. Option A splits ARE data across root fields and extension entries.
2. **Complexity:** Option A is slightly simpler to implement but pollutes the top level of the master schema unnecessarily over time.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

Option B safely enhances the structural taxonomy of the DDR specifications to accommodate complex modular extensions.

**Option B** is recommended because:

* **Logical Grouping:** It keeps the extension models functionally grouped, ensuring modular isolation.
* **Limits Root Entries:** It contains the spread of custom root-level objects, ensuring a tight core schema.
* **Future Proofing:** It establishes a clear, scalable pattern for other complex extension parameters moving forward.
