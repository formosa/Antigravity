---
name: python-code-optimizer
description: Comprehensively optimizes Python code quality through multi-stage analysis including complexity reduction, professional Numpy-style documentation, PEP 8 compliance, performance profiling, maintainability enhancement, and academic-level refactoring. Use when improving Python code quality, refactoring legacy code, preparing code for production, or elevating code to academic/professional standards.
license: Apache-2.0
compatibility: Optimized for Google Antigravity IDE 1.15.6, Gemini 3 Pro. Requires Python 3.8+, pylint, radon, black, isort.
metadata:
  author: enterprise-development-team
  version: "1.15.6"
  target_model: gemini-3-pro
  optimization_level: academic-professional
allowed-tools: Bash(python:*) Bash(pylint:*) Read Write
---

# Python Code Optimizer Skill

## Overview

This skill provides comprehensive Python code optimization following a systematic, multi-stage strategy designed to transform code to academic-level professional quality. The optimization process analyzes code structure, performance characteristics, documentation completeness, and maintainability metrics.

## When to Use This Skill

Activate this skill when you need to:

- Refactor Python code to professional/academic standards
- Add comprehensive Numpy-style docstrings to undocumented code
- Reduce cyclomatic complexity and improve maintainability
- Optimize code performance while preserving functionality
- Prepare code for production deployment or peer review
- Transform legacy code into modern, idiomatic Python
- Enforce PEP 8 and industry best practices

## Optimization Strategy

### Stage 1: Initial Analysis

1. Parse the target Python file and validate syntax
2. Generate complexity metrics (cyclomatic, cognitive, maintainability index)
3. Identify code smells, anti-patterns, and technical debt
4. Profile performance bottlenecks and resource usage
5. Document current state baseline for comparison

### Stage 2: Structural Optimization

1. Decompose complex functions (cyclomatic complexity > 10)
2. Extract repeated code into reusable utilities
3. Apply SOLID principles and design patterns where appropriate
4. Optimize algorithmic complexity (time/space)
5. Refactor nested structures and reduce indentation depth

### Stage 3: Documentation Enhancement

1. Add comprehensive Numpy-style docstrings to all functions/classes
2. Include parameter types, return values, exceptions, examples
3. Document algorithmic complexity and performance considerations
4. Add inline comments for non-obvious logic
5. Create module-level documentation

### Stage 4: Code Quality Enforcement

1. Apply PEP 8 formatting via Black
2. Optimize imports with isort
3. Run pylint with enterprise-grade configuration
4. Validate type hints and add where missing
5. Ensure consistent naming conventions

### Stage 5: Performance Optimization

1. Profile execution time and memory usage
2. Replace inefficient patterns with optimized alternatives
3. Implement caching for expensive operations
4. Vectorize operations where applicable (NumPy/Pandas)
5. Optimize I/O operations and resource management

### Stage 6: Validation & Testing

1. Verify all optimizations preserve original functionality
2. Run validation suite against test cases
3. Generate before/after comparison report
4. Document all changes with rationale
5. Create optimization summary

## Usage Instructions

### Basic Usage

```bash
# Optimize a single Python file
python scripts/optimize_python.py --input path/to/script.py --output path/to/optimized_script.py

# With detailed reporting
python scripts/optimize_python.py --input script.py --output optimized.py --report --verbose
```

### Advanced Options

```bash
# Specify optimization level (conservative, balanced, aggressive)
python scripts/optimize_python.py --input script.py --level aggressive

# Focus on specific optimization categories
python scripts/optimize_python.py --input script.py --focus documentation,performance

# Generate detailed analysis report only (no modifications)
python scripts/analyze_complexity.py --input script.py --output analysis_report.json
```

### Integration with Antigravity IDE

When invoked within Antigravity IDE 1.15.6:

1. The skill automatically detects the active Python file
2. Runs comprehensive analysis in background
3. Presents optimization suggestions with confidence scores
4. Allows interactive acceptance/rejection of changes
5. Generates diff view with explanations
6. Updates file with accepted optimizations

## Output Format

The optimization process generates:

1. **Optimized Python file** - Professionally refactored code
2. **Optimization report** - Detailed metrics and improvements
3. **Change log** - Line-by-line documentation of modifications
4. **Validation results** - Test suite confirmation
5. **Metrics comparison** - Before/after quality scores

## Quality Metrics Tracked

- **Cyclomatic Complexity**: Target < 10 per function
- **Maintainability Index**: Target > 70
- **Code Coverage**: Documentation at 100%
- **PEP 8 Compliance**: 100%
- **Type Hint Coverage**: Target > 90%
- **Performance**: Baseline comparison

## Best Practices

1. **Always backup** original files before optimization
2. **Review changes** carefully - automated refactoring may alter logic
3. **Run tests** after optimization to verify functionality
4. **Iterate** - some optimizations require multiple passes
5. **Consult references** in `references/` for detailed guidance

## Common Optimization Patterns

### Pattern 1: Function Decomposition

**Before**: 100-line function with cyclomatic complexity 25
**After**: 5 focused functions, each < 20 lines, complexity < 5

### Pattern 2: Documentation Enhancement

**Before**: No docstrings, unclear parameter purposes
**After**: Complete Numpy-style documentation with examples

### Pattern 3: Performance Optimization

**Before**: O(n²) nested loops
**After**: O(n) vectorized operations or appropriate data structures

## Error Handling

The skill handles various edge cases:

- **Syntax errors**: Reported with line numbers, optimization skipped
- **Import errors**: Logged, missing dependencies documented
- **Circular refactoring**: Detected and prevented
- **Loss of functionality**: Automatically rolled back
- **Resource constraints**: Optimization scaled to available memory

## Reference Materials

For detailed information, consult:

- [Optimization Guide](references/OPTIMIZATION_GUIDE.md) - Comprehensive optimization strategies
- [Numpy Docstring Templates](references/NUMPY_DOCSTRING_TEMPLATES.md) - Documentation examples
- [Best Practices](references/BEST_PRACTICES.md) - Industry standards and patterns

## Validation

Run the validation suite to verify optimization quality:

```bash
python scripts/validation_suite.py --original original.py --optimized optimized.py
```

This ensures:

- Functional equivalence
- Performance improvement
- Documentation completeness
- Style compliance
- Maintainability enhancement

## Limitations

- Cannot optimize runtime-dependent code without test data
- May not detect all domain-specific anti-patterns
- Performance optimization requires representative workloads
- Some optimizations may reduce readability for complex domains

## Support

For optimization issues or questions:

1. Check the [Optimization Guide](references/OPTIMIZATION_GUIDE.md)
2. Review the generated optimization report for specific recommendations
3. Consult [Best Practices](references/BEST_PRACTICES.md) for pattern-specific guidance
