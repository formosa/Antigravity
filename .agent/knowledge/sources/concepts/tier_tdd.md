---
archetype: concept
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/tier_icd.md
related:
  - concepts/tier_isp.md
tiers:
  - TDD
agents:
  - tdd_designer
---

# Tier: TDD

> **Scope**: Definition, boundaries, and content requirements for the Technical Design Document tier.
>
> **Excludes**: TDD authoring protocols; specific constraint enforcement rules.

## Summary

The TDD (Technical Design Document) is Tier 6 of the DDR hierarchy. It defines component structure without implementation logic by answering "What classes/modules exist?" TDD provides the blueprint for code organization.

## Definition

The **TDD tier** captures component class names, dependencies, socket configurations, state management structures, and interface contracts—defining WHAT exists and HOW it's wired, but NOT the implementation logic.

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Blueprints |
| **Question** | "What classes/modules exist?" |
| **Persona** | Lead Developer |
| **Audience** | Developers, code reviewers |
| **Tag Format** | `TDD-N` (block), `TDD-N.M` (atomic) |

### Key Content

- Component class names
- Dependencies (imports)
- Socket configurations
- State management structures
- Concurrency strategies
- Interface contracts (abstract methods)

### Citation Requirements

- TDD tags MUST cite SAD (structure) and ICD (contracts) tags
- Every structural element traces to architectural decision

### Critical Rule

TDD defines **WHAT exists** and **HOW it's wired**, NOT the logic:

| ✅ TDD Content | ❌ Not TDD Content |
|:---------------|:-------------------|
| Class names | Algorithm implementations |
| Method signatures | Business logic |
| Dependencies | Control flow |
| Socket bindings | Message handling code |

## Context

TDD is the final design layer before code:
- **Cites**: SAD tags, ICD tags
- **Cited by**: ISP tags
- **File location**: `docs/06_tdd/`

---

## References

- `concepts/tier_icd.md` — Parent tier (contracts)
- `concepts/tier_isp.md` — Next tier (prompts)
- Source: `ddr_meta_standard.txt` §2.6 Technical Design Document
