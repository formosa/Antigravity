# Traceability Report

**Analyzed:** 236 tags | **Violations:** 46

## SIBLING_CITATION (3)

| ID | Title | Severity | Cited Tag | Message |
| :--- | :------ | :--------- | :---------- | :-------- |
| `FSD-8` | Intent Resolution (The "Brain") | **ERROR** | FSD-1 (Process Orchestration) | Cites sibling 'FSD-1' |
| `FSD-9` | User Experience (UX) | **ERROR** | FSD-1.2 (**UI Process:** Handles user interaction (PySide6).) | Cites sibling 'FSD-1.2' |
| `ICD-4` | Response Payload Schema | **ERROR** | ICD-3 (Metadata Schema (JSON)) | Cites sibling 'ICD-3' |

## INVALID_PARENT_TIER (34)

| ID | Title | Severity | Cited Tag | Message |
| :--- | :------ | :--------- | :---------- | :-------- |
| `ICD-3` | Metadata Schema (JSON) | **ERROR** | FSD-6.3 (**Correlation:** All logs must include `request_id` for correlation across processes.) | Invalid parent tier 'FSD' for 'ICD'. Allowed: ['SAD', 'NFR'] |
| `ISP-1.2` | **Socket:** Bind `ROUTER` using config from `ICD-1`. | **ERROR** | ICD-1 (IPC Configuration (ipc_config.yaml)) | Invalid parent tier 'ICD' for 'ISP'. Allowed: ['TDD'] |
| `ISP-1.4` | **HSM:** Setup `transitions.Machine` with states from `FSD-2`. | **ERROR** | FSD-2.3 (**Required States:** `Root(DEFAULT)`, `initializing`, `sleeping`, `waking`, `active`, `busy` (`llm`, `tts`, `stt`), `error`, `shutting_down`.) | Invalid parent tier 'FSD' for 'ISP'. Allowed: ['TDD'] |
| `ISP-1.4` | **HSM:** Setup `transitions.Machine` with states from `FSD-2`. | **ERROR** | FSD-2 (Hierarchical State Machine (HSM)) | Invalid parent tier 'FSD' for 'ISP'. Allowed: ['TDD'] |
| `SAD-5` | Configuration Driven | **ERROR** | BRD-3.2 (**Customizability:** Allow extension via a modular architecture.) | Invalid parent tier 'BRD' for 'SAD'. Allowed: ['FSD', 'NFR'] |
| `TDD-1` | Component: CoreProcess | **ERROR** | FSD-1.1 (Core Hub) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.10` | Connect `PUSH` socket to `core.push_connect` (SNDHWM=1, LINGER=0) for logging. | **ERROR** | FSD-6.1 (All processes must emit logs to the central LogServer.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.11` | **Scan Logic:** On startup, iterate directories in `config.core.extensions.path`. | **ERROR** | FSD-3 (Modular Extensions (Tools/Routines)) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.14` | **Structure:** `self.command_registry: Dict[str, Callable]`. | **ERROR** | FSD-8.2 (**Command Registry:** Core maintains a registry of valid commands mapping "String" → "Callable".) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.14` | **Structure:** `self.command_registry: Dict[str, Callable]`. | **ERROR** | FSD-8 (Intent Resolution (The "Brain")) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.4` | Set `ZMQ_ROUTER_MANDATORY=1` to detect unroutable messages. | **ERROR** | NFR-5.6 (**Message Routability:** The Core must explicitly detect and handle attempts to send messages to disconnected or non-existent service identities.) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.4` | Set `ZMQ_ROUTER_MANDATORY=1` to detect unroutable messages. | **ERROR** | NFR-5 (Fault Tolerance) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.6` | Initialize HSM using `transitions.Machine`. State definitions include both statically-defined core states and dynamically-compiled states from Tool/Routine extensions. | **ERROR** | FSD-2.2 (**Dynamic Compilation:** HSM must be dynamically compiled at startup from definitions provided by Tools, Routines, and Services.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.6` | Initialize HSM using `transitions.Machine`. State definitions include both statically-defined core states and dynamically-compiled states from Tool/Routine extensions. | **ERROR** | FSD-2.3 (**Required States:** `Root(DEFAULT)`, `initializing`, `sleeping`, `waking`, `active`, `busy` (`llm`, `tts`, `stt`), `error`, `shutting_down`.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.6` | Initialize HSM using `transitions.Machine`. State definitions include both statically-defined core states and dynamically-compiled states from Tool/Routine extensions. | **ERROR** | FSD-2 (Hierarchical State Machine (HSM)) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.9` | **Timeout Monitor:** On every loop iteration, check `active_requests` for timestamps exceeding `response_timeout_s`. | **ERROR** | FSD-7.3 (**Timeout:** Core detects non-response (>5.0s) and triggers error state.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-1.9` | **Timeout Monitor:** On every loop iteration, check `active_requests` for timestamps exceeding `response_timeout_s`. | **ERROR** | FSD-7 (Error Handling Strategy) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-2.5` | `PUSH`: Connects to LogServer `PULL`. Must set `SNDHWM=1` and `LINGER=0` (Fire-and-Forget). | **ERROR** | NFR-5.3 (**Fire-and-Forget:** Log messages are acceptable to be lost if LogServer is down.) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-2.5` | `PUSH`: Connects to LogServer `PULL`. Must set `SNDHWM=1` and `LINGER=0` (Fire-and-Forget). | **ERROR** | NFR-5 (Fault Tolerance) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-2.8` | **State Awareness:** Must subscribe to HSM state changes and apply CSS classes (`sleeping`, `active`). | **ERROR** | FSD-9.1 (**State Reflection:** UI must visually reflect state (Dark/Gray for Sleep, Bright/Color for Active).) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-2.9` | **Input Control:** Widget `setReadOnly(True)` in Sleep; `installEventFilter` to catch Click-to-Wake events. | **ERROR** | FSD-9.2 (**Input Locking:** Text input disabled in Sleep; Blinking cursor only in Active.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-3` | Component: LogServerSink | **ERROR** | FSD-6.1 (All processes must emit logs to the central LogServer.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-3.4` | Execute tight poll loop (1ms timeout) to maximize throughput. | **ERROR** | NFR-4.6 (**Logging:** LogServer must support ≥ 10,000 msgs/sec.) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-3.4` | Execute tight poll loop (1ms timeout) to maximize throughput. | **ERROR** | NFR-4 (Latency & Throughput) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-4` | Component: Tool/Routine Interface | **ERROR** | FSD-3 (Modular Extensions (Tools/Routines)) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-4.3` | `get_hsm_states() -> List[Dict]`: Return state definitions for dynamic compilation. | **ERROR** | FSD-2.2 (**Dynamic Compilation:** HSM must be dynamically compiled at startup from definitions provided by Tools, Routines, and Services.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-4.3` | `get_hsm_states() -> List[Dict]`: Return state definitions for dynamic compilation. | **ERROR** | FSD-2 (Hierarchical State Machine (HSM)) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5` | Component: AudioWorkerLoop | **ERROR** | FSD-4 (Audio Acquisition (Audio Service)) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5` | Component: AudioWorkerLoop | **ERROR** | NFR-3 (Resource Isolation) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5.3` | **Stage 1 (WWD):** Process audio chunks through pvporcupine. On detection, check Core state before emitting event. | **ERROR** | FSD-4.1 (**Wake Word:** Always-on detection using `pvporcupine`.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5.3` | **Stage 1 (WWD):** Process audio chunks through pvporcupine. On detection, check Core state before emitting event. | **ERROR** | FSD-4.2 (**Constraint:** Must only send `WAKE_WORD_DETECTED` if Core is in `idle` state.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5.4` | **Stage 2 (VAD):** Apply webrtcvad (CPU) for initial speech detection, buffer frames for STT handoff. | **ERROR** | FSD-4.3 (**VAD (Stage 1):** Real-time, CPU-based VAD using `webrtcvad`.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5.5` | **State Check:** Query Core HSM state via `client.get_state()`. Only emit `WAKE_WORD_DETECTED` if state is `idle`. | **ERROR** | FSD-4.2 (**Constraint:** Must only send `WAKE_WORD_DETECTED` if Core is in `idle` state.) | Invalid parent tier 'FSD' for 'TDD'. Allowed: ['SAD', 'ICD'] |
| `TDD-5.6` | **Denoising:** Apply RNNoise or equivalent before WWD/VAD stages. Must operate within NFR-3 latency budget. | **ERROR** | NFR-3 (Resource Isolation) | Invalid parent tier 'NFR' for 'TDD'. Allowed: ['SAD', 'ICD'] |

## ORPHAN (9)

| ID | Title | Severity | Cited Tag | Message |
| :--- | :------ | :--------- | :---------- | :-------- |
| `TERM-AUDIO-PROCESS` | Audio Process | **ERROR** | None | No parent citations |
| `TERM-CORE-PROCESS` | Core Process | **ERROR** | None | No parent citations |
| `TERM-HSM` | HSM | **ERROR** | None | No parent citations |
| `TERM-LOGSERVER` | LogServer | **ERROR** | None | No parent citations |
| `TERM-ROUTINE` | Routine | **ERROR** | None | No parent citations |
| `TERM-RUNTIME-PROCESS` | Runtime Process | **ERROR** | None | No parent citations |
| `TERM-SERVICE` | Service | **ERROR** | None | No parent citations |
| `TERM-TOOL` | Tool | **ERROR** | None | No parent citations |
| `TERM-UI-PROCESS` | UI Process | **ERROR** | None | No parent citations |
