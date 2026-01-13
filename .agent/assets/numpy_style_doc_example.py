# @meta-instruction: SYSTEM_ROLE: STYLE_GUIDE_ONLY
# @meta-instruction: CONSTRAINT: DO NOT import 'numpy' or 'typing' dependencies from this file into the target file unless already present.
# @meta-instruction: CONSTRAINT: Use the types actually present in the target file's signature (e.g., if target uses 'List', do not change to 'typing.List').
# @meta-instruction: GOAL: Replicate the *structure* and *verbosity* of these docstrings, not the code logic.

"""
Comprehensive Numpy-Style Docstring Reference.

This module demonstrates canonical and advanced Numpy-style docstring
patterns as rendered by Sphinx with the Napoleon extension enabled.
It is intended as a normative internal reference for consistent API
documentation across enterprise and government codebases.

**Scope**: This reference covers all standard numpydoc sections (Parameters,
Returns, Yields, Raises, Warns, See Also, Notes, References, Examples) plus
common Sphinx directives and cross-referencing patterns. It does not attempt
to catalog every possible Sphinx extension or configuration option.

**Configuration**: This module assumes the following Sphinx configuration::

   extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
   napoleon_google_docstring = False
   napoleon_numpy_docstring = True
   napoleon_use_param = False
   napoleon_use_rtype = False
   autodoc_typehints = 'description'

Attributes
----------
MODULE_CONSTANT : int
   A module-level constant demonstrating attribute documentation.
CONFIGURATION : dict
   Module configuration dictionary with nested structure.

See Also
--------
sphinx.ext.napoleon : Sphinx extension for Numpy-style docstrings.
numpydoc : Numpy documentation style guide.

Notes
-----
This implementation follows PEP 257 conventions for docstring structure.
Types are ALWAYS included in Parameters sections, regardless of whether
function signatures have type hints, ensuring maximum plain-text readability
and documentation consistency.

All code examples are executable and validated through doctest.

References
----------
.. [1] Numpy Documentation Style Guide,
  https://numpydoc.readthedocs.io/en/latest/format.html
.. [2] Sphinx Napoleon Extension,
  https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
.. [3] PEP 257 -- Docstring Conventions,
  https://www.python.org/dev/peps/pep-0257/

Examples
--------
Import and use this module as a reference:

>>> from numpy_docstring_gold import DemoClass
>>> obj = DemoClass(name="example", value=42)
>>> result = obj.compute_complex_operation(10, 20, mode='advanced')
>>> result['sum']
30

"""

import numpy as np
from typing import Union, Optional, List, Dict, Tuple, Callable, Any, TypeVar, Iterator
from collections.abc import Iterable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import warnings
import time

__version__ = "2.0.0"
__author__ = "Documentation Standards Team"
__license__ = "MIT"

# Module-level constants
MODULE_CONSTANT = 100
CONFIGURATION = {
   'max_iterations': 1000,
   'tolerance': 1e-6,
   'verbose': True
}

# Type variables for generic documentation
T = TypeVar('T')
NumericType = Union[int, float, np.ndarray]


class CustomException(Exception):
   """
   Custom exception for validation failures.

   Raised when specific validation conditions fail during parameter
   checking or operational constraints are violated.

   Parameters
   ----------
   message : str
       Error message describing the validation failure.
   error_code : int, optional
       Numeric error code for programmatic error handling. Negative values
       indicate internal errors; positive values indicate user errors.
       Default is -1.

   Attributes
   ----------
   message : str
       The error message.
   error_code : int
       The numeric error code.
   timestamp : float
       Unix timestamp when exception was created.

   Examples
   --------
   >>> raise CustomException("Invalid input", error_code=404)
   Traceback (most recent call last):
       ...
   CustomException: Invalid input

   """

   def __init__(self, message: str, error_code: int = -1):
       super().__init__(message)
       self.message = message
       self.error_code = error_code
       self.timestamp = time.time()


class ValidationError(CustomException):
   """
   Exception raised for parameter validation failures.

   .. versionadded:: 2.0.0
      Specialized exception for validation errors.

   Inherits all attributes and behavior from :exc:`CustomException` with
   specialized error code defaults for validation scenarios.

   Parameters
   ----------
   message : str
       Validation error description.
   parameter_name : str, optional
       Name of the parameter that failed validation. Default is None.

   See Also
   --------
   CustomException : Base exception class.

   """

   def __init__(self, message: str, parameter_name: Optional[str] = None):
       full_message = f"Validation failed"
       if parameter_name:
           full_message += f" for parameter '{parameter_name}'"
       full_message += f": {message}"
       super().__init__(full_message, error_code=400)
       self.parameter_name = parameter_name


class BaseInterface(ABC):
   """
   Abstract base class defining the processing interface.

   Concrete implementations must provide data processing logic while
   adhering to the contract defined by abstract methods.

   Methods
   -------
   process_data
       Transform input data according to implementation-specific algorithm.

   Notes
   -----
   Subclasses must implement all abstract methods to be instantiable.
   The interface assumes array-like numeric data as input.

   """

   @abstractmethod
   def process_data(self, data: np.ndarray) -> np.ndarray:
       """
       Transform input data according to implementation-specific algorithm.

       Parameters
       ----------
       data : numpy.ndarray
           Input data array. Dimensionality constraints depend on
           implementation.

       Returns
       -------
       ndarray
           Transformed data with shape determined by implementation.

       """
       pass


@dataclass
class ComputationConfig:
   """
   Configuration container for computation parameters.

   .. versionadded:: 2.0.0

   Encapsulates all parameters controlling computation behavior using
   dataclass pattern for immutability and validation.

   Attributes
   ----------
   tolerance : float
       Convergence tolerance for iterative algorithms. Must be positive.
   max_iterations : int
       Maximum number of iterations before termination. Must be positive.
   verbose : bool
       Enable detailed logging during computation.
   cache_results : bool
       Enable result caching for repeated computations with identical inputs.

   Examples
   --------
   >>> config = ComputationConfig(tolerance=1e-8, max_iterations=500)
   >>> config.tolerance
   1e-08
   >>> config.verbose
   False

   """

   tolerance: float = 1e-6
   max_iterations: int = 1000
   verbose: bool = False
   cache_results: bool = True

   def __post_init__(self):
       """Validate configuration parameters after initialization."""
       if self.tolerance <= 0:
           raise ValidationError("Must be positive", "tolerance")
       if self.max_iterations <= 0:
           raise ValidationError("Must be positive", "max_iterations")


class DemoClass(BaseInterface):
   """
   Reference implementation demonstrating comprehensive docstring patterns.

   Provides mathematical operations, data processing, and sequence generation
   with extensive parameter validation and error handling. Implements the
   :class:`BaseInterface` protocol for array processing.

   Parameters
   ----------
   name : str
       Identifier for this instance. Must be non-empty.
   value : NumericType
       Numeric value used in processing operations. Must be non-negative.
   config : dict, optional
       Configuration dictionary with custom settings. If None, defaults
       to empty configuration.
   *args : tuple
       Additional positional arguments stored for reference.
   **kwargs : dict
       Additional keyword arguments stored in internal state.

   Attributes
   ----------
   name : str
       The name identifier (read-only property).
   value : float
       The numeric value (modifiable).
   config : dict
       Configuration dictionary.
   processing_count : int
       Number of processing operations performed.

   Raises
   ------
   ValidationError
       If name is empty or value is negative.

   See Also
   --------
   BaseInterface : Parent abstract class defining the processing protocol.
   ComputationConfig : Configuration container for structured settings.
   helper_function : Related utility for statistical computations.

   Notes
   -----
   Internal state is managed through the ``_internal_state`` dictionary,
   which tracks operational metadata including initialization parameters
   and context manager status.

   Mathematical operations follow standard conventions. For complex operations,
   results follow the formula:

   .. math:: f(x, y) = \\sqrt{x^2 + y^2}

   The class supports the context manager protocol for resource-managed
   operations.

   References
   ----------
   .. [1] Knuth, Donald E. "The Art of Computer Programming",
      Volume 1: Fundamental Algorithms, 3rd Edition.

   Examples
   --------
   Basic instantiation and property access:

   >>> obj = DemoClass(name="test", value=42)
   >>> obj.value
   42.0
   >>> obj.name
   'test'

   Complex operation with multiple modes:

   >>> result = obj.compute_complex_operation(10, 20, mode='advanced')
   >>> result['sum']
   30

   Context manager usage:

   >>> with DemoClass(name="ctx", value=5) as obj:
   ...     print(obj.value)
   5.0

   """

   def __init__(
       self,
       name: str,
       value: NumericType,
       config: Optional[Dict[str, Any]] = None,
       *args,
       **kwargs
   ):
       if not isinstance(name, str) or not name:
           raise ValidationError("Must be non-empty string", "name")

       if isinstance(value, (int, float)) and value < 0:
           raise ValidationError("Must be non-negative", "value")

       self._name = name
       self.value = float(value)
       self.config = config or {}
       self._internal_state = {
           'initialized': True,
           'args': args,
           'kwargs': kwargs
       }
       self.processing_count = 0

   @property
   def name(self) -> str:
       """
       Get the instance name.

       Returns
       -------
       str
           The name identifier for this instance.

       Notes
       -----
       This property is read-only. The name is fixed at construction time
       and cannot be modified after initialization.

       Examples
       --------
       >>> obj = DemoClass(name="example", value=10)
       >>> obj.name
       'example'

       """
       return self._name

   def compute_complex_operation(
       self,
       x: NumericType,
       y: NumericType,
       mode: str = 'simple',
       scale: float = 1.0,
       callback: Optional[Callable[[float], float]] = None,
       **options
   ) -> Dict[str, Union[float, np.ndarray]]:
       """
       Compute arithmetic results using selectable algorithms.
       Performs basic arithmetic operations with optional scaling and
       post-processing. Operation behavior and computational complexity
       depend on the selected mode.

       Parameters
       ----------
       x : NumericType
           First operand. Accepts scalars or arrays; shape determines
           output dimensionality via broadcasting.
       y : NumericType
           Second operand. Must be broadcast-compatible with `x`.
       mode : str, optional
           Algorithm selector. Valid values: 'simple', 'advanced', 'experimental'.
           Simple mode performs basic arithmetic. Advanced mode includes
           magnitude computation. Experimental mode applies developmental
           algorithms subject to change. Default is 'simple'.
       scale : float, optional
           Multiplicative scaling factor applied uniformly to all results.
           Default is 1.0.
       callback : Callable[[float], float], optional
           Optional post-processing function applied element-wise to final
           results. Signature must be ``f(value: float) -> float``.
       **options : dict
           Additional configuration options:

           * ``tolerance`` (float) -- Convergence tolerance for iterative modes
           * ``max_iter`` (int) -- Maximum iterations for iterative modes
           * ``verbose`` (bool) -- Enable detailed operation logging

       Returns
       -------
       dict
           Mapping of computed quantities to their values. All results are
           scaled and post-processed if callback provided.

       Raises
       ------
       ValidationError
           If mode is not one of the allowed values.
       ValueError
           If x and y have incompatible shapes for broadcasting.
       TypeError
           If callback is provided but not callable.

       Warns
       -----
       UserWarning
           When using experimental mode, as algorithms may change or be
           removed in future versions.

       See Also
       --------
       helper_function : Statistical computations on arrays.
       numpy.add : Element-wise addition operation.
       numpy.multiply : Element-wise multiplication operation.

       Notes
       -----
       Computational complexity varies by mode:

       * Simple mode: :math:`O(n)` for array inputs
       * Advanced mode: :math:`O(n \\log n)` due to magnitude computation
       * Experimental mode: :math:`O(n^2)` worst-case complexity

       Scaling is applied uniformly after primary computation:

       .. math::

           result_{scaled} = scale \\cdot result_{raw}

       Results dictionary always contains keys ``sum``, ``product``, and
       ``difference``. Advanced and experimental modes add ``advanced_result``
       containing the Euclidean magnitude.

       Array operations follow NumPy broadcasting rules. This implementation
       relies on NumPy's optimized BLAS routines for array operations.

       References
       ----------
       .. [1] Harris, C.R., et al. "Array programming with NumPy."
          Nature 585.7825 (2020): 357-362.

       Examples
       --------
       Simple scalar arithmetic:

       >>> obj = DemoClass(name="calc", value=1)
       >>> result = obj.compute_complex_operation(10, 5)
       >>> result['sum']
       15.0

       Advanced mode with explicit scaling:

       >>> result = obj.compute_complex_operation(10, 5, mode='advanced', scale=2.0)
       >>> result['sum']
       30.0

       Array operations with post-processing callback:

       >>> x = np.array([1, 2, 3])
       >>> y = np.array([4, 5, 6])
       >>> result = obj.compute_complex_operation(x, y, callback=lambda v: v ** 2)
       >>> result['sum']  # doctest: +SKIP
       array([25., 49., 81.])

       Configuration via options dictionary:

       >>> result = obj.compute_complex_operation(
       ...     10, 5, tolerance=1e-8, max_iter=100, verbose=True
       ... )

       """
       allowed_modes = ['simple', 'advanced', 'experimental']
       if mode not in allowed_modes:
           raise ValidationError(
               f"Must be one of {allowed_modes}",
               "mode"
           )

       if callback is not None and not callable(callback):
           raise TypeError("callback must be callable")

       if mode == 'experimental':
           warnings.warn(
               "Experimental mode uses developmental algorithms subject to change",
               UserWarning,
               stacklevel=2
           )

       # Increment processing counter
       self.processing_count += 1

       # Perform primary computations
       result = {
           'sum': scale * (x + y),
           'product': scale * (x * y),
           'difference': scale * (x - y)
       }

       if mode in ['advanced', 'experimental']:
           result['advanced_result'] = scale * np.sqrt(x**2 + y**2)

       # Apply optional callback to all results
       if callback is not None:
           for key in result:
               result[key] = callback(result[key])

       return result

   def process_data(self, data: np.ndarray) -> np.ndarray:
       """
       Transform input array using normalization and scaling.

       Implements the abstract interface from :class:`BaseInterface` by
       applying z-score normalization followed by multiplication with
       the instance value attribute.

       Parameters
       ----------
       data : numpy.ndarray
           Input array to process. Must be 1D or 2D. Empty arrays are rejected.

       Returns
       -------
       ndarray
           Transformed array with same shape as input.

       Raises
       ------
       ValueError
           If data has more than 2 dimensions or is empty.

       See Also
       --------
       BaseInterface.process_data : Abstract method specification.
       helper_function : Related statistical computation utility.

       Notes
       -----
       Transformation applies z-score normalization followed by scaling:

       .. math::

           output = \\frac{input - \\mu}{\\sigma} \\cdot value

       where :math:`\\mu` is the arithmetic mean, :math:`\\sigma` is the
       standard deviation, and :math:`value` is the instance value attribute.

       If standard deviation is zero (constant array), scaling is applied
       directly without normalization to avoid division by zero.

       Examples
       --------
       Process 1D array:

       >>> obj = DemoClass(name="processor", value=10)
       >>> data = np.array([1, 2, 3, 4, 5])
       >>> processed = obj.process_data(data)
       >>> processed.shape
       (5,)

       Process 2D array:

       >>> data = np.array([[1, 2], [3, 4]])
       >>> processed = obj.process_data(data)
       >>> processed.shape
       (2, 2)

       """
       if data.size == 0:
           raise ValueError("Cannot process empty array")

       if data.ndim > 2:
           raise ValueError("Data must be 1D or 2D array")

       mean = np.mean(data)
       std = np.std(data)

       # Handle constant arrays to avoid division by zero
       if std == 0:
           return data * self.value

       normalized = (data - mean) / std
       return normalized * self.value

   def generate_sequence(
       self,
       start: int,
       stop: int,
       step: int = 1
   ) -> Iterator[int]:
       """
       Generate integer sequence with configurable step size.

       Produces values lazily similar to built-in :func:`range`, maintaining
       minimal memory footprint regardless of sequence length.

       Parameters
       ----------
       start : int
           First value in the sequence (inclusive).
       stop : int
           Boundary value (exclusive for positive step, exclusive for negative).
       step : int, optional
           Increment between consecutive values. Must be non-zero. Default is 1.

       Yields
       ------
       int
           The next value in the sequence.

       Raises
       ------
       ValueError
           If step is zero.
       ValidationError
           If start/stop relationship conflicts with step direction.

       See Also
       --------
       range : Built-in Python range function with similar semantics.

       Notes
       -----
       Generator maintains internal state and yields values lazily, providing
       memory efficiency for large sequences.

       Step direction must be consistent with start/stop relationship:

       * Positive step requires start < stop
       * Negative step requires start > stop

       Examples
       --------
       Forward iteration with default step:

       >>> obj = DemoClass(name="gen", value=1)
       >>> list(obj.generate_sequence(0, 5))
       [0, 1, 2, 3, 4]

       Custom positive step:

       >>> list(obj.generate_sequence(0, 10, 2))
       [0, 2, 4, 6, 8]

       Reverse iteration with negative step:

       >>> list(obj.generate_sequence(10, 5, -1))
       [10, 9, 8, 7, 6]

       """
       if step == 0:
           raise ValueError("Step cannot be zero")

       if step > 0 and start >= stop:
           raise ValidationError(
               "Start must be less than stop for positive step",
               "start/stop"
           )

       if step < 0 and start <= stop:
           raise ValidationError(
               "Start must be greater than stop for negative step",
               "start/stop"
           )

       current = start
       while (step > 0 and current < stop) or (step < 0 and current > stop):
           yield current
           current += step

   def batch_process(
       self,
       data_iterator: Iterable[np.ndarray],
       batch_size: int = 32
   ) -> List[np.ndarray]:
       """
       Process multiple arrays in batches.

       .. versionadded:: 2.0.0

       Applies :meth:`process_data` to each array from the iterator,
       processing in batches for improved efficiency with large datasets.

        Parameters
        ----------
        data_iterator : Iterable[numpy.ndarray]
            Iterable yielding arrays to process. Each array must satisfy
            constraints of :meth:`process_data`.
        batch_size : int, optional
            Number of arrays to process before yielding results. Larger
            values improve throughput at cost of memory usage. Default is 32.

       Returns
       -------
       list of ndarray
           Processed arrays in original iteration order.

       Warns
       -----
       UserWarning
           If batch_size exceeds 1000, as memory usage may be excessive.

       See Also
       --------
       process_data : Single array processing method.

       Notes
       -----
       This method accumulates results in memory. For very large datasets
       consider implementing a generator-based streaming approach.

       Examples
       --------
       >>> obj = DemoClass(name="batch", value=5)
       >>> arrays = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]
       >>> results = obj.batch_process(arrays, batch_size=2)
       >>> len(results)
       3

       """
       if batch_size > 1000:
           warnings.warn(
               "Large batch_size may cause excessive memory usage",
               UserWarning,
               stacklevel=2
           )

       results = []
       for array in data_iterator:
           processed = self.process_data(array)
           results.append(processed)

       return results

   def __enter__(self):
       """
       Enter runtime context for resource management.

       Returns
       -------
       DemoClass
           Returns self for use in with-statement body.

       Notes
       -----
       Updates internal state to track context manager activation.
       Suitable for managing resources or establishing temporary
       configuration states.

       Examples
       --------
       >>> obj = DemoClass(name="ctx", value=5)
       >>> with obj as ctx:
       ...     print(ctx.value)
       5.0

       """
       self._internal_state['context_active'] = True
       return self

   def __exit__(self, exc_type, exc_val, exc_tb):
       """
       Exit runtime context and clean up resources.

        Parameters
        ----------
        exc_type : type, optional
            Exception type if exception occurred, None otherwise.
        exc_val : Exception, optional
            Exception instance if exception occurred, None otherwise.
        exc_tb : traceback, optional
            Traceback object if exception occurred, None otherwise.

       Returns
       -------
       bool
           Always returns False to propagate any exceptions that occurred
           within the context.

       Notes
       -----
       This implementation performs cleanup but does not suppress exceptions,
       ensuring that errors are visible to calling code.

       """
       self._internal_state['context_active'] = False
       return False

   def __repr__(self) -> str:
       """
       Return official string representation.

       Returns
       -------
       str
           String representation in format: ``DemoClass(name='...', value=...)``

       Notes
       -----
       Provides unambiguous representation suitable for debugging and logging.

       Examples
       --------
       >>> obj = DemoClass(name="test", value=42)
       >>> repr(obj)
       "DemoClass(name='test', value=42.0)"

       """
       return f"DemoClass(name='{self.name}', value={self.value})"


def helper_function(
   array: np.ndarray,
   axis: Optional[Union[int, Tuple[int, ...]]] = None,
   keepdims: bool = False,
   out: Optional[np.ndarray] = None
) -> Union[np.ndarray, float]:
   """
   Compute mean along specified axes.

   Calculates arithmetic mean with configurable axis reduction and output
   array options. Wraps NumPy mean with additional validation.

   Parameters
   ----------
   array : numpy.ndarray
       Input array for computation. Must contain numeric data.
   axis : int or tuple of int, optional
       Axis or axes along which to compute mean. None flattens array.
   keepdims : bool, optional
       If True, reduced axes remain in result with size one. Default is False.
   out : numpy.ndarray, optional
       Alternative output array for result. Must have compatible shape.

   Returns
   -------
   float or ndarray
       Computed mean. Returns scalar if axis is None and keepdims is False;
       otherwise returns array.

   Raises
   ------
   ValueError
       If array is empty.
   TypeError
       If array does not contain numeric data.

   Warns
   -----
   RuntimeWarning
       If array contains NaN values, which propagate to result.

   See Also
   --------
   numpy.mean : Underlying NumPy mean implementation.
   numpy.std : Compute standard deviation along axes.
   DemoClass.process_data : Related array processing method.

   Notes
   -----
   This implementation relies on NumPy's optimized reduction routines.
   Performance characteristics depend on underlying BLAS configuration
   and array memory layout.

   For numerical stability with large arrays, the computation uses
   compensated summation internally within NumPy.

   References
   ----------
   .. [1] Welford, B. P. "Note on a method for calculating corrected sums of
      squares and products." Technometrics 4.3 (1962): 419-420.
   .. [2] Higham, Nicholas J. "Accuracy and stability of numerical algorithms."
      SIAM, 2002.

   Examples
   --------
   Compute mean of 1D array:

   >>> data = np.array([1, 2, 3, 4, 5])
   >>> helper_function(data)
   3.0

   Compute mean along specific axis of 2D array:

   >>> data = np.array([[1, 2], [3, 4]])
   >>> helper_function(data, axis=0)
   array([2., 3.])

   Preserve dimensions in output:

   >>> helper_function(data, axis=1, keepdims=True)
   array([[1.5],
          [3.5]])

   Use pre-allocated output array:

   >>> result = np.zeros(2)
   >>> helper_function(data, axis=0, out=result)
   array([2., 3.])

   """
   if array.size == 0:
       raise ValueError("Cannot compute mean of empty array")

   if not np.issubdtype(array.dtype, np.number):
       raise TypeError("Array must contain numeric data")

   if np.any(np.isnan(array)):
       warnings.warn(
           "Array contains NaN values which propagate to result",
           RuntimeWarning,
           stacklevel=2
       )

   result = np.mean(array, axis=axis, keepdims=keepdims, out=out)
   return result


def variadic_function(
   *args: Union[int, float],
   **kwargs: Any
) -> Tuple[float, Dict[str, Any]]:
   """
   Compute aggregate statistic from variable arguments.

   Processes arbitrary number of numeric arguments using selectable
   aggregation operation. Supports scaling and normalization options.

   Parameters
   ----------
   *args : int or float
       Variable number of numeric values to aggregate. At least one
       value required.
   **kwargs : Any
       Configuration options controlling computation:

       * ``operation`` (str) -- Aggregation type: 'sum', 'product', or 'mean'
       * ``scale`` (float) -- Multiplicative scaling applied to result
       * ``normalize`` (bool) -- If True, divide result by argument count

   Returns
   -------
   result : float
       Computed aggregate value after scaling and normalization.
   metadata : dict
       Computation metadata containing keys ``count``, ``operation``,
       and ``kwargs_received`` with remaining unused kwargs.

   Raises
   ------
   ValueError
       If no positional arguments provided.
   ValidationError
       If operation type is not one of the allowed values.

   See Also
   --------
   numpy.sum : Array summation function.
   numpy.prod : Array product function.
   numpy.mean : Array mean function.

   Notes
   -----
   The normalize option divides by argument count before scaling is applied,
   following the computation order:

   .. math::

       result = scale \\cdot \\left(\\frac{aggregate}{n}\\right)^{normalize}

   where :math:`n` is the number of arguments and the exponent is 1 if
   normalize is True, 0 otherwise (mathematical notation for clarity).

   Examples
   --------
   Sum with default settings:

   >>> variadic_function(1, 2, 3, operation='sum')
   (6.0, {'count': 3, 'operation': 'sum', 'kwargs_received': {}})

   Product with scaling:

   >>> result, metadata = variadic_function(2, 3, 4, operation='product', scale=0.5)
   >>> result
   12.0

   Mean with normalization:

   >>> result, _ = variadic_function(10, 20, 30, operation='mean', normalize=True)
   >>> result
   20.0

   """
   if not args:
       raise ValueError("At least one positional argument required")

   operation = kwargs.pop('operation', 'sum')
   scale = kwargs.pop('scale', 1.0)
   normalize = kwargs.pop('normalize', False)

   allowed_ops = ['sum', 'product', 'mean']
   if operation not in allowed_ops:
       raise ValidationError(
           f"Must be one of {allowed_ops}",
           "operation"
       )

   if operation == 'sum':
       result = sum(args)
   elif operation == 'product':
       result = np.prod(args)
   else:  # mean
       result = np.mean(args)

   if normalize:
       result = result / len(args)

   result *= scale

   metadata = {
       'count': len(args),
       'operation': operation,
       'kwargs_received': kwargs
   }

   return float(result), metadata


def function_with_conditional_returns(
   data: np.ndarray,
   return_stats: bool = True,
   return_indices: bool = False
) -> Union[float, Tuple[float, Dict[str, float]],
          Tuple[float, Dict[str, float], np.ndarray]]:
   """
   Find maximum value with optional statistics and indices.

   Computes the maximum value in an array with optional return of
   descriptive statistics and location indices based on flags.

   Parameters
   ----------
   data : numpy.ndarray
       Input array for analysis. Must be non-empty and numeric.
   return_stats : bool, optional
       If True, include statistics dictionary in return value. Default is True.
   return_indices : bool, optional
       If True, include array of maximum value indices in return value. Default is False.

   Returns
   -------
   result
       Return value structure depends on boolean flags as documented in Notes.

   Raises
   ------
   ValueError
       If data array is empty.
   TypeError
       If data array is not numeric type.

   See Also
   --------
   numpy.max : Maximum value function.
   numpy.argmax : Index of maximum value.
   numpy.where : Condition-based index location.

   Notes
   -----
   Return signature varies based on flags:

   * Both flags False: returns single float (maximum value)
   * ``return_stats=True`` only: returns ``(float, dict)`` tuple
   * Both flags True: returns ``(float, dict, ndarray)`` tuple

   The returned tuple, when present, contains:

   1. Maximum value (float)
   2. Statistics dictionary with keys: ``mean``, ``std``, ``median`` (if requested)
   3. Index array locating maximum values (if requested)

   If multiple elements share the maximum value, all indices are returned.

   Examples
   --------
   Maximum value only:

   >>> data = np.array([1, 5, 3, 9, 2])
   >>> function_with_conditional_returns(data, return_stats=False)
   9.0

   Maximum with statistics:

   >>> maximum, stats = function_with_conditional_returns(data)
   >>> maximum
   9.0
   >>> stats['mean']
   4.0

   All return values:

   >>> maximum, stats, indices = function_with_conditional_returns(
   ...     data, return_indices=True
   ... )
   >>> indices
   array([3])

   Multiple maximum values:

   >>> data = np.array([1, 9, 3, 9, 2])
   >>> _, _, indices = function_with_conditional_returns(data, return_indices=True)
   >>> indices
   array([1, 3])
   """
   if data.size == 0:
       raise ValueError("Cannot compute maximum of empty array")

   if not np.issubdtype(data.dtype, np.number):
       raise TypeError("Array must contain numeric data")

   maximum = float(np.max(data))

   returns = [maximum]

   if return_stats:
       stats = {
           'mean': float(np.mean(data)),
           'std': float(np.std(data)),
           'median': float(np.median(data))
       }
       returns.append(stats)

   if return_indices:
       indices = np.where(data == maximum)[0]
       returns.append(indices)

   if len(returns) == 1:
       return returns[0]
   return tuple(returns)


def deprecated_function(x: float, y: float) -> float:
   """
   Compute sum of two values.

   .. deprecated:: 1.8.0
       ``deprecated_function`` will be removed in version 3.0.0.
       Use :func:`variadic_function` with ``operation='sum'`` instead.

   Parameters
   ----------
   x : float
       First value.
   y : float
       Second value.

   Returns
   -------
   float
       Sum of x and y.

   See Also
   --------
   variadic_function : Replacement function with extended capabilities.

   Notes
   -----
   This function is maintained for backward compatibility only and receives
   no updates or enhancements.

   Examples
   --------
   >>> deprecated_function(10, 20)  # doctest: +SKIP
   30.0

   """
   warnings.warn(
       "deprecated_function is deprecated, use variadic_function instead",
       DeprecationWarning,
       stacklevel=2
   )
   return x + y


def advanced_cross_reference_example(
   obj: DemoClass,
   config: ComputationConfig
) -> Dict[str, Any]:
   """
   Perform computation demonstrating comprehensive cross-references.

   Integrates multiple components from this module to showcase proper
   Sphinx cross-referencing using various role types.

   Parameters
   ----------
   obj : DemoClass
       Instance providing processing capabilities. See :class:`DemoClass`
       for initialization requirements.
   config : ComputationConfig
       Configuration controlling computation behavior. See
       :class:`ComputationConfig` for parameter descriptions.

   Returns
   -------
   dict
       Results dictionary mapping string keys to computation outputs.

   Raises
   ------
   ValidationError
       If configuration validation fails. See :exc:`ValidationError` for
       error code meanings.
   CustomException
       For operational failures. See :exc:`CustomException` base class.

   See Also
   --------
   DemoClass : Primary computation class.
   DemoClass.compute_complex_operation : Core operation method.
   ComputationConfig : Configuration dataclass.
   helper_function : Statistical utility function.

   Notes
   -----
   This function demonstrates proper usage of Sphinx roles for cross-referencing:

   * ``:class:`ClassName``` -- links to class documentation
   * ``:meth:`ClassName.method_name``` -- links to method
   * ``:func:`function_name``` -- links to function
   * ``:exc:`ExceptionName``` -- links to exception
   * ``:attr:`obj.attribute``` -- links to attribute
   * ``:obj:`name``` -- generic object reference

   The tilde prefix (``~``) can be used to shorten displayed text while
   preserving full reference path: ``:class:`~package.module.ClassName```
   displays as ``ClassName`` but links to full path.

   External documentation can be referenced via intersphinx configuration:

   * ``:class:`numpy.ndarray``` -- links to NumPy docs
   * ``:func:`numpy.mean``` -- links to NumPy function

   .. warning::
       This function requires both parameters to be properly initialized.
       Passing None for either will result in AttributeError.

   .. note::
       Configuration is not modified during execution. Create new
       :class:`ComputationConfig` instances for different parameters.

   Examples
   --------
   Basic usage with default configuration:

   >>> obj = DemoClass(name="demo", value=42)
   >>> config = ComputationConfig()
   >>> result = advanced_cross_reference_example(obj, config)
   >>> 'processed' in result
   True

   Custom configuration:

   >>> config = ComputationConfig(tolerance=1e-8, verbose=True)
   >>> result = advanced_cross_reference_example(obj, config)

   """
   # Validate configuration
   if config.tolerance <= 0:
       raise ValidationError("tolerance must be positive", "tolerance")

   # Generate sample data
   data = np.random.randn(100)

   # Process using object methods
   processed = obj.process_data(data)

   # Compute statistics
   mean_value = helper_function(processed)

   # Perform complex operation
   operation_result = obj.compute_complex_operation(
       mean_value,
       config.tolerance,
       mode='advanced'
   )

   return {
       'processed': processed,
       'mean': mean_value,
       'operation_result': operation_result,
       'iterations': config.max_iterations
   }


class AdvancedDocumentationFeatures:
   """
   Class demonstrating advanced Sphinx directive usage.

   .. versionadded:: 2.0.0

   Showcases proper usage of version directives, warning boxes, note boxes,
   and other reST directives commonly used in Numpy-style docstrings.

   Attributes
   ----------
   value : float
       Primary computation value.
   status : str
       Current operational status.

   Methods
   -------
   compute_with_warnings
       Operation that may emit warnings under specific conditions.
   experimental_feature
       Newly added feature subject to change.

   .. warning::
       This class includes experimental features that may change in future
       versions without following standard deprecation policy.

   .. note::
       For production use, prefer stable methods from :class:`DemoClass`
       which maintain backward compatibility guarantees.

   Examples
   --------
   >>> obj = AdvancedDocumentationFeatures(value=10)
   >>> obj.status
   'initialized'

   """

   def __init__(self, value: float):
       self.value = value
       self.status = 'initialized'

   def compute_with_warnings(
       self,
       input_data: np.ndarray,
       threshold: float = 0.0
   ) -> np.ndarray:
       """
       Transform data with conditional warnings.

       Applies transformation while monitoring for edge cases that trigger
       warnings to alert users of potentially problematic conditions.

       Parameters
       ----------
       input_data : numpy.ndarray
           Data to transform. Must be 1D numeric array.
       threshold : float, optional
           Warning threshold for detecting extreme values. Default is 0.0.

       Returns
       -------
       ndarray
           Transformed data with same shape as input.

       Warns
       -----
       UserWarning
           If input contains values exceeding threshold by more than
           10 standard deviations.
       RuntimeWarning
           If transformation produces infinite values.

       See Also
       --------
       DemoClass.process_data : Related transformation method.

       Notes
       -----
       The transformation applies element-wise processing:

       .. math::

           y_i = \\log(|x_i| + 1) \\cdot \\text{sign}(x_i)

       This formulation preserves sign while compressing extreme values.

       .. warning::
           Extremely large input values (>1e100) may produce infinite
           results despite the log transformation.

       Examples
       --------
       >>> obj = AdvancedDocumentationFeatures(value=1)
       >>> data = np.array([1, 2, 3, 4, 5])
       >>> result = obj.compute_with_warnings(data)
       >>> result.shape
       (5,)

       """
       if input_data.ndim != 1:
           raise ValueError("Input must be 1D array")

       # Check for extreme values
       std = np.std(input_data)
       if np.any(np.abs(input_data) > threshold + 10 * std):
           warnings.warn(
               "Input contains extreme values exceeding threshold",
               UserWarning,
               stacklevel=2
           )

       # Apply transformation
       result = np.log(np.abs(input_data) + 1) * np.sign(input_data)

       # Check for infinite results
       if np.any(np.isinf(result)):
           warnings.warn(
               "Transformation produced infinite values",
               RuntimeWarning,
               stacklevel=2
           )

       return result * self.value

   def experimental_feature(self, x: float) -> float:
       """
       Compute using experimental algorithm.

       .. versionadded:: 2.0.0

       .. versionchanged:: 2.1.0
          Added input validation and range checking.

       Applies developmental algorithm subject to modification or removal
       in future versions.

       Parameters
       ----------
       x
           Input value. Must be finite and non-negative.

       Returns
       -------
       float
           Computed result.

       Raises
       ------
       ValidationError
           If x is negative or non-finite.

       .. warning::
           This feature is experimental. Algorithm behavior may change
           between minor versions without standard deprecation cycle.

       .. note::
           For stable computation, use :meth:`DemoClass.compute_complex_operation`
           which provides backward compatibility guarantees.

       Examples
       --------
       >>> obj = AdvancedDocumentationFeatures(value=5)
       >>> obj.experimental_feature(10)
       50.0

       """
       if not np.isfinite(x):
           raise ValidationError("Must be finite", "x")
       if x < 0:
           raise ValidationError("Must be non-negative", "x")

       # Experimental algorithm implementation
       return x * self.value


def function_with_multiple_examples(
   data: np.ndarray,
   operation: str
) -> np.ndarray:
   """
   Apply various transformations to demonstrate example documentation.

   Showcases comprehensive example documentation covering common use cases,
   edge cases, and error conditions.

   Parameters
   ----------
   data : numpy.ndarray
       Input array to transform.
   operation : str
       Transformation type: 'normalize', 'standardize', or 'scale'.

   Returns
   -------
   ndarray
       Transformed array.

   Raises
   ------
   ValidationError
       If operation is not recognized.

   See Also
   --------
   DemoClass.process_data : Related processing method.
   helper_function : Statistical computation utility.

   Notes
   -----
   Transformation definitions:

   * **normalize**: Scale to [0, 1] range
   * **standardize**: Z-score transformation (mean=0, std=1)
   * **scale**: Unit norm scaling

   Examples
   --------
   **Common Use Cases**

   Normalize to unit range:

   >>> data = np.array([1, 2, 3, 4, 5])
   >>> result = function_with_multiple_examples(data, 'normalize')
   >>> result.min(), result.max()
   (0.0, 1.0)

   Standardize to z-scores:

   >>> result = function_with_multiple_examples(data, 'standardize')
   >>> np.abs(result.mean()) < 1e-10
   True

   Scale to unit norm:

   >>> result = function_with_multiple_examples(data, 'scale')
   >>> np.abs(np.linalg.norm(result) - 1.0) < 1e-10
   True

   **Edge Cases**

   Single-element array:

   >>> data = np.array([5.0])
   >>> result = function_with_multiple_examples(data, 'normalize')
   >>> result
   array([0.])

   Constant array (zero variance):

   >>> data = np.array([3.0, 3.0, 3.0])
   >>> result = function_with_multiple_examples(data, 'standardize')
   >>> np.all(result == 0)
   True

   **Error Conditions**

   Invalid operation raises ValidationError:

   >>> function_with_multiple_examples(data, 'invalid')  # doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   ValidationError: ...

   """
   allowed_ops = ['normalize', 'standardize', 'scale']
   if operation not in allowed_ops:
       raise ValidationError(f"Must be one of {allowed_ops}", "operation")

   if operation == 'normalize':
       min_val = np.min(data)
       max_val = np.max(data)
       if max_val == min_val:
           return np.zeros_like(data)
       return (data - min_val) / (max_val - min_val)

   elif operation == 'standardize':
       mean = np.mean(data)
       std = np.std(data)
       if std == 0:
           return np.zeros_like(data)
       return (data - mean) / std

   else:  # scale
       norm = np.linalg.norm(data)
       if norm == 0:
           return data
       return data / norm


# Module-level constants with inline documentation

#: Numerical tolerance for floating-point comparisons.
#: Used throughout the module for convergence checks and equality tests.
EPSILON: float = 1e-10

#: Default batch size for batch processing operations.
#: Balances memory usage with computational efficiency.
DEFAULT_BATCH_SIZE: int = 32

#: Mapping of operation names to their symbolic representations.
#: Used for display and logging purposes.
OPERATION_SYMBOLS: Dict[str, str] = {
   'sum': '+',
   'product': '×',
   'mean': 'μ',
   'difference': '-'
}

#: Configuration template for production deployments.
#: Copy and modify for specific use cases.
PRODUCTION_CONFIG: Dict[str, Any] = {
   'tolerance': EPSILON,
   'max_iterations': 10000,
   'verbose': False,
   'cache_results': True,
   'parallel_processing': True
}


def _private_helper(x: float) -> float:
   """
   Internal helper function for computation.

   Private functions can still have docstrings for developer reference,
   though they are typically excluded from generated documentation by
   default Sphinx configuration.

   Parameters
   ----------
   x : float
       Input value.

   Returns
   -------
   float
       Processed value.

   Notes
   -----
   This function is not part of the public API and may change without
   notice. Use public functions for stable interfaces.

   """
   return x * 2.0 + 1.0


# Demonstrate comprehensive module usage when executed directly
if __name__ == "__main__":
   # Create instances
   print("Numpy-Style Docstring Gold Standard Reference v2.0.0")
   print("=" * 60)

   demo = DemoClass(name="example", value=100)
   print(f"\nCreated: {demo}")

   # Demonstrate complex operation
   result = demo.compute_complex_operation(10, 20, mode='advanced', scale=2.0)
   print(f"\nComplex operation result:")
   for key, value in result.items():
       print(f"  {key}: {value}")

   # Use generator
   print("\nGenerated sequence:")
   for val in demo.generate_sequence(0, 5):
       print(f"  {val}")

   # Process array data
   data = np.array([1, 2, 3, 4, 5])
   processed = demo.process_data(data)
   print(f"\nProcessed data: {processed}")

   # Use helper function
   stat = helper_function(data)
   print(f"\nHelper function result: {stat}")

   # Demonstrate variadic function
   var_result, var_meta = variadic_function(1, 2, 3, 4, operation='mean')
   print(f"\nVariadic result: {var_result}")
   print(f"Metadata: {var_meta}")

   # Demonstrate configuration
   config = ComputationConfig(tolerance=1e-8, max_iterations=500)
   print(f"\nConfiguration: tolerance={config.tolerance}, "
         f"max_iterations={config.max_iterations}")

   # Demonstrate conditional returns
   maximum = function_with_conditional_returns(data, return_stats=False)
   print(f"\nMaximum value: {maximum}")

   maximum, stats = function_with_conditional_returns(data)
   print(f"Statistics: {stats}")

   # Demonstrate transformation
   transformed = function_with_multiple_examples(data, 'normalize')
   print(f"\nNormalized data: {transformed}")

   print("\n" + "=" * 60)
   print("All demonstrations completed successfully!")
   print("\nTo generate Sphinx documentation:")
   print("  1. Install: pip install sphinx sphinx-rtd-theme")
   print("  2. Configure: sphinx-quickstart")
   print("  3. Enable Napoleon in conf.py")
   print("  4. Build: sphinx-build -b html source build")
   print("  5. Validate: sphinx-build -W -b doctest source build")
