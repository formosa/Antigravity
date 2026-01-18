---
archetype: pattern
status: validated
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
related:
  - patterns/tag_syntax.md
  - patterns/manifest_structure.md
---

# Knowledge Source Template

> **Scope**: Canonical template specification for authoring DDR knowledge source files.
>
> **Excludes**: Tag syntax (see `tag_syntax.md`); manifest structure (see `manifest_structure.md`).

## Summary

All knowledge source files follow a standardized template with minimal YAML frontmatter and archetype-specific body sections. This ensures consistency, enables machine parsing, and reduces authoring friction.

## Structure

### Universal Template

```markdown
---
archetype: concept | protocol | constraint | pattern | vocabulary
status: active | review | validated
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: []
related: []
---

# [Title]

> **Scope**: One-sentence statement of what this source covers.
>
> **Excludes**: What this explicitly does NOT cover.

## Summary

One paragraph for agent context injection.

[Archetype-specific sections...]

---

## References

- `path/to/related.md` — Relationship note
```

## Fields

### Frontmatter (Required)

| Field | Type | Description |
|:------|:-----|:------------|
| `archetype` | enum | One of: concept, protocol, constraint, pattern, vocabulary, context |
| `status` | enum | One of: draft, review, validated |
| `version` | semver | Semantic version (MAJOR.MINOR.PATCH) |
| `created` | date | Creation date (YYYY-MM-DD) |
| `updated` | date | Last modification date |
| `requires` | array | Paths to prerequisite knowledge sources |
| `related` | array | Paths to related knowledge sources |

### Frontmatter (Optional)

| Field | Type | Description | Default |
|:------|:-----|:------------|:--------|
| `tiers` | array | Applicable DDR tiers | all |
| `agents` | array | Relevant agent handles | all |

### Body (Required)

| Section | Description |
|:--------|:------------|
| `# [Title]` | H1 header matching filename |
| `> Scope/Excludes` | Blockquote defining boundaries |
| `## Summary` | Agent-injectable context paragraph |
| `## References` | Cross-references with relationship notes |

---

## Archetype-Specific Sections

### Concept

| Section | Purpose |
|:--------|:--------|
| `## Definition` | Precise, authoritative statement |
| `## Characteristics` | Key properties or attributes |
| `## Context` | When/where this applies |

### Protocol

| Section | Purpose |
|:--------|:--------|
| `## Prerequisites` | What must be true before executing |
| `## Procedure` | Numbered steps with decision points |
| `## Outcomes` | Result table (Success/Failure conditions) |

### Constraint

| Section | Purpose |
|:--------|:--------|
| `## Rule Statement` | Bold MUST/MUST NOT directive |
| `## Rationale` | Why this exists |
| `## Detection` | How to identify violations |
| `## Enforcement` | Violation/severity/resolution table |
| `## Examples` | ✅ Correct and ❌ Incorrect |

### Pattern

| Section | Purpose |
|:--------|:--------|
| `## Structure` | Template with placeholders |
| `## Fields` | Field descriptions table |
| `## Usage Examples` | Basic and complete examples |
| `## Anti-Patterns` | What NOT to do |

### Vocabulary

| Section | Purpose |
|:--------|:--------|
| `## Terms` | Term/Definition/Usage/Avoid table |
| `## Abbreviations` | Abbrev/Expansion/Context table |
| `## Enforcement` | Validation procedure |

---

## Design Principles

1. **Minimal Frontmatter**: Only machine-parseable metadata
2. **Rich Body**: Human-readable content with clear structure
3. **No Redundancy**: Each piece of information appears once
4. **Graceful Defaults**: Omitted optional fields use sensible defaults
5. **Archetype Flexibility**: Core template + archetype variations

---

## References

- `patterns/tag_syntax.md` — RST directive format
- `patterns/manifest_structure.md` — Reconciliation format
- `vocabulary/glossary.md` — Archetype definitions
