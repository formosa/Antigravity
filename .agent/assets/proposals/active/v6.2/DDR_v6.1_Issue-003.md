---
document:
  id:              DDR_v6.1_Issue-003
  title:           "Resolution Report for ISSUE-003: ParentCitation Permits Forbidden `extends` Edges in `parent_ids`"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  resolved:        "2026-03-27"
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
tier_refs:   ["All (schema)"]
section_ref: "§3.7, §8.1"
rule_refs:   [CIT-R5]
updated:     2026-03-27
resolved:    2026-03-27
```

> **Resolution (2026-03-27):** Option A — Restricted `ParentCitation.edge_type` to Core citation edges only.

### 1. Validation Audit of ISSUE-003

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` was conducted to investigate the claims of "ISSUE-003: ParentCitation Permits Forbidden `extends` Edges in `parent_ids`."

The normative rule in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:328-331` states that "Extension extends edges are stored in extension_annotations only - never in parent_ids." The schema description for `extension_annotations` repeats that boundary in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1159-1167`, ending with "Never in parent_ids or content." Yet `ParentCitation.edge_type` still declares `enum: [derives, constrains, implements, extends]` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1185-1193`. A local `jsonschema` validation probe using `parent_ids: [{id: "SIL-1.1", edge_type: "extends"}]` returned `VALID`.

**Findings:**

1. **Rule and Schema Disagree on Allowed Core Edges:** `CIT-R5` forbids `extends` inside `parent_ids`, but the schema still accepts it as a valid `ParentCitation.edge_type`. That means the machine contract is currently broader than the normative citation rules.
2. **The Core/Extension Boundary Can Be Bypassed Structurally:** Because `parent_ids` is the authoritative Core DAG channel, allowing `extends` there lets extension semantics masquerade as Core lineage. Downstream tooling cannot trust the graph shape to distinguish authoritative parentage from read-only extension relationships.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-003

The resolution goal is to make the schema enforce the same Core-versus-Extension boundary that `CIT-R5` already states normatively, while minimizing future citation-model churn.

#### Option A: Remove `extends` from `ParentCitation`

Narrow `ParentCitation.edge_type` to `[derives, constrains, implements]` and leave the broader four-term edge vocabulary documented only where extension semantics are described conceptually. This is the smallest possible schema patch and it directly eliminates the invalid `parent_ids` shape that currently validates. Tooling that consumes `parent_ids` becomes simpler because it no longer has to special-case an impossible edge. The tradeoff is that the global conceptual vocabulary and the Core storage vocabulary remain implicitly separate rather than being modeled as separate types.

* **Supporting Insights:** If the project wants the least disruptive hotfix, removing `extends` from the existing enum is enough to make `CIT-R5` enforceable at the point where the defect occurs. It is a targeted correction, not a structural redesign.
* **Citations:** [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum).

#### Option B: Split Core Citation Types from the Broader Edge Vocabulary

Define a Core-only citation model for `parent_ids` and preserve the broader four-edge vocabulary in a separate type used only where Extension concepts are modeled. The clean 2020-12 shape is a `oneOf` split in which `DerivesCitation` requires `edge_type: const: derives`, while `CoreCitation` requires `edge_type: enum: [constrains, implements]`; `edge_type` itself becomes the effective discriminator, so no extra tag field is needed. If the project also adopts ISSUE-004's citation-variant refactor, this can become a single cohesive `ParentCitation` redesign rather than two overlapping schema edits. This approach is a slightly larger change, but it turns the current implicit distinction into an explicit type boundary that validators and tooling can rely on.

* **Supporting Insights:** The current defect exists because one enum is doing double duty: it mixes "all conceptual edge types in the system" with "edge types legal in `parent_ids`." Splitting those responsibilities and using `edge_type` constraints as the branch selector gives the schema a sharper model of the Core/Extension boundary and pairs naturally with the adjacent ISSUE-004 repair.
* **Citations:** [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum), [JSON Schema boolean combination (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Repair Scope:** Option A is the smallest correct fix because it removes the single illegal enum member from the exact schema surface where the defect occurs. Option B introduces a broader type split to solve a problem that the current evidence does not require to be solved structurally.
2. **Cross-Issue Coordination:** Option A can still be landed in the same `ParentCitation` edit window as ISSUE-004 without forcing a citation-type redesign. Option B bundles both issues into a larger refactor, which raises migration cost even though the validated defects are narrower.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is a single forbidden value on a schema type that exists specifically to model `parent_ids`. Removing `extends` from `ParentCitation.edge_type` restores `CIT-R5` exactly where the contract is currently too permissive, and ISSUE-004 can still be coordinated on the same schema surface without broadening this issue into a citation-variant redesign.

**Option A** is recommended because:

* **Direct Rule Alignment:** It makes the schema enforce `CIT-R5` at the point where the violation currently slips through.
* **Minimal Schema Churn:** Existing validators and consumers keep the same `ParentCitation` shape and only lose an invalid edge value they should never have accepted.
* **Clearer Core Boundary:** `parent_ids` becomes a reliably Core-only citation channel without requiring a broader type split that the current defect evidence does not demand.

### 4. Implementation Note

Resolved in the live `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.2\ddr_node_schema_v6.2.yaml` citation surface by restricting `ParentCitation.edge_type` to `[derives, constrains, implements]`. Post-change validation confirmed that a `parent_ids` entry using `edge_type: extends` is rejected while the canonical system definition remains schema-valid.