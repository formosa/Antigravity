"""
10-factor scoring matrix for DDR tier classification.

Implements the scoring weights from classification-scoring.md §Step 1.
"""

import re
from typing import Dict, List
from enum import Enum


class FactorPresence(Enum):
    """Factor presence levels for scoring adjustment."""
    NONE = "none"
    PARTIAL = "partial"
    YES = "yes"


class ScoringMatrix:
    """
    Multi-factor scoring matrix for tier ambiguity resolution.

    Implements the 10-factor weights from classification-scoring.md:
    1. Contains numeric metrics
    2. References hardware
    3. Describes user behavior
    4. Names patterns
    5. Defines JSON/YAML
    6. Contains class names
    7. Has executable code
    8. Uses "must/shall"
    9. Includes rationale
    10. Technology-agnostic

    Parameters
    ----------
    weights_config : Dict
        Tier weights per factor from configuration.

    Attributes
    ----------
    factors : List[str]
        All 10 factor names.
    weights : Dict[str, Dict[str, int]]
        Weight lookup: factor -> tier -> weight.

    Examples
    --------
    >>> matrix = ScoringMatrix(config)
    >>> factors = matrix.analyze_fragment("System must handle < 1ms latency")
    >>> print(factors['numeric_metrics'])
    FactorPresence.YES
    """

    def __init__(self, weights_config: Dict):
        """
        Initialize scoring matrix with tier weights.

        Implements: classification-scoring.md Step 1 matrix
        """
        self.weights = weights_config
        self.factors = [
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

    def analyze_fragment(self, fragment: str) -> Dict[str, FactorPresence]:
        """
        Analyze fragment and detect presence of all 10 factors.

        Parameters
        ----------
        fragment : str
            Information fragment to analyze.

        Returns
        -------
        Dict[str, FactorPresence]
            Presence level for each factor.
        """
        return {
            'numeric_metrics': self._detect_numeric_metrics(fragment),
            'hardware_reference': self._detect_hardware_reference(fragment),
            'user_behavior': self._detect_user_behavior(fragment),
            'pattern_names': self._detect_pattern_names(fragment),
            'schema_definition': self._detect_schema_definition(fragment),
            'class_names': self._detect_class_names(fragment),
            'executable_code': self._detect_executable_code(fragment),
            'modal_keywords': self._detect_modal_keywords(fragment),
            'includes_rationale': self._detect_rationale(fragment),
            'technology_agnostic': self._detect_technology_agnostic(fragment)
        }

    def get_weights(self, factor_name: str) -> Dict[str, int]:
        """
        Get tier weights for a specific factor.

        Parameters
        ----------
        factor_name : str
            Factor name from self.factors.

        Returns
        -------
        Dict[str, int]
            Tier -> weight mapping.
        """
        return self.weights.get(factor_name, {})

    # ========================================================================
    # Factor Detection Methods
    # ========================================================================

    def _detect_numeric_metrics(self, fragment: str) -> FactorPresence:
        """
        Factor 1: Contains numeric metrics (< 1s, 50MB, 99.9%, etc.).

        Scores: NFR=3, ICD=2, BRD=1
        """
        # Patterns for metrics with units
        patterns = [
            r'\d+\s*(ms|millisecond|second|minute|hour|day|week)',
            r'\d+\s*(B|KB|MB|GB|TB|byte)',
            r'\d+\s*%',
            r'<\s*\d+',
            r'>\s*\d+',
            r'\d+\.\d+\s*(uptime|latency|throughput)',
            r'\d+\s*(fps|hz|bps|mbps)'
        ]

        matches = sum(1 for p in patterns if re.search(p, fragment, re.IGNORECASE))

        if matches >= 2:
            return FactorPresence.YES
        elif matches == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_hardware_reference(self, fragment: str) -> FactorPresence:
        """
        Factor 2: References hardware (CPU, GPU, VRAM, RTX, etc.).

        Scores: NFR=3, SAD=1, BRD=1
        """
        hardware_terms = [
            r'\b(cpu|gpu|vram|ram|memory)\b',
            r'\b(rtx|cuda|amd|intel|nvidia)\b',
            r'\b(ssd|hdd|disk|storage)\b',
            r'\b(core|thread|socket)\b',
            r'\b(bandwidth|throughput|latency)\b'
        ]

        matches = sum(1 for term in hardware_terms if re.search(term, fragment, re.IGNORECASE))

        if matches >= 2:
            return FactorPresence.YES
        elif matches == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_user_behavior(self, fragment: str) -> FactorPresence:
        """
        Factor 3: Describes user behavior or interaction.

        Scores: FSD=3, BRD=2
        """
        behavior_terms = [
            r'\b(user|operator|stakeholder|person)\b',
            r'\b(interact|click|press|speak|type)\b',
            r'\b(see|view|hear|receive|experience)\b',
            r'\b(workflow|process|task|action)\b',
            r'\b(feedback|notification|alert|response)\b'
        ]

        matches = sum(1 for term in behavior_terms if re.search(term, fragment, re.IGNORECASE))

        if matches >= 3:
            return FactorPresence.YES
        elif matches >= 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_pattern_names(self, fragment: str) -> FactorPresence:
        """
        Factor 4: Names architectural patterns.

        Scores: SAD=3, TDD=1
        """
        patterns = [
            r'\b(hub-and-spoke|hub and spoke)\b',
            r'\b(dealer|router|push|pull|pub|sub)\b',
            r'\b(singleton|factory|observer|strategy)\b',
            r'\b(microservice|monolith|layered)\b',
            r'\b(pipeline|orchestration|choreography)\b',
            r'\b(topology|architecture|pattern)\b'
        ]

        matches = sum(1 for p in patterns if re.search(p, fragment, re.IGNORECASE))

        if matches >= 2:
            return FactorPresence.YES
        elif matches == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_schema_definition(self, fragment: str) -> FactorPresence:
        """
        Factor 5: Defines JSON/YAML schemas or data structures.

        Scores: ICD=3, ISP=1
        """
        schema_indicators = [
            r'\{[^}]*:[^}]*\}',  # JSON-like
            r'\w+:\s*\w+',  # YAML-like
            r'\bschema\b',
            r'\b(json|yaml|xml|protobuf)\b',
            r'\b(field|property|attribute):\s*\w+',
            r'\b(string|integer|boolean|array|object|float)\b'
        ]

        matches = sum(1 for ind in schema_indicators if re.search(ind, fragment, re.IGNORECASE))

        if matches >= 3:
            return FactorPresence.YES
        elif matches >= 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_class_names(self, fragment: str) -> FactorPresence:
        """
        Factor 6: Contains class names (PascalCase identifiers).

        Scores: TDD=3, ISP=2
        """
        # PascalCase pattern
        class_pattern = r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b'
        matches = re.findall(class_pattern, fragment)

        # Filter out common non-class words
        non_classes = {'JavaScript', 'Python', 'TypeScript'}
        actual_classes = [m for m in matches if m not in non_classes]

        if len(actual_classes) >= 2:
            return FactorPresence.YES
        elif len(actual_classes) == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_executable_code(self, fragment: str) -> FactorPresence:
        """
        Factor 7: Has executable code (def, class, import, etc.).

        Scores: ISP=3
        """
        code_indicators = [
            r'\bdef\s+\w+\s*\(',
            r'\bclass\s+\w+',
            r'\bimport\s+\w+',
            r'\bfrom\s+\w+\s+import',
            r'\breturn\s+\w+',
            r'\bif\s+\w+\s*:',
            r'\bfor\s+\w+\s+in\s',
            r'self\.\w+'
        ]

        matches = sum(1 for ind in code_indicators if re.search(ind, fragment))

        if matches >= 2:
            return FactorPresence.YES
        elif matches == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_modal_keywords(self, fragment: str) -> FactorPresence:
        """
        Factor 8: Uses RFC 2119 modal keywords (MUST, SHALL, SHOULD, MAY).

        Scores: NFR=3, FSD=2, BRD=2
        """
        modal_pattern = r'\b(must|shall|should|may|required|mandatory|optional)\b'
        matches = len(re.findall(modal_pattern, fragment, re.IGNORECASE))

        if matches >= 2:
            return FactorPresence.YES
        elif matches == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_rationale(self, fragment: str) -> FactorPresence:
        """
        Factor 9: Includes rationale or justification.

        Scores: BRD=3, SAD=3, TDD=2
        """
        rationale_indicators = [
            r'\b(because|since|due to|in order to)\b',
            r'\b(enables|allows|supports|facilitates)\b',
            r'\b(objective|goal|purpose|intent)\b',
            r'\b(why|reason|rationale|justification)\b'
        ]

        matches = sum(1 for ind in rationale_indicators if re.search(ind, fragment, re.IGNORECASE))

        if matches >= 2:
            return FactorPresence.YES
        elif matches == 1:
            return FactorPresence.PARTIAL
        else:
            return FactorPresence.NONE

    def _detect_technology_agnostic(self, fragment: str) -> FactorPresence:
        """
        Factor 10: Technology-agnostic (no specific libraries/tools).

        Scores: BRD=3, NFR=1, FSD=2

        Note: This is an inverse factor - absence of tech terms scores higher.
        """
        tech_terms = [
            r'\b(python|javascript|java|c\+\+|rust)\b',
            r'\b(zeromq|zmq|mqtt|redis|kafka)\b',
            r'\b(pytorch|tensorflow|keras)\b',
            r'\b(react|vue|angular|django|flask)\b',
            r'\b(postgres|mysql|mongodb|sqlite)\b',
            r'\b(docker|kubernetes|aws|gcp|azure)\b'
        ]

        matches = sum(1 for term in tech_terms if re.search(term, fragment, re.IGNORECASE))

        if matches == 0:
            return FactorPresence.YES  # Fully agnostic
        elif matches == 1:
            return FactorPresence.PARTIAL  # Mostly agnostic
        else:
            return FactorPresence.NONE  # Tech-specific
