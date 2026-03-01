#!/usr/bin/env python3
import argparse, json, shutil, subprocess, sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / "config.json"
    schemas_dir = Path("c:/AI/10162025/maggie/Antigravity/.agent/assets/schemas")
    do_validation = True
    if config_path.exists():
        cfg = json.loads(config_path.read_text())
        schemas_dir = Path(cfg.get("default_schema_location", str(schemas_dir)))
        do_validation = cfg.get("enable_auto_validation", True)

    target_dir = schemas_dir / args.name
    dts_path = target_dir / f"{args.name}.d.ts"
    backup_path = target_dir / f"{args.name}.d.ts.bak"

    if not dts_path.exists():
        print(f"❌ Schema .d.ts not found at {dts_path}")
        sys.exit(1)

    if not do_validation:
        print("✅ Auto-validation disabled.")
        sys.exit(0)

    print(f"Validating {dts_path}...")
    result = subprocess.run(["tsc", "--noEmit", str(dts_path)], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Validation Failed. Outputting errors:")
        print(result.stderr or result.stdout)

        # Rollback logic
        if backup_path.exists():
            print(f"⚠️ Rolling back {dts_path} to previous state...")
            shutil.copy(backup_path, dts_path)
        else:
            print("⚠️ No backup found (initial creation). File remains unchanged for manual correction.")
        sys.exit(1)

    print(f"✅ Schema {args.name} validated successfully.")
    # Create/update backup post successful validation
    shutil.copy(dts_path, backup_path)

if __name__ == "__main__":
    main()
