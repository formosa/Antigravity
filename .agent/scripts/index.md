# Agent Scripts Index

> Consolidated registry of root script implementations in `.agent/scripts/`.
>
> Scope: discovery, first-pass selection, and quick routing across durable script assets that live directly under the scripts root.
>
> Total scripts: `8`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked script implementation or linked tool definition, the implementation and tool definition are authoritative.

## Use This Index

1. Use the selection map to identify the most likely root script by intent.
2. Use the manifest to confirm the implementation path, category, and optional tool linkage.
3. Open the linked tool definition before execution when invocation semantics, output handling, or safety boundaries matter.

## Selection Map

- `cleanup_temp_assets`: Audit and optionally clean up stale agent temp run directories in .agent/.temp.
- `directory_tree`: Generate and format text-based directory tree representations with configurable filtering and statistics.
- `generate_ddr_release_docs`: Generate DDR v7.0 markdown release surfaces from the v7.0 YAML authority pair.
- `managed_temp`: Manage timestamped run directories under .agent/.temp for single-task artifacts.
- `rebuild_docs`: Rebuild Sphinx documentation outputs with managed-temp warning capture.
- `runtime_target`: Shared loader and validator for the repository runtime target manifest.
- `update_index`: Regenerate governed root and tests script indexes in .agent/scripts/.
- `validate_ddr_release`: Validate the DDR v7.0 release package against the owned release boundary.

## Manifest

```yaml
scripts:
- id: cleanup_temp_assets
  definition: .agent/scripts/cleanup_temp_assets.py
  asset_structure: flat-file
  category: utility_and_infrastructure
  implementation: .agent/scripts/cleanup_temp_assets.py
  keywords:
  - script
  - cleanup
  - temp
  - assets
  - utility_and_infrastructure
  - tool-linked
  use_when:
  - Audit and optionally clean up stale agent temp run directories in .agent/.temp.
  tool_definition: .agent/tools/cleanup_temp_assets.md
- id: directory_tree
  definition: .agent/scripts/directory_tree.py
  asset_structure: flat-file
  category: analysis_and_reporting
  implementation: .agent/scripts/directory_tree.py
  keywords:
  - script
  - directory
  - tree
  - analysis_and_reporting
  use_when:
  - Generate and format text-based directory tree representations with configurable
    filtering and statistics.
- id: generate_ddr_release_docs
  definition: .agent/scripts/generate_ddr_release_docs.py
  asset_structure: flat-file
  category: utility_and_infrastructure
  implementation: .agent/scripts/generate_ddr_release_docs.py
  keywords:
  - script
  - generate
  - ddr
  - release
  - docs
  - utility_and_infrastructure
  - tool-linked
  use_when:
  - Generate DDR v7.0 markdown release surfaces from the v7.0 YAML authority pair.
  tool_definition: .agent/tools/generate_ddr_release_docs.md
- id: managed_temp
  definition: .agent/scripts/managed_temp.py
  asset_structure: flat-file
  category: general_scripts
  implementation: .agent/scripts/managed_temp.py
  keywords:
  - script
  - managed
  - temp
  - general_scripts
  use_when:
  - Manage timestamped run directories under .agent/.temp for single-task artifacts.
- id: rebuild_docs
  definition: .agent/scripts/rebuild_docs.py
  asset_structure: flat-file
  category: utility_and_infrastructure
  implementation: .agent/scripts/rebuild_docs.py
  keywords:
  - script
  - rebuild
  - docs
  - utility_and_infrastructure
  - tool-linked
  use_when:
  - Rebuild Sphinx documentation outputs with managed-temp warning capture.
  tool_definition: .agent/tools/rebuild_docs.md
- id: runtime_target
  definition: .agent/scripts/runtime_target.py
  asset_structure: flat-file
  category: general_scripts
  implementation: .agent/scripts/runtime_target.py
  keywords:
  - script
  - runtime
  - target
  - general_scripts
  use_when:
  - Shared loader and validator for the repository runtime target manifest.
- id: update_index
  definition: .agent/scripts/update_index.py
  asset_structure: flat-file
  category: governance_and_inventory
  implementation: .agent/scripts/update_index.py
  keywords:
  - script
  - update
  - index
  - governance_and_inventory
  use_when:
  - Regenerate governed root and tests script indexes in .agent/scripts/.
- id: validate_ddr_release
  definition: .agent/scripts/validate_ddr_release.py
  asset_structure: flat-file
  category: utility_and_infrastructure
  implementation: .agent/scripts/validate_ddr_release.py
  keywords:
  - script
  - validate
  - ddr
  - release
  - utility_and_infrastructure
  - tool-linked
  use_when:
  - Validate the DDR v7.0 release package against the owned release boundary.
  tool_definition: .agent/tools/validate_ddr_release.md
```

## Script Records

### `cleanup_temp_assets`

- Implementation: [`cleanup_temp_assets.py`](cleanup_temp_assets.py)
- Best used for: Audit and optionally clean up stale agent temp run directories in .agent/.temp.
- Category: `utility_and_infrastructure`
- Tool Definition: [`cleanup_temp_assets.md`](../tools/cleanup_temp_assets.md)
- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.

### `directory_tree`

- Implementation: [`directory_tree.py`](directory_tree.py)
- Best used for: Generate and format text-based directory tree representations with configurable filtering and statistics.
- Category: `analysis_and_reporting`
- Tool Definition: none
- Open the script implementation when internal helper behavior or direct invocation details matter.

### `generate_ddr_release_docs`

- Implementation: [`generate_ddr_release_docs.py`](generate_ddr_release_docs.py)
- Best used for: Generate DDR v7.0 markdown release surfaces from the v7.0 YAML authority pair.
- Category: `utility_and_infrastructure`
- Tool Definition: [`generate_ddr_release_docs.md`](../tools/generate_ddr_release_docs.md)
- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.

### `managed_temp`

- Implementation: [`managed_temp.py`](managed_temp.py)
- Best used for: Manage timestamped run directories under .agent/.temp for single-task artifacts.
- Category: `general_scripts`
- Tool Definition: none
- Open the script implementation when internal helper behavior or direct invocation details matter.

### `rebuild_docs`

- Implementation: [`rebuild_docs.py`](rebuild_docs.py)
- Best used for: Rebuild Sphinx documentation outputs with managed-temp warning capture.
- Category: `utility_and_infrastructure`
- Tool Definition: [`rebuild_docs.md`](../tools/rebuild_docs.md)
- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.

### `runtime_target`

- Implementation: [`runtime_target.py`](runtime_target.py)
- Best used for: Shared loader and validator for the repository runtime target manifest.
- Category: `general_scripts`
- Tool Definition: none
- Open the script implementation when internal helper behavior or direct invocation details matter.

### `update_index`

- Implementation: [`update_index.py`](update_index.py)
- Best used for: Regenerate governed root and tests script indexes in .agent/scripts/.
- Category: `governance_and_inventory`
- Tool Definition: none
- Open the script implementation when internal helper behavior or direct invocation details matter.

### `validate_ddr_release`

- Implementation: [`validate_ddr_release.py`](validate_ddr_release.py)
- Best used for: Validate the DDR v7.0 release package against the owned release boundary.
- Category: `utility_and_infrastructure`
- Tool Definition: [`validate_ddr_release.md`](../tools/validate_ddr_release.md)
- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.

## Category Totals

- `utility_and_infrastructure`: `4`
- `analysis_and_reporting`: `1`
- `governance_and_inventory`: `1`
- `general_scripts`: `2`
- `total`: `8`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- It inventories only root-level Python scripts under `.agent/scripts/` and excludes the governed `tests/` subtree.
- When a task depends on exact CLI behavior, outputs, or deletion semantics, defer to the linked script implementation and any linked tool definition.
