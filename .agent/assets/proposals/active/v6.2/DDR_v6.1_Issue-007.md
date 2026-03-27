---
document:
  id:              DDR_v6.1_Issue-007
  title:           "Resolution Report for ISSUE-007: `lifecycle` Object Accepts Arbitrary Keys"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  resolved:        "2026-03-27"
  status:          "RESOLVED"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-007"

### Agent Context

```yaml
id:          ISSUE-007
status:      RESOLVED
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["All lifecycle blocks"]
section_ref: "Schema Root, §3.8"
rule_refs:   []
updated:     2026-03-27
resolved:    2026-03-27
```

> **Resolution (2026-03-27):** Option A — Closed the `lifecycle` object against undeclared keys.

### 1. Validation Audit of ISSUE-007

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` was conducted to investigate the claims of "ISSUE-007: `lifecycle` Object Accepts Arbitrary Keys."

The `lifecycle` object is defined at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:401-421` with `required: [status_transitions]` and named properties for `status_transitions`, `prohibited_transitions`, and `guard_definitions`. Unlike surrounding major objects such as the root schema (`:31`), `project` (`:67`), `system_metadata` (`:93`), `DdrNode` (`:1087`), and `ParentCitation` (`:1179`), the `lifecycle` block is not closed with `additionalProperties: false`. A direct `jsonschema` validation probe accepted `lifecycle: {status_transitions: [], rogue_key: true}`. This confirms that undeclared lifecycle keys are structurally valid today.

**Findings:**

1. **The Lifecycle Authority Surface Is Open:** The schema enumerates a specific lifecycle contract, but validators do not reject undeclared sibling properties inside that same object. That makes the authority block looser than the rest of the schema's major surfaces.
2. **Lifecycle Extensions Can Leak In Silently:** Because the openness is implicit rather than designed, tools can start depending on ad hoc lifecycle keys without any versioned schema change. That undermines the closed-contract discipline used almost everywhere else in the document.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-007

The resolution goal is to ensure the lifecycle authority block is explicit about whether it is closed or intentionally extensible.

#### Option A: Add `additionalProperties: false` to `lifecycle`

Close the existing `lifecycle` object with `additionalProperties: false`. This is the smallest and clearest repair because it matches the design pattern already used across the schema's other major object surfaces. It preserves the current lifecycle structure exactly while preventing undeclared keys from being treated as valid contract data. Future lifecycle expansion can still happen through explicit versioned schema edits.

* **Supporting Insights:** The defect here is not missing lifecycle content but an unintentionally open property surface. Closing the object restores consistency with the rest of the schema at minimal cost.
* **Citations:** [JSON Schema object reference (`additionalProperties`)](https://json-schema.org/understanding-json-schema/reference/object).

#### Option B: Close the Core Lifecycle Surface and Add an Explicit Extension Channel

Close the core `lifecycle` object, but if controlled extensibility is actually desired, add a clearly named subordinate extension bag with its own namespacing rules. This is broader than Option A because it introduces a new contract surface and a naming policy for lifecycle extensions. The benefit is that lifecycle extensibility becomes explicit and reviewable instead of leaking through accidental openness. The tradeoff is extra schema complexity for a capability the current document does not otherwise signal.

* **Supporting Insights:** If the project anticipates vendor-specific or tool-specific lifecycle metadata, an explicit extension channel is much safer than a silently open normative object. It keeps the core contract stable while still leaving room for controlled annotations.
* **Citations:** [JSON Schema object reference (`additionalProperties`)](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema object reference (`propertyNames`)](https://json-schema.org/understanding-json-schema/reference/object).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Implementation Cost:** Option A is a one-line closure change with negligible migration cost. Option B adds a new extension surface and therefore a new policy to explain, review, and maintain.
2. **Extensibility Posture:** Option A treats the current openness as accidental and closes it. Option B preserves extensibility, but only by making it explicit and governed.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Nothing in the current v6.1 lifecycle contract suggests that arbitrary sibling keys are intentionally supported. The evidence reads as an omission, not a designed extension mechanism.

**Option A** is recommended because:

* **Contract Consistency:** It brings `lifecycle` into line with the schema's otherwise closed major-object pattern.
* **Minimal Blast Radius:** It fixes the defect without redesigning the lifecycle authority surface.
* **Stronger Validator Signal:** Undeclared lifecycle keys stop passing silently and start failing where the contract is defined.

### 4. Implementation Note

Implemented in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.2\ddr_node_schema_v6.2.yaml` by adding `additionalProperties: false` to the `lifecycle` object definition. Post-change validation confirmed that undeclared lifecycle keys now fail while the canonical lifecycle block in `ddr_system_v6.2.yaml` remains valid.