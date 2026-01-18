---
archetype: pattern
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
related:
  - protocols/reconciliation_dirty_flag.md
  - protocols/reconciliation_inventory.md
---

# Manifest Structure

> **Scope**: Format specification for reconciliation manifest blocks.
>
> **Excludes**: Dirty flag protocols; inventory maintenance procedures.

## Summary

Reconciliation manifests track document integrity state at the section level. Every major documentation section must include a manifest block at the end, recording tag inventory, integrity status, and pending issues.

## Structure

```rst
.. reconciliation_manifest:
   :section_id: "unique-section-name"
   :integrity_status: "CLEAN" | "DIRTY"
   :timestamp: "YYYY-MM-DD"
   :tag_count: <integer>
   :tag_inventory: ["TAG-1", "TAG-1.1", ...]
   :pending_items: [<issue objects>]
```

## Fields

| Field | Required | Type | Description |
|:------|:--------:|:-----|:------------|
| `:section_id:` | Yes | string | Unique identifier for section (e.g., "fsd-root") |
| `:integrity_status:` | Yes | enum | "CLEAN" or "DIRTY" |
| `:timestamp:` | Yes | date | Last update date (YYYY-MM-DD) |
| `:tag_count:` | Yes | integer | Count of tags in `:tag_inventory:` |
| `:tag_inventory:` | Yes | array | Complete list of all tag IDs in section |
| `:pending_items:` | Yes | array | List of issue objects (empty if CLEAN) |

### Issue Object Schema

```json
{
  "target_tag": "TAG-ID",
  "source_trigger": "PARENT-TAG modified|deleted",
  "issue_type": "CONSTRAINT_VIOLATION|MISSING_PARENT|ORPHAN",
  "description": "Human-readable explanation"
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `target_tag` | string | Tag affected by the issue |
| `source_trigger` | string | What caused the issue |
| `issue_type` | enum | Category of problem |
| `description` | string | Human-readable details |

## Usage Examples

### Basic (Clean State)

```rst
.. reconciliation_manifest:
   :section_id: "brd-root"
   :integrity_status: "CLEAN"
   :timestamp: "2026-01-16"
   :tag_count: 12
   :tag_inventory: ["BRD-1", "BRD-2", "BRD-2.1", "BRD-2.2", "BRD-2.3",
                    "BRD-3", "BRD-4", "BRD-5", "BRD-5.1", "BRD-5.2",
                    "BRD-6", "BRD-7"]
   :pending_items: []
```

### Complete (Dirty State)

```rst
.. reconciliation_manifest:
   :section_id: "fsd-root"
   :integrity_status: "DIRTY"
   :timestamp: "2026-01-16"
   :tag_count: 46
   :tag_inventory: ["FSD-1", "FSD-1.1", "FSD-1.2", "FSD-1.3", "FSD-1.4",
                    "FSD-2", "FSD-2.1", "FSD-2.2", "FSD-2.3",
                    ...,
                    "FSD-9", "FSD-9.1", "FSD-9.2", "FSD-9.3", "FSD-9.4"]
   :pending_items: [
     {
       "target_tag": "FSD-4.2",
       "source_trigger": "BRD-5.2 modified",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Latency target changed from <1s to <500ms"
     },
     {
       "target_tag": "FSD-7.5",
       "source_trigger": "NFR-3 deleted",
       "issue_type": "MISSING_PARENT",
       "description": "Parent citation no longer exists"
     }
   ]
```

## Anti-Patterns

### ❌ Missing Manifest

Section ends without reconciliation block.

**Problem**: No way to track integrity state or tag inventory.

### ❌ Mismatched Count

```rst
:tag_count: 10
:tag_inventory: ["FSD-1", "FSD-2", "FSD-3"]  ← Only 3 items
```

**Problem**: Count must equal inventory length.

### ❌ Stale Inventory

Inventory lists tags that no longer exist in section text.

**Problem**: Creates false positive tag references.

---

## References

- `protocols/reconciliation_dirty_flag.md` — When to set DIRTY
- `protocols/reconciliation_inventory.md` — Inventory maintenance
- Source: `ddr_meta_standard.txt` §4.2 Reconciliation Manifest System
