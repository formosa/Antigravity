"""
Core validation engine for block-atomic tag hierarchy.

Implements: DDR System constraint enforcement
Requirements: tag_immutability.md, block-atomic precedence rules
"""

from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass

from .parser import RSTParser
from .models import Tag, ValidationResult, Violation, ViolationType
from ..rules.ordering_rule import OrderingRule
from ..rules.citation_rule import CitationRule
from ..rules.consistency_rule import ConsistencyRule


@dataclass
class ValidationContext:
    """
    Context for validation operations.

    Attributes
    ----------
    file_path : Path
        Path to file being validated.
    tier : str
        DDR tier (BRD, NFR, FSD, SAD, ICD, TDD, ISP).
    strict_mode : bool
        If True, warnings treated as errors.
    """
    file_path: Path
    tier: str
    strict_mode: bool = False


class BlockAtomicValidator:
    """
    Validates block-atomic tag hierarchy according to DDR rules.

    Rules enforced:
    1. Block tags (TIER-N) precede atomic children (TIER-N.M)
    2. Atomic tags cite their block parent via :links:
    3. Prefix consistency (TIER matches between block/atomic)
    4. No orphaned atomic tags

    Ref: |patterns/tag_syntax.md|, |constraints/tag_citation_required.md|

    Parameters
    ----------
    config : Dict
        Configuration dictionary from skill_manifest.yaml.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize validator with configuration.

        Implements: Block-atomic validation protocol
        """
        self.config = config or {}
        self.parser = RSTParser()
        self.rules = [
            OrderingRule(self.config),
            CitationRule(self.config),
            ConsistencyRule(self.config)
        ]

    def validate_file(self, file_path: Path, tier: str = None) -> ValidationResult:
        """
        Validate single RST file for block-atomic compliance.

        Parameters
        ----------
        file_path : Path
            Path to RST file to validate.
        tier : str, optional
            Override tier detection (BRD, NFR, etc.).

        Returns
        -------
        ValidationResult
            Validation outcome with violations list.

        Raises
        ------
        FileNotFoundError
            If file_path does not exist.
        ValueError
            If file contains invalid RST syntax.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Parse RST content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tags = self.parser.parse_tags(content)

        # Infer tier from file path if not provided
        if tier is None:
            tier = self._infer_tier(file_path)

        context = ValidationContext(
            file_path=file_path,
            tier=tier,
            strict_mode=self.config.get('strict_mode', False)
        )

        # Run all validation rules
        violations = []
        for rule in self.rules:
            violations.extend(rule.validate(tags, context))

        return ValidationResult(
            file_path=file_path,
            tier=tier,
            total_tags=len(tags),
            violations=violations,
            is_valid=len(violations) == 0
        )

    def validate_project(self, project_root: Path) -> List[ValidationResult]:
        """
        Validate all RST files in project.

        Parameters
        ----------
        project_root : Path
            Root directory of DDR project.

        Returns
        -------
        List[ValidationResult]
            Results for each validated file.
        """
        results = []

        # Find all RST files in docs/ subdirectories
        docs_path = project_root / "docs"
        if not docs_path.exists():
            return results

        for rst_file in docs_path.rglob("*.rst"):
            # Skip reconciliation manifests
            if "reconciliation_manifest" in rst_file.name.lower():
                continue

            try:
                result = self.validate_file(rst_file)
                results.append(result)
            except Exception as e:
                # Log error but continue validation
                print(f"Error validating {rst_file}: {e}")

        return results

    def _infer_tier(self, file_path: Path) -> str:
        """
        Infer DDR tier from file path.

        Parameters
        ----------
        file_path : Path
            Path to RST file.

        Returns
        -------
        str
            Inferred tier (BRD, NFR, FSD, SAD, ICD, TDD, ISP).
        """
        # Map directory names to tiers
        tier_mapping = {
            "01_brd": "BRD",
            "02_nfr": "NFR",
            "03_fsd": "FSD",
            "04_sad": "SAD",
            "05_icd": "ICD",
            "06_tdd": "TDD",
            "07_isp": "ISP"
        }

        parts = file_path.parts
        for part in parts:
            if part in tier_mapping:
                return tier_mapping[part]

        # Fallback: parse first tag in file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tags = self.parser.parse_tags(content)
        if tags:
            return tags[0].tier

        return "UNKNOWN"

    def get_block_atomic_map(self, tags: List[Tag]) -> Dict[str, List[Tag]]:
        """
        Build mapping of block tags to their atomic children.

        Parameters
        ----------
        tags : List[Tag]
            List of all tags in document.

        Returns
        -------
        Dict[str, List[Tag]]
            Map of block_id -> [atomic_tags].
        """
        block_map = {}

        for tag in tags:
            if tag.is_atomic:
                block_id = tag.get_block_id()
                if block_id not in block_map:
                    block_map[block_id] = []
                block_map[block_id].append(tag)

        return block_map

    def find_block_tag(self, atomic_tag: Tag, tags: List[Tag]) -> Optional[Tag]:
        """
        Find corresponding block tag for atomic tag.

        Parameters
        ----------
        atomic_tag : Tag
            Atomic tag (TIER-N.M).
        tags : List[Tag]
            All tags in document.

        Returns
        -------
        Optional[Tag]
            Corresponding block tag or None.
        """
        expected_block_id = atomic_tag.get_block_id()

        for tag in tags:
            if tag.tag_id == expected_block_id:
                return tag

        return None
