---
archetype: concept
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/tier_nfr.md
related:
  - concepts/tier_sad.md
  - constraints/fsd_no_implementation.md
tiers:
  - FSD
agents:
  - fsd_analyst
---

# Tier: FSD

> **Scope**: Definition, boundaries, and content requirements for the Feature Specifications Document tier.
>
> **Excludes**: FSD authoring protocols; specific constraint enforcement rules.

## Summary

The FSD (Feature Specifications Document) is Tier 3 of the DDR hierarchy. It defines system capabilities and user-facing behavior by answering "What does the system do?" FSD translates business requirements and constraints into concrete functional specifications.

## Definition

The **FSD tier** captures what the system does from a user/stakeholder perspective—capabilities, behaviors, workflows, and interaction patterns—without specifying implementation details.

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Behavior |
| **Question** | "What does the system do?" |
| **Persona** | Product Owner |
| **Audience** | Product managers, UX designers, architects |
| **Tag Format** | `FSD-N` (block), `FSD-N.M` (atomic) |

### Key Content

- System capabilities
- Process orchestration
- State machine definitions
- Voice/user interaction pipelines
- Error handling strategies
- User experience requirements

### Citation Requirements

- FSD tags MUST cite BRD and/or NFR tags that establish the need
- Multiple parent citations allowed

### Constraints

| Constraint | Rule |
|:-----------|:-----|
| No Implementation | No code, algorithms, or class structures |
| Behavior Focus | Describe WHAT happens, not HOW |
| User Perspective | Frame from user/stakeholder viewpoint |
| Testable | Behaviors must be verifiable |

## Context

FSD is the pivotal tier between business and technical:
- **Cites**: BRD, NFR tags
- **Cited by**: SAD tags
- **File location**: `docs/03_fsd/`

---

## References

- `concepts/tier_nfr.md` — Parent tier (boundaries)
- `concepts/tier_sad.md` — Next tier (structure)
- `constraints/fsd_no_implementation.md` — No code rule
- Source: `ddr_meta_standard.txt` §2.3 Feature Specifications Document
