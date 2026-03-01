#!/usr/bin/env python3
import json, re
from pathlib import Path

def main():
    config_path = Path(__file__).parent.parent / "config.json"
    schemas_dir = Path("c:/AI/10162025/maggie/Antigravity/.agent/assets/schemas")
    if config_path.exists():
        schemas_dir = Path(json.loads(config_path.read_text()).get("default_schema_location", str(schemas_dir)))

    index_md = schemas_dir / "index.md"
    lines = ["# SCHEMA DIRECTORY INDEX\n", "| Schema Name | Version | Description |", "| :--- | :--- | :--- |"]

    for dts_file in schemas_dir.rglob("*.d.ts"):
        content = dts_file.read_text(encoding='utf-8')
        name = dts_file.parent.name

        version_match = re.search(r"version:\s*['\"]([^'\"]+)['\"]", content)
        desc_match = re.search(r"description:\s*['\"]([^'\"]+)['\"]", content)

        version = version_match.group(1) if version_match else "1.0.0"
        desc = desc_match.group(1) if desc_match else "Schema definition."
        lines.append(f"| {name} | {version} | {desc} |")

    index_md.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print("✅ index.md updated successfully.")

if __name__ == "__main__":
    main()
