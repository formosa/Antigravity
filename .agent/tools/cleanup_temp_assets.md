---
type: tool
name: "cleanup_temp_assets"
description: "Audits and optionally removes stale run directories under .agent/.temp."
command: "& \"${workspaceFolder}/.venv/Scripts/python.exe\" \"${workspaceFolder}/.agent/scripts/cleanup_temp_assets.py\""
runtime: system
confirmation: never
args: {}
---

# Tool: Cleanup Temp Assets

Audits the managed temp workspace under `.agent/.temp/` and reports:

1. Invalid directory names that do not match the run-directory convention
2. Empty run directories
3. Retained failure directories marked with `retained-on-failure.txt`
4. Stale non-retained run directories older than the configured age threshold

## Default Behavior

- The tool runs in dry-run mode by default.
- No directories are deleted unless the underlying script is invoked with explicit destructive flags.

## Configuration

- **Script Path**: `.agent/scripts/cleanup_temp_assets.py`
- **Interpreter**: `${workspaceFolder}/.venv/Scripts/python.exe`
- **Default Threshold**: `7` days
- **Managed Root**: `.agent/.temp/`

## Invocation

```powershell
& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/cleanup_temp_assets.py"
```

## Destructive Examples

```powershell
& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/cleanup_temp_assets.py" --delete-empty
& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/cleanup_temp_assets.py" --delete-stale --stale-days 14
& "${workspaceFolder}/.venv/Scripts/python.exe" "${workspaceFolder}/.agent/scripts/cleanup_temp_assets.py" --delete-retained
```

## Safety Contract

- The script refuses to delete anything outside `.agent/.temp/`.
- Retained failure directories are never deleted unless `--delete-retained` is explicitly supplied.
