---
name: global-security-guardrails
description: Enforces absolute security boundaries, network access restrictions, and credential protection protocols across all agentic workflows.
trigger: always_on
priority: critical
# HUMAN CONTEXT: This Security Policy is formatted as a Rule asset with 'critical'
# priority and 'always_on' activation. This guarantees the Antigravity semantic router
# permanently anchors these constraints to the end of the context window, allowing
# them to override any conflicting logic generated during dynamic workflows.
---

<forbidden_actions>

- **Credential Exposure:** Never generate, log, or embed hardcoded passwords, API keys, or access tokens within source code, test files, or artifact outputs.
- **Destructive Operations:** Do not utilize `os.system()`, `subprocess.run()`, or `shutil.rmtree()` to execute unverified shell commands or delete directories without explicit user confirmation via an artifact.
- **Data Exfiltration:** Do not write scripts that transmit local workspace data or environment variables to external telemetry or logging servers.
</forbidden_actions>

<allowed_domains>
If a workflow or skill requires documentation retrieval or API integration, you are strictly limited to the following whitelisted domains:

- `*.qt.io`
- `docs.python.org`
- `*.google.com`
- `github.com`
</allowed_domains>

<verification_step>
SILENT SECURITY AUDIT:
Before finalizing any code modification or terminal execution, you must internally parse your generated output against the `<forbidden_actions>` list. If any network requests are formulated, verify the target URL matches the `<allowed_domains>` regex exactly. If a violation is detected, you must silently purge the output and halt the workflow.
</verification_step>
