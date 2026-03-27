from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"{path} did not parse as a YAML mapping.")
    return data


def build_index(node_schema_fields: list[dict]) -> tuple[dict[str, dict], list[str]]:
    index: dict[str, dict] = {}
    duplicates: list[str] = []

    for entry in node_schema_fields:
        property_name = entry.get("property")
        if not isinstance(property_name, str) or not property_name:
            raise ValueError("Every node_schema_fields entry must declare a non-empty 'property' value.")
        if property_name in index:
            duplicates.append(property_name)
        index[property_name] = entry

    return index, duplicates


def validate_sync(system_path: Path, schema_path: Path) -> list[str]:
    errors: list[str] = []

    system_data = load_yaml(system_path)
    schema_data = load_yaml(schema_path)

    node_schema_fields = system_data.get("node_schema_fields")
    if not isinstance(node_schema_fields, list):
        raise TypeError(f"{system_path} is missing a list-valued 'node_schema_fields' section.")

    schema_node = (
        schema_data.get("$defs", {})
        .get("DdrNode", {})
    )
    ddr_node_properties = schema_node.get("properties")
    if not isinstance(ddr_node_properties, dict):
        raise TypeError(f"{schema_path} is missing $defs.DdrNode.properties.")

    documented_index, duplicates = build_index(node_schema_fields)
    if duplicates:
        errors.append(f"Duplicate node_schema_fields entries: {', '.join(sorted(set(duplicates)))}")

    documented_properties = set(documented_index)
    schema_properties = set(ddr_node_properties)

    missing_from_docs = sorted(schema_properties - documented_properties)
    if missing_from_docs:
        errors.append(
            "Properties present in $defs.DdrNode but undocumented in node_schema_fields: "
            + ", ".join(missing_from_docs)
        )

    extra_in_docs = sorted(documented_properties - schema_properties)
    if extra_in_docs:
        errors.append(
            "Properties documented in node_schema_fields but absent from $defs.DdrNode: "
            + ", ".join(extra_in_docs)
        )

    conditional_expectations = {
        "constraint_origin": "conditional",
        "prior_status": "conditional",
        "express_mode_group": "conditional",
    }
    for property_name, expected_cardinality in conditional_expectations.items():
        entry = documented_index.get(property_name)
        if entry is None:
            continue
        actual_cardinality = entry.get("cardinality")
        if actual_cardinality != expected_cardinality:
            errors.append(
                f"{property_name} should declare cardinality '{expected_cardinality}' "
                f"but found '{actual_cardinality}'."
            )

    for property_name, entry in documented_index.items():
        if not any(isinstance(entry.get(key), str) and entry.get(key).strip() for key in ("description", "semantics")):
            errors.append(
                f"{property_name} must include descriptive metadata in node_schema_fields "
                f"(description or semantics)."
            )

    return errors


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Validate that node_schema_fields remains synchronized with $defs.DdrNode."
    )
    parser.add_argument(
        "--system",
        type=Path,
        default=script_dir / "ddr_system_v6.2.yaml",
        help="Path to the DDR system-definition YAML file.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=script_dir / "ddr_node_schema_v6.2.yaml",
        help="Path to the DDR node schema YAML file.",
    )
    args = parser.parse_args()

    try:
        errors = validate_sync(args.system.resolve(), args.schema.resolve())
    except Exception as exc:  # pragma: no cover - defensive CLI reporting
        print(f"SYNC_CHECK_ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("SYNC_CHECK_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SYNC_CHECK_OK")
    print(f"- system: {args.system.resolve()}")
    print(f"- schema: {args.schema.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
