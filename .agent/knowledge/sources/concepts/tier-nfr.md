---
archetype: concept
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier-hierarchy.md
  - concepts/tier-brd.md
related:
  - concepts/tier-fsd.md
  - constraints/nfr-numeric-constraints.md
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

| Attribute      | Value                               |
| :------------- | :---------------------------------- |
| **Layer**      | Boundaries                          |
| **Question**   | "What are the system limits?"       |
| **Persona**    | SysAdmin                            |
| **Audience**   | Architects, operations, QA          |
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

| Keyword    | Meaning               |
| :--------- | :-------------------- |
| **MUST**   | Mandatory requirement |
| **SHOULD** | Recommended practice  |
| **MAY**    | Optional feature      |

### Constraints

| Constraint     | Rule                                      |
| :------------- | :---------------------------------------- |
| Numeric Values | All targets must include specific numbers |
| Measurable     | Constraints must be testable              |
| Justified      | Each constraint traces to BRD objective   |

## Context

NFR bridges business intent to technical constraints:

- **Cites**: BRD tags
- **Cited by**: FSD, ICD tags
- **File location**: `docs/02_nfr/`

---

## References

- `concepts/tier-brd.md` — Parent tier (context)
- `concepts/tier-fsd.md` — Next tier (behavior)
- `constraints/nfr-numeric-constraints.md` — Numeric values rule
- Source: `.agent/assets/documentation_system.md` §2.2 Non-Functional Requirements