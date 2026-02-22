"""
Unit tests for BlockAtomicValidator.

Tests all validation rules against fixture files.
"""

import pytest
from pathlib import Path
import tempfile

from block_atomic_validator.core.validator import BlockAtomicValidator
from block_atomic_validator.core.models import ViolationType


@pytest.fixture
def validator():
    """Create validator instance with default config."""
    return BlockAtomicValidator()


@pytest.fixture
def temp_rst_file():
    """Create temporary RST file for testing."""
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.rst',
        delete=False
    ) as f:
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


class TestBlockAtomicValidator:
    """Test suite for block-atomic validation."""

    def test_valid_structure(self, validator, temp_rst_file):
        """Test validation passes for valid block-atomic structure."""
        content = """
.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Wake word detection stage
   :id: FSD-4.1
   :links: FSD-4

.. fsd:: VAD stage
   :id: FSD-4.2
   :links: FSD-4
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        assert result.is_valid
        assert len(result.violations) == 0
        assert result.total_tags == 3

    def test_ordering_violation(self, validator, temp_rst_file):
        """Test detection of block appearing after atomic."""
        content = """
.. fsd:: Wake word detection stage
   :id: FSD-4.1
   :links: FSD-4

.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        assert not result.is_valid
        assert result.error_count >= 1

        # Find ordering violation
        ordering_violations = [
            v for v in result.violations
            if v.type == ViolationType.ORDERING_VIOLATION
        ]
        assert len(ordering_violations) == 1
        assert "FSD-4" in ordering_violations[0].message
        assert "FSD-4.1" in ordering_violations[0].message

    def test_missing_block_citation(self, validator, temp_rst_file):
        """Test detection of atomic not citing block parent."""
        content = """
.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Wake word detection stage
   :id: FSD-4.1
   :links: BRD-5, NFR-2
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        assert not result.is_valid

        # Find citation violation
        citation_violations = [
            v for v in result.violations
            if v.type == ViolationType.MISSING_BLOCK_CITATION
        ]
        assert len(citation_violations) == 1
        assert "FSD-4.1" in citation_violations[0].tag_id
        assert "FSD-4" in citation_violations[0].related_tag_id

    def test_orphaned_atomic(self, validator, temp_rst_file):
        """Test detection of atomic without corresponding block."""
        content = """
.. fsd:: Wake word detection stage
   :id: FSD-4.1
   :links: FSD-4
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        assert not result.is_valid

        # Find orphan violation
        orphan_violations = [
            v for v in result.violations
            if v.type == ViolationType.ORPHANED_ATOMIC
        ]
        assert len(orphan_violations) == 1
        assert "FSD-4.1" in orphan_violations[0].tag_id
        assert "FSD-4" in orphan_violations[0].related_tag_id

    def test_prefix_mismatch(self, validator, temp_rst_file):
        """Test detection of tier prefix inconsistency."""
        content = """
.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. nfr:: Latency constraint
   :id: NFR-4.1
   :links: FSD-4
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        # Find prefix mismatch violation
        prefix_violations = [
            v for v in result.violations
            if v.type == ViolationType.PREFIX_MISMATCH
        ]
        assert len(prefix_violations) == 1
        assert "NFR-4.1" in prefix_violations[0].tag_id

    def test_multiple_violations(self, validator, temp_rst_file):
        """Test file with multiple violation types."""
        content = """
.. fsd:: Atomic without block
   :id: FSD-1.1
   :links: FSD-1

.. fsd:: Missing citation
   :id: FSD-2.1
   :links: BRD-3

.. fsd:: Block after atomic
   :id: FSD-2
   :links: BRD-3
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        assert not result.is_valid
        assert result.error_count >= 3

        # Should have: orphan, missing citation, ordering
        assert any(
            v.type == ViolationType.ORPHANED_ATOMIC
            for v in result.violations
        )
        assert any(
            v.type == ViolationType.MISSING_BLOCK_CITATION
            for v in result.violations
        )
        assert any(
            v.type == ViolationType.ORDERING_VIOLATION
            for v in result.violations
        )

    def test_complex_valid_structure(self, validator, temp_rst_file):
        """Test complex valid structure with multiple blocks."""
        content = """
.. brd:: Business Objective 1
   :id: BRD-1

.. brd:: Specific requirement 1.1
   :id: BRD-1.1
   :links: BRD-1

.. brd:: Specific requirement 1.2
   :id: BRD-1.2
   :links: BRD-1

.. brd:: Business Objective 2
   :id: BRD-2

.. brd:: Specific requirement 2.1
   :id: BRD-2.1
   :links: BRD-2

.. brd:: Specific requirement 2.2
   :id: BRD-2.2
   :links: BRD-2
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="BRD")

        assert result.is_valid
        assert result.total_tags == 6
        assert len(result.violations) == 0


class TestTagParsing:
    """Test tag parsing functionality."""

    def test_parse_block_tag(self, validator, temp_rst_file):
        """Test parsing of block-level tag."""
        content = """
.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5
"""
        temp_rst_file.write_text(content)

        result = validator.validate_file(temp_rst_file, tier="FSD")

        assert len(result.violations) == 0
        tags = validator.parser.parse_tags(content)
        assert len(tags) == 1
        assert tags[0].is_block
        assert not tags[0].is_atomic

    def test_parse_atomic_tag(self, validator, temp_rst_file):
        """Test parsing of atomic-level tag."""
        content = """
.. fsd:: Voice Pipeline
   :id: FSD-4
   :links: BRD-5

.. fsd:: Wake word detection
   :id: FSD-4.1
   :links: FSD-4
"""
        temp_rst_file.write_text(content)

        tags = validator.parser.parse_tags(content)
        assert len(tags) == 2
        assert tags[1].is_atomic
        assert not tags[1].is_block
        assert tags[1].get_block_id() == "FSD-4"


class TestProjectValidation:
    """Test project-wide validation."""

    def test_validate_empty_project(self, validator):
        """Test validation of project with no docs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            results = validator.validate_project(project_root)
            assert len(results) == 0

    def test_validate_project_with_files(self, validator):
        """Test validation of project with multiple files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            docs_dir = project_root / "docs" / "03_fsd"
            docs_dir.mkdir(parents=True)

            # Create test files
            file1 = docs_dir / "fsd1.rst"
            file1.write_text("""
.. fsd:: Valid Block
   :id: FSD-1
   :links: BRD-1

.. fsd:: Valid Atomic
   :id: FSD-1.1
   :links: FSD-1
""")

            file2 = docs_dir / "fsd2.rst"
            file2.write_text("""
.. fsd:: Invalid Atomic
   :id: FSD-2.1
   :links: FSD-2
""")

            results = validator.validate_project(project_root)

            assert len(results) == 2
            assert results[0].is_valid  # file1 valid
            assert not results[1].is_valid  # file2 has orphan


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
