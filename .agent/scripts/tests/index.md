# Agent Script Tests Index

> Consolidated registry of governed test and validation scripts in `.agent/scripts/tests/`.
>
> Scope: discovery, first-pass selection, and quick routing across unit tests, diagnostics, and fixture helpers that support the scripts collection.
>
> Total test scripts: `7`
>
> Parent: [`.agent/scripts/`](..)
>
> Authority rule: if this index conflicts with a linked test implementation, the test script is authoritative.

## Use This Index

1. Use the selection map to identify the most relevant test, diagnostic, or fixture script.
2. Use the manifest to confirm the implementation path and category before execution.
3. Open the linked test implementation when exact assertions, environment assumptions, or fixture behavior matter.

## Selection Map

- `chaos_script`: Chaos fixture script used for adversarial or low-quality test inputs.
- `test_cleanup_temp_assets`: Unit tests for cleanup_temp_assets.py.
- `test_directory_tree`: Unit tests for directory_tree.py.
- `test_managed_temp`: Unit tests for managed_temp.py.
- `test_rebuild_docs`: Unit tests for rebuild_docs.py.
- `test_update_index`: Unit tests for update_index.py.
- `validate_env`: Validation gate for the Antigravity PowerShell execution baseline.

## Manifest

```yaml
tests:
- id: chaos_script
  definition: .agent/scripts/tests/chaos_script.py
  asset_structure: flat-file
  category: fixtures_and_chaos
  implementation: .agent/scripts/tests/chaos_script.py
  keywords:
  - script
  - chaos
  - fixtures_and_chaos
  use_when:
  - Chaos fixture script used for adversarial or low-quality test inputs.
- id: test_cleanup_temp_assets
  definition: .agent/scripts/tests/test_cleanup_temp_assets.py
  asset_structure: flat-file
  category: unit_tests
  implementation: .agent/scripts/tests/test_cleanup_temp_assets.py
  keywords:
  - script
  - test
  - cleanup
  - temp
  - assets
  - unit_tests
  use_when:
  - Unit tests for cleanup_temp_assets.py.
- id: test_directory_tree
  definition: .agent/scripts/tests/test_directory_tree.py
  asset_structure: flat-file
  category: unit_tests
  implementation: .agent/scripts/tests/test_directory_tree.py
  keywords:
  - script
  - test
  - directory
  - tree
  - unit_tests
  use_when:
  - Unit tests for directory_tree.py.
- id: test_managed_temp
  definition: .agent/scripts/tests/test_managed_temp.py
  asset_structure: flat-file
  category: unit_tests
  implementation: .agent/scripts/tests/test_managed_temp.py
  keywords:
  - script
  - test
  - managed
  - temp
  - unit_tests
  use_when:
  - Unit tests for managed_temp.py.
- id: test_rebuild_docs
  definition: .agent/scripts/tests/test_rebuild_docs.py
  asset_structure: flat-file
  category: unit_tests
  implementation: .agent/scripts/tests/test_rebuild_docs.py
  keywords:
  - script
  - test
  - rebuild
  - docs
  - unit_tests
  use_when:
  - Unit tests for rebuild_docs.py.
- id: test_update_index
  definition: .agent/scripts/tests/test_update_index.py
  asset_structure: flat-file
  category: unit_tests
  implementation: .agent/scripts/tests/test_update_index.py
  keywords:
  - script
  - test
  - update
  - index
  - unit_tests
  use_when:
  - Unit tests for update_index.py.
- id: validate_env
  definition: .agent/scripts/tests/validate_env.py
  asset_structure: flat-file
  category: diagnostics_and_validation
  implementation: .agent/scripts/tests/validate_env.py
  keywords:
  - script
  - validate
  - env
  - diagnostics_and_validation
  use_when:
  - Validation gate for the Antigravity PowerShell execution baseline.
```

## Test Script Records

### `chaos_script`

- Implementation: [`chaos_script.py`](chaos_script.py)
- Best used for: Chaos fixture script used for adversarial or low-quality test inputs.
- Category: `fixtures_and_chaos`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

### `test_cleanup_temp_assets`

- Implementation: [`test_cleanup_temp_assets.py`](test_cleanup_temp_assets.py)
- Best used for: Unit tests for cleanup_temp_assets.py.
- Category: `unit_tests`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

### `test_directory_tree`

- Implementation: [`test_directory_tree.py`](test_directory_tree.py)
- Best used for: Unit tests for directory_tree.py.
- Category: `unit_tests`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

### `test_managed_temp`

- Implementation: [`test_managed_temp.py`](test_managed_temp.py)
- Best used for: Unit tests for managed_temp.py.
- Category: `unit_tests`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

### `test_rebuild_docs`

- Implementation: [`test_rebuild_docs.py`](test_rebuild_docs.py)
- Best used for: Unit tests for rebuild_docs.py.
- Category: `unit_tests`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

### `test_update_index`

- Implementation: [`test_update_index.py`](test_update_index.py)
- Best used for: Unit tests for update_index.py.
- Category: `unit_tests`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

### `validate_env`

- Implementation: [`validate_env.py`](validate_env.py)
- Best used for: Validation gate for the Antigravity PowerShell execution baseline.
- Category: `diagnostics_and_validation`
- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.

## Category Totals

- `unit_tests`: `5`
- `diagnostics_and_validation`: `1`
- `fixtures_and_chaos`: `1`
- `total`: `7`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- It inventories only live Python files in `.agent/scripts/tests/` and excludes generated indexes, caches, and compiled artifacts.
- When a task depends on exact assertions, subprocess expectations, or fixture semantics, defer to the linked test implementation.
