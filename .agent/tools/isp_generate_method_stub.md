---
type: tool
name: "generate_method_stub"
description: "Generates Python method stub with complete Numpy-style docstring including Parameters, Returns, and Raises sections."
command: ".venv\\Scripts\\python .agent/scripts/generate_method_stub.py --name \"${name}\" --tdd-ref \"${tdd_ref}\""
runtime: system
confirmation: never
args:
  name:
    description: "Method name"
    required: true
  tdd_ref:
    description: "TDD tag reference"
    required: true
  params:
    description: "Parameters: name:type:desc,..."
    required: false
  return_type:
    description: "Return type (default: None)"
    required: false
  fsd_ref:
    description: "FSD tag reference"
    required: false
  raises:
    description: "Exceptions: Type:condition,..."
    required: false
---

# Tool: Generate Method Stub

## Overview

Creates ISP-compliant method stub with Numpy docstring and traceability links.

## Knowledge Sources

- **Stub Only**: `.agent/knowledge/sources/constraints/isp_stub_only.md`
- **Numpy Docstrings**: `.agent/knowledge/sources/constraints/isp_numpy_docstrings.md`

## Configuration

- **Entry Point**: `.agent/scripts/generate_method_stub.py`
- **Interpreter**: `.venv/Scripts/python`
- **Arguments**:
    - `--name`: Required. Method name.
    - `--tdd-ref`: Required. TDD reference.
    - `--params`: Optional. Parameters.
    - `--return-type`: Optional. Return type.
    - `--fsd-ref`: Optional. FSD reference.
    - `--raises`: Optional. Exceptions.

## Protocol & Validation

### Success Verification
1. Valid Python method definition
2. Docstring includes `Implements: |TDD-xxx|`
3. Body contains only `pass`

### Example Output
```python
def process_message(self, message: str) -> bool:
    """
    Process message.

    Implements: |TDD-1.2|

    Parameters
    ----------
    message : str
        Message content.

    Returns
    -------
    bool
        Success status.
    """
    pass
```

## Rules
- **Stub-Only**: Body contains only `pass`
- **TDD Reference Required**: `Implements:` line mandatory
