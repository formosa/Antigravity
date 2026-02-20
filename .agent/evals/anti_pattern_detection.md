---
type: evaluation
name: "System Anti-Pattern Detection"
target_agent: "@ddr_orchestrator"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Scan full documentation corpus for anti-patterns"
  - "Verify zero false positives in clean sections"
rubric:
  - "Must report zero anti-pattern violations"
  - "Must correctly categorize any detected issues"
---

# Evaluation: System Anti-Pattern Detection

## Test Procedure

1. Build needs.json:

   ```powershell
   & ".venv/Scripts/sphinx-build.exe" -b needs "docs" "docs/_build"
   ```

2. Execute:

   ```powershell
   & ".venv/Scripts/python" ".agent/scripts/detect_anti_patterns.py" --needs-json "docs/_build/json/needs.json"
   ```

3. Count total violations from output
4. Pass if `violations == 0`
