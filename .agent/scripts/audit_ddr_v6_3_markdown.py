from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ASSET_DIR = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "proposals"
    / "active"
    / "v6.3"
)
SYSTEM_YAML = ASSET_DIR / "ddr_system_v6.3.yaml"
SCHEMA_YAML = ASSET_DIR / "ddr_node_schema_v6.3.yaml"
MARKDOWN = ASSET_DIR / "DDR System(v6.3).md"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def collect_authoritative_ids(system_data: dict) -> list[str]:
    ids: list[str] = []

    def add(value: str | None) -> None:
        if value:
            ids.append(value)

    for axiom in system_data.get("axioms", []):
        add(axiom.get("id"))

    for invariant in system_data.get("dag_invariants", []):
        add(invariant.get("id"))

    for citation_rule in system_data.get("citation_rules", []):
        add(citation_rule.get("rule_id") or citation_rule.get("id"))

    for tier in system_data.get("tier_definitions", []):
        for rule in tier.get("atomic_inclusion_rules", []):
            add(rule.get("rule_id") or rule.get("id"))
        for rule in tier.get("atomic_exclusion_rules", []):
            add(rule.get("rule_id") or rule.get("id"))
        for rule in tier.get("bridge_rules", []):
            add(rule.get("rule_id") or rule.get("id"))

    for extension in system_data.get("extension_catalog", []):
        add(extension.get("id"))
        for rule in extension.get("rules", []):
            add(rule.get("rule_id") or rule.get("id"))

    lifecycle = system_data.get("lifecycle", {})
    for guard in lifecycle.get("guard_definitions", []):
        add(guard.get("guard_id") or guard.get("id"))

    return ids


def system_definition_required_surfaces(schema_data: dict) -> list[str]:
    for branch in schema_data.get("allOf", []):
        profile = (
            branch.get("if", {})
            .get("properties", {})
            .get("document_profile", {})
            .get("const")
        )
        if profile == "system_definition":
            return list(branch.get("then", {}).get("required", []))
    return []


def collect_failures(markdown_text: str, system_data: dict, schema_data: dict) -> list[str]:
    failures: list[str] = []

    required_headings = [
        "## 0. Authority Model and Root Contract",
        "### 0.2 Root Contract Quick Reference",
        "### 0.3 System-Definition Required Surface",
        "### 3.1 Node Schema",
        "### 3.1.1 ParentCitation Contract",
        "### 3.5 DAG Invariants",
        "### 3.5.1 Rule-ID Family Closure",
        "### 3.8 Node Status Lifecycle",
        "### 3.8.1 Lifecycle Quick Reference",
        "### 8.4 Extension Annotation Safeguards",
        "## Appendix C: YAML and Schema Surface Crosswalk",
    ]
    for heading in required_headings:
        if heading not in markdown_text:
            failures.append(f"Missing required heading: {heading}")

    metadata_pairs = [
        ("ddr_version", str(system_data.get("ddr_version"))),
        ("document_profile", str(system_data.get("document_profile"))),
        ("project.name", str(system_data.get("project", {}).get("name"))),
        ("project.created", str(system_data.get("project", {}).get("created"))),
        ("project.mode", str(system_data.get("project", {}).get("mode"))),
        ("system_metadata.status", str(system_data.get("system_metadata", {}).get("status"))),
        ("system_metadata.date", str(system_data.get("system_metadata", {}).get("date"))),
        ("system_metadata.scope", str(system_data.get("system_metadata", {}).get("scope"))),
        (
            "system_metadata.authority",
            str(system_data.get("system_metadata", {}).get("authority")),
        ),
        (
            "system_metadata.lineage",
            str(system_data.get("system_metadata", {}).get("lineage")),
        ),
    ]
    for field_name, expected_value in metadata_pairs:
        if field_name not in markdown_text:
            failures.append(f"Missing rendered metadata field name: {field_name}")
        if expected_value not in markdown_text:
            failures.append(
                f"Missing rendered metadata value for {field_name}: {expected_value}"
            )

    expected_active_tiers = ", ".join(system_data.get("active_tiers", []))
    if expected_active_tiers not in markdown_text:
        failures.append(
            "Missing canonical active_tiers rendering: "
            f"{expected_active_tiers}"
        )

    required_surface_tokens = system_definition_required_surfaces(schema_data)
    for token in required_surface_tokens:
        if token not in markdown_text:
            failures.append(f"Missing system_definition required surface token: {token}")

    coverage_groups = {
        "document_profile coverage": [
            "project_instance",
            "project_instance_express",
            "system_definition",
        ],
        "ParentCitation coverage": [
            "ParentCitation",
            "derivation_mode",
            "never valid inside `parent_ids`",
        ],
        "lifecycle guard coverage": [
            "gc-001",
            "gc-002",
            "gc-003",
            "gc-004",
            "gc-005",
            "gc-006",
            "gc-007",
            "gc-008",
            "gc-009",
            "lifecycle.status_transitions",
        ],
        "ARE custom-profile coverage": [
            "Custom profiles",
            "required_fields",
            "profile_template",
            "minimum_surfacing_threshold",
            "override_policy",
        ],
        "rule family coverage": [
            "InvariantId",
            "CitationRuleId",
            "AtomicRuleId",
            "ExtensionRuleId",
        ],
        "extension shadow-key coverage": [
            "shadow-key",
            "extension_annotations",
            "EXTENSION_ID::annotation_key",
        ],
    }
    for label, tokens in coverage_groups.items():
        missing = [token for token in tokens if token not in markdown_text]
        if missing:
            failures.append(f"Incomplete {label}: missing {missing}")

    authoritative_ids = collect_authoritative_ids(system_data)
    missing_ids = [
        identifier for identifier in authoritative_ids if identifier not in markdown_text
    ]
    if missing_ids:
        failures.append(
            "Missing authoritative identifiers in Markdown: "
            + ", ".join(sorted(missing_ids))
        )

    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", markdown_text, flags=re.S)
    if len(mermaid_blocks) < 4:
        failures.append(
            f"Expected a Mermaid suite of at least 4 blocks, found {len(mermaid_blocks)}"
        )
    for index, block in enumerate(mermaid_blocks, start=1):
        if "accTitle:" not in block:
            failures.append(f"Mermaid block {index} missing accTitle")
        if "accDescr:" not in block:
            failures.append(f"Mermaid block {index} missing accDescr")

    appendix_start = markdown_text.find("## Appendix C: YAML and Schema Surface Crosswalk")
    appendix_text = markdown_text[appendix_start:] if appendix_start != -1 else ""
    crosswalk_tokens = [
        "ddr_version",
        "system_metadata",
        "axioms",
        "edge_type_definitions",
        "node_schema_fields",
        "ParentCitation",
        "dag_invariants",
        "Rule-ID defs",
        "node_id_format",
        "citation_rules",
        "lifecycle.status_transitions",
        "consumption_modes",
        "express_mode",
        "tier_definitions",
        "constraint_precedence",
        "operations",
        "extension_system",
        "extension_annotations",
        "extension_catalog",
        "are_scoring_profiles",
        "compliance_checklist",
        "glossary",
        "version_history",
        "tier_migration",
    ]
    for token in crosswalk_tokens:
        if token not in appendix_text:
            failures.append(f"Appendix C missing crosswalk token: {token}")

    return failures


def main() -> int:
    system_data = load_yaml(SYSTEM_YAML)
    schema_data = load_yaml(SCHEMA_YAML)
    markdown_text = MARKDOWN.read_text(encoding="utf-8")

    failures = collect_failures(markdown_text, system_data, schema_data)
    authoritative_id_count = len(collect_authoritative_ids(system_data))
    mermaid_count = len(re.findall(r"```mermaid\n(.*?)\n```", markdown_text, flags=re.S))

    print(f"Authoritative identifiers checked: {authoritative_id_count}")
    print(f"Mermaid blocks checked: {mermaid_count}")

    if failures:
        print("AUDIT FAILED")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("AUDIT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
