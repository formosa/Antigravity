# NFR Classification Example

## Input Fragment

> "IPC message dispatch must achieve sub-millisecond latency (< 1ms) for metadata-only frames and complete round-trip within 20ms for 1MB payloads on the target hardware (AMD Ryzen 9 5900X, 32GB RAM)."

## Analysis

### Decision Tree Traversal

**Q1: WHY?** Business justification?
❌ **NO** - This is a constraint, not business value

**Q2: LIMITS?** Defines constraints/boundaries?
✅ **YES** - Specific performance targets and hardware specifications

**Assignment**: **NFR**

### Factor Detection

| Factor             | Present?   | Evidence                      |
| :----------------- | :--------: | :---------------------------- |
| Numeric metrics    | ✅         | "< 1ms", "20ms", "1MB"        |
| Hardware reference | ✅         | "AMD Ryzen 9 5900X, 32GB RAM" |
| Modality keywords  | ✅         | "must achieve"                |

### Scoring (if ambiguous)

Not needed - clear NFR assignment from decision tree

### Validation

✅ **PASS** - Numeric values with units
✅ **PASS** - Specific hardware constraints
⚠️ **WARNING** - Should cite parent BRD justifying this constraint

### Output (RST)

```rst
.. nfr:: IPC Performance Constraints
   :id: NFR-4
   :links: BRD-8

.. nfr:: IPC Dispatch: Sub-millisecond (< 1ms) for metadata-only frames.
   :id: NFR-4.1
   :links: NFR-4

.. nfr:: Round Trip: < 20ms for 1MB payload frames.
   :id: NFR-4.2
   :links: NFR-4

.. nfr:: Target Hardware: AMD Ryzen 9 5900X, 32GB DDR4-3200 RAM.
   :id: NFR-1.1
   :links: BRD-3
```

### Confidence

**Score**: 0.92 (High)
**Rationale**: Clear performance constraints with specific numeric targets and hardware specs - classic NFR characteristics