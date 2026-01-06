"""
UUID Generation Tool.

Generates a Version 4 Universally Unique Identifier (UUID).
This tool is primarily used by workflows to establish unique, non-colliding
sandbox directory names for parallel agent operations.

Meta
----
Tool Definition : .agent/tools/generate_uuid.mdt
Workflow Role   : Infrastructure / Concurrency Safety
Architect       : Antigravity IDE (Adversarial Lead)

Usage
-----
    python generate_uuid.py

Exit Codes
----------
0 : Success (UUID printed to stdout)
1 : Unexpected Error (Details printed to stderr)
"""

import sys
import uuid


def generate_uuid_v4() -> str:
    """
    Generate a random Version 4 UUID.

    Returns
    -------
    str
        The string representation of the UUID.
    """
    return str(uuid.uuid4())


def main() -> int:
    """
    CLI entry point for UUID generation.

    Prints the UUID to stdout if successful. Prints error message to stderr
    if an unexpected failure occurs.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    # No arguments expected.
    if len(sys.argv) > 1:
        print("Usage: python generate_uuid.py", file=sys.stderr)
        print("Error: This tool accepts no arguments.", file=sys.stderr)
        return 1

    try:
        uid_str = generate_uuid_v4()
        # Print ONLY the UUID string to stdout for easy capturing by workflows.
        print(uid_str, end="")
        return 0
    except Exception as e:
        # This catch-all is highly unlikely to be triggered by uuid4,
        # but defensive programming requires it for system stability.
        print(f"CRITICAL ERROR: Failed to generate UUID system randomness source: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
