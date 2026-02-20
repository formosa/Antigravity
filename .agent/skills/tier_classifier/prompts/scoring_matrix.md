# Multi-Factor Scoring Matrix

Apply when decision tree yields ambiguous results (fragment partially matches multiple tiers).

## Scoring Procedure

### Step 1: Identify Present Factors

Scan fragment for presence of each classification factor.

### Step 2: Apply Tier Weights

For each present factor, add tier-specific weights to running totals.

### Step 3: Calculate Tier Scores

Sum all applied weights per tier.

### Step 4: Resolve Ties

If multiple tiers tie for highest score, favor higher abstraction (leftward in hierarchy):

```
BRD > NFR > FSD > SAD > ICD > TDD > ISP
```

---

## Classification Factors & Weights

| Factor                       | BRD   | NFR   | FSD   | SAD   | ICD   | TDD   | ISP   | Detection Pattern                            |
| :--------------------------- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :------------------------------------------- |
| **Contains numeric metrics** | 1     | **3** | 1     | 0     | 2     | 0     | 0     | Numbers with units (ms, MB, %, cores)        |
| **References hardware**      | 1     | **3** | 0     | 1     | 0     | 0     | 0     | GPU, CPU, RAM, network specs                 |
| **Describes user behavior**  | 2     | 0     | **3** | 0     | 0     | 0     | 0     | User actions, workflows, interactions        |
| **Names patterns**           | 0     | 0     | 0     | **3** | 0     | 1     | 0     | Hub-and-Spoke, Client-Server, Event-Driven   |
| **Defines JSON/YAML**        | 0     | 0     | 0     | 0     | **3** | 0     | 1     | Schema structures, field definitions         |
| **Contains class names**     | 0     | 0     | 0     | 0     | 0     | **3** | 2     | CamelCase identifiers, OOP terms             |
| **Has executable code**      | 0     | 0     | 0     | 0     | 0     | 0     | **3** | Python syntax, `def`, `class`, `pass`        |
| **Uses "must/shall"**        | 2     | **3** | 2     | 1     | 1     | 1     | 0     | RFC 2119 keywords (MUST, SHALL, SHOULD, MAY) |
| **Includes rationale**       | **3** | 1     | 1     | **3** | 0     | 2     | 0     | "Because...", "to enable...", "justifies..." |
| **Technology-agnostic**      | **3** | 1     | 2     | 0     | 0     | 0     | 0     | No specific libraries, languages, frameworks |

---

## Worked Example

**Fragment**: "The system must aggregate all log messages into a single file with automatic rotation every 50MB and retain logs for 30 days."

### Factor Detection

| Factor              | Present?   | Reasoning                              |
| :------------------ | :--------: | :------------------------------------- |
| Numeric metrics     | ✅ YES     | "50MB", "30 days"                      |
| Hardware reference  | ❌ NO      | No CPU/GPU/RAM mentioned               |
| User behavior       | ❌ NO      | No user actions described              |
| Pattern naming      | ❌ NO      | No architectural pattern named         |
| JSON/YAML schema    | 🟡 PARTIAL | Implies config schema but not explicit |
| Class names         | ❌ NO      | No OOP identifiers                     |
| Executable code     | ❌ NO      | No Python syntax                       |
| Must/shall          | ✅ YES     | "must aggregate"                       |
| Rationale           | ❌ NO      | No "because" explanation               |
| Technology-agnostic | ✅ YES     | No specific tech mentioned             |

### Score Calculation

| Tier    | Calculation                                | Total              |
| :------ | :----------------------------------------- | :----------------: |
| **BRD** | (numeric:1) + (must:2) + (tech-agnostic:3) | **6**              |
| **NFR** | (numeric:3) + (must:3) + (tech-agnostic:1) | **7** ← **Winner** |
| **FSD** | (must:2) + (tech-agnostic:2)               | **4**              |
| **SAD** | —                                          | **0**              |
| **ICD** | (numeric:2) + (schema:3) + (must:1)        | **6**              |
| **TDD** | —                                          | **0**              |
| **ISP** | —                                          | **0**              |

### Decision: NFR (Score: 7)

**Confidence**: 0.85 (clear winner, appropriate semantic fit)

---

## Confidence Calculation

```
confidence = (winner_score / total_possible_score) * semantic_fit_multiplier

Where:
- total_possible_score = max score any tier could achieve with all factors
- semantic_fit_multiplier ∈ [0.7, 1.0] based on contextual appropriateness
```

### Confidence Thresholds

| Score    | Interpretation      | Action                                      |
| :------- | :------------------ | :------------------------------------------ |
| 0.9-1.0  | High confidence     | Proceed with classification                 |
| 0.7-0.89 | Moderate confidence | Suggest human review                        |
| 0.5-0.69 | Low confidence      | Request fragment decomposition              |
| <0.5     | Very low confidence | Return ambiguous result with all candidates |

---

## Special Cases

### Tie-Breaking Example

Fragment scores: BRD=8, NFR=8, FSD=5

**Resolution**: Assign **BRD** (higher abstraction wins)

### Cross-Tier Synthesis

Fragment scores: FSD=10, ICD=9, TDD=8

**Interpretation**: Fragment spans multiple concerns
**Action**: Suggest decomposition into:

1. FSD tag for behavioral aspect
2. ICD tag for data contract
3. TDD tag for class structure

### Low Scores Across All Tiers

All tiers score < 3

**Interpretation**: Fragment may be:

- Too vague/incomplete
- Outside DDR scope
- Requires additional context

**Action**: Return classification error with guidance