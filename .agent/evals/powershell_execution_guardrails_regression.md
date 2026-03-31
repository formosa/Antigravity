# PowerShell Execution Guardrails Regression Cases

Use these cases to verify that the PowerShell guardrail keeps addressing the failure families found in local Codex session transcripts.

## Case Format

- Failure family
- Original bad command pattern
- Expected compliant pattern
- Expected fallback behavior

## CASE-001: `rg` Launcher Access Denied

- Failure family: launcher and packaging failure
- Original bad command pattern: `rg --files .agent`
- Expected compliant pattern: verify `rg` first, then use it only if it launches
- Expected fallback behavior: immediately switch to `Get-ChildItem -Recurse -File` plus `Select-String`; do not retry `rg` repeatedly

## CASE-002: Bash Heredoc in PowerShell

- Failure family: Unix shell syntax emitted in Windows PowerShell
- Original bad command pattern:

```powershell
python - <<'PY'
print("hello")
PY
```

- Expected compliant pattern:

```powershell
@'
print("hello")
'@ | python -
```

- Expected fallback behavior: if stdin piping becomes fragile, write a UTF-8 temp file and pass the file path instead

## CASE-003: Unquoted Path with Spaces or Parentheses

- Failure family: path parsing and command tokenization
- Original bad command pattern:

```powershell
Get-Content .agent\assets\proposals\active\v6\DDR System(v6.1).md
```

- Expected compliant pattern:

```powershell
Get-Content -LiteralPath '.agent\assets\proposals\active\v6\DDR System(v6.1).md'
```

- Expected fallback behavior: none; the command should be emitted correctly on first attempt

## CASE-004: Unsupported Optional Cmdlet

- Failure family: assuming a non-core PowerShell cmdlet exists
- Original bad command pattern:

```powershell
Get-Content file.yaml -Raw | ConvertFrom-Yaml
```

- Expected compliant pattern: check `Get-Command ConvertFrom-Yaml -ErrorAction SilentlyContinue` first
- Expected fallback behavior: use a project-local or Python-based YAML reader when the cmdlet is unavailable

## CASE-005: Unsupported External CLI

- Failure family: assuming a non-core external executable exists
- Original bad command pattern:

```powershell
ruby -e "require 'yaml'; puts YAML.load_file('file.yaml').keys"
```

- Expected compliant pattern: verify `ruby` with `Get-Command` before use
- Expected fallback behavior: use a PowerShell-native or Python-based alternative instead of retrying `ruby`

## CASE-006: Parser-Fragile One-Liner

- Failure family: oversized command with dense regex and multiple pipelines
- Original bad command pattern: a single PowerShell line combining recursive file discovery, regex extraction, object construction, and final formatting
- Expected compliant pattern: split the work into short statements, or move the regex payload into a here-string or inline Python block
- Expected fallback behavior: preserve PowerShell-native syntax while reducing quoting complexity and parser risk

## CASE-007: Fragile Regex Quoting in `rg`

- Failure family: regular expression quoting that breaks PowerShell parsing before `rg` runs
- Original bad command pattern: `rg -n '...content\', \'parent_ids\'...' file.yaml`
- Expected compliant pattern: use a PowerShell-safe quoted string or a here-string for the regex
- Expected fallback behavior: if the regex remains too fragile, switch to `Select-String` or break the search into smaller patterns
