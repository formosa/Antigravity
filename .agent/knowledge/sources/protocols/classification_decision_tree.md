---
archetype: protocol
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
related:
  - protocols/classification_scoring.md
agents:
  - ddr_orchestrator
---

# Classification Decision Tree

> **Scope**: Primary algorithm for assigning unclassified information to DDR tiers.
>
> **Excludes**: Ambiguity resolution (see `classification_scoring.md`); tier definitions.

## Summary

The classification decision tree provides a sequential question-based algorithm for determining which DDR tier owns a piece of information. It processes from highest abstraction (BRD) to lowest (ISP), assigning to the first tier that matches.

## Prerequisites

- Unclassified information fragment to analyze
- Familiarity with tier definitions (`concepts/tier_*.md`)
- Glossary for consistent terminology

## Procedure

### Decision Flow

```
INPUT: Unclassified Information Fragment
           │
           ▼
┌───────────────────────────────┐
│ Q1: Does it answer "WHY"?     │
│ (Business value, ROI, market) │
└───────┬───────────────────┬───┘
        │ YES               │ NO
        ▼                   ▼
  ┌─────────┐         ┌─────────────────────────┐
  │   BRD   │         │ Q2: Does it define      │
  └─────────┘         │ LIMITS? (Hardware, SLAs)│
                      └────┬────────────────┬───┘
                           │ YES            │ NO
                           ▼                ▼
                      ┌─────────┐    ┌──────────────────┐
                      │   NFR   │    │ Q3: Does it      │
                      └─────────┘    │ describe WHAT?   │
                                     │ (Features, UX)   │
                                     └────┬────────┬────┘
                                          │ YES    │ NO
                                          ▼        ▼
                                    ┌─────────┐  ┌────────────────┐
                                    │   FSD   │  │ Q4: Does it    │
                                    └─────────┘  │ define HOW?    │
                                                 │ (Patterns)     │
                                                 └────┬──────┬────┘
                                                      │ YES  │ NO
                                                      ▼      ▼
                                                ┌─────────┐ ┌──────────┐
                                                │   SAD   │ │ Q5: Is   │
                                                └─────────┘ │ SCHEMA?  │
                                                            └────┬─┬───┘
                                                            YES  │ │ NO
                                                              ▼  ▼
                                                         ┌─────────┐
                                                         │   ICD   │
                                                         └────┬────┘
                                                              │
                                  ┌───────────────────────────┴────────┐
                                  │ Q6: CLASS STRUCTURE?               │
                                  │ (Methods, dependencies)            │
                                  └────┬───────────────────────────┬───┘
                                       │ YES                       │ NO
                                       ▼                           ▼
                                 ┌─────────┐                 ┌─────────┐
                                 │   TDD   │                 │   ISP   │
                                 └─────────┘                 └─────────┘
```

### Step-by-Step

1. **Q1: WHY?** Does this explain business value, ROI, market need, or strategic objective?
   - YES → **BRD**
   - NO → Continue

2. **Q2: LIMITS?** Does this define constraints, SLAs, hardware specs, or performance bounds?
   - YES → **NFR**
   - NO → Continue

3. **Q3: WHAT?** Does this describe capabilities, features, user interactions, or behaviors?
   - YES → **FSD**
   - NO → Continue

4. **Q4: HOW?** Does this define architectural patterns, process topology, or organization?
   - YES → **SAD**
   - NO → Continue

5. **Q5: SCHEMA?** Does this define data formats, message structures, or contracts?
   - YES → **ICD**
   - NO → Continue

6. **Q6: CLASS?** Does this specify class structure, methods, or dependencies?
   - YES → **TDD**
   - NO → **ISP** (executable code skeleton)

## Outcomes

| Result | Next Action |
|:-------|:------------|
| Clear tier match | Create tag in appropriate tier |
| Ambiguous (multiple partial matches) | Use `classification_scoring.md` |
| No match | Re-examine fragment; may need decomposition |

---

## References

- `protocols/classification_scoring.md` — Ambiguity resolution
- `concepts/tier_hierarchy.md` — Tier definitions
- Source: `4. Information Assessment & Classification Framework.md` §4.1
