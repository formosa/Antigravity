---
archetype: index
status: active
version: 1.1.0
created: 2026-01-16
updated: 2026-02-15
scope: knowledge-root
index_policy: in_scope_requires_frontmatter
path_convention: knowledge-root-relative
---

# Knowledge Base Index

> Root index for all agent knowledge layers.

## Architecture

The knowledge base is organized into two distinct layers with strict precedence rules:

| Layer | Directory | Scope | Precedence |
| :------ | :---------- | :------ | :----------- |
| **1. Sources** | [`sources/`](sources/_index.md) | Static DDR Framework (Concepts, Protocols, Constraints, Patterns, Vocabulary) | **High** — Canonical |
| **2. Context** | [`context/`](context/_index.md) | Project-Specific Terminology (currently: Maggie) | **Low** — Defers to Sources |

## Precedence Rule

In case of conflict between a Sources definition and a Context definition, the **Sources** definition prevails unless the Context file explicitly documents an intentional project-specific deviation.
