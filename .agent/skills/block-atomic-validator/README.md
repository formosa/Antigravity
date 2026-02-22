# Block-Atomic Validator Skill

**Version:** 1.0.0
**Target IDE:** Google Antigravity IDE 1.16.5+
**Category:** DDR System Enforcement

---

## Overview

The Block-Atomic Validator is a Claude Skill that enforces strict hierarchical relationships between block-level tags (`TIER-N`) and atomic-level tags (`TIER-N.M`) in DDR System documentation.

### Key Validations

1. **Ordering**: Block tags must appear before their atomic children in document order
2. **Citation**: Atomic tags must cite their parent block via `:links:` directive
3. **Consistency**: No orphaned atomic tags without corresponding blocks
4. **Prefix**: Tier prefix matches between block and atomic tags

---

## Installation

### Prerequisites

- Google Antigravity IDE 1.16.5 or later
- Python 3.9+
- DDR System project structure

### Install via Antigravity Package Manager

```bash
# From Antigravity IDE terminal
antigravity skill install block_atomic_validator
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/ddr-system/block-atomic-validator.git
cd block-atomic-validator

# Install dependencies
pip install -e .

# Register with Antigravity IDE
antigravity skill register .
```

---

## Configuration

### Default Configuration

The skill uses sensible defaults from `skill_manifest.yaml`:

```yaml
validation_rules:
  ordering_violation:
    enabled: true
    severity: "error"

  missing_block_citation:
    enabled: true
    severity: "error"

  orphaned_atomic:
    enabled: true
    severity: "error"

  prefix_mismatch:
    enabled: true
    severity: "warning"
```

### Custom Configuration

Override defaults in your project's `.antigravity/settings.yaml`:

```yaml
skills:
  block_atomic_validator:
    strict_mode: true
    validation_rules:
      prefix_mismatch:
        severity: "error"  # Elevate warnings to errors
```

---

## Usage

### Automatic Validation

The skill automatically validates on:

- **File Save**: `Ctrl+S` triggers validation
- **File Open**: Opening `.rst` files in `docs/` triggers validation
- **Project Build**: Build command validates all files

### Manual Validation

#### Validate Current File

```
Ctrl+Shift+V B
```

Or via command palette:

```
DDR: Validate Block-Atomic Structure
```

#### Validate Entire Project

```bash
# From Antigravity terminal
antigravity skill run block_atomic_validator --scope project
```

### View Results

Validation results appear in:

1. **Problems Panel**: Bottom panel with filterable diagnostics
2. **Inline Warnings**: Squiggly underlines in editor
3. **Hover Tooltips**: Hover over violations for details

---

## Validation Rules

### Rule DDR001: Ordering Violation

**Severity:** Error

**Description:** Block tag must appear before atomic children.

**Example:**

```rst
❌ INVALID:

.. fsd:: Specific feature detail
   :id: FSD-4.1
   :links: FSD-4

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5
```

**Fix:**

```rst
✅ VALID:

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Specific feature detail
   :id: FSD-4.1
   :links: FSD-4
```

---

### Rule DDR002: Missing Block Citation

**Severity:** Error

**Description:** Atomic tag must cite parent block in `:links:`.

**Example:**

```rst
❌ INVALID:

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Specific feature detail
   :id: FSD-4.1
   :links: BRD-5, NFR-2  ← Missing FSD-4
```

**Fix:**

```rst
✅ VALID:

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Specific feature detail
   :id: FSD-4.1
   :links: FSD-4  ← Cites block parent
```

---

### Rule DDR003: Orphaned Atomic

**Severity:** Error

**Description:** Atomic tag has no corresponding block tag.

**Example:**

```rst
❌ INVALID:

.. fsd:: Specific feature detail
   :id: FSD-4.1
   :links: FSD-4

(No FSD-4 block exists)
```

**Fix:**

```rst
✅ VALID:

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Specific feature detail
   :id: FSD-4.1
   :links: FSD-4
```

---

### Rule DDR004: Prefix Mismatch

**Severity:** Warning

**Description:** Tier prefix inconsistency between block/atomic.

**Example:**

```rst
❌ INVALID:

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. nfr:: Latency constraint
   :id: NFR-4.1  ← Tier mismatch
   :links: FSD-4
```

---

## Integration with Antigravity IDE

### IDE Hooks

The skill registers the following hooks:

| Hook | Trigger | Action |
|:-----|:--------|:-------|
| `on_file_save` | File saved | Validate file |
| `on_file_open` | File opened | Validate file |
| `on_project_build` | Build initiated | Validate all files |

### Commands

| Command | Keybinding | Description |
|:--------|:-----------|:------------|
| `ddr.validate_block_atomic` | `Ctrl+Shift+V B` | Validate current file |
| `ddr.fix_block_atomic` | `Ctrl+Shift+F B` | Auto-fix violations |

### Diagnostic Format

Results use Antigravity's native diagnostic format:

```json
{
  "file": "docs/03_fsd/fsd.rst",
  "tier": "FSD",
  "is_valid": false,
  "diagnostics": [
    {
      "code": "DDR001",
      "severity": "error",
      "message": "Block tag FSD-4 must appear before atomic child FSD-4.1",
      "range": {
        "start": {"line": 42, "character": 0},
        "end": {"line": 42, "character": 9999}
      }
    }
  ]
}
```

---

## Testing

### Run Unit Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest --cov=src/block_atomic_validator tests/
```

### Test Fixtures

Sample test files are in `tests/fixtures/`:

- `valid_brd.rst` - Valid block-atomic structure
- `invalid_ordering.rst` - Ordering violations
- `invalid_citation.rst` - Citation violations

---

## API Reference

### Core Classes

#### `BlockAtomicValidator`

Main validation engine.

```python
from block_atomic_validator.core.validator import BlockAtomicValidator

validator = BlockAtomicValidator(config)
result = validator.validate_file(Path("docs/03_fsd/fsd.rst"))
```

#### `Tag`

DDR tag representation.

```python
from block_atomic_validator.core.models import Tag

tag = Tag(
    tag_id="FSD-4.1",
    tier="FSD",
    block_number=4,
    atomic_number=1,
    line_number=42,
    title="Wake word detection"
)
```

#### `ValidationResult`

Validation outcome.

```python
result.is_valid  # bool
result.violations  # List[Violation]
result.error_count  # int
result.warning_count  # int
```

---

## Troubleshooting

### Issue: Validator not triggering

**Solution:** Check Antigravity skill status

```bash
antigravity skill status block_atomic_validator
```

### Issue: False positives

**Solution:** Verify RST directive syntax

```rst
.. tier:: Title  ← Space required after ::
   :id: TAG-N    ← Three-space indent
   :links: PAR   ← Links on separate line
```

### Issue: Performance slow on large projects

**Solution:** Enable incremental validation in settings

```yaml
skills:
  block_atomic_validator:
    incremental_validation: true
```

---

## Development

### Project Structure

```
block_atomic_validator/
├── src/block_atomic_validator/
│   ├── core/          # Validation engine
│   ├── rules/         # Validation rules
│   ├── reporters/     # Output formatters
│   └── utils/         # Helper functions
├── tests/             # Test suite
├── docs/              # Documentation
└── antigravity_hooks/ # IDE integration
```

### Contributing

1. Fork repository
2. Create feature branch
3. Add tests for new rules
4. Update documentation
5. Submit pull request

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Documentation**: <https://ddr-system.docs/skills/block-atomic-validator>
- **Issues**: <https://github.com/ddr-system/block-atomic-validator/issues>
- **DDR System**: See attached `ddr_system.txt` for framework details

---

## Version History

### 1.0.0 (2026-02-20)

- Initial release
- Four core validation rules
- Antigravity IDE 1.16.5+ support
- Auto-fix suggestions
- Project-wide validation
