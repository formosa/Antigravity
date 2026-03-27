---
document:
  id:              DDR_v6.1_Issue-013
  title:           "Resolution Report for ISSUE-013: `node_schema_fields` Is Documentation-Only, Not Machine-Enforced"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  resolved:        "2026-03-27"
  status:          "RESOLVED"
  severity:        "MODERATE"
  type:            "DESIGN_INADEQUACY"
---

## Optimized Resolution Strategy for "ISSUE-013"

### Agent Context

```yaml
id:          ISSUE-013
status:      RESOLVED
severity:    MODERATE
type:        DESIGN_INADEQUACY
tier_refs:   ["System-definition files"]
section_ref: "§3.1"
rule_refs:   []
updated:     2026-03-27
resolved:    2026-03-27
```

> **Resolution (2026-03-27):** Option A — Added a deterministic sync validator between `node_schema_fields` and `$defs.DdrNode`.

### 1. Validation Audit of ISSUE-013

An audit of `.agent/assets/proposals/active/v6.1/ddr_system_v6.1.yaml` and `.agent/assets/proposals/active/v6.1/ddr_node_schema.yaml` confirms a maintainability gap.

The system definition includes a documentation-oriented `node_schema_fields` section with field-level semantics, cardinality notes, and compatibility commentary. Separately, the enforceable schema defines `$defs.DdrNode` as the machine contract. There is no schema-level assertion, generated artifact linkage, or synchronization mechanism tying these two representations together. This permits silent drift between what is documented and what is actually validated.

**Findings:**

1. **Dual-source schema metadata exists:** The project maintains parallel representations of node fields (documentation list + enforceable schema) without a binding contract.
2. **Drift risk is structural, not hypothetical:** Because no automated or schema-native synchronization is present, divergence can occur without immediate detection by validators.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-013

The resolution goal is to reduce or eliminate schema/documentation drift while maintaining usability for both human readers and tooling.

#### Option A: Add Deterministic Synchronization Checks in CI

Keep both artifacts but add a project check that compares `node_schema_fields` entries against `$defs.DdrNode` properties and selected metadata expectations. Fail CI when field names diverge, required/optional mismatches appear, or documented fields no longer exist in the enforceable schema. This option preserves current authoring patterns and minimizes immediate format churn. It treats consistency as a verifiable process invariant.

* **Supporting Insights:** This approach is minimally disruptive and aligns with repository constraints that favor targeted, independently resolvable changes. It can be introduced quickly and iterated without schema redesign.
* **Citations:** [JSON Schema best practices overview (official docs)](https://json-schema.org/learn/getting-started-step-by-step), [GitHub Actions workflow validation patterns](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)

#### Option B: Consolidate Field Documentation into `DdrNode` Metadata

Eliminate the parallel `node_schema_fields` list and make `$defs.DdrNode` the single authoritative source by enriching property metadata (`description`, titles, deprecation notes, extension annotations). Generate human-readable reference views from the schema rather than hand-maintaining two independent structures. This removes drift at the source and strengthens toolchain determinism. The tradeoff is migration effort for any existing consumers that parse `node_schema_fields` directly.

* **Supporting Insights:** Single-source-of-truth design lowers long-term entropy and is generally preferred for standards-like artifacts where validation and documentation must stay aligned.
* **Citations:** [JSON Schema annotations (`title`, `description`, `deprecated`)](https://json-schema.org/understanding-json-schema/reference/annotations), [IETF JSON Schema Validation Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

1. **Implementation cost:** Option A is low-cost and operational; Option B is medium-to-high cost due to migration work.
2. **Drift prevention strength:** Option A detects drift after edits; Option B removes the duplicate source and prevents most drift by design.
3. **Backward compatibility:** Option A preserves existing consumers; Option B may require downstream adaptation.
4. **Time-to-value:** Option A can be deployed immediately; Option B delivers stronger long-term architecture once migration completes.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a missing synchronization mechanism between two already-existing documentation surfaces, not a runtime schema failure that requires an immediate artifact redesign. A deterministic check closes the gap quickly while preserving current consumers and authoring habits.

**Option A** is recommended because:

- Delivers immediate protection against divergence with minimal disruption.
- Preserves current artifact structure while introducing measurable consistency guarantees.
- Supports incremental hardening and evidence-based migration planning.
- Keeps the path open for Option B later if/when consumer and tooling impact is acceptable.

### 4. Implementation Note

Implemented as `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.2\validate_node_schema_fields_sync.py`, a deterministic validator that compares `node_schema_fields` in `ddr_system_v6.2.yaml` against `$defs.DdrNode` in `ddr_node_schema_v6.2.yaml` and checks the documented conditional-cardinality metadata. The live artifacts now pass this check, and drifted temporary fixtures fail, giving the issue a concrete machine-enforced guard instead of a documentation-only expectation.
