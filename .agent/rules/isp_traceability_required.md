---
type: rule
name: "ISP Traceability Required"
globs:
  - "docs/07_isp/*.rst"
priority: 85
trigger:
  - "implements"
  - "requirements"
  - "docstring"
severity: mandatory
description: "ISP docstrings must include Implements: and Requirements: citations."
---
# ISP Traceability Required Rule

## Rule Statement

**ISP: All class and method docstrings MUST include `Implements:` citations linking to TDD tags.**

## Detection

| Pattern | Indication |
|:--------|:-----------|
| Missing `Implements:` | No TDD citation in docstring |
| Missing `Requirements:` | No FSD/NFR citation |
| Invalid tag format | `TDD-1` without pipe delimiters |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Missing `Implements:` | ERROR | Add TDD citation |
| Invalid citation format | WARNING | Use `|TAG-X|` format |

## Examples

### ✅ Correct

```python
def route_message(self, frame: list) -> bool:
    """
    Route incoming ZMQ frame to appropriate handler.

    Implements: |TDD-1.4|
    Requirements: |FSD-1.1|
    """
    pass
```

### ❌ Incorrect

```python
def route_message(self, frame: list) -> bool:
    """Route incoming ZMQ frame."""
    pass
```

**Why**: No `Implements:` or `Requirements:` lines.

## References

- Knowledge: `constraints/isp_numpy_docstrings.md`
- Source: DDR Meta-Standard §2.7
