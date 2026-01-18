---
type: evaluation
name: "System Anti-Pattern Detection"
description: "Validates zero anti-pattern violations across entire DDR corpus."
target_agent: "@ddr_orchestrator"
threshold: 0
metrics:
  - name: violation_count
    type: count
    target: 0
test_cases: "needs.json"
schedule: "pre-release"
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
