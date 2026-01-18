---
type: tool
name: "scoring_matrix"
description: "Resolves ambiguous tier classification using weighted scoring factors."
command: ".venv\\Scripts\\python .agent/scripts/scoring_matrix.py --fragment \"${fragment}\" --candidates \"${candidates}\""
runtime: system
confirmation: never
args:
  fragment:
    description: "Information fragment to score"
    required: true
  candidates:
    description: "Comma-separated list of candidate tiers (e.g., 'FSD,SAD')"
    required: true
---

# Tool: Scoring Matrix

## Overview

Resolves ambiguous tier classification by applying a weighted multi-factor scoring
matrix. Used when `classify_information` returns `ambiguous: true`.

## Knowledge Source

- **Scoring Protocol**: `.agent/knowledge/sources/protocols/classification_scoring.md`

## Configuration

- **Entry Point**: `.agent/scripts/scoring_matrix.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--fragment`: Required. The information text to score.
    - `--candidates`: Required. Comma-separated candidate tiers.
    - `--verbose`: Optional. Include detailed factor breakdown.

## Execution Steps

### 1. Parse Candidates
- Accept comma-separated tier codes
- Validate each is a valid DDR tier

### 2. Evaluate Factors
For each factor, score presence (0-3 points per tier):

| Factor | Best Tier |
|:-------|:----------|
| Numeric metrics | NFR (3) |
| Hardware reference | NFR (3) |
| User behavior | FSD (3) |
| Pattern naming | SAD (3) |
| Schema definition | ICD (3) |
| Class names | TDD (3) |
| Executable code | ISP (3) |
| Must/shall modality | NFR (3) |
| Includes rationale | BRD/SAD (3) |
| Technology-agnostic | BRD (3) |

### 3. Sum Scores
- Aggregate factor weights for each candidate tier
- Identify tier with highest score

### 4. Apply Tie-Breaker
If scores are tied, assign to higher abstraction tier:
```
BRD > NFR > FSD > SAD > ICD > TDD > ISP
```

### 5. Output Result
- JSON with winner, all scores, justification

## Protocol & Validation

### Success Verification
1. Confirm output contains `winner`, `scores`, `justification` fields
2. Confirm `winner` is one of the input candidates
3. Confirm `scores` sums match factor evaluations

### Example Output
```json
{
  "winner": "NFR",
  "scores": {
    "NFR": 7.0,
    "FSD": 2.0
  },
  "justification": "Scored 3 factors. Winner: NFR with 7.0 points.",
  "tie_broken": false
}
```

## Rules
- **Minimum Candidates**: Requires at least 2 candidate tiers
- **Tie-Breaking**: Higher abstraction wins (BRD > ISP direction)
- **Low Score Warning**: If winner < 3 points, fragment may need decomposition
