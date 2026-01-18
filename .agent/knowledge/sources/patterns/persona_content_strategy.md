---
archetype: pattern
status: validated
version: 1.0.0
created: 2026-01-17
updated: 2026-01-17
requires:
  - vocabulary/glossary.md
related:
  - patterns/knowledge_source_template.md
---

# Persona Content Strategy

> **Scope**: Decision criteria for when to inline constraint content vs. use `context_globs` references in persona definitions.
>
> **Excludes**: Persona frontmatter schema (see `antigravity_types.d.ts`).

## Summary

Persona files use a hybrid content strategy: validation/enforcement personas inline critical rules for deterministic access, while authoring/specialist personas reference knowledge sources via `context_globs` for maintainability.

## Structure

### Decision Matrix

| Persona Type | Strategy | Rationale |
|:-------------|:---------|:----------|
| Cross-tier validators | **Inline** | Determinism critical for validation |
| Tier specialists | **Refs only** | Authoring tolerates retrieval latency |
| Utility agents | **Refs only** | Maintenance simplicity preferred |
| Orchestrator | **Refs only** | Delegates to specialists |

## Fields

| Criterion | Inline | Refs Only |
|:----------|:-------|:----------|
| Latency tolerance | Low (validation) | High (authoring) |
| Maintenance priority | Lower | Higher |
| Self-containment | Required | Optional |
| Knowledge sync | Manual | Automatic |

## Usage Examples

### Inline (Validators)

```yaml
# antipattern_scanner.mdc
context_globs:
  - "docs/**/*.rst"
  - ".agent/knowledge/sources/constraints/*.md"
```

Body contains `## EXPERTISE (INLINED RULES)` with hardcoded forbidden terms.

### Refs Only (Specialists)

```yaml
# brd_strategist.mdc
context_globs:
  - "docs/01_brd/*.rst"
  - ".agent/rules/brd_*.md"
  - ".agent/knowledge/sources/concepts/tier_brd.md"
```

Body contains brief constraints referencing knowledge sources.

## Anti-Patterns

### ❌ Inlining in All Personas

**Problem**: Maintenance burden; changes require updating multiple files.

### ❌ Refs Only for Validators

**Problem**: Validation agents need immediate rule access without I/O latency.

---

## References

- `patterns/knowledge_source_template.md` — Template specification
