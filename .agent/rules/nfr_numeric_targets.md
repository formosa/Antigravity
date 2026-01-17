---
type: rule
priority: 90
trigger:
  - "performance"
  - "latency"
  - "throughput"
  - "constraint"
severity: mandatory
description: "NFR constraints must include specific, measurable numeric targets (<Number> <Unit>) and use RFC 2119."
---
# NFR Numeric Targets Rule

## Rule Statement
**NFR Constraints MUST include specific, measurable numeric targets (triplet: Keyword + Number + Unit) and use RFC 2119 modality (MUST, SHOULD, MAY).**

## Detection
| Pattern | Examples |
|:--------|:---------|
| Vague performance claims | "fast", "efficient", "responsive", "real-time" (without ms) |
| Missing units | "latency less than 100" |
| Qualitative descriptors | "high throughput", "low power" |
| Non-RFC 2119 modality | "it is necessary to", "should" (lowercase) |

## Enforcement
| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Vague descriptor | ERROR | Replace with specific `<number> <unit>` |
| Missing modality | ERROR | Add MUST, SHOULD, or MAY |
| Unitless value | ERROR | Add appropriate unit (ms, %, FPS, etc.) |

## Forbidden Terms
| Category | Terms |
|:---------|:------|
| Performance | fast, optimized, efficient, snappy |
| Latency | low-latency, real-time (without ms) |
| Throughput | high-speed, bulk |
| Power | low-power, battery-friendly |

## Enforcement Protocol
1. **Scan** NFR content for performance/constraint claims.
2. **Verify** presence of RFC 2119 keyword (MUST, SHOULD, MAY).
3. **Verify** presence of numeric value AND unit close to the claim.
4. **If** missing → **ERROR** and request quantification.

## Examples

### ✅ Correct
```rst
.. nfr:: The audio processing pipeline MUST maintain a latency of < 50ms.
   :id: NFR-4.2
```

### ❌ Incorrect
```rst
.. nfr:: The audio processing pipeline should be fast.
   :id: NFR-4.2
```
**Why**: "fast" is qualitative, missing number/unit, and "should" is lowercase.
