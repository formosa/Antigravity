---
archetype: protocol
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/information_flow.md
related:
  - protocols/reconciliation_inventory.md
  - protocols/impact_analysis.md
agents:
  - tag_reconciler
  - manifest_manager
---

# Reconciliation Dirty Flag

> **Scope**: Protocol for setting, propagating, and clearing DIRTY integrity status.
>
> **Excludes**: Tag inventory maintenance; impact analysis.

## Summary

The dirty flag (`integrity_status: "DIRTY"`) signals that a documentation section contains unresolved inconsistencies. This protocol defines when to set the flag, how changes propagate, and when the flag can be cleared.

## Prerequisites

- Access to reconciliation manifests
- Knowledge of modification type
- Understanding of downstream dependencies

## Procedure

### Step 1: Detect Trigger Event

Events that trigger DIRTY status:

| Event | Affected Section(s) |
|:------|:--------------------|
| Tag content modified | Section containing tag + all citing sections |
| Tag added | Section containing tag |
| Tag deleted | Section containing tag + all citing sections |
| Parent tag modified | All child-citing sections |
| Citation added/removed | Section containing tag |

### Step 2: Set Dirty Flag

Update the section's reconciliation manifest:

```rst
.. reconciliation_manifest:
   :section_id: fsd-root
   :integrity_status: "DIRTY"      ← Changed from "CLEAN"
   :timestamp: "2026-01-16"
   :pending_items: [
     {
       "target_tag": "FSD-4.2",
       "source_trigger": "BRD-5.2 modified",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Latency target changed from <1s to <500ms"
     }
   ]
```

### Step 3: Propagate Downstream

For parent modifications, set DIRTY on all downstream sections:

```
BRD section modified
  → Set NFR section DIRTY
    → Set FSD section DIRTY
      → Set SAD section DIRTY
        → ... cascade continues
```

### Step 4: Record Pending Items

Each affected tag gets a pending item entry:

```json
{
  "target_tag": "FSD-4.2",
  "source_trigger": "BRD-5.2 modified",
  "issue_type": "CONSTRAINT_VIOLATION",
  "description": "Human-readable explanation"
}
```

**Issue Types**:
- `CONSTRAINT_VIOLATION`: Parent constraint changed
- `MISSING_PARENT`: Cited tag not found
- `ORPHAN`: No parent citation

### Step 5: Clear Flag (Resolution)

DIRTY status may ONLY be cleared when:
1. All `pending_items` have been resolved
2. A dedicated reconciliation pass has validated consistency
3. Human or agent has confirmed alignment

**Clear procedure**:
```rst
.. reconciliation_manifest:
   :section_id: fsd-root
   :integrity_status: "CLEAN"
   :timestamp: "2026-01-16"
   :pending_items: []
```

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Flag set | Trigger event occurred | Begin reconciliation |
| Flag propagated | Downstream sections flagged | Schedule cascade review |
| Flag cleared | All items resolved | Document resolution |

---

## References

- `protocols/reconciliation_inventory.md` — Tag count maintenance
- `protocols/impact_analysis.md` — Finding affected sections
- Source: `ddr_meta_standard.txt` §4.2, §4.3
