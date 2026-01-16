---
archetype: concept
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/tier_brd.md
related:
  - concepts/tier_fsd.md
  - constraints/nfr_numeric_constraints.md
tiers:
  - NFR
agents:
  - nfr_enforcer
---

# Tier: NFR

> **Scope**: Definition, boundaries, and content requirements for the Non-Functional Requirements tier.
>
> **Excludes**: NFR authoring protocols; specific constraint enforcement rules.

## Summary

The NFR (Non-Functional Requirements) is Tier 2 of the DDR hierarchy. It establishes hard constraints and performance targets by answering "What are the system limits?" NFR tags define the boundaries within which all features must operate.

## Definition

The **NFR tier** captures measurable constraints, performance targets, and environmental specifications that limit or shape system behavior. NFRs use RFC 2119 modality (MUST, SHOULD, MAY).

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Boundaries |
| **Question** | "What are the system limits?" |
| **Persona** | SysAdmin |
| **Audience** | Architects, operations, QA |
| **Tag Format** | `NFR-N` (block), `NFR-N.M` (atomic) |

### Key Content

- Hardware environment specifications
- Security and network constraints
- Resource isolation requirements
- Performance targets (latency, throughput)
- Reliability and fault tolerance constraints
- Modality indicators (MUST/SHOULD/MAY)

### Citation Requirements

- NFR tags MUST cite BRD tags that justify each constraint
- Multiple BRD citations allowed for synthesis points

### Modality (RFC 2119)

| Keyword | Meaning |
|:--------|:--------|
| **MUST** | Mandatory requirement |
| **SHOULD** | Recommended practice |
| **MAY** | Optional feature |

### Constraints

| Constraint | Rule |
|:-----------|:-----|
| Numeric Values | All targets must include specific numbers |
| Measurable | Constraints must be testable |
| Justified | Each constraint traces to BRD objective |

## Context

NFR bridges business intent to technical constraints:
- **Cites**: BRD tags
- **Cited by**: FSD, ICD tags
- **File location**: `docs/02_nfr/`

---

## References

- `concepts/tier_brd.md` — Parent tier (context)
- `concepts/tier_fsd.md` — Next tier (behavior)
- `constraints/nfr_numeric_constraints.md` — Numeric values rule
- Source: `ddr_meta_standard.txt` §2.2 Non-Functional Requirements
