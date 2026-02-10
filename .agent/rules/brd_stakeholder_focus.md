---
type: rule
name: "BRD Stakeholder Focus"
activation: glob
globs:
  - "docs/01_brd/*.rst"
priority: 70
severity: guideline
description: "BRD requirements should identify which stakeholders benefit."
---
# BRD Stakeholder Focus Rule

## Rule Statement

**BRD: Requirements SHOULD identify the stakeholders who benefit from each objective.**

## Detection

| Pattern | Indication |
|:--------|:-----------|
| No stakeholder mention | Requirement lacks "who benefits" |
| Generic "users" | Could be more specific |
| Missing persona context | No role identification |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| No stakeholder identified | WARNING | Add beneficiary context |
| Vague stakeholder | INFO | Specify role or persona |

## Typical Stakeholders

- End users — What do they gain?
- Enterprise customers — Revenue impact?
- Business owners — Competitive advantage?
- Compliance officers — Regulatory requirements?
- Developers — Productivity improvements?

## Examples

### ✅ Correct

.. code-block:: rst

   .. brd:: Enable accessibility users to interact hands-free.
      :id: BRD-5.7

### ❌ Could Improve

.. code-block:: rst

   .. brd:: Enable hands-free interaction.
      :id: BRD-5.7

**Why**: Who benefits? Add stakeholder context.

## Related Rules

- [brd_technology_agnostic.md](brd_technology_agnostic.md) — No tech terms in BRD
- [brd_measurable_metrics.md](brd_measurable_metrics.md) — Quantifiable success criteria

## References

- Knowledge: `concepts/tier_brd.md`
- Source: DDR Meta-Standard §2.1
