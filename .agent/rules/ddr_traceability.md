---
type: rule
name: "DDR Traceability Rules"
globs:
  - "docs/**/*.rst"
priority: 50
trigger:
  - "traceability"
  - "audit"
  - "validation"
severity: mandatory
description: "Master dispatcher for DDR traceability validation. Routes to specific trace rules."
---
# DDR Traceability Rules

## Rule Statement

**Master dispatcher for DDR traceability validation. Routes to specific trace rules for enforcement.**

## Scope

Validates documentation integrity via constituent trace rules. This file acts as an entry point; defer to specific rules for actionable details.

## Constituent Rules

| Constraint | Rule File | Primary Triggers |
|:-----------|:----------|:-----------------|
| Complete chain to BRD | `trace_complete_chain.md` | `orphan`, `chain` |
| No forward references | `trace_no_forward_references.md` | `forward`, `reference` |
| No sibling citations | `trace_no_sibling_citations.md` | `sibling`, `peer` |
| Parent citation required | `ddr_traceability_mandate.md` | `tag`, `citation` |

## References

- Knowledge: `protocols/traceability_chain.md`
- Source: DDR Meta-Standard §4
