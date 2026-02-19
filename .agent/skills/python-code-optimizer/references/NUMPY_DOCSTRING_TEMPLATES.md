# Numpy-Style Docstring Templates

> Reference templates for the `python-code-optimizer` Antigravity Skill v3.0.0.

---

## Module-Level Docstring

```python
"""
Module Short Title

One-paragraph description of module purpose, primary responsibilities,
and how it fits into the broader system architecture.

Notes
-----
Any important implementation notes, assumptions, or constraints.

References
----------
.. [1] Author, "Title", Journal, Year.

Examples
--------
>>> import module_name
>>> module_name.primary_function(arg)
expected_output
"""
```

---

## Function Docstring (Full)

```python
def function_name(
    param1: int,
    param2: str,
    optional_param: Optional[float] = None
) -> Dict[str, Any]:
    """
    Concise one-line summary (imperative mood, no period at end).

    Extended description spanning multiple lines if needed. Explain
    the purpose, algorithm, or important behavioral nuances that are
    not obvious from the signature.

    Parameters
    ----------
    param1 : int
        Description of param1. Include valid ranges if applicable.
        E.g., must be in range [1, 1000].
    param2 : str
        Description of param2. Describe expected format or valid values.
    optional_param : float, optional
        Description of optional_param. Default is None, which triggers
        automatic computation of the value.

    Returns
    -------
    Dict[str, Any]
        Description of the returned dictionary. Document its keys:
        - 'result' : int — primary computation result
        - 'metadata' : dict — processing metadata

    Raises
    ------
    ValueError
        If param1 is outside the valid range [1, 1000].
    TypeError
        If param2 is not a string.
    RuntimeError
        If internal computation fails due to resource constraints.

    See Also
    --------
    related_function : Brief description of relationship.
    another_function : Brief description of relationship.

    Notes
    -----
    Time complexity: O(n log n) where n = len(param2).
    Space complexity: O(n).

    Caching is applied for repeated calls with identical parameters
    using `functools.lru_cache`.

    References
    ----------
    .. [1] Cormen et al., "Introduction to Algorithms", 3rd Ed., 2009.

    Examples
    --------
    Basic usage:

    >>> result = function_name(42, "hello")
    >>> result['result']
    expected_value

    With optional parameter:

    >>> result = function_name(42, "hello", optional_param=3.14)
    >>> result['metadata']['param_used']
    3.14

    Edge case:

    >>> function_name(0, "hello")
    Traceback (most recent call last):
        ...
    ValueError: param1 must be in range [1, 1000].
    """
```

---

## Class Docstring (Full)

```python
class ClassName:
    """
    One-line summary of class purpose.

    Extended description explaining the class responsibilities,
    design patterns applied, and usage context.

    Parameters
    ----------
    init_param1 : str
        Description of constructor parameter.
    init_param2 : int, default=10
        Description with default value noted.

    Attributes
    ----------
    public_attr : str
        Description of a public instance attribute.
    computed_attr : float
        Description of a computed/derived attribute.

    Methods
    -------
    primary_method(arg)
        Brief summary of primary method.
    secondary_method(a, b)
        Brief summary of secondary method.

    Raises
    ------
    ValueError
        If init_param2 is negative.

    Notes
    -----
    Thread safety: This class is NOT thread-safe. Use external locking
    when sharing instances across threads.

    Examples
    --------
    >>> obj = ClassName("example", init_param2=5)
    >>> obj.primary_method("input")
    'expected_output'
    """
```

---

## Property Docstring

```python
@property
def computed_value(self) -> float:
    """
    Computed property description (noun phrase).

    Extended explanation if the computation is non-trivial.

    Returns
    -------
    float
        Description of the returned value and its units/range.

    Raises
    ------
    RuntimeError
        If the object has not been initialized before access.
    """
```

---

## Generator / Iterator Docstring

```python
def generate_batches(
    data: List[Any],
    batch_size: int
) -> Generator[List[Any], None, None]:
    """
    Yield successive fixed-size batches from a sequence.

    Parameters
    ----------
    data : List[Any]
        Source sequence to batch.
    batch_size : int
        Number of elements per batch. Must be > 0.

    Yields
    ------
    List[Any]
        A batch containing up to `batch_size` elements from `data`.

    Raises
    ------
    ValueError
        If batch_size is not a positive integer.

    Examples
    --------
    >>> list(generate_batches([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    """
```
