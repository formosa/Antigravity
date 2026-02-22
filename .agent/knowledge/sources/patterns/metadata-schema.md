---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/knowledge-source-template.md
related:
  - sources/patterns/source-citation-style.md
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

### Optional Frontmatter Fields

- requires
- related
- tags

### Status Enum

- draft
- review
- active
- deprecated

### Path Rules

- Paths MUST be knowledge-root-relative (`sources/...`, `context/...`).
- Relative parent navigation (`../`) is prohibited.

### Index Rule

- `index.md` files MUST carry the exact frontmatter for `IndexDefinition` (including optional fields like `scope`, `index_policy`, `path_convention`, `project`, `context_mode`).
- `index.md` files act as programmatic routing layers and MUST NOT contain human documentation. They explicitly point the agent to `README.md` (e.g., "Refer to README.md for conceptual content").
- `README.md` files are strictly for human prose and MUST NOT contain YAML frontmatter.

---

## References

- `sources/patterns/knowledge-source-template.md` — Authoring template