---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/tier_hierarchy.md
  - patterns/tag_syntax.md
related:
  - patterns/worked_example_feature.md
  - protocols/workflow_document_feature.md
---

# Template: New Feature

> **Scope**: Copy-paste starter template for documenting a new feature across all 7 DDR tiers.
>
> **Excludes**: Template for bug fixes (see `template_bug_fix.md`); tag syntax details (see `tag_syntax.md`).

## Summary

This template provides the minimal scaffolding for a complete 7-tier feature documentation chain. Replace bracketed placeholders with actual content. Each tier's `:links:` follows the citation matrix exactly.

## Structure

```rst
.. brd:: [Feature Name]
   :id: BRD-X
   [Business Value — measurable, no technology]

.. nfr:: [Constraint Name]
   :id: NFR-X
   :links: BRD-X
   [Quantifiable target — numeric values required]

.. fsd:: [Behavior Name]
   :id: FSD-X
   :links: NFR-X, BRD-X
   [What the system does — no implementation]

.. sad:: [Pattern Name]
   :id: SAD-X
   :links: FSD-X, NFR-X
   [Architecture decisions — components, topology]

.. icd:: [Schema Name]
   :id: ICD-X
   :links: SAD-X
   [Data contract — JSON/YAML schema]

.. tdd:: [Component Name]
   :id: TDD-X
   :links: SAD-X, ICD-X
   [Class blueprint — methods, signatures]

.. isp:: [Stub Name]
   :id: ISP-X
   :links: TDD-X
   [Code skeleton — pass only, NumPy docstrings]
```

## Fields

| Placeholder | Description | Constraint |
| :------------ | :------------ | :----------- |
| `[Feature Name]` | Business-facing feature title | No technology terms |
| `BRD-X` | Unique BRD tag ID | Immutable once assigned |
| `[Business Value]` | ROI, strategic justification | Measurable metrics required |
| `NFR-X` through `ISP-X` | Sequential tier IDs | Must follow citation matrix |

## Anti-Patterns

- Skipping tiers (e.g., BRD → SAD without NFR/FSD)
- Using technology terms in BRD
- Omitting `:links:` directive
- Putting implementation logic in ISP stubs

---

## References

- `patterns/tag_syntax.md` — Tag ID format
- `patterns/worked_example_feature.md` — Complete worked example
- `protocols/workflow_document_feature.md` — Step-by-step workflow
- Source: `.agent/assets/documentation_system.md` §22.1 Template: New Feature
