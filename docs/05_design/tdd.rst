TDD — Technical Design (Blueprints)
====================================================================================================

Component Blueprints


.. impl:: Component: CoreProcess
   :id: TDD-1
   :links: SAD-2,FSD-1.1

.. impl:: **Class Name:** `CoreProcess`
   :id: TDD-1.1
   :links: TDD-1

.. impl:: **Dependencies:** `zmq`, `queue`, `itertools`, `transitions`, `yaml`, `threading`, `importlib`, `pathlib`.
   :id: TDD-1.2
   :links: TDD-1

   **Socket Configuration:**

.. impl:: Bind `ROUTER` socket to address defined in `ipc_config.yaml` (`core.router_bind`).
   :id: TDD-1.3
   :links: ICD-1,SAD-3.2,SAD-3

.. impl:: Connect `PUSH` socket to `core.push_connect` (SNDHWM=1, LINGER=0) for logging.
   :id: TDD-1.10
   :links: FSD-6.1,SAD-3.5,SAD-3

.. impl:: Set `ZMQ_ROUTER_MANDATORY=1` to detect unroutable messages.
   :id: TDD-1.4
   :links: NFR-5.6,NFR-5

   **State Management:**

.. impl:: Initialize `active_requests` dictionary: `Dict[str, Tuple[bytes, float, str]]` (ID → Identity, Timestamp, Command).
   :id: TDD-1.5
   :links: SAD-1.4,SAD-1

.. impl:: Initialize HSM using `transitions.Machine`. State definitions include both statically-defined core states and dynamically-compiled states from Tool/Routine extensions.
   :id: TDD-1.6
   :links: FSD-2.2,FSD-2.3,FSD-2

   **Concurrency (Main Loop):**

.. impl:: **Receiver Thread:** Spawns a `threading.Thread` to poll the `ROUTER` socket and push frames to `self.queue`.
   :id: TDD-1.7
   :links: SAD-4.1,SAD-4

.. impl:: **Event Loop:** Pops items from `self.queue` (PriorityQueue) and dispatches to HSM triggers.
   :id: TDD-1.8
   :links: SAD-4.2,SAD-4

.. impl:: **Timeout Monitor:** On every loop iteration, check `active_requests` for timestamps exceeding `response_timeout_s`.
   :id: TDD-1.9
   :links: FSD-7.3,FSD-7

   **Extension Discovery:**

.. impl:: **Scan Logic:** On startup, iterate directories in `config.core.extensions.path`.
   :id: TDD-1.11
   :links: FSD-3

.. impl:: **Validation:** Parse `manifest.yaml` in subdirectories (`tools/`, `routines/`).
   :id: TDD-1.12
   :links: TDD-1

.. impl:: **Loading:** Use `importlib` to dynamically import the module specified in manifest `entry_point`.
   :id: TDD-1.13
   :links: TDD-1

   **Command Resolution:**

.. impl:: **Structure:** `self.command_registry: Dict[str, Callable]`.
   :id: TDD-1.14
   :links: FSD-8.2,FSD-8

.. impl:: **Logic:** `resolve_intent(input_str: str)` checks registry before HSM dispatch.
   :id: TDD-1.15
   :links: TDD-1



.. impl:: Component: ServiceClient
   :id: TDD-2
   :links: SAD-3.1,SAD-4

.. impl:: **Class Name:** `ServiceClient`
   :id: TDD-2.1
   :links: TDD-2

.. impl:: **Purpose:** Standardized base implementation for UI, Runtime, and Audio services.
   :id: TDD-2.2
   :links: TDD-2

.. impl:: **Dependencies:** `yaml`, `zmq`, `queue`, `itertools`, `threading`.
   :id: TDD-2.3
   :links: TDD-2

   **Socket Configuration:**

.. impl:: `DEALER`: Connects to Core `ROUTER`. Identity is auto-assigned by ZMQ.
   :id: TDD-2.4
   :links: ICD-2.1,ICD-2

.. impl:: `PUSH`: Connects to LogServer `PULL`. Must set `SNDHWM=1` and `LINGER=0` (Fire-and-Forget).
   :id: TDD-2.5
   :links: SAD-3.8,NFR-5.3,NFR-5

   **Queuing Strategy:**

.. impl:: Internal `queue.PriorityQueue` populated by a dedicated `_receiver_thread`.
   :id: TDD-2.6
   :links: SAD-4.1,SAD-4

.. impl:: Internal `queue.PriorityQueue` populated by a dedicated `_receiver_thread`.
   :id: TDD-2.6
   :links: SAD-4.1

.. impl:: Ordering enforced via `(priority, itertools.count(), message)` tuple.
   :id: TDD-2.7
   :links: SAD-4.6

   **UI Requirements:**

.. impl:: **State Awareness:** Must subscribe to HSM state changes and apply CSS classes (`sleeping`, `active`).
   :id: TDD-2.8
   :links: FSD-9.1

.. impl:: **Input Control:** Widget `setReadOnly(True)` in Sleep; `installEventFilter` to catch Click-to-Wake events.
   :id: TDD-2.9
   :links: FSD-9.2,SAD-4



.. impl:: Component: LogServerSink
   :id: TDD-3
   :links: FSD-6.1,ICD-1

.. impl:: **Class Name:** `LogServerSink`
   :id: TDD-3.1
   :links: TDD-3

.. impl:: **Dependencies:** `loguru`, `zmq`.
   :id: TDD-3.2
   :links: TDD-3

   **Socket Configuration:**

.. impl:: Bind `PULL` socket to address defined in `ipc_config.yaml` (`logserver.pull_bind`).
   :id: TDD-3.3
   :links: SAD-3.6,SAD-3

   **Processing Loop:**

.. impl:: Execute tight poll loop (1ms timeout) to maximize throughput.
   :id: TDD-3.4
   :links: NFR-4.6,NFR-4

.. impl:: Parse inbound frames as `[metadata_json, message_string]`.
   :id: TDD-3.5
   :links: ICD-2.5,ICD-2

   **Persistence:**

.. impl:: Configure `loguru` rotation (50MB) and retention (30 days).
   :id: TDD-3.6
   :links: ICD-1


   Interface Contracts


.. impl:: Component: Tool/Routine Interface
   :id: TDD-4
   :links: FSD-3

.. impl:: **Class Name:** `AbstractTool`, `AbstractRoutine` (ABC).
   :id: TDD-4.1
   :links: TDD-4

   **Abstract Methods:**

.. impl:: `initialize(core_context: CoreProcess)`: Inject Core dependencies.
   :id: TDD-4.2
   :links: TDD-4

.. impl:: `get_hsm_states() -> List[Dict]`: Return state definitions for dynamic compilation.
   :id: TDD-4.3
   :links: FSD-2.2,FSD-2

.. impl:: `handle_event(event_data: Dict) -> str`: Process business logic and return next trigger.
   :id: TDD-4.4
   :links: TDD-4

   **Manifest Contract:**

.. impl:: **Requirement:** Every extension directory must contain `manifest.yaml`.
   :id: TDD-4.5
   :links: TDD-4

.. impl:: **Schema:**
   :id: TDD-4.6
   :links: TDD-4

    - `name`: Unique identifier (string).
    - `version`: Semantic version (string).
    - `type`: "tool" | "routine".
    - `entry_point`: Relative path to python module definition (e.g., "src.plugin").



.. metadata:
   :file-id: tdd-root
   :title: "Technical Design"
   :version: "5.0"
   :date: "2025-12-17"
   :author: "Anthony Formosa"
   :roadmap_version: "5.0"
   :template_version: "2.0"
   :status: "Active"
   :llm-permissions: read-only
   :purpose: "Define Component Structure (No Logic)"

