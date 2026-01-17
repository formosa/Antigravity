---
type: rule
name: "ISP Numpy Docstring"
globs:
  - "docs/07_isp/*.rst"
priority: 80
trigger:
  - "docstring"
  - "documentation"
  - "numpy"
severity: mandatory
description: "All ISP code must use Numpy-style docstrings with proper sections."
---
# ISP Numpy Docstring Rule

## Rule Statement

**ISP: All classes and methods MUST have Numpy-style docstrings with Parameters, Returns, and Raises sections.**

## Detection

| Pattern | Indication |
|:--------|:-----------|
| Missing docstring | Method without `"""..."""` |
| Wrong format | Google-style (`Args:`), reST-style |
| Missing sections | No Parameters, Returns, or Attributes |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Missing docstring | ERROR | Add Numpy-style docstring |
| Wrong format | WARNING | Convert to Numpy style |
| Missing sections | WARNING | Add required sections |

## Examples

### ✅ Correct

```python
def route_message(self, frame: list) -> bool:
    """
    Route incoming ZMQ frame to appropriate handler.

    Parameters
    ----------
    frame : list
        ZMQ multipart message [identity, metadata, payload].

    Returns
    -------
    bool
        True if message was successfully routed.
    """
    pass
```

### ❌ Incorrect (Google-style)

```python
def run(self):
    """Run the main loop.

    Args:
        None
    """
    pass
```

**Why**: Uses `Args:` instead of `Parameters`.

## References

- Knowledge: `constraints/isp_numpy_docstrings.md`
- Source: DDR Meta-Standard §2.7
