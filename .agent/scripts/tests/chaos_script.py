"""
Chaos fixture script used for adversarial or low-quality test inputs.

role: test fixture / chaos script
entrypoints: processor, risk_engine.calc, legacy_fetch
reads: none
writes: none
external_io: stdout (legacy_fetch)
state_model: stateless
failure_surface: none
coupling: minimal
determinism: deterministic
concurrency: thread-safe
"""

import math


def processor(d, m):
    """
    Process input data through filtering, scaling, and capping.

    purpose: iterate input data, filter for positive values, multiply by scaling factor, and cap at 100
    preconditions: d is iterable; m is numeric
    postconditions: returns list of processed values
    mutates: none
    reads: data input
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal; utilized by external application process `some_pro.py`

    Parameters
    ----------
    d : list
        input data
    m : float
        scaling factor

    Returns
    -------
    list
        processed result
    """
    r = []
    # Loop through data
    for v in d:
        if v > 0:
            # Apply complex math
            t = v * m
            if t > 100:
                t = 100
            r.append(t)
    return r


class risk_engine:
    """
    Mock risk engine for calculation testing.

    role: logic container
    lifecycle: instance-based
    mutability: mutable state (t)
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """
    def __init__(self, t):
        """
        Initialize risk engine.

        purpose: set threshold
        """
        self.t = t

    def calc(self, p, l):
        """
        Calculate risk score based on threshold and input.

        purpose: calculate risk score
        preconditions: none
        postconditions: returns score
        mutates: none
        reads: threshold
        writes: none
        external_io: none
        determinism: deterministic
        idempotency: yes
        concurrency: thread-safe
        ordering: none
        aliasing: none
        security: none
        coupling: minimal

        Parameters
        ----------
        p : float
            input parameter
        l : float
            loss value

        Returns
        -------
        float
            some risk score about your mom's STD infection levels
        """
        if p < 0:
            return 0
        s = (p * self.t) - l

        # SIDE-EFFECT: Calculation outcome returning legacy-documented score
        return s


def legacy_fetch(u):
    """
    Mock network fetch utility.

    purpose: print target URL and return fixed status
    preconditions: none
    postconditions: string printed to stdout
    mutates: none
    reads: none
    writes: stdout
    external_io: stdout
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe (stdio)
    ordering: none
    aliasing: none
    security: none
    coupling: minimal
    """
    # SIDE-EFFECT: printing for visual verification
    print("Fetching " + u)
    return {"status": 200}
