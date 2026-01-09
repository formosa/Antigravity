
# MAGGIE Framework Documentation Hierarchy: Comprehensive Technical Analysis

## Executive Summary

This report provides a complete analysis of the MAGGIE Development Documentation Roadmap (DDR) hierarchical structure, establishing precise classification criteria, boundary definitions, and practical examples for each documentation tier. The DDR implements a seven-tier cascade from strategic business context through executable code stubs, enforcing strict traceability and vertical consistency across all layers.

----------

## 1. Documentation Hierarchy Overview

### 1.1 Architectural Philosophy

The DDR implements a **waterfall-traceable, LLM-optimized documentation architecture** where each tier answers a specific question and enforces parent-child citation relationships:

```
BRD (Why?)
  ↓ cites
NFR (Within what constraints?)
  ↓ cites
FSD (What capabilities?)
  ↓ cites
SAD (How structured?)
  ↓ cites
ICD (What contracts?)
  ↓ cites
TDD (What components?)
  ↓ cites
ISP (What code?)

```

**Key Principles:**

-   **Unidirectional Authority:** Child tiers cite parent tiers using `← |PARENT-TAG|` syntax
-   **Atomic Traceability:** Every requirement/specification has a unique, immutable tag (e.g., `|BRD-5.2|`)
-   **Persona-Driven:** Each tier assumes a distinct stakeholder perspective
-   **LLM-Parseable:** Strict formatting enables automated validation and consistency checking

----------

## 2. Tier-by-Tier Boundary Definitions

### 2.1 BRD — Business Requirements Document

**Tier Position:** Layer 1 (Root)
**Answers:** "Why are we building this?"
**Persona:** Executive Strategist / Product Owner
**Scope:** Strategic objectives, business justification, stakeholder needs

#### Classification Criteria

**INCLUDE if information:**

1.  Describes the fundamental **business problem** being solved
2.  Defines **strategic objectives** independent of technical implementation
3.  Articulates **stakeholder value propositions**
4.  Establishes **success metrics** at the organizational level (uptime SLAs, user satisfaction)
5.  States **high-level scope** boundaries (what's in/out of MVP)
6.  Identifies **environmental/operational constraints** (offline requirement, privacy mandates)

**EXCLUDE if information:**

1.  Specifies technical architectures, patterns, or technologies
2.  Defines data structures, APIs, or protocols
3.  Describes implementation details or algorithms
4.  Contains hardware specifications beyond environmental context
5.  Provides numeric performance targets more granular than SLAs

#### Qualification Rubric
| Criterion | BRD-Appropriate | Not BRD-Appropriate |
|:--|:--|:--|
| **Abstraction Level** | "Enable privacy-preserving AI" | "Use local TCP sockets" |
| **Stakeholder Focus** | "End users require offline capability" | "Runtime process uses ONNX" |
| **Temporal Scope** | "Strategic objective for 2025-2026" | "Queue timeout = 100ms" |
| **Justification Type** | "Competitive advantage" | "Prevents memory leak" |
| **Success Measure** | "99.9% uptime SLA" | "<1ms dispatch latency" |

#### Real-World Examples

**Example 1: Strategic Objective (INCLUDE)**

```
|BRD-2|: "Enable responsive, privacy-preserving AI assistant capabilities
without dependency on cloud infrastructure."

```

-   **Why BRD:** States a business-driven technology mandate (privacy, offline)
-   **Not Lower Tier:** Doesn't specify _how_ (multi-process, ZeroMQ)

**Example 2: Stakeholder Problem (INCLUDE)**

```
|BRD-4|: "Users require AI assistant capabilities but are constrained by
internet dependency, privacy concerns, and single-process limitations."

```

-   **Why BRD:** Describes the market/user pain point, not the solution
-   **Not Lower Tier:** Doesn't prescribe architecture

**Example 3: Incorrectly Classified (EXCLUDE)**

```
BAD: |BRD-X|: "Use ZeroMQ ROUTER-DEALER pattern for IPC"

```

-   **Why Not BRD:** This is a technical architecture decision (belongs in SAD)
-   **Correct Classification:** |SAD-1.1| ← |BRD-5| (traces to "offline framework" scope)

**Example 4: Scope Boundary (INCLUDE)**

```
|BRD-5.2|: "Local LLM, TTS, and STT inference."

```

-   **Why BRD:** Defines functional scope at the capability level
-   **Not Lower Tier:** Doesn't specify models, frameworks, or APIs

----------

### 2.2 NFR — Non-Functional Requirements

**Tier Position:** Layer 2
**Answers:** "Within what constraints must the system operate?"
**Persona:** Systems Administrator / Performance Engineer
**Scope:** Hardware limits, performance targets, reliability thresholds, security boundaries

#### Classification Criteria

**INCLUDE if information:**

1.  Specifies **hardware resource limits** (CPU model, VRAM capacity, RAM allocation)
2.  Defines **quantitative performance targets** (latency thresholds, throughput minimums)
3.  Establishes **reliability/availability requirements** (fault tolerance, uptime)
4.  States **security constraints** (network isolation, encryption requirements)
5.  Mandates **technology dependencies** (Python 3.11+, CUDA toolkit)
6.  Prescribes **resource utilization bounds** (max CPU %, memory footprints)

**EXCLUDE if information:**

1.  Describes business objectives or user value propositions
2.  Defines functional behavior or capabilities
3.  Specifies implementation details (class names, method signatures)
4.  Describes data schemas or message formats
5.  Provides architectural patterns (unless as constraints)

#### Qualification Rubric


| Criterion | NFR-Appropriate | Not NFR-Appropriate |
| :--- | :--- | :--- |
| **Measurability** | "<1ms dispatch latency" | "Fast IPC communication" |
| **Constraint Type** | "RTX 3080 10GB VRAM limit" | "Use GPU for inference" |
| **Enforcement** | "No process shall block >5s" | "Core routes messages" |
| **Scope** | "All communication via 127.0.0.1" | "ROUTER binds to :5555" |
| **Invariance** | "Python >=3.11 required" | "Import zmq.Context" |

#### Real-World Examples

**Example 1: Hardware Constraint (INCLUDE)**

```
|NFR-1.2|: "GPU: RTX 3080 10GB VRAM (Runtime/Inference only)."

```

-   **Why NFR:** Specifies non-negotiable hardware boundary
-   **Traces To:** |BRD-6.1| ("High-end consumer workstation")
-   **Downstream Impact:** TDD must design around 10GB VRAM limit

**Example 2: Performance Target (INCLUDE)**

```
|NFR-4.1|: "IPC Dispatch: Sub-millisecond (<1ms) for metadata-only messages."

```

-   **Why NFR:** Quantifiable performance requirement
-   **Traces To:** |BRD-8.1| ("Sub-250ms IPC dispatch")
-   **Downstream Impact:** SAD must choose non-blocking I/O patterns

**Example 3: Reliability Constraint (INCLUDE)**

```
|NFR-5.1|: "No process shall block waiting for another during standard IPC."

```

-   **Why NFR:** Non-functional reliability requirement
-   **Traces To:** |BRD-3.4| ("Reduce downtime through multi-process isolation")
-   **Downstream Impact:** SAD mandates receiver threads + queues

**Example 4: Incorrectly Classified (EXCLUDE)**

```
BAD: |NFR-X|: "Core process routes messages between UI and Runtime"

```

-   **Why Not NFR:** This describes functional behavior, not constraints
-   **Correct Classification:** |FSD-1.1| ← |NFR-5.1| (constraint on blocking)

----------

### 2.3 FSD — Feature Specification Document

**Tier Position:** Layer 3
**Answers:** "What does the system do?"
**Persona:** Product Manager / Business Analyst
**Scope:** System capabilities, functional behavior, user-facing features, workflows

#### Classification Criteria

**INCLUDE if information:**

1.  Describes **user-observable capabilities** (voice interaction, wake word detection)
2.  Defines **system behaviors** in response to events (state transitions, error handling)
3.  Specifies **feature workflows** (audio pipeline stages, intent resolution)
4.  Articulates **functional responsibilities** per component (Core routes, Runtime infers)
5.  States **business logic rules** (only send wake word if Core is idle)
6.  Describes **data flows** at the conceptual level (Audio → Core → Runtime)

**EXCLUDE if information:**

1.  Specifies technical implementations (socket types, thread models)
2.  Defines data schemas, protocols, or message formats
3.  Describes class structures or method signatures
4.  Provides performance metrics or resource limits
5.  States business objectives without functional specifications

#### Qualification Rubric


| Criterion | FSD-Appropriate | Not FSD-Appropriate |
| :--- | :--- | :--- |
| **Observability** | "UI reflects HSM state visually" | "UI uses PySide6 framework" |
| **Action Trigger** | "Wake word detection transitions to Active" | "Porcupine engine runs on CPU" |
| **Capability** | "System supports STT, TTS, LLM inference" | "Runtime uses ONNX Runtime GPU" |
| **Workflow** | "Audio → Core → Runtime → Core → UI" | "Messages use ROUTER-DEALER pattern" |
| **Business Rule** | "Only emit WAKE_WORD if Core is Idle" | "Check state via HSM trigger guard" |

#### Real-World Examples

**Example 1: Functional Capability (INCLUDE)**

```
|FSD-5.1|: "Execute transcription using faster-whisper (ONNX) on audio
buffers routed from Audio Service."

```

-   **Why FSD:** Describes what the system does (STT capability)
-   **Traces To:** |BRD-5.2| (Local STT inference), |NFR-1.2| (GPU constraint)
-   **Downstream:** SAD defines routing topology, ICD defines message schema

**Example 2: Behavioral Rule (INCLUDE)**

```
|FSD-4.2|: "Must only send WAKE_WORD_DETECTED if Core is in idle state."

```

-   **Why FSD:** Specifies conditional functional behavior
-   **Traces To:** |BRD-5.6| (HSM orchestration)
-   **Downstream:** TDD implements state query mechanism

**Example 3: Workflow Definition (INCLUDE)**

```
|FSD-8|: "Intent Resolution (The 'Brain')"
  |FSD-8.1|: Core accepts inputs (VOICE, CLI, GUI) as uniform text strings.
  |FSD-8.3|: IF input matches Registry Key → Execute immediately.
  |FSD-8.4|: IF no match → Forward to LLM Service.

```

-   **Why FSD:** Describes the decision-making workflow
-   **Traces To:** |BRD-5.6| (HSM orchestration)
-   **Downstream:** TDD defines `command_registry` structure

**Example 4: Incorrectly Classified (EXCLUDE)**

```
BAD: |FSD-X|: "Core uses zmq.ROUTER socket bound to tcp://127.0.0.1:5555"

```

-   **Why Not FSD:** This is implementation detail (architecture/protocol)
-   **Correct Classification:** |SAD-3.2| (Integration Strategy) ← |FSD-1.1| (routing capability)

----------

### 2.4 SAD — System Architecture Document

**Tier Position:** Layer 4
**Answers:** "How is the system structured?"
**Persona:** Software Architect / Systems Designer
**Scope:** Architectural patterns, component topology, integration strategies, design principles

#### Classification Criteria

**INCLUDE if information:**

1.  Defines **architectural patterns** (Hub-and-Spoke, Pub-Sub, Event-Driven)
2.  Specifies **component topology** (process diagrams, socket relationships)
3.  Describes **integration strategies** (Request-Response, Fire-and-Forget)
4.  Establishes **technology choices** for architectural concerns (ZeroMQ for IPC)
5.  Articulates **design principles** (no shared abstraction, configuration-driven)
6.  Defines **concurrency models** (receiver threads, priority queues)

**EXCLUDE if information:**

1.  Specifies exact data formats or schemas
2.  Provides class/method implementation details
3.  Defines business logic or functional workflows
4.  States performance targets (unless as design justification)
5.  Describes user-facing features

#### Qualification Rubric


| Criterion | SAD-Appropriate | Not SAD-Appropriate |
| :--- | :--- | :--- |
| **Abstraction** | "Hub-and-Spoke topology" | "Core binds port 5555" | | **Pattern** | "ROUTER-DEALER for request-response" | "Metadata frame is JSON" |
| **Principle** | "No shared base class for patterns" | "Class ServiceClient extends ABC" |
| **Technology** | "ZeroMQ for non-blocking IPC" | "import zmq; ctx = zmq.Context()" |
| **Concurrency** | "Receiver threads + PriorityQueue" | "threading.Thread(target=_poll_loop)" |

#### Real-World Examples

**Example 1: Architectural Pattern (INCLUDE)**

```
|SAD-1.1|: "Hub-and-Spoke: Core Process acts as central ROUTER (Hub);
Services are DEALER (Spokes)."

```

-   **Why SAD:** Defines the structural pattern
-   **Traces To:** |FSD-1.1| (Core routes messages)
-   **Downstream:** ICD defines frame structure, TDD implements sockets

**Example 2: Integration Strategy (INCLUDE)**

```
|SAD-3|: "Integration Strategy"
  |SAD-3.1|: Core ↔ Services (Request-Response)
  |SAD-3.2|: Pattern: ZeroMQ ROUTER (Core) ↔ DEALER (Service)
  |SAD-3.5|: All Processes → LogServer (Logging)
  |SAD-3.6|: Pattern: ZeroMQ PUSH → PULL

```

-   **Why SAD:** Describes how components integrate
-   **Traces To:** |FSD-6.1| (distributed logging), |NFR-2.1| (local TCP only)
-   **Downstream:** ICD defines message frames, TDD configures sockets

**Example 3: Design Principle (INCLUDE)**

```
|SAD-1.3|: "No Shared Abstraction: ROUTER-DEALER and PUSH-PULL patterns
are implemented separately to avoid artificial coupling."

```

-   **Why SAD:** Articulates architectural decision rationale
-   **Traces To:** |NFR-5.1| (non-blocking requirement)
-   **Downstream:** TDD creates separate CoreProcess and ServiceClient classes

**Example 4: Concurrency Model (INCLUDE)**

```
|SAD-4|: "Concurrency Model"
  |SAD-4.1|: Each process uses dedicated thread to poll ZMQ sockets.
  |SAD-4.2|: Main loop processes PriorityQueue (non-blocking).

```

-   **Why SAD:** Defines how concurrency is achieved architecturally
-   **Traces To:** |NFR-5.1| (no blocking on IPC)
-   **Downstream:** TDD specifies `_start_receiver_thread()` method

**Example 5: Topology Diagram (INCLUDE)**

```
|SAD-2|: "Process Topology"
[ASCII diagram showing ROUTER-DEALER connections and PUSH-PULL logging]

```

-   **Why SAD:** Visual representation of architectural structure
-   **Downstream:** TDD uses this to determine socket bindings per component

----------

### 2.5 ICD — Interface Control Document

**Tier Position:** Layer 5
**Answers:** "What are the data contracts?"
**Persona:** Data Engineer / Integration Specialist
**Scope:** Message schemas, configuration formats, protocol specifications, API contracts

#### Classification Criteria

**INCLUDE if information:**

1.  Defines **message schemas** (JSON structures, field types, validation rules)
2.  Specifies **configuration file formats** (YAML structure, required keys)
3.  Documents **protocol specifications** (frame ordering, header formats)
4.  Establishes **data validation rules** (mandatory fields, enum values)
5.  Describes **payload encoding** (UTF-8 text, binary PCM, multipart)
6.  Defines **API contracts** (request/response pairs, error codes)

**EXCLUDE if information:**

1.  Describes business logic or functional behavior
2.  Specifies class structures or implementation details
3.  Defines architectural patterns or topologies
4.  States performance requirements
5.  Provides code implementations


### Qualification Rubric

| Criterion | ICD-Appropriate | Not ICD-Appropriate |
| :--- | :--- | :--- |
| **Data Shape** | `{"command": "string", "priority": 0\|1}` | "Messages are prioritized" |
| **Validation** | "request_id: UUID v4 format required" | "Generate UUID on send" |
| **Encoding** | "Payload: UTF-8 JSON or raw bytes" | "Parse JSON with json.loads()" |
| **Contract** | "Response echoes original request_id" | "Track request_id in dict" |
| **Protocol** | "Frame 0: Metadata, Frame 1+: Payload" | "Use send_multipart() method" |

#### Real-World Examples

**Example 1: Message Schema (INCLUDE)**

```json
|ICD-3|: "Metadata Schema (JSON)"
{
  "source": "UI | Audio | Runtime | Core",
  "destination": "Target_Service_Name",
  "command": "function_name_or_signal",
  "request_id": "uuid-v4-string",
  "timestamp": "ISO-8601-string",
  "priority": 0 | 1,
  "payload_type": "json | binary | text"
}

```

-   **Why ICD:** Defines exact data structure and types
-   **Traces To:** |SAD-1.4| (context propagation), |SAD-4.7| (priority levels)
-   **Downstream:** TDD uses this schema for validation logic

**Example 2: Configuration Format (INCLUDE)**

```yaml
|ICD-1|: "IPC Configuration (ipc_config.yaml)"
core:
  router_bind: "tcp://127.0.0.1:5555"
  queue_maxsize: 1000
  response_timeout_s: 5.0

```

-   **Why ICD:** Specifies exact YAML structure and key names
-   **Traces To:** |SAD-5.1| (configuration-driven design), |NFR-3.3| (memory footprint)
-   **Downstream:** TDD implements `yaml.safe_load()` parsing

**Example 3: Frame Protocol (INCLUDE)**

```yaml
|ICD-2|: "Frame Structure"
  |ICD-2.2|: Outbound (DEALER): [metadata_json, payload_bytes...]
  |ICD-2.3|: Inbound (ROUTER): [service_identity, b'', metadata_json, payload_bytes...]

```

-   **Why ICD:** Defines wire-level protocol format
-   **Traces To:** |SAD-3.2| (ROUTER-DEALER pattern)
-   **Downstream:** TDD implements frame parsing logic

**Example 4: Response Contract (INCLUDE)**

```json
|ICD-4|: "Response Payload Schema"
{
  "status": "success | error",
  "error_code": "optional_string_or_null"
}

```

-   **Why ICD:** Defines API contract for error handling
-   **Traces To:** |FSD-5.4| (error reporting), |FSD-7| (error handling)
-   **Downstream:** TDD implements response validation

----------

### 2.6 TDD — Technical Design Document

**Tier Position:** Layer 6
**Answers:** "What components implement the contracts?"
**Persona:** Lead Developer / Module Designer
**Scope:** Class structures, component blueprints, method signatures, dependency graphs

#### Classification Criteria

**INCLUDE if information:**

1.  Defines **class names and purposes** (`CoreProcess`, `ServiceClient`)
2.  Specifies **method signatures** (parameters, return types)
3.  Lists **component dependencies** (imported modules, libraries)
4.  Describes **internal data structures** (dicts, queues, state machines)
5.  Articulates **component responsibilities** (what each class must do)
6.  Maps **architectural patterns to implementation units** (receiver thread per process)

**EXCLUDE if information:**

1.  Provides actual implementation code (function bodies)
2.  Defines business logic workflows
3.  Specifies data schemas or message formats
4.  States performance targets or constraints
5.  Describes user-facing features

#### Qualification Rubric


| Criterion | TDD-Appropriate | Not TDD-Appropriate |
| :--- | :--- | :--- |
| **Component** | "Class: CoreProcess" | "Core routes messages" |
| **Structure** | "active_requests: Dict\[str, Tuple\[bytes, float, str\]\]" | `{"req-123": (b'\x00\x01', 1234.56, "llm")}` |
| **Signature** | `send_request(cmd: str, payload: dict, priority: int)` | `self.dealer.send_multipart([meta, data])` |
| **Dependency** | "Import: zmq, queue, transitions" | `import zmq; ctx = zmq.Context()` |
| **Blueprint** | "Spawns receiver thread on init" | `threading.Thread(target=self._poll).start()` |

#### Real-World Examples

**Example 1: Component Blueprint (INCLUDE)**

```
|TDD-1|: "Component: CoreProcess"
  |TDD-1.1|: Class Name: CoreProcess
  |TDD-1.2|: Dependencies: zmq, queue, itertools, transitions, yaml, threading
  |TDD-1.3|: Socket: Bind ROUTER to core.router_bind (from config)
  |TDD-1.5|: State: active_requests: Dict[str, Tuple[bytes, float, str]]
  |TDD-1.7|: Concurrency: Spawns receiver thread to poll ROUTER

```

-   **Why TDD:** Defines the class structure without implementation
-   **Traces To:** |SAD-2| (topology), |ICD-1| (config schema), |SAD-4.1| (receiver thread)
-   **Downstream:** ISP provides code stubs with `pass` statements

**Example 2: Method Signature (INCLUDE)**

```python
|TDD-1.M2|: send_to_service(service_identity: bytes, frames: list) -> None
"""
Send multipart message to specific service using ROUTER envelope.
Frame structure: [service_identity, b'', metadata_json, payload_bytes...]
"""

```

-   **Why TDD:** Defines interface without logic
-   **Traces To:** |ICD-2.3| (frame structure), |SAD-3.4| (routing table)
-   **Downstream:** ISP implements with actual ZMQ calls

**Example 3: Internal Structure (INCLUDE)**

```
|TDD-2.6|: "Internal queue.PriorityQueue populated by _receiver_thread"
|TDD-2.7|: "Ordering: (priority, itertools.count(), message) tuple"

```

-   **Why TDD:** Specifies internal data structure design
-   **Traces To:** |SAD-4.5| (queue structure), |SAD-4.6| (FIFO ordering)
-   **Downstream:** ISP initializes queue in `__init__`

**Example 4: Incorrectly Classified (EXCLUDE)**

```python
BAD: |TDD-X|:
def send_log(self, level, message):
    metadata = json.dumps({"level": level, "timestamp": time.time()})
    self.log_push.send_multipart([metadata.encode(), message.encode()])

```

-   **Why Not TDD:** This is implementation code (belongs in ISP)
-   **Correct Classification:** |ISP-2| ← |TDD-2| (stub with signature only)

----------

### 2.7 ISP — Implementation Stub Prompts

**Tier Position:** Layer 7 (Leaf)
**Answers:** "What code structure should I generate?"
**Persona:** Code Generator / AI Assistant
**Scope:** Python stub code, Numpy docstrings, structural scaffolding

#### Classification Criteria

**INCLUDE if information:**

1.  Provides **executable Python stubs** (class/method definitions with `pass`)
2.  Includes **Numpy-style docstrings** (parameters, returns, references)
3.  Contains **structural scaffolding** (imports, class hierarchy)
4.  Embeds **traceability markers** (`Ref: |TAG|` in docstrings)
5.  Specifies **implementation hints** (comments on next steps)
6.  Demonstrates **correct usage patterns** (example instantiation)

**EXCLUDE if information:**

1.  Provides complete, production-ready implementations
2.  Includes complex business logic (beyond stubs)
3.  Defines data schemas or architectural patterns
4.  States requirements or specifications

#### Qualification Rubric


### Qualification Rubric

| Criterion | ISP-Appropriate | Not ISP-Appropriate |
| :--- | :--- | :--- |
| **Code State** | `def run(self): pass` | `def run(self): while True: ...` |
| **Documentation** | Numpy docstring with `Ref: |TAG|` | Inline comments only |
| **Completeness** | Structural skeleton | Fully implemented logic |
| **Guidance** | `# TODO: Implement timeout check` | Complete algorithm |
| **Traceability** | `Initialize. Ref: |TDD-1|` | |

#### Real-World Examples

**Example 1: Class Stub (INCLUDE)**

```python
|ISP-1|: "Stub: Core Process"

import zmq
import yaml
import queue
from transitions import Machine

class CoreProcess:
    """
    Orchestrates IPC between services using ZeroMQ ROUTER pattern.

    Implements
    ----------
    |TDD-1|, |FSD-1|

    Attributes
    ----------
    active_requests : dict
        Maps request_id to (identity, timestamp, command)
    queue : PriorityQueue
        Internal message queue from receiver thread
    """

    def __init__(self, config_path: str):
        """
        Initialize ZMQ Context, bind ROUTER socket.

        Parameters
        ----------
        config_path : str
            Path to ipc_config.yaml (|ICD-1|)

        References
        ----------
        |TDD-1.3|, |SAD-5.1|
        """
        pass

    def run(self) -> None:
        """
        Main event loop. Process queue, check timeouts, drive HSM.

        References
        ----------
        |TDD-1.8|, |FSD-2|
        """
        pass

```

-   **Why ISP:** Provides executable scaffold with traceability
-   **Traces To:** All parent tiers via embedded tags
-   **Usage:** Developer runs, fills `pass` statements with logic

**Example 2: Method Stub with Implementation Hints (INCLUDE)**

```python
|ISP-2.3|:

def send_log(self, level: str, message: str, request_id: str = None) -> None:
    """
    Fire-and-forget log emission.

    Parameters
    ----------
    level : str
        One of: DEBUG, INFO, WARNING, ERROR, CRITICAL
    message : str
        Log message content
    request_id : str, optional
        UUID for correlation (|ICD-3|)

    Implementation Notes
    --------------------
    1. Construct metadata dict per |ICD-3| schema
    2. Serialize to JSON, encode to bytes
    3. Call self.log_push.send_multipart([metadata, message])
    4. Wrap in try-except for zmq.Again (non-blocking)

    References
    ----------
    |TDD-2.5|, |SAD-3.8|, |FSD-6.2|
    """
    pass

```

-   **Why ISP:** Provides clear implementation guidance
-   **Traces To:** TDD (signature), ICD (schema), SAD (HWM config)

**Example 3: Configuration-Driven Initialization (INCLUDE)**

```python
|ISP-3.1|:

class ServiceClient:
    def __init__(self, service_name: str, config_path: str):
        """
        Connect DEALER and PUSH sockets per configuration.

        Parameters
        ----------
        service_name : str
            One of: 'ui', 'runtime', 'audio'
        config_path : str
            Path to ipc_config.yaml

        Implementation Steps
        --------------------
        1. Load config: cfg = yaml.safe_load(open(config_path))
        2. Extract: self.cfg = cfg['services'][service_name]
        3. Create DEALER: self.dealer = ctx.socket(zmq.DEALER)
        4. Connect: self.dealer.connect(self.cfg['dealer_connect'])
        5. Create PUSH with SNDHWM=1, LINGER=0 (|SAD-3.8|)
        6. Start receiver thread: self._start_receiver_thread()

        References
        ----------
        |TDD-2.2|, |ICD-1|, |NFR-5.3|
        """
        pass

```

-   **Why ISP:** Step-by-step implementation roadmap
-   **Traces To:** Configuration schema, architectural constraints

----------

## 3. Cross-Tier Distinction Demonstrations

### 3.1 Wake Word Detection Feature (Vertical Slice)

**BRD Perspective (Why):**

```
|BRD-5.1|: "Offline, multi-process Python framework."

```

-   **Focus:** Business justification for voice interaction without internet

**NFR Perspective (Constraints):**

```
|NFR-3.2|: "Audio Priority: CPU-bound services must prioritize low-latency."

```

-   **Focus:** Performance constraint on wake word detection

**FSD Perspective (What):**

```
|FSD-4.1|: "Wake Word: Always-on detection using pvporcupine."
|FSD-4.2|: "Must only send WAKE_WORD_DETECTED if Core is in idle state."

```

-   **Focus:** Functional behavior and business rule

**SAD Perspective (How Structured):**

```
|SAD-4.1|: "Receiver thread polls ZMQ socket, pushes to PriorityQueue."

```

-   **Focus:** Concurrency architecture for non-blocking wake word handling

**ICD Perspective (Contracts):**

```json
|ICD-3|: {"command": "WAKE_WORD_DETECTED", "priority": 0, ...}

```

-   **Focus:** Exact message format sent by Audio Service

**TDD Perspective (Components):**

```
|TDD-2.9|: "UI: installEventFilter to catch Click-to-Wake events."

```

-   **Focus:** Component-level implementation requirement

**ISP Perspective (Code):**

```python
def audio_worker_loop(client: ServiceClient):
    # Setup pvporcupine
    if is_wake_word(audio_chunk):
        client.send_request("WAKE_WORD_DETECTED", ...)

```

-   **Focus:** Executable scaffold

### 3.2 Error Handling (Cross-Cutting Concern)

| Tier | Content | Distinction |
| :--- | :--- | :--- |
| **BRD** | ` | BRD-3.4 |
| **NFR** | ` | NFR-5.2 |
| **FSD** | ` | FSD-7.2 |
| **SAD** | ` | SAD-5.1 |
| **ICD** | ` | ICD-4 |
| **TDD** | ` | TDD-1.9 |
| **ISP** | `def check_timeouts(self): pass` | Code stub |

## 4. Information Assessment & Classification Framework

### 4.1 Decision Tree for Tier Assignment

```
┌─────────────────────────────────────────────────────────────┐
│ INPUT: Unclassified Information Fragment                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
          ┌───────────────────────────────┐
          │ Does it answer "WHY build?"   │
          │ (Business value, ROI, market) │
          └───────┬───────────────────┬───┘
                  │ YES               │ NO
                  ▼                   ▼
            ┌─────────┐         ┌─────────────────────────┐
            │   BRD   │         │ Does it define LIMITS?  │
            └─────────┘         │ (Hardware, SLAs, bounds)│
                                └────┬────────────────┬───┘
                                     │ YES            │ NO
                                     ▼                ▼
                                ┌─────────┐    ┌──────────────────┐
                                │   NFR   │    │ Does it describe │
                                └─────────┘    │ CAPABILITIES?    │
                                               │ (Features, UX)   │
                                               └────┬────────┬────┘
                                                    │ YES    │ NO
                                                    ▼        ▼
                                              ┌─────────┐  ┌────────────────┐
                                              │   FSD   │  │ Does it define │
                                              └─────────┘  │ STRUCTURE?     │
                                                           │ (Patterns, topology)│
                                                           └────┬──────┬────┘
                                                                │ YES  │ NO
                                                                ▼      ▼
                                                          ┌─────────┐ ┌──────────┐
                                                          │   SAD   │ │ Is it a  │
                                                          └─────────┘ │ SCHEMA?  │
                                                                      └────┬─┬───┘
                                                                           │ │ NO
                                                                      YES  │ │
                                                                        ▼  ▼
                                                                   ┌────────────┐
                                                                   │    ICD     │
                                                                   └─────┬──────┘
                                                                         │
                                            ┌────────────────────────────┴─────────┐
                                            │ Does it define CLASS STRUCTURE?      │
                                            │ (Methods, dependencies, blueprints)  │
                                            └────┬─────────────────────────────┬───┘
                                                 │ YES                         │ NO
                                                 ▼                             ▼
                                           ┌─────────┐                   ┌─────────┐
                                           │   TDD   │                   │   ISP   │
                                           └─────────┘                   └─────────┘

```

### 4.2 Multi-Factor Classification Matrix

For ambiguous cases, score the information against these criteria (0-3 scale, 3 = strong match):


| Factor | BRD | NFR | FSD | SAD | ICD | TDD | ISP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Contains numeric metrics | 1 | 3 | 1 | 0 | 2 | 0 | 0 |
| References hardware | 1 | 3 | 0 | 1 | 0 | 0 | 0 |
| Describes user behavior | 2 | 0 | 3 | 0 | 0 | 0 | 0 |
| Names patterns | 0 | 0 | 0 | 3 | 0 | 1 | 0 |
| Defines JSON/YAML | 0 | 0 | 0 | 0 | 3 | 0 | 1 |
| Contains class names | 0 | 0 | 0 | 0 | 0 | 3 | 2 |
| Has executable code | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| Uses "must/shall" | 2 | 3 | 2 | 1 | 1 | 1 | 0 |
| Includes rationale | 3 | 1 | 1 | 3 | 0 | 2 | 0 |
| Technology-agnostic | 3 | 1 | 2 | 0 | 0 | 0 | 0 |

**Classification Rule:** Assign to tier with highest total score. Ties favor higher abstraction (left).

### 4.3 Worked Example: Classifying New Information

**Input Fragment:**

> "The system must aggregate all log messages into a single file with automatic rotation every 50MB and retain logs for 30 days."

**Step 1: Initial Assessment**

-   Contains numeric metrics? **YES** (50MB, 30 days) → NFR or ICD candidate
-   Describes hardware? **NO**
-   Describes user behavior? **NO**
-   Defines structure? **NO**
-   Defines schema? **PARTIAL** (file format unspecified)

**Step 2: Matrix Scoring**


| Factor | Score | Reasoning |
| :--- | :--- | :--- |
| Numeric metrics | NFR=3, ICD=2 | Performance/config values |
| Hardware reference | All=0 | No hardware mentioned |
| User behavior | All=0 | Internal system behavior |
| Pattern naming | All=0 | No patterns referenced |
| Schema definition | ICD=3 | Implies loguru config schema |
| Class names | All=0 | No classes mentioned |
| Executable code | All=0 | No code provided |
| Must/shall modality | NFR=3, FSD=2 | Strong requirement |
| Rationale included | All=0 | No justification given |
| Technology-agnostic | BRD=3, NFR=1 | Rotation is generic concept |

**Step 3: Tier Scores**

-   BRD: 3 (agnostic) = **3**
-   NFR: 3 (metrics) + 3 (modality) + 1 (agnostic) = **7** ← WINNER
-   FSD: 2 (modality) = **2**
-   ICD: 2 (metrics) + 3 (schema) = **5**
-   All others: **0**

**Step 4: Contextual Validation**

-   Does NFR make sense? **YES** - This is a **non-functional requirement** about operational limits (rotation size, retention period)
-   Does it trace to BRD? **YES** - Could trace to `|BRD-3.5|` ("Observability: Enhanced debugging")
-   Does it enable downstream design? **YES** - SAD chooses LogServer pattern, ICD defines config schema, TDD implements loguru

**Final Classification:**

```
|NFR-7|: Log Management Constraints ← |BRD-3.5|
  |NFR-7.1|: Logs must be aggregated to single unified file.
  |NFR-7.2|: Automatic rotation every 50MB.
  |NFR-7.3|: Retention period: 30 days minimum.

```

----------

## 5. Vertical Abstraction & Specification Protocols

### 5.1 Upward Abstraction (Child → Parent)

When an orphaned specification exists without a parent requirement, synthesize the parent by extracting the **strategic intent** or **constraint boundary**.

#### Protocol Steps

1.  **Identify the Essence:** Strip implementation details, preserve the "why" or "what limit"
2.  **Elevate Abstraction:** Transform technical specifics into business/constraint language
3.  **Validate Scope:** Ensure parent tier encompasses multiple potential child implementations
4.  **Check Redundancy:** Verify parent doesn't duplicate existing tags

#### Example 1: TDD → SAD Abstraction

**Orphaned Child (TDD):**

```
|TDD-1.7|: "Concurrency: Spawns receiver thread to poll ROUTER socket."

```

**Abstraction Process:**

-   **Technical Detail:** "Spawns receiver thread"
-   **Architectural Pattern:** "Non-blocking I/O via background polling"
-   **Constraint Context:** Must avoid blocking main loop (traces to NFR-5.1)

**Synthesized Parent (SAD):**

```
|SAD-4.1| ← |NFR-5.1|: "Receiver Threads: Each process uses dedicated
thread to poll ZMQ sockets and push to internal PriorityQueue."

```

**Validation:**

-   ✅ Covers multiple implementations (Core, UI, Runtime, Audio)
-   ✅ Describes architectural mechanism, not specific code
-   ✅ Cites constraint that mandates the pattern

#### Example 2: FSD → BRD Abstraction

**Orphaned Child (FSD):**

```
|FSD-4.1|: "Wake Word: Always-on detection using pvporcupine."

```

**Abstraction Process:**

-   **Functional Spec:** "Wake word detection"
-   **User Value:** "Hands-free voice activation"
-   **Business Objective:** "Enable natural voice interaction"

**Synthesized Parent (BRD):**

```
|BRD-5.7|: "Voice Activation: Enable hands-free voice interaction for
accessibility and user convenience."

```

**Validation:**

-   ✅ Technology-agnostic (doesn't specify pvporcupine)
-   ✅ Focuses on business value, not implementation
-   ✅ Supports multiple potential wake word technologies

#### Example 3: ICD → SAD Abstraction

**Orphaned Child (ICD):**

```json
|ICD-2.2|: "Outbound (DEALER): [metadata_json, payload_bytes...]"

```

**Abstraction Process:**

-   **Protocol Detail:** "Metadata + payload frame structure"
-   **Integration Pattern:** "Request-response messaging"
-   **Architectural Choice:** "ZeroMQ DEALER socket pattern"

**Synthesized Parent (SAD):**

```
|SAD-3.2| ← |FSD-1.1|: "Pattern: ZeroMQ ROUTER (Core) ↔ DEALER (Service)
for bidirectional request-response messaging."

```

**Validation:**

-   ✅ Defines the architectural pattern enabling the protocol
-   ✅ Justifies why frame structure exists (DEALER requirements)
-   ✅ Traces to functional requirement (Core routing)

### 5.2 Downward Specification (Parent → Child)

When a high-level requirement lacks implementation details, decompose it by extracting **concrete mechanisms** or **technical constraints**.

#### Protocol Steps

1.  **Identify Implementation Vectors:** What specific technologies/patterns enable this?
2.  **Extract Measurables:** Convert qualitative goals to quantitative specs
3.  **Partition by Concern:** Separate architecture, data, and code aspects
4.  **Maintain Traceability:** Cite parent tag in all derived children

#### Example 1: BRD → NFR Specification

**Orphaned Parent (BRD):**

```
|BRD-8.1|: "Latency: Sub-250ms IPC dispatch; <1s LLM response."

```

**Specification Process:**

-   **Implied Constraints:** System must use non-blocking I/O
-   **Hardware Requirements:** Need fast CPU for IPC, GPU for LLM
-   **Measurable Targets:** Break down into component-level latencies

**Synthesized Children (NFR):**

```
|NFR-4| ← |BRD-8.1|: "Latency & Throughput"
  |NFR-4.1|: "IPC Dispatch: Sub-millisecond (<1ms) for metadata-only."
  |NFR-4.2|: "Round Trip: <5ms metadata; <20ms for 1MB payload."
  |NFR-4.3|: "LLM Inference: <1s average response time."

```

**Validation:**

-   ✅ All children trace to parent
-   ✅ Quantifies ambiguous "sub-250ms" into specific component budgets
-   ✅ Adds granularity (metadata vs payload latency)

#### Example 2: NFR → SAD Specification

**Orphaned Parent (NFR):**

```
|NFR-5.1|: "No process shall block waiting for another during IPC."

```

**Specification Process:**

-   **Architectural Implication:** Need asynchronous messaging
-   **Pattern Selection:** ZeroMQ with dedicated receiver threads
-   **Data Structure:** Internal queues to decouple I/O from logic

**Synthesized Children (SAD):**

```
|SAD-4| ← |NFR-5.1|: "Concurrency Model"
  |SAD-4.1|: "Receiver Threads: Dedicated thread polls ZMQ sockets."
  |SAD-4.2|: "Main Loop: Processes PriorityQueue (non-blocking)."
  |SAD-4.3|: "Queueing: Must use queue.PriorityQueue."

```

**Validation:**

-   ✅ Translates constraint into concrete architectural decisions
-   ✅ Specifies mechanism that enforces parent requirement
-   ✅ Enables multiple implementations (Core, Services)

#### Example 3: FSD → ICD Specification

**Orphaned Parent (FSD):**

```
|FSD-6.3|: "Correlation: All logs must include request_id."

```

**Specification Process:**

-   **Data Requirement:** request_id field in log metadata
-   **Format Constraint:** Must be UUID v4 format
-   **Protocol Rule:** Must be propagated in every IPC frame

**Synthesized Children (ICD):**

```
|ICD-3| ← |FSD-6.3|: "Metadata Schema (JSON)"
{
  "request_id": "uuid-v4-string",  // REQUIRED
  ...
}

|ICD-2.5| ← |FSD-6.3|: "Log Frame: [metadata_json, message_string]"
// Metadata MUST include request_id from originating event

```

**Validation:**

-   ✅ Defines exact data structure to implement feature
-   ✅ Specifies format constraint (UUID v4)
-   ✅ Covers all message types (IPC and logging)

### 5.3 Lateral Expansion (Sibling Generation)

When a tag exists in isolation but implies peer requirements, generate siblings by identifying **parallel concerns** at the same abstraction level.

#### Example: Generating FSD Siblings

**Existing Singleton:**

```
|FSD-7.1|: "LogServer Fault: Senders continue, drop logs silently."

```

**Implied Parallel Concerns:**

-   What about UI/Runtime/Audio faults?
-   What about Core faults?
-   What about timeout scenarios?

**Generated Siblings:**

```
|FSD-7| ← |BRD-2|, |NFR-5|: "Error Handling Strategy"
  |FSD-7.1|: "LogServer Fault: Senders continue, drop logs silently."
  |FSD-7.2|: "Service Fault: Core detects, marks unavailable, error state."
  |FSD-7.3|: "Timeout: Core detects non-response >5s, triggers error."
  |FSD-7.4|: "Core Fault: Services disconnect, attempt reconnect."

```

**Validation:**

-   ✅ All siblings address fault tolerance at same abstraction (behavior)
-   ✅ Comprehensive coverage of failure modes
-   ✅ Uniform citation of parent requirements

----------

## 6. Advanced Classification Scenarios

### 6.1 Hybrid Information Fragments

Some statements contain information spanning multiple tiers. Apply **decomposition** to separate concerns.

#### Scenario 1: Technology-Constraint Hybrid

**Input:**

> "Use ZeroMQ ROUTER-DEALER pattern because it provides non-blocking, fault-isolated IPC required by the reliability SLA."

**Decomposition:**

1.  **Business Requirement (BRD):**

```
|BRD-2|: "System must ensure fault tolerance and maintainability."

```

2.  **Constraint (NFR):**

```
|NFR-5.1| ← |BRD-2|: "No process shall block waiting for another."

```

3.  **Architecture (SAD):**

```
|SAD-3.2| ← |NFR-5.1|: "Pattern: ZeroMQ ROUTER-DEALER for non-blocking IPC."

```

4.  **Rationale (SAD):**

```
|SAD-3.2.R1|: "ROUTER-DEALER chosen over REQ-REP because:
- Asynchronous (meets NFR-5.1)
- Identity-based routing (enables fault isolation per NFR-5.2)"

```

#### Scenario 2: Feature-Schema Hybrid

**Input:**

> "The system shall log all inference requests with timestamp, request_id, model_name, and latency in JSON format."

**Decomposition:**

1.  **Feature (FSD):**

```
|FSD-6.4| ← |BRD-3.5|: "Traceability: 100% request coverage in logs."

```

2.  **Data Contract (ICD):**

```json
|ICD-5| ← |FSD-6.4|: "Inference Log Schema"
{
  "timestamp": "ISO-8601-string",
  "request_id": "uuid-v4",
  "model_name": "string",
  "latency_ms": "float"
}

```

3.  **Implementation (TDD):**

```
|TDD-3.5| ← |ICD-5|: "Parse inbound frames as [metadata_json, message_string]
where metadata conforms to ICD-5 schema."

```

### 6.2 Temporal Classification Shifts

Information may move between tiers as the project evolves. Recognize these transitions.

#### Example: Prototype → Production Shift

**Phase 1 (MVP - BRD):**

```
|BRD-9.2|: "Future: Multi-GPU ONNX worker pool."

```

-   **Status:** Out of scope, strategic placeholder

**Phase 2 (Enhancement - NFR):**

```
|NFR-8| ← |BRD-9.2|: "GPU Scalability"
  |NFR-8.1|: "Support up to 4 NVIDIA GPUs (A100 40GB each)."
  |NFR-8.2|: "Linear throughput scaling: 4x GPUs = 3.5x throughput."

```

-   **Status:** Now a constraint for upcoming release

**Phase 3 (Implementation - SAD):**

```
|SAD-6| ← |NFR-8|: "Multi-GPU Topology"
  |SAD-6.1|: "Pattern: Worker Pool with GPU Affinity Pinning."
  |SAD-6.2|: "Load Balancer: Round-robin across DEALER sockets."

```

-   **Status:** Architectural design in progress

### 6.3 Cross-Document References

Some information exists at intersections. Use **composite tags** to maintain traceability.

#### Example: Security Spanning BRD + NFR

**Business Context (BRD):**

```
|BRD-6.3|: "Security: All communication limited to local sockets."

```

**Technical Constraint (NFR):**

```
|NFR-2| ← |BRD-6.3|: "Security & Network"
  |NFR-2.1|: "All communication via 127.0.0.1 (no external access)."
  |NFR-2.2|: "No cloud dependencies for runtime operations."

```

**Architecture (SAD):**

```
|SAD-3.2| ← |NFR-2.1|: "ZeroMQ binds to tcp://127.0.0.1:* exclusively."

```

**Configuration (ICD):**

```yaml
|ICD-1| ← |SAD-3.2|:
core:
  router_bind: "tcp://127.0.0.1:5555"  # Localhost only per NFR-2.1

```

**Composite Traceability:**

```
|ICD-1| ← |SAD-3.2| ← |NFR-2.1| ← |BRD-6.3|

```

----------

## 7. Reconciliation & Integrity Protocols

### 7.1 The Manifest System

Each document section includes a `reconciliation_manifest` tracking:

```yaml
.. reconciliation_manifest:
   :section_id: "fsd-root"
   :integrity_status: "CLEAN" | "DIRTY"
   :timestamp: "2025-12-17"
   :tag_count: 46
   :tag_inventory: ["FSD-1", "FSD-1.1", ..., "FSD-9.4"]
   :pending_items: []

```

### 7.2 Dirty Flag Triggers

**Automatic DIRTY Status When:**

1.  **Tag Modified:** Any edit to a tag's content
2.  **Tag Deleted:** Removal of a tag and its downstream citations
3.  **Tag Added:** New tag without parent validation
4.  **Child Orphaned:** Parent deleted but children remain
5.  **Inventory Mismatch:** Tag count ≠ actual tags in section

### 7.3 Pending Items Schema

When inconsistencies detected, append to `pending_items`:

```json
{
  "target_tag": "FSD-4.4",
  "source_trigger": "NFR-1.1",
  "issue_type": "CONSTRAINT_VIOLATION",
  "description": "NFR-1.1 now mandates CPU-only for Audio, but FSD-4.4
                  specifies GPU-based Silero VAD. Resolve conflict."
}

```

**Issue Types:**

-   `CONSTRAINT_VIOLATION`: Child violates modified parent constraint
-   `MISSING_PARENT`: Orphaned child needs upstream justification
-   `BROKEN_CITATION`: Tagged parent doesn't exist
-   `DUPLICATE_SPEC`: Multiple children specify same implementation

### 7.4 Reconciliation Workflow

```
1. Detect Change → Set integrity_status = "DIRTY"
2. Analyze Impact → Scan all downstream citations
3. Generate Pending Items → Document conflicts
4. Human Review → Architect resolves conflicts
5. Update Tags → Modify content, citations
6. Validate Inventory → Recount tags, update manifest
7. Clear Dirty Flag → integrity_status = "CLEAN"

```

#### Example: Reconciliation After NFR Change

**Initial State:**

```
|NFR-3.3| ← |BRD-6.1|: "Memory (Core Queue): 1000 cap, ~10-50 MB."
|ICD-1|: core.queue_maxsize: 1000
|TDD-1|: self.queue = PriorityQueue(maxsize=config['queue_maxsize'])

```

**Change Event:**

```
MODIFIED: |NFR-3.3| → "Memory (Core Queue): 2000 cap, ~20-100 MB."

```

**Manifest Update:**

```yaml
:integrity_status: "DIRTY"
:pending_items:
  - target_tag: "ICD-1"
    source_trigger: "NFR-3.3"
    issue_type: "CONSTRAINT_VIOLATION"
    description: "Config schema specifies 1000, NFR now requires 2000."

```

**Resolution:**

```yaml
# Update ICD-1
core:
  queue_maxsize: 2000  # Updated per NFR-3.3 revision

# TDD-1 inherits automatically (no change needed - reads from config)

# Clear manifest
:integrity_status: "CLEAN"
:pending_items: []

```

----------

## 8. Practical Application Guidelines

### 8.1 New Feature Workflow

**Scenario:** Add "Voice Sentiment Analysis" feature

**Step 1: BRD (Business Justification)**

```
|BRD-10|: "Sentiment-Aware Responses"
Enable context-aware emotional intelligence to improve user satisfaction
and engagement metrics (target: 25% increase in session duration).

```

**Step 2: NFR (Constraints)**

```
|NFR-9| ← |BRD-10|: "Sentiment Analysis Constraints"
  |NFR-9.1|: CPU-based inference (max 50ms latency per audio chunk).
  |NFR-9.2|: Model size <100MB (fits in system RAM).
  |NFR-9.3|: Accuracy: F1 score ≥ 0.75 on IEMOCAP dataset.

```

**Step 3: FSD (Behavior)**

```
|FSD-10| ← |NFR-9|: "Sentiment Detection Pipeline"
  |FSD-10.1|: Audio Service extracts prosodic features (pitch, energy).
  |FSD-10.2|: Sentiment classifier runs asynchronously (non-blocking).
  |FSD-10.3|: Results tagged to request_id, sent to Core.
  |FSD-10.4|: LLM Service receives sentiment context in prompt metadata.

```

**Step 4: SAD (Architecture)**

```
|SAD-7| ← |FSD-10.2|: "Asynchronous Sentiment Processing"
  |SAD-7.1|: Pattern: Fire-and-forget PUSH (Audio) → PULL (Core).
  |SAD-7.2|: No blocking on sentiment result (best-effort enrichment).

```

**Step 5: ICD (Contracts)**

```json
|ICD-6| ← |SAD-7.1|: "Sentiment Metadata Schema"
{
  "request_id": "uuid-v4",
  "sentiment": {
    "label": "neutral" | "positive" | "negative" | "unknown",
    "confidence": 0.0-1.0,
    "valence": -1.0 to +1.0,
    "arousal": 0.0 to 1.0
  }
}

```

**Step 6: TDD (Component Design)**

```
|TDD-5| ← |ICD-6|: "Component: SentimentClassifier"
  |TDD-5.1|: Class: SentimentClassifier (runs in Audio Process).
  |TDD-5.2|: Dependencies: librosa, numpy, onnxruntime (CPU).
  |TDD-5.3|: Method: analyze(audio_chunk: np.ndarray) -> Dict.
  |TDD-5.4|: Internal: ONNX model loaded on init (<100MB per NFR-9.2).

```

**Step 7: ISP (Code Stub)**

```python
|ISP-6| ← |TDD-5|:

import numpy as np
import onnxruntime as ort

class SentimentClassifier:
    """
    CPU-based sentiment analysis from audio prosody.

    Implements
    ----------
    |TDD-5|, |FSD-10|

    Constraints
    -----------
    |NFR-9.1|: Max 50ms latency
    |NFR-9.2|: Model <100MB
    """

    def __init__(self, model_path: str):
        """
        Load ONNX model for CPU inference.

        Parameters
        ----------
        model_path : str
            Path to sentiment.onnx (<100MB per |NFR-9.2|)

        References
        ----------
        |TDD-5.4|
        """
        pass

    def analyze(self, audio_chunk: np.ndarray) -> dict:
        """
        Extract sentiment from audio prosody.

        Parameters
        ----------
        audio_chunk : np.ndarray
            PCM audio (16kHz, mono)

        Returns
        -------
        dict
            Sentiment metadata per |ICD-6| schema

        References
        ----------
        |FSD-10.1|, |NFR-9.1|
        """
        pass

```

### 8.2 Refactoring Existing Documentation

**Scenario:** Discovered `|FSD-4.4|` incorrectly specifies GPU-based VAD, violating `|NFR-1.1|` (CPU-only Audio)

**Step 1: Identify Conflict**

```
|NFR-1.1|: "CPU: AMD Ryzen 9 5900X (Audio/Core must run here)."
|FSD-4.4|: "VAD (Stage 2): Silero via ONNX Runtime GPU."
           ^^^^^^^^^^^^ CONFLICT: Audio process can't use GPU

```

**Step 2: Mark Dirty**

```yaml
.. reconciliation_manifest (FSD):
   :integrity_status: "DIRTY"
   :pending_items:
     - target_tag: "FSD-4.4"
       source_trigger: "NFR-1.1"
       issue_type: "CONSTRAINT_VIOLATION"
       description: "FSD-4.4 specifies GPU inference but NFR-1.1 restricts
                     Audio Process to CPU only."

```

**Step 3: Resolve Conflict**

**Option A: Move to Runtime Process (Architecture Change)**

```
REVISED |FSD-4.4| ← |NFR-1.2|: "VAD (Stage 2): Silero via ONNX Runtime
GPU in Runtime Process. Audio sends raw buffer to Core for routing."

NEW |SAD-8|: "Audio-to-Runtime VAD Pipeline"
  |SAD-8.1|: Audio (webrtcvad) → Core → Runtime (Silero) → Core.
  |SAD-8.2|: Adds 10-20ms IPC overhead (acceptable per NFR-4.2).

```

**Option B: Use CPU-based Silero (Simpler)**

```
REVISED |FSD-4.4| ← |NFR-1.1|, |BRD-5.2|: "VAD (Stage 2): Silero via
ONNX Runtime CPU. Runs locally in Audio Process."

UPDATE |NFR-9.4|: "Silero VAD CPU Latency: <30ms per chunk."

```

**Step 4: Cascade Updates**

```
UPDATE |TDD-2.X|: "Audio Process: ONNX Runtime CPU session for Silero."
UPDATE |ICD-X|: Remove GPU memory allocation from audio config.
CLEAN reconciliation_manifest.

```

----------

## 9. Common Pitfalls & Anti-Patterns

### 9.1 Anti-Pattern: Technology in BRD

**WRONG:**

```
|BRD-X|: "Use ZeroMQ for inter-process communication."

```

**Why Wrong:** BRD should be technology-agnostic. "ZeroMQ" is an implementation detail.

**CORRECT:**

```
|BRD-5.1|: "Offline, multi-process framework with low-latency IPC."
|NFR-5.1| ← |BRD-5.1|: "No process blocking on IPC (sub-ms dispatch)."
|SAD-3.2| ← |NFR-5.1|: "Technology: ZeroMQ ROUTER-DEALER pattern."

```

### 9.2 Anti-Pattern: Business Logic in TDD

**WRONG:**

```python
|TDD-X|:
def handle_wake_word(self):
    """Only send WAKE_WORD if Core is idle."""
    if self.core_state == "idle":
        self.send_request("WAKE_WORD")

```

**Why Wrong:** TDD defines structure, not logic. Business rules belong in FSD.

**CORRECT:**

```
|FSD-4.2|: "Must only send WAKE_WORD_DETECTED if Core is in idle state."
|TDD-X| ← |FSD-4.2|: "Method: check_core_state() -> bool"
|ISP-X| ← |TDD-X|: [Code stub with logic implementation]

```

### 9.3 Anti-Pattern: Schema in SAD

**WRONG:**

```json
|SAD-X|: "Metadata Format"
{"command": "string", "request_id": "uuid"}

```

**Why Wrong:** SAD defines patterns, not data shapes. Schemas belong in ICD.

**CORRECT:**

```
|SAD-3.4|: "Requirement: Core maintains routing table (identity → socket)."
|ICD-3| ← |SAD-3.4|: [JSON schema with request_id field]

```

### 9.4 Anti-Pattern: Implementation in ISP

**WRONG:**

```python
|ISP-X|:
def send_log(self, level, msg):
    meta = json.dumps({"level": level, "ts": time.time()})
    self.push.send_multipart([meta.encode(), msg.encode()])

```

**Why Wrong:** ISP provides stubs, not complete implementations.

**CORRECT:**

```python
|ISP-X|:
def send_log(self, level: str, msg: str) -> None:
    """
    Fire-and-forget log emission.

    Implementation Steps
    --------------------
    1. Construct metadata per |ICD-3|
    2. Serialize to JSON, encode UTF-8
    3. Call self.push.send_multipart([meta, msg])
    4. Wrap in try-except for zmq.Again

    References
    ----------
    |TDD-2.5|, |SAD-3.8|
    """
    pass

```

### 9.5 Anti-Pattern: Circular Citations

**WRONG:**

```
|NFR-5.1| ← |SAD-4.1|: "No blocking on IPC."
|SAD-4.1| ← |NFR-5.1|: "Use receiver threads."

```

**Why Wrong:** Creates circular dependency. Parent → Child flow must be strictly downward.

**CORRECT:**

```
|NFR-5.1| ← |BRD-3.4|: "No blocking on IPC."
|SAD-4.1| ← |NFR-5.1|: "Pattern: Receiver threads + queues."

```

----------

## 10. LLM-Specific Optimization Strategies

### 10.1 Contextual Chunking for Token Efficiency

**Problem:** Full DDR exceeds LLM context windows.

**Solution:** Hierarchical retrieval with tag-based indexing.

```python
# Pseudo-code for LLM retrieval system
def get_context_for_tag(tag_id: str, depth: int = 2) -> str:
    """
    Retrieve tag + ancestors + children up to depth levels.

    Example: get_context_for_tag("FSD-4.2", depth=2)
    Returns:
      - FSD-4.2 (target)
      - FSD-4 (parent block)
      - NFR-1.1, BRD-5.6 (grandparents via citations)
      - TDD-2.9 (child implementation)
    """
    context = fetch_tag_content(tag_id)
    context += fetch_ancestors(tag_id, depth)
    context += fetch_children(tag_id, depth)
    return context

```

### 10.2 Validation Prompts

**Integrity Check Prompt:**

```
You are validating DDR integrity. Check:
1. Does every ← |TAG| citation reference an existing tag?
2. Does tag_inventory match actual tags in section?
3. Are there any orphaned children without parents?
4. Do all ISP stubs trace to TDD blueprints?

Report violations as JSON:
{
  "broken_citations": ["FSD-X.Y ← |MISSING|"],
  "orphans": ["TDD-5"],
  "inventory_errors": {"expected": 46, "actual": 45}
}

```

**Classification Prompt:**

```
Given: "The system must rotate logs every 50MB."

Classify into tier using decision tree:
1. Business value? NO
2. Hardware/SLA constraint? YES → Candidate: NFR
3. Functional behavior? PARTIAL (implied)
4. Score matrix...

Output:
{
  "tier": "NFR",
  "tag_id": "NFR-7.2",
  "parent_citation": "|BRD-3.5|",
  "rationale": "Operational constraint on log storage."
}

```

### 10.3 Reconciliation Prompts

**Dirty Flag Resolution:**

```
Context:
  |NFR-3.3| changed: queue_maxsize 1000 → 2000
  Pending items: ICD-1 violates new constraint

Task:
1. Update |ICD-1| config schema: queue_maxsize: 2000
2. Verify |TDD-1| reads from config (auto-inherits)
3. Check |ISP-1| stub references config loading
4. Clear pending_items, set integrity_status: CLEAN

Output updated sections with change markers:
```yaml
# UPDATED |ICD-1|
core:
  queue_maxsize: 2000  # ← Modified per NFR-3.3 revision

```

----------

## 11. Summary Reference Tables

### 11.1 Quick Classification Guide

| Information Type | Primary Tier | Secondary Tier (if hybrid) |
|-------------------------|--------------|----------------------------|
| Business goal | BRD | - |
| Market problem | BRD | - |
| SLA target | BRD | NFR (if quantified) |
| Hardware spec | NFR | - |
| Performance target | NFR | - |
| Security constraint | NFR | BRD (if strategic) |
| User workflow | FSD | - |
| Feature capability | FSD | - |
| Error handling behavior | FSD | - |
| Architectural pattern | SAD | - |
| Component topology | SAD | - |
| Technology choice | SAD | NFR (if constraint-driven) |
| JSON schema | ICD | - |
| Config format | ICD | - |
| API contract | ICD | - |
| Class structure | TDD | - |
| Method signature | TDD | ISP (if stub included) |
| Dependency list | TDD | - |
| Code stub | ISP | - |
| Docstring | ISP | - |

### 11.2 Traceability Validation Checklist

-   [ ] Every tag has format `|TIER-N|` or `|TIER-N.M|`
-   [ ] Every child cites parent(s) using `← |PARENT|`
-   [ ] No forward references (child cited before parent defined)
-   [ ] No sibling citations (FSD-X.1 ← FSD-X.2)
-   [ ] No circular chains (A ← B ← A)
-   [ ] Reconciliation manifest matches actual tag count
-   [ ] No orphaned tags (except BRD root level)
-   [ ] All ISP stubs reference TDD components
-   [ ] All TDD components cite ICD schemas (where applicable)
-   [ ] All SAD patterns trace to NFR constraints or FSD features

### 11.3 Persona-Question-Output Map


| Tier | Persona | Core Question | Typical Output |
| :--- | :--- | :--- | :--- |
| BRD | Executive | "Why invest?" | ROI justification, strategic objectives |
| NFR | SysAdmin | "What limits?" | Performance SLAs, hardware specs |
| FSD | Product Manager | "What features?" | Use cases, workflows, acceptance criteria |
| SAD | Architect | "What structure?" | Topology diagrams, pattern selections |
| ICD | Data Engineer | "What contracts?" | JSON schemas, YAML configs, API specs |
| TDD | Lead Developer | "What classes?" | Component blueprints, method signatures |
| ISP | Code Generator | "What scaffold?" | Python stubs with docstrings |

----------

## 12. Conclusion

The MAGGIE DDR implements a **seven-tier, vertically-traceable documentation architecture** optimized for both human comprehension and LLM-assisted development. Key takeaways:

1.  **Strict Hierarchy:** Each tier answers one question, cites parents, enables children
2.  **Immutable IDs:** Tags are database keys, never resequenced
3.  **Reconciliation:** Dirty flags track cascading impacts of changes
4.  **Abstraction/Specification:** Orphans resolved by synthesizing parents or decomposing children
5.  **LLM Optimization:** Tag-based retrieval, validation prompts, and structured formats enable AI collaboration

**Next Actions:**

-   Use decision tree (Section 4.1) for real-time classification
-   Apply matrix scoring (Section 4.2) for ambiguous cases
-   Follow upward/downward protocols (Section 5) for orphan resolution
-   Reference anti-patterns (Section 9) to avoid common mistakes
-   Deploy LLM prompts (Section 10.2) for automated validation

This framework ensures every piece of information—from strategic intent through executable code—maintains precise traceability, enabling confident modification, extension, and AI-assisted generation across the entire MAGGIE application lifecycle.

----------


## 13. Extended Classification Scenarios & Edge Cases

### 13.1 Multi-Tier Decomposition Patterns

#### Pattern 1: Security Requirement Cascade

**Business Driver (BRD):**

```
|BRD-11|: "Data Sovereignty Compliance"
Ensure all user data remains within jurisdictional boundaries to comply
with GDPR, CCPA, and healthcare data protection regulations. This enables
deployment in regulated industries (healthcare, finance, government).

```

-   **Abstraction:** Regulatory compliance as competitive advantage
-   **Stakeholder:** Legal/Compliance teams, Enterprise customers

**System Constraint (NFR):**

```
|NFR-10| ← |BRD-11|: "Data Locality Enforcement"
  |NFR-10.1|: No network transmission beyond localhost (127.0.0.1).
  |NFR-10.2|: No filesystem access outside designated data directory.
  |NFR-10.3|: All model weights must be locally stored (<5GB total).
  |NFR-10.4|: Encryption at rest: AES-256 for persistent logs/state.

```

-   **Abstraction:** Technical boundaries enforcing business requirement
-   **Measurable:** File paths, encryption standards, size limits

**Functional Specification (FSD):**

```
|FSD-11| ← |NFR-10|: "Secure Data Handling"
  |FSD-11.1|: Core validates all file paths against whitelist before access.
  |FSD-11.2|: LogServer encrypts files before writing to disk.
  |FSD-11.3|: Runtime rejects model load requests outside approved directory.
  |FSD-11.4|: UI displays data locality status indicator (green="local only").

```

-   **Abstraction:** Observable system behaviors enforcing constraints
-   **User-Facing:** Status indicators, error messages

**Architecture (SAD):**

```
|SAD-9| ← |FSD-11.1|: "Path Validation Strategy"
  |SAD-9.1|: Pattern: Whitelist validator with chroot-style restriction.
  |SAD-9.2|: Core maintains allowed_paths registry (loaded from config).
  |SAD-9.3|: All Services query Core before filesystem operations.

```

-   **Abstraction:** Architectural mechanism implementing validation
-   **Technology-Neutral:** Doesn't specify validation library

**Data Contract (ICD):**

```yaml
|ICD-7| ← |SAD-9.2|: "Security Configuration Schema"
security:
  allowed_directories:
    - "./models"
    - "./logs"
    - "./extensions"
  encryption:
    algorithm: "AES-256-CBC"
    key_derivation: "PBKDF2"
    iterations: 100000

```

-   **Abstraction:** Exact configuration structure
-   **Validation:** YAML schema with required fields

**Component Design (TDD):**

```
|TDD-6| ← |ICD-7|, |SAD-9.1|: "Component: PathValidator"
  |TDD-6.1|: Class: PathValidator
  |TDD-6.2|: Dependencies: pathlib, os
  |TDD-6.3|: Method: is_allowed(path: Path) -> bool
  |TDD-6.4|: Internal: _normalize_path() resolves symlinks, checks whitelist
  |TDD-6.5|: Raises: SecurityError if path outside allowed directories

```

-   **Abstraction:** Class structure without implementation logic
-   **Contract:** Method signatures, exceptions

**Code Stub (ISP):**

```python
|ISP-7| ← |TDD-6|:

from pathlib import Path
from typing import List

class PathValidator:
    """
    Validates filesystem paths against whitelist.

    Implements
    ----------
    |TDD-6|, |FSD-11.1|

    Security
    --------
    |NFR-10.2|: Prevents directory traversal attacks

    Attributes
    ----------
    allowed_dirs : List[Path]
        Whitelisted directories from |ICD-7|
    """

    def __init__(self, allowed_dirs: List[str]):
        """
        Initialize validator with allowed directories.

        Parameters
        ----------
        allowed_dirs : List[str]
            Paths from security.allowed_directories (|ICD-7|)

        Implementation Notes
        --------------------
        1. Convert strings to Path objects
        2. Resolve to absolute paths (resolve symlinks)
        3. Store in self.allowed_dirs

        References
        ----------
        |TDD-6.2|, |SAD-9.2|
        """
        pass

    def is_allowed(self, path: Path) -> bool:
        """
        Check if path is within allowed directories.

        Parameters
        ----------
        path : Path
            Path to validate

        Returns
        -------
        bool
            True if path is within whitelist

        Raises
        ------
        SecurityError
            If path attempts directory traversal (|TDD-6.5|)

        Implementation Notes
        --------------------
        1. Resolve path to absolute (handle .., symlinks)
        2. Check if any allowed_dir is parent of path
        3. Use path.is_relative_to() for safety

        References
        ----------
        |TDD-6.3|, |FSD-11.1|
        """
        pass

```

**Traceability Chain:**

```
|ISP-7| ← |TDD-6| ← |ICD-7|, |SAD-9| ← |FSD-11| ← |NFR-10| ← |BRD-11|

```

----------

#### Pattern 2: Performance Optimization Cascade

**Business Goal (BRD):**

```
|BRD-12|: "Real-Time Conversational Experience"
Enable fluid, human-like conversational flow with minimal perceived latency
to increase user engagement and reduce abandonment rates (target: <5% session
abandonment due to lag).

```

**Performance Constraint (NFR):**

```
|NFR-11| ← |BRD-12|: "End-to-End Latency Budget"
  |NFR-11.1|: Voice-to-Response (E2E): ≤3s (95th percentile).
  |NFR-11.2|: Breakdown: STT(500ms) + LLM(1500ms) + TTS(800ms) + IPC(200ms).
  |NFR-11.3|: First-token latency (LLM): ≤200ms.
  |NFR-11.4|: GPU utilization: ≥80% during inference (avoid idle waste).

```

**Feature Specification (FSD):**

```
|FSD-12| ← |NFR-11|: "Progressive Response Rendering"
  |FSD-12.1|: UI displays "thinking" indicator within 100ms of user input.
  |FSD-12.2|: LLM tokens stream to UI as generated (no buffer wait).
  |FSD-12.3|: TTS begins synthesis after first sentence (≥5 tokens).
  |FSD-12.4|: Audio playback starts before full synthesis completes.

```

**Architecture (SAD):**

```
|SAD-10| ← |FSD-12.2|: "Streaming Architecture"
  |SAD-10.1|: Pattern: Producer-Consumer with bounded queues.
  |SAD-10.2|: LLM yields tokens to queue (non-blocking generation).
  |SAD-10.3|: UI consumes tokens via polling (100ms interval).
  |SAD-10.4|: Back-pressure: LLM pauses if queue full (size=50 tokens).

```

**Data Contract (ICD):**

```json
|ICD-8| ← |SAD-10.2|: "Streaming Token Schema"
{
  "type": "token_delta" | "stream_end",
  "request_id": "uuid-v4",
  "sequence_num": 0,  // Monotonic counter for ordering
  "token": "string",  // Single token (or null if stream_end)
  "cumulative_text": "string"  // Full text so far (for UI fallback)
}

```

**Component Design (TDD):**

```
|TDD-7| ← |ICD-8|, |SAD-10.2|: "Component: LLMStreamer"
  |TDD-7.1|: Class: LLMStreamer (runs in Runtime Process)
  |TDD-7.2|: Dependencies: onnxruntime-gpu, queue, threading
  |TDD-7.3|: Method: generate_stream(prompt: str, request_id: str) -> Generator
  |TDD-7.4|: Internal: token_queue (maxsize=50 per SAD-10.4)
  |TDD-7.5|: Sends token_delta messages via ServiceClient for each yield

```

**Code Stub (ISP):**

```python
|ISP-8| ← |TDD-7|:

from typing import Generator
import queue
import threading

class LLMStreamer:
    """
    Streaming text generation with back-pressure control.

    Implements
    ----------
    |TDD-7|, |FSD-12.2|

    Performance
    -----------
    |NFR-11.3|: First token within 200ms
    |NFR-11.4|: Maintains ≥80% GPU utilization

    Attributes
    ----------
    token_queue : queue.Queue
        Bounded queue for back-pressure (|SAD-10.4|)
    """

    def __init__(self, model_session, client: ServiceClient):
        """
        Initialize streamer with ONNX session and IPC client.

        Parameters
        ----------
        model_session : ort.InferenceSession
            Pre-loaded ONNX model
        client : ServiceClient
            For sending token_delta messages

        References
        ----------
        |TDD-7.2|
        """
        self.token_queue = queue.Queue(maxsize=50)  # |SAD-10.4|
        pass

    def generate_stream(self, prompt: str, request_id: str) -> Generator[str, None, None]:
        """
        Generate tokens and yield to consumer.

        Parameters
        ----------
        prompt : str
            User input text
        request_id : str
            UUID for correlation (|ICD-8|)

        Yields
        ------
        str
            Individual tokens

        Implementation Notes
        --------------------
        1. Tokenize prompt, prepare ONNX inputs
        2. For each generation step:
           a. Run ONNX inference (single token)
           b. Decode token to string
           c. Construct token_delta message (|ICD-8|)
           d. Send via self.client.send_request()
           e. Yield token to caller
           f. Check if token_queue full (back-pressure)
        3. Send stream_end message after EOS token

        Performance
        -----------
        - First yield MUST occur within 200ms (|NFR-11.3|)
        - Use ort.SessionOptions.graph_optimization_level = 99

        References
        ----------
        |TDD-7.3|, |SAD-10.2|, |FSD-12.2|
        """
        pass

```

----------

### 13.2 Conflict Resolution Matrices

#### Scenario: Contradictory Requirements

**Conflict:**

```
|NFR-4.3|: "LLM Inference: <1s average response time."
|NFR-10.3|: "All model weights <5GB total (for data sovereignty)."

PROBLEM: Quantized models <5GB achieve only ~1.5s inference time on RTX 3080.

```

**Resolution Framework:**


| Option | BRD Impact | NFR Changes | FSD Changes | SAD Changes | Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Relax Latency** | Acceptable if <2s | Update NFR-4.3 → <2s | No change | No change | Low user satisfaction |
| **B: Increase Model Size** | Violates BRD-11 | Update NFR-10.3 → <8GB | No change | No change | Regulatory risk |
| **C: Upgrade Hardware** | Cost increase | Update NFR-1.2 → RTX 4090 | No change | No change | Budget impact |
| **D: Hybrid Approach** | Partial compliance | Add NFR-11.5: "Fast mode" | Add FSD-13: "User selects mode" | Update SAD for conditional loading | Complexity increase |

**Recommended: Option D (Hybrid)**

**Updated Documentation:**

```
|BRD-11.1| (NEW): "Flexible Compliance Modes"
Support both strict compliance (offline, <5GB) and performance mode
(relaxed limits) to serve different market segments.

|NFR-11.5| ← |BRD-11.1|: "Model Size Modes"
  - Compliance Mode: Models ≤5GB, latency ≤2s
  - Performance Mode: Models ≤12GB, latency ≤1s

|FSD-13| ← |NFR-11.5|: "User Mode Selection"
  |FSD-13.1|: UI provides mode toggle in settings (requires restart).
  |FSD-13.2|: Core validates hardware capabilities before mode switch.
  |FSD-13.3|: Compliance mode disables network features (strict isolation).

|SAD-11| ← |FSD-13|: "Conditional Model Loading"
  |SAD-11.1|: Config schema includes 'operating_mode' field.
  |SAD-11.2|: Runtime selects model manifest based on mode.

```

----------

### 13.3 Cross-Process Feature Mapping

#### Feature: "Conversation History with Semantic Search"

This feature spans all processes and tiers. Map it comprehensively:

**BRD (Business Value):**

```
|BRD-13|: "Contextual Memory"
Enable users to reference past conversations without manual note-taking,
increasing productivity and reducing repetitive queries (target: 30% reduction
in duplicate questions).

```

**NFR (Constraints):**

```
|NFR-12| ← |BRD-13|: "Memory Subsystem Constraints"
  |NFR-12.1|: Embedding model: <500MB, CPU-only (for continuous background indexing).
  |NFR-12.2|: Vector search: <50ms for 10k entries (HNSW index).
  |NFR-12.3|: Storage: SQLite database, <1GB for 1 year of conversations.
  |NFR-12.4|: Privacy: No cloud sync, all data local.

```

**FSD (Capabilities):**

```
|FSD-14| ← |NFR-12|: "Conversation Indexing"
  |FSD-14.1|: After each LLM response, generate embedding (384-dim vector).
  |FSD-14.2|: Store in local vector database (conversation_id, timestamp, text, embedding).
  |FSD-14.3|: User can query: "What did I ask about recipes last week?"
  |FSD-14.4|: System returns top-5 semantic matches with timestamps.
  |FSD-14.5|: Clicking match loads full conversation in UI sidebar.

```

**SAD (Architecture):**

```
|SAD-12| ← |FSD-14|: "Memory Architecture"
  |SAD-12.1|: New Service: MemoryService (CPU-bound, separate process).
  |SAD-12.2|: Pattern: Async indexing (POST request, no blocking wait).
  |SAD-12.3|: Pattern: Sync search (GET request, blocks UI until results).
  |SAD-12.4|: Database: SQLite with FTS5 (full-text) + FAISS (vector).
  |SAD-12.5|: Topology:

    Runtime (LLM) → Core → MemoryService (index)
    UI (search) → Core → MemoryService → UI (results)

```

**ICD (Contracts):**

```json
|ICD-9| ← |SAD-12.2|: "Memory Index Request"
{
  "command": "memory_index",
  "request_id": "uuid",
  "payload": {
    "conversation_id": "uuid",
    "timestamp": "ISO-8601",
    "text": "full conversation text",
    "speaker": "user" | "assistant"
  }
}

|ICD-10| ← |SAD-12.3|: "Memory Search Request"
{
  "command": "memory_search",
  "request_id": "uuid",
  "payload": {
    "query": "recipe for pasta",
    "top_k": 5,
    "date_range": {
      "start": "ISO-8601",
      "end": "ISO-8601"
    }
  }
}

|ICD-11| ← |FSD-14.4|: "Memory Search Response"
{
  "status": "success",
  "results": [
    {
      "conversation_id": "uuid",
      "timestamp": "ISO-8601",
      "snippet": "You asked: 'How do I make carbonara?'",
      "similarity_score": 0.89
    }
  ]
}

```

**TDD (Components):**

```
|TDD-8| ← |ICD-9|, |SAD-12|: "Component: MemoryService"
  |TDD-8.1|: Class: MemoryService (inherits ServiceClient pattern)
  |TDD-8.2|: Dependencies: sentence-transformers, faiss-cpu, sqlite3
  |TDD-8.3|: Method: index_conversation(text: str, metadata: dict)
  |TDD-8.4|: Method: search_memory(query: str, top_k: int) -> List[dict]
  |TDD-8.5|: Internal: embedding_model (all-MiniLM-L6-v2, 384-dim)
  |TDD-8.6|: Internal: faiss_index (HNSW, M=16, efConstruction=200)
  |TDD-8.7|: Internal: sqlite_conn (conversations table + FTS5)

|TDD-9| ← |FSD-14.5|: "Component: UI ConversationSidebar"
  |TDD-9.1|: Class: ConversationSidebar (QWidget)
  |TDD-9.2|: Method: display_results(results: List[dict])
  |TDD-9.3|: Method: on_result_click(conversation_id: str) → load_conversation
  |TDD-9.4|: Signal: conversation_selected(uuid) → connects to main chat view

```

**ISP (Stubs):**

```python
|ISP-9| ← |TDD-8|:

import faiss
import sqlite3
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class MemoryService(ServiceClient):
    """
    Conversation indexing and semantic search service.

    Implements
    ----------
    |TDD-8|, |FSD-14|

    Performance
    -----------
    |NFR-12.2|: Search latency <50ms for 10k entries

    Attributes
    ----------
    embedding_model : SentenceTransformer
        all-MiniLM-L6-v2 (384-dim, |TDD-8.5|)
    faiss_index : faiss.IndexHNSWFlat
        Vector index (|TDD-8.6|)
    db_conn : sqlite3.Connection
        Local conversation database (|TDD-8.7|)
    """

    def __init__(self, config_path: str, db_path: str):
        """
        Initialize memory service with embedding model and database.

        Parameters
        ----------
        config_path : str
            Path to ipc_config.yaml
        db_path : str
            Path to conversations.db (SQLite)

        Implementation Notes
        --------------------
        1. Call super().__init__("memory", config_path)
        2. Load embedding model (sentence-transformers)
        3. Initialize FAISS index or load from disk
        4. Connect to SQLite database
        5. Create tables if not exist (conversations, embeddings)

        References
        ----------
        |TDD-8.2|, |SAD-12.4|
        """
        super().__init__("memory", config_path)
        pass

    def index_conversation(self, text: str, metadata: dict) -> None:
        """
        Generate embedding and store in vector database.

        Parameters
        ----------
        text : str
            Full conversation text
        metadata : dict
            Contains conversation_id, timestamp, speaker (|ICD-9|)

        Implementation Notes
        --------------------
        1. Generate embedding: self.embedding_model.encode(text)
        2. Add to FAISS index: self.faiss_index.add(embedding)
        3. Insert into SQLite: (conversation_id, text, timestamp)
        4. Commit transaction
        5. Send log confirmation (non-blocking)

        Performance
        -----------
        - CPU-only embedding generation (|NFR-12.1|)
        - Async execution (no blocking Core) (|SAD-12.2|)

        References
        ----------
        |TDD-8.3|, |FSD-14.1|
        """
        pass

    def search_memory(self, query: str, top_k: int = 5) -> List[dict]:
        """
        Semantic search across conversation history.

        Parameters
        ----------
        query : str
            User search query
        top_k : int
            Number of results to return

        Returns
        -------
        List[dict]
            Results matching |ICD-11| schema

        Implementation Notes
        --------------------
        1. Generate query embedding
        2. FAISS search: distances, indices = index.search(embedding, top_k)
        3. Retrieve metadata from SQLite using indices
        4. Construct response per |ICD-11|
        5. Return results (sorted by similarity_score DESC)

        Performance
        -----------
        - Must complete <50ms for 10k entries (|NFR-12.2|)
        - Use HNSW parameters: M=16, efSearch=64

        References
        ----------
        |TDD-8.4|, |FSD-14.4|
        """
        pass

```

----------

## 14. Advanced Traceability Techniques

### 14.1 Impact Analysis Queries

When modifying a tag, determine downstream effects:

**Query Template:**

```
SELECT child_tag, child_content, tier
FROM documentation
WHERE parent_citations LIKE '%|TARGET_TAG|%'
ORDER BY tier_depth DESC;

```

**Example: Changing |NFR-4.3|**

```
INPUT: |NFR-4.3|: "LLM Inference: <1s" → CHANGING TO <2s

IMPACT ANALYSIS:
┌──────────┬────────────────────────────────────┬──────┐
│ Child    │ Content Summary                    │ Tier │
├──────────┼────────────────────────────────────┼──────┤
│ FSD-12.3 │ TTS begins after first sentence    │ FSD  │ ← May need timing adjustment
│ SAD-10.4 │ Back-pressure queue size           │ SAD  │ ← OK (architecture unchanged)
│ ICD-8    │ Streaming token schema             │ ICD  │ ← OK (schema unchanged)
│ TDD-7.3  │ generate_stream() method           │ TDD  │ ← OK (implementation detail)
│ ISP-8    │ Performance note in docstring      │ ISP  │ ← UPDATE REQUIRED
└──────────┴────────────────────────────────────┴──────┘

ACTION ITEMS:
1. Update |ISP-8| docstring: "First token within 200ms" (still achievable)
2. Review |FSD-12.3|: Verify 2s budget still allows sentence-level TTS start
3. Mark reconciliation_manifest as DIRTY with pending review

```

### 14.2 Traceability Graphs

Visualize tag relationships for complex features:

```mermaid
graph TD
    BRD13["|BRD-13|<br/>Contextual Memory"]
    NFR12["|NFR-12|<br/>Memory Constraints"]
    FSD14["|FSD-14|<br/>Indexing Behavior"]
    SAD12["|SAD-12|<br/>Memory Architecture"]
    ICD9["|ICD-9|<br/>Index Schema"]
    ICD10["|ICD-10|<br/>Search Schema"]
    TDD8["|TDD-8|<br/>MemoryService"]
    ISP9["|ISP-9|<br/>Service Stub"]

    BRD13 --> NFR12
    NFR12 --> FSD14
    FSD14 --> SAD12
    SAD12 --> ICD9
    SAD12 --> ICD10
    ICD9 --> TDD8
    ICD10 --> TDD8
    TDD8 --> ISP9

    style BRD13 fill:#e1f5ff
    style NFR12 fill:#fff3e0
    style FSD14 fill:#f3e5f5
    style SAD12 fill:#e8f5e9
    style ICD9 fill:#fce4ec
    style ICD10 fill:#fce4ec
    style TDD8 fill:#fff9c4
    style ISP9 fill:#f1f8e9

```

### 14.3 Orphan Detection Algorithms

**Upward Orphan (Missing Parent):**

```python
def detect_upward_orphans(documentation: dict) -> List[str]:
    """
    Find tags that cite non-existent parents.

    Returns
    -------
    List[str]
        Tag IDs with broken citations
    """
    all_tags = set(documentation.keys())
    orphans = []

    for tag_id, content in documentation.items():
        citations = extract_citations(content)  # Parse ← |PARENT| syntax
        for parent in citations:
            if parent not in all_tags:
                orphans.append(f"{tag_id} ← |{parent}| (MISSING)")

    return orphans

```

**Downward Orphan (No Children):**

```python
def detect_downward_orphans(documentation: dict, tier: str) -> List[str]:
    """
    Find tier-N tags that have no tier-(N+1) children.
    Indicates incomplete specification.

    Parameters
    ----------
    tier : str
        Current tier (e.g., "FSD")

    Returns
    -------
    List[str]
        Tags requiring downstream specification
    """
    child_tier_map = {"BRD": "NFR", "NFR": "FSD", "FSD": "SAD",
                      "SAD": "ICD", "ICD": "TDD", "TDD": "ISP"}

    if tier not in child_tier_map:
        return []  # ISP has no children

    child_tier = child_tier_map[tier]
    tier_tags = [t for t in documentation if t.startswith(tier)]
    child_citations = set()

    for child_tag, content in documentation.items():
        if child_tag.startswith(child_tier):
            citations = extract_citations(content)
            child_citations.update(citations)

    orphans = [t for t in tier_tags if t not in child_citations]
    return orphans

```

**Example Output:**

```
UPWARD ORPHANS (Broken Citations):
- |FSD-14.2| ← |NFR-999| (MISSING) → CREATE NFR-999 or FIX CITATION

DOWNWARD ORPHANS (Incomplete Specs):
- |SAD-7| (no ICD children) → CREATE ICD schema for sentiment data
- |FSD-11.3| (no SAD children) → SPECIFY architecture for model validation

```

----------

## 15. Documentation Evolution Strategies

### 15.1 Version Control Integration

**Tag Stability Across Versions:**

```
VERSION 1.0:
|FSD-4.1|: "Wake Word: Always-on detection using pvporcupine."

VERSION 2.0:
|FSD-4.1|: "Wake Word: Always-on detection using pvporcupine."
|FSD-4.6| (NEW): "Multi-Wake-Word: Support custom wake phrases via training API."

```

**Rules:**

1.  **Never Delete Tags:** Mark as DEPRECATED instead
2.  **Never Renumber:** Add new sequential IDs (e.g., .6, .7)
3.  **Maintain Citations:** Old tags remain valid parents

**Deprecation Pattern:**

```
|NFR-3.3| [DEPRECATED v2.0 → See |NFR-13.1|]: "Memory (Core Queue): 1000 cap."
|NFR-13.1| ← |NFR-3.3|: "Memory (Core Queue): Dynamic sizing, 500-5000 cap."

```

### 15.2 Feature Flag Documentation

For gradual rollouts, extend tags with feature flag markers:

```
|FSD-15| [FEATURE_FLAG: streaming_tts]: "Streaming TTS Synthesis"
  |FSD-15.1|: UI plays audio chunks as generated (no full buffer wait).
  |FSD-15.2|: Runtime yields TTS frames incrementally.

|SAD-13| ← |FSD-15| [FEATURE_FLAG: streaming_tts]: "Streaming TTS Pattern"
  |SAD-13.1|: Pattern: Generator-based synthesis with chunk yields.
  |SAD-13.2|: Protocol: WebSocket for real-time audio frames.

```

**Configuration Hook:**

```yaml
|ICD-12| ← |SAD-13|:
features:
  streaming_tts:
    enabled: false  # Toggle without code changes
    chunk_size_ms: 200

```

### 15.3 Migration Paths

When refactoring requires tag restructuring:

**Before (V1):**

```
|FSD-4|: "Audio Acquisition"
  |FSD-4.1|: Wake Word
  |FSD-4.2|: VAD Stage 1
  |FSD-4.3|: VAD Stage 2

```

**After (V2 - Reorganized):**

```
|FSD-4| [RESTRUCTURED v2.0]: "Audio Acquisition"
  → See |FSD-4-V2| for current specification

|FSD-4-V2|: "Audio Processing Pipeline"
  |FSD-4-V2.1|: "Wake Word Detection" ← |FSD-4.1| (legacy)
  |FSD-4-V2.2|: "Voice Activity Detection"
    |FSD-4-V2.2.1|: Stage 1 (webrtcvad) ← |FSD-4.2| (legacy)
    |FSD-4-V2.2.2|: Stage 2 (Silero) ← |FSD-4.3| (legacy)
  |FSD-4-V2.3|: "Noise Reduction" (NEW)

```

**Migration Manifest:**

```yaml
migrations:
  - version: "2.0"
    date: "2026-03-15"
    changes:
      - type: "restructure"
        old_root: "|FSD-4|"
        new_root: "|FSD-4-V2|"
        mapping:
          "|FSD-4.1|": "|FSD-4-V2.1|"
          "|FSD-4.2|": "|FSD-4-V2.2.1|"
          "|FSD-4.3|": "|FSD-4-V2.2.2|"

```

----------

## 16. LLM-Assisted Workflows

### 16.1 Automated Tag Generation

**Prompt Template for New Feature:**

~~~
CONTEXT:
You are generating DDR documentation for a new feature.

INPUT:
Feature Name: "Voice Emotion Modulation"
Description: Adjust TTS emotional tone base on conversation context (calm, energetic, empathetic).

TASK: Generate tags for ALL tiers (BRD through ISP) following these rules:

1.  BRD: Business value, market differentiation
2.  NFR: Performance constraints, model size limits
3.  FSD: Functional behavior, user-observable effects
4.  SAD: Architecture pattern (where does emotion analysis run?)
5.  ICD: Data schema for emotion metadata
6.  TDD: Component structure (class names, methods)
7.  ISP: Python stub with docstrings

OUTPUT FORMAT:

```yaml
tags:
  BRD-14:
    content: |
      Emotional Intelligence Enhancement
      Enable empathetic, context-aware responses to improve user satisfaction...
    citations: []
  NFR-14:
    content: |
      Emotion Analysis Constraints
      |NFR-14.1|: Emotion classifier: <200MB, CPU-only
      |NFR-14.2|: Analysis latency: <100ms per response
    citations: ["|BRD-14|"]
  # ... (continue for all tiers)

	```

~~~

### 16.2 Citation Validation Prompts

**Automated Integrity Check:**

```

TASK: Validate traceability for |FSD-14| subtree

RULES:

1.  Every FSD-14.X must cite parent (NFR, BRD)
2.  Every cited parent must exist
3.  No sibling citations (FSD-14.1 ← FSD-14.2)
4.  At least one SAD child must exist for each FSD-14.X

CHECK: |FSD-14|: [citations found: |NFR-12|, |BRD-13|] ✓ VALID |FSD-14.1|: [citations: |NFR-12.1|] ✓ VALID |FSD-14.2|: [citations: |NFR-12.1|] ✓ VALID |FSD-14.3|: [citations: NONE] ✗ MISSING PARENT |FSD-14.4|: [citations: |FSD-14.3|] ✗ SIBLING CITATION

ACTION REQUIRED:

-   Add parent citation to |FSD-14.3| (suggest: |NFR-12|)
-   Replace |FSD-14.4| ← |FSD-14.3| with upstream citation

```

### 16.3 Reconciliation Automation

**Dirty Flag Resolution Workflow:**
```python
def auto_reconcile(modified_tag: str, new_content: str) -> dict:
    """
    Automated reconciliation after tag modification.

    Returns
    -------
    dict
        Reconciliation plan with suggested updates
    """
    plan = {
        "modified": modified_tag,
        "downstream_impacts": [],
        "suggested_updates": [],
        "manual_review_required": []
    }

    # Find all children citing this tag
    children = find_children(modified_tag)

    for child in children:
        # Analyze semantic changes
        old_constraints = extract_constraints(get_original(modified_tag))
        new_constraints = extract_constraints(new_content)

        added = new_constraints - old_constraints
        removed = old_constraints - new_constraints

        if removed:
            # Constraint relaxed - child may need update
            plan["downstream_impacts"].append({
                "tag": child,
                "issue": "Parent constraint relaxed",
                "detail": f"Removed: {removed}",
                "action": "REVIEW: Can child simplify implementation?"
            })

        if added:
            # New constraint - child may violate
            child_content = get_content(child)
            if conflicts_with(child_content, added):
                plan["manual_review_required"].append({
                    "tag": child,
                    "issue": "CONSTRAINT_VIOLATION",
                    "detail": f"Child violates new constraint: {added}"
                })
            else:
                plan["suggested_updates"].append({
                    "tag": child,
                    "action": "ADD_CITATION",
                    "detail": f"Acknowledge new constraint: {added}"
                })

    return plan

```

----------

## 17. Real-World Application: Complete Feature Lifecycle

### 17.1 Feature Request: "Multi-User Support"

**Initial Stakeholder Request:**

> "We need to support multiple user profiles so families can share one MAGGIE instance with personalized preferences and conversation history."

**Step 1: BRD Analysis (Strategist Persona)**

```
QUESTION: What is the business value?
ANSWER: Expands addressable market from individuals to households (3-5x users per installation).

QUESTION: What is the strategic objective?
ANSWER: Increase user engagement through personalization without sacrificing privacy.

GENERATED TAG:
|BRD-15|: "Multi-User Personalization"
Enable household-shared deployment with per-user preferences, conversation history,
and voice profiles. Target: 60% of installs used by 2+ users within 3 months.

SUCCESS METRICS:
- Average users per installation: ≥2.3
- User switching frequency: ≥5 switches/week
- Preference satisfaction: ≥85% (user survey)

```

**Step 2: NFR Analysis (SysAdmin Persona)**

```
QUESTION: What are the hard limits?
ANSWERS:
- Storage: Each user profile ~500MB (embeddings, history, preferences)
- Performance: User switching must complete <2s
- Security: Profiles must be encrypted separately (AES-256)
- Scalability: Support 1-10 users per installation

GENERATED TAGS:
|NFR-15| ← |BRD-15|: "Multi-User Constraints"
  |NFR-15.1|: Storage per user: ≤500MB (10 users = 5GB total).
  |NFR-15.2|: User switch latency: ≤2s (model reload, history load).
  |NFR-15.3|: Profile encryption: AES-256, separate keys per user.
  |NFR-15.4|: Concurrent users: Max 1 active (hardware limit).
  |NFR-15.5|: Voice biometrics: ≥95% identification accuracy (Resemblyzer).

```

**Step 3: FSD Analysis (Product Manager Persona)**

```
QUESTION: What does the user experience?
ANSWERS:
- Login screen on app start
- Voice-based authentication ("Hey Maggie, it's Alice")
- Visual indicator of current user
- User-specific conversation history sidebar
- Per-user TTS voice settings

GENERATED TAGS:
|FSD-16| ← |NFR-15|: "Multi-User Experience"
  |FSD-16.1|: UI displays user selection screen on startup.
  |FSD-16.2|: Voice login: User says "Hey Maggie, it's [name]" → auto-switch.
  |FSD-16.3|: Visual: Avatar + name displayed in top-right corner.
  |FSD-16.4|: Conversation history filtered by active user_id.
  |FSD-16.5|: TTS voice preferences loaded from user profile.
  |FSD-16.6|: Manual switch: Settings → Users → Select → Confirm.

```

**Step 4: SAD Analysis (Architect Persona)**

```
QUESTION: How do we structure this?
ANSWERS:
- New database table: users (id, name, voice_embedding, preferences_json)
- User profiles stored in ./users/{user_id}/ directory
- Voice biometrics run in Audio Process (CPU-only Resemblyzer)
- Current user_id propagated in all IPC messages (metadata)

GENERATED TAGS:
|SAD-14| ← |FSD-16|: "Multi-User Architecture"
  |SAD-14.1|: Data Model: SQLite users table + per-user directories.
  |SAD-14.2|: Pattern: Active user_id in session context (Core maintains).
  |SAD-14.3|: Voice ID: Audio Process runs Resemblyzer on wake word.
  |SAD-14.4|: User Switch Flow:
    1. Audio detects voice → sends embedding to Core
    2. Core queries MemoryService for user_id match
    3. Core loads user profile, updates session context
    4. Core broadcasts USER_CHANGED event to all services
  |SAD-14.5|: Security: User-specific encryption keys derived from master key + user_id.

```

**Step 5: ICD Analysis (Data Engineer Persona)**

```
QUESTION: What are the data contracts?
ANSWER: Define schemas for user profiles, voice embeddings, switch events.

GENERATED TAGS:
|ICD-13| ← |SAD-14.1|: "User Profile Schema (SQLite)"
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    voice_embedding BLOB,  -- 256-dim Resemblyzer vector
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preferences TEXT  -- JSON: {tts_voice, theme, language}
);

|ICD-14| ← |SAD-14.3|: "Voice ID Request"
{
  "command": "identify_user",
  "request_id": "uuid",
  "payload": {
    "audio_embedding": [0.123, -0.456, ...],  // 256-dim array
    "confidence_threshold": 0.85
  }
}

|ICD-15| ← |SAD-14.4|: "User Switch Event (Broadcast)"
{
  "command": "USER_CHANGED",
  "priority": 0,  // High priority
  "payload": {
    "user_id": "alice_profile_001",
    "display_name": "Alice",
    "preferences": {...}
  }
}

```

**Step 6: TDD Analysis (Lead Developer Persona)**

```
QUESTION: What components implement this?
ANSWER: New UserManager in Core, UI components, Audio voice ID.

GENERATED TAGS:
|TDD-10| ← |ICD-13|, |SAD-14|: "Component: UserManager"
  |TDD-10.1|: Class: UserManager (runs in Core Process)
  |TDD-10.2|: Dependencies: sqlite3, cryptography
  |TDD-10.3|: Method: load_user(user_id: str) -> UserProfile
  |TDD-10.4|: Method: identify_from_voice(embedding: np.ndarray) -> str
  |TDD-10.5|: Method: switch_user(new_user_id: str) -> None
  |TDD-10.6|: Internal: active_user: UserProfile (session state)
  |TDD-10.7|: Internal: user_db: sqlite3.Connection

|TDD-11| ← |ICD-14|: "Component: Audio VoiceIdentifier"
  |TDD-11.1|: Class: VoiceIdentifier (in Audio Process)
  |TDD-11.2|: Dependencies: resemblyzer
  |TDD-11.3|: Method: extract_embedding(audio: np.ndarray) -> np.ndarray
  |TDD-11.4|: Internal: resemblyzer_model (CPU-based)

```

**Step 7: ISP Analysis (Code Generator Persona)**

```python
|ISP-10| ← |TDD-10|:

import sqlite3
import json
import numpy as np
from dataclasses import dataclass
from cryptography.fernet import Fernet

@dataclass
class UserProfile:
    """
    User profile data structure.

    Attributes
    ----------
    user_id : str
        Unique identifier (|ICD-13|)
    display_name : str
        User-facing name
    preferences : dict
        TTS voice, theme, language settings
    voice_embedding : np.ndarray
        256-dim Resemblyzer vector (|ICD-14|)
    """
    user_id: str
    display_name: str
    preferences: dict
    voice_embedding: np.ndarray

class UserManager:
    """
    Manages user profiles, authentication, and session state.

    Implements
    ----------
    |TDD-10|, |FSD-16|

    Security
    --------
    |NFR-15.3|: Per-user AES-256 encryption

    Attributes
    ----------
    active_user : UserProfile
        Currently logged-in user (|TDD-10.6|)
    user_db : sqlite3.Connection
        SQLite database (|ICD-13|)
    """

    def __init__(self, db_path: str, master_key: bytes):
        """
        Initialize user manager with database connection.

        Parameters
        ----------
        db_path : str
            Path to users.db
        master_key : bytes
            Master encryption key (32 bytes)

        Implementation Notes
        --------------------
        1. Connect to SQLite database
        2. Create users table if not exists (|ICD-13|)
        3. Initialize active_user = None (no user logged in)
        4. Store master_key for deriving per-user keys

        References
        ----------
        |TDD-10.2|, |SAD-14.1|
        """
        pass

    def load_user(self, user_id: str) -> UserProfile:
        """
        Load user profile from database.

        Parameters
        ----------
        user_id : str
            User identifier

        Returns
        -------
        UserProfile
            Decrypted user profile object

        Raises
        ------
        ValueError
            If user_id not found in database

        Implementation Notes
        --------------------
        1. Query users table: SELECT * WHERE user_id = ?
        2. Decrypt preferences JSON using per-user key
        3. Deserialize voice_embedding BLOB to numpy array
        4. Construct UserProfile dataclass
        5. Return profile

        Performance
        -----------
        Must complete within 2s budget (|NFR-15.2|)

        References
        ----------
        |TDD-10.3|, |ICD-13|
        """
        pass

    def identify_from_voice(self, embedding: np.ndarray,
                            threshold: float = 0.85) -> str:
        """
        Identify user from voice embedding using cosine similarity.

        Parameters
        ----------
        embedding : np.ndarray
            256-dim Resemblyzer embedding from Audio Service
        threshold : float
            Minimum similarity score for positive ID (|NFR-15.5|)

        Returns
        -------
        str
            user_id of best match, or "unknown" if below threshold

        Implementation Notes
        --------------------
        1. Query all users: SELECT user_id, voice_embedding
        2. For each user:
           a. Compute cosine_similarity(embedding, user_embedding)
           b. Track best_match (user_id, score)
        3. If best_score >= threshold: return user_id
        4. Else: return "unknown"

        Performance
        -----------
        - Linear scan acceptable for ≤10 users (|NFR-15.4|)
        - Vectorize with numpy for speed

        References
        ----------
        |TDD-10.4|, |ICD-14|, |SAD-14.4|
        """
        pass

    def switch_user(self, new_user_id: str) -> None:
        """
        Switch active user and broadcast change event.

        Parameters
        ----------
        new_user_id : str
            Target user identifier

        Implementation Notes
        --------------------
        1. Load new user profile: profile = self.load_user(new_user_id)
        2. Update session: self.active_user = profile
        3. Construct USER_CHANGED event (|ICD-15|)
        4. Broadcast to all services via Core's routing
        5. Log user switch with request_id

        Side Effects
        ------------
        - All services receive USER_CHANGED and reload user-specific data
        - UI updates avatar and name display
        - Memory Service switches to user's conversation history

        References
        ----------
        |TDD-10.5|, |FSD-16.6|, |SAD-14.4|
        """
        pass

```

----------

## 18. Final Recommendations & Best Practices

### 18.1 Documentation Maintenance Schedule


| Activity | Frequency | Responsible Persona |
|----------|-----------|---------------------|
| **Tag Inventory Audit** | Weekly | Any developer |
| **Broken Citation Check** | On every commit | Automated CI/CD |
| **Orphan Detection** | Sprint planning | Tech Lead |
| **Reconciliation Sweep** | After major refactor | Architect |
| **Version Migration** | Release milestones | Product Owner |
| **LLM Context Test** | Monthly | DevOps |

### 18.2 Tag Naming Conventions

**DO:**

-   Use semantic numbering: `|FSD-14|` for "Multi-User", `|FSD-15|` for "Streaming"
-   Group related features in consecutive blocks
-   Add descriptive comments: `|NFR-15| ← |BRD-15|: "Multi-User Constraints"`

**DON'T:**

-   Use arbitrary jumps: `|FSD-5|` then `|FSD-100|`
-   Reuse deleted tag IDs
-   Create non-sequential sub-tags: `|FSD-10.1|`, `|FSD-10.5|` (missing .2-.4)

### 18.3 Citation Patterns

**Preferred (Specific):**

```
|TDD-8.3| ← |ICD-9|, |FSD-14.1|: Method traces to exact data schema and feature spec

```

**Acceptable (Block-Level):**

```
|SAD-12| ← |FSD-14|: Architecture implements entire feature set

```

**Avoid (Ambiguous):**

```
|ISP-9| ← |TDD-8|, |ICD-9|, |FSD-14|, |NFR-12|: Too many parents obscures primary relationship

```

### 18.4 When to Create New Tiers

The seven-tier structure is **fixed**. Never add custom intermediate tiers like "PRD" or "HLD". Instead:

**If you need more granularity:**

-   Use sub-atomic tags: `|FSD-14.2.1|`, `|FSD-14.2.2|`
-   Add sections within tiers: "Core Capabilities", "Extended Features"
-   Create appendices: "Performance Tuning Guide" (references tags, not new tier)

**If information doesn't fit:**

-   Re-evaluate classification using decision tree (Section 4.1)
-   Check for hybrid content requiring decomposition (Section 13.1)
-   Consult persona-question map (Section 11.3)

----------

## 19. Conclusion

The MAGGIE DDR establishes a **rigorous, LLM-optimized framework** for managing software design documentation across seven distinct abstraction tiers. This report has provided:

1.  **Precise Boundary Definitions:** Each tier has clear inclusion/exclusion criteria (Section 2)
2.  **Classification Rubrics:** Decision trees and scoring matrices for ambiguous information (Section 4)
3.  **Real-World Examples:** Industry-grade demonstrations of correct vs. incorrect classification (Sections 2-3, 6, 13, 17)
4.  **Abstraction/Specification Protocols:** Systematic methods for generating parent/child tags (Section 5)
5.  **Integrity Mechanisms:** Reconciliation manifests, dirty flags, and automated validation (Sections 7, 14, 16)
6.  **Practical Workflows:** Complete feature lifecycle from business need to code stub (Section 17)

**Key Principles to Remember:**

-   **Unidirectional Flow:** Information cascades downward (BRD → ISP), citations flow upward
-   **Immutable IDs:** Tags are permanent database keys
-   **Persona-Driven:** Each tier assumes a distinct stakeholder viewpoint
-   **LLM-Parseable:** Strict formatting enables automated tooling

**Application Guidance:**

-   Start classification with decision tree (Section 4.1)
-   Validate with scoring matrix (Section 4.2) for ambiguous cases
-   Use worked examples (Sections 13, 17) as templates
-   Apply anti-pattern checklist (Section 9) before committing
-   Run integrity checks (Section 14.3) in CI/CD pipeline

This framework transforms documentation from a static artifact into a **living, traceable knowledge graph** that scales with project complexity while maintaining precision for both human developers and AI assistants.

## 20. Advanced Integration Patterns

### 20.1 External System Integration Documentation

When MAGGIE integrates with external systems (APIs, databases, hardware), document the boundary contracts across all tiers.

#### Example: Home Automation Integration

**Business Requirement (BRD):**

```
|BRD-16|: "Smart Home Control"
Enable voice control of home automation devices (lights, thermostats, locks)
to position MAGGIE as a central home hub. Target: 40% of users connect ≥3 devices
within first month.

MARKET DIFFERENTIATION:
- Offline operation (no cloud dependency for local devices)
- Privacy-preserving (device state never leaves network)
- Vendor-agnostic (Zigbee, Z-Wave, Matter protocols)

```

**Constraints (NFR):**

```
|NFR-16| ← |BRD-16|: "Home Automation Constraints"
  |NFR-16.1|: Protocol support: Zigbee 3.0, Z-Wave 700 series, Matter 1.0.
  |NFR-16.2|: Device discovery: <5s for 50 devices on local network.
  |NFR-16.3|: Command latency: <500ms from voice to device action.
  |NFR-16.4|: No internet dependency for local device control.
  |NFR-16.5|: Hardware: USB Zigbee/Z-Wave dongle required.
  |NFR-16.6|: Concurrent device commands: Support up to 10 simultaneous operations.

```

**Feature Specification (FSD):**

```
|FSD-17| ← |NFR-16|: "Device Control Workflow"
  |FSD-17.1|: User: "Turn on kitchen lights" → LLM extracts intent → Device command.
  |FSD-17.2|: LLM identifies: {action: "turn_on", device: "kitchen_lights"}.
  |FSD-17.3|: Core queries DeviceService for device ID matching "kitchen_lights".
  |FSD-17.4|: DeviceService sends Zigbee command to physical device.
  |FSD-17.5|: Device confirms state change → UI displays "Kitchen lights: ON".
  |FSD-17.6|: Error handling: "Device unreachable" spoken via TTS if timeout.
  |FSD-17.7|: Device discovery: On startup, scan network for compatible devices.
  |FSD-17.8|: User can rename devices via UI: "Living Room Lamp 1" → "Reading Light".

```

**Architecture (SAD):**

```
|SAD-15| ← |FSD-17|: "Home Automation Architecture"
  |SAD-15.1|: New Service: DeviceService (separate process, USB hardware access).
  |SAD-15.2|: Pattern: Command-Query Separation
    - Commands: Async fire-and-forget (turn_on, set_temperature)
    - Queries: Sync request-response (get_state, list_devices)
  |SAD-15.3|: Device Registry: SQLite table mapping friendly_name → device_id → protocol.
  |SAD-15.4|: Protocol Abstraction: Plugin architecture for Zigbee/Z-Wave/Matter.
  |SAD-15.5|: Topology:

    UI/Voice → Core → LLM (intent extraction)
                ↓
           Core → DeviceService → USB Dongle → Physical Device
                ↓
           Core → UI (state update)

  |SAD-15.6|: Fault Tolerance: DeviceService crash does not affect Core/LLM.

```

**Data Contracts (ICD):**

```json
|ICD-16| ← |SAD-15.3|: "Device Registry Schema (SQLite)"
CREATE TABLE devices (
    device_id TEXT PRIMARY KEY,
    friendly_name TEXT NOT NULL,
    device_type TEXT,  -- 'light', 'thermostat', 'lock', etc.
    protocol TEXT,     -- 'zigbee', 'zwave', 'matter'
    protocol_address TEXT,  -- Device-specific ID (Zigbee EUI64, etc.)
    capabilities TEXT, -- JSON: {brightness: true, color: false, ...}
    room TEXT,         -- 'kitchen', 'bedroom', etc.
    last_seen TIMESTAMP
);

|ICD-17| ← |FSD-17.2|: "Device Command Schema"
{
  "command": "device_control",
  "request_id": "uuid",
  "payload": {
    "device_id": "zigbee_bulb_001",
    "action": "turn_on" | "turn_off" | "set_brightness" | "set_color",
    "parameters": {
      "brightness": 75,  // 0-100, optional
      "color": {"r": 255, "g": 200, "b": 150}  // RGB, optional
    }
  }
}

|ICD-18| ← |FSD-17.5|: "Device State Update (Broadcast)"
{
  "command": "DEVICE_STATE_CHANGED",
  "priority": 1,
  "payload": {
    "device_id": "zigbee_bulb_001",
    "friendly_name": "Kitchen Lights",
    "state": {
      "power": "on",
      "brightness": 75,
      "reachable": true
    },
    "timestamp": "ISO-8601"
  }
}

```

**Component Design (TDD):**

```
|TDD-12| ← |ICD-16|, |SAD-15|: "Component: DeviceService"
  |TDD-12.1|: Class: DeviceService (inherits ServiceClient)
  |TDD-12.2|: Dependencies: zigpy (Zigbee), python-openzwave (Z-Wave), pyserial
  |TDD-12.3|: Method: discover_devices() -> List[Device]
  |TDD-12.4|: Method: send_command(device_id: str, action: str, params: dict) -> bool
  |TDD-12.5|: Method: get_device_state(device_id: str) -> dict
  |TDD-12.6|: Internal: device_registry (SQLite connection)
  |TDD-12.7|: Internal: protocol_handlers (dict mapping 'zigbee' → ZigbeeHandler)
  |TDD-12.8|: Thread: device_monitor (polls devices every 30s for state changes)

|TDD-13| ← |SAD-15.4|: "Component: ProtocolHandler (Abstract)"
  |TDD-13.1|: Class: ProtocolHandler (ABC)
  |TDD-13.2|: Method: discover() -> List[Device]
  |TDD-13.3|: Method: send_command(address: str, action: str, params: dict)
  |TDD-13.4|: Method: get_state(address: str) -> dict
  |TDD-13.5|: Subclasses: ZigbeeHandler, ZWaveHandler, MatterHandler

```

**Implementation Stubs (ISP):**

```python
|ISP-11| ← |TDD-12|:

import sqlite3
from typing import List, Dict
from abc import ABC, abstractmethod

class Device:
    """
    Device data model matching |ICD-16| schema.

    Attributes
    ----------
    device_id : str
        Unique identifier
    friendly_name : str
        User-assigned name
    protocol : str
        'zigbee', 'zwave', 'matter'
    capabilities : dict
        Supported actions/parameters
    """
    def __init__(self, device_id: str, friendly_name: str,
                 protocol: str, capabilities: dict):
        self.device_id = device_id
        self.friendly_name = friendly_name
        self.protocol = protocol
        self.capabilities = capabilities

class ProtocolHandler(ABC):
    """
    Abstract base for protocol-specific device communication.

    Implements
    ----------
    |TDD-13|, |SAD-15.4|

    Subclasses
    ----------
    ZigbeeHandler, ZWaveHandler, MatterHandler
    """

    @abstractmethod
    def discover(self) -> List[Device]:
        """
        Scan network for devices using this protocol.

        Returns
        -------
        List[Device]
            Discovered devices with populated metadata

        Performance
        -----------
        Must complete within 5s (|NFR-16.2|)

        References
        ----------
        |TDD-13.2|, |FSD-17.7|
        """
        pass

    @abstractmethod
    def send_command(self, address: str, action: str, params: dict) -> bool:
        """
        Send control command to physical device.

        Parameters
        ----------
        address : str
            Protocol-specific device address (e.g., Zigbee EUI64)
        action : str
            Command type from |ICD-17|
        params : dict
            Action parameters (brightness, color, etc.)

        Returns
        -------
        bool
            True if device acknowledged command

        Performance
        -----------
        Must complete within 500ms (|NFR-16.3|)

        References
        ----------
        |TDD-13.3|, |FSD-17.4|
        """
        pass

class DeviceService(ServiceClient):
    """
    Home automation device management service.

    Implements
    ----------
    |TDD-12|, |FSD-17|

    Constraints
    -----------
    |NFR-16.5|: Requires USB Zigbee/Z-Wave dongle

    Attributes
    ----------
    device_registry : sqlite3.Connection
        Local device database (|ICD-16|)
    protocol_handlers : Dict[str, ProtocolHandler]
        Protocol-specific communication handlers
    """

    def __init__(self, config_path: str, db_path: str, usb_port: str):
        """
        Initialize device service with hardware connection.

        Parameters
        ----------
        config_path : str
            Path to ipc_config.yaml
        db_path : str
            Path to devices.db
        usb_port : str
            Serial port for USB dongle (e.g., '/dev/ttyUSB0')

        Implementation Notes
        --------------------
        1. Call super().__init__("device", config_path)
        2. Connect to device registry database
        3. Initialize protocol handlers:
           - ZigbeeHandler(usb_port) if dongle supports Zigbee
           - ZWaveHandler(usb_port) if dongle supports Z-Wave
        4. Start device_monitor thread (|TDD-12.8|)

        References
        ----------
        |TDD-12.2|, |NFR-16.5|
        """
        super().__init__("device", config_path)
        pass

    def discover_devices(self) -> List[Device]:
        """
        Scan network for all compatible devices.

        Returns
        -------
        List[Device]
            All discovered devices across all protocols

        Implementation Notes
        --------------------
        1. For each protocol_handler in self.protocol_handlers.values():
           a. devices = handler.discover()
           b. For each device:
              - Check if already in registry (by protocol_address)
              - If new: INSERT INTO devices
              - If exists: UPDATE last_seen
           c. Aggregate all devices
        2. Return combined list

        Performance
        -----------
        Parallelizable: Run protocol.discover() in separate threads
        Total time <5s for 50 devices (|NFR-16.2|)

        References
        ----------
        |TDD-12.3|, |FSD-17.7|
        """
        pass

    def send_command(self, device_id: str, action: str, params: dict) -> bool:
        """
        Execute device control command.

        Parameters
        ----------
        device_id : str
            Device identifier from registry
        action : str
            Command type (|ICD-17|)
        params : dict
            Action parameters

        Returns
        -------
        bool
            True if command succeeded

        Implementation Notes
        --------------------
        1. Query registry: SELECT protocol, protocol_address WHERE device_id = ?
        2. Get handler: handler = self.protocol_handlers[protocol]
        3. Execute: success = handler.send_command(address, action, params)
        4. If success:
           a. Broadcast DEVICE_STATE_CHANGED (|ICD-18|)
           b. Log command execution
        5. Return success status

        Error Handling
        --------------
        - Device unreachable: Broadcast error, return False
        - Invalid action: Log warning, return False

        References
        ----------
        |TDD-12.4|, |FSD-17.4|, |FSD-17.6|
        """
        pass

```

----------

### 20.2 Plugin Architecture Documentation

For extensible systems like MAGGIE's Tool/Routine framework, document the plugin contract.

**Plugin Lifecycle Specification:**

```
|FSD-18| ← |BRD-5.3|: "Extension Lifecycle Management"
  |FSD-18.1|: Discovery: Core scans ./extensions/ on startup.
  |FSD-18.2|: Validation: Each extension must have valid manifest.yaml.
  |FSD-18.3|: Loading: Core imports entry_point module via importlib.
  |FSD-18.4|: Initialization: Core calls extension.initialize(core_context).
  |FSD-18.5|: HSM Integration: Core merges extension.get_hsm_states() into main HSM.
  |FSD-18.6|: Error Isolation: Extension crash does not halt Core (logged as ERROR).
  |FSD-18.7|: Unloading: Extensions can be disabled via config (hot-reload not supported in MVP).

```

**Plugin Contract (ICD):**

```yaml
|ICD-19| ← |FSD-18.2|: "Extension Manifest Schema"
# File: ./extensions/my_tool/manifest.yaml
name: "my_tool"              # Unique identifier (required)
version: "1.0.0"             # Semantic version (required)
type: "tool" | "routine"     # Extension type (required)
entry_point: "src.plugin"    # Python module path (required)
dependencies:                # Optional: External pip packages
  - "requests>=2.28.0"
  - "beautifulsoup4"
requires_services:           # Optional: Service process dependencies
  - "runtime"                # Requires Runtime for LLM calls
  - "ui"                     # Requires UI for user interaction
metadata:                    # Optional: Display info
  author: "Developer Name"
  description: "Brief description"
  license: "MIT"

```

**Plugin Base Class (TDD):**

```python
|TDD-14| ← |ICD-19|, |FSD-18|: "Component: AbstractExtension"

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AbstractExtension(ABC):
    """
    Base class for all Tools and Routines.

    Implements
    ----------
    |TDD-14|, |FSD-3|

    Lifecycle
    ---------
    1. Core instantiates: ext = ExtensionClass()
    2. Core initializes: ext.initialize(core_context)
    3. Core queries: states = ext.get_hsm_states()
    4. Core registers: ext event handlers with HSM

    Attributes
    ----------
    core_context : CoreContext
        Injected dependency for Core services
    """

    @abstractmethod
    def initialize(self, core_context: Any) -> None:
        """
        Called once during Core startup.

        Parameters
        ----------
        core_context : CoreContext
            Provides access to:
            - core_context.send_to_service(service, command, payload)
            - core_context.logger (Loguru instance)
            - core_context.config (Dict from ipc_config.yaml)

        Implementation Notes
        --------------------
        - Load extension-specific configuration
        - Initialize internal state
        - Validate required services are available

        Raises
        ------
        RuntimeError
            If required service not available

        References
        ----------
        |FSD-18.4|, |TDD-4.2|
        """
        pass

    @abstractmethod
    def get_hsm_states(self) -> List[Dict[str, Any]]:
        """
        Return HSM state definitions for dynamic compilation.

        Returns
        -------
        List[Dict]
            State configuration dicts for transitions library

        Schema
        ------
        [
          {
            "name": "state_name",
            "parent": "busy",  # Optional: Nested state
            "on_enter": "method_name",  # Optional: Callback
            "on_exit": "method_name"    # Optional: Callback
          },
          ...
        ]

        Example
        -------
        Tool that adds "exporting" state under "busy":
        [
          {"name": "exporting", "parent": "busy", "on_enter": "start_export"}
        ]

        References
        ----------
        |FSD-18.5|, |FSD-2.2|, |TDD-4.3|
        """
        pass

    @abstractmethod
    def handle_event(self, event_data: Dict[str, Any]) -> str:
        """
        Process business logic for extension-specific events.

        Parameters
        ----------
        event_data : dict
            Event payload from Core, structure:
            {
              "event_type": "user_command" | "service_response" | "timer",
              "command": str,  # If user_command
              "response": dict,  # If service_response
              "request_id": str
            }

        Returns
        -------
        str
            Next HSM trigger to fire (e.g., "to_idle", "to_error")

        Implementation Notes
        --------------------
        - Inspect event_data["event_type"]
        - Execute tool/routine logic
        - Call core_context.send_to_service() for IPC
        - Return appropriate HSM trigger

        Error Handling
        --------------
        - Raise exceptions for unrecoverable errors (Core logs + error state)
        - Return "to_error" trigger for graceful error handling

        References
        ----------
        |FSD-18.6|, |TDD-4.4|
        """
        pass

```

----------

### 20.3 Performance Profiling Documentation

When optimizing performance, document both targets and measurement methodology.

**Performance Requirements (NFR):**

```
|NFR-17| ← |BRD-8|: "Performance Profiling & Optimization"
  |NFR-17.1|: Instrumentation overhead: <1% CPU, <10MB RAM.
  |NFR-17.2|: Metrics collection frequency: Every 100ms (non-blocking).
  |NFR-17.3|: Metrics storage: Rolling buffer, last 1 hour of data.
  |NFR-17.4|: Metrics visualization: Real-time dashboard (optional UI tab).
  |NFR-17.5|: Exportable reports: JSON export for offline analysis.

```

**Profiling Features (FSD):**

```
|FSD-19| ← |NFR-17|: "Performance Monitoring"
  |FSD-19.1|: Core tracks per-request latency breakdown:
    - IPC routing time
    - Service processing time (STT, LLM, TTS)
    - Queue wait time
  |FSD-19.2|: Services report GPU/CPU utilization every 100ms.
  |FSD-19.3|: Memory profiler tracks per-process RSS/VRAM usage.
  |FSD-19.4|: UI displays real-time metrics:
    - Current FPS (UI responsiveness)
    - LLM tokens/second
    - Audio buffer health (underrun/overrun count)
  |FSD-19.5|: Admin command: "/metrics export" → saves JSON to ./logs/metrics_{timestamp}.json.

```

**Metrics Schema (ICD):**

```json
|ICD-20| ← |FSD-19.1|: "Performance Metrics Schema"
{
  "timestamp": "ISO-8601",
  "request_id": "uuid",
  "latency_breakdown": {
    "total_ms": 1234.5,
    "ipc_routing_ms": 2.1,
    "stt_processing_ms": 450.0,
    "llm_inference_ms": 780.0,
    "tts_synthesis_ms": 2.4
  },
  "resource_usage": {
    "core_process": {"cpu_percent": 5.2, "rss_mb": 45},
    "runtime_process": {"cpu_percent": 85.0, "rss_mb": 3200, "vram_mb": 4800},
    "ui_process": {"cpu_percent": 12.0, "rss_mb": 180}
  },
  "queue_stats": {
    "core_queue_size": 3,
    "runtime_queue_size": 1,
    "max_wait_time_ms": 15.0
  }
}

```

----------

## 21. Documentation Anti-Pattern Deep Dive

### 21.1 The "Implementation Leak" Anti-Pattern

**Problem:** Technical implementation details appearing in business/feature tiers.

**Example (WRONG):**

```
|FSD-X|: "The system uses zmq.ROUTER socket bound to tcp://127.0.0.1:5555
to receive user requests from the PySide6 QApplication main thread."

```

**Why Wrong:**

-   **FSD Violation:** Mentions specific technologies (ZeroMQ, PySide6)
-   **Mixed Abstraction:** Combines behavior (receive requests) with implementation (socket binding)
-   **Maintenance Burden:** Technology changes require FSD updates (should be isolated to SAD/TDD)

**Correct Decomposition:**

```
|FSD-1.1| ← |BRD-5|: "Core routes request-response messages between services."

|SAD-3.2| ← |FSD-1.1|, |NFR-5.1|: "Pattern: ZeroMQ ROUTER (Core) ↔ DEALER (Service)."

|ICD-1| ← |SAD-3.2|:
core:
  router_bind: "tcp://127.0.0.1:5555"

|TDD-1.3| ← |ICD-1|: "Socket: Bind ROUTER to core.router_bind (from config)."

|ISP-1| ← |TDD-1.3|:
def __init__(self, config_path: str):
    self.router = self.context.socket(zmq.ROUTER)
    self.router.bind(self.config['router_bind'])

```

----------

### 21.2 The "Orphaned Rationale" Anti-Pattern

**Problem:** Design decisions without traceability to requirements.

**Example (WRONG):**

```
|SAD-X|: "Use priority queues for message ordering."

```

**Why Wrong:**

-   **No Justification:** Doesn't explain WHY priority matters
-   **No Traceability:** Missing citation to parent requirement
-   **Incomplete:** Doesn't specify priority levels or ordering rules

**Correct Pattern:**

```
|NFR-5.1| ← |BRD-3.4|: "No process shall block waiting for another."

|SAD-4.3| ← |NFR-5.1|: "Queueing Strategy"
  |SAD-4.3.R1|: RATIONALE: Priority queues prevent control messages
  (shutdown, error) from being blocked behind long-running data
  messages, enforcing the non-blocking constraint.

  |SAD-4.4| ← |SAD-4.3|: "Must use queue.PriorityQueue."
  |SAD-4.5| ← |SAD-4.3|: "Structure: (priority, counter, message)."
  |SAD-4.8| ← |SAD-4.3|: "High Priority (0): shutdown, error_notification."
  |SAD-4.9| ← |SAD-4.3|: "Normal Priority (1): Inference requests."

```

----------

### 21.3 The "Premature Optimization" Anti-Pattern

**Problem:** Performance targets without business justification.

**Example (WRONG):**

```
|NFR-X|: "All IPC messages must complete in <100 microseconds."

```

**Why Wrong:**

-   **No Business Context:** Why does 100μs matter to users/business?
-   **Over-Specification:** May be orders of magnitude tighter than needed
-   **Implementation Constraint:** Forces expensive optimizations without ROI

**Correct Pattern:**

```
|BRD-12|: "Real-Time Conversational Experience"
Target: <5% session abandonment due to lag (current: 18%).

|NFR-11.1| ← |BRD-12|: "End-to-End Latency: ≤3s (voice-to-response, 95th percentile)."
  RATIONALE: User research shows 3s perceived as "instant",
  >5s causes frustration and abandonment.

|NFR-11.2| ← |NFR-11.1|: "Latency Budget Breakdown"
  - STT: 500ms (allows buffering for VAD endpoint detection)
  - LLM: 1500ms (achievable with INT4 quantization on RTX 3080)
  - TTS: 800ms (streaming synthesis, first audio chunk <200ms)
  - IPC: 200ms (total overhead across all routing)

  RATIONALE: Budget allocates majority to inference tasks (80%),
  minimizes overhead (7%), provides margin for 95th percentile variance.

|NFR-4.2| ← |NFR-11.2|: "IPC Round Trip: <20ms for 1MB payload."
  RATIONALE: 200ms total IPC budget / 10 average messages per request = 20ms each.

```

----------

## 22. Template Library

### 22.1 New Feature Template

Use this template when documenting a new feature from scratch:

~~~markdown
## Feature: [Feature Name]

### BRD: Business Justification
|BRD-X|: "[Feature Name]"
[Problem being solved, market opportunity, competitive advantage]

**Success Metrics:**
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]

### NFR: Constraints & Limits
|NFR-X| ← |BRD-X|: "[Feature Name] Constraints"
  |NFR-X.1|: [Performance constraint with measurement]
  |NFR-X.2|: [Resource constraint (CPU/GPU/RAM/Storage)]
  |NFR-X.3|: [Security/Privacy constraint]
  |NFR-X.4|: [Scalability limit]

### FSD: User-Facing Behavior
|FSD-X| ← |NFR-X|: "[Feature Name] Workflow"
  |FSD-X.1|: [User action 1] → [System response]
  |FSD-X.2|: [User action 2] → [System response]
  |FSD-X.3|: [Error scenario] → [Fallback behavior]

### SAD: Architecture
|SAD-X| ← |FSD-X|: "[Feature Name] Architecture"
  |SAD-X.1|: [Pattern selection with rationale]
  |SAD-X.2|: [Component topology/interaction]
  |SAD-X.3|: [Technology choices]

### ICD: Data Contracts
|ICD-X| ← |SAD-X|: "[Feature Name] Schemas"
```json
{
  "command": "...",
  "payload": {...}
}

```

### TDD: Component Design

|TDD-X| ← |ICD-X|, |SAD-X|: "Component: [ClassName]" |TDD-X.1|: Class: [ClassName] |TDD-X.2|: Dependencies: [list] |TDD-X.3|: Method: [signature]

### ISP: Implementation Stub

|ISP-X| ← |TDD-X|:

```python
class [ClassName]:
    """
    [Description]

    Implements
    ----------
    |TDD-X|, |FSD-X|
    """
    def __init__(self, ...):
        """..."""
        pass

```

~~~

---

### 22.2 Bug Fix Documentation Template

When fixing bugs, update documentation to prevent recurrence:

~~~markdown
## Bug Fix: [Bug ID/Title]

### Root Cause Analysis
**Tier:** [Which tier had incorrect specification]
**Tag:** |[TIER]-X| (the tag with the bug)

**Symptom:** [User-observable behavior]
**Root Cause:** [Technical explanation]

### Documentation Updates

**BEFORE (Incorrect):**

```

|[TAG]|: [Old content with bug]

```

**AFTER (Corrected):**

```

|[TAG]|: [New content fixing bug]

|[TAG].R1| (NEW RATIONALE): Previous spec caused [bug] because [explanation]. Updated to [solution] which prevents [failure mode].

```

### Downstream Impacts
- |TAG-CHILD-1|: [Update required? Yes/No]
- |TAG-CHILD-2|: [Update required? Yes/No]

### Test Coverage Addition
|TEST-X| ← |TAG|:
```python
def test_[bug_scenario]():
    """Regression test for Bug [ID]."""
    # Test that previously failing scenario now passes

```

~~~

---

### 22.3 Refactoring Documentation Template

When refactoring requires tag restructuring:

~~~markdown
## Refactoring: [Refactor Name]

### Motivation
**Problem:** [Why existing structure is problematic]
**Solution:** [How reorganization improves it]

### Migration Map
| Old Tag | New Tag | Status | Notes |
|---------|---------|--------|-------|
| `|OLD-1|` | `|NEW-1|` | MOVED | Content unchanged |
| `|OLD-2|` | `|NEW-2|` | SPLIT | Split into NEW-2.1, NEW-2.2 |
| `|OLD-3|` | DELETED | MERGED | Merged into NEW-1 |

### Backward Compatibility

```

|OLD-1| [DEPRECATED v2.5 → See |NEW-1|]: "..."

```

### Citation Updates
**Automated:**
- All `← |OLD-1|` citations replaced with `← |NEW-1|`

**Manual Review Required:**
- |CHILD-X|: Check if split requires citing both NEW-2.1 and NEW-2.2

~~~

----------

## 23. Conclusion & Quick Reference

### 23.1 The Golden Rules

1.  **Abstraction Always Flows Downward:** BRD → NFR → FSD → SAD → ICD → TDD → ISP
2.  **Citations Always Flow Upward:** Every tag cites its justification (`← |PARENT|`)
3.  **IDs Are Immutable:** Never renumber, always append
4.  **Orphans Must Be Resolved:** Every tag needs a parent (except BRD root)
5.  **Rationale Is Mandatory:** Design decisions require explicit justification
6.  **Tiers Are Fixed:** Seven tiers only, no custom intermediate layers

### 23.2 Quick Classification Checklist

**When you have a new piece of information, ask:**

-   [ ] Does it answer "Why build this?" → **BRD**
-   [ ] Does it define hard limits (hardware/SLAs)? → **NFR**
-   [ ] Does it describe what users experience? → **FSD**
-   [ ] Does it specify architectural patterns? → **SAD**
-   [ ] Does it define data shapes (JSON/YAML)? → **ICD**
-   [ ] Does it describe class structure? → **TDD**
-   [ ] Is it executable Python code? → **ISP**

### 23.3 Common Mistakes Summary

Mistake

Problem

Solution

Technology in BRD

"Use PostgreSQL"

Abstract to "Persistent storage"

Missing citations

Orphaned tags

Add `←

Implementation in
