---
document:
  id:              DDR_v6.1_Issue-001
  title:           "Resolution Report for ISSUE-001: `lifecycle` Required Despite Lean Project-Instance Contract"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
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
tier_refs:   ["All project-instance files"]
section_ref: "Schema Root"
rule_refs:   []
```

### 1. Validation Audit of ISSUE-001

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` was conducted to investigate the claims of "ISSUE-001: `lifecycle` Required Despite Lean Project-Instance Contract."

The contradiction is explicit inside `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:19-23`, where the root description states that "All sections beyond ddr_version, active_tiers, and nodes are optional, enabling lean project-instance files while permitting comprehensive system-definition files." The same file immediately declares a root `required` list at `:26-30` containing `ddr_version`, `active_tiers`, `nodes`, and `lifecycle`. The existing root surface already includes a system-definition marker: `system_metadata` is declared at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:90-92` as "System-level metadata for DDR specification definition files." A local `jsonschema` validation probe using a seven-tier `active_tiers` list plus only `ddr_version`, `active_tiers`, and `nodes` failed with `'lifecycle' is a required property`, confirming that the machine contract rejects the minimum project-instance shape the description advertises.

**Findings:**

1. **Root Contract Contradiction:** The schema description and the schema assertion disagree at the same document root. Any consumer that follows the published "lean project-instance" guidance will still fail validation because the authoritative contract is the `required` array, not the prose summary.
2. **Lean Project Instances Are Currently Impossible:** This is not a downstream lifecycle-quality issue; it is a top-level admissibility defect. Until the root requirement is reconciled, every project-instance producer must either embed unnecessary lifecycle metadata or generate files that the schema itself rejects.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

The resolution goal is to restore a single truthful root contract for DDR v6.1 so that project-instance generation and schema validation describe the same admissible document shape.

#### Option A: Make `lifecycle` Conditional by the Existing `system_metadata` Marker

Remove `lifecycle` from the unconditional root `required` list and re-introduce it through a root-level conditional or `oneOf` branch that activates only when `system_metadata` is present. In practice, the system-definition profile becomes "`system_metadata` present and `lifecycle` required," while the lean project-instance profile becomes "`system_metadata` absent and `lifecycle` optional." This keeps `lifecycle` mandatory where the DDR system definition is the authoritative source of lifecycle semantics while preserving the advertised lean project-instance contract. It also avoids adding a new discriminator field such as `definition_kind` or `document_class`, which would create extra authoring burden and a second root contract surface that can drift.

* **Supporting Insights:** The root description already treats system-definition files and project-instance files as distinct document classes inside one schema, and `system_metadata` is already described as specific to specification-definition files. Reusing that existing structural marker is a tighter design than inventing a new discriminator just to recover a distinction the schema already encodes informally.
* **Citations:** [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals).

#### Option B: Normalize on a Universally Required `lifecycle` Block

Keep `lifecycle` universally required and rewrite the surrounding contract text so every DDR file, including project instances, explicitly embeds lifecycle metadata. To reduce authoring friction, the project could publish a canonical minimal lifecycle stub for project-instance producers, but the contract would still become heavier than the current description claims. This option avoids conditional logic at the schema root and gives every validator a single uniform top-level shape. Its tradeoff is that it abandons the current "lean project-instance" design objective rather than preserving it.

* **Supporting Insights:** A single unconditional root shape is simpler to explain to tooling authors, but that simplicity is purchased by expanding every project-instance artifact. The change therefore shifts complexity from the schema to the documents that the schema certifies.
* **Citations:** [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema: A Media Type for Describing JSON Documents](https://json-schema.org/draft/2020-12/draft-bhutton-json-schema-00).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Contract Preservation:** Option A preserves the documented dual-role schema design by letting lean project instances remain lean while still requiring lifecycle authority for system-definition files. Option B resolves the contradiction by rewriting the contract around the stricter current validator and abandoning the published lean-instance promise.
2. **Implementation Blast Radius:** Option A changes only the root validation rule and can still be expressed with an existing-marker conditional or `oneOf` branch keyed off `system_metadata`. Option B pushes migration cost into every project-instance producer, related documentation artifact, and example file.
3. **Future Flexibility:** Option A closes the present defect without adding a new discriminator or wider root redesign, while still leaving room for a later explicit profile split if future evidence shows one is necessary. Option B settles the contradiction by making every file heavier, which is harder to reverse later.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a direct contradiction between the root description and the root `required` list. Reusing the existing `system_metadata` marker to make `lifecycle` conditional repairs that contradiction exactly where it occurs without expanding the contract for every project-instance file.

**Option A** is recommended because:

* **Exact Contract Repair:** It makes the machine contract match the published minimum project-instance shape instead of redefining the shape around the defect.
* **Low Migration Cost:** Existing system-definition files keep mandatory lifecycle authority, while lean project instances stop carrying unnecessary lifecycle data.
* **Reuse of Existing Structure:** The already-declared `system_metadata` marker is enough to distinguish the authoritative system-definition profile without inventing a new discriminator field.
