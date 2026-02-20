---
archetype: index
status: active
version: 1.1.0
created: 2026-01-16
updated: 2026-02-15
scope: context-index
project: antigravity
context_mode: namespaced
---

# Project Context Index

> Project-specific terminology for DDR agent operations.
>
> **Project**: Maggie (AI Assistant Framework)
>
> **Layer**: Project-Specific Context (scoped to one documentation project)
>
> **Parent index**: [`knowledge/README.md`](../README.md) · **Sibling**: [`sources/README.md`](../sources/README.md)

## Files

| File | Purpose |
| :----- | :-------- |
| [glossary.md](glossary.md) | Project terms and abbreviations |

## Precedence

Context definitions defer to DDR Source definitions in case of conflict, unless an intentional project-specific deviation is explicitly documented here.

## Context Namespace Policy

Context files are project-scoped overlays and MUST declare their namespace.

- `context/glossary.md` is currently retained for Maggie terminology compatibility.
- Future contexts SHOULD split by namespace (e.g., `maggie_*`, `antigravity_*`) to avoid semantic bleed.
