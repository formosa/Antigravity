---
archetype: constraint
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - vocabulary/glossary.md
  - constraints/tag_immutability.md
related:
  - constraints/tag_citation_required.md
---

# Tag Deprecation Lifecycle

> **Scope**: Rules governing tag deprecation — never delete, never renumber, maintain legacy citations.
>
> **Excludes**: Tag creation rules; citation chain validation.

## Summary

Tags are permanent database keys. They may be deprecated but never deleted or renumbered. Deprecated tags remain valid citation parents for legacy nodes to prevent chain breakage.

## Rule Statement

**Tags MUST NOT be deleted or renumbered. Deprecated tags MUST retain their `:links:` validity.**

## Rationale

Deleting or renumbering tags would break all downstream citations, causing cascading orphans across the documentation graph. Tag IDs function as immutable keys in a relational model.

## Detection

| Check | Method |
| :------ | :------- |
| Deleted tag | Tag ID referenced in `:links:` but not found in documentation |
| Renumbered tag | Two tags with identical content, different IDs |
| Broken legacy chain | Deprecated parent no longer resolves |

## Enforcement

| Violation | Severity | Resolution |
| :---------- | :--------- | :----------- |
| Tag deleted | ERROR | Restore tag with `[DEPRECATED vX.Y]` marker |
| Tag renumbered | ERROR | Revert to original ID, deprecate if needed |
| Legacy chain broken | WARNING | Verify deprecated parent still exists |

## Examples

✅ **Correct**:

```rst
.. brd:: Original Feature [DEPRECATED v2.1]
   :id: BRD-3
```

❌ **Incorrect**:

```rst
# BRD-3 deleted, BRD-3 content moved to BRD-7
```

### Transitions

| From | To | Action |
| :----- | :--- | :------- |
| Active | Deprecated | Mark `[DEPRECATED vX.Y]`, create replacement with new ID |
| Deprecated | Removed | Sunsetting — only after confirming zero downstream citations |

---

## References

- `constraints/tag_immutability.md` — ID immutability rule
- `constraints/tag_citation_required.md` — Citation mandate
- Source: `documentation_system.md` §15.1 Tag Deprecation
