NFR — System Constraints (Boundaries)
====================================================================================================

Hardware & Environment Limits


.. nfr:: Target Environment
   :id: NFR-1
   :links: BRD-6

.. nfr:: **CPU:** AMD Ryzen 9 5900X (Audio/Core must run here).
   :id: NFR-1.1
   :links: NFR-1

.. nfr:: **GPU:** RTX 3080 10GB VRAM (Runtime/Inference only).
   :id: NFR-1.2
   :links: NFR-1

.. nfr:: **RAM:** 32GB System Memory.
   :id: NFR-1.3
   :links: NFR-1

.. nfr:: **OS:** Windows 11 Pro x64.
   :id: NFR-1.4
   :links: NFR-1

.. nfr:: **Python:** Version >= 3.11.
   :id: NFR-1.5
   :links: NFR-1

.. nfr:: **CUDA:** Toolkit installed for GPU inference.
   :id: NFR-1.6
   :links: NFR-1



.. nfr:: Security & Network
   :id: NFR-2
   :links: BRD-3,BRD-6

.. nfr:: All communication limited to local TCP sockets (`127.0.0.1`) via ZeroMQ.
   :id: NFR-2.1
   :links: NFR-2

.. nfr:: No cloud dependencies allowed for runtime operations.
   :id: NFR-2.2
   :links: NFR-2



.. nfr:: Resource Isolation
   :id: NFR-3
   :links: BRD-3,BRD-6

.. nfr:: **CPU Idle:** Processes polling for IPC messages must consume <5% CPU when idle.
   :id: NFR-3.1
   :links: NFR-3

.. nfr:: **Audio Priority:** CPU-bound services (Audio) must prioritize low-latency over idle CPU.
   :id: NFR-3.2
   :links: NFR-3

.. nfr:: **Memory Footprint (Core Queue):** 1000 cap, ~10-50 MB.
   :id: NFR-3.3
   :links: NFR-3

.. nfr:: **Memory Footprint (UI Queue):** 100 cap, ~1-5 MB.
   :id: NFR-3.4
   :links: NFR-3

.. nfr:: **Memory Footprint (Runtime Queue):** 50 cap, ~5-25 MB.
   :id: NFR-3.5
   :links: NFR-3

.. nfr:: **Memory Footprint (Audio Queue):** 50 cap, ~1-5 MB.
   :id: NFR-3.6
   :links: NFR-3


   Performance Targets


.. nfr:: Latency & Throughput
   :id: NFR-4
   :links: BRD-5.2,BRD-8

.. nfr:: **IPC Dispatch:** Sub-millisecond (<1ms) for metadata-only messages.
   :id: NFR-4.1
   :links: NFR-4

.. nfr:: **Round Trip:** <5ms metadata-only; <20ms for 1MB payload (excluding processing).
   :id: NFR-4.2
   :links: NFR-4

.. nfr:: **LLM Inference:** <1s average response time.
   :id: NFR-4.3
   :links: NFR-4

.. nfr:: **TTS:** ≤2s average end-to-end response.
   :id: NFR-4.4
   :links: NFR-4

.. nfr:: **UI Responsiveness:** No input blocking >100ms.
   :id: NFR-4.5
   :links: NFR-4

.. nfr:: **Logging:** LogServer must support ≥ 10,000 msgs/sec.
   :id: NFR-4.6
   :links: NFR-4

.. nfr:: **HSM:** Must support ≥ 1,000 state transitions/sec.
   :id: NFR-4.7
   :links: NFR-4

.. nfr:: **Queue Operations:** O(log n) time (1-5 microseconds).
   :id: NFR-4.8
   :links: NFR-4


   Reliability Constraints


.. nfr:: Fault Tolerance
   :id: NFR-5
   :links: BRD-2

.. nfr:: **Non-blocking:** No process shall block waiting for another during standard IPC.
   :id: NFR-5.1
   :links: NFR-5

.. nfr:: **Isolation:** Failures in UI, Runtime, or Audio must not cascade to Core.
   :id: NFR-5.2
   :links: NFR-5

.. nfr:: **Fire-and-Forget:** Log messages are acceptable to be lost if LogServer is down.
   :id: NFR-5.3
   :links: NFR-5

.. nfr:: **Timeout Accuracy:** Detection must be within ±100ms of configured limit.
   :id: NFR-5.4
   :links: NFR-5

.. nfr:: **Core Failure:** In-flight requests are considered lost (MVP acceptable).
   :id: NFR-5.5
   :links: NFR-5

.. nfr:: **Message Routability:** The Core must explicitly detect and handle attempts to send messages to disconnected or non-existent service identities.
   :id: NFR-5.6
   :links: NFR-5



.. nfr:: Key Dependencies
   :id: NFR-6
   :links: BRD-6

.. nfr:: `PySide6`: Default GUI framework.
   :id: NFR-6.1
   :links: NFR-6

.. nfr:: `pyzmq`: Non-blocking IPC.
   :id: NFR-6.2
   :links: NFR-6

.. nfr:: `onnxruntime-gpu`: GPU inference.
   :id: NFR-6.3
   :links: NFR-6

.. nfr:: `loguru`: Distributed logging.
   :id: NFR-6.4
   :links: NFR-6

.. nfr:: `transitions`: HSM implementation.
   :id: NFR-6.5
   :links: NFR-6




.. metadata:
   :file-id: nfr-root
   :title: "System Constraints"
   :version: "5.0"
   :date: "2025-12-17"
   :author: "Anthony Formosa"
   :roadmap_version: "5.0"
   :template_version: "2.0"
   :status: "Active"
   :llm-permissions: read-only
   :purpose: "Define Hard Limits & Constraints"

