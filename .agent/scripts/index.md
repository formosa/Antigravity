# Agent Scripts Index

> Consolidated registry of root script implementations in `.agent/scripts/`.
>
> Scope: discovery, first-pass selection, and quick routing across durable script assets that live directly under the scripts root.
>
> Total scripts: `4`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked script implementation or linked tool definition, the implementation and tool definition are authoritative.

## Use This Index

1. Use the selection map to identify the most likely root script by intent.
2. Use the manifest to confirm the implementation path, category, and optional tool linkage.
3. Open the linked tool definition before execution when invocation semantics, output handling, or safety boundaries matter.

## Selection Map

- `cleanup_temp_assets`: Audit and optionally clean up stale managed temp run directories.
- `directory_tree`: Generate a directory tree with filtering, labeling, and reporting.
- `generate_uuid`: Generate a UUIDv4 string for workflow and temp-path capture.
- `update_index`: Regenerate the governed root and tests script indexes.

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
  - Audit and optionally clean up stale managed temp run directories.
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
  - Generate a directory tree with filtering, labeling, and reporting.
- id: generate_uuid
  definition: .agent/scripts/generate_uuid.py
  asset_structure: flat-file
  category: utility_and_infrastructure
  implementation: .agent/scripts/generate_uuid.py
  keywords:
  - script
  - generate
  - uuid
  - utility_and_infrastructure
  - tool-linked
  use_when:
  - Generate a UUIDv4 string for workflow and temp-path capture.
  tool_definition: .agent/tools/generate_uuid.md
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
  - Regenerate the governed root and tests script indexes.
```

## Script Records

### `cleanup_temp_assets`

- Implementation: [`cleanup_temp_assets.py`](cleanup_temp_assets.py)
- Best used for: Audit and optionally clean up stale managed temp run directories.
- Category: `utility_and_infrastructure`
- Tool Definition: [`cleanup_temp_assets.md`](../tools/cleanup_temp_assets.md)
- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.

### `directory_tree`

- Implementation: [`directory_tree.py`](directory_tree.py)
- Best used for: Generate a directory tree with filtering, labeling, and reporting.
- Category: `analysis_and_reporting`
- Tool Definition: none
- Open the script implementation when internal helper behavior or direct invocation details matter.

### `generate_uuid`

- Implementation: [`generate_uuid.py`](generate_uuid.py)
- Best used for: Generate a UUIDv4 string for workflow and temp-path capture.
- Category: `utility_and_infrastructure`
- Tool Definition: [`generate_uuid.md`](../tools/generate_uuid.md)
- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.

### `update_index`

- Implementation: [`update_index.py`](update_index.py)
- Best used for: Regenerate the governed root and tests script indexes.
- Category: `governance_and_inventory`
- Tool Definition: none
- Open the script implementation when internal helper behavior or direct invocation details matter.

## Category Totals

- `utility_and_infrastructure`: `2`
- `analysis_and_reporting`: `1`
- `governance_and_inventory`: `1`
- `total`: `4`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- It inventories only root-level Python scripts under `.agent/scripts/` and excludes the governed `tests/` subtree.
- When a task depends on exact CLI behavior, outputs, or deletion semantics, defer to the linked script implementation and any linked tool definition.
