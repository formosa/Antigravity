---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/tier-hierarchy.md
  - concepts/information-flow.md
related:
  - patterns/llm-validation-prompts.md
---

# Contextual Chunking

> **Scope**: Pattern for retrieving DDR context within LLM token limits.
>
> **Excludes**: Full document retrieval; embedding strategies.

## Summary

When the full DDR exceeds LLM context windows, hierarchical retrieval with tag-based indexing provides focused context. This pattern retrieves a target tag plus its immediate lineage (ancestors and children) to maximize relevance while minimizing token usage.

## Structure

### Algorithm

1. **Retrieve Target Tag**: Load the specific tag and its metadata.
2. **Fetch Ancestors**: Traverse `:links:` upward (depth limit: 2 levels).
3. **Fetch Children**: Traverse citations downward (depth limit: 2 levels).
4. **Assemble Context**: Result contains full lineage without noise.

### Parameters

| Parameter          | Default   | Description                     |
| :----------------- | :-------- | :------------------------------ |
| `ancestor_depth`   | 2         | Levels to traverse upward       |
| `child_depth`      | 2         | Levels to traverse downward     |
| `include_siblings` | false     | Include peer tags at same level |

## Anti-Patterns

- Loading the entire DDR into context (token overflow)
- Retrieving only the target tag (insufficient context)
- Ignoring depth limits (unbounded traversal)

---

## References

- `concepts/information-flow.md` — Citation and cascade principles
- `patterns/llm-validation-prompts.md` — Prompt templates for LLM validation
- Source: `.agent/assets/documentation_system.md` §10.1 Contextual Chunking