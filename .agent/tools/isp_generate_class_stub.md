---
type: tool
name: "generate_class_stub"
description: "Generates Python class stub from TDD specification with Numpy-style docstring and pass-only __init__."
command: ".venv\\Scripts\\python .agent/scripts/generate_class_stub.py --tdd-id \"${tdd_id}\" --needs-json \"${needs_json}\""
runtime: system
confirmation: never
args:
  tdd_id:
    description: "TDD tag ID"
    required: true
  needs_json:
    description: "Path to needs.json (default: docs/_build/json/needs.json)"
    required: false
  output:
    description: "Output file path (default: stdout)"
    required: false
---

# Tool: Generate Class Stub

## Overview

Creates ISP-compliant Python class stub from TDD tag with Numpy docstring and pass-only `__init__`.

## Knowledge Sources

- **Stub Only**: `.agent/knowledge/sources/constraints/isp_stub_only.md`
- **Numpy Docstrings**: `.agent/knowledge/sources/constraints/isp_numpy_docstrings.md`

## Configuration

- **Entry Point**: `.agent/scripts/generate_class_stub.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--tdd-id`: Required. TDD tag ID.
    - `--needs-json`: Optional. Path to needs.json.
    - `--output`: Optional. Output file path.

## Protocol & Validation

### Success Verification
1. Valid Python class definition
2. Docstring includes `Ref: |TDD-xxx|`
3. `__init__` contains only `pass`

### Example Output
```python
class UserAuthentication:
    """
    Handles user login.

    Ref: |TDD-1|
    """

    def __init__(self):
        """Initialize UserAuthentication."""
        pass
```

## Rules
- **Stub-Only**: Methods contain only `pass`
- **TDD Reference Required**: Must link to source TDD
