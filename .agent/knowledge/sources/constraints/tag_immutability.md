---
archetype: constraint
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
related:
  - constraints/tag_citation_required.md
  - patterns/tag_syntax.md
---

# Tag Immutability

> **Scope**: Rule that tag IDs are permanent identifiers that never change or get reused.
>
> **Excludes**: Tag syntax format; citation requirements.

## Summary

Tag IDs are database keys, not ordinal positions. Once a tag ID is assigned, it permanently identifies that specific requirement or design element. IDs are never re-sequenced, recycled, or modified.

## Rule Statement

**ALL TIERS: Tag IDs MUST remain immutable once assigned.**

## Rationale

Immutable IDs prevent cascading reference updates across the entire document hierarchy when items are added, removed, or reordered. Citations remain valid regardless of document restructuring.

## Detection

How to identify violations:

| Pattern | Violation Type |
|:--------|:---------------|
| ID renumbered after deletion | Re-sequencing |
| Deleted ID assigned to new tag | Recycling |
| ID format changed (BRD-1 → BRD-001) | Format mutation |
| Tag moved, ID changed to fit sequence | Reordering |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Re-sequenced IDs | ERROR | Restore original IDs |
| Recycled deleted ID | ERROR | Mint new ID |
| Format mutation | WARNING | Standardize format |

## Examples

### ✅ Correct

Initial state:
```
- Item A |BRD-5.1|
- Item B |BRD-5.2|
- Item C |BRD-5.3|
```

After deleting Item B:
```
- Item A |BRD-5.1|
- Item C |BRD-5.3|         ← ID preserved
```

After inserting new item:
```
- Item A |BRD-5.1|
- New Item |BRD-5.4|       ← Next available ID
- Item C |BRD-5.3|
```

### ❌ Incorrect

After deleting Item B:
```
- Item A |BRD-5.1|
- Item C |BRD-5.2|         ← WRONG: ID changed from 5.3
```

After inserting new item:
```
- Item A |BRD-5.1|
- New Item |BRD-5.2|       ← WRONG: Reused deleted ID
- Item C |BRD-5.3|
```

**Why**: Re-sequencing or recycling breaks all downstream citations to the modified IDs.

---

## References

- `patterns/tag_syntax.md` — ID format specification
- Source: `ddr_meta_standard.txt` §3.3 Tag Lifecycle & Stability Rules
