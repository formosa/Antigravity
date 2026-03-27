---
document:
  id:              DDR_v6.1_Issue-003
  title:           "Resolution Report for ISSUE-003: ParentCitation Permits Forbidden `extends` Edges in `parent_ids`"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  status:          "OPEN"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-003"

### Agent Context

```yaml
id:          ISSUE-003
status:      OPEN
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   ["All (schema)"]
section_ref: "§3.7, §8.1"
rule_refs:   [CIT-R5]
```

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

1. **Repair Scope:** Option A is the fastest direct fix because it edits a single enum in place. Option B changes more schema structure, but it eliminates the conceptual ambiguity that allowed the defect to emerge in the first place.
2. **Cross-Issue Stability:** Option A resolves only the immediate `extends` leak. Option B aligns better with ISSUE-004, where the same `ParentCitation` surface also needs a stronger structural split for `derivation_mode` semantics.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

Although Option B is slightly larger than a one-line enum trim, it uses the already-required `ParentCitation` repair window to separate Core storage semantics from broader edge vocabulary semantics. Implemented as a variant split keyed by `edge_type`, it makes the fix more durable without introducing a redundant discriminator and avoids revisiting the same type again when ISSUE-004 is resolved.

**Option B** is recommended because:

* **Type-System Clarity:** It gives `parent_ids` a Core-only citation contract and lets `edge_type` itself discriminate the legal citation branches instead of relying on prose to explain why one enum member is actually forbidden there.
* **Cross-Issue Efficiency:** It lets ISSUE-003 and ISSUE-004 be resolved in one coordinated schema redesign rather than in two partially overlapping patches.
* **Boundary Hardening:** It makes the Core/Extension separation explicit in the schema itself, which lowers the risk of future regressions that leak extension semantics back into the authoritative DAG.

### 4. GPT-5.4 Endorsement

GPT-5.4 endorses the current Recommended Strategy, **Option B**, as the maximally optimized solution for ISSUE-003.

This endorsement is based on the shape of the defect in DDR v6.1: the problem is not only that `extends` appears in one enum, but that a single `ParentCitation` type is carrying both Core DAG semantics and broader conceptual edge vocabulary. Option B fixes the immediate leak and removes the underlying modeling ambiguity in a way that also aligns with ISSUE-004, which makes it more durable than a one-line enum restriction alone.
