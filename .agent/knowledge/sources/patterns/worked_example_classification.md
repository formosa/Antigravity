---
archetype: pattern
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - protocols/classification_decision_tree.md
  - protocols/classification_scoring.md
related:
  - patterns/worked_example_feature.md
---

# Worked Example: Classification

> **Scope**: Step-by-step demonstration of tier classification using decision tree and scoring matrix.
>
> **Excludes**: Feature documentation workflow; abstraction protocols.

## Summary

This worked example demonstrates the complete classification process for an ambiguous information fragment, showing decision tree traversal, scoring matrix application, and final tier assignment with RST output.

## Input Fragment

> "The system must aggregate all log messages into a single file with automatic rotation every 50MB and retain logs for 30 days."

## Step 1: Decision Tree Traversal

### Q1: Does it answer "WHY build?"

**Analysis**: No—this describes an operational constraint, not business justification.

**Result**: Not BRD → Continue

### Q2: Does it define LIMITS?

**Analysis**: YES—contains specific limits:
- 50MB rotation threshold
- 30-day retention period

**Result**: Candidate for NFR

### Initial Assessment: NFR

However, there's ambiguity—this could also be ICD (configuration schema). Apply scoring matrix.

## Step 2: Scoring Matrix Application

| Factor | Present? | Scores Applied |
|:-------|:--------:|:---------------|
| Contains numeric metrics | YES | NFR=3, ICD=2, BRD=1 |
| References hardware | NO | — |
| Describes user behavior | NO | — |
| Names patterns | NO | — |
| Defines JSON/YAML | PARTIAL | ICD=3 |
| Contains class names | NO | — |
| Has executable code | NO | — |
| Uses "must/shall" | YES | NFR=3, FSD=2, BRD=2 |
| Includes rationale | NO | — |
| Technology-agnostic | YES | BRD=3, NFR=1, FSD=2 |

## Step 3: Calculate Tier Scores

| Tier | Calculation | Total |
|:-----|:------------|:-----:|
| BRD | 1 + 2 + 3 | 6 |
| NFR | 3 + 3 + 1 | **7** ← Winner |
| FSD | 2 + 2 | 4 |
| SAD | — | 0 |
| ICD | 2 + 3 | 5 |
| TDD | — | 0 |
| ISP | — | 0 |

## Step 4: Contextual Validation

| Check | Result |
|:------|:-------|
| Does NFR make sense? | YES—operational limits (size, time) |
| Can it cite BRD? | YES—traces to observability objective |
| Does it enable downstream? | YES—SAD chooses logging pattern, ICD defines config |

## Step 5: Final Output

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

## Key Decisions

| Decision Point | Choice | Rationale |
|:---------------|:-------|:----------|
| NFR vs ICD | NFR | Constraint > Schema (ICD is downstream) |
| Block + Atomics | Yes | Multiple related constraints warrant grouping |
| Parent citation | BRD-3.5 | "Observability/debugging" business objective |

---

## References

- `protocols/classification_decision_tree.md` — Primary algorithm
- `protocols/classification_scoring.md` — Ambiguity resolution
- Source: `4. Information Assessment & Classification Framework.md` §4.3
