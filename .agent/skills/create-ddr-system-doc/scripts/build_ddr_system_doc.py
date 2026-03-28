#!/usr/bin/env python3
"""
Build authoritative DDR System Markdown documentation from a schema/spec pair.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path
from typing import Any

import jsonschema
import yaml


SECTION_HEADINGS = {
    "design": "## 1. Design Philosophy",
    "axioms": "## 2. Foundational Axioms",
    "dag": "## 3. DAG Internal Model",
    "modes": "## 4. Consumption Modes",
    "tiers": "## 5. Tier Specifications",
    "precedence": "## 6. Constraint Precedence",
    "operations": "## 7. Atomic Operations Protocol",
    "extensions": "## 8. Extension System",
    "catalog": "## 9. Extension Catalog",
    "diagram": "## 10. Architecture Diagram",
    "compliance": "## 11. Compliance Checklist",
    "glossary": "## Glossary",
    "history": "## Appendix A: Version History",
    "migration": "## Appendix B: Legacy Tier Migration",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build DDR System Markdown documentation from schema and spec YAML files."
    )
    parser.add_argument("schema_path", help="Path to the DDR schema YAML file.")
    parser.add_argument("spec_path", help="Path to the DDR system specification YAML file.")
    parser.add_argument(
        "--output",
        help="Output Markdown path. Defaults to DDR System(v<ddr_version>).md beside the spec file.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    text = textwrap.dedent(text).strip()
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line != "").strip()


def inline_text(value: Any) -> str:
    text = normalize_text(value)
    text = re.sub(r"\s+", " ", text)
    return text.replace("|", "\\|")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    header_row = "| " + " | ".join(inline_text(cell) for cell in headers) + " |"
    divider = "| " + " | ".join("---" for _ in headers) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(inline_text(cell) or "-" for cell in row) + " |")
    return "\n".join([header_row, divider, *body])


def checkbox_list(items: list[Any]) -> str:
    return "\n".join(f"- [ ] {normalize_text(item)}" for item in items)


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"- {normalize_text(item)}" for item in items)


def numbered_list(items: list[Any]) -> str:
    return "\n".join(f"{index}. {normalize_text(item)}" for index, item in enumerate(items, start=1))


def yes_no(value: Any) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if value is None:
        return "-"
    text = normalize_text(value)
    return text[:1].upper() + text[1:] if text else "-"


def code_block(text: str, language: str = "text") -> str:
    return f"```{language}\n{text.rstrip()}\n```"


def quote_block(text: str) -> str:
    lines = [line for line in normalize_text(text).splitlines() if line]
    return "\n".join(f"> {line}" for line in lines)


def version_label(spec: dict[str, Any]) -> str:
    return inline_text(spec.get("ddr_version", "unknown"))


def previous_version_heading(lineage: str) -> str:
    match = re.search(r"v\d+(?:\.\d+)?", lineage)
    if match:
        return f"### 1.1 Changes from {match.group(0)}"
    return "### 1.1 Changes from Prior Version"


def schema_required_fields(schema: dict[str, Any]) -> set[str]:
    ddr_node = schema.get("$defs", {}).get("DdrNode", {})
    required = ddr_node.get("required", []) or schema.get("required", [])
    return {str(item) for item in required}


def schema_properties(schema: dict[str, Any]) -> dict[str, Any]:
    ddr_node = schema.get("$defs", {}).get("DdrNode", {})
    return ddr_node.get("properties", {}) or schema.get("properties", {})


def summarize_parents(node: dict[str, Any]) -> str:
    parents = node.get("parent_ids", [])
    if not parents:
        return "ROOT"
    pieces = []
    for parent in parents:
        label = f"{parent.get('id')} ({parent.get('edge_type')}"
        if parent.get("derivation_mode"):
            label += f", {parent.get('derivation_mode')}"
        label += ")"
        pieces.append(label)
    return ", ".join(pieces)


def status_values(spec: dict[str, Any]) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    lifecycle = spec.get("lifecycle", {})
    for transition in lifecycle.get("status_transitions", []):
        for key in ("from", "to"):
            value = transition.get(key)
            if isinstance(value, str) and value not in seen and not value.startswith("{"):
                seen.add(value)
                values.append(value)
    for transition in lifecycle.get("prohibited_transitions", []):
        value = transition.get("from")
        if isinstance(value, str) and value not in seen:
            seen.add(value)
            values.append(value)
        for item in transition.get("to", []):
            if isinstance(item, str) and item not in seen:
                seen.add(item)
                values.append(item)
    preferred = [
        "DRAFT",
        "ACTIVE",
        "DIRTY",
        "DEPRECATED",
        "SUPERSEDE_PENDING",
        "SUPERSEDED",
        "DELETED",
    ]
    ordered = [item for item in preferred if item in seen]
    for item in values:
        if item not in ordered:
            ordered.append(item)
    return ordered


def format_node_schema_rows(schema: dict[str, Any], spec: dict[str, Any]) -> list[list[str]]:
    required = schema_required_fields(schema)
    properties = schema_properties(schema)
    rows: list[list[str]] = []
    for field in spec.get("node_schema_fields", []):
        property_name = field.get("property", "")
        description_parts = []
        description = field.get("description")
        if not description and not any(
            field.get(key) for key in ("semantics", "backward_compatibility", "cardinality")
        ):
            description = properties.get(property_name, {}).get("description")
        if description:
            description_parts.append(normalize_text(description))
        if field.get("semantics"):
            description_parts.append(f"Semantics: {normalize_text(field['semantics'])}")
        if field.get("backward_compatibility"):
            description_parts.append(
                f"Backward compatibility: {normalize_text(field['backward_compatibility'])}"
            )
        if field.get("cardinality"):
            description_parts.append(f"Cardinality: {normalize_text(field['cardinality'])}")
        rows.append(
            [
                property_name,
                field.get("type", properties.get(property_name, {}).get("type", "-")),
                "Required" if property_name in required else "Optional",
                " ".join(description_parts).strip(),
            ]
        )
    return rows


def build_universal_node_format(schema: dict[str, Any], spec: dict[str, Any]) -> str:
    properties = schema_properties(schema)
    status_enum = properties.get("status", {}).get("enum", [])
    statuses = " | ".join(status_enum or status_values(spec))
    lines = [
        "[TIER]-[N].[M]: [Title]",
        f"  status:        {statuses or '[StatusEnum]'}",
    ]
    field_names = {field.get("property") for field in spec.get("node_schema_fields", [])}
    if "prior_status" in field_names:
        lines.append("  prior_status:  [StatusEnum]  <- present only during in-flight SUPERSEDE")
    lines.extend(
        [
            "  version:       [SemVer]",
            "  created:       [ISO 8601]",
            "  modified:      [ISO 8601]",
            "  parent_ids:    [{id: [TIER-N.M], edge_type: derives|constrains|implements,",
            "                   derivation_mode?: semantic|traceability}, ...]",
            "                 <- empty only for root nodes",
            "",
            "  [Tier-compliant content body]",
        ]
    )
    return code_block("\n".join(lines))


def build_topology_summary(spec: dict[str, Any]) -> str:
    rows = []
    for node in spec.get("nodes", []):
        rows.append([node.get("id"), node.get("tier"), node.get("title"), summarize_parents(node)])
    parts = [
        f"Active tiers: {', '.join(spec.get('active_tiers', []))}",
        "",
        markdown_table(["Representative Node", "Tier", "Title", "Parents"], rows),
    ]
    return "\n".join(parts)


def build_lifecycle_section(spec: dict[str, Any]) -> str:
    lifecycle = spec.get("lifecycle", {})
    parts = [
        quote_block(
            "Authority note: lifecycle.status_transitions is the machine-readable authority for valid"
            " status transitions."
        ),
        "",
        markdown_table(
            ["From", "To", "Operation", "Guards", "Notes"],
            [
                [
                    item.get("from"),
                    item.get("to"),
                    item.get("operation"),
                    ", ".join(item.get("guards", [])),
                    item.get("notes", ""),
                ]
                for item in lifecycle.get("status_transitions", [])
            ],
        ),
    ]
    prohibited = lifecycle.get("prohibited_transitions", [])
    if prohibited:
        parts.extend(
            [
                "",
                "**Prohibited transitions**",
                "",
                markdown_table(
                    ["From", "Prohibited To", "Reason"],
                    [
                        [item.get("from"), ", ".join(item.get("to", [])), item.get("reason", "")]
                        for item in prohibited
                    ],
                ),
            ]
        )
    guards = lifecycle.get("guard_definitions", [])
    if guards:
        parts.extend(
            [
                "",
                markdown_table(
                    ["Guard ID", "Description", "Verification Mode"],
                    [
                        [item.get("id"), item.get("description"), item.get("verification_mode", "")]
                        for item in guards
                    ],
                ),
            ]
        )
    return "\n".join(parts)


def build_tier_section(spec: dict[str, Any]) -> str:
    parts = [SECTION_HEADINGS["tiers"]]
    for index, tier in enumerate(spec.get("tier_definitions", [])):
        flags = []
        if tier.get("is_optional"):
            flags.append("Optional")
        if tier.get("is_merge_node"):
            flags.append("Merge Node")
        if tier.get("is_terminal_leaf"):
            flags.append("Terminal Leaf")
        suffix = f" ({', '.join(flags)})" if flags else ""
        parts.extend(
            [
                "",
                f"### Tier {index} - {tier.get('tier_id')}: {tier.get('label')}{suffix}",
                "",
                markdown_table(
                    ["Property", "Value"],
                    [
                        ["Layer", tier.get("layer_label", "")],
                        ["Core Question", tier.get("core_question", "")],
                        ["Activation Condition", tier.get("activation_condition", "")],
                        ["Root Behavior", tier.get("root_when", "")],
                        ["Optional", yes_no(tier.get("is_optional"))],
                        ["Merge Node", yes_no(tier.get("is_merge_node"))],
                        ["Terminal Leaf", yes_no(tier.get("is_terminal_leaf"))],
                    ],
                ),
            ]
        )
        parents = tier.get("parent_relationships", [])
        if parents:
            parts.extend(
                [
                    "",
                    "**Parent relationships**",
                    "",
                    markdown_table(
                        ["Tier", "Edge Type", "Condition"],
                        [[item.get("tier"), item.get("edge_type"), item.get("condition", "")] for item in parents],
                    ),
                ]
            )
        children = tier.get("child_relationships", [])
        if children:
            parts.extend(
                [
                    "",
                    "**Child relationships**",
                    "",
                    markdown_table(
                        ["Tier", "Edge Type", "Condition"],
                        [[item.get("tier"), item.get("edge_type"), item.get("condition", "")] for item in children],
                    ),
                ]
            )
        inclusion = tier.get("atomic_inclusion_rules", [])
        if inclusion:
            parts.extend(
                [
                    "",
                    "**Atomic inclusion rules**",
                    "",
                    markdown_table(
                        ["Rule", "Verification", "Statement", "Violation Consequence"],
                        [
                            [
                                item.get("rule_id"),
                                item.get("verification_mode", ""),
                                item.get("statement", ""),
                                item.get("violation_consequence", ""),
                            ]
                            for item in inclusion
                        ],
                    ),
                ]
            )
        exclusion = tier.get("atomic_exclusion_rules", [])
        if exclusion:
            parts.extend(
                [
                    "",
                    "**Atomic exclusion rules**",
                    "",
                    markdown_table(
                        ["Rule", "Statement"],
                        [[item.get("rule_id"), item.get("statement", "")] for item in exclusion],
                    ),
                ]
            )
    return "\n".join(parts)


def build_operations_section(spec: dict[str, Any]) -> str:
    operations = spec.get("operations", {})
    manifest_schema = operations.get("reconciliation_manifest_schema", {})
    parts = [
        SECTION_HEADINGS["operations"],
        "",
        "### 7.1 Core Operations",
        "",
        markdown_table(
            ["Operation", "Description", "Validation Trigger"],
            [
                [item.get("name"), item.get("description"), item.get("validation_trigger")]
                for item in operations.get("core_operations", [])
            ],
        ),
    ]
    if operations.get("design_decision_removed_ops"):
        parts.extend(["", quote_block(operations["design_decision_removed_ops"])])
    parts.extend(
        [
            "",
            "### 7.2 Dirty State and Propagation",
            "",
            markdown_table(
                ["Trigger", "Nodes Affected"],
                [
                    [item.get("trigger"), item.get("nodes_affected")]
                    for item in operations.get("dirty_flag_triggers", [])
                ],
            ),
        ]
    )
    if operations.get("dirty_flag_notes"):
        parts.extend(["", bullet_list(operations["dirty_flag_notes"])])
    if operations.get("dirty_classification"):
        parts.extend(
            [
                "",
                markdown_table(
                    ["Classification", "Description"],
                    [
                        [item.get("type"), item.get("description")]
                        for item in operations.get("dirty_classification", [])
                    ],
                ),
            ]
        )
    if operations.get("supersede_dirty_behavior"):
        parts.extend(["", normalize_text(operations["supersede_dirty_behavior"])])
    parts.extend(["", "### 7.3 Resolution Workflow", ""])
    if operations.get("resolution_workflow"):
        parts.append(normalize_text(operations["resolution_workflow"]))
        parts.append("")
    protocol = operations.get("conflict_resolution_protocol", {})
    if protocol.get("steps"):
        parts.append("**Conflict resolution protocol**")
        parts.append("")
        parts.append(numbered_list(protocol["steps"]))
        parts.append("")
    if protocol.get("audit_requirement"):
        parts.append(normalize_text(protocol["audit_requirement"]))
        parts.append("")
    semantic_rules = operations.get("semantic_consistency_rules", {})
    if semantic_rules:
        parts.append("**Semantic consistency rules**")
        parts.append("")
        if semantic_rules.get("description"):
            parts.append(normalize_text(semantic_rules["description"]))
        if semantic_rules.get("enforcement"):
            parts.append("")
            parts.append(f"Enforcement: {normalize_text(semantic_rules['enforcement'])}")
        parts.append("")
    parts.extend(["### 7.4 Reconciliation Manifest Schema", ""])
    if operations.get("reconciliation_manifest_tracks"):
        parts.append("**Tracked items**")
        parts.append("")
        parts.append(bullet_list(operations["reconciliation_manifest_tracks"]))
        parts.append("")
    manifest_item_types = manifest_schema.get("manifest_item_types", [])
    if manifest_item_types:
        parts.append(
            markdown_table(
                ["Item Type", "Severity", "Description", "Fields"],
                [
                    [
                        item.get("item_type"),
                        item.get("severity", ""),
                        item.get("description", ""),
                        ", ".join(item.get("fields", [])),
                    ]
                    for item in manifest_item_types
                ],
            )
        )
        parts.append("")
    semantic_gap = manifest_schema.get("semantic_gap_classification", {})
    if semantic_gap:
        parts.append("**Semantic gap classification**")
        parts.append("")
        if semantic_gap.get("description"):
            parts.append(normalize_text(semantic_gap["description"]))
            parts.append("")
        if semantic_gap.get("allowed_types"):
            parts.append(f"Allowed types: {', '.join(semantic_gap['allowed_types'])}")
            parts.append("")
        if semantic_gap.get("constraints"):
            parts.append(bullet_list(semantic_gap["constraints"]))
    return "\n".join(part for part in parts if part is not None)


def build_extension_system_section(spec: dict[str, Any]) -> str:
    extension_system = spec.get("extension_system", {})
    candidate_pool = extension_system.get("candidate_pool", {})
    activation_states = candidate_pool.get("activation_states", {})
    state_rows = []
    for state_name in ("active", "paused", "disabled"):
        state = activation_states.get(state_name, {})
        if not state:
            continue
        state_rows.append(
            [
                state_name,
                state.get("inference", ""),
                yes_no(state.get("pool_visibility")),
                yes_no(state.get("pool_preserved_restart")),
                yes_no(state.get("promotion_allowed")),
                yes_no(state.get("discard_allowed")),
            ]
        )
    parts = [
        SECTION_HEADINGS["extensions"],
        "",
        "### 8.1 Architecture",
        "",
        normalize_text(extension_system.get("architecture_description", "")),
    ]
    if extension_system.get("permitted_actions"):
        parts.extend(["", "**Extensions may:**", "", bullet_list(extension_system["permitted_actions"])])
    if extension_system.get("prohibited_actions"):
        parts.extend(
            ["", "**Extensions may not:**", "", bullet_list(extension_system["prohibited_actions"])]
        )
    parts.extend(["", "### 8.2 Extension Candidate Pool", ""])
    if candidate_pool.get("description"):
        parts.append(normalize_text(candidate_pool["description"]))
        parts.append("")
    bullet_rows = []
    if candidate_pool.get("candidate_status_value"):
        bullet_rows.append(f"Candidate status value: {normalize_text(candidate_pool['candidate_status_value'])}")
    if candidate_pool.get("visibility_rule"):
        bullet_rows.append(normalize_text(candidate_pool["visibility_rule"]))
    if candidate_pool.get("effect_on_core_status"):
        bullet_rows.append(f"Core impact: {normalize_text(candidate_pool['effect_on_core_status'])}")
    if candidate_pool.get("promotion_mechanism"):
        bullet_rows.append(normalize_text(candidate_pool["promotion_mechanism"]))
    if bullet_rows:
        parts.extend([bullet_list(bullet_rows), ""])
    if state_rows:
        parts.extend(
            [
                markdown_table(
                    [
                        "State",
                        "Inference",
                        "Pool Visible",
                        "Pool Preserved (Restart)",
                        "Promotion Allowed",
                        "Discard Allowed",
                    ],
                    state_rows,
                ),
                "",
            ]
        )
    transitions = activation_states.get("transitions", [])
    if transitions:
        parts.extend(
            [
                markdown_table(
                    ["From", "To", "Permitted", "Effect / Rationale"],
                    [
                        [
                            item.get("from"),
                            item.get("to"),
                            yes_no(item.get("permitted", True)),
                            item.get("effect", item.get("rationale", "")),
                        ]
                        for item in transitions
                    ],
                ),
                "",
            ]
        )
    if candidate_pool.get("checkpoint_path"):
        parts.append(f"Checkpoint path: `{normalize_text(candidate_pool['checkpoint_path'])}`")
        parts.append("")
    if candidate_pool.get("discard_trigger"):
        parts.append(normalize_text(candidate_pool["discard_trigger"]))
        parts.append("")
    parts.extend(["### 8.3 Extension Integration Rules", ""])
    if extension_system.get("integration_rules"):
        parts.append(
            markdown_table(
                ["Rule", "Statement"],
                [
                    [item.get("rule_id"), item.get("statement")]
                    for item in extension_system.get("integration_rules", [])
                ],
            )
        )
        parts.append("")
    for note in extension_system.get("normative_notes", []):
        parts.extend([quote_block(note), ""])
    return "\n".join(part for part in parts if part is not None).rstrip()


def build_are_profiles_section(spec: dict[str, Any]) -> str:
    profiles = spec.get("are_scoring_profiles", {})
    if not profiles:
        return ""
    parts = ["#### ARE Scoring Profiles", "", "Scoring profiles govern ARE confidence scoring and promotion gates.", ""]
    for profile_name in ("standard_v1", "conservative_v1"):
        profile = profiles.get(profile_name)
        if not profile:
            continue
        parts.append(f"**`{profile_name}`**")
        parts.append("")
        if profile.get("context_note"):
            parts.append(normalize_text(profile["context_note"]))
            parts.append("")
        if profile.get("input_signals"):
            parts.append(
                markdown_table(
                    ["Input Signal", "Weight Category", "Description"],
                    [
                        [item.get("signal_id"), item.get("weight_category"), item.get("description")]
                        for item in profile.get("input_signals", [])
                    ],
                )
            )
            parts.append("")
        if profile.get("score_bands"):
            parts.append(
                markdown_table(
                    ["Band", "Score Range", "Promotion Guidance"],
                    [
                        [
                            item.get("band_id"),
                            " - ".join(str(value) for value in item.get("range", [])),
                            item.get("promotion_guidance"),
                        ]
                        for item in profile.get("score_bands", [])
                    ],
                )
            )
            parts.append("")
        if profile.get("minimum_surfacing_threshold") is not None:
            parts.append(
                "Minimum surfacing threshold: "
                f"**{inline_text(profile['minimum_surfacing_threshold'])}**."
            )
            parts.append("")
        if profile.get("override_policy"):
            parts.append(normalize_text(profile["override_policy"]))
            parts.append("")
    custom = profiles.get("custom", {})
    if custom:
        parts.append("**Custom profiles**")
        parts.append("")
        if custom.get("required_fields"):
            parts.append(
                "Required fields: " + ", ".join(f"`{item}`" for item in custom["required_fields"])
            )
            parts.append("")
        if custom.get("validation_note"):
            parts.append(normalize_text(custom["validation_note"]))
            parts.append("")
    return "\n".join(parts).rstrip()


def build_extension_catalog_section(spec: dict[str, Any]) -> str:
    parts = [SECTION_HEADINGS["catalog"]]
    for extension in spec.get("extension_catalog", []):
        parts.extend(
            [
                "",
                f"### {extension.get('id')} - {extension.get('name')}",
                "",
            ]
        )
        contract_line = f"**Contract:** {normalize_text(extension.get('contract', ''))}"
        contract_line += f" | **Reads:** {', '.join(extension.get('reads', [])) or '-'}"
        contract_line += f" | **Annotates:** {', '.join(extension.get('annotates', [])) or '-'}"
        if extension.get("scoring_profile"):
            contract_line += f" | **Scoring Profile:** `{normalize_text(extension['scoring_profile'])}`"
        parts.append(contract_line)
        if extension.get("notes"):
            parts.extend(["", quote_block(extension["notes"])])
        rules = extension.get("rules", [])
        if rules:
            parts.extend(
                [
                    "",
                    markdown_table(
                        ["Rule", "Statement"],
                        [[item.get("rule_id"), item.get("statement")] for item in rules],
                    ),
                ]
            )
        if extension.get("id") == "E5" and spec.get("are_scoring_profiles"):
            parts.extend(["", build_are_profiles_section(spec)])
    return "\n".join(parts)


def build_mermaid(spec: dict[str, Any]) -> str:
    tier_lookup = {tier.get("tier_id"): tier for tier in spec.get("tier_definitions", [])}
    lines = [
        "flowchart TD",
        '    subgraph CORE["Core DDR System"]',
    ]
    for tier_id in spec.get("active_tiers", []):
        tier = tier_lookup.get(tier_id, {})
        label = tier.get("label", tier_id)
        suffix = []
        if tier.get("is_optional"):
            suffix.append("optional")
        if tier.get("is_merge_node"):
            suffix.append("merge")
        suffix_text = f" ({', '.join(suffix)})" if suffix else ""
        mermaid_label = f'{tier_id} - {label}{suffix_text}'.replace('"', "'")
        lines.append(f'        {tier_id}["{mermaid_label}"]')
    lines.append("    end")
    lines.append("")
    lines.append('    subgraph EXTENSIONS["Extensions"]')
    for extension in spec.get("extension_catalog", []):
        short_name = extension.get("id", "EXT")
        mermaid_label = f"{short_name}: {extension.get('name', short_name)}".replace('"', "'")
        lines.append(f'        {short_name}["{mermaid_label}"]')
    lines.append("    end")
    lines.append("")
    for node in spec.get("nodes", []):
        child = node.get("tier")
        for parent in node.get("parent_ids", []):
            source = str(parent.get("id", "")).split("-", 1)[0]
            edge_type = parent.get("edge_type", "")
            if edge_type == "constrains":
                lines.append(f"    {source} -. constrains .-> {child}")
            else:
                lines.append(f"    {source} -->|{edge_type}| {child}")
    for extension in spec.get("extension_catalog", []):
        source = extension.get("id")
        for target in extension.get("annotates", []):
            lines.append(f"    {source} -. extends .-> {target}")
    return code_block("\n".join(lines), "mermaid")


def expected_headings(spec: dict[str, Any]) -> list[str]:
    headings = [
        f"# DDR System Specification v{version_label(spec)}",
        SECTION_HEADINGS["design"],
        SECTION_HEADINGS["axioms"],
        SECTION_HEADINGS["dag"],
        SECTION_HEADINGS["modes"],
        SECTION_HEADINGS["tiers"],
        SECTION_HEADINGS["precedence"],
        SECTION_HEADINGS["operations"],
        SECTION_HEADINGS["extensions"],
        SECTION_HEADINGS["catalog"],
        SECTION_HEADINGS["diagram"],
        SECTION_HEADINGS["compliance"],
        SECTION_HEADINGS["glossary"],
        SECTION_HEADINGS["history"],
        SECTION_HEADINGS["migration"],
    ]
    if spec.get("system_metadata", {}).get("changes_from_prior") is not None:
        lineage = normalize_text(spec.get("system_metadata", {}).get("lineage", ""))
        headings.append(previous_version_heading(lineage))
    if "errata_log" in spec:
        headings.append("### 1.2 Errata Log")
    headings.extend(
        [
            "### 3.1 Node Schema",
            "### 3.2 Edge Types",
            "### 3.3 Universal Node Format",
            "### 3.4 Core DAG Topology",
            "### 3.5 DAG Invariants",
            "### 3.6 Node ID Format",
            "### 3.7 Citation Rules",
            "### 3.8 Node Status Lifecycle",
            "### Express Mode Group Map",
            "### 7.1 Core Operations",
            "### 7.2 Dirty State and Propagation",
            "### 7.3 Resolution Workflow",
            "### 7.4 Reconciliation Manifest Schema",
            "### 8.1 Architecture",
            "### 8.2 Extension Candidate Pool",
            "### 8.3 Extension Integration Rules",
        ]
    )
    return headings


def validate_output_text(markdown: str, spec: dict[str, Any]) -> list[str]:
    issues = []
    for heading in expected_headings(spec):
        if heading not in markdown:
            issues.append(f"Missing heading: {heading}")
    if "```mermaid" not in markdown:
        issues.append("Missing Mermaid architecture diagram.")
    if "[TODO" in markdown:
        issues.append("Unresolved TODO placeholder detected.")
    tier_count = len(spec.get("tier_definitions", []))
    extension_count = len(spec.get("extension_catalog", []))
    actual_tier_headings = len(re.findall(r"^### Tier \d+ - ", markdown, flags=re.MULTILINE))
    actual_extension_headings = len(re.findall(r"^### E\d+ - ", markdown, flags=re.MULTILINE))
    if tier_count and actual_tier_headings != tier_count:
        issues.append(
            f"Tier subsection count mismatch: expected {tier_count}, found {actual_tier_headings}."
        )
    if extension_count and actual_extension_headings != extension_count:
        issues.append(
            f"Extension subsection count mismatch: expected {extension_count}, found {actual_extension_headings}."
        )
    return issues


def build_markdown(schema: dict[str, Any], spec: dict[str, Any]) -> str:
    meta = spec.get("system_metadata", {})
    lineage = normalize_text(meta.get("lineage", ""))
    metadata_rows = [
        ["Version", spec.get("ddr_version", "")],
        ["Status", meta.get("status", "")],
        ["Date", meta.get("date", "")],
        ["Scope", meta.get("scope", "")],
        ["Authority", meta.get("authority", "")],
        ["Lineage", meta.get("lineage", "")],
    ]
    if spec.get("project", {}).get("mode"):
        metadata_rows.append(["Mode", spec["project"]["mode"]])
    parts = [
        f"# DDR System Specification v{version_label(spec)}",
        "",
        "> **Deterministic Design & Requirements System - Authoritative Reference**",
        "",
        markdown_table(["Property", "Value"], metadata_rows),
    ]
    if spec.get("active_tiers"):
        parts.extend(["", f"Active tiers: {', '.join(spec['active_tiers'])}"])
    if meta.get("single_source_of_truth"):
        parts.extend(["", quote_block(f"Single source of truth. {meta['single_source_of_truth']}")])

    parts.extend(["", "---", "", SECTION_HEADINGS["design"], ""])

    philosophy = meta.get("design_philosophy", [])
    if philosophy:
        parts.append("This specification is governed by the design principles declared in the source definition.")
        parts.append("")
        for index, principle in enumerate(philosophy, start=1):
            parts.append(
                f"{index}. **{normalize_text(principle.get('principle', 'Principle'))}** - "
                f"{normalize_text(principle.get('description', ''))}"
            )
        parts.append("")
    parts.append(previous_version_heading(lineage))
    parts.append("")
    changes = meta.get("changes_from_prior", [])
    if changes:
        parts.append(
            markdown_table(
                ["Area", "Prior", "Current", "Rationale"],
                [
                    [item.get("area"), item.get("prior"), item.get("current"), item.get("rationale")]
                    for item in changes
                ],
            )
        )
    else:
        parts.append("No prior-version changes were declared in the specification.")
    parts.extend(["", "### 1.2 Errata Log", ""])
    errata = spec.get("errata_log", [])
    if errata:
        parts.append(
            markdown_table(
                ["ID", "Date", "Summary", "Resolution"],
                [
                    [
                        item.get("id", ""),
                        item.get("date", ""),
                        item.get("summary", item.get("description", "")),
                        item.get("resolution", ""),
                    ]
                    for item in errata
                ],
            )
        )
    else:
        parts.append("No active errata entries are carried in the authoritative YAML definition.")

    parts.extend(
        [
            "",
            "---",
            "",
            SECTION_HEADINGS["axioms"],
            "",
            markdown_table(
                ["ID", "Axiom", "Statement", "Implication"],
                [
                    [item.get("id"), item.get("name"), item.get("statement"), item.get("implication")]
                    for item in spec.get("axioms", [])
                ],
            ),
            "",
            "---",
            "",
            SECTION_HEADINGS["dag"],
            "",
            "### 3.1 Node Schema",
            "",
            markdown_table(
                ["Property", "Type", "Required", "Description"],
                format_node_schema_rows(schema, spec),
            ),
            "",
            "### 3.2 Edge Types",
            "",
            markdown_table(
                ["Type", "Symbol", "Semantics"],
                [
                    [item.get("type"), item.get("symbol"), item.get("semantics")]
                    for item in spec.get("edge_type_definitions", {}).get("types", [])
                ],
            ),
        ]
    )
    if spec.get("edge_type_definitions", {}).get("design_decision"):
        parts.extend(["", quote_block(spec["edge_type_definitions"]["design_decision"])])
    parts.extend(
        [
            "",
            "### 3.3 Universal Node Format",
            "",
            build_universal_node_format(schema, spec),
            "",
            "### 3.4 Core DAG Topology",
            "",
            build_topology_summary(spec),
            "",
            "### 3.5 DAG Invariants",
            "",
            markdown_table(
                ["Invariant", "Statement"],
                [[item.get("id"), item.get("statement")] for item in spec.get("dag_invariants", [])],
            ),
            "",
            "### 3.6 Node ID Format",
            "",
            code_block(
                "\n".join(
                    [
                        f"General pattern: {normalize_text(spec.get('node_id_format', {}).get('general_pattern', ''))}",
                        f"XPD pattern:     {normalize_text(spec.get('node_id_format', {}).get('xpd_pattern', ''))}",
                        "Examples:        "
                        + " | ".join(spec.get("node_id_format", {}).get("examples", [])),
                    ]
                )
            ),
        ]
    )
    if spec.get("node_id_format", {}).get("immutability_rule"):
        parts.extend(["", normalize_text(spec["node_id_format"]["immutability_rule"])])
    parts.extend(
        [
            "",
            "### 3.7 Citation Rules",
            "",
            markdown_table(
                ["Rule", "Statement"],
                [[item.get("rule_id"), item.get("statement")] for item in spec.get("citation_rules", [])],
            ),
            "",
            "### 3.8 Node Status Lifecycle",
            "",
            build_lifecycle_section(spec),
            "",
            "---",
            "",
            SECTION_HEADINGS["modes"],
            "",
            markdown_table(
                ["Mode", "Description", "Best Fit"],
                [
                    [item.get("mode"), item.get("description"), item.get("best_fit")]
                    for item in spec.get("consumption_modes", [])
                ],
            ),
        ]
    )
    express_mode = spec.get("express_mode", {})
    if express_mode.get("description"):
        parts.extend(["", normalize_text(express_mode["description"])])
    parts.extend(["", "### Express Mode Group Map", ""])
    if express_mode.get("groups"):
        parts.append(
            markdown_table(
                ["Group", "Tiers", "Label"],
                [
                    [item.get("group_id"), ", ".join(item.get("tiers", [])), item.get("label")]
                    for item in express_mode.get("groups", [])
                ],
            )
        )
    else:
        parts.append("No Express Mode groups are declared.")
    if express_mode.get("unbundle_determinism_rule"):
        parts.extend(["", f"Unbundle determinism rule: {normalize_text(express_mode['unbundle_determinism_rule'])}"])
    if express_mode.get("deferred_fragment_handling"):
        parts.extend(
            ["", f"Deferred fragment handling: {normalize_text(express_mode['deferred_fragment_handling'])}"]
        )

    parts.extend(["", "---", "", build_tier_section(spec), "", "---", "", SECTION_HEADINGS["precedence"], ""])
    precedence = spec.get("constraint_precedence", {})
    parts.append(
        markdown_table(
            ["Priority", "Tier", "Rationale"],
            [
                [item.get("priority"), item.get("tier"), item.get("rationale")]
                for item in precedence.get("tiers", [])
            ],
        )
    )
    if precedence.get("override_principle"):
        parts.extend(["", normalize_text(precedence["override_principle"])])
    if precedence.get("constraint_classes"):
        parts.extend(
            [
                "",
                markdown_table(
                    ["Class", "Description"],
                    [
                        [item.get("class"), item.get("description")]
                        for item in precedence.get("constraint_classes", [])
                    ],
                ),
            ]
        )
    for key in ("intra_tier_conflict_rule", "physical_constraint_rule", "physical_constraint_escalation"):
        if precedence.get(key):
            label = key.replace("_", " ").capitalize()
            parts.extend(["", f"**{label}**", "", normalize_text(precedence[key])])

    parts.extend(["", "---", "", build_operations_section(spec), "", "---", "", build_extension_system_section(spec)])
    parts.extend(["", "---", "", build_extension_catalog_section(spec), "", "---", "", SECTION_HEADINGS["diagram"], "", build_mermaid(spec)])

    compliance = spec.get("compliance_checklist", {})
    parts.extend(["", "---", "", SECTION_HEADINGS["compliance"], ""])
    if compliance.get("structural_validation"):
        parts.extend(["### Structural Validation", "", checkbox_list(compliance["structural_validation"]), ""])
    if compliance.get("atomic_rule_validation"):
        parts.extend(["### Atomic Rule Validation", "", checkbox_list(compliance["atomic_rule_validation"]), ""])
    if compliance.get("extension_validation"):
        parts.extend(["### Extension Validation", "", checkbox_list(compliance["extension_validation"]), ""])

    parts.extend(
        [
            "---",
            "",
            SECTION_HEADINGS["glossary"],
            "",
            markdown_table(
                ["Term", "Definition"],
                [[item.get("term"), item.get("definition")] for item in spec.get("glossary", [])],
            ),
            "",
            "---",
            "",
            SECTION_HEADINGS["history"],
            "",
            markdown_table(
                ["Version", "Date", "Change Summary"],
                [
                    [item.get("version"), item.get("date"), item.get("summary")]
                    for item in spec.get("version_history", [])
                ],
            ),
            "",
            "---",
            "",
            SECTION_HEADINGS["migration"],
            "",
        ]
    )
    migration = spec.get("tier_migration", {})
    if migration.get("policy"):
        parts.extend([quote_block(f"Migration policy: {migration['policy']}"), ""])
    if migration.get("tier_map"):
        parts.append(
            markdown_table(
                ["From Tier", "To Tier", "Notes"],
                [
                    [item.get("from_tier"), item.get("to_tier"), item.get("notes")]
                    for item in migration.get("tier_map", [])
                ],
            )
        )
        parts.append("")
    if migration.get("rule_map"):
        parts.extend(
            [
                "### Rule-Level Cross-Reference",
                "",
                markdown_table(
                    ["From Rule ID(s)", "To Rule ID(s)", "Consolidation Status", "Notes"],
                    [
                        [
                            item.get("from_rule_ids"),
                            item.get("to_rule_ids"),
                            item.get("consolidation_status"),
                            item.get("notes"),
                        ]
                        for item in migration.get("rule_map", [])
                    ],
                ),
            ]
        )

    markdown = "\n".join(parts).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", markdown)


def validate_schema_and_spec(schema: dict[str, Any], spec: dict[str, Any]) -> None:
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(spec), key=lambda item: list(item.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "<root>"
        raise ValueError(f"Specification failed schema validation at {location}: {error.message}")


def resolve_output_path(spec_path: Path, spec: dict[str, Any], output: str | None) -> Path:
    if output:
        return Path(output)
    return spec_path.with_name(f"DDR System(v{version_label(spec)}).md")


def main() -> int:
    args = parse_args()
    schema_path = Path(args.schema_path)
    spec_path = Path(args.spec_path)
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    if not spec_path.is_file():
        raise FileNotFoundError(f"Specification file not found: {spec_path}")

    schema = load_yaml(schema_path)
    spec = load_yaml(spec_path)
    validate_schema_and_spec(schema, spec)

    output_path = resolve_output_path(spec_path, spec, args.output)
    if output_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"Output already exists: {output_path}. Re-run with --overwrite to replace it."
        )

    markdown = build_markdown(schema, spec)
    issues = validate_output_text(markdown, spec)
    if issues:
        raise ValueError("Generated document failed internal validation:\n- " + "\n- ".join(issues))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(output_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
