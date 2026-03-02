---
name: enterprise-python-service-mesh-v1.2.0
description: "High-concurrency architectural enforcer for distributed Python services. Optimizes Gemini 3.1 Pro for 24-thread parallel verification and zero-latency async patterns."
version: "1.2.0"
trigger: glob
globs: "src/services/**/*.py, internal/core/*.py"
priority: critical
execution_tier: parallel_high_perf
---

# Enterprise Python Service Architecture

<constraints>
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
**SILENT VERIFICATION PROTOCOL (Gemini 3.1 Pro Reasoning):**

1. **AST Analysis:** Scan the file for any imports from `requests` or `time`. If found, silently refactor to `aiohttp` and `asyncio` before output.
2. **Type-Check Loop:** Verify that every function has a non-void return type hint. Confirm no `Any` types are present in variable assignments.
3. **Hardware-Parallel Audit:** Execute a secondary reasoning pass in a parallel thread to check for race conditions in `async` function bodies.
4. **Contract Validation:** Ensure all class-based data structures inherit from the project's `BaseContract` and not raw `dict`.
</verification_step>
