---
name: enterprise-python-service-mesh-v1.2.0
description: "Architectural enforcer for distributed Python services. Optimizes for Gemini 3.1 Pro reasoning patterns and async I/O integrity."
version: "1.2.0"
trigger: glob
globs: "src/services/**/*.py, internal/core/*.py"
priority: critical
execution_tier: standard
---
<constraints>

# Enterprise Python Service Architecture

## 1. Concurrency & I/O Integrity

- **Non-Blocking Mandate:** All I/O operations must utilize `asyncio` or `trio` primitives. Usage of `requests`, `urllib`, or `time.sleep` is strictly prohibited.
- **Event Loop Protection:** CPU-bound tasks exceeding 50ms must be offloaded to `loop.run_in_executor()` to prevent event loop starvation.

## 2. Deterministic Type Safety (Level 3)

- **Zero-Elision Policy:** The use of `Any`, `Incomplete`, or `Unknown` is forbidden. Complex external types must be modeled using `typing.Protocol` or `typing.TypedDict`.
- **Generic Variance:** All generic collections must specify variance (e.g., `Sequence[T_co]`) to ensure covariance/contravariance integrity.

## 3. Resilience & Exception Handling

- **Specific Catching:** `try...except` blocks must target leaf-node exceptions. Catching `Exception` or `BaseException` is a critical violation.
- **Traceback Sanitization:** Exception logging must use a custom `SanitizedLogger` to prevent PII leakage in stack traces.

## 4. Data Contract Enforcement

- **Pydantic V2 Migration:** All ingress/egress payloads must be validated via `pydantic.BaseModel` with `strict=True` enabled.
</constraints>

<verification_step>
**AGENTIC VERIFICATION PROTOCOL:**

1. **Architectural Review:** Evaluate the asynchronous design pattern for potential event-loop bottlenecks.
2. **Contract Validation:** Ensure all class-based data structures align logically with the project's `BaseContract`.
3. **Dependency Check:** Suggest modern async alternatives if synchronous blocking libraries are detected in the architecture.
</verification_step>
