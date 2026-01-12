SAD — Architecture Definitions (Structure)
====================================================================================================

.. sad:: Architectural Patterns
   :id: SAD-1
   :links: FSD-1.1

.. sad:: **Hub-and-Spoke:** Core Process acts as the central `ROUTER` (Hub); Services are `DEALER` (Spokes).
   :id: SAD-1.1
   :links: SAD-1

.. sad:: **Decoupled Sink:** Dedicated LogServer acts as `PULL` sink for `PUSH` sources.
   :id: SAD-1.2
   :links: SAD-1

.. sad:: **No Shared Abstraction:** `ROUTER-DEALER` and `PUSH-PULL` patterns are implemented separately to avoid artificial coupling.
   :id: SAD-1.3
   :links: SAD-1

.. sad:: **Context Propagation:** `request_id` must be passed in every frame.
   :id: SAD-1.4
   :links: SAD-1



.. sad:: Process Topology
   :id: SAD-2
   :links: FSD-1.1

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



.. sad:: Integration Strategy
   :id: SAD-3
   :links: FSD-6.1,NFR-2.1,NFR-2

.. sad:: **Core ↔ Services (Request-Response):**
   :id: SAD-3.1
   :links: SAD-3

.. sad:: **Pattern:** ZeroMQ `ROUTER` (Core) ↔ `DEALER` (Service).
   :id: SAD-3.2
   :links: SAD-3

.. sad:: **Type:** Bidirectional.
   :id: SAD-3.3
   :links: SAD-3

.. sad:: **Requirement:** Core maintains routing table (client identity → socket identity).
   :id: SAD-3.4
   :links: SAD-3

.. sad:: **All Processes → LogServer (Logging):**
   :id: SAD-3.5
   :links: SAD-3

.. sad:: **Pattern:** ZeroMQ `PUSH` (Client) → `PULL` (LogServer).
   :id: SAD-3.6
   :links: SAD-3

.. sad:: **Type:** Unidirectional, Fire-and-Forget.
   :id: SAD-3.7
   :links: SAD-3

.. sad:: **Requirement:** Senders must set `SNDHWM=100` and `LINGER=0` to buffer micro-bursts without blocking.
   :id: SAD-3.8
   :links: SAD-3



.. sad:: Concurrency Model
   :id: SAD-4
   :links: NFR-5.1

.. sad:: **Receiver Threads:** Each process uses a dedicated thread to poll ZMQ sockets and push to an internal `queue.PriorityQueue`.
   :id: SAD-4.1
   :links: SAD-4

.. sad:: **Main Loop:** The main application loop processes the `PriorityQueue` to remain non-blocking.
   :id: SAD-4.2
   :links: SAD-4

.. sad:: **Queueing:**
   :id: SAD-4.3
   :links: SAD-4

.. sad:: Must use `queue.PriorityQueue`.
   :id: SAD-4.4
   :links: SAD-4

.. sad:: **Structure:** `(priority, counter, message)`.
   :id: SAD-4.5
   :links: SAD-4

.. sad:: **Ordering:** Monotonic counter (`itertools.count`) ensures FIFO within priority levels.
   :id: SAD-4.6
   :links: SAD-4

.. sad:: **Priority Levels:**
   :id: SAD-4.7
   :links: SAD-4

.. sad:: **High (0):** `shutdown`, `error_notification`, `state_change`.
   :id: SAD-4.8
   :links: SAD-4

.. sad:: **Normal (1):** Inference requests, status updates.
   :id: SAD-4.9
   :links: SAD-4



.. sad:: Configuration Driven
   :id: SAD-5
   :links: BRD-3.2

.. sad:: All IPC endpoints (addresses, ports) and parameters (queue sizes, timeouts) must be loaded from `ipc_config.yaml`.
   :id: SAD-5.1
   :links: SAD-5




.. metadata:
   :file-id: sad-root
   :title: "Architecture Definitions"
   :version: "5.0"
   :date: "2025-12-17"
   :author: "Anthony Formosa"
   :roadmap_version: "5.0"
   :template_version: "2.0"
   :status: "Active"
   :llm-permissions: read-only
   :purpose: "Define Architecture & Patterns"


