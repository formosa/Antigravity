---
archetype: constraint
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
related:
  - constraints/tag_citation_required.md
  - protocols/abstraction_lateral.md
---

# Sibling Prohibition

> **Scope**: Rule that tags cannot cite peer tags within the same tier block.
>
> **Excludes**: Parent-child citations; cross-tier citations.

## Summary

Sub-atomic tags within the same block-level parent are peers, not hierarchical dependencies. Citations are strictly for vertical (cross-layer) justification. Block membership already establishes grouping—sibling citations are redundant and create false dependencies.

## Rule Statement

**ALL TIERS: Tags MUST NOT cite peer tags at the same abstraction level.**

## Rationale

- Citations establish **vertical** justification (why this exists)
- Sibling relationships are **horizontal** (related concerns at same level)
- Block membership already groups related items
- Sibling citations create tangled dependencies that complicate refactoring

## Detection

How to identify violations:

| Pattern | Example |
|:--------|:--------|
| Same prefix in `:links:` | FSD-4.4 links to FSD-4.3 |
| Same block parent | Both tags under FSD-4 |
| Sequential dependency | "This follows from..." sibling |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Sibling citation | ERROR | Remove sibling link |
| Sequential dependency | WARNING | Express in prose, not citation |

## Examples

### ✅ Correct

```rst
.. fsd:: Error Handling Strategy
   :id: FSD-7
   :links: BRD-2, NFR-5

.. fsd:: LogServer Fault handling
   :id: FSD-7.1
   :links: FSD-7             ← Cites block parent, not siblings

.. fsd:: Service Fault handling
   :id: FSD-7.2
   :links: FSD-7             ← Same: cites block parent
```

Express sequential relationships in prose:
```rst
.. fsd:: VAD (Stage 2): Neural VAD refines Stage 1 output.
   :id: FSD-4.4
   :links: FSD-4             ← Cites parent block
```

### ❌ Incorrect

```rst
.. fsd:: VAD (Stage 2): Refines Stage 1.
   :id: FSD-4.4
   :links: FSD-4.3           ← WRONG: Sibling citation
```
**Why**: FSD-4.3 and FSD-4.4 are peers under FSD-4. Sequential relationship should be expressed in text content, not citation.

```rst
.. nfr:: Memory limit.
   :id: NFR-1.3
   :links: NFR-1.2           ← WRONG: Sibling citation
```
**Why**: NFR-1.2 and NFR-1.3 are both atomic items under NFR-1.

---

## References

- `concepts/tier_hierarchy.md` — Vertical structure
- `protocols/abstraction_lateral.md` — Proper sibling generation
- Source: `ddr_meta_standard.txt` §3.6 Lateral Dependency Prohibition
