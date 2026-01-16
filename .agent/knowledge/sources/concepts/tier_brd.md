---
archetype: concept
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
related:
  - concepts/tier_nfr.md
  - constraints/brd_technology_agnostic.md
  - constraints/brd_measurable_metrics.md
tiers:
  - BRD
agents:
  - brd_strategist
---

# Tier: BRD

> **Scope**: Definition, boundaries, and content requirements for the Business Requirements Document tier.
>
> **Excludes**: BRD authoring protocols; specific constraint enforcement rules.

## Summary

The BRD (Business Requirements Document) is Tier 1 of the DDR hierarchy. It establishes strategic justification by answering "Why are we building this system?" BRD tags are the root authority—the only tags that require no parent citations.

## Definition

The **BRD tier** captures business context, strategic objectives, and success criteria in technology-agnostic language. It defines the problem space and value proposition without specifying solutions.

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Context |
| **Question** | "Why are we building this?" |
| **Persona** | Strategist |
| **Audience** | Stakeholders, executives, product leadership |
| **Tag Format** | `BRD-N` (block), `BRD-N.M` (atomic) |

### Key Content

- Project purpose and identity
- Strategic objectives
- Problem statement
- High-level scope
- Success criteria (measurable)
- Target stakeholders

### Downstream Authority

All NFR and FSD tags MUST cite specific BRD tags as their ultimate justification.

### Constraints

| Constraint | Rule |
|:-----------|:-----|
| Technology Agnostic | No technology terms (ZeroMQ, Python, GPU) |
| Measurable Metrics | Success criteria must be quantifiable |
| Stakeholder Focus | Identify benefiting stakeholders |
| No Implementation | Describe WHAT to achieve, not HOW |

## Context

BRD is the foundation of all documentation:
- **Citing BRD**: NFR and FSD tiers cite BRD directly
- **No citations**: BRD tags have no parent (root authority)
- **File location**: `docs/01_brd/`

---

## References

- `concepts/tier_hierarchy.md` — Position in seven-tier structure
- `concepts/tier_nfr.md` — Next tier (boundaries)
- `constraints/brd_technology_agnostic.md` — No tech terms rule
- Source: `ddr_meta_standard.txt` §2.1 Business Requirements Document
