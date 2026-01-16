---
archetype: concept
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/tier_fsd.md
related:
  - concepts/tier_icd.md
tiers:
  - SAD
agents:
  - sad_architect
---

# Tier: SAD

> **Scope**: Definition, boundaries, and content requirements for the System Architecture Document tier.
>
> **Excludes**: SAD authoring protocols; specific constraint enforcement rules.

## Summary

The SAD (System Architecture Document) is Tier 4 of the DDR hierarchy. It defines high-level organization and patterns by answering "How is the system structured?" SAD translates behavioral requirements into architectural decisions.

## Definition

The **SAD tier** captures architectural patterns, process topology, integration strategies, and structural organization—the "shape" of the system without component-level implementation details.

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Structure |
| **Question** | "How is the system organized?" |
| **Persona** | Architect |
| **Audience** | Technical leads, senior developers |
| **Tag Format** | `SAD-N` (block), `SAD-N.M` (atomic) |

### Key Content

- Architectural patterns (Hub-and-Spoke, etc.)
- Process topology
- Integration strategies
- Concurrency model
- Configuration strategy
- ASCII topology diagrams (mandatory)

### Citation Requirements

- SAD tags MUST cite FSD tags that define behaviors being structured
- May also cite NFR for constraint-driven decisions

### Diagram Requirement

ASCII topology diagrams are **mandatory** for SAD sections:

```
+---------------+          +------------------+          +-----------------+
|  UI (DEALER)  | <------> |   Core (ROUTER)  | <------> | Runtime (DEALER)|
+---------------+          +------------------+          +-----------------+
```

## Context

SAD bridges behavioral requirements to technical design:
- **Cites**: FSD tags (primarily), NFR tags (for constraints)
- **Cited by**: ICD, TDD tags
- **File location**: `docs/04_sad/`

---

## References

- `concepts/tier_fsd.md` — Parent tier (behavior)
- `concepts/tier_icd.md` — Next tier (contracts)
- Source: `ddr_meta_standard.txt` §2.4 System Architecture Document
