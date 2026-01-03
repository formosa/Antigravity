# Maggie Application Framework - Context Dump
> **Format:** Flattened Hierarchy. Optimized for LLM Context.


## 1. REQUIREMENTS (BRD)

### BRD — Business Requirements (Context)

**[BRD-1] Project Purpose**
Develop a fully offline-capable, high-performance, real-time Python AI assistant framework (MAGGIE).
It **must** integrate modular “Services” for local LLM inference, Text-to-Speech (TTS), Speech-to-Text (STT), and Wake Word Detection (WWD).
It **must** implement a modular event loop, “Routines” for task-specific application functionality, and provide extension via “Services”, “Tools”, and “Routines”.

**[BRD-2] Strategic Objective**
Enable responsive, privacy-preserving AI assistant capabilities without dependency on cloud infrastructure.
The system **must** ensure fault tolerance, maintainability, and deterministic state transitions via an HSM.

**[BRD-3] Business Rationale**
Rationale for business decisions.

**[BRD-3.1] **Privacy & Offline:** Enable operation without internet dependency or data leakage.** -> BRD-3

**[BRD-3.2] **Customizability:** Allow extension via a modular architecture.** -> BRD-3

**[BRD-3.3] **Performance:** Leverage local GPU resources for low-latency performance.** -> BRD-3

**[BRD-3.4] **Reliability:** Reduce downtime through multi-process isolation.** -> BRD-3

**[BRD-3.5] **Observability:** Enhance debugging via distributed, correlated logging.** -> BRD-3

**[BRD-4] Problem Statement**
Users require AI assistant capabilities but are constrained by internet dependency, privacy concerns, and the limitations of single-process applications.
The framework requires a high-performance, non-blocking, and fault-isolating Inter-Process Communication (IPC) architecture.

System Scope

**[BRD-5] High-level Scope**
Scope definition.

**[BRD-5.1] Offline, multi-process Python framework.** -> BRD-5

**[BRD-5.2] Local LLM, TTS, and STT inference.** -> BRD-5

**[BRD-5.3] Modular "Tool" and "Routine" expansion system.** -> BRD-5

**[BRD-5.4] Centralized, correlated logging.** -> BRD-5

**[BRD-5.5] Intuitive UI for control and state feedback.** -> BRD-5

**[BRD-5.6] Hierarchical State Machine (HSM) for orchestration.** -> BRD-5

**[BRD-6] Constraints & Environment**

**[BRD-6.1] **Target Environment:** High-end consumer workstation.** -> BRD-6

**[BRD-6.2] **Operation:** Real-time operation with limited blocking tolerance.** -> BRD-6

**[BRD-6.3] **Security:** Local sockets only (127.0.0.1).** -> BRD-6
Success Criteria

**[BRD-7] Stakeholders**

**[BRD-7.1] **Primary:** End users requiring offline AI assistant functionality.** -> BRD-7

**[BRD-7.2] **Secondary:** Developers extending Maggie via Tools/Routines.** -> BRD-7

**[BRD-7.3] **Tertiary:** DevOps and QA Engineers (monitoring, testing).** -> BRD-7

**[BRD-8] Success Metrics**

**[BRD-8.1] **Latency:** Sub-250ms IPC dispatch; <1s LLM response.** -> BRD-8

**[BRD-8.2] **Reliability:** 99.9% Core uptime; mean uptime >= 72 hours.** -> BRD-8

**[BRD-8.3] **Observability:** 100% request traceability.** -> BRD-8
Future Work

**[BRD-9] Future Scope (Out of Initial Scope)**

**[BRD-9.1] Persistent HSM state for crash recovery.** -> BRD-9

**[BRD-9.2] Multi-GPU ONNX worker pool.** -> BRD-9

**[BRD-9.3] Real-time streaming for TTS/STT.** -> BRD-9

**[BRD-9.4] Metrics dashboard with live state visualization.** -> BRD-9

**[BRD-9.5] Request cancellation support.** -> BRD-9

**[BRD-9.6] Remote/distributed ONNX deployment.** -> BRD-9

**[BRD-9.7] Offline speaker diarization.** -> BRD-9


## 2. CONSTRAINTS (NFR)

### NFR — System Constraints (Boundaries)

**[NFR-1] Target Environment** -> BRD-6

**[NFR-1.1] **CPU:** AMD Ryzen 9 5900X (Audio/Core must run here).** -> NFR-1

**[NFR-1.2] **GPU:** RTX 3080 10GB VRAM (Runtime/Inference only).** -> NFR-1

**[NFR-1.3] **RAM:** 32GB System Memory.** -> NFR-1

**[NFR-1.4] **OS:** Windows 11 Pro x64.** -> NFR-1

**[NFR-1.5] **Python:** Version >= 3.11.** -> NFR-1

**[NFR-1.6] **CUDA:** Toolkit installed for GPU inference.** -> NFR-1

**[NFR-2] Security & Network** -> BRD-3, BRD-6

**[NFR-2.1] All communication limited to local TCP sockets (`127.0.0.1`) via ZeroMQ.** -> NFR-2

**[NFR-2.2] No cloud dependencies allowed for runtime operations.** -> NFR-2

**[NFR-3] Resource Isolation** -> BRD-3, BRD-6

**[NFR-3.1] **CPU Idle:** Processes polling for IPC messages must consume <5% CPU when idle.** -> NFR-3

**[NFR-3.2] **Audio Priority:** CPU-bound services (Audio) must prioritize low-latency over idle CPU.** -> NFR-3

**[NFR-3.3] **Memory Footprint (Core Queue):** 1000 cap, ~10-50 MB.** -> NFR-3

**[NFR-3.4] **Memory Footprint (UI Queue):** 100 cap, ~1-5 MB.** -> NFR-3

**[NFR-3.5] **Memory Footprint (Runtime Queue):** 50 cap, ~5-25 MB.** -> NFR-3

**[NFR-3.6] **Memory Footprint (Audio Queue):** 50 cap, ~1-5 MB.** -> NFR-3
Performance Targets

**[NFR-4] Latency & Throughput** -> BRD-5.2, BRD-8

**[NFR-4.1] **IPC Dispatch:** Sub-millisecond (<1ms) for metadata-only messages.** -> NFR-4

**[NFR-4.2] **Round Trip:** <5ms metadata-only; <20ms for 1MB payload (excluding processing).** -> NFR-4

**[NFR-4.3] **LLM Inference:** <1s average response time.** -> NFR-4

**[NFR-4.4] **TTS:** ≤2s average end-to-end response.** -> NFR-4

**[NFR-4.5] **UI Responsiveness:** No input blocking >100ms.** -> NFR-4

**[NFR-4.6] **Logging:** LogServer must support ≥ 10,000 msgs/sec.** -> NFR-4

**[NFR-4.7] **HSM:** Must support ≥ 1,000 state transitions/sec.** -> NFR-4

**[NFR-4.8] **Queue Operations:** O(log n) time (1-5 microseconds).** -> NFR-4
Reliability Constraints

**[NFR-5] Fault Tolerance** -> BRD-2

**[NFR-5.1] **Non-blocking:** No process shall block waiting for another during standard IPC.** -> NFR-5

**[NFR-5.2] **Isolation:** Failures in UI, Runtime, or Audio must not cascade to Core.** -> NFR-5

**[NFR-5.3] **Fire-and-Forget:** Log messages are acceptable to be lost if LogServer is down.** -> NFR-5

**[NFR-5.4] **Timeout Accuracy:** Detection must be within ±100ms of configured limit.** -> NFR-5

**[NFR-5.5] **Core Failure:** In-flight requests are considered lost (MVP acceptable).** -> NFR-5

**[NFR-5.6] **Message Routability:** The Core must explicitly detect and handle attempts to send messages to disconnected or non-existent service identities.** -> NFR-5

**[NFR-6] Key Dependencies** -> BRD-6

**[NFR-6.1] `PySide6`: Default GUI framework.** -> NFR-6

**[NFR-6.2] `pyzmq`: Non-blocking IPC.** -> NFR-6

**[NFR-6.3] `onnxruntime-gpu`: GPU inference.** -> NFR-6

**[NFR-6.4] `loguru`: Distributed logging.** -> NFR-6

**[NFR-6.5] `transitions`: HSM implementation.** -> NFR-6


## 3. SPECIFICATIONS (FSD)

### FSD — Feature Specifications (Behavior)

**[FSD-1] Process Orchestration** -> BRD-5, NFR-5
The system must maintain independent but interconnected processes utilizing a multi-process architecture:

**[FSD-1.1] Core Hub** -> FSD-1
Routes request-response messages between services and tracks in-flight requests via `request_id`.

**Services (Spokes):**

**[FSD-1.2] **UI Process:** Handles user interaction (PySide6).** -> FSD-1

**[FSD-1.3] **Runtime Process:** GPU-optimized environment for model inference.** -> FSD-1

**[FSD-1.4] **Audio Process:** Real-time audio I/O, WWD, and VAD.** -> FSD-1

**[FSD-1.5] **LogServer (Sink):** Aggregates logs via PULL socket.** -> FSD-1

**[FSD-2] Hierarchical State Machine (HSM)** -> BRD-2

**[FSD-2.1] Core must maintain an HSM (using `transitions` library).** -> FSD-2

**[FSD-2.2] **Dynamic Compilation:** HSM must be dynamically compiled at startup from definitions provided by Tools, Routines, and Services.** -> FSD-2

**[FSD-2.3] **Required States:** `Root(DEFAULT)`, `initializing`, `sleeping`, `waking`, `active`, `busy` (`llm`, `tts`, `stt`), `error`, `shutting_down`.** -> FSD-2

**[FSD-3] Modular Extensions (Tools/Routines)** -> BRD-5

**[FSD-3.1] **Tools:** Modular functional assets with specific HSM states (e.g., File Export).** -> FSD-3

**[FSD-3.2] **Routines:** Structured workflows composed of Tools and Services (e.g., Recipe Creator).** -> FSD-3

**[FSD-3.3] **Default Routine:** A "Primary Routine" providing conversational LLM chat mapping GUI inputs to CLI commands.** -> FSD-3
Voice Interaction Pipeline

**[FSD-4] Audio Acquisition (Audio Service)** -> BRD-5, NFR-3

**[FSD-4.1] **Wake Word:** Always-on detection using `pvporcupine`.** -> FSD-4

**[FSD-4.2] **Constraint:** Must only send `WAKE_WORD_DETECTED` if Core is in `idle` state.** -> FSD-4

**[FSD-4.3] **VAD (Stage 1):** Real-time, CPU-based VAD using `webrtcvad`.** -> FSD-4

**[FSD-4.4] **VAD (Stage 2):** Neural VAD (Silero via ONNX Runtime CPU) runs locally in Audio Process. Refines |FSD-4.3| output.** -> BRD-5.2, NFR-1.1, NFR-1

**[FSD-4.5] **Signal Output:** Emits normalized `SIGNAL_SPEECH` (Text) or `SIGNAL_WAKE` (Event) to Core. No command interpretation.** -> FSD-4

**[FSD-5] Inference Execution (Runtime Service)** -> BRD-5, NFR-1

**[FSD-5.1] **STT:** Execute transcription using `faster-whisper` (ONNX) on audio buffers routed from Audio Service.** -> FSD-5

**[FSD-5.2] **LLM:** Execute text generation using local models via ONNX Runtime.** -> FSD-5

**[FSD-5.3] **TTS:** Execute synthesis using `kokoro` (ONNX).** -> FSD-5

**[FSD-5.4] **Error Handling:** Must report clear error codes (e.g., `ONNX_E_CUDA_OOM`).** -> FSD-5
Logging & Observability

**[FSD-6] Distributed Logging** -> BRD-3, NFR-5

**[FSD-6.1] All processes must emit logs to the central LogServer.** -> FSD-6

**[FSD-6.2] **Fire-and-Forget:** Senders must never block; messages are dropped if LogServer is down.** -> FSD-6

**[FSD-6.3] **Correlation:** All logs must include `request_id` for correlation across processes.** -> FSD-6

**[FSD-6.4] **Traceability:** 100% traceable request coverage.** -> FSD-6

**[FSD-7] Error Handling Strategy** -> BRD-2, NFR-5

**[FSD-7.1] **LogServer Fault:** Senders continue normally, silently dropping logs.** -> FSD-7

**[FSD-7.2] **Service Fault:** Core detects disconnection, marks service unavailable, transitions requests to error.** -> FSD-7

**[FSD-7.3] **Timeout:** Core detects non-response (>5.0s) and triggers error state.** -> FSD-7

**[FSD-7.4] **Core Fault:** Services remain operational but disconnected; attempt reconnect on restart.** -> FSD-7

**[FSD-8] Intent Resolution (The "Brain")** -> BRD-5.6, FSD-1

**[FSD-8.1] **Input Normalization:** Core accepts inputs (`VOICE`, `CLI`, `GUI`) as uniform text strings.** -> FSD-8

**[FSD-8.2] **Command Registry:** Core maintains a registry of valid commands mapping "String" → "Callable".** -> FSD-8

**[FSD-8.3] **Fast Path:** IF input matches Registry Key → Execute immediately (Deterministic).** -> FSD-8

**[FSD-8.4] **Slow Path:** IF input does not match → Forward to LLM Service for inference (Probabilistic).** -> FSD-8

**[FSD-9] User Experience (UX)** -> BRD-5.5, FSD-1.2

**[FSD-9.1] **State Reflection:** UI must visually reflect state (Dark/Gray for Sleep, Bright/Color for Active).** -> FSD-9

**[FSD-9.2] **Input Locking:** Text input disabled in Sleep; Blinking cursor only in Active.** -> FSD-9

**[FSD-9.3] **Wake Triggers:** System wakes on Voice ("Hey Maggie") OR Click-to-Wake on input box.** -> FSD-9


## 4. ARCHITECTURE (SAD)

### SAD — Architecture Definitions (Structure)

**[SAD-1] Architectural Patterns** -> FSD-1.1

**[SAD-1.1] **Hub-and-Spoke:** Core Process acts as the central `ROUTER` (Hub); Services are `DEALER` (Spokes).** -> SAD-1

**[SAD-1.2] **Decoupled Sink:** Dedicated LogServer acts as `PULL` sink for `PUSH` sources.** -> SAD-1

**[SAD-1.3] **No Shared Abstraction:** `ROUTER-DEALER` and `PUSH-PULL` patterns are implemented separately to avoid artificial coupling.** -> SAD-1

**[SAD-1.4] **Context Propagation:** `request_id` must be passed in every frame.** -> SAD-1

**[SAD-2] Process Topology** -> FSD-1.1
.. mermaid::

   graph LR
      subgraph Services ["External Services (DEALER)"]
         direction TB
         UI["UI"]
         Runtime["Runtime"]
         Audio["Audio"]
      end

      Core["Core Process (ROUTER)"]
      LogServer["LogServer (PULL)"]

      %% Bidirectional Request-Response (ROUTER-DEALER)
      %% Using explicit links for clarity in LR, Core is the Hub
      UI <==> Core
      Runtime <==> Core
      Audio <==> Core

      %% Unidirectional Fire-and-Forget (PUSH-PULL)
      %% Dotted lines for logging
      UI -. PUSH .-> LogServer
      Runtime -. PUSH .-> LogServer
      Audio -. PUSH .-> LogServer
      Core -. PUSH .-> LogServer

      %% Styling
      classDef core fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,rx:5,ry:5;
      classDef service fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,rx:5,ry:5;
      classDef sink fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:5,ry:5;

      class Core core;
      class UI,Runtime,Audio service;
      class LogServer sink;

      %% Curve smoothing
      linkStyle default interpolate basis

**[SAD-3] Integration Strategy** -> FSD-6.1, NFR-2.1, NFR-2

**[SAD-3.1] **Core ↔ Services (Request-Response):**** -> SAD-3

**[SAD-3.2] **Pattern:** ZeroMQ `ROUTER` (Core) ↔ `DEALER` (Service).** -> SAD-3

**[SAD-3.3] **Type:** Bidirectional.** -> SAD-3

**[SAD-3.4] **Requirement:** Core maintains routing table (client identity → socket identity).** -> SAD-3

**[SAD-3.5] **All Processes → LogServer (Logging):**** -> SAD-3

**[SAD-3.6] **Pattern:** ZeroMQ `PUSH` (Client) → `PULL` (LogServer).** -> SAD-3

**[SAD-3.7] **Type:** Unidirectional, Fire-and-Forget.** -> SAD-3

**[SAD-3.8] **Requirement:** Senders must set `SNDHWM=100` and `LINGER=0` to buffer micro-bursts without blocking.** -> SAD-3

**[SAD-4] Concurrency Model** -> NFR-5.1

**[SAD-4.1] **Receiver Threads:** Each process uses a dedicated thread to poll ZMQ sockets and push to an internal `queue.PriorityQueue`.** -> SAD-4

**[SAD-4.2] **Main Loop:** The main application loop processes the `PriorityQueue` to remain non-blocking.** -> SAD-4

**[SAD-4.3] **Queueing:**** -> SAD-4

**[SAD-4.4] Must use `queue.PriorityQueue`.** -> SAD-4

**[SAD-4.5] **Structure:** `(priority, counter, message)`.** -> SAD-4

**[SAD-4.6] **Ordering:** Monotonic counter (`itertools.count`) ensures FIFO within priority levels.** -> SAD-4

**[SAD-4.7] **Priority Levels:**** -> SAD-4

**[SAD-4.8] **High (0):** `shutdown`, `error_notification`, `state_change`.** -> SAD-4

**[SAD-4.9] **Normal (1):** Inference requests, status updates.** -> SAD-4

**[SAD-5] Configuration Driven** -> BRD-3.2

**[SAD-5.1] All IPC endpoints (addresses, ports) and parameters (queue sizes, timeouts) must be loaded from `ipc_config.yaml`.** -> SAD-5


## 5. DATA CONTRACTS (ICD)

### ICD — Interface & Data Schemas (Contracts)

**[ICD-1] IPC Configuration (ipc_config.yaml)** -> SAD-5.1, NFR-3.3, NFR-3.4, NFR-3.5, NFR-3.6, NFR-3
.. code-block:: yaml

   core:
     router_bind: "tcp://127.0.0.1:5555"
     push_connect: "tcp://127.0.0.1:5556"    # Added for Core logging
     router_hwm: 1000
     queue_maxsize: 1000
     poll_timeout_ms: 100
     response_timeout_s: 5.0
     extensions:
       path: "./extensions"      # Root for tools/routines discovery

   logserver:
     pull_bind: "tcp://127.0.0.1:5556"
     poll_timeout_ms: 1      # Tight loop for high throughput
     log_rotation_mb: 50
     log_retention_days: 30

   services:
     ui:
       dealer_connect: "tcp://127.0.0.1:5555"
       push_connect: "tcp://127.0.0.1:5556"
       queue_maxsize: 100
       poll_timeout_ms: 100
     runtime:
       dealer_connect: "tcp://127.0.0.1:5555"
       push_connect: "tcp://127.0.0.1:5556"
       queue_maxsize: 50
       poll_timeout_ms: 100
     audio:
       dealer_connect: "tcp://127.0.0.1:5555"
       push_connect: "tcp://127.0.0.1:5556"
       queue_maxsize: 50
       poll_timeout_ms: 10

Message Protocols

**[ICD-2] Frame Structure** -> SAD-3.2, SAD-3.6, SAD-1.4, SAD-1

**[ICD-2.1] **Core ↔ Services (ROUTER-DEALER):**** -> ICD-2

**[ICD-2.2] **Outbound (DEALER):** `[metadata_json, payload_bytes...]`** -> ICD-2

**[ICD-2.3] **Inbound (ROUTER):** `[service_identity, b'', metadata_json, payload_bytes...]`** -> ICD-2

**[ICD-2.4] **All → LogServer (PUSH-PULL):**** -> ICD-2

**[ICD-2.5] **Frame:** `[metadata_json, message_string]`** -> ICD-2

**[ICD-2.6] **Payloads:**** -> ICD-2

**[ICD-2.7] Text: JSON-encoded UTF-8 bytes.** -> ICD-2

**[ICD-2.8] Binary: Raw bytes (PCM, tensors).** -> ICD-2

**[ICD-2.9] Multi-part: Supported for zero-copy efficiency.** -> ICD-2

**[ICD-3] Metadata Schema (JSON)** -> FSD-6.3, SAD-4.7, SAD-4
Every IPC message frame 0 (Metadata) must validate against:

.. code-block:: json

   {
     "source": "UI | Audio | Runtime | Core",
     "destination": "Target_Service_Name",
     "command": "function_name_or_signal",
     "request_id": "uuid-v4-string",
     "timestamp": "ISO-8601-string",
     "priority": 1,
     "payload_type": "json | binary | text"
   }

Note: Priority 0 = High, 1 = Normal

**[ICD-4] Response Payload Schema** -> ICD-3
.. code-block:: json

   {
     "source": "Runtime",
     "destination": "UI",
     "command": "llm_inference_response",
     "request_id": "uuid-echoed",
     "timestamp": "ISO-8601-string",
     "status": "success | error",
     "error_code": "optional_string_or_null"
   }


## 6. DESIGN BLUEPRINTS (TDD)

### TDD — Technical Design (Blueprints)

**[TDD-1] Component: CoreProcess** -> SAD-2, FSD-1.1

**[TDD-1.1] **Class Name:** `CoreProcess`** -> TDD-1

**[TDD-1.2] **Dependencies:** `zmq`, `queue`, `itertools`, `transitions`, `yaml`, `threading`, `importlib`, `pathlib`.** -> TDD-1
**Socket Configuration:**

**[TDD-1.3] Bind `ROUTER` socket to address defined in `ipc_config.yaml` (`core.router_bind`).** -> ICD-1, SAD-3.2, SAD-3

**[TDD-1.4] Set `ZMQ_ROUTER_MANDATORY=1` to detect unroutable messages.** -> NFR-5.6, NFR-5
**State Management:**

**[TDD-1.5] Initialize `active_requests` dictionary: `Dict[str, Tuple[bytes, float, str]]` (ID → Identity, Timestamp, Command).** -> SAD-1.4, SAD-1

**[TDD-1.6] Initialize HSM using `transitions.Machine`. State definitions include both statically-defined core states and dynamically-compiled states from Tool/Routine extensions.** -> FSD-2.2, FSD-2.3, FSD-2
**Concurrency (Main Loop):**

**[TDD-1.7] **Receiver Thread:** Spawns a `threading.Thread` to poll the `ROUTER` socket and push frames to `self.queue`.** -> SAD-4.1, SAD-4

**[TDD-1.8] **Event Loop:** Pops items from `self.queue` (PriorityQueue) and dispatches to HSM triggers.** -> SAD-4.2, SAD-4

**[TDD-1.9] **Timeout Monitor:** On every loop iteration, check `active_requests` for timestamps exceeding `response_timeout_s`.** -> FSD-7.3, FSD-7
**Extension Discovery:**

**[TDD-1.10] Connect `PUSH` socket to `core.push_connect` (SNDHWM=1, LINGER=0) for logging.** -> FSD-6.1, SAD-3.5, SAD-3

**[TDD-1.11] **Scan Logic:** On startup, iterate directories in `config.core.extensions.path`.** -> FSD-3

**[TDD-1.12] **Validation:** Parse `manifest.yaml` in subdirectories (`tools/`, `routines/`).** -> TDD-1

**[TDD-1.13] **Loading:** Use `importlib` to dynamically import the module specified in manifest `entry_point`.** -> TDD-1
**Command Resolution:**

**[TDD-1.14] **Structure:** `self.command_registry: Dict[str, Callable]`.** -> FSD-8.2, FSD-8

**[TDD-1.15] **Logic:** `resolve_intent(input_str: str)` checks registry before HSM dispatch.** -> TDD-1

**[TDD-2] Component: ServiceClient** -> SAD-3.1, SAD-4

**[TDD-2.1] **Class Name:** `ServiceClient`** -> TDD-2

**[TDD-2.2] **Purpose:** Standardized base implementation for UI, Runtime, and Audio services.** -> TDD-2

**[TDD-2.3] **Dependencies:** `yaml`, `zmq`, `queue`, `itertools`, `threading`.** -> TDD-2
**Socket Configuration:**

**[TDD-2.4] `DEALER`: Connects to Core `ROUTER`. Identity is auto-assigned by ZMQ.** -> ICD-2.1, ICD-2

**[TDD-2.5] `PUSH`: Connects to LogServer `PULL`. Must set `SNDHWM=1` and `LINGER=0` (Fire-and-Forget).** -> SAD-3.8, NFR-5.3, NFR-5
**Queuing Strategy:**

**[TDD-2.6] Internal `queue.PriorityQueue` populated by a dedicated `_receiver_thread`.** -> SAD-4.1, SAD-4

**[TDD-2.7] Ordering enforced via `(priority, itertools.count(), message)` tuple.** -> SAD-4.6
**UI Requirements:**

**[TDD-2.8] **State Awareness:** Must subscribe to HSM state changes and apply CSS classes (`sleeping`, `active`).** -> FSD-9.1

**[TDD-2.9] **Input Control:** Widget `setReadOnly(True)` in Sleep; `installEventFilter` to catch Click-to-Wake events.** -> FSD-9.2, SAD-4

**[TDD-3] Component: LogServerSink** -> FSD-6.1, ICD-1

**[TDD-3.1] **Class Name:** `LogServerSink`** -> TDD-3

**[TDD-3.2] **Dependencies:** `loguru`, `zmq`.** -> TDD-3
**Socket Configuration:**

**[TDD-3.3] Bind `PULL` socket to address defined in `ipc_config.yaml` (`logserver.pull_bind`).** -> SAD-3.6, SAD-3
**Processing Loop:**

**[TDD-3.4] Execute tight poll loop (1ms timeout) to maximize throughput.** -> NFR-4.6, NFR-4

**[TDD-3.5] Parse inbound frames as `[metadata_json, message_string]`.** -> ICD-2.5, ICD-2
**Persistence:**

**[TDD-3.6] Configure `loguru` rotation (50MB) and retention (30 days).** -> ICD-1
Interface Contracts

**[TDD-4] Component: Tool/Routine Interface** -> FSD-3

**[TDD-4.1] **Class Name:** `AbstractTool`, `AbstractRoutine` (ABC).** -> TDD-4
**Abstract Methods:**

**[TDD-4.2] `initialize(core_context: CoreProcess)`: Inject Core dependencies.** -> TDD-4

**[TDD-4.3] `get_hsm_states() -> List[Dict]`: Return state definitions for dynamic compilation.** -> FSD-2.2, FSD-2

**[TDD-4.4] `handle_event(event_data: Dict) -> str`: Process business logic and return next trigger.** -> TDD-4
**Manifest Contract:**

**[TDD-4.5] **Requirement:** Every extension directory must contain `manifest.yaml`.** -> TDD-4

**[TDD-4.6] **Schema:**** -> TDD-4
 - `name`: Unique identifier (string).
 - `version`: Semantic version (string).
 - `type`: "tool" | "routine".
 - `entry_point`: Relative path to python module definition (e.g., "src.plugin").


## 7. TEST PROMPTS (ISP)

### ISP — Implementation Stubs (Prompts)

**[ISP-1] Stub: Core Process** -> TDD-1
**Implementation Requirements:**

**[ISP-1.1] **Class Structure:** Inherit structure from `CoreProcess` blueprint.** -> TDD-1.1, TDD-1

**[ISP-1.2] **Socket:** Bind `ROUTER` using config from `ICD-1`.** -> TDD-1.3, ICD-1, TDD-1

**[ISP-1.3] **Orchestration:** Initialize `active_requests` dict and `PriorityQueue`.** -> TDD-1.5, TDD-1

**[ISP-1.4] **HSM:** Setup `transitions.Machine` with states from `FSD-2`.** -> TDD-1.6, FSD-2.3, FSD-2
.. code-block:: python

   import zmq
   import yaml
   import queue
   import itertools
   import threading
   from transitions import Machine

   class CoreProcess:
       """
       Orchestrates IPC between services using ZeroMQ ROUTER pattern.
       """
       def __init__(self, config_path: str):
           """
           Initialize ZMQ Context, Bind ROUTER.
           Init self.active_requests = {} (ID -> Identity, Ts, Cmd).
           Init self.queue = PriorityQueue(maxsize).
           Init self.counter = itertools.count().
           """
           pass

       def _start_receiver_thread(self) -> None:
           """
           Spawns a daemon thread running a ZMQ Poller.
           Parse: [client_identity, b'', metadata, payload...]
           Put (priority, next(counter), (client_identity, frames)) into queue.
           """
           pass

       def run(self) -> None:
           """
           Main Event Loop.
           1. Process self.queue (Priority).
           2. Check timeouts in self.active_requests (>5.0s).
           3. Drive HSM transitions (enter_processing, enter_error).
           """
           pass

**[ISP-2] Stub: Service Client** -> TDD-2
**Implementation Requirements:**

**[ISP-2.1] **Base Class:** Define `ServiceClient` for UI/Runtime/Audio.** -> TDD-2.1, TDD-2

**[ISP-2.2] **Connectivity:** Setup `DEALER` (Command) and `PUSH` (Log) sockets.** -> TDD-2.4, TDD-2.5, TDD-2

**[ISP-2.3] **Threading:** Implement `_receiver_thread` to populate internal `PriorityQueue`.** -> TDD-2.6, TDD-2
.. code-block:: python

   class ServiceClient:
       """
       Standard client for Service processes.
       Maintains DEALER (Command) and PUSH (Log) sockets.
       """
       def __init__(self, service_name: str, config_path: str):
           """
           Connects DEALER and PUSH sockets based on ICD-1.
           Sets PUSH socket to SNDHWM=1, LINGER=0 (Fire-and-Forget).
           Starts receiver thread.
           """
           pass

       def send_request(self, command: str, payload: dict, priority: int = 1) -> None:
           """
           Constructs metadata (ICD-3) and sends via DEALER.
           """
           pass

       def send_log(self, level: str, message: str, request_id: str = None) -> None:
           """
           Fire-and-forget log emission.
           Constructs frame: [Metadata(ICD-3), Message].
           Must swallow zmq.Again exceptions.
           """
           pass

**[ISP-3] Stub: LogServer Sink** -> TDD-3
**Implementation Requirements:**

**[ISP-3.1] **Socket:** Bind `PULL` socket for aggregation.** -> TDD-3.3, TDD-3

**[ISP-3.2] **Performance:** Use 1ms poll timeout for high throughput.** -> TDD-3.4, TDD-3

**[ISP-3.3] **Storage:** Configure `loguru` rotation/retention policies.** -> TDD-3.6, TDD-3
.. code-block:: python

   from loguru import logger

   class LogServerSink:
       """
       Aggregates logs from all services via PULL socket.
       """
       def __init__(self, config_path: str):
           """
           Bind PULL socket.
           Configure Loguru (Rotation: 50MB, Retention: 30 Days).
           """
           pass

       def run(self) -> None:
           """
           Tight Poll Loop (1ms).
           Parse [metadata, message] -> logger.log().
           """
           pass

**[ISP-4] Stub: Tool/Routine Interface** -> TDD-4
**Implementation Requirements:**

**[ISP-4.1] **Extensibility:** Define `AbstractTool` and `AbstractRoutine` using `ABC`.** -> TDD-4.1, TDD-4

**[ISP-4.2] **Contract:** Enforce `initialize`, `get_hsm_states`, and `handle_event`.** -> TDD-4.2, TDD-4.3, TDD-4.4, TDD-4
.. code-block:: python

   from abc import ABC, abstractmethod
   from typing import List, Dict

   class AbstractTool(ABC):
       """
       Interface for modular functional assets.
       """
       @abstractmethod
       def initialize(self, core_context) -> None:
           pass

       @abstractmethod
       def get_hsm_states(self) -> List[Dict]:
           """Return state definitions for dynamic compilation."""
           pass

       @abstractmethod
       def handle_event(self, event_data: Dict) -> str:
           """Process logic and return next trigger."""
           pass

**[ISP-5] Stub: Audio Worker Loop** -> FSD-4, NFR-3
**Implementation Requirements:**

**[ISP-5.1] **Logic:** Implement Wake Word -> VAD -> STT pipeline.** -> FSD-4

**[ISP-5.2] **Constraint:** Check Core State (`idle`) before sending Wake Word events.** -> FSD-4.2, FSD-4
.. code-block:: python

   def audio_worker_loop(client: ServiceClient):
       """
       Real-time audio processing loop.
       """
       # Setup pvporcupine (Wake Word) and webrtcvad (VAD)

       while True:
           # 1. Read Audio Chunk
           # 2. Denoise
           # 3. Check Wake Word -> client.send_request("WAKE_WORD") IF Core is IDLE
           # 4. Check VAD -> Buffer for STT
           # 5. Handle inbound IPC messages (client.poll_queue)
           pass

### FSD — Feature Specifications (Behavior)

**[7D2AF] **Audio Feedback:**
 :id: FSD-9.4
 :links: FSD-9**
- *Sleep -> Waking (Click):* Play "Yes? Just one moment, please."
- *Waking -> Active:* Play "How can I assist you."

**[C6B06] **Transitions:**
 :id: FSD-2.4
 :links: FSD-2**
- `sleeping` (Start): Low power, UI Dark, Input Locked.
- `waking`: Triggered by `WAKE_WORD` or `GUI_INTERACTION`.
- `active`: Normal operation, UI Bright, Input Unlocked.

### Controlled Terms

**[TERM-AUDIO-PROCESS] Audio Process**
A specialized Runtime Process dedicated to audio capture, processing, or playback.

**[TERM-CORE-PROCESS] Core Process**
The central orchestrator of the Maggie system. Responsible for lifecycle management, message routing, and service coordination. Never referred to as "Manager" or "Host".

**[TERM-HSM] HSM**
Hierarchical State Machine. The primary architectural pattern for managing complex system states.

**[TERM-LOGSERVER] LogServer**
The centralized logging service that aggregates and persists system logs from all processes.

**[TERM-ROUTINE] Routine**
A predefined sequence of Tool invocations or logic steps designed to achieve a higher-level goal.

**[TERM-RUNTIME-PROCESS] Runtime Process**
A generic term for any independent operating system process spawned or managed by the Core Process.

**[TERM-SERVICE] Service**
A long-running, addressable component providing specific functionality (e.g., LogServer, CommandDispatcher).

**[TERM-TOOL] Tool**
A discrete, executable unit of logic that can be invoked by an agent or the Core Process to perform a specific task.

**[TERM-UI-PROCESS] UI Process**
A specialized Runtime Process dedicated to rendering the graphical user interface.

