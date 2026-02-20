---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/metadata_schema.md
related:
  - sources/patterns/knowledge_source_template.md
---

# Source Citation Style

> **Scope**: Standard syntax for provenance citations in DDR knowledge documents.
> **Excludes**: Citation topology between DDR tags (`:links:`).

## Summary

All provenance references must resolve to concrete repository paths and stable section identifiers.

## Structure

### Canonical Form

- Source: `.agent/assets/documentation_system.md` §X (Section Title), §X.Y

### Rules

1. Repository path is mandatory.
2. Section number is mandatory when available.
3. Section title is recommended for human readability.
4. Free-text source titles without path are prohibited.

### Examples

✅ Correct:

- Source: `.agent/assets/documentation_system.md` §5 (Vertical Abstraction & Specification Protocols), §5.2

❌ Incorrect:

- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.2

---

## References

- `sources/patterns/metadata_schema.md` — Validation contract