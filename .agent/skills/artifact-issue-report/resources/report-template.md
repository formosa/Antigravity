<document_purpose>
This template defines the canonical `v6.1` issue-report structure used by
`artifact-issue-report`. New reports and first-write migrations must follow this shape exactly.
Legacy `v4` and `v5` reports remain valid historical artifacts, but they are not the
generation target.
</document_purpose>

<template_structure>

```markdown
---
document:
  id:              {{DOCUMENT_ID}}
  title:           "Resolution Report for {{ISSUE_ID}}: {{ISSUE_TITLE}}"
  format_version:  "{{FORMAT_VERSION}}"
  target_platform: "{{TARGET_PLATFORM}}"
  target_model:    "{{TARGET_MODEL}}"
  subject:         "{{SUBJECT_SYSTEM_NAME}}"
  created:         "{{CREATED_DATE}}"
  updated:         "{{UPDATED_DATE}}"
{{RESOLVED_FRONTMATTER_LINE}}
  status:          "{{STATUS}}"
  severity:        "{{SEVERITY}}"
  type:            "{{TYPE}}"
---

## Optimized Resolution Strategy for "{{ISSUE_ID}}"

### Agent Context

```yaml
id:          {{ISSUE_ID}}
status:      {{STATUS}}
severity:    {{SEVERITY}}
type:        {{TYPE}}
tier_refs:   {{TIER_REFS}}
section_ref: {{SECTION_REF}}
rule_refs:   {{RULE_REFS}}
updated:     {{UPDATED_DATE}}
{{RESOLVED_AGENT_CONTEXT_LINE}}
```

{{RESOLUTION_CALLOUT_BLOCK}}
### 1. Validation Audit of {{ISSUE_ID}}

An evaluation of {{PRIMARY_SOURCE_FILES}} was conducted to investigate the claims of "{{ISSUE_ID}}: {{ISSUE_TITLE}}."

{{AUDIT_NARRATIVE}}

**Findings:**

1. **{{FINDING_1_LABEL}}:** {{FINDING_1_DESCRIPTION}}
2. **{{FINDING_2_LABEL}}:** {{FINDING_2_DESCRIPTION}}

### 2. Suggested Strategies for Optimal Resolution of {{ISSUE_ID}}

{{RESOLUTION_PREAMBLE}}

#### Option A: {{OPTION_A_LABEL}}

{{OPTION_A_DESCRIPTION}}

* **Supporting Insights:** {{OPTION_A_INSIGHTS}}
* **Citations:** {{OPTION_A_CITATIONS}}

#### Option B: {{OPTION_B_LABEL}}

{{OPTION_B_DESCRIPTION}}

* **Supporting Insights:** {{OPTION_B_INSIGHTS}}
* **Citations:** {{OPTION_B_CITATIONS}}

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to {{SUBJECT_SYSTEM_NAME}} invariants:

1. **{{TRADEOFF_1_LABEL}}:** {{TRADEOFF_1_ANALYSIS}}
2. **{{TRADEOFF_2_LABEL}}:** {{TRADEOFF_2_ANALYSIS}}

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **{{RECOMMENDED_OPTION}} (Recommended Strategy)**.

{{ENDORSEMENT_RATIONALE}}

**{{RECOMMENDED_OPTION}}** is recommended because:

* **{{JUSTIFICATION_1_LABEL}}:** {{JUSTIFICATION_1_DESCRIPTION}}
* **{{JUSTIFICATION_2_LABEL}}:** {{JUSTIFICATION_2_DESCRIPTION}}
* **{{JUSTIFICATION_3_LABEL}}:** {{JUSTIFICATION_3_DESCRIPTION}}

### 4. Implementation Note

{{IMPLEMENTATION_NOTE}}
```

</template_structure>

<placeholder_resolution_rules>

| Placeholder                                         | Source                                                                    | Fallback                                                                  |
| :-------------------------------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------------------------ |
| `{{DOCUMENT_ID}}`                                   | Constructed `{SubjectShortId}_Issue-{NNN}`                                | RFQ                                                                       |
| `{{ISSUE_ID}}`                                      | User request or tracker registry                                          | RFQ                                                                       |
| `{{ISSUE_TITLE}}`                                   | Issue heading from tracker                                                | RFQ                                                                       |
| `{{FORMAT_VERSION}}`                                | Tracker `document.format_version` or canonical issue-report format string | `"v6.1"`                                                                  |
| `{{TARGET_PLATFORM}}`                               | Tracker `document.target_platform`                                        | `"Google Antigravity >=1.20.3"`                                           |
| `{{TARGET_MODEL}}`                                  | Tracker `document.target_model`                                           | `"Gemini 3.1 Pro"`                                                        |
| `{{SUBJECT_SYSTEM_NAME}}`                           | Tracker `document.subject`                                                | RFQ                                                                       |
| `{{CREATED_DATE}}`                                  | Report generation date                                                    | —                                                                         |
| `{{UPDATED_DATE}}`                                  | Report generation date                                                    | —                                                                         |
| `{{RESOLVED_FRONTMATTER_LINE}}`                     | `  resolved:        "YYYY-MM-DD"\n` when status is `RESOLVED`             | empty string                                                              |
| `{{STATUS}}`                                        | Parsed issue status                                                       | RFQ                                                                       |
| `{{SEVERITY}}`                                      | Parsed issue severity                                                     | RFQ                                                                       |
| `{{TYPE}}`                                          | Parsed issue type                                                         | RFQ                                                                       |
| `{{TIER_REFS}}`                                     | Parsed tiers affected, normalized as a YAML list                          | `["All"]`                                                                 |
| `{{SECTION_REF}}`                                   | Parsed spec section or tracker context                                    | `""`                                                                      |
| `{{RULE_REFS}}`                                     | Parsed rule identifiers or tracker context                                | `[]`                                                                      |
| `{{RESOLVED_AGENT_CONTEXT_LINE}}`                   | `resolved:    YYYY-MM-DD\n` when status is `RESOLVED`                     | empty string                                                              |
| `{{RESOLUTION_CALLOUT_BLOCK}}`                      | Preserved tracker callout plus trailing blank line when present           | empty string                                                              |
| `{{PRIMARY_SOURCE_FILES}}`                          | Repo-relative file paths with line spans                                  | `tracker evidence only`                                                   |
| `{{OPTION_A_CITATIONS}}` / `{{OPTION_B_CITATIONS}}` | 1-2 authoritative sources                                                 | `No authoritative external reference identified for this specific claim.` |
| `{{IMPLEMENTATION_NOTE}}`                           | Status-sensitive implementation summary                                   | RFQ                                                                       |

</placeholder_resolution_rules>
