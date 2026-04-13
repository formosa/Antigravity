#!/usr/bin/env python3
"""
Validate the DDR v7.0 release package against the owned release boundary.

role: release validator
entrypoints: main
reads: ddr/ddr_system_v7.0.yaml; ddr/ddr_node_schema_v7.0.yaml; ddr/conformance/v7.0/; generated markdown outputs
writes: stdout only
external_io: fs
state_model: stateless
failure_surface: missing release artifacts; malformed YAML; schema validation failures; corpus expectation mismatches
coupling: coupled to DDR v7.0 release paths and generator provenance contract
determinism: input-dependent
concurrency: process-local
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import jsonschema
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SYSTEM = REPO_ROOT / "ddr" / "ddr_system_v7.0.yaml"
DEFAULT_SCHEMA = REPO_ROOT / "ddr" / "ddr_node_schema_v7.0.yaml"
DEFAULT_CANONICAL = REPO_ROOT / "ddr" / "DDR System(v7.0).md"
DEFAULT_MANUAL = REPO_ROOT / "ddr" / "ddr_ref_manual_v7.0.md"
DEFAULT_CORPUS_ROOT = REPO_ROOT / "ddr" / "conformance" / "v7.0"
GENERATOR_PATH = ".agent/scripts/generate_ddr_release_docs.py"


def repo_relative(path: Path) -> str:
    """Return a repo-relative POSIX path when possible."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_yaml_document(path: Path) -> dict[str, Any]:
    """Load a YAML document and require a mapping root."""
    if not path.exists():
        raise SystemExit(f"[ERROR] Missing YAML input: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SystemExit(f"[ERROR] Malformed YAML in {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise SystemExit(f"[ERROR] Expected a mapping root in {path}.")
    return loaded


def extract_provenance_header(path: Path) -> dict[str, str]:
    """Extract the generated provenance header from a markdown file."""
    if not path.exists():
        raise SystemExit(f"[ERROR] Missing generated markdown output: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.startswith("<!--\n"):
        raise SystemExit(f"[ERROR] Missing provenance header in {path}.")
    end_index = text.find("\n-->")
    if end_index == -1:
        raise SystemExit(f"[ERROR] Unterminated provenance header in {path}.")
    header_block = text[5:end_index]
    header: dict[str, str] = {}
    for raw_line in header_block.splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        header[key.strip()] = value.strip()
    return header


def validate_markdown_provenance(
    *,
    path: Path,
    expected_role: str,
    system_path: Path,
    schema_path: Path,
) -> None:
    """Validate a generated markdown file's provenance header."""
    header = extract_provenance_header(path)
    expected_pairs = {
        "generated_by": GENERATOR_PATH,
        "source_system": repo_relative(system_path),
        "source_schema": repo_relative(schema_path),
        "surface_role": expected_role,
        "authority": "explanatory_only_yaml_pair_governs",
    }
    for key, expected_value in expected_pairs.items():
        actual = header.get(key)
        if actual != expected_value:
            raise SystemExit(
                f"[ERROR] Provenance mismatch in {path}: expected {key}={expected_value!r}, got {actual!r}."
            )


def validate_yaml_instance(schema: dict[str, Any], instance: dict[str, Any], source: Path) -> None:
    """Validate a YAML instance against the provided schema."""
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as exc:
        raise SystemExit(f"[ERROR] Schema validation failed for {source}: {exc.message}") from exc


def load_manifest(path: Path) -> dict[str, Any]:
    """Load the conformance manifest."""
    manifest = load_yaml_document(path)
    if "cases" not in manifest or not isinstance(manifest["cases"], list):
        raise SystemExit(f"[ERROR] Conformance manifest {path} is missing a 'cases' list.")
    return manifest


def validate_corpus_case(
    *,
    schema: dict[str, Any],
    case: dict[str, Any],
    manifest_dir: Path,
) -> tuple[str, bool]:
    """Validate a single corpus case and return an (id, passed) tuple."""
    case_id = str(case.get("id", "<missing-id>"))
    case_path = manifest_dir / str(case["path"])
    expected = str(case["expected"])
    instance = load_yaml_document(case_path)

    try:
        jsonschema.validate(instance, schema)
        if expected != "valid":
            raise SystemExit(f"[ERROR] Invalid corpus case passed unexpectedly: {case_id}")
    except jsonschema.ValidationError as exc:
        if expected != "invalid":
            raise SystemExit(f"[ERROR] Valid corpus case failed: {case_id}: {exc.message}") from exc
        expected_snippet = case.get("expected_error_contains")
        if expected_snippet and expected_snippet not in exc.message:
            raise SystemExit(
                "[ERROR] Invalid corpus case failed for an unexpected reason: "
                f"{case_id}. Expected message containing {expected_snippet!r}, got {exc.message!r}."
            ) from exc
    return case_id, True


def validate_corpus(schema: dict[str, Any], corpus_root: Path) -> list[str]:
    """Validate every corpus case and return the successful case ids."""
    manifest = load_manifest(corpus_root / "manifest.yaml")
    results: list[str] = []
    manifest_dir = (corpus_root / "manifest.yaml").parent
    for case in manifest["cases"]:
        case_id, _ = validate_corpus_case(schema=schema, case=case, manifest_dir=manifest_dir)
        results.append(case_id)
    return results


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--system", type=Path, default=DEFAULT_SYSTEM)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--canonical-doc", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--manual-doc", type=Path, default=DEFAULT_MANUAL)
    parser.add_argument("--corpus-root", type=Path, default=DEFAULT_CORPUS_ROOT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the owned DDR v7.0 release validation boundary."""
    args = parse_args(argv)
    schema = load_yaml_document(args.schema)
    system = load_yaml_document(args.system)

    validate_yaml_instance(schema, system, args.system)
    validate_markdown_provenance(
        path=args.canonical_doc,
        expected_role="canonical_human_readable",
        system_path=args.system,
        schema_path=args.schema,
    )
    validate_markdown_provenance(
        path=args.manual_doc,
        expected_role="explanatory_reference_manual",
        system_path=args.system,
        schema_path=args.schema,
    )

    validated_case_ids = validate_corpus(schema, args.corpus_root)
    print(f"[OK] authority pair validated against {args.schema}")
    print(f"[OK] markdown provenance verified for {args.canonical_doc.name} and {args.manual_doc.name}")
    print(f"[OK] conformance corpus validated: {len(validated_case_ids)} case(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
