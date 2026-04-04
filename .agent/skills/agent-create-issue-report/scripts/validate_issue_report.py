#!/usr/bin/env python3
"""
Compatibility wrapper for the canonical artifact-issue-report validator.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


CANONICAL_SCRIPT_PATH = (
    Path(__file__).resolve().parents[4]
    / ".agent"
    / "skills"
    / "artifact-issue-report"
    / "scripts"
    / "validate_issue_report.py"
)

spec = importlib.util.spec_from_file_location("artifact_issue_report_validate_issue_report", CANONICAL_SCRIPT_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


if __name__ == "__main__":
    raise SystemExit(module.main())
