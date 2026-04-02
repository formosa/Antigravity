#!/usr/bin/env python3
"""
Quick validation script for the current Antigravity skill contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import sys
from pathlib import Path

import yaml

REQUIRED_FRONTMATTER_KEYS = {"description", "version"}
OPTIONAL_FRONTMATTER_KEYS = {"name"}
DEPRECATED_PROPERTIES = {"type", "priority", "scope", "tags", "metadata"}
REQUIRED_XML_BLOCKS = (
    "when_to_use",
    "how_to_use",
    "constraints",
    "resources_reference",
)
REQUIRED_ROOT_README_BLOCKS = (
    "document_purpose",
    "authority_order",
    "schema_relationships",
    "modification_history",
)
REQUIRED_SCHEMA_RELATIONSHIP_KEYS = {
    "schema_of_this_skill",
    "owned_schema_ids",
    "consumed_schema_ids",
    "mirror_root",
    "mirror_policy",
}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
DESCRIPTION_BOUNDARY_HINTS = ("do not use", "not for", "not when", "exclude", "except")
WEAK_DESCRIPTION_TERMS = ("helper", "utils", "tools", "stuff", "things", "misc")
RESOURCE_ACTION_HINTS = ("read ", "run ", "execute ", "open ")


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        if not self.valid:
            return "Skill validation failed."
        if self.warnings:
            return "Skill is valid against the current contract, with warnings."
        return "Skill is valid against the current contract."


def extract_tag_block(content: str, block_name: str) -> str | None:
    pattern = rf"(?ms)^[ \t]*<{block_name}>[ \t]*\r?\n(.*?)^[ \t]*</{block_name}>[ \t]*$"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def extract_xml_block(content: str, block_name: str) -> str | None:
    return extract_tag_block(content, block_name)


def extract_frontmatter(content: str) -> tuple[dict | None, str | None]:
    if not content.startswith("---"):
        return None, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        return None, f"Invalid YAML in frontmatter: {exc}"

    if not isinstance(frontmatter, dict):
        return None, "Frontmatter must parse to a key-value mapping."

    return frontmatter, None


def iter_resource_entries(resources_block: str) -> list[str]:
    entries = []
    for raw_line in resources_block.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("-"):
            entry = stripped[1:].strip()
            if entry:
                entries.append(entry)
    return entries


def extract_path_from_resource_entry(entry: str) -> str | None:
    match = re.search(r"`([^`]+)`", entry)
    if match:
        return match.group(1)

    if re.fullmatch(r"[A-Za-z0-9._/\-]+/?", entry):
        return entry

    return None


def split_markdown_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_semver(version_text: str) -> tuple[int, int, int] | None:
    if not SEMVER_PATTERN.fullmatch(version_text):
        return None
    major, minor, patch = version_text.split(".")
    return int(major), int(minor), int(patch)


def classify_semver_change(previous: str, current: str) -> str | None:
    previous_tuple = parse_semver(previous)
    current_tuple = parse_semver(current)
    if previous_tuple is None or current_tuple is None or current_tuple <= previous_tuple:
        return None
    if current_tuple[0] != previous_tuple[0]:
        return "major"
    if current_tuple[1] != previous_tuple[1]:
        return "minor"
    return "patch"


def parse_history_rows(block_text: str) -> tuple[list[dict[str, str]] | None, str | None]:
    table_lines = [line.strip() for line in block_text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return None, "README <modification_history> must contain a header, separator, and at least one data row."

    header = split_markdown_row(table_lines[0])
    expected_header = ["Date", "Version", "SemVer", "Classification", "Description"]
    if header != expected_header:
        return None, "README <modification_history> must use columns: Date | Version | SemVer | Classification | Description."

    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        columns = split_markdown_row(line)
        if len(columns) != 5:
            return None, f"Invalid modification history row: {line}"
        rows.append(dict(zip(expected_header, columns)))

    if not rows:
        return None, "README <modification_history> must contain at least one data row."

    return rows, None


def resolve_resource_path(skill_path: Path, path_text: str) -> Path | None:
    normalized = path_text.replace("\\", "/")
    candidate_paths = [skill_path / Path(normalized), Path.cwd() / Path(normalized)]

    for ancestor in skill_path.parents:
        candidate_paths.append(ancestor / Path(normalized))

    seen: set[Path] = set()
    for candidate in candidate_paths:
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate

    return None


def validate_resource_entries(skill_path: Path, resources_block: str, result: ValidationResult) -> None:
    entries = iter_resource_entries(resources_block)
    if not entries:
        result.warnings.append("`<resources_reference>` is empty. Add skill-local files here once the skill relies on them.")
        return

    for entry in entries:
        path_text = extract_path_from_resource_entry(entry)
        if path_text is None:
            result.warnings.append(
                f"Resource entry should wrap a repo-relative path in backticks and say whether to read or run it: {entry}"
            )
            continue

        if "\\" in path_text:
            result.warnings.append(f"Resource path should use forward slashes: {path_text}")

        resource_path = resolve_resource_path(skill_path, path_text)
        if resource_path is None:
            result.errors.append(f"Referenced resource path does not exist: {path_text}")

        lowered = entry.lower()
        if not any(hint in lowered for hint in RESOURCE_ACTION_HINTS):
            result.warnings.append(f"Resource entry should say whether the file is read or run: {entry}")


def validate_root_readme(skill_path: Path, skill_version: str, result: ValidationResult) -> None:
    readme_path = skill_path / "README.md"
    if not readme_path.exists():
        result.errors.append("README.md not found at skill root.")
        return

    content = readme_path.read_text(encoding="utf-8")
    blocks: dict[str, str] = {}
    for block_name in REQUIRED_ROOT_README_BLOCKS:
        block = extract_tag_block(content, block_name)
        if block is None:
            result.errors.append(f"README.md is missing required <{block_name}> block.")
        else:
            blocks[block_name] = block

    if result.errors:
        return

    try:
        fence_match = re.search(r"```yaml\s*\r?\n(.*?)\r?\n```", blocks["schema_relationships"], re.DOTALL)
        schema_relationships_text = fence_match.group(1) if fence_match else blocks["schema_relationships"]
        schema_relationships = yaml.safe_load(schema_relationships_text)
    except yaml.YAMLError as exc:
        result.errors.append(f"Invalid YAML in README <schema_relationships>: {exc}")
        return

    if not isinstance(schema_relationships, dict):
        result.errors.append("README <schema_relationships> must parse to a YAML mapping.")
        return

    keys = set(schema_relationships.keys())
    missing_keys = REQUIRED_SCHEMA_RELATIONSHIP_KEYS - keys
    unexpected_keys = keys - REQUIRED_SCHEMA_RELATIONSHIP_KEYS
    if missing_keys:
        result.errors.append(f"README <schema_relationships> is missing keys: {', '.join(sorted(missing_keys))}.")
    if unexpected_keys:
        result.errors.append(f"README <schema_relationships> has unexpected keys: {', '.join(sorted(unexpected_keys))}.")

    schema_of_this_skill = schema_relationships.get("schema_of_this_skill")
    owned_schema_ids = schema_relationships.get("owned_schema_ids")
    consumed_schema_ids = schema_relationships.get("consumed_schema_ids")
    mirror_root = schema_relationships.get("mirror_root")
    mirror_policy = schema_relationships.get("mirror_policy")

    if schema_of_this_skill != "skill":
        result.errors.append("README <schema_relationships> must declare `schema_of_this_skill: skill`.")

    for field_name, field_value in (
        ("owned_schema_ids", owned_schema_ids),
        ("consumed_schema_ids", consumed_schema_ids),
    ):
        if not isinstance(field_value, list) or not all(isinstance(item, str) and item.strip() for item in field_value):
            result.errors.append(f"README <schema_relationships> field `{field_name}` must be a list of non-empty schema IDs.")

    if mirror_root != "resources/schema/":
        result.errors.append("README <schema_relationships> must set `mirror_root: resources/schema/`.")

    if mirror_policy != "read-only-derived-from-.agent/schemas":
        result.errors.append(
            "README <schema_relationships> must set `mirror_policy: read-only-derived-from-.agent/schemas`."
        )

    rows, rows_error = parse_history_rows(blocks["modification_history"])
    if rows_error:
        result.errors.append(rows_error)
        return

    assert rows is not None
    for index, row in enumerate(rows):
        version_text = row["Version"]
        semver_text = row["SemVer"].lower()
        if parse_semver(version_text) is None:
            result.errors.append(f"README history version must use semantic versioning: {version_text}")
            continue
        if index == 0:
            if semver_text != "initial":
                result.errors.append("The first README history row must use `initial` in the SemVer column.")
            continue
        previous_version = rows[index - 1]["Version"]
        expected_change = classify_semver_change(previous_version, version_text)
        if expected_change is None:
            result.errors.append(
                f"README history version must strictly increase between {previous_version} and {version_text}."
            )
            continue
        if semver_text != expected_change:
            result.errors.append(
                f"README history row for version {version_text} must use `{expected_change}` in the SemVer column."
            )

    latest_version = rows[-1]["Version"]
    if latest_version != skill_version:
        result.errors.append(
            f"README history latest version `{latest_version}` must match SKILL.md version `{skill_version}`."
        )

    if result.errors:
        return

    mirror_root_path = skill_path / Path(str(mirror_root).rstrip("/"))
    if not mirror_root_path.exists():
        result.errors.append(f"Schema mirror root does not exist: {mirror_root}")
        return

    flat_entries = [entry.name for entry in mirror_root_path.iterdir() if entry.is_file()]
    if flat_entries:
        result.errors.append(
            "Flat files are not allowed directly under `resources/schema/`: " + ", ".join(sorted(flat_entries))
        )

    required_schema_ids: list[str] = []
    for schema_id in [schema_of_this_skill, *(owned_schema_ids or []), *(consumed_schema_ids or [])]:
        if schema_id not in required_schema_ids:
            required_schema_ids.append(schema_id)

    unexpected_dirs = [
        entry.name for entry in mirror_root_path.iterdir() if entry.is_dir() and entry.name not in required_schema_ids
    ]
    if unexpected_dirs:
        result.errors.append(
            "Unexpected schema mirror directories present under `resources/schema/`: "
            + ", ".join(sorted(unexpected_dirs))
        )

    for schema_id in required_schema_ids:
        schema_dir = mirror_root_path / schema_id
        if not schema_dir.exists():
            result.errors.append(f"Missing vendored schema mirror: resources/schema/{schema_id}/")
            continue
        if not (schema_dir / "README.md").exists():
            result.errors.append(f"Schema mirror is missing README.md: resources/schema/{schema_id}/README.md")
        if not list(schema_dir.glob("*.d.ts")):
            result.errors.append(f"Schema mirror is missing a .d.ts contract file: resources/schema/{schema_id}/")


def validate_quality(frontmatter: dict, blocks: dict[str, str], result: ValidationResult) -> None:
    description = str(frontmatter.get("description", "")).strip()
    description_lower = description.lower()
    when_to_use_lower = blocks["when_to_use"].lower()

    if not SEMVER_PATTERN.fullmatch(str(frontmatter.get("version", "")).strip()):
        result.warnings.append("`version` should use semantic versioning, e.g. `1.0.0`.")

    if len(description.split()) < 12:
        result.warnings.append("`description` is short. Add explicit trigger context and task boundaries.")

    if "use when" not in description_lower:
        result.warnings.append("`description` should explicitly say when the skill should trigger.")

    if not any(hint in description_lower for hint in DESCRIPTION_BOUNDARY_HINTS):
        result.warnings.append("`description` should include at least one clear exclusion such as `Do not use when ...`.")

    if any(term in description_lower for term in WEAK_DESCRIPTION_TERMS):
        result.warnings.append("`description` uses vague terms. Replace them with concrete task words and artifacts.")

    if not any(hint in when_to_use_lower for hint in DESCRIPTION_BOUNDARY_HINTS):
        result.warnings.append("`<when_to_use>` should include at least one explicit exclusion.")

    if "example prompt:" not in when_to_use_lower:
        result.warnings.append("`<when_to_use>` should include concrete example prompts for trigger testing.")

    for block_name, block_text in blocks.items():
        if "todo" in block_text.lower():
            result.warnings.append(f"`<{block_name}>` still contains TODO placeholders.")

    if "todo" in description_lower:
        result.warnings.append("`description` still contains TODO placeholders.")


def validate_skill(skill_path: str | Path) -> ValidationResult:
    result = ValidationResult()
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        result.errors.append("SKILL.md not found.")
        return result

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, error = extract_frontmatter(content)
    if error:
        result.errors.append(error)
        return result

    detected_keys = set(frontmatter.keys())
    deprecated = detected_keys.intersection(DEPRECATED_PROPERTIES)
    if deprecated:
        result.errors.append(
            "CRITICAL: Detected deprecated legacy tags "
            f"({', '.join(sorted(deprecated))}). Remove them for current-contract compliance."
        )

    allowed_properties = REQUIRED_FRONTMATTER_KEYS | OPTIONAL_FRONTMATTER_KEYS
    unexpected_keys = detected_keys - allowed_properties
    if unexpected_keys:
        result.errors.append(f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}.")

    missing_required = REQUIRED_FRONTMATTER_KEYS - detected_keys
    if missing_required:
        result.errors.append(f"Missing required frontmatter key(s): {', '.join(sorted(missing_required))}.")

    name_value = frontmatter.get("name")
    if name_value is not None and not SKILL_NAME_PATTERN.fullmatch(str(name_value)):
        result.errors.append("`name` must use lowercase letters, digits, and hyphens only, with a maximum length of 64.")

    description_value = frontmatter.get("description")
    if description_value is not None and not str(description_value).strip():
        result.errors.append("`description` must be non-empty.")

    version_value = frontmatter.get("version")
    if version_value is not None and not str(version_value).strip():
        result.errors.append("`version` must be non-empty.")

    blocks: dict[str, str] = {}
    for block_name in REQUIRED_XML_BLOCKS:
        block = extract_xml_block(content, block_name)
        if block is None:
            result.errors.append(f"Missing required <{block_name}> XML block.")
        else:
            blocks[block_name] = block

    if result.errors:
        return result

    validate_root_readme(skill_path, str(frontmatter.get("version", "")).strip(), result)
    if result.errors:
        return result

    validate_resource_entries(skill_path, blocks["resources_reference"], result)
    validate_quality(frontmatter, blocks, result)
    return result


def print_validation_result(result: ValidationResult) -> None:
    print(result.summary())

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    validation_result = validate_skill(sys.argv[1])
    print_validation_result(validation_result)
    sys.exit(0 if validation_result.valid else 1)
