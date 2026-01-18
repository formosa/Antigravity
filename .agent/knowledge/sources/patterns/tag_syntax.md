---
archetype: pattern
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
related:
  - constraints/tag_immutability.md
  - constraints/tag_citation_required.md
---

# Tag Syntax

> **Scope**: Format specification for DDR tag IDs and RST directive syntax.
>
> **Excludes**: Citation rules; tag lifecycle.

## Summary

DDR tags use a consistent format: tier prefix, hyphen, sequential integer, optional atomic suffix. Tags are defined using Sphinx-Needs RST directives with required `:id:` and `:links:` fields.

## Structure

### ID Format

```
|TIER-N|        Block-level tag
|TIER-N.M|      Atomic-level tag
```

| Component | Format | Examples |
|:----------|:-------|:---------|
| Tier prefix | Uppercase 3-letter abbreviation | BRD, NFR, FSD, SAD, ICD, TDD, ISP |
| Separator | Hyphen | `-` |
| Block number | Sequential integer (no padding) | 1, 2, 10, 99 |
| Atomic suffix | `.` + sequential integer | .1, .2, .10 |

### RST Directive Syntax

```rst
.. tier:: Title or Description
   :id: TIER-N
   :links: PARENT-X, PARENT-Y
```

## Fields

| Field | Required | Type | Description |
|:------|:--------:|:-----|:------------|
| Directive | Yes | `.. tier::` | Tier name lowercase (brd, nfr, fsd, etc.) |
| Title | Yes | string | Human-readable description |
| `:id:` | Yes | TAG-ID | Unique identifier in correct format |
| `:links:` | Conditional | TAG-ID list | Parent citations (required for non-BRD) |

## Usage Examples

### Basic

```rst
.. brd:: Project Purpose
   :id: BRD-1
```

### Complete

```rst
.. nfr:: Latency & Throughput
   :id: NFR-4
   :links: BRD-8

.. nfr:: IPC Dispatch: Sub-millisecond (< 1ms) for metadata-only.
   :id: NFR-4.1
   :links: NFR-4

.. nfr:: LLM Inference: < 1s average response time.
   :id: NFR-4.2
   :links: NFR-4
```

### Multi-Parent Citation

```rst
.. tdd:: CoreProcess class structure.
   :id: TDD-1
   :links: SAD-2, FSD-1.1, ICD-1
```

## Anti-Patterns

### ❌ Wrong Delimiters

```rst
[BRD-1]   ← WRONG: Square brackets
{BRD-1}   ← WRONG: Curly braces
```
**Problem**: Only pipe delimiters (`|BRD-1|`) are valid for inline references.

### ❌ Zero Padding

```rst
:id: BRD-01
:id: NFR-001
```
**Problem**: IDs must be plain integers without leading zeros.

### ❌ Wrong Separator

```rst
:id: BRD_1   ← WRONG: Underscore
:id: BRD.1   ← WRONG: Dot (that's atomic format)
```
**Problem**: Tier and number separated by hyphen only.

### ❌ Lowercase Prefix

```rst
:id: brd-1
:id: Brd-1
```
**Problem**: Tier prefix must be UPPERCASE.

---

## References

- `constraints/tag_immutability.md` — ID permanence
- `constraints/tag_citation_required.md` — Links requirement
- Source: `ddr_meta_standard.txt` §3.1 Tag Format Specification
