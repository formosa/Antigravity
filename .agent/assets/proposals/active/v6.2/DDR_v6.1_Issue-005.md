---
document:
  id:              DDR_v6.1_Issue-005
  title:           "Resolution Report for ISSUE-005: Reserved Extension Annotation Shadow Keys Are Not Schema-Blocked"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  status:          "OPEN"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-005"

### Agent Context

```yaml
id:          ISSUE-005
status:      OPEN
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["All Extensions (schema)"]
section_ref: "§3.1, §8.1"
rule_refs:   [AX-6, CIT-R5, EXT-R3]
```

### 1. Validation Audit of ISSUE-005

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` was conducted to investigate the claims of "ISSUE-005: Reserved Extension Annotation Shadow Keys Are Not Schema-Blocked."

The prohibition exists in prose at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1162-1167`, which states that keys named `content`, `parent_ids`, `status`, `tier`, or `id` "are never valid here." The actual acceptance rule at `:1168-1171` is broader: `patternProperties` allows any key matching `^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$`, which includes names such as `HRE::content`. A local `jsonschema` validation probe using `extension_annotations: {HRE::content: "shadow"}` returned `VALID`, confirming that the reserved-suffix rule is currently documentary rather than structural.

**Findings:**

1. **Reserved-Key Safety Is Not Machine-Enforced:** The schema text promises that several suffixes are invalid, but the only actual key-level validator is a positive namespace-format regex that still admits those suffixes. Consumers therefore cannot rely on the schema to block shadow keys.
2. **The Core/Extension Isolation Contract Is Weaker Than Advertised:** `extension_annotations` is the sanctioned channel for Extension metadata, so gaps there matter disproportionately. If reserved suffixes are allowed, extensions can encode names that visually shadow Core fields even while the prose says that should never happen.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-005

The resolution goal is to make the extension-annotation namespace rules mechanically enforceable without undermining the existing Extension/Core separation model.

#### Option A: Explicitly Block Reserved Annotation Suffixes

Keep the current namespaced annotation design, but add a second key-validation layer that rejects keys whose segment after `::` is `content`, `parent_ids`, `status`, `tier`, or `id`. In Draft 2020-12 this can be expressed cleanly with `propertyNames`, either as a negative reserved-suffix pattern or as a `not` guard composed with the existing namespace-format rule. This preserves the current extension architecture while finally making the published safety constraint testable. It also avoids pushing collision-handling complexity into every downstream consumer.

* **Supporting Insights:** The schema already validates annotation key format, so the missing piece is not a new concept but a narrower key-name constraint. Tightening the schema here keeps the Core/Extension boundary enforced at the intake point instead of relying on runtime conventions.
* **Citations:** [JSON Schema object reference (`propertyNames`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema object reference (`patternProperties`)](https://json-schema.org/understanding-json-schema/reference/object).

#### Option B: Relax the Normative Text and Delegate Collision Handling to Tooling

Remove the "never valid" language from the schema description and treat namespacing alone as the only guaranteed separation mechanism. Under this strategy, `HRE::content` and similar keys remain structurally valid, and any collision sensitivity is delegated to extension-specific contracts, renderers, or normalization pipelines. This avoids adding another schema rule, but it weakens the current safety posture and makes interoperability depend more heavily on consumer discipline. It also leaves the published Core/Extension boundary looser than the rest of the extension model suggests.

* **Supporting Insights:** Option B is effectively a policy retreat rather than a technical repair. It is viable only if the project is comfortable replacing a schema-level guarantee with a convention enforced elsewhere.
* **Citations:** [JSON Schema object reference (`propertyNames`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema object reference (`patternProperties`)](https://json-schema.org/understanding-json-schema/reference/object).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Safety Guarantee Location:** Option A keeps the reserved-word guarantee inside the schema, where every producer and validator sees the same rule. Option B removes that guarantee from the schema and forces each toolchain to decide how much collision protection it wants.
2. **Complexity Distribution:** Option A adds a modest schema constraint but simplifies downstream consumer behavior because invalid shadow keys never validate. Option B keeps the schema simpler, but it spreads the complexity into tooling, documentation, and extension-specific review practices.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

DDR v6.1 already claims that these shadow keys are invalid, and JSON Schema provides a direct way to enforce property-name constraints. Using that capability is a smaller and cleaner fix than weakening the published rule and asking every consumer to compensate for it independently.

**Option A** is recommended because:

* **Spec-to-Schema Alignment:** It makes the machine contract finally enforce the reserved-suffix rule that the prose already declares.
* **Stronger Extension Isolation:** Extension metadata stays namespaced without being able to mimic Core field names at the schema boundary.
* **Lower Operational Ambiguity:** Producers get immediate validation feedback, and consumers no longer need private heuristics to detect or sanitize shadow keys.

### 4. GPT-5.4 Endorsement

GPT-5.4 endorses the current Recommended Strategy, **Option A**, as the maximally optimized solution for ISSUE-005.

This endorsement is based on the current DDR v6.1 contract boundary: the issue is a missing schema-level prohibition on already-identified reserved suffixes inside `extension_annotations`. Option A restores that guarantee exactly where the spec says it should live, with minimal blast radius and without weakening AX-6, CIT-R5, or EXT-R3 by delegating collision handling to downstream tooling.
