---
type: tool
name: "generate_uuid"
description: "Generates a Version 4 Universally Unique Identifier (UUID) string."
command: "& \"${workspaceFolder}/.venv/Scripts/python.exe\" \"${workspaceFolder}/.agent/scripts/generate_uuid.py\""
runtime: system
confirmation: never
args: {}
---

# Tool: Generate UUID

Generates a single, random Version 4 UUID string.
This output is primarily intended to be captured by a Workflow to create transient, unique subfolders within the `.agent/.sandbox/` directory, ensuring concurrency safety between parallel agent tasks.

## Configuration
- **Script Path**: `.agent/scripts/generate_uuid.py`
- **Interpreter**: `${workspaceFolder}/.venv/Scripts/python.exe`
- **Timeout**: 5s

## Input Schema
This tool accepts no input arguments.

## Invocation

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/generate_uuid.py"
```

## Exit Codes & Interpretation
| Code | Status | Agent Interpretation |
|:----:|:-------|:---------------------|
| **0** | **SUCCESS** | A valid UUID string was output to stdout. Capture this string for use in subsequent workflow steps. |
| **1** | **ERROR** | System failure in generating randomness. Do not proceed with tasks requiring unique paths. |

## Operational Protocol
1.  **Usage Context:** Use this tool at the beginning of any workflow that requires writing temporary files.
2.  **Path Construction:** Combine the output string with the sandbox root to create safe paths.
    * *Example Pattern:* `.agent/.sandbox/task-<UUID_OUTPUT>/`
3.  **Capture Output:** Ensure the workflow step executing this tool is configured to capture standard output into a variable.

## Example Usage (Workflow Context)
*Note: This tool is rarely called interactively by a human. It is usually invoked within a workflow step to capture its output variable.*

```yaml
# Example Workflow Step defining variable capture
- id: get_run_id
  name: Generate Unique Run ID
  action: execute_tool
  tool: /generate_uuid
  # The output UUID is now available as ${get_run_id.output}
```
