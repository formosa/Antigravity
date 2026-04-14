#!/usr/bin/env python3
"""
Generate DDR v7.0 markdown release surfaces from the v7.0 YAML authority pair.

role: release-doc generator
entrypoints: main
reads: ddr/ddr_system_v7.0.yaml; ddr/ddr_node_schema_v7.0.yaml
writes: ddr/DDR System(v7.0).md; ddr/ddr_ref_manual_v7.0.md
external_io: fs
state_model: stateless
failure_surface: missing input files; malformed YAML; write failures
coupling: coupled to DDR v7.0 YAML surface names and top-level contract fields
determinism: input-dependent
concurrency: process-local
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SYSTEM = REPO_ROOT / "ddr" / "ddr_system_v7.0.yaml"
DEFAULT_SCHEMA = REPO_ROOT / "ddr" / "ddr_node_schema_v7.0.yaml"
DEFAULT_CANONICAL = REPO_ROOT / "ddr" / "DDR System(v7.0).md"
DEFAULT_MANUAL = REPO_ROOT / "ddr" / "ddr_ref_manual_v7.0.md"
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


def write_text(path: Path, content: str) -> None:
    """Write UTF-8 text with normalized newlines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_provenance_header(
    *,
    surface_role: str,
    system_path: Path,
    schema_path: Path,
) -> str:
    """Build a deterministic provenance header for generated markdown."""
    return "\n".join(
        [
            "<!--",
            f"generated_by: {GENERATOR_PATH}",
            f"source_system: {repo_relative(system_path)}",
            f"source_schema: {repo_relative(schema_path)}",
            f"surface_role: {surface_role}",
            "authority: explanatory_only_yaml_pair_governs",
            "-->",
            "",
        ]
    )


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a basic GitHub-flavored Markdown table."""
    def clean_cell(cell: str) -> str:
        return cell.replace("\n", " ").strip()

    lines = [
        "| " + " | ".join(clean_cell(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(clean_cell(c) for c in row) + " |" for row in rows)
    return "\n".join(lines)


def render_bullets(values: list[str]) -> str:
    """Render flat bullets."""
    return "\n".join(f"- {value}" for value in values)


def render_authority_rows(system: dict[str, Any]) -> list[list[str]]:
    """Convert authority hierarchy into table rows."""
    rows: list[list[str]] = []
    hierarchy = system["authority_hierarchy"]
    rows.append(
        [
            hierarchy["semantic_authority"]["surface"],
            hierarchy["semantic_authority"]["path"],
            hierarchy["semantic_authority"]["precedence"],
        ]
    )
    rows.append(
        [
            hierarchy["structural_authority"]["surface"],
            hierarchy["structural_authority"]["path"],
            hierarchy["structural_authority"]["precedence"],
        ]
    )
    for surface in hierarchy["generated_surfaces"]:
        rows.append(
            [
                surface["surface"],
                surface["path"],
                surface["authority_note"],
            ]
        )
    return rows


def render_profile_axis(axis: dict[str, Any]) -> str:
    """Render a profile axis section."""
    levels = [
        f"`{level['id']}`: {level['description']}"
        for level in axis["levels"]
    ]
    return "\n".join(
        [
            f"### `{axis['axis_name']}`",
            "",
            axis["purpose"],
            "",
            render_bullets(levels),
        ]
    )


def render_profile_matrix_rows(system: dict[str, Any]) -> list[list[str]]:
    """Render use-case matrix rows."""
    rows: list[list[str]] = []
    for entry in system["profile_matrices"]:
        rows.append(
            [
                entry["use_case"],
                entry["minimum_system_class"],
                entry["minimum_operational_maturity"],
                entry["minimum_assurance_profile"],
                ", ".join(entry["readiness_gates"]),
            ]
        )
    return rows


def render_tier_quick_start_rows(system: dict[str, Any]) -> list[list[str]]:
    """Render quick-start examples from tier definitions."""
    rows: list[list[str]] = []
    for tier in system["tier_definitions"]:
        rows.append(
            [
                tier["tier_id"],
                tier["label"],
                tier.get("quick_start_example", "No quick-start example declared."),
            ]
        )
    return rows


def render_generator_rows(system: dict[str, Any]) -> list[list[str]]:
    """Render reference generator rows."""
    rows: list[list[str]] = []
    for generator in system["reference_generators"]:
        rows.append(
            [
                generator["generator_id"],
                generator["script_path"],
                ", ".join(generator["outputs"]),
            ]
        )
    return rows


def render_release_rows(system: dict[str, Any]) -> list[list[str]]:
    """Render release-tool rows."""
    return [
        [
            "validator",
            system["conformance_suite"]["validator_command"],
            system["conformance_suite"]["corpus_root"],
        ],
        [
            "migration",
            system["migration_contract"]["source_version"],
            system["migration_contract"]["target_version"],
        ],
    ]


def render_canonical_markdown(
    *,
    system: dict[str, Any],
    schema: dict[str, Any],
    system_path: Path,
    schema_path: Path,
) -> str:
    """Render the canonical human-readable surface."""
    version = system["ddr_version"]
    metadata = system["system_metadata"]
    readiness_rows = [
        [system["design_complete"]["gate"], system["design_complete"]["definition"]],
        [system["production_ready"]["gate"], system["production_ready"]["definition"]],
    ]
    root_rows = [
        ["ddr_version", version],
        ["document_profile", system["document_profile"]],
        ["project.name", system["project"]["name"]],
        ["project.mode", system["project"]["mode"]],
        ["system_metadata.status", metadata["status"]],
        ["system_metadata.date", metadata["date"]],
        ["schema.$id", schema["$id"]],
    ]
    sections = [
        build_provenance_header(
            surface_role="canonical_human_readable",
            system_path=system_path,
            schema_path=schema_path,
        ),
        f"# DDR System v{version} Canonical Rendering",
        "",
        "This Markdown surface is generated from the v7.0 YAML authority pair. The YAML pair remains normative.",
        "",
        "## Root Contract",
        "",
        render_table(["Property", "Value"], root_rows),
        "",
        "## Authority Hierarchy",
        "",
        render_table(["Surface", "Path", "Precedence"], render_authority_rows(system)),
        "",
        "## Profile Axes",
        "",
        render_profile_axis(system["system_class"]),
        "",
        render_profile_axis(system["operational_maturity"]),
        "",
        render_profile_axis(system["assurance_profile"]),
        "",
        "## Readiness Gates",
        "",
        render_table(["Gate", "Definition"], readiness_rows),
        "",
        "## Runtime Contract",
        "",
        render_bullets(
            [
                f"Concurrency: {system['runtime_contract']['concurrency']}",
                f"Persistence: {system['runtime_contract']['persistence']}",
                f"Eventing: {system['runtime_contract']['eventing']}",
                f"API shape: {system['runtime_contract']['api_shape']}",
                f"Rollback semantics: {system['runtime_contract']['rollback_semantics']}",
                f"Validation ledger: {system['runtime_contract']['validation_ledger']}",
            ]
        ),
        "",
        "## Production Contracts",
        "",
        render_bullets(
            [
                f"Security and operations: {system['production_contracts']['security_operations']['profile_gate']}",
                f"Online runtime: {system['production_contracts']['online_runtime']['profile_gate']}",
                f"Data governance: {system['production_contracts']['data_governance']['profile_gate']}",
                f"Supply chain: {system['production_contracts']['supply_chain']['profile_gate']}",
            ]
        ),
        "",
        "## Release Surface Ownership",
        "",
        render_table(["Surface", "Implementation", "Output Scope"], render_generator_rows(system)),
        "",
        render_table(["Surface", "Command / Source", "Corpus / Target"], render_release_rows(system)),
        "",
    ]
    return "\n".join(sections)


def render_reference_manual(
    *,
    system: dict[str, Any],
    schema: dict[str, Any],
    system_path: Path,
    schema_path: Path,
) -> str:
    """Render the explanatory reference manual surface."""
    version = system["ddr_version"]
    manifest_rows = [
        ["document_profile", system["document_profile"]],
        ["schema_title", schema["title"]],
        ["corpus_root", system["conformance_suite"]["corpus_root"]],
        ["migration_scope", system["migration_contract"]["scope"]],
    ]
    compliance_guidance = system["compliance_checklist"].get("profile_guidance", [])
    sections = [
        build_provenance_header(
            surface_role="explanatory_reference_manual",
            system_path=system_path,
            schema_path=schema_path,
        ),
        f"# DDR System v{version} Reference Manual",
        "",
        "This manual is generated from the authoritative v7.0 YAML pair and remains explanatory only.",
        "",
        "## Orientation",
        "",
        render_table(["Field", "Value"], manifest_rows),
        "",
        "## Profile Matrix",
        "",
        render_table(
            ["Use Case", "System Class", "Maturity", "Assurance", "Readiness Gates"],
            render_profile_matrix_rows(system),
        ),
        "",
        "## Tier Quick Starts",
        "",
        render_table(["Tier", "Label", "Quick Start"], render_tier_quick_start_rows(system)),
        "",
        "## Compliance Guidance",
        "",
        render_bullets(compliance_guidance),
        "",
        "## Conformance and Migration",
        "",
        render_bullets(system["conformance_suite"]["round_trip_requirements"]),
        "",
        render_bullets(
            [
                f"Migration source: {system['migration_contract']['source_version']}",
                f"Migration target: {system['migration_contract']['target_version']}",
                f"Migration owner: {system['migration_contract']['owner']}",
            ]
        ),
        "",
        "## Reference Generators",
        "",
        render_table(["Generator", "Script", "Outputs"], render_generator_rows(system)),
        "",
    ]
    return "\n".join(sections)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--system", type=Path, default=DEFAULT_SYSTEM)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--canonical-out", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--manual-out", type=Path, default=DEFAULT_MANUAL)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Generate both governed v7.0 markdown release surfaces."""
    args = parse_args(argv)
    system = load_yaml_document(args.system)
    schema = load_yaml_document(args.schema)

    canonical = render_canonical_markdown(
        system=system,
        schema=schema,
        system_path=args.system,
        schema_path=args.schema,
    )
    manual = render_reference_manual(
        system=system,
        schema=schema,
        system_path=args.system,
        schema_path=args.schema,
    )

    write_text(args.canonical_out, canonical)
    write_text(args.manual_out, manual)
    print(f"[OK] wrote {args.canonical_out}")
    print(f"[OK] wrote {args.manual_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
