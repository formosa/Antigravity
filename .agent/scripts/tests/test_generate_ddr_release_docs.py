#!/usr/bin/env python3
"""
Unit tests for generate_ddr_release_docs.py.

role: unit test suite for DDR release-doc generation
entrypoints: main
reads: generate_ddr_release_docs.py (via dynamic import)
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: highly coupled to generate_ddr_release_docs.py
determinism: deterministic
concurrency: process-local
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "generate_ddr_release_docs.py"
SPEC = importlib.util.spec_from_file_location("generate_ddr_release_docs", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["generate_ddr_release_docs"] = MODULE
SPEC.loader.exec_module(MODULE)


def sample_system() -> dict:
    """Build the minimal system surface required by the generator."""
    return {
        "ddr_version": "7.0",
        "document_profile": "system_definition",
        "project": {"name": "Test DDR", "mode": "full"},
        "system_metadata": {"status": "Finalized", "date": "2026-04-13"},
        "authority_hierarchy": {
            "semantic_authority": {
                "surface": "ddr_system_v7.0.yaml",
                "path": "ddr/ddr_system_v7.0.yaml",
                "precedence": "semantic",
            },
            "structural_authority": {
                "surface": "ddr_node_schema_v7.0.yaml",
                "path": "ddr/ddr_node_schema_v7.0.yaml",
                "precedence": "structural",
            },
            "generated_surfaces": [
                {
                    "surface": "DDR System(v7.0).md",
                    "path": "ddr/DDR System(v7.0).md",
                    "authority_note": "yaml governs",
                }
            ],
        },
        "system_class": {
            "axis_name": "system_class",
            "purpose": "shape",
            "levels": [{"id": "developer_tool", "description": "local tooling"}],
        },
        "operational_maturity": {
            "axis_name": "operational_maturity",
            "purpose": "maturity",
            "levels": [{"id": "local_only", "description": "local"}],
        },
        "assurance_profile": {
            "axis_name": "assurance_profile",
            "purpose": "assurance",
            "levels": [{"id": "standard", "description": "standard"}],
        },
        "design_complete": {"gate": "design_complete", "definition": "done"},
        "production_ready": {"gate": "production_ready", "definition": "ready"},
        "runtime_contract": {
            "concurrency": "single writer",
            "persistence": "yaml",
            "eventing": "manifest",
            "api_shape": "typed",
            "rollback_semantics": "atomic",
            "validation_ledger": "durable",
        },
        "production_contracts": {
            "security_operations": {"profile_gate": "svc", "obligations": ["identity"]},
            "online_runtime": {"profile_gate": "online", "obligations": ["retry"]},
            "data_governance": {"profile_gate": "data", "obligations": ["privacy"]},
            "supply_chain": {"profile_gate": "build", "obligations": ["sbom"]},
        },
        "reference_generators": [
            {
                "generator_id": "canonical",
                "script_path": ".agent/scripts/generate_ddr_release_docs.py",
                "outputs": ["ddr/DDR System(v7.0).md"],
            }
        ],
        "conformance_suite": {
            "validator_command": "python .agent/scripts/validate_ddr_release.py",
            "corpus_root": "ddr/conformance/v7.0",
            "round_trip_requirements": ["docs provenance matches"],
        },
        "migration_contract": {
            "source_version": "6.3",
            "target_version": "7.0",
            "scope": "upgrade",
            "owner": "board",
        },
        "profile_matrices": [
            {
                "use_case": "developer_tools",
                "minimum_system_class": "developer_tool",
                "minimum_operational_maturity": "local_only",
                "minimum_assurance_profile": "standard",
                "readiness_gates": ["design_complete"],
            }
        ],
        "tier_definitions": [
            {
                "tier_id": "SIL",
                "label": "Intent",
                "quick_start_example": "State the objective.",
            }
        ],
        "compliance_checklist": {"profile_guidance": ["design_complete first"]},
    }


def sample_schema() -> dict:
    """Build the minimal schema surface required by the generator."""
    return {"$id": "ddr-system-v7.0-schema", "title": "DDR System v7.0 Machine Contract"}


class TestGenerateDdrReleaseDocs(unittest.TestCase):
    """Regression tests for the DDR release-doc generator."""

    def test_generator_writes_provenance_headers(self) -> None:
        """Verify generated outputs include deterministic provenance headers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            system_path = root / "system.yaml"
            schema_path = root / "schema.yaml"
            canonical_path = root / "canonical.md"
            manual_path = root / "manual.md"
            system_path.write_text(yaml.safe_dump(sample_system(), sort_keys=False), encoding="utf-8")
            schema_path.write_text(yaml.safe_dump(sample_schema(), sort_keys=False), encoding="utf-8")

            MODULE.main(
                [
                    "--system",
                    str(system_path),
                    "--schema",
                    str(schema_path),
                    "--canonical-out",
                    str(canonical_path),
                    "--manual-out",
                    str(manual_path),
                ]
            )

            canonical = canonical_path.read_text(encoding="utf-8")
            manual = manual_path.read_text(encoding="utf-8")
            self.assertIn("generated_by: .agent/scripts/generate_ddr_release_docs.py", canonical)
            self.assertIn("surface_role: canonical_human_readable", canonical)
            self.assertIn("surface_role: explanatory_reference_manual", manual)
            self.assertIn("authority: explanatory_only_yaml_pair_governs", manual)

    def test_generator_honors_output_path_selection(self) -> None:
        """Verify the CLI can target arbitrary output paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            system_path = root / "inputs" / "system.yaml"
            schema_path = root / "inputs" / "schema.yaml"
            canonical_path = root / "out" / "custom-canonical.md"
            manual_path = root / "out" / "custom-manual.md"
            system_path.parent.mkdir(parents=True)
            system_path.write_text(yaml.safe_dump(sample_system(), sort_keys=False), encoding="utf-8")
            schema_path.write_text(yaml.safe_dump(sample_schema(), sort_keys=False), encoding="utf-8")

            MODULE.main(
                [
                    "--system",
                    str(system_path),
                    "--schema",
                    str(schema_path),
                    "--canonical-out",
                    str(canonical_path),
                    "--manual-out",
                    str(manual_path),
                ]
            )

            self.assertTrue(canonical_path.exists())
            self.assertTrue(manual_path.exists())

    def test_generator_fails_fast_for_missing_or_malformed_yaml(self) -> None:
        """Verify missing and malformed YAML inputs halt generation immediately."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            system_path = root / "system.yaml"
            schema_path = root / "schema.yaml"
            schema_path.write_text("not: [valid\n", encoding="utf-8")

            with self.assertRaises(SystemExit):
                MODULE.main(
                    [
                        "--system",
                        str(system_path),
                        "--schema",
                        str(schema_path),
                    ]
                )


if __name__ == "__main__":
    unittest.main()
