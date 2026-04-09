---
name: "powershell-execution-guardrails"
version: "1.2.1"
description: "Always-on Windows PowerShell execution guardrails focused on PowerShell-native syntax, workspace-interpreter preference, safe quoting, tool fallback behavior, and UTF-8-safe shell I/O."
trigger: "always_on"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. PowerShell-Native Commands Only: On Windows, emit PowerShell syntax only. Do not use Bash heredocs (`<<`), `bash -lc`, `/dev/null`, or other Unix-only shell idioms. If a multiline stdin payload is needed, use a PowerShell here-string piped to the process, or write a UTF-8 temp file.
2. Quote Fragile Paths Explicitly: Any path containing spaces or parentheses MUST be quoted. PowerShell file cmdlets MUST use `-LiteralPath` when targeting a concrete path to avoid wildcard or parser surprises.
3. Verify Non-Core Tools Before Use: Before using `rg`, `ConvertFrom-Yaml`, `ruby`, `npx`, or any non-core executable or cmdlet, verify it with `Get-Command`. If it is unavailable, switch to a PowerShell-native or project-local alternative instead of retrying the missing tool.
4. First-Failure Search Fallback: Prefer `rg` for fast search only when it launches successfully. If `rg` is unavailable or fails to start, immediately fall back to `Get-ChildItem -Recurse -File` plus `Select-String` and do not keep retrying `rg`.
5. Keep Shell Steps Parser-Safe: Prefer short multi-statement PowerShell over dense regex-heavy one-liners. If quoting becomes fragile or the command needs multiple pipelines, move the payload into a PowerShell here-string or a small inline Python block.
6. Prefer the Workspace Interpreter: When `.venv/Scripts/python.exe` exists, invoke that interpreter path directly instead of relying on a bare `python` command. Do not assume the virtual environment is auto-activated.
7. Keep Text I/O UTF-8 Safe: Preserve `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` for Python subprocesses when encoding matters. PowerShell text writes MUST specify `-Encoding UTF8`.
8. Forbid Naked `python` When the Workspace Interpreter Is Known: If the repository-local interpreter path is known and exists, do not emit `python ...` as the primary invocation form. Use the explicit workspace path unless the task is intentionally validating PATH behavior.

</constraints>

<verification_step>
Before executing a PowerShell command, silently verify: the syntax is PowerShell-native; there is no Bash heredoc or Unix-only shell idiom; paths with spaces or parentheses are quoted and use `-LiteralPath` where applicable; non-core tools have been checked or replaced with a fallback; Python invocations prefer the workspace interpreter when it exists; multiline payloads use a here-string or UTF-8 file handoff; and the command is not an oversized parser-fragile one-liner.
</verification_step>
