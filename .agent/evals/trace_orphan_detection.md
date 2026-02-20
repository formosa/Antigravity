---
type: evaluation
name: "Orphan Detection"
target_agent: "@traceability_auditor"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Process a dataset with known orphan tags (n=5)"
  - "Process a clean dataset with full traceability"
rubric:
  - "Must detect exactly 5 orphan tags in the seeded dataset"
  - "Must report 0 orphan tags in the clean dataset"
  - "Error log must isolate file/line for each orphan"
---

# Evaluation: Orphan Detection

## Test Procedure

1. Load test data with seeded orphans
2. Execute:

   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/generate_traceability_report.py" --needs-json "test_cases/orphan_needs.json" --format json
   ```

3. Extract `orphans[]` from output
4. Calculate: `detection_rate = (detected / seeded) * 100`
5. Pass if `detection_rate == 100`