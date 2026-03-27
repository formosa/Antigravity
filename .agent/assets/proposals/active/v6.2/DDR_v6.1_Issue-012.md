---
document:
  id:              DDR_v6.1_Issue-012
  title:           "Resolution Report for ISSUE-012: `parent_ids` Empty Array Default Allows Orphaned Non-Root Nodes"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.1"
  created:         "2026-03-27"
  status:          "OPEN"
  severity:        "MAJOR"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-012"

### Agent Context

```yaml
id:          ISSUE-012
status:      OPEN
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   ["All (schema)"]
section_ref: "§3.1, §3.5, §3.7"
rule_refs:   ["INV-5", "CIT-R1", "AX-1"]
```

### 1. Validation Audit of ISSUE-012

An audit of `.agent/assets/proposals/active/v6.1/ddr_node_schema.yaml` and `.agent/assets/proposals/active/v6.1/ddr_system_v6.1.yaml` confirms the issue.

`DdrNode.parent_ids` is described as "Empty only for root nodes ... Non-root nodes require ≥1 entry", but the schema block does not enforce `minItems` or any root-aware conditional. The field is defined with `default: []`, which allows empty arrays structurally. In the system specification, both `INV-5` and `CIT-R1` require non-root nodes to have at least one parent citation. Because the machine schema does not encode that invariant, non-root orphan nodes can pass schema validation despite violating normative traceability rules.

**Findings:**

1. **Normative-to-schema mismatch is real:** The prose contract and invariant/rule layer require non-root parent linkage, but the machine contract does not enforce it.
2. **Current schema permits structural orphaning:** Empty `parent_ids` remains valid independent of node tier or graph context, so enforcement is deferred to runtime tooling.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-012

The resolution goal is to restore schema-level enforcement of non-root parent cardinality while preserving legitimate root-node exceptions.

#### Option A: Root-Aware Conditional `minItems` Enforcement

Retain the existing `DdrNode` model and add conditional schema clauses that require `parent_ids.minItems: 1` for non-root nodes. Preserve root exceptions by expressing conditions tied to tier activation semantics (e.g., XPD roots when active, SIL roots when XPD inactive). This approach is surgical and aligns with the existing design preference for minimal targeted corrections. It also preserves backward compatibility for validators and code generators that already consume the current node shape.

* **Supporting Insights:** This issue is a pure contract-enforcement gap, not a modeling gap. A conditional fix closes the defect with minimal schema churn and supports independent resolution as required by the proposal constraints.
* **Citations:** [JSON Schema conditionals (`if`/`then`/`else`)](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema arrays (`minItems`)](https://json-schema.org/understanding-json-schema/reference/array)

#### Option B: Split Root and Non-Root Node Variants

Refactor `DdrNode` into explicit root-capable and non-root variants (or tier-specific variants) where parent cardinality is encoded structurally. In this approach, only root variants permit empty `parent_ids`; non-root variants require one or more citations by construction. This improves type clarity and error quality, and composes naturally with tier-specific modeling proposed in ISSUE-011. The tradeoff is significantly broader schema change and migration overhead.

* **Supporting Insights:** Structural variants improve long-term expressiveness where multiple cross-field invariants depend on node role. However, this broadens the implementation surface and may conflict with the stated preference for minimal edits.
* **Citations:** [JSON Schema combinators (`oneOf`)](https://json-schema.org/understanding-json-schema/reference/combining), [JSON Schema object modeling](https://json-schema.org/understanding-json-schema/reference/object)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

1. **Change scope:** Option A is localized and low-risk; Option B is architectural and high-impact.
2. **Rule enforcement fidelity:** Both can enforce non-root cardinality, but Option B does so more structurally.
3. **Adoption cost:** Option A is easier for current consumers; Option B requires broader migration and revalidation.
4. **Coordination burden:** Option A remains independently resolvable; Option B introduces coupling to broader schema redesign initiatives.

#### Endorsement and Contextual Justification

**Option A (Recommended Strategy)**

- Provides a direct fix for the verified defect with minimal blast radius.
- Aligns schema behavior with `INV-5` and `CIT-R1` without redesigning node taxonomy.
- Preserves independence of issue resolution and established compatibility expectations.
- Keeps future refactor latitude open if a later tier-variant redesign is approved.
