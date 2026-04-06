#!/usr/bin/env python3
"""
Scaffold a new core schema directory from an example artifact.

role: core schema scaffold utility
entrypoints: main
reads: config.json, example artifact
writes: new schema directory and example.md
external_io: fs
state_model: stateless
failure_surface: fs access errors; config missing; example missing
coupling: coupled to core schema directory structure and config.json
determinism: deterministic
concurrency: not thread-safe; process-local
"""

import argparse
import json
import shutil
from pathlib import Path

def main():
    """
    Execute the core schema scaffolding logic.

    purpose: entrypoint
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-file", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / "config.json"
    repo_root = Path(__file__).resolve().parents[4]
    schemas_dir = repo_root / ".agent" / "schemas"
    if config_path.exists():
        cfg = json.loads(config_path.read_text())
        rel = cfg.get("default_schema_location", None)
        if rel:
            schemas_dir = (repo_root / rel).resolve()

    target_dir = schemas_dir / args.name
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file_path = Path(args.target_file)
    if target_file_path.exists():
        shutil.copy(target_file_path, target_dir / "example.md")
        print(f"[OK] Schema scaffolded: {target_dir}")
    else:
        print(f"[ERROR] Target file not found: {target_file_path}")

if __name__ == "__main__":
    main()
