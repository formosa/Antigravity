---
archetype: constraint
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_nfr.md
related: []
tiers:
  - NFR
agents:
  - nfr_enforcer
---

# NFR Numeric Constraints

> **Scope**: Rule that NFR constraints must include specific numeric values.
>
> **Excludes**: Other tier constraints; BRD measurable metrics.

## Summary

NFR (Non-Functional Requirements) define measurable system limits. Every constraint, target, or threshold must include specific numeric values—vague or qualitative limits are not enforceable.

## Rule Statement

**NFR: All constraints and performance targets MUST include specific numeric values with units.**

## Rationale

- Numeric values enable automated testing
- Specific targets prevent ambiguity in implementation
- Measurable constraints support acceptance criteria
- Units ensure consistent interpretation

## Detection

How to identify violations:

| Pattern | Examples |
|:--------|:---------|
| Missing numbers | "low latency", "high throughput" |
| Missing units | "latency < 100" (100 what?) |
| Vague bounds | "reasonable", "acceptable" |
| Qualitative limits | "minimal overhead" |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| No numeric value | ERROR | Add specific number |
| Missing units | ERROR | Specify units (ms, MB, etc.) |
| Vague bound | ERROR | Quantify limit |

## Examples

### ✅ Correct

```rst
.. nfr:: IPC Dispatch: Sub-millisecond (< 1ms) for metadata-only.
   :id: NFR-4.1
   :links: BRD-8.1
```

```rst
.. nfr:: GPU VRAM: 10GB dedicated for model inference.
   :id: NFR-1.2
   :links: BRD-6
```

```rst
.. nfr:: Log rotation: Automatic rotation every 50MB, 30-day retention.
   :id: NFR-7.2
   :links: BRD-3.5
```

```rst
.. nfr:: Response timeout: 5 seconds maximum before error state.
   :id: NFR-5.3
   :links: BRD-2
```

### ❌ Incorrect

```rst
.. nfr:: System must have low latency.
   :id: NFR-4
```
**Why**: "Low" is subjective. Correct: "< 1 second latency"

```rst
.. nfr:: Memory usage must be reasonable.
   :id: NFR-2
```
**Why**: "Reasonable" is unmeasurable. Correct: "< 4GB RAM usage"

```rst
.. nfr:: Latency must be under 100.
   :id: NFR-4.1
```
**Why**: Missing units. Correct: "< 100ms"

---

## References

- `concepts/tier_nfr.md` — NFR tier definition
- Source: `ddr_meta_standard.txt` §2.2 Non-Functional Requirements
