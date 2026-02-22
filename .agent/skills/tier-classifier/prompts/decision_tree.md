# Decision Tree Classification Algorithm

Execute questions sequentially. Assign to first tier that matches.

## Q1: Business Justification Test
**Question**: Does this fragment answer "WHY are we building this?"

**Indicators**:
- Strategic objectives, market positioning, competitive advantage
- ROI projections, cost justification, business value
- Stakeholder needs, problem statements, project purpose
- Success criteria for project viability

**Examples**:
- ✅ "Enable hands-free interaction for accessibility-conscious users"
- ✅ "Reduce customer support costs by 30% via self-service AI"
- ❌ "System must respond within 1 second" (this is NFR - constraint)

**Decision**:
- YES → **Assign BRD**, STOP
- NO → Continue to Q2

---

## Q2: Constraint Boundary Test
**Question**: Does this fragment define LIMITS, constraints, or system boundaries?

**Indicators**:
- Hardware specifications (GPU memory, CPU cores, network bandwidth)
- Performance targets (latency, throughput, response time) with numeric values
- Security constraints, network isolation requirements
- Resource limits, fault tolerance thresholds
- RFC 2119 modality keywords: MUST, SHALL, SHOULD, MAY

**Examples**:
- ✅ "GPU VRAM: 10GB dedicated for model inference"
- ✅ "IPC latency MUST be < 1ms for metadata frames"
- ❌ "User can interrupt AI during speech" (this is FSD - behavior)

**Decision**:
- YES → **Assign NFR**, STOP
- NO → Continue to Q3

---

## Q3: Capability/Behavior Test
**Question**: Does this fragment describe WHAT the system does from user/stakeholder perspective?

**Indicators**:
- User-facing features, workflows, interaction patterns
- System capabilities, process orchestration, state machines
- Error handling strategies (from user view)
- Voice/UI pipelines, user experience requirements
- Technology-agnostic behavioral descriptions

**Examples**:
- ✅ "Voice pipeline: wake word → VAD → speech recognition → LLM"
- ✅ "System maintains states: sleeping, waking, active, busy, error"
- ❌ "Hub-and-Spoke messaging pattern" (this is SAD - architecture)

**Decision**:
- YES → **Assign FSD**, STOP
- NO → Continue to Q4

---

## Q4: Architectural Structure Test
**Question**: Does this fragment define HOW the system is organized/structured?

**Indicators**:
- Architectural patterns (Hub-and-Spoke, Client-Server, Event-Driven)
- Process topology, component relationships
- Integration strategies, concurrency models
- Configuration strategies (centralized, distributed)
- ASCII topology diagrams

**Examples**:
- ✅ "Core (ROUTER) hub with UI/Audio/Runtime as DEALER spokes"
- ✅ "Decoupled logging: services PUSH, LogServer PULL"
- ❌ "Log frame contains source, level, timestamp" (this is ICD - schema)

**Decision**:
- YES → **Assign SAD**, STOP
- NO → Continue to Q5

---

## Q5: Data Contract Test
**Question**: Does this fragment define data shapes, schemas, or message formats?

**Indicators**:
- JSON/YAML configuration schemas
- Message frame structures, payload formats
- Metadata schemas, API contracts
- Request/response structures
- Field-level specifications with types

**Examples**:
- ✅ `{"source": "UI", "destination": "Core", "command": "..."}`
- ✅ `rotation_mb: 50` in YAML config
- ❌ "CoreProcess class with run() method" (this is TDD - class structure)

**Decision**:
- YES → **Assign ICD**, STOP
- NO → Continue to Q6

---

## Q6: Class Structure Test
**Question**: Does this fragment specify class/module structure without executable logic?

**Indicators**:
- Component class names, inheritance hierarchies
- Method signatures (names, parameters, return types)
- Dependencies (imports, external libraries)
- Socket configurations, state management structures
- Interface contracts (abstract methods)
- **No** algorithm implementations, control flow, or business logic

**Examples**:
- ✅ "CoreProcess class: __init__(config_path), run(), route_message(frame)"
- ✅ "Dependencies: zmq, loguru, yaml"
- ❌ Actual method implementations with logic

**Decision**:
- YES → **Assign TDD**, STOP
- NO → Continue to Q7

---

## Q7: Implementation Stub Test (Default/Terminal)
**Question**: Does this fragment contain executable code skeletons?

**Indicators**:
- Python class stubs with type hints
- Numpy-style docstrings (Parameters, Returns, Implements, Requirements)
- Method bodies containing only `pass` statements
- Inline traceability comments (`# Ref: |TDD-X|`)

**Examples**:
- ✅ `def run(self) -> None: """Main loop. Implements: |TDD-1.8|""" pass`
- ✅ Complete stub with docstring but no logic

**Decision**:
- **Assign ISP**, STOP

---

## Ambiguity Handling

If fragment matches multiple tiers during traversal (e.g., contains both business value AND numeric constraints), note all candidate tiers and proceed to scoring matrix in `scoring_matrix.md`.

## Edge Cases

### Empty/Minimal Content
- Fragment too brief to classify → Request decomposition or additional context

### Cross-Tier Synthesis
- Fragment spans multiple concerns → Suggest decomposition into multiple tags

### Already Classified
- Fragment references existing tag IDs → Extract tier from tag prefix (BRD-5 → BRD)