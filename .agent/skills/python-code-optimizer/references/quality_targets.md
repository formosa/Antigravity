# Quality Targets Reference

## Threshold Tiers

| Metric | Enterprise Target | Academic Target | Tool | Source |
| --- | --- | --- | --- | --- |
| Cyclomatic Complexity | ≤ 10 / function | ≤ 6 | radon cc, AST | McCabe (1976) |
| Cognitive Complexity | ≤ 15 / function | ≤ 10 | AST | SonarSource (2016) |
| Maintainability Index | ≥ 75 | ≥ 85 | radon mi, SEI formula | SEI/CMU |
| Structural Entropy | < 0.4 | < 0.25 | `analyze_entropy.py` | Internal doctrine |
| Doc Coverage | ≥ 80% | 100% | `validation_suite.py` | Enterprise standard |
| Type Hint Coverage | ≥ 70% | ≥ 95% | `validation_suite.py` | PEP 484 |
| PEP 8 Violations | 0 | 0 | Ruff (replaces pycodestyle) | PEP 8 |
| Max Function Lines | ≤ 50 | ≤ 30 | AST | Clean Code F4 |
| Max Function Args | ≤ 5 | ≤ 3 | AST, pylint | Clean Code F1 |
| Max Nesting Depth | ≤ 4 | ≤ 3 | AST | Entropy doctrine |

## Optimization Levels

- **conservative**: Only enforce critical checks (syntax, API preservation). No AST refactoring.
- **balanced**: Enforce all enterprise targets. AST refactoring with comment preservation.
- **aggressive**: Enforce academic targets, rewrite non-conforming code.
- **extreme**: All aggressive transformations plus maximum refactoring depth; academic thresholds (CC ≤ 6, MI ≥ 85, entropy < 0.25, args ≤ 3, 100% docs, 95% type hints); comment-preserving AST rewrites.
