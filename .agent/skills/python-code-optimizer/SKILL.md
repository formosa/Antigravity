---
type: skill
name: python-code-optimizer
description: Comprehensively optimizes Python code quality through multi-stage AST-based analysis including Clean Code enforcement and PEP 8 compliance.
scope: workspace
---

# Python Code Optimizer

Multi-stage optimization pipeline that transforms Python source files into
enterprise-grade, academically rigorous code. Enforces Robert C. Martin's
Clean Code principles alongside structural entropy metrics.

## Quick Start

### 1. Optimize

```bash
python .agents/skills/python-code-optimizer/scripts/optimize_python.py \
  --input <file.py> --output <file.2.py> --level aggressive --report
```

### 2. Validate

```bash
python .agents/skills/python-code-optimizer/scripts/validation_suite.py \
  --original <file.py> --optimized <file.2.py>
```

### 3. Analyze Complexity / Entropy

```bash
python .agents/skills/python-code-optimizer/scripts/analyze_complexity.py --input <file.py>
python .agents/skills/python-code-optimizer/scripts/analyze_entropy.py <file.py>
```

## Optimization Pipeline

1. **Analysis** — Parse AST, compute cyclomatic & cognitive complexity, entropy
2. **Structure Analysis** — Identify complex functions, duplicated code, excess args
3. **AST Refactoring** — RefactorEngine: naming conventions, docstring injection, type stubs, string modularization, anti-pattern cleanup (with comment preservation)
4. **Documentation Analysis** — Identify undocumented functions and classes
5. **Quality Enforcement** — Ruff formatting & linting, PEP 8 compliance
6. **Performance Analysis** — Detect O(n²) patterns, recommend caching
7. **Validation** — Verify API preservation, syntax, and quality score ≥ 75

Optimization levels: `conservative` (analysis only) | `balanced` (enterprise targets) | `aggressive` (academic targets) | `extreme` (maximum refactoring, CC ≤ 6, MI ≥ 85)

## Quality Targets

| Metric                 | Target          | Tool                  |
| ---------------------- | --------------- | --------------------- |
| Cyclomatic Complexity  | ≤ 10 / function | radon, AST            |
| Cognitive Complexity   | ≤ 15 / function | AST                   |
| Maintainability Index  | ≥ 75            | radon, SEI formula    |
| Structural Entropy     | < 0.4           | `analyze_entropy.py`  |
| Documentation Coverage | ≥ 80%           | `validation_suite.py` |
| Type Hint Coverage     | ≥ 70%           | `validation_suite.py` |
| PEP 8 Violations       | 0               | Ruff                  |
| Max Function Lines     | ≤ 50            | AST                   |
| Max Function Args      | ≤ 5             | AST, pylint           |
| Max Nesting Depth      | ≤ 4             | AST                   |

## Clean Code Rules

For the complete enforcement ruleset (N1–N7, F1–F4, C1–C4, G5–G36, S1–S3),
read [resources/clean_code_rules.md](resources/clean_code_rules.md)
before applying optimizations.

## Error Handling

- **Syntax error in input** — Refuse modification, report pre-existing issue
- **API symbols removed** — Abort, restore backup, report missing symbols
- **Quality score < 75** — Warn user, provide improvement recommendations
- **Tool not installed** — Fall back to AST-based analysis, log warning

## Agent Execution Notes

- **Encoding**: All file I/O uses UTF-8. All subprocess calls use `errors='replace'`. Console output is ASCII-only.
- **Failure Safety**: On engine failure, the original file is preserved unchanged.
- **String Thresholds**: Vary by optimization level — `extreme`: >=2 newlines/>=100 chars; `balanced`: >=6/>=300.