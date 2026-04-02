---
name: python-code-optimizer
version: 2.0.2
description: Optimizes Python code using deterministic AST-first transformations with validation gates and rollback safety. Use when the task is to improve Python maintainability, complexity, or style while preserving behavior. Do not use when the requested change is a non-Python task or an intentional behavior rewrite without preservation goals.
---

<when_to_use>

- The user asks to improve Python quality, maintainability, or style.
- The user asks for complexity/entropy reduction or Clean Code enforcement.
- Do not use this skill when the request targets non-Python files or intentionally changes behavior instead of preserving it.
- Example prompt: "Optimize this Python module for readability and lower complexity without changing behavior."
- Example prompt: "Run the Python optimizer workflow on src/parser.py with conservative settings."
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

- Run `.agent/skills/python-code-optimizer/scripts/optimize_python.py` to perform the deterministic optimization pass.
- Run `.agent/skills/python-code-optimizer/scripts/validation_suite.py` to confirm behavioral and quality preservation after optimization.
- Run `.agent/skills/python-code-optimizer/scripts/analyze_complexity.py` to establish the baseline and post-change complexity profile.
- Run `.agent/skills/python-code-optimizer/scripts/analyze_entropy.py` to measure structural entropy before or after transformation.
- Read `.agent/skills/python-code-optimizer/resources/clean_code_rules.md` to preserve the local optimization heuristics and naming standards.
</resources_reference>
