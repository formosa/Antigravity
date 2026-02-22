"""
Unit tests for scoring matrix functionality.

Tests the 10-factor detection and scoring calculations from
classification-scoring.md.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pytest
from scoring_matrix import ScoringMatrix, FactorPresence
from utils import load_config


@pytest.fixture
def scoring_matrix():
    """Create scoring matrix with default config."""
    config = load_config("config/scoring_weights.yaml")
    return ScoringMatrix(config)


class TestFactorDetection:
    """Test individual factor detection methods."""

    def test_numeric_metrics_detection(self, scoring_matrix):
        """Test Factor 1: Numeric metrics detection."""
        # Strong presence
        fragment1 = "System must respond in < 1 second with 99.9% uptime"
        result1 = scoring_matrix._detect_numeric_metrics(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "Latency must be under 100ms"
        result2 = scoring_matrix._detect_numeric_metrics(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "System must be fast and reliable"
        result3 = scoring_matrix._detect_numeric_metrics(fragment3)
        assert result3 == FactorPresence.NONE

    def test_hardware_reference_detection(self, scoring_matrix):
        """Test Factor 2: Hardware reference detection."""
        # Strong presence
        fragment1 = "GPU VRAM must be 10GB dedicated for model inference"
        result1 = scoring_matrix._detect_hardware_reference(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "CPU-bound processing required"
        result2 = scoring_matrix._detect_hardware_reference(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "System processes user requests"
        result3 = scoring_matrix._detect_hardware_reference(fragment3)
        assert result3 == FactorPresence.NONE

    def test_user_behavior_detection(self, scoring_matrix):
        """Test Factor 3: User behavior detection."""
        # Strong presence
        fragment1 = "User speaks wake word, system responds, user sees feedback"
        result1 = scoring_matrix._detect_user_behavior(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "User receives notification"
        result2 = scoring_matrix._detect_user_behavior(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "System processes internal messages"
        result3 = scoring_matrix._detect_user_behavior(fragment3)
        assert result3 == FactorPresence.NONE

    def test_pattern_names_detection(self, scoring_matrix):
        """Test Factor 4: Architectural pattern names."""
        # Strong presence
        fragment1 = "Hub-and-Spoke pattern with DEALER-ROUTER topology"
        result1 = scoring_matrix._detect_pattern_names(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "Singleton pattern for configuration"
        result2 = scoring_matrix._detect_pattern_names(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "Process handles requests"
        result3 = scoring_matrix._detect_pattern_names(fragment3)
        assert result3 == FactorPresence.NONE

    def test_schema_definition_detection(self, scoring_matrix):
        """Test Factor 5: JSON/YAML schema definitions."""
        # Strong presence
        fragment1 = '{"source": "string", "priority": integer, "payload": object}'
        result1 = scoring_matrix._detect_schema_definition(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "field: value in YAML format"
        result2 = scoring_matrix._detect_schema_definition(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "System stores data"
        result3 = scoring_matrix._detect_schema_definition(fragment3)
        assert result3 == FactorPresence.NONE

    def test_class_names_detection(self, scoring_matrix):
        """Test Factor 6: Class name (PascalCase) detection."""
        # Strong presence
        fragment1 = "CoreProcess and RuntimeProcess classes"
        result1 = scoring_matrix._detect_class_names(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "LogServer component"
        result2 = scoring_matrix._detect_class_names(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "process handles messages"
        result3 = scoring_matrix._detect_class_names(fragment3)
        assert result3 == FactorPresence.NONE

    def test_executable_code_detection(self, scoring_matrix):
        """Test Factor 7: Executable code detection."""
        # Strong presence
        fragment1 = "def run(self):\n    import zmq\n    return None"
        result1 = scoring_matrix._detect_executable_code(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "class CoreProcess:"
        result2 = scoring_matrix._detect_executable_code(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "Process executes logic"
        result3 = scoring_matrix._detect_executable_code(fragment3)
        assert result3 == FactorPresence.NONE

    def test_modal_keywords_detection(self, scoring_matrix):
        """Test Factor 8: RFC 2119 modal keywords."""
        # Strong presence
        fragment1 = "System MUST handle requests and SHOULD validate inputs"
        result1 = scoring_matrix._detect_modal_keywords(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "Required functionality"
        result2 = scoring_matrix._detect_modal_keywords(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "System handles requests"
        result3 = scoring_matrix._detect_modal_keywords(fragment3)
        assert result3 == FactorPresence.NONE

    def test_rationale_detection(self, scoring_matrix):
        """Test Factor 9: Rationale/justification detection."""
        # Strong presence
        fragment1 = "System enables debugging because centralized logs facilitate correlation"
        result1 = scoring_matrix._detect_rationale(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "In order to improve performance"
        result2 = scoring_matrix._detect_rationale(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence
        fragment3 = "System processes requests"
        result3 = scoring_matrix._detect_rationale(fragment3)
        assert result3 == FactorPresence.NONE

    def test_technology_agnostic_detection(self, scoring_matrix):
        """Test Factor 10: Technology-agnostic language (inverse)."""
        # Strong presence (agnostic)
        fragment1 = "System enables real-time interaction"
        result1 = scoring_matrix._detect_technology_agnostic(fragment1)
        assert result1 == FactorPresence.YES

        # Partial presence
        fragment2 = "System uses Python for processing"
        result2 = scoring_matrix._detect_technology_agnostic(fragment2)
        assert result2 == FactorPresence.PARTIAL

        # No presence (tech-specific)
        fragment3 = "ZeroMQ DEALER socket with PyTorch inference"
        result3 = scoring_matrix._detect_technology_agnostic(fragment3)
        assert result3 == FactorPresence.NONE


class TestScoringMatrix:
    """Test complete scoring matrix functionality."""

    def test_analyze_fragment_comprehensive(self, scoring_matrix):
        """Test complete fragment analysis with multiple factors."""
        fragment = (
            "System MUST aggregate all log messages into a single file "
            "with automatic rotation every 50MB and retain logs for 30 days"
        )

        factors = scoring_matrix.analyze_fragment(fragment)

        # Should detect numeric metrics
        assert factors['numeric_metrics'] != FactorPresence.NONE

        # Should detect modal keywords
        assert factors['modal_keywords'] != FactorPresence.NONE

        # Should be technology-agnostic
        assert factors['technology_agnostic'] == FactorPresence.YES

        # Should NOT detect code
        assert factors['executable_code'] == FactorPresence.NONE

    def test_get_weights(self, scoring_matrix):
        """Test weight retrieval for factors."""
        weights = scoring_matrix.get_weights('numeric_metrics')

        assert 'NFR' in weights
        assert weights['NFR'] == 3
        assert weights['ICD'] == 2

    def test_all_factors_present(self, scoring_matrix):
        """Test that all 10 factors are analyzed."""
        fragment = "Test fragment"
        factors = scoring_matrix.analyze_fragment(fragment)

        expected_factors = [
            'numeric_metrics',
            'hardware_reference',
            'user_behavior',
            'pattern_names',
            'schema_definition',
            'class_names',
            'executable_code',
            'modal_keywords',
            'includes_rationale',
            'technology_agnostic'
        ]

        for factor in expected_factors:
            assert factor in factors
            assert isinstance(factors[factor], FactorPresence)


class TestRealWorldFragments:
    """Test scoring on real-world DDR fragments."""

    def test_clear_nfr_fragment(self, scoring_matrix):
        """Test fragment that clearly belongs to NFR."""
        fragment = "IPC Dispatch: Sub-millisecond (< 1ms) for metadata-only"
        factors = scoring_matrix.analyze_fragment(fragment)

        # Strong numeric metrics
        assert factors['numeric_metrics'] in [FactorPresence.YES, FactorPresence.PARTIAL]

        # Likely has modal language
        # Technology-specific is okay for NFR
        assert factors['technology_agnostic'] in [FactorPresence.PARTIAL, FactorPresence.NONE]

    def test_clear_brd_fragment(self, scoring_matrix):
        """Test fragment that clearly belongs to BRD."""
        fragment = "Enable comprehensive debugging through correlated, centralized logging"
        factors = scoring_matrix.analyze_fragment(fragment)

        # Should be technology-agnostic
        assert factors['technology_agnostic'] == FactorPresence.YES

        # Should have rationale
        assert factors['includes_rationale'] != FactorPresence.NONE

        # Should NOT have code
        assert factors['executable_code'] == FactorPresence.NONE

    def test_clear_isp_fragment(self, scoring_matrix):
        """Test fragment that clearly belongs to ISP."""
        fragment = "def run(self) -> None:\n    pass"
        factors = scoring_matrix.analyze_fragment(fragment)

        # Should have executable code
        assert factors['executable_code'] != FactorPresence.NONE

        # Should NOT be technology-agnostic
        assert factors['technology_agnostic'] != FactorPresence.YES


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
