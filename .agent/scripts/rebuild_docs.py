"""
Rebuild Sphinx documentation outputs with managed-temp warning capture.

role: documentation rebuild utility
entrypoints: main
reads: docs source tree
writes: docs/_build outputs and failure-only managed temp logs
external_io: fs, sphinx subprocesses
state_model: stateless
failure_surface: sphinx build failures; output validation failures; fs access errors
coupling: coupled to local docs/ layout and managed temp helper
determinism: input-dependent (filesystem state and sphinx results)
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

from managed_temp import RETAINED_MARKER_NAME, cleanup_run_dir, create_run_dir, retain_failure


TASK_SLUG = "rebuild-docs"
NEEDS_LOG_NAME = "refresh-context.log"
HTML_LOG_NAME = "refresh-context-html.log"


@dataclass(frozen=True)
class BuildSpec:
    """
    Describe one Sphinx build invocation.

    purpose: immutable build configuration
    """

    builder: str
    output_dir: Path
    log_path: Path
    extra_args: tuple[str, ...] = ()


def repo_root() -> Path:
    """
    Resolve the repository root for docs builds.

    purpose: path resolution base
    """
    return Path(__file__).resolve().parents[2]


def count_warning_lines(log_path: Path) -> int:
    """
    Count Sphinx warning lines in a log file.

    purpose: warning reporting
    """
    if not log_path.exists():
        return 0
    return sum(1 for line in log_path.read_text(encoding="utf-8").splitlines() if line.startswith("WARNING:"))


def validate_outputs(root: Path) -> list[str]:
    """
    Verify that required docs outputs exist and are non-empty.

    purpose: post-build validation
    """
    errors: list[str] = []
    needs_json = root / "docs" / "_build" / "json" / "needs.json"
    html_index = root / "docs" / "_build" / "html" / "index.html"

    if not needs_json.exists():
        errors.append(f"Missing Sphinx needs export: {needs_json}")
    elif needs_json.stat().st_size == 0:
        errors.append(f"Sphinx needs export is empty: {needs_json}")

    if not html_index.exists():
        errors.append(f"Missing Sphinx HTML index: {html_index}")

    return errors


def build_specs(root: Path, run_dir: Path) -> list[BuildSpec]:
    """
    Construct the ordered Sphinx build specifications for the local docs tree.

    purpose: deterministic build sequencing
    """
    return [
        BuildSpec(
            builder="needs",
            output_dir=root / "docs" / "_build" / "json",
            log_path=run_dir / NEEDS_LOG_NAME,
        ),
        BuildSpec(
            builder="html",
            output_dir=root / "docs" / "_build" / "html",
            log_path=run_dir / HTML_LOG_NAME,
            extra_args=("-a",),
        ),
    ]


def run_sphinx_build(root: Path, python_executable: str, spec: BuildSpec) -> subprocess.CompletedProcess[str]:
    """
    Execute a single Sphinx build and capture stdout/stderr.

    purpose: subprocess execution
    """
    command = [
        python_executable,
        "-m",
        "sphinx",
        "-b",
        spec.builder,
        *spec.extra_args,
        "-w",
        str(spec.log_path),
        "docs",
        str(spec.output_dir),
    ]
    return subprocess.run(
        command,
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def run_rebuild(
    root: Path,
    *,
    python_executable: str | None = None,
    temp_root: str | Path | None = None,
) -> int:
    """
    Rebuild docs, validating outputs and enforcing managed temp retention rules.

    purpose: full docs rebuild workflow
    """
    run_dir = create_run_dir(TASK_SLUG, temp_root=temp_root)
    python_executable = python_executable or sys.executable

    try:
        for spec in build_specs(root, run_dir):
            result = run_sphinx_build(root, python_executable, spec)
            if result.returncode != 0:
                reason = f"Sphinx {spec.builder} build failed with exit code {result.returncode}."
                retain_failure(run_dir, reason, temp_root=temp_root)
                if result.stdout:
                    print(result.stdout.rstrip())
                if result.stderr:
                    print(result.stderr.rstrip(), file=sys.stderr)
                print(f"[ERROR] {reason}")
                print(f"[ERROR] Retained logs at {run_dir}")
                return 1

        output_errors = validate_outputs(root)
        warning_count = sum(count_warning_lines(spec.log_path) for spec in build_specs(root, run_dir))
        if output_errors:
            reason = "Docs rebuild completed but output validation failed."
            retain_failure(run_dir, reason, temp_root=temp_root)
            for error in output_errors:
                print(f"[ERROR] {error}", file=sys.stderr)
            print(f"[ERROR] Retained logs at {run_dir}")
            return 1

        cleanup_run_dir(run_dir, temp_root=temp_root)
        print("[OK] Documentation rebuild completed successfully.")
        print(f"Warnings detected: {warning_count}")
        if warning_count > 5:
            print('Follow-up suggestion: Documentation Cleanup')
        return 0
    except Exception as exc:
        retain_failure(run_dir, str(exc), temp_root=temp_root)
        print(f"[ERROR] Docs rebuild failed unexpectedly: {exc}", file=sys.stderr)
        print(f"[ERROR] Retained logs at {run_dir}", file=sys.stderr)
        return 1


def main() -> int:
    """
    Execute the docs rebuild workflow from the repository root.

    purpose: CLI entrypoint
    """
    return run_rebuild(repo_root())


if __name__ == "__main__":
    raise SystemExit(main())
