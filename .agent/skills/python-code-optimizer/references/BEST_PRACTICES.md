# Enterprise Python Best Practices

> Reference guide for the `python-code-optimizer` Antigravity Skill v1.15.6.

---

## 1. Code Structure & Architecture

### Single Responsibility Principle

Each module, class, and function should have exactly one reason to change.

```python
# Anti-pattern: God function
def process_user_order(user_id, items, payment, notify):
    user = fetch_user(user_id)           # DB concern
    total = sum(i['price'] for i in items)  # calculation concern
    charge(payment, total)               # payment concern
    send_email(user['email'], items)     # notification concern

# Better: Separated responsibilities
def process_user_order(user_id: int, items: List[Item]) -> OrderResult:
    user  = UserRepository.get(user_id)
    order = OrderCalculator.compute(items)
    PaymentService.charge(user.payment_method, order.total)
    NotificationService.send_order_confirmation(user, order)
    return order
```

---

## 2. Constants and Configuration

```python
# Anti-pattern: magic numbers
if retries > 3:
    sleep(0.5)

# Best practice: named constants at module level
MAX_RETRY_ATTEMPTS: int = 3
RETRY_BACKOFF_SECONDS: float = 0.5

if retries > MAX_RETRY_ATTEMPTS:
    sleep(RETRY_BACKOFF_SECONDS)
```

---

## 3. Logging Standards

```python
import logging

logger = logging.getLogger(__name__)

# Levels: DEBUG → INFO → WARNING → ERROR → CRITICAL
logger.debug("Entering _process_batch: size=%d", len(batch))
logger.info("Optimization complete: %d changes applied", n)
logger.warning("Complexity threshold exceeded: %s=%d", name, cc)
logger.error("Failed to write output: %s", str(e), exc_info=True)
```

---

## 4. Context Managers for Resources

```python
# Always use context managers for I/O
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Database connections
with db.connection() as conn:
    results = conn.execute(query)

# Temporary directories
import tempfile
with tempfile.TemporaryDirectory() as tmp_dir:
    working_file = Path(tmp_dir) / 'work.py'
```

---

## 5. Dataclass vs. NamedTuple vs. TypedDict

| Use Case                        | Recommended Type   |
|---------------------------------|--------------------|
| Mutable data container          | `@dataclass`       |
| Immutable record                | `NamedTuple`       |
| Dict with typed keys            | `TypedDict`        |
| Config with defaults + methods  | `@dataclass`       |

---

## 6. Defensive Programming

```python
def divide(numerator: float, denominator: float) -> float:
    """
    Safely divide two numbers.

    Parameters
    ----------
    numerator : float
        Dividend value.
    denominator : float
        Divisor value; must not be zero.

    Returns
    -------
    float
        Result of numerator / denominator.

    Raises
    ------
    ValueError
        If denominator is zero.
    TypeError
        If either argument is not a numeric type.
    """
    if not isinstance(numerator, (int, float)):
        raise TypeError(f"Expected numeric, got {type(numerator).__name__}")
    if not isinstance(denominator, (int, float)):
        raise TypeError(f"Expected numeric, got {type(denominator).__name__}")
    if denominator == 0:
        raise ValueError("Denominator must not be zero.")
    return numerator / denominator
```

---

## 7. Testing Standards (companion to optimization)

```python
import pytest

class TestDivide:
    """Test suite for the divide() function."""

    def test_positive_division(self) -> None:
        assert divide(10.0, 2.0) == 5.0

    def test_zero_denominator_raises(self) -> None:
        with pytest.raises(ValueError, match="Denominator must not be zero"):
            divide(5.0, 0.0)

    def test_type_error_on_string(self) -> None:
        with pytest.raises(TypeError):
            divide("5", 2.0)

    @pytest.mark.parametrize("n,d,expected", [
        (9.0, 3.0, 3.0),
        (-6.0, 2.0, -3.0),
        (0.0, 5.0, 0.0),
    ])
    def test_parametrized(self, n, d, expected) -> None:
        assert divide(n, d) == pytest.approx(expected)
```

---

## 8. Version Compatibility

Target Python 3.8+ for enterprise compatibility:

```python
# Use __future__ annotations for forward references (Python 3.8)
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .heavy_module import HeavyClass  # Avoid circular imports
```

---

## 9. Security Considerations

- Never use `eval()` or `exec()` on untrusted input
- Use `secrets` module (not `random`) for security tokens
- Validate and sanitize all external inputs
- Avoid `pickle` for untrusted data (prefer JSON or msgpack)
- Use `subprocess` with explicit argument lists (not shell=True)

```python
# Dangerous
subprocess.run(user_input, shell=True)

# Safe
subprocess.run(['git', 'status', '--short'], capture_output=True)
```

---

## 10. Performance Profiling Reference

```bash
# Profile execution time
python -m cProfile -s cumulative script.py

# Memory profiling (requires memory_profiler)
python -m memory_profiler script.py

# Line-level profiling (requires line_profiler)
kernprof -l -v script.py
```
