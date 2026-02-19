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

## Execution Planning

Rules governing the generation of implementation plans:

- Never use descriptive or ambiguous placeholders (e.g., "run the script").
- All execution plans MUST contain explicit, verbatim command blocks.
- You MUST explicitly validate the existence of target files using the `Test-Path` cmdlet before attempting to execute Python scripts against them.
