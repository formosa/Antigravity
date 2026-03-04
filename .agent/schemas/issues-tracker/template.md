# {{SUBJECT_SYSTEM_NAME}} — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the {{SUBJECT_SYSTEM_NAME}}. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read only the `` blocks within each issue before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              {{DOCUMENT_ID}}
  title:           "{{SUBJECT_SYSTEM_NAME}} — Issues Tracker"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "{{SUBJECT_SYSTEM_NAME}}"
  created:         "{{YYYY-MM-DD}}"
  last_modified:   "{{YYYY-MM-DD}}"
  author:          "{{AUTHOR_NAME}}"
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT      # Specification makes contradictory claims
    - DESIGN_INADEQUACY     # Feature is absent, under-specified, or insufficient
    - UNNECESSARY_COMPLEXITY # System is more complex than the problem demands
    - AXIOM_VIOLATION       # A rule or behavior contradicts a stated axiom
    - SCHEMA_DEFECT         # Machine-readable schema is incorrect or incomplete
    - MIGRATION_GAP         # Version migration is incomplete or unresolved
    - LIFECYCLE_GAP         # A state, transition, or lifecycle path is undefined
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every new issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the specific issue. 2–4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the spec, plus the logical chain that makes this a problem.
Use inline code formatting for rule IDs and tier names.]

#### Impact Assessment-[NNN]
[What breaks, is ambiguous, or fails if this issue is not resolved.
State the concrete failure mode.]

#### Resolution-[NNN]: Option A — [Short Label]
[Detailed description of first resolution approach. Include specific rule/section changes
required, draft replacement language where applicable, and any trade-offs.]

#### Resolution-[NNN]: Option B — [Short Label]
[Detailed description of second, distinctly different resolution approach. Must not be
a minor variant of Option A — must represent a meaningfully different design decision.]

#### Notes-[NNN]
[Any cross-references, dependencies on other issues, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID | Severity | Type | Status | Tiers Affected | Title |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## ISSUES

---

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue RESOLVED until all steps are confirmed.

```plaintext
1. IDENTIFY issue ID and selected Resolution Option (A or B)
2. DRAFT the specific changes to {{SUBJECT_FILE_NAME}} and/or associated schemas
3. VERIFY draft changes do not introduce new issues (check cross-references in Notes fields)
4. UPDATE the issue entry:
   - Set status: IN_REVIEW
   - Set updated: [date]
5. HUMAN REVIEW of draft changes
6. On approval:
   - Set status: RESOLVED
   - Set resolved: [date]
   - Record resolution: "Option [A|B]: [one-line summary]"
7. UPDATE ISSUE REGISTRY table
8. UPDATE document header metadata (open_issues, resolved_issues)
```

---

## APPENDIX: CROSS-ISSUE DEPENDENCY MAP

> Issues that share a dependency — resolving one may affect the other.

| Issue | Depends On | Nature of Dependency |
| --- | --- | --- |
| | | |

---

*{{SUBJECT_SYSTEM_NAME}} Issues Tracker — IT-1.0*
*{{TOTAL_ISSUES_COUNT}} issues identified | {{RESOLVED_ISSUES_COUNT}} resolved | Last updated: {{YYYY-MM-DD}}*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*
