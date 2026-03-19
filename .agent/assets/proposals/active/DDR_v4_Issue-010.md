---
document:
  id:              DDR_v4_Issue-010
  title:           "Resolution Report for ISSUE-010: extension_annotations Namespace Enforcement Is Absent at Schema Level"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v4.0"
  created:         "2026-03-19"
  status:          "OPEN"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-010"

### Agent Context

```yaml
id:          ISSUE-010
status:      OPEN
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   [ALL]
section_ref: §8, §8.3
rule_refs:   [EXT-R3, AX-6]
```

### 1. Validation Audit of ISSUE-010

An evaluation of `ddr_node_schema.yaml` (§3.1 DdrNode definition), `DDR System(Opus_v4).md` (§8 Extension System, §8.3 Extension Integration Rules), `ddr_system_v4.0.yaml` (§8 extension_system), and `DDR_v4_Adversarial_Audit.md` (Finding-10) was conducted to investigate the claims of "ISSUE-010: `extension_annotations` Namespace Enforcement Is Absent at Schema Level."

The `DdrNode` definition in `ddr_node_schema.yaml` (lines 793–800) defines the `extension_annotations` field as:

```yaml
extension_annotations:
  type: object
  description: >
    Read-only Extension metadata (§3.1, §8.1). Keys namespaced by
    Extension ID (e.g. 'HRE::min_hardware_profile'). Never in parent_ids
    or content (CIT-R5, EXT-R3).
  additionalProperties: true
  default: {}
```

The `description` field correctly references the `EXT-R3` naming convention and `CIT-R5` placement constraint. However, the operative schema keyword is `additionalProperties: true`, which accepts *any* key-value pair without structural validation. No `patternProperties` keyword is present. The schema declares `additionalProperties: false` on the `DdrNode` object itself (line 735), preventing top-level field injection — but within `extension_annotations`, the open schema permits keys such as `content`, `parent_ids`, `status`, or any namespace-less string. These keys would shadow Core node field names and pass JSON Schema 2020-12 validation without error.

`EXT-R3` is defined in `DDR System(Opus_v4).md` (line 587): *"Annotations must be namespaced by Extension ID (e.g., `HRE::min_hardware_profile`)."* The corresponding YAML encoding in `ddr_system_v4.0.yaml` (lines 1081–1084) repeats this statement. Both sources treat namespace compliance as a normative rule, but no schema construct enforces it.

`AX-6` (Declarative Integrity, `DDR System(Opus_v4).md`, line 50) states: *"The Core is strictly declarative; all inference, optimization, and automated recommendation are Extension-only behaviors."* Extensions may not *"Modify any Core node's content, parent_ids, tier, or status"* (§8.1 prohibited actions, `DDR System(Opus_v4).md`, line 564). The `DDR_v4_Adversarial_Audit.md` Finding-10 (lines 208–231) independently identifies this same gap and notes: *"A non-conforming Extension (buggy or adversarial) could write keys like `content`, `parent_ids`, `status`, or namespace-less keys like `min_hardware_profile` and pass JSON Schema validation."*

**Findings:**

1. **Schema-Rule Enforcement Gap:** `EXT-R3` establishes a normative namespace convention (`EXTENSION_ID::annotation_key`), but `ddr_node_schema.yaml` does not enforce this convention at the schema level. The rule exists only as prose and descriptive text — not as a machine-verifiable constraint. Any JSON Schema 2020-12 validator processing a DDR node will accept non-namespaced annotation keys without error. This means the schema contract is incomplete: it validates structural shape but not naming compliance, contradicting the system's §11 claim that schemas are "machine-parseable" (ICL-R2).

2. **Core Field Shadowing Risk:** The `additionalProperties: true` policy on `extension_annotations` permits keys that share names with `DdrNode` top-level properties (`content`, `parent_ids`, `status`, `tier`, `id`). While these keys are nested within `extension_annotations` and do not directly overwrite Core fields, a buggy Extension runtime or a naive deserialization layer could conflate annotation keys with Core node fields if the namespace boundary is not enforced. The schema provides no defense-in-depth against this failure mode.

3. **Cross-Extension Collision Undetectable:** Without namespace enforcement, two Extensions could independently write to the same annotation key (e.g., both HRE and DGA writing a key `min_profile`). The schema cannot detect this collision because it imposesi no naming structure. Only runtime Extension integration logic could identify the conflict — but the schema is the foundational validation layer and should catch structural violations before runtime.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-010

The resolution must make `EXT-R3` namespace compliance mechanically verifiable at the JSON Schema level, eliminating reliance on runtime-only enforcement while preserving backward compatibility for compliant Extension annotations.

#### Option A: Add patternProperties Constraint with additionalProperties: false

Replace the current `extension_annotations` schema definition in `ddr_node_schema.yaml` with a `patternProperties` constraint that enforces the `EXTENSION_ID::annotation_key` format:

```yaml
extension_annotations:
  type: object
  description: >
    Read-only Extension metadata (§3.1, §8.1). Keys MUST follow format:
    EXTENSION_ID::annotation_key (EXT-R3). EXTENSION_ID must be uppercase
    alphanumeric. annotation_key must be lowercase snake_case.
  patternProperties:
    "^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$":
      description: "Valid namespaced annotation. Format: EXTENSION_ID::annotation_key"
  additionalProperties: false
  default: {}
```

The `patternProperties` + `additionalProperties: false` combination is the idiomatic JSON Schema 2020-12 mechanism for key-name validation. Any key not matching the regex `^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$` will fail validation immediately. This is a non-breaking change for all compliant Extensions (any annotation already following the `HRE::min_hardware_profile` convention passes unchanged). Non-compliant annotations are caught at validation time rather than at runtime.

* **Supporting Insights:** The DDR schema already uses `additionalProperties: false` on the `DdrNode` object itself (line 735 of `ddr_node_schema.yaml`) and on every `$defs` type definition throughout the schema — demonstrating an established project convention of closed schemas. Applying the same strictness to `extension_annotations` is architecturally consistent. The `Axiom` definition (lines 390–403) uses `pattern: "^AX-[0-9]+$"` on the `id` field, establishing a precedent for regex-based format enforcement within the schema.

* **Citations:** JSON Schema Draft 2020-12 specification ([json-schema.org](https://json-schema.org/draft/2020-12/json-schema-core)) defines `patternProperties` as the mechanism for validating property names against regular expressions and `additionalProperties` as the constraint on unevaluated properties. The combination of `patternProperties` + `additionalProperties: false` is the recommended pattern for enforcing closed object schemas with dynamic key names, as documented in the JSON Schema Understanding guide ([json-schema.org/understanding-json-schema](https://json-schema.org/understanding-json-schema/reference/object#additionalproperties)).

#### Option B: Introduce a Structured ExtensionAnnotation Array Type

Replace the map-based `extension_annotations` with a typed array of `ExtensionAnnotation` objects, where each annotation is a first-class typed record with explicit `extension_id`, `annotation_key`, and `value` fields:

```yaml
ExtensionAnnotation:
  type: object
  required: [extension_id, annotation_key, value]
  additionalProperties: false
  properties:
    extension_id:
      type: string
      pattern: "^[A-Z][A-Z0-9_]+$"
    annotation_key:
      type: string
      pattern: "^[a-z][a-z0-9_]+$"
    value:
      description: "Annotation value. Any JSON-serializable type."

# In DdrNode:
extension_annotations:
  type: array
  items:
    $ref: "#/$defs/ExtensionAnnotation"
  default: []
```

This changes the data model from a flat key-value map to a structured array of typed records. The `extension_id` and `annotation_key` are validated independently via their own regex patterns. Cross-Extension collisions become detectable by uniqueness constraints on the `[extension_id, annotation_key]` tuple. Querying annotations by Extension becomes a filter on `extension_id` rather than key-prefix parsing. This is a **breaking schema change** — the field type changes from `object` to `array`, requiring migration of all existing DDR project files that contain Extension annotations.

* **Supporting Insights:** The DDR schema already models `parent_ids` as a typed array of `ParentCitation` objects (lines 773–780 of `ddr_node_schema.yaml`) rather than a flat string list — demonstrating a project precedent for promoting structurally important relationships to first-class typed records. Applying the same pattern to Extension annotations elevates them from opaque key-value metadata to structurally queryable, independently validated records. This aligns with the system's architectural emphasis on machine-parseable contracts (ICL-R2, AX-3).

* **Citations:** ISO/IEC 23053:2022 ("Framework for AI Systems Using Machine Learning") emphasizes that metadata associated with AI system components should be structured and independently auditable. The structured array approach aligns with the principle of typed, self-describing metadata records recommended by the OpenAPI Specification v3.1 ([spec.openapis.org](https://spec.openapis.org/oas/v3.1.0)) for extension metadata fields, which uses typed objects over unstructured maps for interoperability and tooling support.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System Specification v4.0 invariants:

1. **Breaking Change Impact:** Option A is non-breaking — all compliant Extension annotations (keys matching `EXTENSION_ID::annotation_key`) pass unchanged. Non-compliant annotations, which are already in violation of `EXT-R3`, are correctly rejected. Option B is a breaking change: the field type changes from `object` to `array`, invalidating all existing DDR project files that have populated `extension_annotations`. This requires a schema migration path, tooling support, and a version bump.

2. **Query Ergonomics:** Option A retains direct key-based access (`node.extension_annotations["HRE::min_hardware_profile"]`), which is idiomatic for map lookups. Option B requires filtering an array by `extension_id` and `annotation_key`, which is more verbose for simple lookups but provides superior structured querying (e.g., "get all annotations from Extension HRE" is a filter on one field rather than substring matching on keys). For agentic workflows where Extensions produce many annotations per node, Option B scales better.

3. **Cross-Extension Collision Detection:** Option A prevents namespace-less keys but does not structurally prevent two Extensions from writing to identical keys — the regex validates format only, not uniqueness. Option B enables a uniqueness constraint on `[extension_id, annotation_key]` tuples, making collision detection a schema-level guarantee. However, JSON Schema 2020-12 does not natively support uniqueness constraints on object property combinations within arrays, so runtime enforcement remains necessary for both options.

4. **Implementation Complexity and Timeline:** Option A requires a single field modification in `ddr_node_schema.yaml` — approximately 5 lines changed. Option B requires a new `$defs` type definition, field type conversion, migration tooling, and updates to every Extension integration rule that references `extension_annotations`. Option A is deployable immediately as a v4.1 patch; Option B is a v5.0 evolution target.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A closes the schema-rule enforcement gap identified in ISSUE-010 with a targeted, non-breaking change that is immediately deployable. It establishes the namespace enforcement foundation upon which Option B could later be built as a major-version evolution.

**Option A** is recommended because:

* **Non-Breaking Deployment:** All compliant Extension annotations pass unchanged. No migration tooling required. No existing DDR project files are invalidated. This can ship as a v4.1 patch.
* **Idiomatic JSON Schema:** The `patternProperties` + `additionalProperties: false` combination is the standard JSON Schema 2020-12 mechanism for key-name validation, maximizing compatibility with existing validation tooling and libraries.
* **Architectural Consistency:** The schema already uses `additionalProperties: false` on all other object types and regex `pattern` constraints on ID fields. Applying the same patterns to `extension_annotations` requires no new structural concepts.
* **Immediate Risk Mitigation:** The Core field shadowing risk (keys like `content`, `parent_ids`, `status` inside `extension_annotations`) and namespace-less key injection are eliminated at the validation layer, restoring defense-in-depth without waiting for a major version overhaul.
* **Evolutionary Path Preserved:** Option A does not preclude Option B. The `patternProperties` enforcement can serve as an interim constraint until the structured array model is adopted in a future major version, at which point the regex validation migrates to per-field `pattern` constraints on `extension_id` and `annotation_key`.
