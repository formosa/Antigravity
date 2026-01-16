---
archetype: constraint
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_isp.md
related:
  - constraints/isp_numpy_docstrings.md
tiers:
  - ISP
agents:
  - isp_codegenerator
---

# ISP Stub Only

> **Scope**: Rule that ISP method bodies must contain only `pass` statements.
>
> **Excludes**: Docstring requirements; ISP structure.

## Summary

ISP (Implementation Stubs & Prompts) provides code skeletons, not implementations. Method bodies must contain only `pass` statements—no algorithms, control flow, API calls, or business logic. The implementation is the developer's responsibility.

## Rule Statement

**ISP: All method/function bodies MUST contain only `pass` statements. No implementation logic allowed.**

## Rationale

- ISP is a starting point, not a finished product
- Actual implementation requires developer judgment
- Stubs ensure structural correctness without prescribing logic
- Pass-only bodies are clearly incomplete, preventing confusion

## Detection

How to identify violations:

| Pattern | Examples |
|:--------|:---------|
| Actual code | `self.socket = zmq.Context()` |
| Control flow | `if condition:`, `for item in:` |
| Return values | `return result` |
| Variable assignment | `data = process()` |
| API calls | `zmq.Context()` |
| Exceptions | `raise ValueError()` |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Any code beyond `pass` | ERROR | Replace with `pass` |
| Return statement | ERROR | Remove; use `pass` |
| Logic in body | ERROR | Move to implementation |

## Examples

### ✅ Correct

```python
class CoreProcess:
    """Orchestrates IPC between services."""

    def __init__(self, config_path: str):
        """
        Initialize ZMQ Context and bind ROUTER socket.

        Implements: |TDD-1.3|, |TDD-1.5|
        """
        pass

    def run(self) -> None:
        """
        Main event loop processing message queue.

        Implements: |TDD-1.8|
        """
        pass

    def route_message(self, frame: list) -> None:
        """
        Route incoming message to appropriate handler.

        Implements: |TDD-1.4|
        """
        pass
```

### ❌ Incorrect

```python
def __init__(self, config_path: str):
    """Initialize ZMQ Context."""
    self.context = zmq.Context()        # WRONG: Actual code
    self.socket = self.context.socket(zmq.ROUTER)
```
**Why**: Contains implementation. Replace entire body with `pass`.

```python
def run(self) -> None:
    """Main event loop."""
    while True:                          # WRONG: Control flow
        msg = self.socket.recv()
        self.handle(msg)
```
**Why**: Contains logic. Replace entire body with `pass`.

```python
def get_status(self) -> str:
    """Return current status."""
    return self.status                   # WRONG: Return statement
```
**Why**: Returns value. Replace with `pass`.

---

## References

- `concepts/tier_isp.md` — ISP tier definition
- `constraints/isp_numpy_docstrings.md` — Docstring requirement
- Source: `ddr_meta_standard.txt` §2.7 Implementation Stubs & Prompts
