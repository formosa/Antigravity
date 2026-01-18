---
type: evaluation
name: "DDR Classification Accuracy"
description: "Measures accuracy of tier classification decisions against ground truth."
target_agent: "@ddr_orchestrator"
threshold: 95
metrics:
  - name: classification_accuracy
    type: percentage
    target: 95
test_cases: "test_cases/tier_classification.json"
schedule: "on_demand"
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
