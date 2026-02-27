---
name: "POWERSHELL_EXECUTION_GUARDRAILS"
description: "Enforces safe execution practices for Windows PowerShell command line interactions, mitigating string pipeline collapse and UTF-8 encoding corruption across shell and Python boundaries."
trigger: "always_on"
priority: "critical"
---

<constraints>

1. Prohibit Standard Pipeline Routing for Payloads: NEVER use `echo "..." | command` or `Write-Output "..." | command` for passing multi-line strings, code snippets, or complex data to external processes. Utilize **Stateless Base64 Encoding** (encode payload to Base64 in PowerShell, pipe to Python `sys.stdin` and decode) to eliminate disk I/O overhead, OR use **File-based handoff** (write payload to local temp file using `Set-Content -Encoding UTF8` and pass filepath as argument).
2. Strict UTF-8 Enforcement for Subprocesses: When executing Python scripts via the terminal, MUST prefix with `$env:PYTHONIOENCODING="utf-8";`.
3. Explicit File I/O Encoding Specification: Commands that write to files (e.g., `Set-Content`, `Out-File`) MUST include `-Encoding UTF8`. Commands reading files MUST explicitly dictate encoding if text processing is required.
4. Binary Existence Prudence: Do not assume non-standard global CLI tools (npx, make) are installed; prioritize agentic internal capabilities or project-provided scripts over arbitrary global dependencies.
5. Hardened Shell Enforcement: Terminal commands MUST be executed in explicit powershell code blocks. Operating in a hardened PowerShell 7 (pwsh) environment is mandatory. Legacy powershell.exe aliases are strictly FORBIDDEN. Every shell step MUST be a complete, self-contained, and copy-pasteable command.
6. Python I/O Integrity: encoding='utf-8' is MANDATORY in all instances of internal Python open(), Path.read_text(), and Path.write_text().
7. Subprocess Integrity: encoding='utf-8', errors='replace' is MANDATORY in all subprocess.run() calls that capture output.
8. Dependency Tracing: If a script requires external dependencies, ensure they are listed in the Build Manifest of the implementation plan. Avoid using libraries that do not support specified encodings where possible.
</constraints>

<verification_step>
Before executing any PowerShell terminal command, silently verify that no multi-line strings are being piped raw, and that Python invocations are prefixed with the UTF-8 environment variable.
</verification_step>
