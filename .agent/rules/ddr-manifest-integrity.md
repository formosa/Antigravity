---
type: rule
name: ddr-manifest-integrity
activation: model_decision
priority: 50
severity: mandatory
---
# DDR Manifest Integrity Rule

## Rule Statement

**After any tag modification, update the reconciliation manifest to maintain synchronization.**

## Trigger Events

| Event                  | Affected Section(s)           |
| :--------------------- | :---------------------------- |
| Tag content modified   | Section + all citing sections |
| Tag added              | Section containing tag        |
| Tag deleted            | Section + all citing sections |
| Parent tag modified    | All child-citing sections     |
| Citation added/removed | Section containing tag        |

## Enforcement Protocol

1. **Update inventory**: Recalculate `:tag_count:` and `:tag_inventory:`
2. **Set dirty flag**: Change `:integrity_status:` to `DIRTY` if dependencies affected
3. **Record pending items**: Add entries to `:pending_items:` for conflicts
4. **Propagate downstream**: DIRTY cascades to all citing sections

## Issue Types

| Type                   | Meaning                   |
| :--------------------- | :------------------------ |
| `CONSTRAINT_VIOLATION` | Parent constraint changed |
| `MISSING_PARENT`       | Cited tag not found       |
| `ORPHAN`               | No parent citation        |

## Clear Conditions

DIRTY status may ONLY be cleared when:

1. All `pending_items` resolved
2. Reconciliation pass validated consistency
3. Human or agent confirmed alignment

## References

- Knowledge: `protocols/reconciliation-dirty-flag.md`
- Knowledge: `protocols/reconciliation-inventory.md`
- Source: DDR Meta-Standard §4.2, §4.3