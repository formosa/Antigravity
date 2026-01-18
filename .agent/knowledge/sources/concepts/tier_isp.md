---
archetype: concept
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/tier_tdd.md
related:
  - constraints/isp_stub_only.md
  - constraints/isp_numpy_docstrings.md
tiers:
  - ISP
agents:
  - isp_codegenerator
---

# Tier: ISP

> **Scope**: Definition, boundaries, and content requirements for the Implementation Stubs & Prompts tier.
>
> **Excludes**: ISP authoring protocols; specific constraint enforcement rules.

## Summary

The ISP (Implementation Stubs & Prompts) is Tier 7 of the DDR hierarchy. It provides executable code skeletons by answering "What is the starting point for coding?" ISP is the terminal tier—fully traceable to business objectives.

## Definition

The **ISP tier** captures Python class stubs with comprehensive Numpy-style docstrings, type hints, and inline traceability citations. Method bodies contain only `pass` statements.

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Prompts |
| **Question** | "What is the code skeleton?" |
| **Persona** | Code Generator |
| **Audience** | Developers, AI coding assistants |
| **Tag Format** | `ISP-N` (block), `ISP-N.M` (atomic) |

### Key Content

- Python class stubs
- Method signatures with type hints
- Numpy-style docstrings
- Inline citation comments (`Implements: |TDD-X|`)
- `pass` statements for logic placeholders

### Citation Requirements

- ISP tags MUST cite TDD tags for every structural element
- Docstrings include `Implements:` and `Requirements:` citations

### Docstring Requirements

| Section | Content |
|:--------|:--------|
| Description | One-line summary |
| Parameters | All arguments with types |
| Returns | Return type and description |
| Implements | TDD tag citations |
| Requirements | FSD/NFR tag citations |

### Critical Constraints

| Constraint | Rule |
|:-----------|:-----|
| Stub Only | Method bodies contain only `pass` |
| No Logic | No algorithms, control flow, or business logic |
| Numpy Format | Docstrings follow Numpy style |
| Full Traceability | Every method cites TDD source |

### Example

```python
class CoreProcess:
    """
    Orchestrates IPC between services using ZeroMQ ROUTER pattern.

    Ref: |TDD-1|, |FSD-1|

    Parameters
    ----------
    config_path : str
        Path to ipc_config.yaml file.
    """
    def __init__(self, config_path: str):
        """
        Initialize ZMQ Context, Bind ROUTER socket.

        Implements: |TDD-1.3|, |TDD-1.5|
        """
        pass
```

## Context

ISP is the terminal tier—everything traces back:
- **Cites**: TDD tags
- **Cited by**: (none—terminal tier)
- **File location**: `docs/07_isp/`

---

## References

- `concepts/tier_tdd.md` — Parent tier (blueprints)
- `constraints/isp_stub_only.md` — Pass-only rule
- `constraints/isp_numpy_docstrings.md` — Docstring format
- Source: `ddr_meta_standard.txt` §2.7 Implementation Stubs & Prompts
