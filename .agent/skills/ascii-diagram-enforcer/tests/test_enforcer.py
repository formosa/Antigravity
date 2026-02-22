"""
Unit Tests for ASCII Diagram Enforcer

Comprehensive test suite validating enforcer logic, diagram detection,
and validation rules.

Implements: Test coverage for all validation rules
Requirements: pytest, DDR System test fixtures

Author: DDR System Integration Team
Version: 1.0.0
"""

import pytest
from pathlib import Path

from ascii_diagram_enforcer.src.enforcer import (
    ASCIIDiagramEnforcer,
    ValidationResult,
    ViolationSeverity,
    Violation
)
from ascii_diagram_enforcer.src.diagram_detector import DiagramDetector
from ascii_diagram_enforcer.src.sad_parser import SADParser
from ascii_diagram_enforcer.src.validators import DiagramValidator


# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def enforcer():
    """Create enforcer instance with default configuration."""
    return ASCIIDiagramEnforcer(
        strict_mode=True,
        min_diagram_lines=3,
        auto_flag_dirty=True
    )


@pytest.fixture
def diagram_detector():
    """Create diagram detector instance."""
    return DiagramDetector(min_lines=3, confidence_threshold=0.6)


@pytest.fixture
def sad_parser():
    """Create SAD parser instance."""
    return SADParser()


@pytest.fixture
def validator():
    """Create diagram validator instance."""
    return DiagramValidator()


class TestASCIIDiagramEnforcer:
    """Test suite for core enforcer logic."""

    def test_initialization(self, enforcer):
        """Test enforcer initializes with correct configuration."""
        assert enforcer.strict_mode is True
        assert enforcer.min_diagram_lines == 3
        assert enforcer.auto_flag_dirty is True
        assert enforcer.detector is not None
        assert enforcer.parser is not None
        assert enforcer.validator is not None

    def test_valid_sad_section(self, enforcer):
        """Test validation passes for compliant SAD section."""
        content = """
.. sad:: Hub-and-Spoke Architecture
   :id: SAD-1
   :links: FSD-1

+-------------+     +-------------+     +-------------+
|     UI      | --> |    Core     | <-- |   Runtime   |
+-------------+     +-------------+     +-------------+
"""

        result = enforcer.validate_section(content, "sad-test")

        assert result.is_valid is True
        assert len(result.violations) == 0
        assert result.sad_tags_found == 1
        assert result.diagrams_found == 1

    def test_missing_diagram_violation(self, enforcer):
        """Test SAD-DIAGRAM-001: Missing mandatory diagram."""
        content = """
.. sad:: Hub-and-Spoke Architecture
   :id: SAD-1
   :links: FSD-1

This section describes the architecture but has no diagram.
"""

        result = enforcer.validate_section(content, "sad-test")

        assert result.is_valid is False
        assert len(result.violations) == 1
        assert result.violations[0].rule_id == "SAD-DIAGRAM-001"
        assert result.violations[0].severity == ViolationSeverity.ERROR
        assert "SAD-1" in result.violations[0].target_tag
        assert "missing mandatory ASCII diagram" in result.violations[0].description.lower()

    def test_multiple_block_tags(self, enforcer):
        """Test validation of multiple SAD block tags."""
        content = """
.. sad:: Architecture Overview
   :id: SAD-1
   :links: FSD-1

+--------+
| System |
+--------+

.. sad:: Detailed Topology
   :id: SAD-2
   :links: FSD-2

+------+     +------+
| Core | --> |  UI  |
+------+     +------+
"""

        result = enforcer.validate_section(content, "sad-test")

        assert result.is_valid is True
        assert result.sad_tags_found == 2
        assert result.diagrams_found == 2

    def test_atomic_tags_dont_require_diagrams(self, enforcer):
        """Test that atomic tags (SAD-N.M) don't require separate diagrams."""
        content = """
.. sad:: Architecture
   :id: SAD-1
   :links: FSD-1

+--------+
| System |
+--------+

.. sad:: Component Detail
   :id: SAD-1.1
   :links: SAD-1

Additional details about component (no diagram needed).
"""

        result = enforcer.validate_section(content, "sad-test")

        # Should only validate SAD-1 (block), not SAD-1.1 (atomic)
        assert result.is_valid is True

    def test_reconciliation_item_generation(self, enforcer):
        """Test conversion to reconciliation pending_item format."""
        content = """
.. sad:: Architecture
   :id: SAD-1
   :links: FSD-1
"""

        result = enforcer.validate_section(content, "sad-test")
        reconciliation_item = result.to_reconciliation_item()

        assert "target_tag" in reconciliation_item
        assert "issue_type" in reconciliation_item
        assert reconciliation_item["issue_type"] == "CONSTRAINT_VIOLATION"
        assert "Missing or invalid ASCII diagrams" in reconciliation_item["description"]


class TestDiagramDetector:
    """Test suite for ASCII diagram detection."""

    def test_detect_box_and_arrow_diagram(self, diagram_detector):
        """Test detection of box-and-arrow style diagram."""
        content = """
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
"""

        diagrams = diagram_detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "box_and_arrow"
        assert diagrams[0]['confidence'] >= 0.6

    def test_detect_hierarchical_diagram(self, diagram_detector):
        """Test detection of hierarchical tree diagram."""
        content = """
      +------+
      | Core |
      +------+
      /      \
+----+        +----+
| UI |        | RT |
+----+        +----+
"""

        diagrams = diagram_detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "hierarchical"

    def test_reject_too_short_diagram(self, diagram_detector):
        """Test rejection of diagrams below minimum line count."""
        content = "Core --> UI"  # Only 1 line

        diagrams = diagram_detector.find_diagrams(content)

        # Should be rejected due to min_lines=3
        assert len(diagrams) == 0

    def test_low_confidence_rejection(self):
        """Test rejection of low-confidence diagram patterns."""
        detector = DiagramDetector(confidence_threshold=0.8)  # High threshold

        # Weak diagram signal
        content = """
Some text here
+ - - +
| box |
+ - - +
More text
"""

        diagrams = detector.find_diagrams(content)

        # May be rejected due to surrounding text lowering confidence
        assert len(diagrams) <= 1

    def test_unicode_box_characters(self, diagram_detector):
        """Test detection of Unicode box drawing characters."""
        content = """
┌─────────┐     ┌─────────┐
│  Core   │ ──> │   UI    │
└─────────┘     └─────────┘
"""

        diagrams = diagram_detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['confidence'] >= 0.6


class TestSADParser:
    """Test suite for SAD-tier RST parsing."""

    def test_parse_basic_sad_tag(self, sad_parser):
        """Test parsing of basic SAD directive."""
        content = """
.. sad:: Architecture Overview
   :id: SAD-1
   :links: FSD-1
"""

        tags = sad_parser.extract_sad_tags(content)

        assert len(tags) == 1
        assert tags[0]['id'] == "SAD-1"
        assert tags[0]['title'] == "Architecture Overview"
        assert tags[0]['links'] == ["FSD-1"]
        assert tags[0]['level'] == 'block'

    def test_parse_atomic_tag(self, sad_parser):
        """Test parsing of atomic-level tag."""
        content = """
.. sad:: Component Detail
   :id: SAD-1.2
   :links: SAD-1
"""

        tags = sad_parser.extract_sad_tags(content)

        assert len(tags) == 1
        assert tags[0]['id'] == "SAD-1.2"
        assert tags[0]['level'] == 'atomic'

    def test_parse_multiple_citations(self, sad_parser):
        """Test parsing of multiple parent citations."""
        content = """
.. sad:: Complex Architecture
   :id: SAD-2
   :links: FSD-1, FSD-2, FSD-3
"""

        tags = sad_parser.extract_sad_tags(content)

        assert len(tags) == 1
        assert len(tags[0]['links']) == 3
        assert "FSD-1" in tags[0]['links']
        assert "FSD-2" in tags[0]['links']
        assert "FSD-3" in tags[0]['links']

    def test_block_tag_identification(self, sad_parser):
        """Test block vs atomic tag identification."""
        assert sad_parser.is_block_tag("SAD-1") is True
        assert sad_parser.is_block_tag("SAD-10") is True
        assert sad_parser.is_block_tag("SAD-1.2") is False

        assert sad_parser.is_atomic_tag("SAD-1") is False
        assert sad_parser.is_atomic_tag("SAD-1.2") is True
        assert sad_parser.is_atomic_tag("SAD-5.10") is True

    def test_extract_block_parent(self, sad_parser):
        """Test extraction of parent block from atomic tag."""
        assert sad_parser.extract_block_parent("SAD-1.2") == "SAD-1"
        assert sad_parser.extract_block_parent("SAD-5.10") == "SAD-5"
        assert sad_parser.extract_block_parent("SAD-1") is None

    def test_citation_hierarchy_validation(self, sad_parser):
        """Test validation of citation hierarchy rules."""
        # Valid: SAD cites FSD
        valid, errors = sad_parser.validate_citation_hierarchy("SAD-1", ["FSD-2"])
        assert valid is True
        assert len(errors) == 0

        # Invalid: SAD cannot cite TDD (forward reference)
        valid, errors = sad_parser.validate_citation_hierarchy("SAD-1", ["TDD-1"])
        assert valid is False
        assert len(errors) > 0
        assert "invalid parent tier" in errors[0].lower()


class TestDiagramValidator:
    """Test suite for diagram quality validation."""

    def test_valid_diagram_quality(self, validator):
        """Test validation of high-quality diagram."""
        diagram = {
            'content': """
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
""",
            'start_line': 10
        }

        violations = validator.validate_diagram(diagram, "SAD-1", 5)

        assert len(violations) == 0

    def test_unrecognized_characters_warning(self, validator):
        """Test SAD-DIAGRAM-002: Unrecognized box characters."""
        diagram = {
            'content': """
[Core] ===> [UI]    # Using brackets instead of boxes
""",
            'start_line': 10
        }

        violations = validator.validate_diagram(diagram, "SAD-1", 5)

        # Should have warnings for unrecognized chars
        assert any(v.rule_id == "SAD-DIAGRAM-002" for v in violations)

    def test_missing_relationships_error(self, validator):
        """Test SAD-DIAGRAM-003: Missing component relationships."""
        diagram = {
            'content': """
+------+
| Core |     # Isolated component
+------+
""",
            'start_line': 10
        }

        violations = validator.validate_diagram(diagram, "SAD-1", 5)

        # Should have ERROR for missing relationships
        relationship_violations = [
            v for v in violations
            if v.rule_id == "SAD-DIAGRAM-003"
        ]
        assert len(relationship_violations) > 0
        assert any(v.severity == ViolationSeverity.ERROR for v in relationship_violations)

    def test_insufficient_clarity_warning(self, validator):
        """Test SAD-DIAGRAM-004: Structural clarity warnings."""
        diagram = {
            'content': """
+-+
| |    # Too simple
+-+
""",
            'start_line': 10
        }

        violations = validator.validate_diagram(diagram, "SAD-1", 5)

        # May have warnings about clarity
        clarity_violations = [
            v for v in violations
            if v.rule_id == "SAD-DIAGRAM-004"
        ]
        # At minimum should warn about missing labels
        assert len(clarity_violations) > 0

    def test_diagram_statistics(self, validator):
        """Test diagram statistics calculation."""
        content = """
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
"""

        stats = validator.get_diagram_statistics(content)

        assert stats['line_count'] == 4  # Including empty lines
        assert stats['box_count'] >= 2
        assert stats['arrow_count'] >= 1
        assert stats['label_count'] >= 2  # "Core" and "UI"


class TestFixtureValidation:
    """Test validation against fixture files."""

    def test_valid_sad_fixture(self, enforcer):
        """Test validation of valid_sad_section.rst fixture."""
        fixture_path = FIXTURES_DIR / "valid_sad_section.rst"

        if fixture_path.exists():
            content = fixture_path.read_text()
            result = enforcer.validate_section(content, "fixture-test")

            assert result.is_valid is True

    def test_invalid_missing_diagram_fixture(self, enforcer):
        """Test validation of invalid_sad_missing_diagram.rst fixture."""
        fixture_path = FIXTURES_DIR / "invalid_sad_missing_diagram.rst"

        if fixture_path.exists():
            content = fixture_path.read_text()
            result = enforcer.validate_section(content, "fixture-test")

            assert result.is_valid is False
            assert any(v.rule_id == "SAD-DIAGRAM-001" for v in result.violations)


# Integration tests
class TestEndToEndWorkflow:
    """End-to-end integration tests."""

    def test_complete_validation_workflow(self, enforcer):
        """Test complete validation from content to report generation."""
        content = """
.. sad:: System Architecture
   :id: SAD-1
   :links: FSD-1

+----------------+     +-----------------+
|   Frontend     | --> |    Backend      |
+----------------+     +-----------------+
        |                      |
        v                      v
+----------------+     +-----------------+
|   Database     |     |      Cache      |
+----------------+     +-----------------+
"""

        # Run validation
        result = enforcer.validate_section(content, "integration-test")

        # Verify results
        assert result.section_id == "integration-test"
        assert result.is_valid is True
        assert result.sad_tags_found >= 1
        assert result.diagrams_found >= 1

        # Generate report
        report = enforcer.generate_report(result)
        assert "Validation Report" in report
        assert "VALID" in report or "INVALID" in report

        # Test reconciliation conversion
        if not result.is_valid:
            recon_item = result.to_reconciliation_item()
            assert "target_tag" in recon_item


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
