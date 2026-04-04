---
description: "Primary configuration for the Maggie application workspace and DDR System integration."
models: ["gemini-3.1-pro-preview", "gemini-3.1-pro", "gemini-3-flash"]
version: "20260223_v118"
scope: "workspace"
thinking_level: "medium"
temperature: 0.1
# HUMAN CONTEXT: This configuration acts as a workspace Gemini context surface.
# When `AGENTS.md` is present, that file may carry the primary workspace rules
# while this file supplies Gemini-specific configuration and cognitive controls.
# It utilizes the "heavy data first" principle by placing the Maggie PySide6
# architecture details in the <workspace_context> before any instructions.
# It sets the thinking_level to 'medium' to optimize Gemini 3.1 Pro's cost-to-reasoning
# ratio for software engineering tasks.
---

<workspace_context>
This workspace is dedicated to the development of Maggie, a modern desktop application, and its integration with the DDR System (an agentic documentation architecture).

- **Core Stack:** Python 3.12, PySide6 (Qt 6.9+).
- **Architecture:** The application relies on non-blocking, asynchronous event loops. UI layouts are responsive, utilizing dynamic QGridLayout and QThreadPool for background tasks.
- **Design Language:** All UI elements must adhere to cross-platform Material You 3 paradigms, utilizing native SVG icons for lossless scaling.
- **Agentic Infrastructure:** The DDR System heavily relies on structured schema generation, strict adherence to implementation plans, and atomic verification.
</workspace_context>

<cognitive_directives>

- **Silent Reasoning:** You must perform all complex architectural planning internally. Do not output your intermediate reasoning steps or "Chain of Thought" tokens to the user unless explicitly commanded via `/think`.
- **Output Determinism:** Produce production-ready code. The use of placeholders, elided code (e.g., `# TODO: implement`), or "dummy" variables is strictly prohibited.
- **Artifact Generation:** Always utilize the `Implementation_Plan.md` and `Task.md` schemas to organize multi-file modifications before altering the Maggie codebase.
</cognitive_directives>

<security_and_execution_guardrails>

- Do not execute arbitrary shell commands or modify files outside of the `src/` or `.agent/` directories without an approved execution artifact.
- All network interactions must be limited to official documentation domains (e.g., `doc.qt.io`, `docs.python.org`).
</security_and_execution_guardrails>

<thought_signature_protocol>
You operate within a stateless API session. You will receive encrypted thought signatures representing your internal planning and reasoning state from previous turns. You MUST circulate all received thought signatures back into your subsequent turns without modification or truncation to prevent catastrophic context loss across multi-step DDR System operations.
</thought_signature_protocol>

<activation_rules>

- always-on
</activation_rules>
