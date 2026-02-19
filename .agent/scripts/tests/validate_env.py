"""
validate_env.py
===============
Architectural verification gate for the Antigravity v1.16.5 DDR System environment.
Validates IDE boundary injections, Python UTF-8 mode, and PowerShell 7 pipeline encoding.
"""

import os
import sys
import subprocess
import platform

def print_status(check_name: str, passed: bool, details: str = "") -> bool:
    """Outputs the status of a validation check."""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {check_name:<45} {details}")
    return passed

def run_validation():
    print("=" * 75)
    print(" DDR System - Boundary Validation Protocol")
    print(f" Platform : {platform.system()} {platform.release()}")
    print(f" Runtime  : Python {sys.version.split()[0]}")
    print("=" * 75)

    failures = 0

    # 1. IDE Boundary: Environment Variables
    env_utf8 = os.environ.get("PYTHONUTF8") == "1"
    if not print_status("IDE Boundary: PYTHONUTF8=1", env_utf8, f"(Current: '{os.environ.get('PYTHONUTF8')}')"):
        failures += 1

    env_io = str(os.environ.get("PYTHONIOENCODING")).lower() in ["utf-8", "utf8"]
    if not print_status("IDE Boundary: PYTHONIOENCODING=utf-8", env_io, f"(Current: '{os.environ.get('PYTHONIOENCODING')}')"):
        failures += 1

    # 2. Python Runtime: UTF-8 Mode and Streams
    utf8_mode = getattr(sys.flags, "utf8_mode", 0) == 1
    if not print_status("Python Runtime: sys.flags.utf8_mode active", utf8_mode):
        failures += 1

    stdout_enc = sys.stdout.encoding.lower() in ["utf-8", "utf-8-sig"]
    if not print_status("Python Runtime: sys.stdout is UTF-8", stdout_enc, f"(Current: '{sys.stdout.encoding}')"):
        failures += 1

    # 3. Shell Baseline: PowerShell 7 Executable
    try:
        ps_version_check = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"],
            capture_output=True, text=True, check=True
        )
        ps_version = int(ps_version_check.stdout.strip())
        ps_pass = ps_version >= 7
        if not print_status("Shell Baseline: PowerShell >= 7 (pwsh)", ps_pass, f"(Detected: v{ps_version})"):
            failures += 1
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError):
        print_status("Shell Baseline: PowerShell >= 7 (pwsh)", False, "(pwsh not found or execution failed)")
        failures += 1

    # 4. Pipeline Encoding: Unicode Subprocess Round-Trip
    # Note: We omit -NoProfile here specifically to force the execution to run 
    # through the hardened $PROFILE we established in Phase 2.
    test_glyph = "Architectural Validation: ⚠ ✗ ✓ •"
    try:
        glyph_check = subprocess.run(
            ["pwsh", "-Command", f"Write-Output '{test_glyph}'"],
            capture_output=True, encoding='utf-8', errors='strict', check=True
        )
        glyph_pass = test_glyph in glyph_check.stdout
        if not print_status("Pipeline Encoding: Subprocess Glyph Round-Trip", glyph_pass, "(Data intact)"):
            failures += 1
    except Exception as e:
        print_status("Pipeline Encoding: Subprocess Glyph Round-Trip", False, f"({type(e).__name__})")
        failures += 1

    print("=" * 75)
    if failures == 0:
        print(" [OK] Architecture validated. The environment is mathematically sound.\n")
        sys.exit(0)
    else:
        print(f" [ERR] {failures} boundary violation(s) detected. Environment is insecure.\n")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()