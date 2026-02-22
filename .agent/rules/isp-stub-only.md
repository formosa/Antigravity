---
type: rule
name: isp-stub-only
activation: glob
globs:
  - "docs/07_isp/*.rst"
priority: 80
severity: mandatory
description: "ISP method bodies must contain only pass statements—no implementation logic."
---
# ISP Stub Only Rule

## Rule Statement

**ISP: All method/function bodies MUST contain only `pass` statements. No implementation logic allowed.**

## Detection

| Pattern             | Examples                        |
| :------------------ | :------------------------------ |
| Actual code         | `self.socket = zmq.Context()`   |
| Control flow        | `if condition:`, `for item in:` |
| Return values       | `return result`                 |
| Variable assignment | `data = process()`              |

## Enforcement

| Violation              | Severity   | Resolution             |
| :--------------------- | :--------: | :--------------------- |
| Any code beyond `pass` | ERROR      | Replace with `pass`    |
| Return statement       | ERROR      | Remove; use `pass`     |
| Logic in body          | ERROR      | Move to implementation |

## Examples

### ✅ Correct

```python
def route_message(self, frame: list) -> None:
    """Route incoming message to appropriate handler."""
    pass
```

### ❌ Incorrect

```python
def __init__(self, config_path: str):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.ROUTER)
```

**Why**: Contains implementation. Replace with `pass`.

## Related Rules

- [isp-numpy-docstring.md](isp-numpy-docstring.md) — Numpy-style docstring format
- [isp-traceability-required.md](isp-traceability-required.md) — Implements/Requirements citations

## References

- Knowledge: `constraints/isp-stub-only.md`
- Source: DDR Meta-Standard §2.7