---
type: evaluation
name: "DDR Classification Accuracy"
target_agent: "@ddr_orchestrator"
judge_model: "gemini-3.1-pro"
pass_threshold: 95
scenarios:
  - "Classify text fragments into DDR tiers"
  - "Compare implementation against ground truth labels"
rubric:
  - "Accuracy >= 95% on test set"
  - "No misclassifications between BRD and ISP"
---

# Evaluation: DDR Classification Accuracy

## Test Procedure

1. Load test data from `test_cases/tier_classification.json`
2. For each case, execute:

   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/classify_information.py" --input "$input"
   ```

3. Compare `output.tier` to `expected.tier`
4. Calculate: `accuracy = (correct / total) * 100`
5. Pass if `accuracy >= 95`