FSD — Feature Specifications (Behavior)
====================================================================================================

System Core Capabilities


.. fsd:: Process Orchestration
   :id: FSD-1
   :links: BRD-5,NFR-5

   The system must maintain independent but interconnected processes utilizing a multi-process architecture:

.. fsd:: Core Hub
   :id: FSD-1.1
   :links: FSD-1

   Routes request-response messages between services and tracks in-flight requests via `request_id`.

   **Services (Spokes):**

.. fsd:: **UI Process:** Handles user interaction (PySide6).
   :id: FSD-1.2
   :links: FSD-1

.. fsd:: **Runtime Process:** GPU-optimized environment for model inference.
   :id: FSD-1.3
   :links: FSD-1

.. fsd:: **Audio Process:** Real-time audio I/O, WWD, and VAD.
   :id: FSD-1.4
   :links: FSD-1

.. fsd:: **LogServer (Sink):** Aggregates logs via PULL socket.
   :id: FSD-1.5
   :links: FSD-1



.. fsd:: Hierarchical State Machine (HSM)
   :id: FSD-2
   :links: BRD-2

.. fsd:: Core must maintain an HSM (using `transitions` library).
   :id: FSD-2.1
   :links: FSD-2

.. fsd:: **Dynamic Compilation:** HSM must be dynamically compiled at startup from definitions provided by Tools, Routines, and Services.
   :id: FSD-2.2
   :links: FSD-2

.. fsd:: **Required States:** `Root(DEFAULT)`, `initializing`, `sleeping`, `waking`, `active`, `busy` (`llm`, `tts`, `stt`), `error`, `shutting_down`.
   :id: FSD-2.3
   :links: FSD-2

.. fsd:: **Transitions:**
   :id: FSD-2.4
   :links: FSD-2

   - `sleeping` (Start): Low power, UI Dark, Input Locked.
   - `waking`: Triggered by `WAKE_WORD` or `GUI_INTERACTION`.
   - `active`: Normal operation, UI Bright, Input Unlocked.


.. fsd:: Modular Extensions (Tools/Routines)
   :id: FSD-3
   :links: BRD-5

.. fsd:: **Tools:** Modular functional assets with specific HSM states (e.g., File Export).
   :id: FSD-3.1
   :links: FSD-3

.. fsd:: **Routines:** Structured workflows composed of Tools and Services (e.g., Recipe Creator).
   :id: FSD-3.2
   :links: FSD-3

.. fsd:: **Default Routine:** A "Primary Routine" providing conversational LLM chat mapping GUI inputs to CLI commands.
   :id: FSD-3.3
   :links: FSD-3


   Voice Interaction Pipeline


.. fsd:: Audio Acquisition (Audio Service)
   :id: FSD-4
   :links: BRD-5,NFR-3

.. fsd:: **Wake Word:** Always-on detection using `pvporcupine`.
   :id: FSD-4.1
   :links: FSD-4

.. fsd:: **Constraint:** Must only send `WAKE_WORD_DETECTED` if Core is in `idle` state.
   :id: FSD-4.2
   :links: FSD-4

.. fsd:: **VAD (Stage 1):** Real-time, CPU-based VAD using `webrtcvad`.
   :id: FSD-4.3
   :links: FSD-4

.. fsd:: **VAD (Stage 2):** Neural VAD (Silero via ONNX Runtime CPU) runs locally in Audio Process. Refines |FSD-4.3| output.
   :id: FSD-4.4
   :links: BRD-5.2,NFR-1.1,NFR-1

.. fsd:: **Signal Output:** Emits normalized `SIGNAL_SPEECH` (Text) or `SIGNAL_WAKE` (Event) to Core. No command interpretation.
   :id: FSD-4.5
   :links: FSD-4



.. fsd:: Inference Execution (Runtime Service)
   :id: FSD-5
   :links: BRD-5,NFR-1

.. fsd:: **STT:** Execute transcription using `faster-whisper` (ONNX) on audio buffers routed from Audio Service.
   :id: FSD-5.1
   :links: FSD-5

.. fsd:: **LLM:** Execute text generation using local models via ONNX Runtime.
   :id: FSD-5.2
   :links: FSD-5

.. fsd:: **TTS:** Execute synthesis using `kokoro` (ONNX).
   :id: FSD-5.3
   :links: FSD-5

.. fsd:: **Error Handling:** Must report clear error codes (e.g., `ONNX_E_CUDA_OOM`).
   :id: FSD-5.4
   :links: FSD-5


   Logging & Observability


.. fsd:: Distributed Logging
   :id: FSD-6
   :links: BRD-3,NFR-5

.. fsd:: All processes must emit logs to the central LogServer.
   :id: FSD-6.1
   :links: FSD-6

.. fsd:: **Fire-and-Forget:** Senders must never block; messages are dropped if LogServer is down.
   :id: FSD-6.2
   :links: FSD-6

.. fsd:: **Correlation:** All logs must include `request_id` for correlation across processes.
   :id: FSD-6.3
   :links: FSD-6

.. fsd:: **Traceability:** 100% traceable request coverage.
   :id: FSD-6.4
   :links: FSD-6



.. fsd:: Error Handling Strategy
   :id: FSD-7
   :links: BRD-2,NFR-5

.. fsd:: **LogServer Fault:** Senders continue normally, silently dropping logs.
   :id: FSD-7.1
   :links: FSD-7

.. fsd:: **Service Fault:** Core detects disconnection, marks service unavailable, transitions requests to error.
   :id: FSD-7.2
   :links: FSD-7

.. fsd:: **Timeout:** Core detects non-response (>5.0s) and triggers error state.
   :id: FSD-7.3
   :links: FSD-7

.. fsd:: **Core Fault:** Services remain operational but disconnected; attempt reconnect on restart.
   :id: FSD-7.4
   :links: FSD-7



.. fsd:: Intent Resolution (The "Brain")
   :id: FSD-8
   :links: BRD-5.6,FSD-1

.. fsd:: **Input Normalization:** Core accepts inputs (`VOICE`, `CLI`, `GUI`) as uniform text strings.
   :id: FSD-8.1
   :links: FSD-8

.. fsd:: **Command Registry:** Core maintains a registry of valid commands mapping "String" → "Callable".
   :id: FSD-8.2
   :links: FSD-8

.. fsd:: **Fast Path:** IF input matches Registry Key → Execute immediately (Deterministic).
   :id: FSD-8.3
   :links: FSD-8

.. fsd:: **Slow Path:** IF input does not match → Forward to LLM Service for inference (Probabilistic).
   :id: FSD-8.4
   :links: FSD-8



.. fsd:: User Experience (UX)
   :id: FSD-9
   :links: BRD-5.5,FSD-1.2

.. fsd:: **State Reflection:** UI must visually reflect state (Dark/Gray for Sleep, Bright/Color for Active).
   :id: FSD-9.1
   :links: FSD-9

.. fsd:: **Input Locking:** Text input disabled in Sleep; Blinking cursor only in Active.
   :id: FSD-9.2
   :links: FSD-9

.. fsd:: **Wake Triggers:** System wakes on Voice ("Hey Maggie") OR Click-to-Wake on input box.
   :id: FSD-9.3
   :links: FSD-9

.. fsd:: **Audio Feedback:**
   :id: FSD-9.4
   :links: FSD-9

   - *Sleep -> Waking (Click):* Play "Yes? Just one moment, please."
   - *Waking -> Active:* Play "How can I assist you."



.. metadata:
   :file-id: fsd-root
   :title: "Feature Specifications"
   :version: "5.0"
   :date: "2025-12-17"
   :author: "Anthony Formosa"
   :roadmap_version: "5.0"
   :template_version: "2.0"
   :status: "Active"
   :llm-permissions: read-only
   :purpose: "Define System Behavior and Capabilities"

