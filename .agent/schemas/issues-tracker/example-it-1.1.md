# Example Payments API — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the Example Payments API. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read the issue heading plus the `Status`, `Severity`, and `Type` metadata lines before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              ITR-EXAMPLE-PAYMENTS-API
  title:           "Example Payments API — Issues Tracker"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity 1.21.9"
  target_model:    "Gemini 3 Pro Preview"
  subject:         "Example Payments API"
  created:         "2026-03-28"
  last_modified:   "2026-03-28"
  author:          "Example Author"
  open_issues:     2
  resolved_issues: 0
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT
    - DESIGN_INADEQUACY
    - UNNECESSARY_COMPLEXITY
    - AXIOM_VIOLATION
    - SCHEMA_DEFECT
    - MIGRATION_GAP
    - LIFECYCLE_GAP
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every updated issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.
> If an issue later becomes `RESOLVED`, a one-line blockquote resolution note may be
> inserted above `#### Problem Statement-[NNN]`.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the issue. 2-4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the local spec plus the logic that makes this a problem.]

#### Impact Assessment-[NNN]
[Concrete failure mode if the issue is not resolved.]

#### Resolution-[NNN]: Option A - [Short Label]
[First resolution approach.]

#### Resolution-[NNN]: Option B - [Short Label]
[Second, materially different approach.]

#### Resolution-[NNN]: Option C - [Short Label]
[Third, materially different approach.]

#### Comparative Analysis-[NNN]
[Direct comparison of Options A, B, and C.]

#### Recommendation-[NNN]
**Endorsed Option:** `Option A|B|C`
[Precise technical justification for the endorsed option.]

#### Supporting Citations-[NNN]
- [Source Name](https://example.com): One-line explanation of why the source supports the endorsed option.

#### Notes-[NNN]
[Cross-references, dependencies, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID | Severity | Type | Status | Tiers Affected | Title |
| --- | --- | --- | --- | --- | --- |
| [ISSUE-001](#issue-001-require-an-explicit-webhook-profile-discriminator) | `CRITICAL` | `SCHEMA_DEFECT` | `OPEN` | `Webhook schema` | Require an explicit webhook profile discriminator |
| [ISSUE-002](#issue-002-normalize-cursor-pagination-error-semantics) | `MODERATE` | `LOGICAL_CONFLICT` | `OPEN` | `Pagination surface` | Normalize cursor pagination error semantics |

---

## ISSUES

---

### ISSUE-001: Require an Explicit Webhook Profile Discriminator

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Webhook schema` | **Spec Section:** `Schema Root, Webhooks`

#### Problem Statement-001

The webhook object supports both shared-account and tenant-scoped delivery modes, but the schema does not expose a discriminator that tells validators or generators which contract branch is active. That leaves required fields mode-dependent in prose only.

#### Evidence & Justification-001

- The local webhook section describes two mutually exclusive delivery modes with different required fields, but the authored object shape remains a single undifferentiated schema.
- Without a discriminator, the contract relies on informal interpretation rather than machine-readable branching.

#### Impact Assessment-001

Client SDK generation and validation can accept structurally impossible payloads because the active mode is not declared in-band. That weakens interoperability and forces downstream tools to infer state from incidental field presence.

#### Resolution-001: Option A - Add `webhook_profile` Enum

Introduce a required `webhook_profile` field with a closed enum such as `shared` or `tenant_scoped`, then branch required-field rules from that discriminator. This is additive and keeps the current object boundary intact.

#### Resolution-001: Option B - Split Webhook Objects by Delivery Mode

Replace the current single webhook object with two explicit object definitions and reference the correct one from each call site. This is clearer conceptually, but it duplicates the shared fields and broadens the migration surface.

#### Resolution-001: Option C - Introduce Conditional Profile Contract

Keep the current webhook object but encode the mutually exclusive required-field sets with explicit conditional schema branches tied to a new profile discriminator. This centralizes the constraint without duplicating the shared shape and keeps the contract machine-readable.

#### Comparative Analysis-001

Option A is the smallest additive change, but by itself it still needs conditional enforcement to be complete. Option B is the clearest separation of concepts, yet it duplicates shared fields and raises compatibility costs. Option C preserves a single object surface while still making the profile branch explicit and machine-enforceable.

#### Recommendation-001

**Endorsed Option:** `Option C`

Option C is endorsed because the discriminator keeps the shape additive, localizes the validation branch, and avoids duplicating every common webhook property across multiple object definitions. It delivers the strongest machine-readable closure with a smaller migration surface than a full object split.

#### Supporting Citations-001

- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance on encoding profile-specific required fields with `if`/`then`.
- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance on closing object contracts with explicit properties and `additionalProperties`.

#### Notes-001

If the system later introduces more than two webhook profiles, revisit whether a split registry becomes clearer than stacked conditional branches.

---

### ISSUE-002: Normalize Cursor Pagination Error Semantics

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `Pagination surface` | **Spec Section:** `Cursor Pagination`

#### Problem Statement-002

The pagination contract treats malformed cursors and well-formed but unknown cursors as the same error case. That conflates parse failures with lookup failures and makes client remediation ambiguous.

#### Evidence & Justification-002

- The current prose collapses all cursor failures into one generic client error without distinguishing syntax errors from stale or unknown cursors.
- Those failures have different operational meanings and should not share a single undifferentiated contract.

#### Impact Assessment-002

Clients cannot tell whether to regenerate the request, repair a malformed token, or treat the cursor as expired. Observability also loses a useful signal because parse failures and stale-resource lookups are merged together.

#### Resolution-002: Option A - Use One Generic Client Error

Keep the current single error contract and document that all cursor failures are treated identically. This minimizes change, but it preserves the ambiguity.

#### Resolution-002: Option B - Use `404` for Any Unknown Cursor

Map all cursor failures to `404` and treat the cursor as an addressable resource lookup. This simplifies the status surface, but it blurs malformed input with missing state.

#### Resolution-002: Option C - Separate Parse and Lookup Failures

Return a client-input error for malformed cursors and a distinct stale-or-unknown cursor error for well-formed tokens that no longer resolve. This preserves a narrow status taxonomy while giving clients actionable remediation guidance.

#### Comparative Analysis-002

Option A is stable but uninformative. Option B creates a cleaner single rule than the current prose, yet it still collapses parse and lookup semantics into one bucket. Option C keeps the contract more expressive without requiring a large expansion of status codes or response shapes.

#### Recommendation-002

**Endorsed Option:** `Option C`

Option C is endorsed because it distinguishes malformed client input from a well-formed cursor that no longer resolves, which gives API consumers clearer remediation guidance and produces better operational telemetry. The added contract surface is small compared to the clarity it restores.

#### Supporting Citations-002

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): The primary HTTP semantics reference for differentiating client input problems from other request-processing failures.
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457): Defines a structured error format that works well when parse failures and stale-cursor failures need distinct machine-readable responses.

#### Notes-002

If the API already emits problem-details payloads, reuse that envelope instead of inventing a second error body format.

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue `RESOLVED` until all steps are confirmed.

```plaintext
1. IDENTIFY the issue ID and selected Resolution Option (A/B/C)
2. DRAFT the specific changes to the subject system source document and/or associated schemas
3. VERIFY the draft changes do not introduce new issues (check cross-references in Notes fields)
4. UPDATE the issue entry:
   - Set status: IN_REVIEW
   - Refresh comparative analysis, recommendation, and supporting citations if the ranking changed
5. HUMAN REVIEW of draft changes
6. On approval:
   - Set status: RESOLVED
   - Set resolved: [date]
   - Record resolution: "Option [A|B|C]: [one-line summary]"
7. UPDATE the ISSUE REGISTRY table
8. UPDATE document header metadata (`open_issues`, `resolved_issues`)
```

---

## APPENDIX: CROSS-ISSUE DEPENDENCY MAP

> Issues that share a dependency - resolving one may affect the other.

| Issue | Depends On | Nature of Dependency |
| --- | --- | --- |
| ISSUE-001 | (none) | Root contract defect; independently actionable. |
| ISSUE-002 | ISSUE-001 | If a discriminator is introduced globally, pagination errors should use the same style of explicit, machine-readable branching. |

---

*Example Payments API Issues Tracker — IT-1.1*
*2 issues identified | 0 resolved | Last updated: 2026-03-28*
*Optimized for Google Antigravity 1.21.9 · Gemini 3 Pro Preview · Progressive Disclosure Context Architecture*
