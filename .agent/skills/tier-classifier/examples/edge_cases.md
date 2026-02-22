# Edge Cases & Boundary Conditions

## Case 1: Cross-Tier Synthesis

### Input
> "The voice pipeline orchestrates wake word detection, voice activity detection, and speech recognition to enable hands-free interaction with sub-200ms end-to-end latency."

### Analysis
This fragment spans **THREE** tiers:
1. **BRD**: "enable hands-free interaction" (business value)
2. **NFR**: "sub-200ms latency" (performance constraint)
3. **FSD**: "orchestrates wake word → VAD → speech recognition" (behavior)

### Recommendation
**Decompose** into three tags:
```rst
.. brd:: Hands-free voice interaction capability
  :id: BRD-5.7

.. nfr:: Voice pipeline latency < 200ms end-to-end
  :id: NFR-8.1
  :links: BRD-5.7

.. fsd:: Voice Pipeline Orchestration
  :id: FSD-4
  :links: BRD-5.7, NFR-8.1

.. fsd:: Stage 1: Wake word detection
  :id: FSD-4.1
  :links: FSD-4

.. fsd:: Stage 2: Voice activity detection (VAD)
  :id: FSD-4.2
  :links: FSD-4

.. fsd:: Stage 3: Speech recognition
  :id: FSD-4.3
  :links: FSD-4
```

---

## Case 2: Minimal/Vague Fragment

### Input
> "System should be fast and reliable."

### Analysis
**Problems**:
- "fast" - subjective, no metric
- "reliable" - subjective, no metric
- No tier indicators

### Classification Result
**UNCLASSIFIABLE**

### Recommendation
Request clarification:
- "How fast? (latency target, throughput, response time)"
- "How reliable? (uptime %, MTBF, recovery time)"
- "What business objective does this serve?"

---

## Case 3: Already-Tagged Content

### Input
> "See |BRD-5.2| for privacy requirements"

### Analysis
**Detected**: Existing tag reference `BRD-5.2`

### Classification Result
**Tier**: BRD (extracted from tag prefix)
**Action**: Link/reference, not new classification

---

## Case 4: Implementation Leakage in FSD

### Input
> "User can interrupt AI mid-sentence by pressing spacebar, which triggers a zmq.DEALER message to Core process."

### Analysis
**Decision Tree**: Q3 (WHAT?) → YES (user behavior) → FSD candidate
**Validation Failure**:
- ❌ Contains implementation details: "zmq.DEALER", "Core process"

### Recommendation
Strip implementation, reclassify as FSD:
```rst
.. fsd:: User can interrupt AI during speech output
  :id: FSD-8.5
  :links: BRD-5, NFR-4.1

.. fsd:: Interrupt triggers immediate response cancellation
  :id: FSD-8.6
  :links: FSD-8.5
```

Move implementation to SAD:
```rst
.. sad:: Interrupt via DEALER → Core → Runtime cancellation signal
  :id: SAD-5.3
  :links: FSD-8.6
```

---

## Case 5: BRD with Technology Terms

### Input
> "Leverage GPU acceleration to achieve real-time inference for competitive advantage."

### Analysis
**Decision Tree**: Q1 (WHY?) → YES → BRD candidate
**Validation Failure**:
- ❌ "GPU" is technology-specific term

### Recommendation
Abstract to technology-agnostic language:
```rst
.. brd:: Real-time AI inference for competitive responsiveness
  :id: BRD-6

.. brd:: Inference speed creates market differentiation vs cloud alternatives
  :id: BRD-6.1
  :links: BRD-6
```

Move GPU requirement to NFR:
```rst
.. nfr:: Hardware acceleration required for inference
  :id: NFR-1
  :links: BRD-6

.. nfr:: GPU with 10GB+ VRAM dedicated to model inference
  :id: NFR-1.2
  :links: NFR-1
```

---

## Case 6: ISP Without Docstring

### Input
```python
def run(self):
   pass
```

### Analysis
**Decision Tree**: Q7 (stub code?) → YES → ISP
**Validation Failure**:
- ❌ Missing Numpy-style docstring
- ❌ Missing `Implements:` citation

### Recommendation
Add required docstring:
```python
def run(self) -> None:
   """
   Main event loop processing message queue.

   Implements: |TDD-1.8|
   Requirements: |FSD-1.1|

   Returns
   -------
   None
   """
   pass
```