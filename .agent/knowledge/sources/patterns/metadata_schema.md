---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/knowledge_source_template.md
related:
  - sources/patterns/source_citation_style.md
  - sources/vocabulary/glossary.md
---

# Metadata Schema

> **Scope**: Canonical machine-validation schema for DDR knowledge files.
> **Excludes**: Semantic correctness of domain statements.

## Summary

Defines normative frontmatter fields, enums, and scope classes used by validation tooling.

## Structure

### In-Scope Archetypes

- concept
- protocol
- constraint
- pattern
- vocabulary
- context
- index

### Required Frontmatter Fields

- archetype
- status
- version
- created
- updated
- requires
- related

### Status Enum

- draft
- review
- active
- deprecated

### Path Rules

- Paths MUST be knowledge-root-relative (`sources/...`, `context/...`).
- Relative parent navigation (`../`) is prohibited.

### Index Rule

`_index.md` files are in-scope and MUST carry frontmatter with `archetype: index`.

---

## References

- `sources/patterns/knowledge_source_template.md` — Authoring template
