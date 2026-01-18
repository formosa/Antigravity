---
archetype: constraint
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
related:
  - constraints/sibling_prohibition.md
  - protocols/traceability_chain.md
---

# Tag Citation Required

> **Scope**: Rule that every tag (except BRD root) must cite at least one parent tag.
>
> **Excludes**: Sibling citation rules; citation format syntax.

## Summary

Every design artifact must cite the requirement(s) that justify its existence. This creates complete traceability from any implementation detail back to business objectives. Only BRD tags (root authority) are exempt.

## Rule Statement

**ALL TIERS (except BRD): Every tagged item MUST have at least one parent citation via the `:links:` directive.**

## Rationale

Parent citations ensure every documentation element has explicit justification. This enables:
- Audit trails from code to business value
- Impact analysis when requirements change
- Orphan detection for unjustified content

## Detection

How to identify violations:

| Pattern | Location |
|:--------|:---------|
| Missing `:links:` directive | Any non-BRD tag |
| Empty `:links:` value | `:links:` with no content |
| Invalid parent reference | `:links:` pointing to non-existent tag |

```rst
.. fsd:: Some Feature
   :id: FSD-5
   (no :links: directive)    ← VIOLATION
```

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Missing `:links:` | ERROR | Add parent citation |
| Empty `:links:` | ERROR | Specify parent tag(s) |
| Invalid parent | ERROR | Fix reference or create parent |
| BRD with `:links:` | WARNING | Remove (BRD is root) |

## Examples

### ✅ Correct

```rst
.. nfr:: Response latency must be under 1 second.
   :id: NFR-4.1
   :links: BRD-5.2

.. sad:: Hub-and-Spoke messaging pattern.
   :id: SAD-1.1
   :links: FSD-1.1

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
**Why**: No justification for why this feature exists.

```rst
.. tdd:: RuntimeProcess class.
   :id: TDD-3
   :links:
```
**Why**: Empty links directive provides no traceability.

---

## References

- `concepts/tier_hierarchy.md` — Valid citation hierarchy
- `protocols/traceability_chain.md` — Chain validation
- Source: `ddr_meta_standard.txt` §4.1 Upstream Citation Mandates
