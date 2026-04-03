#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / "config.json"
    repo_root = Path(__file__).resolve().parents[4]
    schemas_dir = repo_root / ".agent" / "schemas"
    do_validation = True
    if config_path.exists():
        cfg = json.loads(config_path.read_text())
        rel = cfg.get("default_schema_location", None)
        if rel:
            schemas_dir = (repo_root / rel).resolve()
        do_validation = cfg.get("enable_auto_validation", True)

    target_dir = schemas_dir / args.name
    dts_path = target_dir / f"{args.name}.d.ts"
    backup_path = target_dir / f"{args.name}.d.ts.bak"

    if not dts_path.exists():
        print(f"[ERROR] Schema .d.ts not found at {dts_path}")
        sys.exit(1)

    if not do_validation:
        print("✅ Auto-validation disabled.")
        sys.exit(0)

    print(f"Validating {dts_path}...")
    project_root = Path(__file__).resolve().parents[4]
    tsc_cmd = project_root / ".nodeenv" / "Scripts" / "tsc.cmd"
    if not tsc_cmd.exists():
        tsc_cmd = "tsc"
    result = subprocess.run([str(tsc_cmd), "--noEmit", str(dts_path)], capture_output=True, text=True)

    if result.returncode != 0:
        print("[ERROR] Validation failed. Outputting errors:")
        print(result.stderr or result.stdout)

        # Rollback logic
        if backup_path.exists():
            print(f"[WARN] Rolling back {dts_path} to previous state...")
            shutil.copy(backup_path, dts_path)
        else:
            print("[WARN] No backup found (initial creation). File remains unchanged for manual correction.")
        sys.exit(1)

    print(f"[OK] Schema {args.name} validated successfully.")
    # Create/update backup post successful validation
    shutil.copy(dts_path, backup_path)

if __name__ == "__main__":
    main()
