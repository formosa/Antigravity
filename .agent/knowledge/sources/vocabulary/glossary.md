---
archetype: vocabulary
status: validated
version: 2.0.0
created: 2026-01-16
updated: 2026-01-18
requires: []
related:
  - ../context/glossary.md
---

# DDR Glossary

> **Scope**: Terminology for the DDR framework and agent operations.
>
> **Excludes**: Project-specific terms (see `context/glossary.md`).

## Summary

DDR controlled vocabulary prevents semantic drift by LLMs. Universal to all DDR projects. Project terminology maintained separately in context layer.

## Terms

| Term | Definition |
|:-----|:-----------|
| **Tag** | Traceable documentation element with unique ID (e.g., `BRD-1.2`) |
| **Citation** | Parent reference via `:links:` directive |
| **Tier** | One of seven DDR abstraction levels (BRD through ISP) |
| **Traceability** | Complete chain of citations from any tag to BRD root |
| **Orphan** | Tag without required parent citation |
| **Manifest** | Reconciliation status block tracking section integrity |
| **Archetype** | Knowledge source type (concept, protocol, constraint, pattern, vocabulary) |

## Abbreviations

| Abbrev | Expansion | Description |
|:-------|:----------|:------------|
| DDR | Development Documentation Roadmap | The documentation framework |
| BRD | Business Requirements Document | Tier 1: Strategic justification |
| NFR | Non-Functional Requirements | Tier 2: Constraints and targets |
| FSD | Feature Specifications Document | Tier 3: System capabilities |
| SAD | System Architecture Document | Tier 4: Structure and patterns |
| ICD | Interface & Contract Definitions | Tier 5: Data schemas |
| TDD | Technical Design Document | Tier 6: Component blueprints |
| ISP | Implementation Stubs & Prompts | Tier 7: Code skeletons |

## Enforcement

1. Scan nouns related to DDR operations
2. Verify against this glossary for framework terms
3. Verify against `context/glossary.md` for project terms
4. Flag unknown terms as errors

---

## References

- Project glossary: `../context/glossary.md`
