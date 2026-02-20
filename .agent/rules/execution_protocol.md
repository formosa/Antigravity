---
type: rule
name: execution_protocol
activation: always_on
priority: 100
severity: mandatory
description: "Strict protocols for shell (PowerShell 7) and Python execution (UTF-8 encoding)."
---
# Antigravity Agent Rules — DDR System Execution

## Shell Protocol

Rules governing shell execution within the Antigravity integrated terminal:

- All terminal commands MUST be executed in explicit `powershell` code blocks.
- You are operating in a hardened PowerShell 7 (`pwsh`) environment. Legacy `powershell.exe` aliases are strictly FORBIDDEN.
- Every shell step MUST be a complete, self-contained, and copy-pasteable command.

## Python Code Protocol

Rules governing Python file operations and external tool execution:

- `encoding='utf-8'` is MANDATORY in all instances of:
  - `open()`
  - `Path.read_text()`
  - `Path.write_text()`
- `encoding='utf-8', errors='replace'` is MANDATORY in all `subprocess.run()` calls that capture output.
- Avoid using libraries that do not support specified encodings where possible.
- If a script requires external dependencies, ensure they are listed in the `Build Manifest` of the implementation plan.

## Enforcement

- **Violation**: Non-UTF8 file operations or use of `powershell.exe`.
- **Severity**: FATAL
- **Action**: Halt execution and request explicit encoding fixes.