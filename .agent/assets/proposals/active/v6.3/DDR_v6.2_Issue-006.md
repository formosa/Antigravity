---
document:
  id:              DDR_v6.2_Issue-006
  title:           "Resolution Report for ISSUE-006: Type Remaining Normative Rule Identifiers"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  status:          "OPEN"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-006"

### Agent Context

```yaml
id:          ISSUE-006
status:      OPEN
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["DAG invariants", "tier rules", "extension rules"]
section_ref: "§3.5, §5, §9"
rule_refs:   []
updated:     2026-03-27
```

### 1. Validation Audit of ISSUE-006

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:595-603`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:607-614`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:676-683`, and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:906-925` was conducted to investigate the claims of "ISSUE-006: Type Remaining Normative Rule Identifiers."

`DagInvariant.id` is still typed only as a generic string at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:595-603`, while `AtomicExclusionRule.rule_id` and `ExtensionRule.rule_id` remain equally loose at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:676-683` and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:919-925`. In the same schema family, `CitationRule.rule_id` and `ExtensionIntegrationRule.rule_id` already use typed patterns at `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:607-614` and `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:906-913`. A local `jsonschema` probe accepted `dag_invariants: [{id: "tier-skip", statement: "bad id still passes"}]`, confirming that malformed normative identifiers remain schema-valid.

**Findings:**

1. **Rule-ID Strictness Is Inconsistent Across Sibling Families:** Some normative identifiers are pattern-typed already, while adjacent families still accept arbitrary strings. That inconsistency weakens the schema as a single authority for rule naming.
2. **Malformed IDs Can Enter Authoritative Documents Early:** Invalid or ad hoc identifiers can pass schema validation and only fail later when tooling expects structured IDs for cross-reference, migration, or alias handling.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-006

The resolution goal is to give all remaining normative rule families the same structural discipline already used by the stricter parts of the schema.

#### Option A: Add Pattern Constraints Per Rule Family

Add explicit regex patterns for each currently untyped family, such as `^INV-[0-9]+$` for `DagInvariant.id` and family-appropriate patterns for tier-rule and extension-rule identifiers. This is the lowest-blast-radius repair because it can be applied directly to the existing object definitions without reorganizing the schema. It closes the present validation gaps quickly, but it still leaves identifier patterns distributed across multiple places.

* **Supporting Insights:** The schema already demonstrates that pattern-typing rule IDs is an accepted design choice for related families. Extending that same discipline to the remaining loose fields is a straightforward consistency repair.
* **Citations:** [JSON Schema string reference](https://json-schema.org/understanding-json-schema/reference/string)

#### Option B: Centralize Rule-ID Definitions

Create reusable `$defs` entries for each rule-ID family and reference them everywhere those identifiers appear. This is a slightly larger cleanup, but it makes the schema's rule-naming authority explicit and reusable across invariant lists, tier rules, extension rules, and future alias or migration surfaces. Centralization also reduces the chance that one family evolves while another silently drifts.

* **Supporting Insights:** Multiple rule-ID families already exist, and at least some of them are shared conceptual vocabularies rather than isolated leaf fields. Pulling those patterns into `$defs` creates a single maintenance point and helps dependent issues such as alias cleanup anchor to one authority.
* **Citations:** [JSON Schema structuring with `$defs`](https://json-schema.org/understanding-json-schema/structuring), [JSON Schema string reference](https://json-schema.org/understanding-json-schema/reference/string)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Repair Speed:** Option A can be applied quickly as a set of local field edits, while Option B requires a modest schema refactor to establish reusable identifier authorities.
2. **Drift Resistance:** Option A still scatters regex rules across multiple definitions; Option B makes each rule family single-source and easier to evolve consistently.
3. **Cross-Issue Leverage:** Option A fixes the immediate validation holes, but Option B also gives dependent work such as ISSUE-007 a clear place to anchor canonical IDs and aliases.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

The validated defect is bigger than a few missing regexes: the schema currently has no single authority for several normative identifier families. Centralizing those families in `$defs` resolves the present looseness and gives future rule-ID cleanup, aliasing, and migration work a stable foundation.

**Option B** is recommended because:

* **Creates One Identifier Authority Per Family:** Readers and validators can find the canonical format in one place instead of hunting across object definitions.
* **Reduces Future Drift:** Updating an identifier family no longer depends on remembering every field that repeats the same pattern.
* **Supports Dependent Cleanup:** Alias mapping, migration tables, and neighboring issues can reuse the same centralized definitions rather than inventing one-off patterns.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.
