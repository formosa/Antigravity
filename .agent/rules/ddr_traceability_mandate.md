---
type: rule
name: "DDR Traceability Mandate"
globs:
  - "docs/**/*.rst"
priority: 60
trigger:
  - "tag"
  - "citation"
  - "parent"
severity: mandatory
description: "Every tag must cite parent (except BRD root). Enforces complete traceability chains."
---
# DDR Traceability Mandate Rule

## Rule Statement

**ALL TIERS (except BRD): Every tagged item MUST have at least one parent citation via the `:links:` directive.**

## Rationale

Parent citations ensure every documentation element has explicit justification:
- Audit trails from code to business value
- Impact analysis when requirements change
- Orphan detection for unjustified content

## Detection

| Pattern | Location |
|:--------|:---------|
| Missing `:links:` directive | Any non-BRD tag |
| Empty `:links:` value | `:links:` with no content |
| Invalid parent reference | `:links:` pointing to non-existent tag |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Missing `:links:` | ERROR | Add parent citation |
| Empty `:links:` | ERROR | Specify parent tag(s) |
| Invalid parent | ERROR | Fix reference or create parent |
| BRD with `:links:` | WARNING | Remove (BRD is root) |

## Enforcement Protocol

1. Check if tag has `:links:` directive
2. Verify cited parent exists
3. Flag orphans for resolution
4. Reject tag creation if validation fails

## Examples

### ✅ Correct

```rst
.. nfr:: Response latency must be under 1 second.
   :id: NFR-4.1
   :links: BRD-5.2

.. tdd:: CoreProcess class structure.
   :id: TDD-1
   :links: SAD-2, ICD-1
```

### ❌ Incorrect

```rst
.. fsd:: Voice interaction pipeline.
   :id: FSD-4
   (no :links:)
```

## References

- Knowledge: `constraints/tag_citation_required.md`
- Source: DDR Meta-Standard §4.1
