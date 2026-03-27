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

The contradiction is explicit inside `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:19-23`, where the root description states that "All sections beyond ddr_version, active_tiers, and nodes are optional, enabling lean project-instance files while permitting comprehensive system-definition files." The same file immediately declares a root `required` list at `:26-30` containing `ddr_version`, `active_tiers`, `nodes`, and `lifecycle`. A local `jsonschema` validation probe using a seven-tier `active_tiers` list plus only `ddr_version`, `active_tiers`, and `nodes` failed with `'lifecycle' is a required property`, confirming that the machine contract rejects the minimum project-instance shape the description advertises.

**Findings:**

1. **Root Contract Contradiction:** The schema description and the schema assertion disagree at the same document root. Any consumer that follows the published "lean project-instance" guidance will still fail validation because the authoritative contract is the `required` array, not the prose summary.
2. **Lean Project Instances Are Currently Impossible:** This is not a downstream lifecycle-quality issue; it is a top-level admissibility defect. Until the root requirement is reconciled, every project-instance producer must either embed unnecessary lifecycle metadata or generate files that the schema itself rejects.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

The resolution goal is to restore a single truthful root contract for DDR v6.1 so that project-instance generation and schema validation describe the same admissible document shape.

#### Option A: Make `lifecycle` Conditional by Document Class

Remove `lifecycle` from the unconditional root `required` list and re-introduce it through a root-level conditional that applies only to system-definition files. The cleanest trigger is an explicit discriminator such as `definition_kind`, but an existing structural marker such as `system_metadata` can also work if the project wants to avoid adding a new root field. This keeps `lifecycle` mandatory where the DDR system definition is the authoritative source of lifecycle semantics while preserving the advertised lean project-instance contract. It also limits the change to the schema surface instead of forcing a project-wide artifact rewrite.

* **Supporting Insights:** The root description already treats system-definition files and project-instance files as distinct document classes inside one schema. A conditional requirement expresses that existing design directly and keeps the machine-readable contract aligned with the published "lean file" intent.
* **Citations:** [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals).

#### Option B: Normalize on a Universally Required `lifecycle` Block

Keep `lifecycle` universally required and rewrite the surrounding contract text so every DDR file, including project instances, explicitly embeds lifecycle metadata. To reduce authoring friction, the project could publish a canonical minimal lifecycle stub for project-instance producers, but the contract would still become heavier than the current description claims. This option avoids conditional logic at the schema root and gives every validator a single uniform top-level shape. Its tradeoff is that it abandons the current "lean project-instance" design objective rather than preserving it.

* **Supporting Insights:** A single unconditional root shape is simpler to explain to tooling authors, but that simplicity is purchased by expanding every project-instance artifact. The change therefore shifts complexity from the schema to the documents that the schema certifies.
* **Citations:** [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema: A Media Type for Describing JSON Documents](https://json-schema.org/draft/2020-12/draft-bhutton-json-schema-00).

#### Option C: Define Explicit Root Document Profiles with Shared Base Definitions

Refactor the schema root into explicit document profiles, using a shared base plus `oneOf`-selected root contracts for `project-instance` and `system-definition` artifacts. Under this approach, a small discriminator such as `document_class` or `definition_kind` becomes the authoritative selector, `lifecycle` is required only for the `system-definition` profile, and the lean project-instance profile retains `ddr_version`, `active_tiers`, and `nodes` as its minimum contract. This resolves ISSUE-001 more cleanly than a single conditional because it makes the dual-role schema architecture explicit instead of inferred from optional structural markers. It also creates a durable foundation for future profile-specific rules without repeatedly stretching the root contract with ad hoc conditionals.

* **Supporting Insights:** The schema description already states that one file certifies two distinct document classes. Promoting that distinction into named root profiles converts an implicit design assumption into a machine-verifiable contract, which is the most robust way to prevent future contradictions of the same kind.
* **Citations:** [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema conditional validation (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference (`required`)](https://json-schema.org/understanding-json-schema/reference/object).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Contract Preservation:** Option A preserves the documented dual-role schema design by letting lean project instances remain lean, while Option B resolves the contradiction by changing the contract to match the current stricter validator. Option C preserves the dual-role design more completely by making the two document classes explicit rather than merely conditionally inferred.
2. **Implementation Blast Radius:** Option A introduces conditional root logic but leaves existing project-instance authoring expectations intact. Option B keeps the schema root simpler, but it pushes a larger migration burden onto every project-instance producer and companion documentation artifact. Option C requires a more deliberate schema refactor, yet it concentrates that complexity in one root redesign rather than in repeated future exceptions.
3. **Long-Term Schema Stability:** Option A fixes the immediate contradiction, but it still leaves document-class identity partially implicit and therefore easier to drift again. Option C hardens the schema architecture by giving validators and generators a first-class document-profile model that can absorb future per-class requirements cleanly.

#### Endorsement and Contextual Justification

The maximally optimized solution is **Option C (Recommended Strategy)**.

DDR v6.1 already describes two document classes; the deeper defect is that the root assertion layer does not model that distinction as a first-class concept. A simple conditional repair would resolve the immediate contradiction, but an explicit profile split is stronger because it aligns the root contract with the schema's own published architecture and reduces future drift risk.

**Option C** is recommended because:

* **Architectural Explicitness:** It turns the schema's existing two-class design into an explicit machine contract instead of relying on conditional inference from optional fields.
* **Future-Proof Profile Evolution:** It creates a clean place to attach additional system-definition-only or project-instance-only requirements without repeating the same root ambiguity.
* **Preserved Lean-Instance Semantics:** Lifecycle authority remains mandatory for the authoritative system definition while project instances can continue to inherit that authority rather than redundantly restating it.
* **Higher Drift Resistance:** Validators, generators, and human readers all gain the same clear root model, which lowers the chance that future edits recreate cross-profile contradictions.

### 4. GPT-5.4 Adjudication

GPT-5.4 does **not** endorse the prior Recommended Strategy (Option A) as the maximally optimized solution. Option A is a valid near-term repair, but it under-specifies the root document-class boundary and leaves the schema vulnerable to renewed cross-profile drift.

GPT-5.4 endorses **Option C** as the maximally optimized strategy because it resolves the immediate `lifecycle` contradiction and repairs the deeper modeling flaw at the same time: DDR v6.1 is a dual-profile schema, and the root contract should say so explicitly.
