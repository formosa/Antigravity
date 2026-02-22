====================================
System Architecture Document (SAD)
====================================

This is an INVALID SAD section - diagrams present but malformed.

.. sad:: Isolated Component
   :id: SAD-1
   :links: FSD-1

This diagram shows only a single isolated component with no relationships.
Violates SAD-DIAGRAM-003 (must show component relationships).

::

   +-------------+
   |    Core     |
   +-------------+

ERROR: No connections to other components!


.. sad:: Too Simple Diagram
   :id: SAD-2
   :links: FSD-2

This diagram is too simplistic and lacks structural clarity.
Violates SAD-DIAGRAM-004 (minimum structural clarity).

::

   Core --> UI

ERROR: Only 1 line, no boxes, insufficient structure!


.. sad:: Unrecognized Characters
   :id: SAD-3
   :links: FSD-3

This diagram uses non-standard characters that aren't recognized.
Violates SAD-DIAGRAM-002 (must use standard box characters).

::

   [Core Service] ===> [UI Service]
   {Process A} ~~~> {Process B}

ERROR: Using brackets and braces instead of proper box drawing characters!


.. sad:: Insufficient Components
   :id: SAD-4
   :links: FSD-4

This diagram has proper structure but shows only one component.
Violates SAD-DIAGRAM-003 (minimum 2 components for architecture).

::

   +------------------+
   | Single Component |
   | No relationships |
   +------------------+
         (alone)

ERROR: Architecture requires multiple interacting components!


.. sad:: Missing Labels
   :id: SAD-5
   :links: FSD-5

This diagram has structure but lacks component labels.
Violates SAD-DIAGRAM-004 (clarity requirement).

::

   +---+     +---+
   |   | --> |   |
   +---+     +---+

ERROR: Boxes have no identifying labels!


.. reconciliation_manifest:
   :section_id: "sad-test-invalid-malformed"
   :integrity_status: "DIRTY"
   :timestamp: "2026-02-20"
   :tag_count: 5
   :tag_inventory: ["SAD-1", "SAD-2", "SAD-3", "SAD-4", "SAD-5"]
   :pending_items: [
     {
       "target_tag": "SAD-1",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Diagram missing component relationships"
     },
     {
       "target_tag": "SAD-2",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Diagram lacks structural clarity"
     },
     {
       "target_tag": "SAD-3",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Diagram uses unrecognized characters"
     },
     {
       "target_tag": "SAD-4",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Insufficient components in diagram"
     },
     {
       "target_tag": "SAD-5",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Diagram missing component labels"
     }
   ]
