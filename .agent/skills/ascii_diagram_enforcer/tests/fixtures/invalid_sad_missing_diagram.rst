====================================
System Architecture Document (SAD)
====================================

This is an INVALID SAD section - missing mandatory ASCII diagrams.

.. sad:: Hub-and-Spoke Architecture
   :id: SAD-1
   :links: FSD-1

The system follows a hub-and-spoke pattern with Core as the central router
orchestrating communication between all peripheral services.

**ERROR: No diagram present!**

This section describes the architecture in prose but fails to provide
the mandatory ASCII topology diagram required by DDR System rules.


.. sad:: IPC Message Flow
   :id: SAD-2
   :links: FSD-1.1

Message flow follows a strict request-reply pattern with correlation tracking
via request_id fields.

Again, no diagram is provided here. This violates SAD-DIAGRAM-001.


.. sad:: Processing Pipeline
   :id: SAD-3
   :links: FSD-4

The processing pipeline consists of multiple stages:

1. Wake word detection
2. Voice activity detection
3. Speech recognition
4. Intent processing
5. Response generation

While this describes the stages, there is no visual diagram showing
the architectural flow between components.


.. reconciliation_manifest:
   :section_id: "sad-test-invalid-missing"
   :integrity_status: "DIRTY"
   :timestamp: "2026-02-20"
   :tag_count: 3
   :tag_inventory: ["SAD-1", "SAD-2", "SAD-3"]
   :pending_items: [
     {
       "target_tag": "SAD-1",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Missing mandatory ASCII diagram"
     },
     {
       "target_tag": "SAD-2",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Missing mandatory ASCII diagram"
     },
     {
       "target_tag": "SAD-3",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Missing mandatory ASCII diagram"
     }
   ]
