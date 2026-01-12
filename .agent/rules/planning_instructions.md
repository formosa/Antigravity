---
type: rule
name: "Adversarial Planning Protocol"
globs:
  - "implementation_plan.md"
  - "task.md"
priority: 90
trigger:
  - "@Implementation_Plan"
severity: mandatory
description: "Enforces rigorous architectural scrutiny, entropy audits, and symbolic complexity analysis before code generation."
---
# RULE: ADVERSARIAL IMPLEMENTATION PROTOCOL

## 1. PRE-COMPUTATION AUDIT (MANDATORY)
Before generating `implementation_plan.md`, execute the following logic verification:
1.  **Tool-Use Verification**: Have you explicitly executed a file-read command on the target files? **IF NO**: Stop. Read the files first.
2.  **Schema Check**: Do you possess the type definitions (TypeScript interfaces/Python TypedDicts) for all modified data structures?

## 2. OUTPUT MAPPING: ANTIGRAVITY SCHEMA
Map your analysis into `implementation_plan.md`.

### Section: # \[Objective & Entropy\]
* **Goal**: One sentence summary.
* **Entropy Audit**: List strictly **unused** imports, dead code, or deprecated patterns detected in the target files.
    * *Directive*: If no entropy is found, state "Entropy: Clean".

### Section: ## Architectural Review
**Trigger**: If `Complexity Level > 2`.
**Constraint**: Use the **Symbolic Complexity Matrix** below (Do not estimate LOC).

| Impact Area | Low Risk | High Risk (Requires Justification) |
| :--- | :--- | :--- |
| **Dependencies** | Standard Lib only | New External Pip/Npm Package |
| **Scope** | Function-local | Global State / IPC / Schema Change |
| **I/O** | Memory only | Disk Write / Network Call |

* **Complexity Level**:
    * **1 (Trivial)**: Local logic only. No I/O.
    * **3 (Standard)**: Existing I/O patterns. No Schema changes.
    * **5 (Critical)**: Schema changes, New Dependencies, or Async concurrency changes.

### Section: ## Build Manifest (Proposed Changes)
For each file, provide specific **Atomic Directives**:
1.  **Signature**: Exact function/class signature to be modified.
2.  **Logic**: Pseudo-code referencing specific variables.
3.  **Prohibitions**: What must NOT be done (e.g., "Do not remove error handling wrapper").

### Section: ## Verification & Falsification
Define steps to verify success AND failure handling.
* **Happy Path**: `pytest -k "test_feature_success"`
* **Failure Path**: `pytest -k "test_feature_invalid_input"` (How does the system behave under stress?)
