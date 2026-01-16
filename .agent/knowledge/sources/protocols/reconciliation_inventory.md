---
archetype: protocol
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
related:
  - protocols/reconciliation_dirty_flag.md
agents:
  - manifest_manager
---

# Reconciliation Inventory

> **Scope**: Protocol for maintaining accurate tag counts and inventories in reconciliation manifests.
>
> **Excludes**: Dirty flag handling; impact analysis.

## Summary

Every reconciliation manifest must maintain an accurate inventory of all tags in its section. This protocol defines how to update `tag_count` and `tag_inventory` when tags are added, removed, or restructured.

## Prerequisites

- Access to section's reconciliation manifest
- List of all tags currently in section text
- Understanding of block vs. atomic tags

## Procedure

### Step 1: Parse Current Inventory

Extract existing inventory from manifest:

```rst
.. reconciliation_manifest:
   :tag_count: 46
   :tag_inventory: ["FSD-1", "FSD-1.1", "FSD-1.2", ..., "FSD-9.4"]
```

### Step 2: Scan Section Text

Parse the section content to find all tag definitions:

```rst
.. fsd:: Process Orchestration
   :id: FSD-1          ← Add to inventory

.. fsd:: Core (Hub)
   :id: FSD-1.1        ← Add to inventory
```

### Step 3: Reconcile Differences

Compare scanned tags against inventory:

| Situation | Action |
|:----------|:-------|
| Tag in text, not in inventory | Add to `tag_inventory` |
| Tag in inventory, not in text | Remove from `tag_inventory` |
| Counts match | No action |

### Step 4: Handle Block Deletions

If a block tag is deleted, ALL its atomic children must also be removed:

**Deleted**: FSD-1

**Remove**:
- FSD-1
- FSD-1.1
- FSD-1.2
- FSD-1.3
- ... (all FSD-1.x)

### Step 5: Update Manifest

Recalculate count and update inventory:

```rst
.. reconciliation_manifest:
   :tag_count: 44           ← Updated count
   :tag_inventory: ["FSD-2", "FSD-2.1", ..., "FSD-9.4"]  ← Updated list
```

### Step 6: Verify Accuracy

Final validation checks:
- `tag_count` equals length of `tag_inventory`
- All inventory items exist in section text
- No duplicate entries in inventory
- Block tags appear before their atomics

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Synchronized | Inventory matches text | Set timestamp |
| Discrepancy found | Mismatch detected | Apply corrections |
| Bulk change | Many adds/removes | Run full reconciliation |

---

## References

- `protocols/reconciliation_dirty_flag.md` — When to flag changes
- Source: `ddr_meta_standard.txt` §4.3 Rule 1: Inventory Maintenance
