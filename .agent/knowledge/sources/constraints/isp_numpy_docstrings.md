---
archetype: constraint
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_isp.md
related:
  - constraints/isp_stub_only.md
tiers:
  - ISP
agents:
  - isp_codegenerator
---

# ISP Numpy Docstrings

> **Scope**: Rule that all ISP code must use Numpy-style docstrings with traceability citations.
>
> **Excludes**: Pass-only rule; ISP structure.

## Summary

All ISP classes, methods, and functions must include comprehensive Numpy-style docstrings. Docstrings must include traceability citations (`Implements:`, `Requirements:`) linking back to TDD and FSD/NFR tags.

## Rule Statement

**ISP: All classes and methods MUST have Numpy-style docstrings with `Implements:` and `Requirements:` citations.**

## Rationale

- Numpy format is IDE-friendly and widely recognized
- Citations enable bi-directional traceability
- Comprehensive docstrings support AI code generation
- Structured format enables automated extraction

## Detection

How to identify violations:

| Pattern | Examples |
|:--------|:---------|
| Missing docstring | Method without `"""..."""` |
| Wrong format | Google-style, reST-style docstrings |
| Missing sections | No Parameters, Returns, or Attributes |
| Missing citations | No `Implements:` or `Requirements:` |
| Invalid tag format | `TDD-1` without pipe delimiters |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Missing docstring | ERROR | Add Numpy-style docstring |
| Wrong format | WARNING | Convert to Numpy style |
| Missing `Implements:` | ERROR | Add TDD citation |
| Invalid citation format | WARNING | Use `|TAG-X|` format |

## Examples

### ✅ Correct

**Class docstring**:
```python
class CoreProcess:
    """
    Orchestrates IPC between services using ZeroMQ ROUTER pattern.

    Ref: |TDD-1|, |FSD-1|

    Parameters
    ----------
    config_path : str
        Path to ipc_config.yaml file.

    Attributes
    ----------
    active_requests : Dict[str, Tuple[bytes, float, str]]
        Tracks in-flight requests by request_id.
    queue : queue.PriorityQueue
        Internal message queue for non-blocking dispatch.
    """
```

**Method docstring**:
```python
def route_message(self, frame: list) -> bool:
    """
    Route incoming ZMQ frame to appropriate handler.

    Implements: |TDD-1.4|
    Requirements: |FSD-1.1|

    Parameters
    ----------
    frame : list
        ZMQ multipart message [identity, metadata, payload].

    Returns
    -------
    bool
        True if message was successfully routed.

    Raises
    ------
    ValueError
        If frame format is invalid.
    """
    pass
```

### ❌ Incorrect

**Missing docstring**:
```python
def run(self):
    pass
```
**Why**: No docstring at all.

**Wrong format (Google-style)**:
```python
def run(self):
    """Run the main loop.

    Args:
        None

    Returns:
        None
    """
    pass
```
**Why**: Uses Google-style `Args:` instead of Numpy-style `Parameters`.

**Missing citations**:
```python
def run(self):
    """
    Run the main event loop.

    Parameters
    ----------
    None
    """
    pass
```
**Why**: No `Implements:` or `Requirements:` lines.

---

## References

- `concepts/tier_isp.md` — ISP tier definition
- `constraints/isp_stub_only.md` — Pass-only requirement
- Source: `ddr_meta_standard.txt` §2.7 Docstring Requirements
