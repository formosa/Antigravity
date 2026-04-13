# Agent Tools Index

> Consolidated registry of tool assets in `.agent/tools/`.
>
> Scope: discovery, first-pass selection, and quick operational reference.
>
> Total tools: `4`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked tool definition, the linked tool definition is authoritative.

## Use This Index

1. Use the selection map to identify the best candidate by intent.
2. Use the manifest to confirm runtime, inputs, outputs, side effects, and safety posture.
3. Open the linked tool definition before execution when destructive behavior, output capture, or post-run validation matters.

## Selection Map

- `cleanup_temp_assets`: audit `.agent/.temp/`; optionally remove empty, stale, or retained-failure managed temp directories when explicit deletion flags are used.
- `generate_ddr_release_docs`: generate the governed DDR v7.0 markdown release surfaces from the v7.0 YAML authority pair.
- `rebuild_docs`: rebuild Sphinx documentation outputs; delete managed temp logs on success and retain them only on failure.
- `validate_ddr_release`: run the owned DDR v7.0 release gate against the authority pair, generated markdown, and conformance corpus.

## Manifest

```yaml
tools:
  - id: cleanup_temp_assets
    definition: .agent/tools/cleanup_temp_assets.md
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
      - managed-temp
    use_when:
      - auditing managed temp workspace state
      - removing empty or stale temp artifacts
      - reviewing retained failure directories

  - id: rebuild_docs
    definition: .agent/tools/rebuild_docs.md
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
      - .agent/.temp/<run-dir>/refresh-context.log (failure only)
      - .agent/.temp/<run-dir>/refresh-context-html.log (failure only)
    primary_side_effects:
      - creates a managed temp run directory during execution
      - deletes the managed temp run directory on success
      - retains the managed temp run directory with a failure marker on rebuild or validation failure
      - rebuilds documentation artifacts under docs/_build/
    implementation: .agent/scripts/rebuild_docs.py
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

  - id: generate_ddr_release_docs
    definition: .agent/tools/generate_ddr_release_docs.md
    category: utility_and_infrastructure
    runtime: system
    confirmation: never
    tool_args: none
    direct_cli_flags:
      - --system
      - --schema
      - --canonical-out
      - --manual-out
    output_capture_required: false
    destructive_capability: none
    primary_outputs:
      - ddr/DDR System(v7.0).md
      - ddr/ddr_ref_manual_v7.0.md
    primary_side_effects:
      - overwrites the governed v7.0 markdown release surfaces
    implementation: .agent/scripts/generate_ddr_release_docs.py
    keywords:
      - ddr
      - release
      - markdown
      - provenance
      - generator
    use_when:
      - generating v7.0 release markdown from the authoritative YAML pair
      - refreshing governed provenance headers on release docs

  - id: validate_ddr_release
    definition: .agent/tools/validate_ddr_release.md
    category: utility_and_infrastructure
    runtime: system
    confirmation: never
    tool_args: none
    direct_cli_flags:
      - --system
      - --schema
      - --canonical-doc
      - --manual-doc
      - --corpus-root
    output_capture_required: false
    destructive_capability: none
    primary_outputs:
      - stdout release-validation summary
    primary_side_effects:
      - none
    implementation: .agent/scripts/validate_ddr_release.py
    keywords:
      - ddr
      - release
      - validator
      - provenance
      - conformance
    use_when:
      - validating the v7.0 authority pair and derived release surfaces
      - executing the owned v7.0 conformance corpus
```

## Tool Records

### `cleanup_temp_assets`

- Definition: [`cleanup_temp_assets.md`](cleanup_temp_assets.md)
- Implementation: [`.agent/scripts/cleanup_temp_assets.py`](../scripts/cleanup_temp_assets.py)
- Best used for: temp-workspace hygiene, stale-run auditing, and controlled cleanup inside `.agent/.temp/`.
- Inputs (tool definition): no structured args.
- Inputs (direct script invocation): optional CLI flags for stale threshold and deletion mode.
- Outputs: reports counts and paths for empty run directories, retained failure directories, stale run directories, and active run directories.
- Outputs in destructive mode: also reports deleted paths.
- Safety contract: dry-run by default.
- Safety contract: refuses to operate outside `.agent/.temp/`.
- Safety contract: retained failure directories are not deleted unless `--delete-retained` is supplied.
- Open the linked definition before execution if any deletion mode is intended.

### `rebuild_docs`

- Definition: [`rebuild_docs.md`](rebuild_docs.md)
- Implementation: [`.agent/scripts/rebuild_docs.py`](../scripts/rebuild_docs.py)
- Best used for: rebuilding Sphinx outputs while keeping temp logs only when a rebuild or output check fails.
- Inputs (tool definition): no structured args.
- Outputs: rebuilds `docs/_build/json/needs.json`.
- Outputs: rebuilds `docs/_build/html/`.
- Outputs on failure: writes warning logs under `.agent/.temp/<run-dir>/`.
- Post-run check: read both generated warning logs.
- Post-run check: confirm `docs/_build/json/needs.json` exists and is non-empty.
- Post-run check: confirm `docs/_build/html/index.html` exists.
- Post-run check: confirm the managed temp run directory is deleted on success.
- Safety contract: writes transient logs only inside the generated temp run directory.
- Safety contract: retains temp logs only when the rebuild fails or output validation fails.
- Safety contract: does not expose destructive delete flags.
- Open the linked definition before execution whenever warning counts or rebuild validation need to be reported.

### `generate_ddr_release_docs`

- Definition: [`generate_ddr_release_docs.md`](generate_ddr_release_docs.md)
- Implementation: [`.agent/scripts/generate_ddr_release_docs.py`](../scripts/generate_ddr_release_docs.py)
- Best used for: generating the governed v7.0 canonical markdown and reference manual from the YAML authority pair.
- Inputs (tool definition): no structured args.
- Inputs (direct script invocation): `--system`, `--schema`, `--canonical-out`, `--manual-out`.
- Outputs: writes `ddr/DDR System(v7.0).md`.
- Outputs: writes `ddr/ddr_ref_manual_v7.0.md`.
- Safety contract: halts on missing or malformed YAML.
- Safety contract: generated markdown remains explanatory only.
- Open the linked definition before execution when custom output routing or provenance expectations matter.

### `validate_ddr_release`

- Definition: [`validate_ddr_release.md`](validate_ddr_release.md)
- Implementation: [`.agent/scripts/validate_ddr_release.py`](../scripts/validate_ddr_release.py)
- Best used for: enforcing the owned v7.0 release gate across YAML authority, markdown provenance, and corpus cases.
- Inputs (tool definition): no structured args.
- Inputs (direct script invocation): `--system`, `--schema`, `--canonical-doc`, `--manual-doc`, `--corpus-root`.
- Outputs: prints a release-validation summary to stdout.
- Safety contract: fails on any schema, provenance, or corpus mismatch.
- Safety contract: has no destructive side effects.
- Open the linked definition before execution whenever the release package needs a stop-go decision.

## Category Totals

- `utility_and_infrastructure`: `4`
- `total`: `4`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- Do not infer unsupported flags, outputs, or safety guarantees from summaries in this index alone.
- When a task depends on exact invocation semantics, exit codes, or validation protocol, defer to the linked tool definition.
