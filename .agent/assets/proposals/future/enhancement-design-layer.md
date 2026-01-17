# Enhancement Proposal: Design Intent Layer (DIL)

**Proposal ID:** EP-DIL-001
**Status:** Draft
**Created:** 2026-01-16
**Category:** DDR System Enhancement
**Estimated Complexity:** Medium-High

---

## 1. Executive Summary

This proposal introduces a **Design Intent Layer (DIL)**—a meta-layer mechanism that enriches DDR documentation by associating architectural elements with established design patterns and flow topologies. The DIL leverages Sphinx-Needs' native PlantUML integration and custom Need Types to create traceable "Hopeful Design" associations that propagate contextual intent through the DDR tier hierarchy.

### Core Value Proposition

| Benefit | Description |
|---------|-------------|
| **Design Continuity** | Established patterns at SAD tier influence implementation decisions at ISP tier |
| **Drift Detection** | Programmatic comparison of intended vs. realized patterns identifies architectural drift |
| **Agent Context Enhancement** | Downstream agents receive enriched context from upstream design intent |
| **Visual Validation** | PlantUML diagrams enable multimodal comparison of ideal vs. actual structures |

---

## 2. Problem Statement

### Current State

The DDR System establishes hierarchical traceability from Business Requirements (BRD) through Implementation Specifications (ISP). However, this traceability focuses on **what** is being built, not **how** architectural decisions should manifest as patterns.

### Gap Analysis

1. **No Pattern Association**: SAD elements describe architecture but don't explicitly associate with recognized design patterns (Observer, Strategy, Factory, etc.)
2. **No Design Intent Propagation**: Downstream tiers lack context about intended structural relationships
3. **No Drift Detection**: Implementation may diverge from architectural intent without detection
4. **Implicit Knowledge Loss**: Pattern decisions exist only in human understanding, not documentation

---

## 3. Proposed Solution

### 3.1 Design Intent Layer Architecture

The DIL introduces a parallel meta-layer that shadows selected DDR tiers, associating elements with design pattern templates.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DDR Hierarchy with DIL                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   BRD ─────► NFR ─────► FSD ─────► SAD ─────► ICD ─────► TDD ────► ISP
│                                     │                               │
│                                     ▼                               ▼
│                              ┌─────────────┐                ┌─────────────┐
│                              │  DIL-SAD    │  ──────────►   │  DIL-ISP    │
│                              │ (Hopeful)   │   propagates   │ (Realized)  │
│                              └─────────────┘                └─────────────┘
│                                     │                               │
│                                     └───────────┬───────────────────┘
│                                                 ▼
│                                        ┌───────────────┐
│                                        │ Drift Report  │
│                                        └───────────────┘
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Custom Sphinx-Needs Types

Define new Need types for Design Intent elements:

```python
# conf.py - Custom Need Type Definitions
needs_types = [
    # Existing DDR types preserved...

    # Design Intent Layer Types
    dict(
        directive="intent",
        title="Design Intent",
        prefix="DI_",
        color="#9B59B6",
        style="node"
    ),
    dict(
        directive="pattern",
        title="Pattern Association",
        prefix="PAT_",
        color="#3498DB",
        style="node"
    ),
    dict(
        directive="realized",
        title="Realized Pattern",
        prefix="RP_",
        color="#27AE60",
        style="node"
    ),
    dict(
        directive="drift",
        title="Pattern Drift",
        prefix="DRIFT_",
        color="#E74C3C",
        style="node"
    ),
]
```

### 3.3 Pattern Template Library

Establish a constrained set of pattern templates to reduce variability:

#### Structural Patterns
- **Adapter** - Interface translation
- **Bridge** - Abstraction/Implementation separation
- **Composite** - Tree structures
- **Decorator** - Wrapper extensions
- **Facade** - Simplified interface
- **Proxy** - Access control wrapper

#### Behavioral Patterns
- **Observer** - Event notification
- **Strategy** - Algorithm encapsulation
- **Command** - Request encapsulation
- **State** - State-dependent behavior
- **Chain of Responsibility** - Handler pipeline

#### Flow Patterns
- **Sequential** - Linear execution
- **Parallel** - Concurrent execution
- **Conditional** - Branching logic
- **Event-Driven** - Reactive execution
- **Pipeline** - Stage-based processing

---

## 4. Implementation Mechanism

### 4.1 DIL-SAD: Hopeful Design Association

An AI agent specializing on the SAD tier analyzes architectural elements and proposes pattern associations.

**Input Context:**
- All SAD-tier Need elements
- Traceability links (satisfies, implements, etc.)
- Element descriptions and content

**Output:**
- Design Intent (`intent::`) directives linking SAD elements to patterns
- PlantUML diagrams representing intended structure

**Example RST:**
```rst
.. intent:: Hub-Spoke Observer Intent
   :id: DI_001
   :pattern: Observer
   :applies_to: SAD-1, SAD-2, SAD-3
   :confidence: HIGH
   :rationale: Core Process (SAD-1) maintains subscriber list; Services (SAD-2, SAD-3) receive state updates

   The Hub-and-Spoke topology maps to the Observer pattern where:

   - **Subject**: Core Process (message router)
   - **Observers**: Service processes (message consumers)

   .. uml::

      @startuml
      !define SUBJECT_COLOR #FFE5E5
      !define OBSERVER_COLOR #E5F5FF

      interface Subject <<SAD-1>> SUBJECT_COLOR {
        +attach(observer)
        +detach(observer)
        +notify()
      }

      interface Observer <<SAD-2, SAD-3>> OBSERVER_COLOR {
        +update()
      }

      Subject "1" o-- "0..*" Observer : notifies
      @enduml
```

### 4.2 DIL-ISP: Realized Pattern Association

An AI agent specializing on the ISP tier examines implementation specifications and identifies realized patterns.

**Input Context:**
- All ISP-tier Need elements
- Upstream DIL-SAD associations (Hopeful Designs)
- Implementation details and code references

**Output:**
- Realized Pattern (`realized::`) directives documenting actual implementation
- Comparison with Hopeful Design

**Example RST:**
```rst
.. realized:: Message Router Implementation
   :id: RP_001
   :pattern: Observer
   :implements: DI_001
   :variance: MINOR
   :drift_items: DRIFT_001

   Implementation realizes the Observer pattern with modifications:

   - Subject role: `CoreProcess.message_router`
   - Observer role: `ServiceProcess.handle_message`
   - Variance: Uses ZMQ ROUTER/DEALER instead of direct callbacks

   .. uml::

      @startuml
      class CoreProcess <<Subject>> {
        -routing_table: Dict
        +register_service()
        +route_message()
      }

      class ServiceProcess <<Observer>> {
        -socket: zmq.Socket
        +handle_message()
      }

      CoreProcess "1" --> "0..*" ServiceProcess : routes via ZMQ
      @enduml
```

### 4.3 Drift Detection and Reporting

Programmatic comparison identifies structural deviations between Hopeful and Realized patterns.

**Drift Categories:**

| Category | Severity | Description |
|----------|----------|-------------|
| **CONFORMANT** | None | Realized pattern matches intent |
| **MINOR** | Low | Implementation varies but preserves pattern intent |
| **MAJOR** | Medium | Significant structural deviation from intent |
| **DIVERGENT** | High | Implementation contradicts design intent |

**Drift Element Example:**
```rst
.. drift:: ZMQ Transport Substitution
   :id: DRIFT_001
   :severity: MINOR
   :hopeful: DI_001
   :realized: RP_001
   :impact: LOW

   **Deviation:** Direct observer callbacks replaced with ZMQ message passing.

   **Justification:** ZMQ provides process isolation and network transparency.

   **Architectural Impact:** Pattern semantics preserved; transport mechanism differs.
```

---

## 5. Agent Workflow Integration

### 5.1 SAD-Tier Agent Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                  SAD Agent Workflow                         │
├─────────────────────────────────────────────────────────────┤
│ 1. ANALYZE    │ Parse SAD-tier elements from needs.json    │
│ 2. CLASSIFY   │ Match element relationships to pattern     │
│               │ templates                                   │
│ 3. ASSOCIATE  │ Create intent:: directives with pattern    │
│               │ assignments                                 │
│ 4. VISUALIZE  │ Generate PlantUML diagrams for each intent │
│ 5. DOCUMENT   │ Produce DIL-SAD documentation tier         │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 ISP-Tier Agent Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                  ISP Agent Workflow                         │
├─────────────────────────────────────────────────────────────┤
│ 1. RECEIVE    │ Ingest DIL-SAD Hopeful Designs as context  │
│ 2. ANALYZE    │ Parse ISP-tier elements from needs.json    │
│ 3. REALIZE    │ Map implementations to Hopeful patterns    │
│ 4. COMPARE    │ Identify structural variances              │
│ 5. REPORT     │ Generate drift:: elements for deviations   │
│ 6. VISUALIZE  │ Produce comparative PlantUML diagrams      │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Context Propagation

Hopeful Designs provide downstream agents with:

1. **Pattern Vocabulary** - Shared language for structural roles
2. **Constraint Guidance** - Expected relationships and multiplicities
3. **Decision Framework** - Basis for evaluating implementation choices
4. **Deviation Justification** - Requirement to document divergence rationale

---

## 6. PlantUML Integration Strategy

### 6.1 Sphinx-Needs Native Support

Sphinx-Needs includes built-in PlantUML support via `sphinxcontrib-plantuml`. Diagrams embed directly in Need content.

**Configuration:**
```python
# conf.py
extensions = [
    'sphinx_needs',
    'sphinxcontrib.plantuml',
]

# PlantUML settings
plantuml = 'java -jar /path/to/plantuml.jar'
plantuml_output_format = 'svg'
```

### 6.2 Contextual Styling Convention

Assign semantic meaning to PlantUML styling:

| Style Element | Meaning |
|---------------|---------|
| `#FFE5E5` (Light Red) | Subject/Publisher role |
| `#E5F5FF` (Light Blue) | Observer/Subscriber role |
| `#E5FFE5` (Light Green) | Conformant implementation |
| `#FFFFE5` (Light Yellow) | Minor variance |
| `#FFE5E5` (Light Red) | Major drift |
| `<<stereotype>>` | DDR Tag reference |
| Solid line (`-->`) | Direct relationship |
| Dashed line (`..>`) | Indirect/derived relationship |

### 6.3 Multimodal Comparison

Agents with vision capabilities can compare side-by-side diagrams:

```
┌────────────────────────┐    ┌────────────────────────┐
│   Hopeful Design       │    │   Realized Pattern     │
│   (DI_001)             │    │   (RP_001)             │
├────────────────────────┤    ├────────────────────────┤
│                        │    │                        │
│   ┌─────────┐          │    │   ┌─────────┐          │
│   │ Subject │          │    │   │CoreProc │          │
│   └────┬────┘          │    │   └────┬────┘          │
│        │ notifies      │    │        │ routes        │
│        ▼               │    │        ▼               │
│   ┌─────────┐          │    │   ┌─────────┐          │
│   │Observer │          │    │   │Service  │          │
│   └─────────┘          │    │   └─────────┘          │
│                        │    │                        │
└────────────────────────┘    └────────────────────────┘
         │                              │
         └──────────────┬───────────────┘
                        ▼
              Visual Diff Analysis
```

---

## 7. Validation Mechanism

### 7.1 Programmatic Validation

Automated checks against pattern constraints:

```python
def validate_pattern_realization(hopeful: Intent, realized: Realized) -> DriftReport:
    """
    Compare Hopeful Design to Realized Pattern.

    Checks:
    1. Role count matches (e.g., 1 Subject, N Observers)
    2. Relationship types preserved
    3. Multiplicity constraints satisfied
    4. Required operations present
    """
    violations = []

    # Check participant counts
    if hopeful.subject_count != realized.subject_count:
        violations.append(DriftViolation(
            type="PARTICIPANT_COUNT",
            expected=hopeful.subject_count,
            actual=realized.subject_count
        ))

    # Check relationship preservation
    for rel in hopeful.relationships:
        if not realized.has_equivalent(rel):
            violations.append(DriftViolation(
                type="RELATIONSHIP_MISSING",
                expected=rel
            ))

    return DriftReport(
        severity=calculate_severity(violations),
        violations=violations
    )
```

### 7.2 Agent-Assisted Validation

For complex structural comparisons, agents can perform multimodal analysis:

1. Render both Hopeful and Realized PlantUML diagrams
2. Compare visual structure using vision capabilities
3. Identify semantic differences not captured by programmatic rules
4. Generate natural language drift explanations

---

## 8. Integration with Existing DDR Infrastructure

### 8.1 needs.json Consumption

DIL agents consume the existing `needs.json` output:

```json
{
  "SAD-1": {
    "id": "SAD-1",
    "type": "arch",
    "title": "Hub-and-Spoke Topology",
    "content": "Core Process acts as central ROUTER...",
    "links": {
      "satisfies": ["FSD-2", "FSD-3"]
    }
  }
}
```

### 8.2 DIL Output Format

DIL augments `needs.json` with pattern metadata:

```json
{
  "DI_001": {
    "id": "DI_001",
    "type": "intent",
    "pattern": "Observer",
    "applies_to": ["SAD-1", "SAD-2", "SAD-3"],
    "role_assignments": {
      "SAD-1": "SUBJECT",
      "SAD-2": "OBSERVER",
      "SAD-3": "OBSERVER"
    },
    "diagram_path": "_static/diagrams/di_001_observer.svg"
  }
}
```

### 8.3 rebuild_docs Integration

Extend existing `rebuild_docs` workflow:

```
1. Build Sphinx HTML (existing)
2. Generate needs.json (existing)
3. Execute DIL-SAD analysis (NEW)
4. Execute DIL-ISP analysis (NEW)
5. Generate drift report (NEW)
6. Rebuild with DIL elements (NEW)
```

---

## 9. Success Criteria

| Metric | Target |
|--------|--------|
| Pattern coverage | ≥80% of SAD elements associated with patterns |
| Drift detection rate | ≥95% of structural deviations identified |
| False positive rate | ≤5% of drift reports are spurious |
| Agent context improvement | Measurable improvement in downstream decisions |
| Build time impact | <30 seconds added to documentation build |

---

## 10. Implementation Phases

### Phase 1: Foundation (Est. 40 hours)
- Define custom Need types in `conf.py`
- Create pattern template library (YAML)
- Establish PlantUML styling conventions
- Document DIL tier structure

### Phase 2: SAD Analysis (Est. 60 hours)
- Develop SAD-tier pattern classification logic
- Implement `intent::` directive generation
- Create PlantUML diagram templates
- Build agent workflow for SAD analysis

### Phase 3: ISP Analysis (Est. 60 hours)
- Develop ISP-tier realization detection
- Implement `realized::` directive generation
- Build comparison logic against Hopeful Designs
- Create `drift::` element generation

### Phase 4: Validation & Reporting (Est. 40 hours)
- Implement programmatic drift detection
- Generate drift reports (Markdown, JSON)
- Integrate with rebuild_docs workflow
- Add visual diff capabilities

**Total Estimated Effort:** 200 hours

---

## 11. Appendix: Naming Alternatives

The term "Hopeful Design" is a working title. Alternatives considered:

| Term | Pros | Cons |
|------|------|------|
| **Hopeful Design** | Evocative, humble | Informal |
| **Design Intent** | Professional, clear | Generic |
| **Architecture Blueprint** | Technical accuracy | Overloaded term |
| **Pattern Aspiration** | Captures forward-looking nature | Unusual phrasing |
| **Structural Target** | Precise | Cold, mechanical |

**Recommendation:** Use **Design Intent** for formal documentation, **Hopeful Design** for conceptual discussions.

---

## 12. References

- [Sphinx-Needs Documentation](https://sphinx-needs.readthedocs.io/)
- [PlantUML Language Reference](https://plantuml.com/guide)
- [Gang of Four Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns)
- DDR Meta-Standard (`ddr_meta_standard.txt`)
- DDR Hierarchy Definition (`ddr_hierarchy.md`)
