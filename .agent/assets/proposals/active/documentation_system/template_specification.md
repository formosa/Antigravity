# Knowledge Source Template Specification

## 1. Adversarial Evaluation of Original Template

### 1.1 Identified Issues

| Issue | Severity | Problem | Resolution |
|:------|:--------:|:--------|:-----------|
| **KS-XXX ID field** | High | Contradicts approved filename-based identification | Remove; derive ID from filename |
| **Title redundancy** | Medium | `title:` in frontmatter AND `# [Title]` header | Remove from frontmatter; derive from H1 |
| **Scope/Boundaries overlap** | High | `scope:` + `excludes:` in frontmatter AND `## Boundaries` section | Consolidate to body section only |
| **Frontmatter bloat** | Medium | 15+ fields increases authoring friction | Reduce to essential machine-parseable fields |
| **Empty sections** | Medium | Template includes all sections; most archetypes need subset | Provide archetype-specific templates |
| **`supersedes: (none)`** | Low | Most files won't supersede anything | Make optional, omit if empty |
| **`tiers: [all]`** | Low | Verbose for common case | Default to "all" if omitted |
| **`validated_by` ambiguous** | Low | `[human|agent]` doesn't identify WHO | Capture validator identity |
| **No creation date** | Medium | Only tracks validation, not authorship | Add `created:` field |
| **Internal comments** | Low | `<!-- VALIDATION NOTES -->` will be copied | Move to separate tracking |

---

## 2. Design Principles

1. **Minimal Frontmatter**: Only machine-parseable metadata that CAN'T be in body
2. **Rich Body**: Human-readable content with clear structure
3. **No Redundancy**: Each piece of information appears ONCE
4. **Graceful Defaults**: Omitted optional fields have sensible defaults
5. **Archetype Flexibility**: Core template + archetype variations

---

## 3. Optimized Universal Template

```markdown
---
archetype: concept | protocol | constraint | pattern | vocabulary
status: draft | review | validated
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD

# Dependencies (paths relative to sources/)
requires: []
related: []

# Applicability (omit entirely if "all")
tiers: []
agents: []
---

# [Title]

> **Scope**: One-sentence statement of what this source covers.
>
> **Excludes**: What this explicitly does NOT cover (with cross-refs).

## Summary

One paragraph for agent context injection. Essential knowledge for quick retrieval.

## Definition

[Primary content - varies by archetype]

---

## References

- `path/to/related.md` — Relationship note
```

---

## 4. Archetype-Specific Templates

### 4.1 Concept

```markdown
---
archetype: concept
status: draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: []
related: []
---

# [Concept Name]

> **Scope**: [What this concept covers]
>
> **Excludes**: [What this does NOT cover]

## Summary

[One paragraph for agent context]

## Definition

[Precise, authoritative definition]

## Characteristics

[Key properties, attributes, or qualities]

## Context

[When/where this applies; relationship to larger system]

---

## References

- [Cross-references]
```

### 4.2 Protocol

```markdown
---
archetype: protocol
status: draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: []
related: []
---

# [Protocol Name]

> **Scope**: [What process this describes]
>
> **Excludes**: [Related processes NOT covered]

## Summary

[One paragraph for agent context]

## Prerequisites

[What must be true before executing]

## Procedure

1. **Step Name**: Description
   - Sub-step if needed
   - Expected outcome

2. **Step Name**: Description
   - Decision point: If X, goto step Y

3. **Step Name**: Final action

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Success | [Criteria] | [What happens] |
| Failure | [Criteria] | [Recovery] |

---

## References

- [Cross-references]
```

### 4.3 Constraint

```markdown
---
archetype: constraint
status: draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: []
related: []
tiers: []
---

# [Constraint Name]

> **Scope**: [What behavior this constrains]
>
> **Excludes**: [Related constraints NOT covered]

## Summary

[One paragraph for agent context]

## Rule Statement

**[TIER-X] MUST/MUST NOT [specific behavior].**

## Rationale

[Why this exists; what problems it prevents]

## Detection

How to identify violations:
- Pattern: `[regex or description]`
- Location: [where to look]

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| [Example] | ERROR | [Fix] |
| [Example] | WARNING | [Fix] |

## Examples

### ✅ Correct
```
[Valid example]
```

### ❌ Incorrect
```
[Invalid example]
```
**Why**: [Explanation]

---

## References

- [Cross-references]
```

### 4.4 Pattern

```markdown
---
archetype: pattern
status: draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: []
related: []
---

# [Pattern Name]

> **Scope**: [What this template covers]
>
> **Excludes**: [Related patterns NOT covered]

## Summary

[One paragraph for agent context]

## Structure

```[format]
[Template with placeholders]
```

## Fields

| Field | Required | Type | Description |
|:------|:--------:|:-----|:------------|
| `field` | Yes | string | [Description] |

## Usage Examples

### Basic
```[format]
[Minimal example]
```

### Complete
```[format]
[Full example]
```

## Anti-Patterns

### ❌ [Name]
```[format]
[What NOT to do]
```
**Problem**: [Why wrong]

---

## References

- [Cross-references]
```

### 4.5 Vocabulary

```markdown
---
archetype: vocabulary
status: draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: []
related: []
---

# [Vocabulary Domain]

> **Scope**: [What terminology this covers]
>
> **Excludes**: [Domains NOT covered]

## Summary

[Purpose of this vocabulary]

## Terms

| Term | Definition | Usage | Avoid |
|:-----|:-----------|:------|:------|
| **Term** | [Definition] | [Correct usage] | [Incorrect synonyms] |

## Abbreviations

| Abbrev | Expansion | Context |
|:-------|:----------|:--------|
| BRD | Business Requirements Document | Tier 1 |

---

## References

- [Cross-references]
```

---

## 5. Template Summary

| Archetype | Key Sections | Purpose |
|:----------|:-------------|:--------|
| **Concept** | Definition, Characteristics, Context | Defines WHAT something IS |
| **Protocol** | Prerequisites, Procedure, Outcomes | Defines HOW to do something |
| **Constraint** | Rule Statement, Detection, Enforcement | Defines MUST/MUST NOT |
| **Pattern** | Structure, Fields, Examples | Provides REUSABLE template |
| **Vocabulary** | Terms table, Abbreviations | Provides NORMATIVE terminology |
