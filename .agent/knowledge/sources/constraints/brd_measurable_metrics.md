---
archetype: constraint
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_brd.md
related:
  - constraints/brd_technology_agnostic.md
tiers:
  - BRD
agents:
  - brd_strategist
---

# BRD Measurable Metrics

> **Scope**: Rule that BRD success criteria must be quantifiable and testable.
>
> **Excludes**: Other BRD constraints; NFR numeric requirements.

## Summary

BRD success criteria must be measurable to enable objective validation. Vague or subjective criteria ("fast", "reliable", "user-friendly") must be converted to quantifiable metrics or removed from BRD.

## Rule Statement

**BRD: Success criteria and objectives MUST include measurable, quantifiable metrics.**

## Rationale

- Measurable criteria enable objective project success assessment
- Vague criteria lead to scope disagreements
- Quantifiable goals drive NFR derivation
- Testable metrics support acceptance validation

## Detection

How to identify violations:

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

## Examples

### ✅ Correct

```rst
.. brd:: System response must feel instantaneous (< 1 second).
   :id: BRD-8.1
```

```rst
.. brd:: Achieve 99.9% operational uptime.
   :id: BRD-2.3
```

```rst
.. brd:: Reduce voice interaction latency by 50% compared to cloud alternatives.
   :id: BRD-5.2
```

```rst
.. brd:: Support 8 hours of continuous operation without degradation.
   :id: BRD-7.1
```

### ❌ Incorrect

```rst
.. brd:: System must be fast.
   :id: BRD-8
```
**Why**: "Fast" is subjective. Correct: "Response time < 1 second"

```rst
.. brd:: Provide reliable operation.
   :id: BRD-2
```
**Why**: "Reliable" is vague. Correct: "99.9% uptime, < 5 second recovery"

```rst
.. brd:: Create an intuitive user experience.
   :id: BRD-9
```
**Why**: "Intuitive" is unmeasurable. Correct: Move UX requirements to FSD, or specify "< 3 steps to complete core task"

---

## References

- `concepts/tier_brd.md` — BRD tier definition
- `constraints/brd_technology_agnostic.md` — Related BRD constraint
- Source: `ddr_meta_standard.txt` §2.1 Business Requirements Document
