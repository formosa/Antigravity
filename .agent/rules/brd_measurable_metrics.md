---
type: rule
name: "BRD Measurable Metrics"
globs:
  - "docs/01_brd/*.rst"
priority: 70
trigger:
  - "fast"
  - "reliable"
  - "scalable"
  - "intuitive"
severity: mandatory
description: "BRD success criteria must include measurable, quantifiable metrics."
---
# BRD Measurable Metrics Rule

## Rule Statement

**BRD: Success criteria and objectives MUST include measurable, quantifiable metrics.**

## Detection

| Pattern | Examples |
|:--------|:---------|
| Subjective adjectives | "fast", "reliable", "scalable" |
| Vague comparatives | "better", "improved", "enhanced" |
| Unmeasurable goals | "user-friendly", "intuitive" |
| Missing targets | "reduce latency" (by how much?) |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Subjective criterion | ERROR | Add specific metric |
| Missing target value | ERROR | Specify numeric target |
| Unmeasurable goal | WARNING | Reframe or move to FSD |

## Metric Format Requirements

| Type | Example |
|:-----|:--------|
| Percentage | "60% user adoption" |
| Time | "within 3 months" |
| Count | "500 users" |
| Currency | "$100K revenue" |

## Examples

### ✅ Correct

.. code-block:: rst

   .. brd:: System response must feel instantaneous (< 1 second).
      :id: BRD-8.1

### ❌ Incorrect

.. code-block:: rst

   .. brd:: System must be fast.
      :id: BRD-8

**Why**: "Fast" is subjective.

## References

- Knowledge: `constraints/brd_measurable_metrics.md`
- Source: DDR Meta-Standard §2.1
