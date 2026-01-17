---
type: rule
name: "DDR ID Immutability"
globs:
  - "docs/**/*.rst"
priority: 100
trigger:
  - "rename"
  - "renumber"
  - "id"
severity: mandatory
description: "Tag IDs are immutable database keys. Never allow renumbering or reuse of deleted IDs."
---
# DDR ID Immutability Rule

## Rule Statement

**ALL TIERS: Tag IDs MUST remain immutable once assigned.**

## Rationale

Immutable IDs prevent cascading reference updates across the entire document hierarchy when items are added, removed, or reordered. Citations remain valid regardless of document restructuring.

## Detection

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

## Enforcement Protocol

1. Never allow renumbering of existing tags
2. Never allow reuse of deleted tag IDs
3. Only permit sequential ID appending
4. DEPRECATED markers allowed, original ID preserved

## Examples

### ✅ Correct

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

```
- Item A |BRD-5.1|
- Item C |BRD-5.2|         ← WRONG: ID changed from 5.3
```

## References

- Knowledge: `constraints/tag_immutability.md`
- Source: DDR Meta-Standard §3.3
