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
  - patterns/template_new_feature.md
  - constraints/tag_deprecation_lifecycle.md
---

# Template: Bug Fix

> **Scope**: Documentation template for bug fix changes — root cause analysis, tag corrections, and regression testing.
>
> **Excludes**: New feature documentation (see `template_new_feature.md`); deprecation procedures.

## Summary

This template structures the documentation of a bug fix. It captures the affected tier and tag, the before/after correction, the rationale, and a regression test stub.

## Structure

### Root Cause Analysis

```markdown
- **Tier**: [Tier where bug manifests]
- **Tag**: [TAG-ID of affected tag]
- **Root Cause**: [Description of the defect]
```

### Documentation Update

```rst
# BEFORE (Incorrect):
.. [tier]:: [Old Content]
   :id: [TAG-ID]
   :links: [parent-ids]

# AFTER (Corrected):
.. [tier]:: [New Content]
   :id: [TAG-ID]
   :links: [parent-ids]
   .. rationale:: [Explanation of the fix]
```

### Regression Test

```python
def test_bug_[TAG-ID]_regression():
    """Verify that [bug description] does not recur."""
    pass  # ISP stub — no implementation logic
```

## Fields

| Placeholder                | Description                               |
| :------------------------- | :---------------------------------------- |
| `[Tier]`                   | One of: BRD, NFR, FSD, SAD, ICD, TDD, ISP |
| `[TAG-ID]`                 | Existing tag being corrected              |
| `[Old Content]`            | Verbatim content before fix               |
| `[New Content]`            | Corrected content                         |
| `[Explanation of the fix]` | Rationale for the change                  |

## Anti-Patterns

- Deleting the old tag instead of correcting it
- Renumbering the tag ID during correction
- Omitting the regression test stub

---

## References

- `patterns/template_new_feature.md` — New feature template
- `constraints/tag_deprecation_lifecycle.md` — Tag preservation rules
- `patterns/tag_syntax.md` — Tag format
- Source: `.agent/assets/documentation_system.md` §22.2 Template: Bug Fix