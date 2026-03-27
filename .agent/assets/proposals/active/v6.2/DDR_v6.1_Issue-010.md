---
document:
  id:              DDR_v6.1_Issue-010
  title:           "Resolution Report for ISSUE-010: Lifecycle Guard References Accept Undefined Guard IDs"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
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
tier_refs:   ["All lifecycle definitions"]
section_ref: "§3.8"
rule_refs:   [gc-001, gc-002, gc-003, gc-004, gc-005, gc-006, gc-007, gc-008, gc-009]
```

### 1. Validation Audit of ISSUE-010

An evaluation of `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml` and `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml` was conducted to investigate the claims of "ISSUE-010: Lifecycle Guard References Accept Undefined Guard IDs."

The lifecycle transition schema defines `guards` at `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_node_schema.yaml:1035-1038` as an array whose items are plain strings. `GuardDefinition.id` is separately typed at `:1061-1063` with the pattern `^gc-[0-9]+$`, but that definition is not reused by `StatusTransition.guards`. The actual lifecycle authority in `c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\active\v6.1\ddr_system_v6.1.yaml:2623-2660` enumerates a closed guard set `gc-001` through `gc-009`. A direct `jsonschema` validation probe accepted a transition with `guards: ['gc-999']`, confirming that undefined guard references are structurally valid today.

**Findings:**

1. **Guard References Lack Referential Integrity:** The schema gives transitions a way to cite guard IDs, but it does not ensure those IDs correspond to the lifecycle authority's declared guard set. Misspellings and phantom guards therefore pass validation.
2. **The Lifecycle Safety Model Can Drift Silently:** Guards are the named preconditions on lifecycle operations. If transitions can cite nonexistent guards, tools cannot rely on validation to catch broken safety references before runtime or review.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-010

The resolution goal is to make lifecycle guard references at least lexically reliable, and ideally fully aligned with the versioned guard set declared by the authority block.

#### Option A: Constrain Guard References to the Versioned Guard Set

Define a reusable guard-reference type for `StatusTransition.guards` that matches the actual v6.1 guard authority, ideally by enumerating `gc-001` through `gc-009` or by centralizing those IDs in one authoritative schema definition reused by both definitions and references. This is the strongest contract because it gives validators exact knowledge of which guards are valid in the versioned lifecycle. It immediately blocks both typos and nonexistent guards. The tradeoff is that the schema must be updated whenever the versioned guard set changes.

* **Supporting Insights:** The current lifecycle block already behaves like versioned authority data, so exact reference typing is consistent with the rest of the design. Closed vocabularies are most valuable where safety-critical preconditions are being referenced by identifier.
* **Citations:** [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object).

#### Option B: Enforce a Lexical Guard-ID Pattern as a Minimum Floor

If the project does not want to close the reference set to exact IDs, at minimum constrain `StatusTransition.guards` to the established lexical format, such as `^gc-[0-9]{3}$`. This is weaker than exact-set validation because values like `gc-999` would still pass, but it at least blocks malformed identifiers like `gc-07` or `guard-seven`. It is a modest improvement with low implementation cost. The tradeoff is that referential integrity remains partly outside the schema.

* **Supporting Insights:** Pattern validation is useful when the project wants a lightweight guardrail without closing the vocabulary. It should be treated as a floor, not as a full substitute for version-aware reference integrity.
* **Citations:** [JSON Schema string reference (`pattern`)](https://json-schema.org/understanding-json-schema/reference/string), [JSON Schema enumerated values (`enum`)](https://json-schema.org/understanding-json-schema/reference/enum).

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.1 invariants:

1. **Integrity Strength:** Option A provides exact-set validation and catches both malformed and nonexistent IDs. Option B improves lexical hygiene only, leaving phantom but well-formed guards structurally valid.
2. **Maintenance Burden:** Option A requires the schema's reference set to evolve with the lifecycle authority. Option B is easier to maintain, but it intentionally stops short of real referential integrity.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The current v6.1 lifecycle authority already publishes a concrete finite guard set. Since these identifiers gate lifecycle safety checks, exact reference validation is worth the small maintenance overhead.

**Option A** is recommended because:

* **Stronger Safety Assurance:** Undefined or misspelled guards stop validating immediately.
* **Versioned Consistency:** References stay aligned with the same closed lifecycle authority that defines the guards.
* **Clearer Tool Behavior:** Consumers can trust that any validated guard reference resolves to a real declared precondition.
