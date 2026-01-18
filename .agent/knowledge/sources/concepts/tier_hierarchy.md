---
archetype: concept
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/ddr_overview.md
related:
  - concepts/information_flow.md
  - concepts/tier_brd.md
  - concepts/tier_nfr.md
  - concepts/tier_fsd.md
  - concepts/tier_sad.md
  - concepts/tier_icd.md
  - concepts/tier_tdd.md
  - concepts/tier_isp.md
---

# Tier Hierarchy

> **Scope**: The seven-tier structure, layer relationships, and validation hierarchy of the DDR.
>
> **Excludes**: Individual tier definitions (see `tier_*.md`); classification protocols.

## Summary

The DDR organizes documentation into seven tiers arranged in a strict causal hierarchy. Each tier answers a specific question, is authored by a specific persona, and cites parent tiers for justification. Information flows downward from BRD to ISP; traceability flows upward.

## Definition

The **tier hierarchy** is the seven-layer structure that organizes all DDR documentation from strategic business intent (BRD) to executable code skeletons (ISP).

## Characteristics

### The Seven Tiers

| Tier | Name | Layer | Question Answered | Persona |
|:----:|:-----|:------|:------------------|:--------|
| 1 | BRD | Context | "Why build it?" | Strategist |
| 2 | NFR | Boundaries | "What limits?" | SysAdmin |
| 3 | FSD | Behavior | "What does it?" | Product Owner |
| 4 | SAD | Structure | "How organize?" | Architect |
| 5 | ICD | Contracts | "What shape?" | Data Engineer |
| 6 | TDD | Blueprints | "What classes?" | Lead Developer |
| 7 | ISP | Prompts | "What stubs?" | Code Generator |

### Validation Hierarchy

Each tier cites its authority from specific parent tiers:

```
BRD (Root Authority)
 ↓
NFR ← BRD
 ↓
FSD ← BRD, NFR
 ↓
SAD ← FSD
 ↓
ICD ← SAD, NFR
 ↓
TDD ← SAD, ICD
 ↓
ISP ← TDD
```

### Critical Rules

1. **No forward references**: A tier cannot cite a lower tier (TDD cannot cite ISP)
2. **No skipping**: SAD cannot cite BRD directly; it must cite via FSD
3. **Root exception**: Only BRD tags have no parent citations
4. **Cross-layer only**: Citations connect tiers, not siblings within a tier

## Context

The tier hierarchy is the organizing principle for:

- **Classification**: Determining which tier owns new information
- **Validation**: Ensuring complete traceability chains
- **Agent routing**: Directing tasks to tier-specialist personas
- **Document structure**: Physical file organization in `docs/` mirrors tiers

---

## References

- `concepts/ddr_overview.md` — DDR foundational principles
- `concepts/information_flow.md` — Citation and cascade mechanics
- Source: `ddr_meta_standard.txt` §2. Document Hierarchy & Tag Topology
