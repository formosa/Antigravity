---
archetype: protocol
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - protocols/classification_decision_tree.md
related: []
agents:
  - ddr_orchestrator
---

# Classification Scoring

> **Scope**: Multi-factor scoring matrix for resolving ambiguous tier classifications.
>
> **Excludes**: Primary classification (see `classification_decision_tree.md`); tier definitions.

## Summary

When the decision tree yields ambiguous results (information matches multiple tiers), use this scoring matrix. Score the fragment against each factor, sum per tier, and assign to the highest scorer. Ties favor higher abstraction (leftward tier).

## Prerequisites

- Decision tree yielded ambiguous result
- Information fragment to classify
- Understanding of each factor's tier correlation

## Procedure

### Step 1: Score Each Factor

Rate the information (0-3 scale) against each factor:

| Factor | BRD | NFR | FSD | SAD | ICD | TDD | ISP |
|:-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Contains numeric metrics | 1 | **3** | 1 | 0 | 2 | 0 | 0 |
| References hardware | 1 | **3** | 0 | 1 | 0 | 0 | 0 |
| Describes user behavior | 2 | 0 | **3** | 0 | 0 | 0 | 0 |
| Names patterns | 0 | 0 | 0 | **3** | 0 | 1 | 0 |
| Defines JSON/YAML | 0 | 0 | 0 | 0 | **3** | 0 | 1 |
| Contains class names | 0 | 0 | 0 | 0 | 0 | **3** | 2 |
| Has executable code | 0 | 0 | 0 | 0 | 0 | 0 | **3** |
| Uses "must/shall" | 2 | **3** | 2 | 1 | 1 | 1 | 0 |
| Includes rationale | **3** | 1 | 1 | **3** | 0 | 2 | 0 |
| Technology-agnostic | **3** | 1 | 2 | 0 | 0 | 0 | 0 |

### Step 2: Calculate Tier Scores

For each factor present in the fragment, add that tier's weight.

**Example Fragment**: "The system must aggregate all log messages into a single file with automatic rotation every 50MB and retain logs for 30 days."

| Factor | Present? | Score Applied |
|:-------|:--------:|:--------------|
| Numeric metrics | YES | NFR=3, ICD=2 |
| Hardware reference | NO | — |
| User behavior | NO | — |
| Pattern naming | NO | — |
| Schema definition | PARTIAL | ICD=3 |
| Class names | NO | — |
| Executable code | NO | — |
| Must/shall modality | YES | NFR=3, FSD=2 |
| Rationale included | NO | — |
| Technology-agnostic | YES | BRD=3, NFR=1 |

### Step 3: Sum and Compare

| Tier | Total Score |
|:-----|:-----------:|
| BRD | 3 |
| NFR | **7** ← Winner |
| FSD | 2 |
| SAD | 0 |
| ICD | 5 |
| TDD | 0 |
| ISP | 0 |

### Step 4: Apply Tie-Breaker

If scores are tied, assign to the **higher abstraction** tier (leftward in hierarchy):
```
BRD > NFR > FSD > SAD > ICD > TDD > ISP
```

### Step 5: Contextual Validation

Before finalizing:
1. Does this tier make semantic sense?
2. Can it trace to appropriate parent tier?
3. Does it enable downstream design decisions?

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Clear winner | One tier scores highest | Assign to that tier |
| Tie | Multiple tiers equal | Use tie-breaker rule |
| Low scores all | No tier > 3 points | Fragment may need decomposition |

---

## References

- `protocols/classification_decision_tree.md` — Primary classification
- Source: `4. Information Assessment & Classification Framework.md` §4.2, §4.3
