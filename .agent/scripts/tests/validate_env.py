"""
validate_env.py
===============
Validation gate for the Antigravity PowerShell execution baseline.
Checks PowerShell 7, UTF-8 defaults, Unicode subprocess round-trips,
and reports whether the packaged rg launcher is usable in this shell.
"""

import os
import platform
import subprocess
import sys


def print_status(check_name: str, passed: bool, details: str = "") -> bool:
    """Output a pass or fail line for a validation check."""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {check_name:<45} {details}")
    return passed


def print_warning(check_name: str, details: str = "") -> None:
    """Output a warning line for a non-fatal validation check."""
    print(f"[WARN] {check_name:<45} {details}")


def run_validation() -> None:
    """Execute the environment validation checks."""
    print("=" * 75)
    print(" Antigravity - PowerShell Execution Validation")
    print(f" Platform : {platform.system()} {platform.release()}")
    print(f" Runtime  : Python {sys.version.split()[0]}")
    print("=" * 75)

    failures = 0

    # 1. IDE Boundary: Environment Variables
    env_utf8 = os.environ.get("PYTHONUTF8") == "1"
    if not print_status(
        "IDE Boundary: PYTHONUTF8=1",
        env_utf8,
        f"(Current: '{os.environ.get('PYTHONUTF8')}')",
    ):
        failures += 1

    env_io = str(os.environ.get("PYTHONIOENCODING")).lower() in ["utf-8", "utf8"]
    if not print_status(
        "IDE Boundary: PYTHONIOENCODING=utf-8",
        env_io,
        f"(Current: '{os.environ.get('PYTHONIOENCODING')}')",
    ):
        failures += 1

    # 2. Python Runtime: UTF-8 Mode and Streams
    utf8_mode = getattr(sys.flags, "utf8_mode", 0) == 1
    if not print_status("Python Runtime: sys.flags.utf8_mode active", utf8_mode):
        failures += 1

    stdout_encoding = (sys.stdout.encoding or "").lower()
    stdout_enc = stdout_encoding in ["utf-8", "utf-8-sig"]
    if not print_status(
        "Python Runtime: sys.stdout is UTF-8",
        stdout_enc,
        f"(Current: '{sys.stdout.encoding}')",
    ):
        failures += 1

    # 3. Shell Baseline: PowerShell 7 Executable
    try:
        ps_version_check = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"],
            capture_output=True,
            text=True,
            check=True,
        )
        ps_version = int(ps_version_check.stdout.strip())
        ps_pass = ps_version >= 7
        if not print_status(
            "Shell Baseline: PowerShell >= 7 (pwsh)",
            ps_pass,
            f"(Detected: v{ps_version})",
        ):
            failures += 1
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError):
        print_status(
            "Shell Baseline: PowerShell >= 7 (pwsh)",
            False,
            "(pwsh not found or execution failed)",
        )
        failures += 1

    # 4. Pipeline Encoding: Unicode Subprocess Round-Trip
    test_glyph = "Architectural Validation: warning x check bullet"
    try:
        glyph_check = subprocess.run(
            ["pwsh", "-Command", f"Write-Output '{test_glyph}'"],
            capture_output=True,
            encoding="utf-8",
            errors="strict",
            check=True,
        )
        glyph_pass = test_glyph in glyph_check.stdout
        if not print_status(
            "Pipeline Encoding: Subprocess Round-Trip",
            glyph_pass,
            "(Data intact)",
        ):
            failures += 1
    except Exception as exc:  # pragma: no cover - diagnostic path
        print_status(
            "Pipeline Encoding: Subprocess Round-Trip",
            False,
            f"({type(exc).__name__})",
        )
        failures += 1

    # 5. Optional Tooling: rg launcher health
    try:
        rg_check = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", "rg --version"],
            capture_output=True,
            text=True,
            check=True,
        )
        first_line = (rg_check.stdout or "").splitlines()[0] if rg_check.stdout else ""
        print_status("Optional Tooling: rg launchability", True, first_line)
    except Exception as exc:  # pragma: no cover - diagnostic path
        print_warning(
            "Optional Tooling: rg launchability",
            f"({type(exc).__name__}) fallback to Get-ChildItem + Select-String",
        )

    print("=" * 75)
    if failures == 0:
        print(" [OK] Core PowerShell execution baseline validated.\n")
        sys.exit(0)

    print(f" [ERR] {failures} core validation failure(s) detected.\n")
    sys.exit(1)


if __name__ == "__main__":
    run_validation()
