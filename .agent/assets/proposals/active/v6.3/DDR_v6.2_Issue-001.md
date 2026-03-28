---
document:
  id:              DDR_v6.2_Issue-001
  title:           "Resolution Report for ISSUE-001: Require the Full System-Definition Normative Surface"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
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
section_ref: "Schema Root, \u00a75-\u00a79"
rule_refs:   []
updated:     2026-03-28
```

### 1. Validation Audit of ISSUE-001

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:27-36`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:205-289`, and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:1-6` was conducted to investigate the claims of "ISSUE-001: Require the Full System-Definition Normative Surface".

The root schema recognizes system-definition intent, but it only hard-requires `lifecycle`. The authoritative system file simultaneously claims to represent the full normative specification, so the schema currently under-enforces the very artifact it is supposed to certify.

**Findings:**

1. **Root Closure Is Incomplete:** System-definition files are identifiable but not required to carry the full authoritative surface.
2. **Authority Can Be Claimed While Incomplete:** A system-definition artifact can validate while omitting major governing sections.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

The resolution goal is to make authoritative document intent explicit enough that incomplete system-definition artifacts cannot validate.

#### Option A: Introduce Explicit Document Profiles

Add a root-level `document_profile` enum such as `project_instance | system_definition` and split root requirements by profile rather than inferring profile from `system_metadata`. This is a larger refactor, but it makes document intent explicit and gives future versions a cleaner place to encode profile-specific obligations.

* **Supporting Insights:** An explicit profile field gives future root requirements one durable branching point.
* **Citations:** [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema structuring](https://json-schema.org/understanding-json-schema/structuring)

#### Option B: Add a Definition Profile Conditional

Add an explicit root conditional keyed to `system_metadata` that requires the minimum normative section set for a system-definition artifact. At minimum this should cover `lifecycle`, `tier_definitions`, `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations`, with any other sections the project considers authoritative for self-hosting spec files.

* **Supporting Insights:** Reusing `system_metadata` repairs the current schema with a smaller migration surface.
* **Citations:** [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Explicitness:** Option A makes document role first-class; Option B still infers it from one metadata block.
2. **Migration:** Option A asks all authoritative documents to adopt a profile field; Option B is the smaller patch.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The updated tracker now prefers explicit document profiles because this is not just a missing required-list problem. DDR needs a durable, in-band way to declare what kind of root document is being authored.

**Option A** is recommended because:

* **Machine-Explicit Intent:** Validators no longer infer authoritative status indirectly.
* **Future-Proof Root Contract:** Later profile-specific rules get one stable branching surface.
* **Single Canonical Schema:** The model stays self-describing inside one schema artifact.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
