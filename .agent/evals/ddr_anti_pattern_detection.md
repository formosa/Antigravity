---
type: evaluation
name: "DDR Anti-Pattern Detection"
target_agent: "@ddr_orchestrator"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Scan seeded anti-patterns from test set"
  - "Verify zero false negatives for known patterns"
rubric:
  - "Must detect all known documentation anti-patterns"
  - "Report must match expected pattern types"
---

# Evaluation: DDR Anti-Pattern Detection

## Test Procedure

1. Load test data from `test_cases/anti_patterns.json`
2. Execute:

   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/detect_anti_patterns.py" --needs-json "test_cases/anti_patterns_needs.json"
   ```

3. Verify each expected pattern appears in output
4. Calculate: `detection_rate = (detected / expected) * 100`
5. Pass if `detection_rate == 100`