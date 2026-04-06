"""
UUID Generation Tool producing Version 4 Universally Unique Identifiers.

role: infrastructure utility for establishing non-colliding sandbox names
entrypoints: generate_uuid_v4, main
reads: system randomness source
writes: stdout (UUID string)
external_io: none
state_model: stateless
failure_surface: entropy source exhaustion (rare)
coupling: minimal; depends on standard uuid library
determinism: nondeterministic
concurrency: thread-safe

Meta
----
Tool Definition : .agent/tools/generate_uuid.mdt
Workflow Role   : Infrastructure / Concurrency Safety
Architect       : Antigravity IDE (Adversarial Lead)
"""

import sys
import uuid


def generate_uuid_v4() -> str:
    """
    Generate a random Version 4 UUID.

    purpose: unique identifier generation
    preconditions: available system entropy
    postconditions: returns 36-character UUID string
    mutates: none
    reads: system randomness
    writes: none
    external_io: none
    determinism: nondeterministic
    idempotency: no
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: uses os.urandom via uuid.uuid4
    coupling: minimal

    Returns
    -------
    str
        randomly generated UUID v4 string
    """
    return str(uuid.uuid4())


def main() -> int:
    """
    CLI entry point for UUID generation.

    purpose: CLI interface for identifier generation
    preconditions: no arguments expected
    postconditions: UUID printed to stdout; exit code returned
    mutates: none
    reads: sys.argv
    writes: stdout
    external_io: none
    determinism: nondeterministic
    idempotency: no
    concurrency: process-local
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Returns
    -------
    int
        0 on success; 1 on unexpected error or argument presence
    """
    if len(sys.argv) > 1:
        print("Usage: python generate_uuid.py", file=sys.stderr)
        print("Error: This tool accepts no arguments.", file=sys.stderr)
        return 1

    try:
        uid_str = generate_uuid_v4()
        # Side-effect: print ONLY the UUID string to stdout for workflow consumption.
        print(uid_str, end="")
        return 0
    except Exception as e:
        # SIDE-EFFECT: defensive critical failure reporting
        print(f"CRITICAL ERROR: Failed to generate UUID system randomness source: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
