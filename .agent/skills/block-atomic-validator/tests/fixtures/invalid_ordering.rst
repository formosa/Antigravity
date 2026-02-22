================================================================================
TEST FIXTURE: Valid Block-Atomic Structure (valid_fsd.rst)
================================================================================

.. fsd:: Voice Interaction Pipeline
   :id: FSD-4
   :links: BRD-5, NFR-7

   Complete voice processing workflow from wake word to response.

.. fsd:: Wake Word Detection (Stage 1)
   :id: FSD-4.1
   :links: FSD-4

   Pvporcupine-based wake word detection with configurable sensitivity.

.. fsd:: Voice Activity Detection (Stage 2)
   :id: FSD-4.2
   :links: FSD-4

   Neural VAD refines Stage 1 output before speech recognition.

.. fsd:: Speech Recognition (Stage 3)
   :id: FSD-4.3
   :links: FSD-4

   Whisper-based ASR transcribes detected speech to text.

.. fsd:: Error Handling Strategy
   :id: FSD-7
   :links: BRD-2, NFR-5

   Comprehensive fault handling for distributed components.

.. fsd:: LogServer Fault
   :id: FSD-7.1
   :links: FSD-7

   Senders continue operation, drop logs silently on LogServer failure.

.. fsd:: Service Fault
   :id: FSD-7.2
   :links: FSD-7

   Core detects unresponsive services, marks unavailable, enters error state.

.. reconciliation_manifest:
   :section_id: "fsd-voice-pipeline"
   :integrity_status: "CLEAN"
   :timestamp: "2026-02-20"
   :tag_count: 7
   :tag_inventory: ["FSD-4", "FSD-4.1", "FSD-4.2", "FSD-4.3",
                    "FSD-7", "FSD-7.1", "FSD-7.2"]
   :pending_items: []


================================================================================
TEST FIXTURE: Invalid Ordering (invalid_ordering.rst)
================================================================================

.. fsd:: Wake Word Detection (Stage 1)
   :id: FSD-4.1
   :links: FSD-4

   ❌ ERROR: This atomic appears BEFORE its block parent

.. fsd:: Voice Interaction Pipeline
   :id: FSD-4
   :links: BRD-5, NFR-7

   ❌ ERROR: This block appears AFTER its atomic child FSD-4.1

.. fsd:: Voice Activity Detection (Stage 2)
   :id: FSD-4.2
   :links: FSD-4

   This one is correctly ordered after FSD-4


================================================================================
TEST FIXTURE: Invalid Citation (invalid_citation.rst)
================================================================================

.. fsd:: Voice Interaction Pipeline
   :id: FSD-4
   :links: BRD-5, NFR-7

   Block parent exists correctly.

.. fsd:: Wake Word Detection (Stage 1)
   :id: FSD-4.1
   :links: BRD-5

   ❌ ERROR: Links to BRD-5 but does NOT cite parent block FSD-4

.. fsd:: Voice Activity Detection (Stage 2)
   :id: FSD-4.2
   :links: NFR-7, BRD-5

   ❌ ERROR: Links to NFR-7 and BRD-5 but does NOT cite parent FSD-4


================================================================================
TEST FIXTURE: Orphaned Atomic (invalid_orphan.rst)
================================================================================

.. fsd:: Wake Word Detection (Stage 1)
   :id: FSD-4.1
   :links: FSD-4

   ❌ ERROR: Atomic tag FSD-4.1 exists but block FSD-4 does NOT exist

.. fsd:: Voice Activity Detection (Stage 2)
   :id: FSD-4.2
   :links: FSD-4

   ❌ ERROR: Another orphaned atomic - still no FSD-4 block

.. fsd:: Error Handling Strategy
   :id: FSD-7
   :links: BRD-2

   ✅ VALID: This is a proper block tag

.. fsd:: Service Fault
   :id: FSD-7.1
   :links: FSD-7

   ✅ VALID: Properly cites its block parent FSD-7


================================================================================
TEST FIXTURE: Prefix Mismatch (invalid_prefix.rst)
================================================================================

.. fsd:: Voice Interaction Pipeline
   :id: FSD-4
   :links: BRD-5

   Block parent with tier FSD

.. nfr:: Latency Constraint
   :id: NFR-4.1
   :links: FSD-4

   ❌ WARNING: Tier is NFR but atomic number implies parent is FSD-4
   Should be FSD-4.1, not NFR-4.1


================================================================================
TEST FIXTURE: Multiple Violations (invalid_multiple.rst)
================================================================================

.. fsd:: Orphaned atomic appears first
   :id: FSD-1.1
   :links: FSD-1

   ❌ ERROR: Orphaned (no FSD-1 exists)

.. fsd:: Missing block citation
   :id: FSD-2.1
   :links: BRD-3

   ❌ ERROR: Does not cite parent FSD-2

.. fsd:: Block appears after atomic
   :id: FSD-2
   :links: BRD-3

   ❌ ERROR: Ordering violation - should appear before FSD-2.1

.. nfr:: Prefix mismatch
   :id: NFR-2.2
   :links: FSD-2

   ❌ WARNING: Tier NFR but atomic suffix suggests FSD-2 parent


================================================================================
TEST FIXTURE: Complex Valid Structure (valid_complex.rst)
================================================================================

.. brd:: Privacy & Security
   :id: BRD-5

   Project must preserve user privacy.

.. brd:: Operate without cloud dependencies
   :id: BRD-5.1
   :links: BRD-5

   All processing occurs locally.

.. brd:: No data transmission
   :id: BRD-5.2
   :links: BRD-5

   Zero network activity during normal operation.

.. brd:: Verifiable isolation
   :id: BRD-5.3
   :links: BRD-5

   Users can audit system behavior.

.. brd:: Performance
   :id: BRD-8

   System must feel instantaneous to users.

.. brd:: Sub-250ms IPC dispatch
   :id: BRD-8.1
   :links: BRD-8

   Metadata-only messages complete under 250ms.

.. brd:: Under 1 second LLM response
   :id: BRD-8.2
   :links: BRD-8

   From query submission to response display.

.. reconciliation_manifest:
   :section_id: "brd-root"
   :integrity_status: "CLEAN"
   :timestamp: "2026-02-20"
   :tag_count: 7
   :tag_inventory: ["BRD-5", "BRD-5.1", "BRD-5.2", "BRD-5.3",
                    "BRD-8", "BRD-8.1", "BRD-8.2"]
   :pending_items: []
