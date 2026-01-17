---
type: rule
name: "Trace Complete Chain"
globs:
  - "docs/**/*.rst"
priority: 90
trigger:
  - "orphan"
  - "chain"
  - "traceability"
severity: mandatory
description: "Every tag must have a complete traceability chain to BRD root."
---
# Trace Complete Chain Rule

## Rule Statement

**ALL TIERS: Every tag (except BRD) MUST have a complete, unbroken citation chain to a BRD tag.**

## Detection

| Violation | How to Detect |
|:----------|:--------------|
| Orphan | Tag has no `:links:` directive |
| Broken chain | Parent tag is itself an orphan |
| Missing parent | Cited tag does not exist |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Orphan tag | ERROR | Add parent citation |
| Broken chain | ERROR | Fix upstream orphan first |
| Missing parent | ERROR | Create parent or fix reference |

## Chain Validation

Recurse upward through `:links:` until reaching BRD:

```
ISP-3.1 → TDD-3 → SAD-2 → FSD-1.3 → BRD-5.2 ✅
ICD-5 → (none) ❌ ORPHAN
```

## Validation Algorithm

```python
def validate_complete_chain(tag_id, documentation):
    visited = set()
    current = tag_id
    chain = [current]

    while not current.startswith("BRD"):
        if current in visited:
            return {"valid": False, "error": "CIRCULAR_DEPENDENCY"}
        visited.add(current)
        parents = extract_citations(documentation[current])
        if not parents:
            return {"valid": False, "error": "BROKEN_CHAIN", "orphan": current}
        current = parents[0]
        chain.append(current)

    return {"valid": True, "chain": chain}
```

## References

- Knowledge: `protocols/traceability_chain.md`
- Source: DDR Meta-Standard §4.1
