# ASCII Diagram Enforcer - API Reference

> **Version**: 1.0.0
> **Python**: 3.8+
> **Type Hints**: Fully typed with mypy compatibility

## Module Overview

```python
from ascii_diagram_enforcer.src import (
    ASCIIDiagramEnforcer,      # Core validation engine
    ValidationResult,           # Result container
    Violation,                  # Single violation
    ViolationSeverity,         # ERROR/WARNING enum
    DiagramDetector,           # Pattern matching
    SADParser,                 # RST parsing
    DiagramValidator           # Quality checks
)
```

---

## Core Classes

### ASCIIDiagramEnforcer

Primary validation engine orchestrating all validation operations.

#### Constructor

```python
def __init__(
    self,
    strict_mode: bool = True,
    min_diagram_lines: int = 3,
    auto_flag_dirty: bool = True
)
```

**Parameters**:

- `strict_mode`: If True, ERROR violations block saves
- `min_diagram_lines`: Minimum lines for valid diagram
- `auto_flag_dirty`: Auto-update reconciliation manifests

**Example**:

```python
enforcer = ASCIIDiagramEnforcer(
    strict_mode=True,
    min_diagram_lines=3,
    auto_flag_dirty=True
)
```

#### validate_section

```python
def validate_section(
    self,
    content: str,
    section_id: str
) -> ValidationResult
```

Validate complete SAD section for diagram compliance.

**Parameters**:

- `content`: Raw RST content of SAD section
- `section_id`: Unique identifier (e.g., 'sad-root')

**Returns**: `ValidationResult` with violations

**Example**:

```python
content = Path('docs/04_sad/arch.rst').read_text()
result = enforcer.validate_section(content, 'sad-architecture')

if result.is_valid:
    print(f"✓ Valid: {result.diagrams_found} diagrams")
else:
    print(f"✗ Invalid: {len(result.violations)} violations")
```

#### generate_report

```python
def generate_report(self, result: ValidationResult) -> str
```

Generate human-readable validation report.

**Parameters**:

- `result`: Validation results to format

**Returns**: Formatted report text

**Example**:

```python
report = enforcer.generate_report(result)
print(report)
# ======================================================================
# ASCII Diagram Enforcer - Validation Report
# ======================================================================
# Section ID: sad-root
# Status: INVALID
# ...
```

---

### ValidationResult

Container for complete validation results.

#### Attributes

```python
@dataclass
class ValidationResult:
    section_id: str                      # Section identifier
    is_valid: bool                       # Overall status
    violations: List[Violation] = []     # Detected violations
    sad_tags_found: int = 0              # Total SAD tags
    diagrams_found: int = 0              # Total diagrams
    missing_diagrams: Set[str] = set()   # Tag IDs missing diagrams
```

#### to_reconciliation_item

```python
def to_reconciliation_item(self) -> Dict
```

Convert violations to DDR reconciliation `pending_item` format.

**Returns**: Dict in reconciliation manifest format

**Example**:

```python
if not result.is_valid:
    pending_item = result.to_reconciliation_item()
    # {
    #   "target_tag": "SAD-1",
    #   "source_trigger": "ascii_diagram_enforcer validation",
    #   "issue_type": "CONSTRAINT_VIOLATION",
    #   "description": "Missing or invalid ASCII diagrams: 2 violation(s)"
    # }
```

---

### Violation

Represents a single validation violation.

#### Attributes

```python
@dataclass
class Violation:
    rule_id: str                         # e.g., 'SAD-DIAGRAM-001'
    severity: ViolationSeverity          # ERROR or WARNING
    target_tag: str                      # SAD tag ID
    line_number: int                     # Line in document
    description: str                     # Human-readable
    suggested_fix: Optional[str] = None  # Remediation hint
```

#### Example

```python
violation = Violation(
    rule_id="SAD-DIAGRAM-001",
    severity=ViolationSeverity.ERROR,
    target_tag="SAD-1",
    line_number=42,
    description="Block-level SAD tag missing mandatory ASCII diagram",
    suggested_fix="Insert ASCII topology diagram"
)
```

---

### ViolationSeverity

Enumeration of violation severity levels.

```python
class ViolationSeverity(Enum):
    ERROR = "ERROR"       # Blocking in strict mode
    WARNING = "WARNING"   # Advisory only
    INFO = "INFO"         # Informational
```

**Usage**:

```python
if violation.severity == ViolationSeverity.ERROR:
    print("🔴 Must fix before save")
elif violation.severity == ViolationSeverity.WARNING:
    print("🟡 Should fix for quality")
```

---

## Detection & Parsing

### DiagramDetector

ASCII diagram pattern matching engine.

#### Constructor

```python
def __init__(
    self,
    min_lines: int = 3,
    confidence_threshold: float = 0.6
)
```

**Parameters**:

- `min_lines`: Minimum consecutive lines for diagram
- `confidence_threshold`: Minimum confidence score (0.0-1.0)

#### find_diagrams

```python
def find_diagrams(self, content: str) -> List[Dict]
```

Locate all ASCII diagrams in document.

**Parameters**:

- `content`: Document content to scan

**Returns**: List of diagram dicts with keys:

- `start_line`: int
- `end_line`: int
- `content`: str
- `style`: str (box_and_arrow, hierarchical, network_topology)
- `confidence`: float

**Example**:

```python
detector = DiagramDetector()
diagrams = detector.find_diagrams(content)

for diagram in diagrams:
    print(f"Found {diagram['style']} diagram at line {diagram['start_line']}")
    print(f"Confidence: {diagram['confidence']:.2f}")
```

---

### SADParser

RST directive parser for SAD tags.

#### extract_sad_tags

```python
def extract_sad_tags(self, content: str) -> List[Dict]
```

Extract all SAD tags from document.

**Parameters**:

- `content`: RST document content

**Returns**: List of tag dicts with keys:

- `id`: str (e.g., 'SAD-1')
- `title`: str
- `links`: List[str] (parent citations)
- `line_number`: int
- `level`: str ('block' or 'atomic')

**Example**:

```python
parser = SADParser()
tags = parser.extract_sad_tags(content)

for tag in tags:
    print(f"{tag['id']}: {tag['title']}")
    print(f"  Level: {tag['level']}")
    print(f"  Cites: {', '.join(tag['links'])}")
```

#### is_block_tag

```python
def is_block_tag(self, tag_id: str) -> bool
```

Check if tag is block-level (SAD-N format).

**Example**:

```python
parser.is_block_tag('SAD-1')      # True
parser.is_block_tag('SAD-1.2')    # False
```

#### is_atomic_tag

```python
def is_atomic_tag(self, tag_id: str) -> bool
```

Check if tag is atomic-level (SAD-N.M format).

---

### DiagramValidator

Diagram quality validation engine.

#### validate_diagram

```python
def validate_diagram(
    self,
    diagram: Dict,
    tag_id: str,
    tag_line: int
) -> List[Violation]
```

Validate diagram quality against all rules.

**Parameters**:

- `diagram`: Diagram dict from DiagramDetector
- `tag_id`: Associated SAD tag
- `tag_line`: Tag line number

**Returns**: List of violations (empty if valid)

**Example**:

```python
validator = DiagramValidator()
violations = validator.validate_diagram(diagram, 'SAD-1', 42)

if not violations:
    print("✓ Diagram passes all quality checks")
else:
    for v in violations:
        print(f"{v.rule_id}: {v.description}")
```

#### get_diagram_statistics

```python
def get_diagram_statistics(self, content: str) -> Dict
```

Calculate diagram structural metrics.

**Returns**: Dict with keys:

- `line_count`: int
- `char_count`: int
- `box_count`: int
- `arrow_count`: int
- `label_count`: int

**Example**:

```python
stats = validator.get_diagram_statistics(diagram_content)
print(f"Boxes: {stats['box_count']}, Arrows: {stats['arrow_count']}")
```

---

## Hook Functions

### Pre-Save Hook

```python
from ascii_diagram_enforcer.hooks.pre_save import validate_before_save

def validate_before_save(document, context) -> Dict[str, any]
```

Pre-save validation hook handler. Blocks save in strict mode if ERROR violations exist.

**Parameters**:

- `document`: Document being saved
- `context`: IDE skill context

**Returns**: Dict with keys:

- `allow_save`: bool
- `violations`: List[Violation]
- `message`: Optional[str]

---

### On-Demand Hook

```python
from ascii_diagram_enforcer.hooks.on_demand import validate_on_request

def validate_on_request(document, context) -> Dict[str, any]
```

Manual validation command handler.

**Parameters**:

- `document`: Document to validate
- `context`: IDE skill context

**Returns**: Dict with keys:

- `success`: bool
- `result`: ValidationResult
- `report`: str

---

### Reconciliation Hook

```python
from ascii_diagram_enforcer.hooks.reconciliation import integrate_with_manifest

def integrate_with_manifest(
    document,
    validation_result: ValidationResult,
    context
) -> Dict[str, any]
```

Update reconciliation manifest with validation results.

**Parameters**:

- `document`: Document with manifest
- `validation_result`: Validation results
- `context`: IDE skill context

**Returns**: Dict with keys:

- `manifest_updated`: bool
- `dirty_flag_set`: bool
- `pending_items_added`: int

---

## DDR Integration

### DDRBridge

Integration layer for DDR ecosystem.

#### Constructor

```python
from ascii_diagram_enforcer.integration.ddr_bridge import DDRBridge

bridge = DDRBridge(context)
```

#### validate_traceability_chain

```python
def validate_traceability_chain(
    self,
    sad_tag: str,
    document_content: str
) -> Dict[str, any]
```

Validate complete chain from SAD to BRD.

**Returns**: Dict with keys:

- `is_valid`: bool
- `chain`: List[str] (tag IDs)
- `missing_links`: List[str]

**Example**:

```python
result = bridge.validate_traceability_chain('SAD-1', content)
print(f"Chain: {' → '.join(result['chain'])}")
# Chain: SAD-1 → FSD-1 → BRD-2
```

#### analyze_downstream_impact

```python
def analyze_downstream_impact(self, sad_tag: str) -> Dict[str, any]
```

Find TDD/ISP tags affected by SAD changes.

**Returns**: Dict with keys:

- `affected_tdd`: List[str]
- `affected_isp`: List[str]
- `total_impact`: int

---

## Utility Functions

### Factory Function

```python
from ascii_diagram_enforcer.src import create_enforcer

enforcer = create_enforcer(
    strict_mode=False,
    min_diagram_lines=3
)
```

Create enforcer with default configuration merged with overrides.

---

## Type Aliases

```python
from typing import Dict, List, Set, Optional, Tuple

TagID = str                # e.g., 'SAD-1'
SectionID = str            # e.g., 'sad-root'
RuleID = str               # e.g., 'SAD-DIAGRAM-001'
LineNumber = int           # 1-based line number
ConfidenceScore = float    # 0.0-1.0 range
```

---

## Constants

```python
# Minimum quality thresholds
MIN_COMPONENTS = 2        # Minimum boxes for architecture
MIN_CONNECTIONS = 1       # Minimum arrows/lines
MIN_DIAGRAM_LINES = 3     # Minimum diagram height

# Confidence thresholds
CONFIDENCE_MINIMUM = 0.6  # Minimum for valid detection
CONFIDENCE_HIGH = 0.8     # High-quality diagram
CONFIDENCE_PERFECT = 0.95 # Near-perfect diagram

# Validation rules
RULE_MISSING_DIAGRAM = "SAD-DIAGRAM-001"
RULE_UNRECOGNIZED_CHARS = "SAD-DIAGRAM-002"
RULE_MISSING_RELATIONSHIPS = "SAD-DIAGRAM-003"
RULE_INSUFFICIENT_CLARITY = "SAD-DIAGRAM-004"
```

---

## Error Handling

All validation functions use Result pattern - never raise exceptions for validation failures.

```python
try:
    result = enforcer.validate_section(content, section_id)
    # Always succeeds - check result.is_valid
except FileNotFoundError:
    # Only for I/O errors, not validation errors
    print("Document not found")
```

---

## Complete Example

```python
from pathlib import Path
from ascii_diagram_enforcer.src import (
    ASCIIDiagramEnforcer,
    ViolationSeverity
)

# Initialize enforcer
enforcer = ASCIIDiagramEnforcer(
    strict_mode=True,
    min_diagram_lines=3
)

# Load document
content = Path('docs/04_sad/architecture.rst').read_text()

# Validate
result = enforcer.validate_section(content, 'sad-architecture')

# Check results
if result.is_valid:
    print(f"✓ PASSED")
    print(f"  SAD tags: {result.sad_tags_found}")
    print(f"  Diagrams: {result.diagrams_found}")
else:
    print(f"✗ FAILED")
    print(f"  Violations: {len(result.violations)}")

    # Count by severity
    errors = sum(
        1 for v in result.violations
        if v.severity == ViolationSeverity.ERROR
    )
    warnings = sum(
        1 for v in result.violations
        if v.severity == ViolationSeverity.WARNING
    )

    print(f"  Errors: {errors}, Warnings: {warnings}")

    # Show violations
    for v in result.violations:
        print(f"\n[{v.severity.value}] {v.rule_id}")
        print(f"  Line {v.line_number}: {v.target_tag}")
        print(f"  {v.description}")
        if v.suggested_fix:
            print(f"  Fix: {v.suggested_fix}")

# Generate report
report = enforcer.generate_report(result)
print("\n" + report)

# Convert to reconciliation format
if not result.is_valid:
    pending_item = result.to_reconciliation_item()
    print(f"\nPending Item: {pending_item}")
```

---

## Version History

### 1.0.0 (2026-02-20)

- Initial release
- Core validation engine
- Antigravity IDE integration
- DDR System reconciliation

---

## See Also

- [Usage Guide](usage.md) - User workflows and examples
- [Architecture](architecture.md) - System design details
- [README](../README.md) - Quick start and installation
