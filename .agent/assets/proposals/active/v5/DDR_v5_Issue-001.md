---
document:
  id:              DDR_v5_Issue-001
  title:           "Resolution Report for ISSUE-001: Schema Omits SUPERSEDE_PENDING from DdrNode Status Enum"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v5.0"
  created:         "2026-03-25"
  status:          "OPEN"
  severity:        "CRITICAL"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-001"

### Agent Context

```yaml
id:          ISSUE-001
status:      OPEN
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.1 (node_schema_fields), §7 (operations), lifecycle
rule_refs:   [AX-3, INV-6]
```

### 1. Validation Audit of ISSUE-001

An evaluation of `ddr_node_schema.yaml` and `ddr_system_v5.0.yaml` was conducted to investigate the claims of "ISSUE-001: Schema Omits SUPERSEDE_PENDING from DdrNode Status Enum."

The audit confirms the schema defect. In `ddr_node_schema.yaml` (line 753), the `status` enum lists 5 values. However, `ddr_system_v5.0.yaml` §3.1 explicitly defines `SUPERSEDE_PENDING` as a sixth status value.

**Findings:**

1. **Validation Failure:** Any DDR project file capturing a mid-SUPERSEDE snapshot will fail schema validation, since `SUPERSEDE_PENDING` is not a valid enum value. Tooling built from the schema will reject structurally correct in-flight states.
2. **Specification Integrity Violation:** The system file and the schema file contradict each other on a normative structural property, violating the single-source-of-truth principle. The SUPERSEDE operation cannot be deterministically represented and validated.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

To resolve the contradiction between the specification and the schema regarding the SUPERSEDE_PENDING status, two distinct strategies are proposed.

#### Option A: Add SUPERSEDE_PENDING to DdrNode.status Enum

Add `SUPERSEDE_PENDING` to the `DdrNode.status` enum in `ddr_node_schema.yaml`. Update the description to include the SUPERSEDE_PENDING transition semantics already documented in the system file. This is a single-line schema fix that brings the schema into alignment with the specification.

* **Supporting Insights:** This is the simpler fix but implies that serialized files may contain SUPERSEDE_PENDING nodes, which the specification describes as transient.
* **Citations:** IEEE 1471 / ISO/IEC 42010 Systems and software engineering - Architecture description.

#### Option B: Model SUPERSEDE_PENDING as an Operational State Outside the Schema Enum

Retain the 5-value enum and add a separate optional boolean field `supersede_pending` to signal in-flight SUPERSEDE status without extending the core status enum. Update the specification to describe SUPERSEDE_PENDING as a runtime-only operational state that is never persisted to a serialized YAML file.

* **Supporting Insights:** SUPERSEDE_PENDING is transient and should never appear in a persisted file. The schema validates at-rest state, not in-flight state. This approach explicitly distinguishes runtime states from persistable states.
* **Citations:** No authoritative external reference identified for this specific claim.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v5.0 invariants:

1. **Architectural Purity:** Option B distinguishes cleanly between runtime operational state and at-rest serialized state, representing higher architectural purity, whereas Option A blends them.
2. **Implementation Complexity:** Option A requires a trivial one-line addition to the schema. Option B requires adding boolean fields and updating multiple sections of the specification to clarify runtime vs persistent concepts.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A provides the most immediate, deterministic alignment between the schema and the specification.

**Option A** is recommended because:

* **Simplicity:** It requires only a single-element addition to an existing enum.
* **Alignment:** It brings the schema perfectly inline with the states already detailed in the lifecycle specification.
* **Tooling Compatibility:** It immediately fixes the validation false-negatives without requiring complex transient-state awareness in basic validators.
