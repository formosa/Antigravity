---
type: rule
name: "Adversarial Planning Protocol (Auto-Refined)"
globs:
  - "implementation_plan.md"
  - "task.md"
priority: 100
trigger:
  - "@Implementation_Plan"
severity: mandatory
description: "Generates a 3-stage refined implementation plan: Audits entropy, simulates adversarial failure, and distills instructions for agentic consumption."
---
# RULE: ADVERSARIAL IMPLEMENTATION PROTOCOL (v2.0)

## 0. META-INSTRUCTION: RECURSIVE REFINEMENT
**WARNING**: You are currently operating in **Antigravity IDE v1.13.3**.
You must perform a **3-Step Internal Cycle** before outputting the final response. Do not output the intermediate thinking steps unless explicitly asked.
1.  **Draft**: Generate the initial solution.
2.  **Verify**: Adversarially attack the draft (Simulate Prompt 2).
3.  **Refine**: Strip all non-essential tokens (Simulate Prompt 3).

---

## 1. STEP ONE: PROBLEM SPACE & ENTROPY AUDIT
Before formulating the plan, execute the following:
1.  **Tool-Use Verification**: Read target files. Do not hallucinate content.
2.  **Entropy Audit**: Identify unused imports, dead code, or deprecated patterns in the context.
3.  **Maximality Check**: Ask: "Is this the maximally optimized solution, or just the easiest one?"

## 2. STEP TWO: ARCHITECTURAL COMPLEXITY MATRIX
Map the task complexity to define the rigor required.

| Impact Area | Low Risk | High Risk (Requires Justification) |
| :--- | :--- | :--- |
| **Dependencies** | Standard Lib only | New External Pip/Npm Package |
| **Scope** | Function-local | Global State / IPC / Schema Change |
| **I/O** | Memory only | Disk Write / Network Call |

## 3. STEP THREE: ADVERSARIAL SIMULATION (INTERNAL)
*Perform this critique internally:*
* **Validity**: Is the code technically accurate for the specific Python version?
* **Falsification**: How does this plan fail under stress? (e.g., `test_feature_invalid_input`).
* **Cognitive Load**: Are the instructions clear enough for a junior agent to execute without asking questions?

## 4. FINAL OUTPUT: THE IMPLEMENTATION PLAN
**Constraint**: The output below must be the result of the "Refine" phase. Remove all conversational filler. Use the following schema strictly.

### Section: # \[Objective & Entropy\]
* **Goal**: One sentence summary.
* **Entropy Status**: "Clean" or list specific dead code to remove.

### Section: ## Build Manifest (Atomic Directives)
*Provide specific instructions for the coding agent. No explanations, only directives.*

**File: `[filename]`**
1.  **Signature**: `[Exact function/class signature]`
2.  **Action**: `[Create | Modify | Delete]`
3.  **Logic**: `[Pseudo-code or specific logic requirements]`
4.  **Prohibitions**: `[What MUST NOT happen]`

### Section: ## Verification Strategy
*Define the success/failure state.*
* **Happy Path**: `pytest -k "test_success_case"`
* **Failure Path**: `pytest -k "test_failure_case"`
