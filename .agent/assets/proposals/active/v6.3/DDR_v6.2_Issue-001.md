---
document:
  id:              DDR_v6.2_Issue-001
  title:           "Resolution Report for ISSUE-001: Require the Full System-Definition Normative Surface"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  updated:         "2026-03-27"
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
tier_refs:   ["System-definition files"]
section_ref: "Schema Root, §5-§9"
rule_refs:   []
updated:     2026-03-27
```

### 1. Validation Audit of ISSUE-001

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:27-36`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:205-289`, and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:247-252` was conducted to investigate the claims of "ISSUE-001: Require the Full System-Definition Normative Surface."

The root contract only adds `lifecycle` when `system_metadata` is present at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:27-36`. The same schema still exposes `dag_invariants`, `citation_rules`, `tier_definitions`, `constraint_precedence`, and `operations` as top-level authority sections at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:205-289`, and `tier_definitions` explicitly says it is required for system-definition files at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:247-252`. A local `jsonschema` probe accepted a document containing only `ddr_version`, the mandatory seven active tiers, one minimal node, `system_metadata`, and `lifecycle`, confirming that the published schema still treats the rest of the normative system-definition surface as optional.

**Findings:**

1. **System-Definition Admission Is Under-Specified:** The schema has a structural marker for system-definition files but uses it to require only `lifecycle`. That leaves the rest of the claimed authoritative surface unenforced at the schema root.
2. **Authoritative Files Can Validate While Incomplete:** A system-definition artifact can present itself as authoritative and still omit major governing sections without failing validation. That weakens the self-hosting contract of DDR v6.2 at the exact boundary the schema is supposed to protect.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

The resolution goal is to make the root schema tell the truth about what a valid DDR v6.2 system-definition artifact must contain.

#### Option A: Add a Definition Profile Conditional

Keep the current implicit document split, but extend the root conditional keyed to `system_metadata` so it requires the minimum authoritative section set for a system-definition file. At minimum that set should include `lifecycle`, `tier_definitions`, `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations`, with any other sections the project treats as normative added to the same branch. This repairs the defect with the smallest contract change because it reuses the schema's existing discriminator rather than inventing a second document-class mechanism.

* **Supporting Insights:** The schema already distinguishes project-instance versus system-definition intent through `system_metadata`. Reusing that marker keeps the repair local to the root contract and preserves the lean project-instance story for files that are not acting as specification authority.
* **Citations:** [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object), [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals)

#### Option B: Introduce Explicit Document Profiles

Add a root-level `document_profile` enum such as `project_instance | system_definition` and split root requirements by that explicit profile instead of inferring intent from `system_metadata`. This is a broader redesign, but it makes author intent machine-explicit and creates a durable place to encode profile-specific obligations as the DDR system evolves. It also gives future efforts such as ARE authority hardening a cleaner root hook than incidental inference from one metadata block.

* **Supporting Insights:** Explicit profiles make the schema's two roles visible instead of implicit, which improves explainability for tooling authors and future maintainers. The tradeoff is a wider migration because every authoritative document would need to declare its profile and align to the new root rules.
* **Citations:** [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema structuring with `$defs`](https://json-schema.org/understanding-json-schema/structuring)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Repair Scope:** Option A closes the critical defect directly at the existing root conditional, while Option B introduces a broader schema redesign centered on explicit document profiles.
2. **Contract Explicitness:** Option A preserves the current implicit split between project-instance and system-definition files; Option B makes that split first-class and easier to reason about across future schema growth.
3. **Migration Cost:** Option A has the smaller blast radius because existing authoritative files already carry `system_metadata`; Option B requires new profile declarations and wider downstream adoption.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated defect is that the current schema already has enough information to recognize a system-definition file but does not enforce the full normative surface once it does. Reusing that existing marker fixes the critical gap without expanding the document model before the project has proven it needs a new explicit profile field.

**Option A** is recommended because:

* **Uses Existing Intent Signals:** `system_metadata` already marks the authoritative file class, so the fix can stay local to the current root contract.
* **Closes the Critical Gap Quickly:** The schema can stop admitting incomplete system-definition artifacts without forcing a broader migration of all DDR documents.
* **Preserves Future Flexibility:** If later versions need explicit profiles, Option A still leaves that path open after the immediate contract defect is repaired.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
