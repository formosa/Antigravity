---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/tier-hierarchy.md
  - protocols/traceability-chain.md
related:
  - patterns/llm-contextual-chunking.md
  - protocols/classification-decision-tree.md
---

# Validation Prompts

> **Scope**: Reusable LLM prompt templates for DDR integrity validation and tier classification.
>
> **Excludes**: Prompt engineering methodology; LLM model selection.

## Summary

Standard prompt templates for the two primary LLM-assisted DDR operations: integrity checking and tier classification. These prompts are designed to be injected into agent context for consistent, repeatable validation.

## Structure

### Integrity Check Prompt

```text
You are validating DDR integrity. Check:
1. Does every :links: reference an existing tag?
2. Does tag_inventory match actual tags?
3. Are there unknown orphans?
4. Do ISP stubs trace to TDD?
```

### Classification Prompt

```text
Given Input X:
1. Business value? -> BRD
2. Constraint? -> NFR
3. Behavior? -> FSD
4. Architecture? -> SAD
5. Schema? -> ICD
```

## Usage Examples

### Basic: Integrity Check
Inject the Integrity Check Prompt with the target documentation section as context. Parse the LLM response for pass/fail per criterion.

### Basic: Classification
Inject the Classification Prompt with the input text. The LLM response indicates the most appropriate tier.

## Anti-Patterns

- Modifying prompts without version-controlling the change
- Using prompts without contextual chunking (see `llm-contextual-chunking.md`)
- Treating LLM classification as authoritative without human review

---

## References

- `protocols/traceability-chain.md` — What integrity checks validate
- `protocols/classification-decision-tree.md` — Deterministic classification
- `patterns/llm-contextual-chunking.md` — Context retrieval for prompts
- Source: `.agent/assets/documentation_system.md` §10.2 Validation Prompts