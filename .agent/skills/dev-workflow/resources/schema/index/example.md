# Agent Tools Index

> Consolidated registry of tool assets in `.agent/tools/`.
>
> Scope: discovery, first-pass selection, and quick operational reference.
>
> Total tools: `3`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked tool definition, the linked tool definition is authoritative.

## Use This Index

1. Use the selection map to identify the best candidate by intent.
2. Use the manifest to confirm runtime, inputs, outputs, side effects, and safety posture.
3. Open the linked tool definition before execution when destructive behavior, output capture, or post-run validation matters.

## Selection Map

- `cleanup_temp_assets`: audit `.agent/.temp/`; optionally remove invalid, empty, stale, or retained-failure run directories when explicit deletion flags are used.
- `generate_uuid`: emit one UUIDv4 string to stdout for capture by workflows or scripts.
- `rebuild_docs`: rebuild Sphinx documentation outputs and write warning logs into a managed temp run directory.

## Manifest

```yaml
tools:
  - id: cleanup_temp_assets
    definition: .agent/tools/cleanup_temp_assets.md
    asset_structure: flat-file
    category: utility_and_infrastructure
    runtime: system
    confirmation: never
    tool_args: none
    direct_cli_flags:
      - --stale-days
      - --delete-empty
      - --delete-stale
      - --delete-retained
    output_capture_required: false
    destructive_capability: conditional
    primary_outputs:
      - stdout audit summary by directory class
      - stdout deleted-directory list when deletion flags are used
    primary_side_effects:
      - none in default dry-run mode
      - may delete directories under .agent/.temp/ when explicitly requested
    implementation: .agent/scripts/cleanup_temp_assets.py
    keywords:
      - temp
      - cleanup
      - stale
      - retained-failure
      - run-directory
    use_when:
      - auditing managed temp workspace state
      - removing empty or stale temp artifacts
      - reviewing retained failure directories

  - id: generate_uuid
    definition: .agent/tools/generate_uuid.md
    asset_structure: flat-file
    category: utility_and_infrastructure
    runtime: system
    confirmation: never
    tool_args: none
    direct_cli_flags: none
    output_capture_required: true
    destructive_capability: none
    primary_outputs:
      - one UUIDv4 string on stdout
    primary_side_effects:
      - none
    implementation: .agent/scripts/generate_uuid.py
    keywords:
      - uuid
      - unique-id
      - run-id
      - temp-path
      - workflow-bootstrap
    use_when:
      - generating a unique identifier for a temp run directory
      - seeding workflow variables with a collision-resistant ID

  - id: rebuild_docs
    definition: .agent/tools/rebuild_docs.md
    asset_structure: flat-file
    category: utility_and_infrastructure
    runtime: system
    confirmation: never
    tool_args: none
    direct_cli_flags: none
    output_capture_required: false
    destructive_capability: none
    primary_outputs:
      - docs/_build/json/needs.json
      - docs/_build/html/
      - .agent/.temp/<run-dir>/refresh-context.log
      - .agent/.temp/<run-dir>/refresh-context-html.log
    primary_side_effects:
      - creates a managed temp run directory
      - rebuilds documentation artifacts under docs/_build/
    implementation: inline powershell command in tool frontmatter
    keywords:
      - docs
      - sphinx
      - html
      - needs
      - warnings
      - rebuild
    use_when:
      - rebuilding documentation outputs
      - regenerating needs export and HTML documentation
      - capturing Sphinx warnings for follow-up review
```

## Tool Records

### `cleanup_temp_assets`

- Definition: [`cleanup_temp_assets.md`](cleanup_temp_assets.md)
- Implementation: [`.agent/scripts/cleanup_temp_assets.py`](../scripts/cleanup_temp_assets.py)
- Best used for: temp-workspace hygiene, stale-run auditing, and controlled cleanup inside `.agent/.temp/`.
- Inputs (tool definition): no structured args.
- Inputs (direct script invocation): optional CLI flags for stale threshold and deletion mode.
- Outputs: reports counts and paths for invalid directories, empty run directories, retained failure directories, stale run directories, and active run directories.
- Outputs in destructive mode: also reports deleted paths.
- Safety contract: dry-run by default.
- Safety contract: refuses to operate outside `.agent/.temp/`.
- Safety contract: retained failure directories are not deleted unless `--delete-retained` is supplied.
- Open the linked definition before execution if any deletion mode is intended.

### `generate_uuid`

- Definition: [`generate_uuid.md`](generate_uuid.md)
- Implementation: [`.agent/scripts/generate_uuid.py`](../scripts/generate_uuid.py)
- Best used for: generating a unique workflow value that must be captured and reused immediately.
- Inputs (tool definition): no structured args.
- Inputs (direct script invocation): no arguments accepted.
- Outputs: emits exactly one UUIDv4 string to stdout on success.
- Failure behavior: emits errors to stderr and exits non-zero on failure or unexpected arguments.
- Safety contract: no filesystem writes.
- Safety contract: no destructive behavior.
- Open the linked definition before use if you need the exit-code contract or workflow-capture example.

### `rebuild_docs`

- Definition: [`rebuild_docs.md`](rebuild_docs.md)
- Implementation: inline PowerShell command in the tool frontmatter
- Best used for: rebuilding Sphinx outputs while preserving warning logs inside the managed temp workspace.
- Inputs (tool definition): no structured args.
- Outputs: rebuilds `docs/_build/json/needs.json`.
- Outputs: rebuilds `docs/_build/html/`.
- Outputs: writes warning logs under `.agent/.temp/<run-dir>/`.
- Post-run check: read both generated warning logs.
- Post-run check: confirm `docs/_build/json/needs.json` exists and is non-empty.
- Post-run check: confirm `docs/_build/html/index.html` exists.
- Safety contract: writes transient logs only inside the generated temp run directory.
- Safety contract: does not expose destructive delete flags.
- Open the linked definition before execution whenever warning counts or rebuild validation need to be reported.

## Category Totals

- `utility_and_infrastructure`: `3`
- `total`: `3`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- Do not infer unsupported flags, outputs, or safety guarantees from summaries in this index alone.
- When a task depends on exact invocation semantics, exit codes, or validation protocol, defer to the linked tool definition.
