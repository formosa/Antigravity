====================================
System Architecture Document (SAD)
====================================

This is a valid SAD section with proper ASCII diagrams for testing.

.. sad:: Hub-and-Spoke Architecture
   :id: SAD-1
   :links: FSD-1

The system follows a hub-and-spoke pattern with Core as the central router
orchestrating communication between all peripheral services.

**Topology Diagram:**

::

   +---------------+          +------------------+          +-----------------+
   |  UI (DEALER)  | <------> |   Core (ROUTER)  | <------> | Runtime (DEALER)|
   +---------------+          +------------------+          +-----------------+
                                      |
                                      v
                              +------------------+
                              | Audio (DEALER)   |
                              +------------------+

.. sad:: Core Process Details
   :id: SAD-1.1
   :links: SAD-1

The Core process binds a ROUTER socket and manages request/response routing.
Atomic tags inherit diagram requirements from parent block.


.. sad:: IPC Message Flow
   :id: SAD-2
   :links: FSD-1.1

Message flow follows a strict request-reply pattern with correlation tracking
via request_id fields.

**Message Flow Diagram:**

::

   Client Service             Core (ROUTER)           Target Service
   +-------------+            +-------------+         +-------------+
   |             |  Request   |             |         |             |
   |   DEALER    |----------->|   Queue     |-------->|   Handler   |
   |             |            |             |         |             |
   |             |  Response  |             |         |             |
   |             |<-----------|   Dispatch  |<--------|             |
   +-------------+            +-------------+         +-------------+


.. sad:: Error Handling Topology
   :id: SAD-3
   :links: FSD-7

Fault tolerance through decoupled logging and graceful degradation.

**Error Topology:**

::

                     ┌──────────────┐
                     │     Core     │
                     └──────┬───────┘
                            │
                    ┌───────┼────────┐
                    │       │        │
                ┌───▼───┐ ┌─▼──┐ ┌──▼───┐
                │  UI   │ │Audio│ │Runtime│
                └───┬───┘ └─┬──┘ └──┬───┘
                    │       │       │
                    └───────┼───────┘
                            │
                      ┌─────▼──────┐
                      │ LogServer  │
                      │   (PULL)   │
                      └────────────┘


.. reconciliation_manifest:
   :section_id: "sad-test-valid"
   :integrity_status: "CLEAN"
   :timestamp: "2026-02-20"
   :tag_count: 4
   :tag_inventory: ["SAD-1", "SAD-1.1", "SAD-2", "SAD-3"]
   :pending_items: []
