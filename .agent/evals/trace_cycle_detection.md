---
type: evaluation
name: "Cycle Detection"
target_agent: "@traceability_auditor"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Process a dataset with known circular dependencies (A->B->C->A)"
  - "Process a clean hierarchical dataset"
rubric:
  - "Must detect all seeded cycles"
  - "Must report 0 cycles in clean dataset"
  - "Must output cycle path in error log"
---

# Evaluation: Cycle Detection

## Test Procedure

1. Load test data with seeded cycles
2. Execute:

   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/build_dependency_graph.py" --needs-json "test_cases/cycle_needs.json"
   ```

3. Extract `cycles[]` from output
4. Calculate: `detection_rate = (detected / seeded) * 100`
5. Pass if `detection_rate == 100`
