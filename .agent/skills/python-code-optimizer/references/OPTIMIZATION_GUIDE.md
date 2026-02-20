# Python Code Optimization Guide

> Comprehensive reference for the `python-code-optimizer` Antigravity Skill v3.0.0.
> Optimized for Gemini 3 Flash agent workflows (Fast mode, Antigravity IDE v1.16.5).

---

## 1. Cyclomatic Complexity Reduction

### Definition

Cyclomatic complexity (CC) measures the number of independent execution paths
through a function. A CC of 1 means one path; each branch (`if`, `for`,
`while`, `except`, `and`, `or`) adds 1.

### Thresholds

| CC Range   | Risk Level     | Action Required                 |
| ---------- | -------------- | ------------------------------- |
| 1–5        | Low            | None                            |
| 6–10       | Moderate       | Review; document logic paths    |
| 11–20      | High           | Refactor; decompose function    |
| 21+        | Very High      | Immediate decomposition         |

### Decomposition Strategy

**Before:**

```python
def process(data, mode, flag, level):
    if mode == 'A':
        if flag:
            if level > 5:
                ...  # 10 more branches
```

**After:**

```python
def process(data: Any, mode: str, flag: bool, level: int) -> Any:
    handler = _get_mode_handler(mode)
    return handler(data, flag, level)

def _get_mode_handler(mode: str) -> Callable:
    handlers = {'A': _handle_mode_a, 'B': _handle_mode_b}
    return handlers.get(mode, _handle_default)
```

---

## 2. Cognitive Complexity

Cognitive complexity differs from cyclomatic complexity by penalizing
nested structures more heavily, reflecting actual human comprehension cost.

### Nesting Penalty Rules

- Each nesting level adds an increment to the cost
- Boolean operators: +1 per operator
- Linear flow breaks (`return`, `break`, `continue`): +1 each

### Reduction Tactics

1. **Early return pattern** — eliminate else after return
2. **Guard clauses** — validate inputs at function entry
3. **Inversion** — flip conditions to remove nesting levels
4. **Extraction** — move nested logic into named helper functions

---

## 3. Maintainability Index Targets

| MI Score   | Grade   | Meaning                            |
| ---------- | ------- | ---------------------------------- |
| 85–100     | A       | Highly maintainable                |
| 70–84      | B       | Maintainable with minor issues     |
| 55–69      | C       | Moderate maintainability           |
| 40–54      | D       | Difficult to maintain              |
| 0–39       | F       | Unmaintainable — requires rewrite  |

### Improving Maintainability

- Reduce function size (target: < 30 LOC per function)
- Increase documentation coverage to > 90%
- Decrease Halstead volume (avoid complex expressions)
- Reduce cyclomatic complexity

---

## 4. Performance Optimization Patterns

### 4.1 List Comprehensions over Loops

```python
# Avoid
results = []
for x in data:
    if x > 0:
        results.append(x * 2)

# Prefer
results = [x * 2 for x in data if x > 0]
```

### 4.2 Generator Expressions for Large Data

```python
# Avoid (builds full list in memory)
total = sum([compute(x) for x in large_dataset])

# Prefer (lazy evaluation)
total = sum(compute(x) for x in large_dataset)
```

### 4.3 functools.lru_cache for Pure Functions

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def expensive_computation(n: int) -> int:
    ...
```

### 4.4 dict.get() over Key Checks

```python
# Avoid
if key in mapping:
    value = mapping[key]
else:
    value = default

# Prefer
value = mapping.get(key, default)
```

### 4.5 String Join over Concatenation

```python
# Avoid (O(n²) memory)
result = ''
for part in parts:
    result += part

# Prefer (O(n))
result = ''.join(parts)
```

---

## 5. Design Patterns for Python

### 5.1 Strategy Pattern (replaces long if/elif chains)

```python
from typing import Callable, Dict

STRATEGIES: Dict[str, Callable] = {
    'fast': fast_algorithm,
    'accurate': accurate_algorithm,
    'balanced': balanced_algorithm,
}

def execute(mode: str, data: Any) -> Any:
    strategy = STRATEGIES.get(mode, balanced_algorithm)
    return strategy(data)
```

### 5.2 Context Manager for Resource Safety

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(config: dict):
    resource = acquire(config)
    try:
        yield resource
    finally:
        release(resource)
```

### 5.3 Dataclasses for Data Containers

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ProcessingResult:
    success: bool
    output: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
```

---

## 6. Import Organization (isort convention)

```python
# 1. Standard library
import ast
import json
from pathlib import Path

# 2. Third-party packages
import numpy as np
import pandas as pd

# 3. Local / project modules
from .utils import helper_function
from .models import DataModel
```

---

## 7. Error Handling Best Practices

```python
# Specific exceptions (never bare except)
try:
    result = risky_operation()
except ValueError as e:
    logger.warning(f"Invalid value: {e}")
    result = default_value
except (IOError, OSError) as e:
    logger.error(f"I/O failure: {e}")
    raise RuntimeError(f"Cannot proceed: {e}") from e
```

---

## 8. Type Annotation Standards

```python
from typing import Any, Dict, List, Optional, Tuple, Union
from collections.abc import Callable, Generator, Sequence

def process_records(
    records: List[Dict[str, Any]],
    transform: Callable[[Dict[str, Any]], Dict[str, Any]],
    limit: Optional[int] = None
) -> Tuple[List[Dict[str, Any]], int]:
    ...
```

---

## 9. Optimization Checklist

### Before Submitting Optimized Code

- [ ] Cyclomatic complexity ≤ 10 per function
- [ ] Maintainability index ≥ 70
- [ ] 100% Numpy-style docstring coverage
- [ ] All parameters and return types annotated
- [ ] Zero PEP 8 violations
- [ ] No bare `except:` clauses
- [ ] No mutable default arguments
- [ ] Imports organized (stdlib → third-party → local)
- [ ] Lines ≤ 88 characters
- [ ] No unused imports
- [ ] No magic numbers (use named constants)
- [ ] Logging instead of print statements (production code)
- [ ] Context managers for file/resource handling