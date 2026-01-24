# Ambiguous Classification Example (Scoring Matrix Required)

## Input Fragment

> "The system must aggregate all log messages into a single file with automatic rotation every 50MB and retain logs for 30 days."

## Analysis

### Decision Tree Traversal

**Q1: WHY?** Business justification?
❌ **NO** - Not about business value

**Q2: LIMITS?** Defines constraints?
🟡 **PARTIAL** - Contains limits (50MB, 30 days) but also describes behavior

**Q3: WHAT?** Describes system behavior?
🟡 **PARTIAL** - Describes what happens to logs but focuses on constraints

**Result**: **AMBIGUOUS** - Proceed to scoring matrix

### Scoring Matrix

| Factor | Present? | BRD | NFR | FSD | ICD | Total |
|:-------|:--------:|:---:|:---:|:---:|:---:|:-----:|
| Numeric metrics | ✅ | +1 | +3 | +1 | +2 | — |
| Modality (must) | ✅ | +2 | +3 | +2 | +1 | — |
| Schema definition | 🟡 | 0 | 0 | 0 | +3 | — |
| Technology-agnostic | ✅ | +3 | +1 | +2 | 0 | — |
| **TOTALS** | — | **6** | **7** | **5** | **6** | — |

**Winner**: **NFR** (Score: 7)

### Contextual Validation

- NFR makes sense: operational limits (size, time)
- Can cite BRD: traces to observability/debugging objective
- Enables downstream: SAD chooses logging pattern, ICD defines config schema

### Output (RST)
```rst
.. nfr:: Log Management Constraints
   :id: NFR-7
   :links: BRD-3.5

.. nfr:: Logs must be aggregated to single unified file.
   :id: NFR-7.1
   :links: NFR-7

.. nfr:: Automatic rotation every 50MB.
   :id: NFR-7.2
   :links: NFR-7

.. nfr:: Retention period: 30 days minimum.
   :id: NFR-7.3
   :links: NFR-7
```

### Confidence

**Score**: 0.78 (Moderate)
**Rationale**: Scoring resolved ambiguity, NFR appropriate for operational constraints, but could potentially be split into NFR (limits) + ICD (config schema)

### Alternative Interpretation

If fragment focused more on config structure, could be ICD:
```rst
.. icd:: Log Configuration Schema
   :id: ICD-6.2
   :links: SAD-6.1, NFR-7.2

.. code-block:: yaml

   logging:
     path: "logs/unified.log"
     rotation_mb: 50
     retention_days: 30
```
