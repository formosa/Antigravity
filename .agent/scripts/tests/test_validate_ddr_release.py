#!/usr/bin/env python3
"""
Unit tests for validate_ddr_release.py.

role: unit test suite for DDR release validation
entrypoints: main
reads: validate_ddr_release.py (via dynamic import)
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: highly coupled to validate_ddr_release.py
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


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "validate_ddr_release.py"
SPEC = importlib.util.spec_from_file_location("validate_ddr_release", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["validate_ddr_release"] = MODULE
SPEC.loader.exec_module(MODULE)


def build_schema() -> dict:
    """Return a small schema used for validator regression tests."""
    return {
        "type": "object",
        "required": ["name"],
        "properties": {"name": {"type": "string"}},
        "additionalProperties": False,
    }


def build_header(*, role: str, system_path: Path, schema_path: Path) -> str:
    """Construct a valid provenance header for validator tests."""
    return "\n".join(
        [
            "<!--",
            "generated_by: .agent/scripts/generate_ddr_release_docs.py",
            f"source_system: {MODULE.repo_relative(system_path)}",
            f"source_schema: {MODULE.repo_relative(schema_path)}",
            f"surface_role: {role}",
            "authority: explanatory_only_yaml_pair_governs",
            "-->",
            "",
            "# Generated",
            "",
        ]
    )


class TestValidateDdrRelease(unittest.TestCase):
    """Regression tests for the DDR release validator."""

    def test_validate_yaml_instance_accepts_matching_document(self) -> None:
        """Verify direct YAML self-validation succeeds for a matching document."""
        schema = build_schema()
        MODULE.validate_yaml_instance(schema, {"name": "ok"}, Path("sample.yaml"))

    def test_load_manifest_requires_cases_list(self) -> None:
        """Verify manifest loading rejects malformed manifests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.yaml"
            path.write_text("version: '7.0'\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                MODULE.load_manifest(path)

    def test_validate_corpus_handles_expected_pass_and_fail(self) -> None:
        """Verify valid cases pass and invalid cases fail for the expected reason."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            corpus_root = root / "corpus"
            valid_dir = corpus_root / "valid"
            invalid_dir = corpus_root / "invalid"
            valid_dir.mkdir(parents=True)
            invalid_dir.mkdir(parents=True)

            (valid_dir / "good.yaml").write_text("name: ok\n", encoding="utf-8")
            (invalid_dir / "bad.yaml").write_text("wrong: nope\n", encoding="utf-8")
            manifest = {
                "version": "7.0",
                "cases": [
                    {"id": "good", "path": "valid/good.yaml", "expected": "valid"},
                    {
                        "id": "bad",
                        "path": "invalid/bad.yaml",
                        "expected": "invalid",
                        "expected_error_contains": "'name' is a required property",
                    },
                ],
            }
            (corpus_root / "manifest.yaml").write_text(
                yaml.safe_dump(manifest, sort_keys=False),
                encoding="utf-8",
            )

            case_ids = MODULE.validate_corpus(build_schema(), corpus_root)

            self.assertEqual(case_ids, ["good", "bad"])

    def test_validate_markdown_provenance_checks_expected_header(self) -> None:
        """Verify provenance validation passes for matching headers and fails on mismatch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            system_path = root / "system.yaml"
            schema_path = root / "schema.yaml"
            canonical = root / "canonical.md"
            bad_manual = root / "manual.md"
            system_path.write_text("name: ok\n", encoding="utf-8")
            schema_path.write_text(yaml.safe_dump(build_schema(), sort_keys=False), encoding="utf-8")
            canonical.write_text(
                build_header(
                    role="canonical_human_readable",
                    system_path=system_path,
                    schema_path=schema_path,
                ),
                encoding="utf-8",
            )
            bad_manual.write_text(
                build_header(
                    role="wrong_role",
                    system_path=system_path,
                    schema_path=schema_path,
                ),
                encoding="utf-8",
            )

            MODULE.validate_markdown_provenance(
                path=canonical,
                expected_role="canonical_human_readable",
                system_path=system_path,
                schema_path=schema_path,
            )
            with self.assertRaises(SystemExit):
                MODULE.validate_markdown_provenance(
                    path=bad_manual,
                    expected_role="explanatory_reference_manual",
                    system_path=system_path,
                    schema_path=schema_path,
                )


if __name__ == "__main__":
    unittest.main()
