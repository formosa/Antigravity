---
archetype: concept
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/tier_sad.md
related:
  - concepts/tier_tdd.md
tiers:
  - ICD
agents:
  - icd_dataengineer
---

# Tier: ICD

> **Scope**: Definition, boundaries, and content requirements for the Interface & Contract Definitions tier.
>
> **Excludes**: ICD authoring protocols; specific constraint enforcement rules.

## Summary

The ICD (Interface & Contract Definitions) is Tier 5 of the DDR hierarchy. It defines data shapes and communication contracts by answering "What are the message/data formats?" ICD specifies the precise schemas that enable component integration.

## Definition

The **ICD tier** captures configuration schemas, message formats, payload structures, and API contracts—the concrete data shapes that components exchange.

## Characteristics

| Attribute | Value |
|:----------|:------|
| **Layer** | Contracts |
| **Question** | "What are the data shapes?" |
| **Persona** | Data Engineer |
| **Audience** | Developers, integrators |
| **Tag Format** | `ICD-N` (block), `ICD-N.M` (atomic) |

### Key Content

- Configuration file schemas (YAML)
- Message frame structures
- Metadata schemas (JSON)
- Request/response payload formats
- API contracts

### Citation Requirements

- ICD tags MUST cite SAD (topology) and NFR (constraints) tags
- Schema definitions trace to architectural decisions

### Format Requirements

| Format | Usage |
|:-------|:------|
| YAML | Configuration files |
| JSON | Metadata and payloads |
| Code blocks | Language-specific with syntax highlighting |

### Example Schema

```json
{
  "source": "UI | Audio | Runtime | Core",
  "destination": "Target_Service_Name",
  "command": "function_name_or_signal",
  "request_id": "uuid-v4-string",
  "timestamp": "ISO-8601-string",
  "priority": 1,
  "payload_type": "json | binary | text"
}
```

## Context

ICD bridges architecture to implementation:
- **Cites**: SAD tags, NFR tags
- **Cited by**: TDD tags
- **File location**: `docs/05_icd/`

---

## References

- `concepts/tier_sad.md` — Parent tier (structure)
- `concepts/tier_tdd.md` — Next tier (blueprints)
- Source: `ddr_meta_standard.txt` §2.5 Interface & Data Schemas
