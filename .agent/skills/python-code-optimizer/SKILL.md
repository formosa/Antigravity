---
name: python-code-optimizer
version: 2.0.0
description: Optimizes Python code using deterministic AST-first transformations with validation gates and rollback safety.
---

<when_to_use>
- The user asks to improve Python quality, maintainability, or style.
- The user asks for complexity/entropy reduction or Clean Code enforcement.
</when_to_use>

<how_to_use>
## Standard workflow
1. Analyze baseline:
   - `python .agent/skills/python-code-optimizer/scripts/analyze_complexity.py --input <file.py>`
   - `python .agent/skills/python-code-optimizer/scripts/analyze_entropy.py <file.py>`
2. Optimize:
   - `python .agent/skills/python-code-optimizer/scripts/optimize_python.py --input <file.py> --output <optimized.py> --level <conservative|balanced|aggressive|extreme> --report`
3. Validate:
   - `python .agent/skills/python-code-optimizer/scripts/validation_suite.py --original <file.py> --optimized <optimized.py>`
4. If validation fails, keep original unchanged and report exact failure.

## Decision policy
- Default level: `balanced`.
- Use `conservative` for minimal-risk edits.
- Use `aggressive`/`extreme` only when explicitly requested or when quality targets are unmet after balanced pass.

## Quality targets
- Cyclomatic complexity: <=10/function
- Cognitive complexity: <=15/function
- Maintainability Index: >=75
- Structural entropy: <0.4
- Documentation coverage: >=80%
- Type hint coverage: >=70%

## Anti-hallucination safeguards
- Never claim metrics without command output.
- Never claim API preservation unless validation confirms it.
- If tooling is missing, report the limitation and run available checks only.
</how_to_use>

<constraints>
- Preserve public API unless user explicitly approves breaking changes.
- Do not silently rewrite behavior-critical logic.
- Prefer script-based transformations over ad-hoc manual rewrites.
</constraints>

<resources_reference>
- `.agent/skills/python-code-optimizer/scripts/optimize_python.py`
- `.agent/skills/python-code-optimizer/scripts/validation_suite.py`
- `.agent/skills/python-code-optimizer/scripts/analyze_complexity.py`
- `.agent/skills/python-code-optimizer/scripts/analyze_entropy.py`
- `.agent/skills/python-code-optimizer/resources/clean_code_rules.md`
</resources_reference>
