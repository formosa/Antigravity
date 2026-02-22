# Knowledge Base Index

> Root index for all agent knowledge layers.

## Architecture

The knowledge base is organized into two distinct layers with strict precedence rules:

| Layer          | Directory                       | Scope                                                                         | Precedence                  |
| :------------- | :------------------------------ | :---------------------------------------------------------------------------- | :-------------------------- |
| **1. Sources** | [`sources/`](sources/README.md) | Static DDR Framework (Concepts, Protocols, Constraints, Patterns, Vocabulary) | **High** — Canonical        |
| **2. Context** | [`context/`](context/README.md) | Project-Specific Terminology (currently: Maggie)                              | **Low** — Defers to Sources |

## Precedence Rule

In case of conflict between a Sources definition and a Context definition, the **Sources** definition prevails unless the Context file explicitly documents an intentional project-specific deviation.

## Naming Conventions

To align Python standards with Antigravity standards, this repository uses a hybrid naming policy:

- **Python code assets** (`.py` modules/packages): use `snake_case`.
- **Antigravity configuration assets** (`.agent/rules`, `.agent/workflows`, `.agent/personas`, `.agent/skills`): use `kebab-case`.
- **Skill static docs/assets**: prefer `resources/` over legacy `references/` for Antigravity v1.16.5 compatibility.
