# Antigravity IDE Integration Guide

## Block-Atomic Validator Skill v1.0.0

> Complete guide for integrating the Block-Atomic Validator into Google's Antigravity IDE 1.16.5+

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [IDE Integration Points](#ide-integration-points)
5. [Custom Workflows](#custom-workflows)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Antigravity IDE**: Version 1.16.5 or later
- **Python**: 3.9+ (included with Antigravity)
- **Operating System**: Windows 11 Pro (as specified in user hardware)
- **Hardware**: AMD Ryzen 9 5900X with 32GB RAM (optimal performance)

### Project Requirements

- DDR System project structure in place
- RST files in `docs/` directory hierarchy
- Sphinx-Needs directives for tag definitions

---

## Installation Methods

### Method 1: Antigravity Package Manager (Recommended)

```bash
# From Antigravity IDE integrated terminal
antigravity skill install block_atomic_validator

# Verify installation
antigravity skill list | grep block_atomic_validator
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/ddr-system/block-atomic-validator.git
cd block-atomic-validator

# Install Python package
pip install -e .

# Register with Antigravity
antigravity skill register .

# Verify registration
antigravity skill status block_atomic_validator
```

### Method 3: From Source (Development)

```bash
# For developers modifying the skill
git clone https://github.com/ddr-system/block-atomic-validator.git
cd block-atomic-validator

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests to verify
pytest tests/ -v

# Register in development mode
antigravity skill register . --dev
```

---

## Configuration

### Default Configuration Location

Antigravity stores skill configurations in:

```
<project_root>/.antigravity/skills/block_atomic_validator.yaml
```

### Basic Configuration

Minimal configuration (uses defaults):

```yaml
# .antigravity/skills/block_atomic_validator.yaml
enabled: true
```

### Advanced Configuration

Full configuration with all options:

```yaml
# .antigravity/skills/block_atomic_validator.yaml
enabled: true
strict_mode: false
auto_fix_enabled: false
report_format: "ide_native"

validation_rules:
  ordering_violation:
    enabled: true
    severity: "error"
    message: "Block tag {block_id} must appear before atomic child {atomic_id}"

  missing_block_citation:
    enabled: true
    severity: "error"
    message: "Atomic tag {atomic_id} must cite parent block {expected_block_id}"

  orphaned_atomic:
    enabled: true
    severity: "error"
    message: "Atomic tag {atomic_id} has no corresponding block tag"

  prefix_mismatch:
    enabled: true
    severity: "warning"
    message: "Atomic tag {atomic_id} tier does not match block prefix"

hooks:
  on_file_save: true
  on_file_open: true
  on_project_build: true

file_patterns:
  include:
    - "**/*.rst"
    - "docs/**/*.rst"
  exclude:
    - "**/reconciliation_manifest.rst"
    - "**/node_modules/**"
    - "**/.git/**"

performance:
  incremental_validation: true
  cache_results: true
  parallel_validation: true
  max_workers: 4  # Optimal for 12-core Ryzen 9

output:
  show_in_problems_panel: true
  show_inline_diagnostics: true
  show_hover_tooltips: true
  diagnostic_source_name: "DDR: Block-Atomic"
```

### Per-User Settings

Override project settings in user preferences:

```
Windows: %APPDATA%\Antigravity\User\settings.yaml
```

```yaml
skills:
  block_atomic_validator:
    strict_mode: true  # Elevate warnings to errors
    auto_fix_enabled: true  # Enable auto-fix on save
```

---

## IDE Integration Points

### 1. Automatic Validation Triggers

#### On File Save

Validation runs automatically when saving `.rst` files:

```python
# Triggered by: Ctrl+S
# Hook: on_file_save
# Behavior: Validates current file, updates Problems panel
```

**Performance**: < 100ms for files with < 100 tags

#### On File Open

Validation runs when opening `.rst` files:

```python
# Triggered by: File → Open, Ctrl+O
# Hook: on_file_open
# Behavior: Background validation, non-blocking
```

**Performance**: < 200ms for initial load

#### On Project Build

Validation runs for all project files:

```python
# Triggered by: Build → Build Project, Ctrl+Shift+B
# Hook: on_project_build
# Behavior: Parallel validation of all .rst files
```

**Performance**: ~500ms per 100 files on Ryzen 9 5900X

---

### 2. Problems Panel Integration

Violations appear in Antigravity's Problems panel:

```
┌─ PROBLEMS ───────────────────────────────────────────────┐
│ ⚠ 3 errors, 1 warning in workspace                       │
├──────────────────────────────────────────────────────────┤
│ ❌ DDR001  Block tag FSD-4 must appear before FSD-4.1    │
│    docs/03_fsd/fsd.rst:42                                 │
│    DDR: Block-Atomic                                      │
├──────────────────────────────────────────────────────────┤
│ ❌ DDR002  Atomic tag FSD-4.2 must cite parent FSD-4     │
│    docs/03_fsd/fsd.rst:58                                 │
│    DDR: Block-Atomic                                      │
├──────────────────────────────────────────────────────────┤
│ ❌ DDR003  Atomic tag FSD-5.1 has no corresponding block │
│    docs/03_fsd/fsd.rst:71                                 │
│    DDR: Block-Atomic                                      │
├──────────────────────────────────────────────────────────┤
│ ⚠ DDR004  Prefix mismatch: NFR-4.1 with FSD-4 parent    │
│    docs/03_fsd/fsd.rst:89                                 │
│    DDR: Block-Atomic                                      │
└──────────────────────────────────────────────────────────┘
```

**Filter violations**: Click `DDR: Block-Atomic` source to show only these

---

### 3. Inline Diagnostics

Violations shown directly in editor:

```rst
.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Wake word detection
   :id: FSD-4.1
   :links: BRD-5         ← ❌ DDR002: Must cite parent FSD-4
   ~~~~~~~~~~~~~~~
```

**Squiggly underline colors**:

- 🔴 Red: Errors
- 🟡 Yellow: Warnings

---

### 4. Hover Tooltips

Hover over violations for details:

```
┌─────────────────────────────────────────────────────┐
│ ❌ DDR002: Block-Atomic Validation                  │
│                                                      │
│ Atomic tag FSD-4.1 must cite parent block FSD-4     │
│ in :links: directive.                               │
│                                                      │
│ Current links: BRD-5                                │
│                                                      │
│ 💡 Quick Fix: Add FSD-4 to :links: directive        │
│    [Fix] [Ignore] [More Info]                       │
└─────────────────────────────────────────────────────┘
```

---

### 5. Quick Fix Actions

Antigravity shows fix suggestions:

```
Right-click violation → Quick Fix... → Select fix:

┌─────────────────────────────────────────────────────┐
│ 💡 Add FSD-4 to :links: directive                   │
│                                                      │
│    :links: FSD-4, BRD-5                             │
│                                                      │
│ 💡 Remove orphaned atomic tag FSD-4.1               │
│                                                      │
│ 💡 Ignore this violation                            │
│    (adds inline comment: .. block-atomic: ignore)   │
└─────────────────────────────────────────────────────┘
```

---

### 6. Keybindings

Default keybindings (customizable):

| Keybinding | Command | Description |
|:-----------|:--------|:------------|
| `Ctrl+Shift+V B` | Validate Block-Atomic | Validate current file |
| `Ctrl+Shift+F B` | Auto-fix Block-Atomic | Apply suggested fixes |
| `Alt+Enter` | Quick Fix | Show fix options at cursor |
| `F8` | Next Problem | Jump to next violation |
| `Shift+F8` | Previous Problem | Jump to previous violation |

**Customize keybindings**:

```
File → Preferences → Keyboard Shortcuts → Search "block atomic"
```

---

### 7. Status Bar Integration

Skill status appears in IDE status bar:

```
┌─────────────────────────────────────────────────────┐
│  ● Python 3.11  |  DDR: ✅ 0 violations  |  UTF-8  │
└─────────────────────────────────────────────────────┘
```

**Click status** to show validation summary

---

## Custom Workflows

### Workflow 1: Pre-Commit Validation

Run validation before Git commits:

```bash
# .antigravity/hooks/pre-commit
#!/bin/bash
antigravity skill run block_atomic_validator --scope staged

if [ $? -ne 0 ]; then
    echo "❌ Block-atomic validation failed. Commit aborted."
    exit 1
fi
```

Make executable:

```bash
chmod +x .antigravity/hooks/pre-commit
```

---

### Workflow 2: CI/CD Integration

GitHub Actions workflow:

```yaml
# .github/workflows/validate-ddr.yml
name: DDR Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Block-Atomic Validator
        run: |
          pip install block-atomic-validator

      - name: Validate Documentation
        run: |
          block-atomic-validator validate --project-root .
```

---

### Workflow 3: Batch Fixing

Apply all auto-fixes across project:

```bash
# Run validator with auto-fix enabled
antigravity skill run block_atomic_validator \
    --scope project \
    --auto-fix \
    --dry-run  # Preview changes first

# Apply fixes
antigravity skill run block_atomic_validator \
    --scope project \
    --auto-fix
```

---

## Troubleshooting

### Issue: Skill Not Loading

**Symptom**: No validation on file save

**Solutions**:

1. Check skill status:

   ```bash
   antigravity skill status block_atomic_validator
   ```

2. Verify Python environment:

   ```bash
   python -m block_atomic_validator --version
   ```

3. Restart Antigravity IDE

4. Reinstall skill:

   ```bash
   antigravity skill uninstall block_atomic_validator
   antigravity skill install block_atomic_validator
   ```

---

### Issue: Performance Degradation

**Symptom**: Validation takes > 1 second

**Solutions**:

1. Enable incremental validation:

   ```yaml
   performance:
     incremental_validation: true
   ```

2. Increase parallel workers:

   ```yaml
   performance:
     max_workers: 8  # Match CPU core count
   ```

3. Exclude large directories:

   ```yaml
   file_patterns:
     exclude:
       - "**/node_modules/**"
       - "**/build/**"
   ```

---

### Issue: False Positives

**Symptom**: Valid structure flagged as violation

**Solutions**:

1. Verify RST syntax:
   - Three-space indent for `:id:` and `:links:`
   - Space after `::` in directive
   - Tag ID follows `TIER-N` or `TIER-N.M` format

2. Check tag immutability:
   - IDs never change after creation
   - No re-sequencing after deletions

3. Add inline ignore:

   ```rst
   .. fsd:: Special case
      :id: FSD-99
      .. block-atomic: ignore-ordering
   ```

---

### Issue: Missing Diagnostics

**Symptom**: Problems panel empty despite violations

**Solutions**:

1. Verify file patterns:

   ```yaml
   file_patterns:
     include:
       - "**/*.rst"  # Ensure your files match
   ```

2. Check diagnostic filter:
   - In Problems panel, click filter icon
   - Ensure "DDR: Block-Atomic" source is enabled

3. Increase log level:

   ```yaml
   logging:
     level: "DEBUG"
     output: ".antigravity/logs/block_atomic.log"
   ```

---

## Advanced Configuration

### Custom Validation Rules

Extend validation with custom rules:

```python
# .antigravity/skills/custom_rules.py
from block_atomic_validator.rules import BaseRule

class CustomRule(BaseRule):
    def validate(self, tags, context):
        violations = []
        # Your custom logic here
        return violations
```

Register custom rule:

```yaml
validation_rules:
  custom_rule:
    enabled: true
    module: ".antigravity.skills.custom_rules"
    class: "CustomRule"
    severity: "warning"
```

---

### Performance Tuning

For large projects (1000+ RST files):

```yaml
performance:
  incremental_validation: true
  cache_results: true
  cache_ttl: 3600  # 1 hour
  parallel_validation: true
  max_workers: 12  # Match CPU cores
  batch_size: 50  # Files per batch

  # Optimize for Ryzen 9 5900X
  thread_pool: "process"  # Use process pool
  affinity_mask: "0xFF"   # Bind to cores 0-7
```

---

## Support

For additional help:

- **Documentation**: <https://ddr-system.docs/skills/block-atomic-validator>
- **GitHub Issues**: <https://github.com/ddr-system/block-atomic-validator/issues>
- **Antigravity Forum**: <https://forum.antigravity.dev/skills>

---

**Last Updated**: 2026-02-20
**Skill Version**: 1.0.0
**Antigravity IDE**: 1.16.5+
