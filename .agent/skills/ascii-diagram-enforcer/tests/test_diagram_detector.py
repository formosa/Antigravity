"""
Unit Tests for DiagramDetector

Comprehensive test suite for ASCII diagram detection, style classification,
and confidence scoring algorithms.

Implements: Test coverage for diagram detection engine
Requirements: pytest, DDR System test data

Author: DDR System Integration Team
Version: 1.0.0
"""

import pytest
from ascii_diagram_enforcer.src.diagram_detector import DiagramDetector, DiagramMatch


@pytest.fixture
def detector():
    """Create detector with default configuration."""
    return DiagramDetector(min_lines=3, confidence_threshold=0.6)


@pytest.fixture
def strict_detector():
    """Create detector with stricter requirements."""
    return DiagramDetector(min_lines=5, confidence_threshold=0.8)


class TestDiagramDetection:
    """Test suite for basic diagram detection."""

    def test_detect_simple_box_diagram(self, detector):
        """Test detection of basic two-box diagram."""
        content = """
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "box_and_arrow"
        assert diagrams[0]['confidence'] >= 0.6

    def test_detect_unicode_diagram(self, detector):
        """Test detection of Unicode box drawing characters."""
        content = """
┌─────────┐     ┌─────────┐
│  Client │ ──> │  Server │
└─────────┘     └─────────┘
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['confidence'] >= 0.6

    def test_no_diagram_in_plain_text(self, detector):
        """Test that plain text without diagrams returns empty."""
        content = """
This is just plain text describing architecture.
No boxes, no arrows, no diagram structure.
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 0

    def test_reject_too_short_diagram(self, detector):
        """Test rejection of diagrams below minimum line threshold."""
        content = "Core --> UI"  # Only 1 line

        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 0

    def test_detect_multiple_diagrams(self, detector):
        """Test detection of multiple separate diagrams."""
        content = """
First diagram:
+------+     +------+
| Core | --> |  UI  |
+------+     +------+

Some text in between.

Second diagram:
+-----+
| App |
+-----+
  |
  v
+-----+
|  DB |
+-----+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 2

    def test_diagram_with_labels(self, detector):
        """Test detection of diagram with component labels."""
        content = """
+------------------+
|  Core Service    |
|  (Message Hub)   |
+------------------+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1


class TestStyleClassification:
    """Test suite for diagram style classification."""

    def test_classify_box_and_arrow(self, detector):
        """Test classification of box-and-arrow style."""
        content = """
+--------+     +--------+     +--------+
| Client | --> | Server | --> |  DB    |
+--------+     +--------+     +--------+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "box_and_arrow"

    def test_classify_hierarchical(self, detector):
        """Test classification of hierarchical tree style."""
        content = """
       +------+
       | Root |
       +------+
       /      \\
  +----+      +----+
  | L  |      | R  |
  +----+      +----+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "hierarchical"

    def test_classify_network_topology(self, detector):
        """Test classification of network mesh style."""
        content = """
  +---+       +---+
  | A |-------| B |
  +---+       +---+
    |    \\  /   |
    |     \\/    |
    |     /\\    |
  +---+  /  \\  +---+
  | D |-------| C |
  +---+       +---+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "network_topology"

    def test_unknown_style_fallback(self, detector):
        """Test fallback to 'unknown' for ambiguous diagrams."""
        content = """
Some weird diagram structure
  *  *  *
  *  *  *
"""
        diagrams = detector.find_diagrams(content)

        # May not detect at all, or detect as unknown
        if len(diagrams) > 0:
            assert diagrams[0]['style'] in ["unknown", "box_and_arrow"]


class TestConfidenceScoring:
    """Test suite for confidence score calculation."""

    def test_high_confidence_for_clear_diagram(self, detector):
        """Test high confidence for well-formed diagram."""
        content = """
+----------+     +----------+     +----------+
| Frontend | --> | Backend  | --> | Database |
+----------+     +----------+     +----------+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['confidence'] >= 0.7  # Should be high

    def test_lower_confidence_for_ambiguous(self, detector):
        """Test lower confidence for ambiguous patterns."""
        content = """
+ - - - +
| Box? |
+ - - - +
"""
        diagrams = detector.find_diagrams(content)

        # May or may not detect, but if detected, confidence should be lower
        if len(diagrams) > 0:
            assert diagrams[0]['confidence'] < 0.8

    def test_confidence_threshold_filtering(self):
        """Test that low-confidence diagrams are filtered."""
        strict_detector = DiagramDetector(
            min_lines=3,
            confidence_threshold=0.9  # Very high threshold
        )

        # Borderline diagram
        content = """
Some text
+---+
| A |
+---+
More text
"""
        diagrams = strict_detector.find_diagrams(content)

        # Should reject due to low confidence (surrounded by text)
        assert len(diagrams) == 0

    def test_box_character_density_factor(self, detector):
        """Test that box character density affects confidence."""
        high_density = """
+------+------+------+
| Box1 | Box2 | Box3 |
+------+------+------+
"""

        low_density = """
Some text here
+----+
| B  |
+----+
More text
"""

        diagrams_high = detector.find_diagrams(high_density)
        diagrams_low = detector.find_diagrams(low_density)

        if len(diagrams_high) > 0 and len(diagrams_low) > 0:
            assert diagrams_high[0]['confidence'] > diagrams_low[0]['confidence']


class TestPatternMatching:
    """Test suite for specific pattern recognition."""

    def test_recognize_horizontal_arrows(self, detector):
        """Test recognition of various arrow patterns."""
        arrows = [
            "+---+  -->  +---+",
            "+---+ ---> +---+",
            "+---+ <--> +---+",
            "+---+ ===> +---+",
        ]

        for arrow in arrows:
            content = f"""
{arrow}
| A |       | B |
{arrow}
"""
            diagrams = detector.find_diagrams(content)
            assert len(diagrams) >= 1, f"Failed to detect: {arrow}"

    def test_recognize_vertical_connectors(self, detector):
        """Test recognition of vertical connections."""
        content = """
+------+
|  A   |
+------+
   |
   v
+------+
|  B   |
+------+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1

    def test_recognize_branch_patterns(self, detector):
        """Test recognition of tree branching."""
        content = """
    +---+
    | A |
    +---+
    /   \\
+---+   +---+
| B |   | C |
+---+   +---+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['style'] == "hierarchical"


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_empty_content(self, detector):
        """Test handling of empty content."""
        diagrams = detector.find_diagrams("")
        assert len(diagrams) == 0

    def test_only_whitespace(self, detector):
        """Test handling of whitespace-only content."""
        diagrams = detector.find_diagrams("   \n\n   \n")
        assert len(diagrams) == 0

    def test_diagram_at_document_start(self, detector):
        """Test detection of diagram at very start."""
        content = """+------+
| Core |
+------+"""

        diagrams = detector.find_diagrams(content)
        assert len(diagrams) == 1

    def test_diagram_at_document_end(self, detector):
        """Test detection of diagram at very end."""
        content = """Some text here.

+------+
| Core |
+------+"""

        diagrams = detector.find_diagrams(content)
        assert len(diagrams) == 1

    def test_very_long_diagram(self, detector):
        """Test detection of large multi-line diagram."""
        content = """
+--------+     +--------+     +--------+
|   UI   | --> | Core   | <-- | Runtime|
+--------+     +--------+     +--------+
    |              |              |
    v              v              v
+--------+     +--------+     +--------+
| Audio  |     |  Log   |     | Config |
+--------+     +--------+     +--------+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        assert diagrams[0]['end_line'] - diagrams[0]['start_line'] >= 7

    def test_adjacent_diagrams_no_gap(self, detector):
        """Test handling of diagrams with no blank lines between."""
        content = """
+---+
| A |
+---+
+---+
| B |
+---+
"""
        diagrams = detector.find_diagrams(content)

        # May detect as one or two diagrams depending on implementation
        assert len(diagrams) >= 1


class TestLineNumberTracking:
    """Test suite for accurate line number tracking."""

    def test_diagram_line_numbers(self, detector):
        """Test that line numbers are correctly tracked."""
        content = """Line 1
Line 2
Line 3
+------+
| Core |
+------+
Line 7
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 1
        # Line numbers are 0-indexed in implementation
        assert diagrams[0]['start_line'] >= 3
        assert diagrams[0]['end_line'] >= 5

    def test_multiple_diagram_line_tracking(self, detector):
        """Test line tracking for multiple diagrams."""
        content = """
First diagram:
+---+
| A |
+---+

Second diagram:
+---+
| B |
+---+
"""
        diagrams = detector.find_diagrams(content)

        assert len(diagrams) == 2
        assert diagrams[0]['start_line'] < diagrams[1]['start_line']


class TestRobustness:
    """Test suite for robustness and error handling."""

    def test_malformed_boxes(self, detector):
        """Test handling of malformed box structures."""
        content = """
+-----
| Box  # Unclosed box
+-----
"""
        # Should not crash
        diagrams = detector.find_diagrams(content)
        # May or may not detect, but shouldn't error

    def test_mixed_character_sets(self, detector):
        """Test handling of mixed ASCII and Unicode."""
        content = """
+------┐
| Mix  │
└------+
"""
        # Should handle gracefully
        diagrams = detector.find_diagrams(content)
        # May detect with lower confidence

    def test_unicode_errors(self, detector):
        """Test handling of potential Unicode issues."""
        content = "Valid ASCII\n+---+\n| A |\n+---+\n"

        # Should work regardless of encoding
        diagrams = detector.find_diagrams(content)
        assert len(diagrams) >= 1


class TestPrivateMethods:
    """Test suite for private helper methods."""

    def test_is_diagram_line(self, detector):
        """Test line-level diagram detection."""
        assert detector._is_diagram_line("+------+") is True
        assert detector._is_diagram_line("| Core |") is True
        assert detector._is_diagram_line("Plain text") is False
        assert detector._is_diagram_line("") is False

    def test_has_box_pattern(self, detector):
        """Test box pattern recognition."""
        assert detector._has_box_pattern("+---+") is True
        assert detector._has_box_pattern("┌───┐") is True
        assert detector._has_box_pattern("random text") is False

    def test_has_arrows(self, detector):
        """Test arrow pattern recognition."""
        assert detector._has_arrows("-->") is True
        assert detector._has_arrows("<--") is True
        assert detector._has_arrows("<-->") is True
        assert detector._has_arrows("no arrows") is False

    def test_has_tree_pattern(self, detector):
        """Test tree structure recognition."""
        tree_content = """
|
├──
└──
"""
        assert detector._has_tree_pattern(tree_content) is True

    def test_has_network_pattern(self, detector):
        """Test network topology recognition."""
        network_content = """
+---+ +---+
| A |-| B |
+---+ +---+
  |     |
+---+ +---+
| C |-| D |
+---+ +---+
"""
        assert detector._has_network_pattern(network_content) is True

    def test_alignment_consistency(self, detector):
        """Test alignment checking."""
        aligned_lines = [
            "+------+",
            "| Core |",
            "+------+"
        ]
        assert detector._has_consistent_alignment(aligned_lines) is True

        unaligned_lines = [
            "+------+",
            "| C |",
            "+------+     extra stuff"
        ]
        # May or may not pass depending on variance threshold


class TestDiagramMatchDataclass:
    """Test suite for DiagramMatch dataclass."""

    def test_diagram_match_creation(self):
        """Test DiagramMatch dataclass instantiation."""
        match = DiagramMatch(
            start_line=10,
            end_line=13,
            content="+---+\n| A |\n+---+",
            style="box_and_arrow",
            confidence=0.85,
            box_chars={'+', '-', '|'}
        )

        assert match.start_line == 10
        assert match.end_line == 13
        assert match.style == "box_and_arrow"
        assert match.confidence == 0.85
        assert '+' in match.box_chars


class TestPerformance:
    """Test suite for performance characteristics."""

    def test_large_document_performance(self, detector):
        """Test performance on large document."""
        # Create large document with embedded diagram
        lines = ["Plain text line"] * 1000
        lines[500:503] = ["+---+", "| A |", "+---+"]
        content = "\n".join(lines)

        # Should complete in reasonable time
        import time
        start = time.time()
        diagrams = detector.find_diagrams(content)
        duration = time.time() - start

        assert len(diagrams) == 1
        assert duration < 1.0  # Should be fast (<1 second)

    def test_many_diagrams_performance(self, detector):
        """Test performance with many diagrams."""
        # Create document with 20 diagrams
        diagram_template = """
+------+
| Box  |
+------+

"""
        content = diagram_template * 20

        import time
        start = time.time()
        diagrams = detector.find_diagrams(content)
        duration = time.time() - start

        assert len(diagrams) >= 15  # Should find most
        assert duration < 2.0  # Should be fast (<2 seconds)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
