
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
| **Structure** | "active_requests: Dict[str, Tuple[bytes, float, str]]" | `{"req-123": (b'\x00\x01', 1234.56, "llm")}` |
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

**Why Wrong:** SAD defines patterns, not data
