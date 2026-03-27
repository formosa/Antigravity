---
document:
  id:              DDR_v6.1_Issue-001
  title:           "Resolution Report for ISSUE-001: `lifecycle` Required Despite Lean Project-Instance Contract"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  resolved:        "2026-03-27"
  status:          "RESOLVED"
  severity:        "CRITICAL"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-001"

### Agent Context

```yaml
id:          ISSUE-001
status:      RESOLVED
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   ["All project-instance files"]
section_ref: "Schema Root"
rule_refs:   []
updated:     2026-03-27
resolved:    2026-03-27
```

> **Resolution (2026-03-27):** Option A — Made `lifecycle` conditional for system-definition files keyed by `system_metadata`.

### 1. Validation Audit of ISSUE-001

An evaluation of `.agent/assets/proposals/active/v6.1/ddr_node_schema.yaml:19-30` and related project-instance validation behavior was conducted to investigate the claims of "ISSUE-001: `lifecycle` Required Despite Lean Project-Instance Contract."

The contradiction is explicit at the schema root. `.agent/assets/proposals/active/v6.1/ddr_node_schema.yaml:19-23` states that all sections beyond `ddr_version`, `active_tiers`, and `nodes` are optional for project-instance files, yet `.agent/assets/proposals/active/v6.1/ddr_node_schema.yaml:26-30` still places `lifecycle` in the root `required` list. The same schema already exposes `system_metadata` as a system-definition marker at `.agent/assets/proposals/active/v6.1/ddr_node_schema.yaml:90-92`. A local validation probe against a lean project-instance document failed with `'lifecycle' is a required property`, confirming that the machine contract rejects the minimum shape the prose describes.

**Findings:**

1. **Root Contract Contradiction:** The schema's descriptive guidance and its authoritative `required` assertion disagree at the same root surface. Any producer that follows the published lean project-instance guidance will still emit a document the schema rejects.
2. **Project-Instance Lean Mode Is Not Actually Available:** This is not merely a documentation gap. Until the requirement is reconciled, every project-instance author must either add unnecessary lifecycle metadata or accept validation failure.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

The resolution goal is to restore a single truthful root contract for DDR v6.1 so lean project instances and machine validation describe the same admissible shape.

#### Option A: Make `lifecycle` Conditional by `system_metadata`

Remove `lifecycle` from the unconditional root `required` list and reintroduce it through a root-level conditional keyed to the existing `system_metadata` marker. Under this model, system-definition files still require lifecycle authority, while lean project-instance files do not. This preserves the dual-profile design already implied by the schema without inventing a new discriminator field.

* **Supporting Insights:** The schema already distinguishes system-definition files from project-instance files informally. Reusing `system_metadata` turns that informal distinction into an enforceable rule with minimal blast radius.
* **Citations:** [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals)

#### Option B: Require `lifecycle` in Every DDR File

Keep `lifecycle` universally required and rewrite the surrounding contract text so project-instance files are explicitly documented as carrying embedded lifecycle metadata. This avoids conditional logic at the schema root and gives tooling one uniform top-level shape. The tradeoff is that it abandons the published lean project-instance design goal rather than repairing it.

* **Supporting Insights:** This strategy simplifies the validator but pushes complexity into every project-instance artifact. It resolves the contradiction by redefining the contract around the existing defect.
* **Citations:** [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema: A Media Type for Describing JSON Documents](https://json-schema.org/draft/2020-12/draft-bhutton-json-schema-00)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Contract Fidelity:** Option A makes the machine contract match the published lean project-instance promise. Option B resolves the mismatch by changing the promise instead.
2. **Implementation Blast Radius:** Option A localizes the change to the root requirement logic. Option B forces every project-instance producer and every related example to adopt heavier documents.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The defect is a contradiction between the schema's own description and its own required-field assertion. Reusing the existing system-definition marker repairs that contradiction at the exact place it occurs without broadening every downstream artifact.

**Option A** is recommended because:

* **Exact Repair:** It makes the validator enforce the already-published dual-profile contract instead of rewriting the contract around the bug.
* **Low Migration Cost:** System-definition files keep mandatory lifecycle authority while lean project instances stop carrying unnecessary metadata.
* **Future Flexibility:** It resolves the present defect without adding a new root discriminator or a larger schema split.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml` by removing `lifecycle` from the unconditional root `required` list and reintroducing it through a root conditional keyed to `system_metadata`. Resolution was validated by confirming that a lean project-instance document without `lifecycle` now passes while `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml` still validates as a system-definition file.
