"""
Audit and optionally clean up stale agent temp run directories in .agent/.temp.

role: operational maintenance utility for agent temp artifacts
entrypoints: main
reads: .agent/.temp directory structure and "retained-on-failure.txt" markers
writes: filesystem (directory removal)
external_io: fs
state_model: stateless
failure_surface: filesystem permission errors; path traversal attempts
coupling: minimal; depends on .agent/.temp structure and naming convention
determinism: input-dependent (filesystem state)
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_STALE_DAYS = 7
RETAINED_MARKER_NAME = "retained-on-failure.txt"
RUN_DIR_PATTERN = re.compile(r"^\d{8}-\d{6}-[0-9a-f]{8}-[a-z0-9][a-z0-9-]*$")
TEMP_ROOT = Path(__file__).resolve().parents[1] / ".temp"


@dataclass(frozen=True)
class RunDirectory:
    """
    Represent a single agent run directory with metadata for audit and cleanup.

    role: value object for run directory state
    lifecycle: transient; constructed during audit
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal

    Attributes
    ----------
    path : Path
        absolute path to the run directory
    age_days : int
        age in whole days since last modification
    modified_at : datetime
        UTC timestamp of last modification
    is_empty : bool
        true if directory contains no files or subdirectories
    is_retained_failure : bool
        true if "retained-on-failure.txt" marker is present
    retention_reason : str | None
        content of the retention marker if present
    is_valid_name : bool
        true if directory name matches RUN_DIR_PATTERN
    """
    path: Path
    age_days: int
    modified_at: datetime
    is_empty: bool
    is_retained_failure: bool
    retention_reason: str | None
    is_valid_name: bool


@dataclass(frozen=True)
class AuditReport:
    """
    Group run directories into categories for reporting and cleanup.

    role: grouped state container for audit results
    lifecycle: transient; constructed during audit
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal

    Attributes
    ----------
    invalid_dirs : list[RunDirectory]
        directories in temp root with invalid name patterns
    empty_run_dirs : list[RunDirectory]
        validly named directories that are empty
    retained_failure_dirs : list[RunDirectory]
        directories containing failure markers
    stale_run_dirs : list[RunDirectory]
        validly named non-retained directories older than threshold
    active_run_dirs : list[RunDirectory]
        validly named non-retained directories within age threshold
    """
    invalid_dirs: list[RunDirectory]
    empty_run_dirs: list[RunDirectory]
    retained_failure_dirs: list[RunDirectory]
    stale_run_dirs: list[RunDirectory]
    active_run_dirs: list[RunDirectory]


def parse_args() -> argparse.Namespace:
    """
    Configure and parse command-line arguments for the cleanup utility.

    purpose: CLI configuration
    preconditions: sys.argv contains valid arguments
    postconditions: returns populated namespace
    mutates: none
    reads: sys.argv
    writes: none
    external_io: none
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: standard argparse validation
    coupling: minimal

    Returns
    -------
    argparse.Namespace
        parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Audit and optionally clean up stale agent temp run directories."
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=DEFAULT_STALE_DAYS,
        help="Age threshold in whole days for stale run-directory reporting.",
    )
    parser.add_argument(
        "--delete-empty",
        action="store_true",
        help="Delete empty run directories inside .agent/.temp.",
    )
    parser.add_argument(
        "--delete-stale",
        action="store_true",
        help="Delete stale non-retained run directories older than --stale-days.",
    )
    parser.add_argument(
        "--delete-retained",
        action="store_true",
        help="Delete retained failure run directories. Use with care.",
    )
    return parser.parse_args()


def is_relative_to(path: Path, root: Path) -> bool:
    """
    Determine if a path is relative to a specified root path.

    purpose: safe path containment check
    preconditions: paths must be valid Path objects
    postconditions: returns boolean containment status
    mutates: none
    reads: filesystem metadata (resolution)
    writes: none
    external_io: none
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        path to check
    root : Path
        potential parent path

    Returns
    -------
    bool
        true if path is under root
    """
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def assert_temp_descendant(path: Path, root: Path) -> None:
    """
    Enforce that a target path resides strictly within the temp root.

    purpose: path traversal protection
    preconditions: root must be the authoritative temp root
    postconditions: raises ValueError if path is outside root
    mutates: none
    reads: filesystem metadata (resolution)
    writes: none
    external_io: none
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: path traversal validation boundary
    coupling: minimal

    Parameters
    ----------
    path : Path
        target directory path
    root : Path
        authoritative temp root path

    Raises
    ------
    ValueError
        if path is outside root or equal to root
    """
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    if resolved_path == resolved_root or not is_relative_to(resolved_path, resolved_root):
        raise ValueError(f"Refusing to operate outside temp root: {resolved_path}")


def iter_temp_directories(root: Path) -> list[Path]:
    """
    List all immediate subdirectories within the temp root.

    purpose: discovery of run directories
    preconditions: root must exist and be a directory
    postconditions: returns list of child directory paths
    mutates: none
    reads: filesystem (directory listing)
    writes: none
    external_io: fs
    determinism: input-dependent (fs state)
    idempotency: yes
    concurrency: thread-safe
    ordering: lexicographical by path name
    aliasing: returns new list of Path objects
    security: none
    coupling: minimal

    Parameters
    ----------
    root : Path
        temp root directory

    Returns
    -------
    list[Path]
        sorted directory paths
    """
    return sorted(path for path in root.iterdir() if path.is_dir())


def load_retention_reason(run_dir: Path) -> str | None:
    """
    Read the retention reason from a marker file if it exists.

    purpose: metadata extraction
    preconditions: run_dir must be a directory
    postconditions: returns string reason or None
    mutates: none
    reads: filesystem (file content)
    writes: none
    external_io: fs
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    run_dir : Path
        run directory to check

    Returns
    -------
    str | None
        retention reason or None if marker missing
    """
    marker = run_dir / RETAINED_MARKER_NAME
    if not marker.is_file():
        return None

    content = marker.read_text(encoding="utf-8").strip()
    return content or "No reason recorded."


def age_in_days(path: Path, *, now: datetime) -> tuple[int, datetime]:
    """
    Calculate the age of a file system path in whole days.

    purpose: stale detection
    preconditions: path must exist
    postconditions: returns integer days and UTC modification time
    mutates: none
    reads: filesystem metadata (stat)
    writes: none
    external_io: fs
    determinism: state-dependent (mtime)
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        target path
    now : datetime
        current UTC time for comparison

    Returns
    -------
    tuple[int, datetime]
        (age_days, modified_at)
    """
    modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age_days = int((now - modified_at).total_seconds() // 86400)
    return age_days, modified_at


def build_run_directory(path: Path, *, now: datetime) -> RunDirectory:
    """
    Construct a RunDirectory model by inspecting the filesystem.

    purpose: state inference
    preconditions: path must be a directory
    postconditions: returns populated RunDirectory object
    mutates: none
    reads: filesystem (stat, iterdir, file exists, file content)
    writes: none
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        directory path
    now : datetime
        current UTC time

    Returns
    -------
    RunDirectory
        inferred run directory state
    """
    age_days, modified_at = age_in_days(path, now=now)
    entries = list(path.iterdir())
    return RunDirectory(
        path=path,
        age_days=age_days,
        modified_at=modified_at,
        is_empty=len(entries) == 0,
        is_retained_failure=(path / RETAINED_MARKER_NAME).is_file(),
        retention_reason=load_retention_reason(path),
        is_valid_name=RUN_DIR_PATTERN.fullmatch(path.name) is not None,
    )


def classify_directories(
    root: Path,
    *,
    stale_days: int = DEFAULT_STALE_DAYS,
    now: datetime | None = None,
) -> AuditReport:
    """
    Scan temp root and categorize all directories into an AuditReport.

    purpose: audit scanning and classification
    preconditions: root must exist
    postconditions: returns populated AuditReport
    mutates: none
    reads: filesystem (directory scan)
    writes: none
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: preserves iter_temp_directories order
    aliasing: none
    security: performs input validation on stale_days
    coupling: minimal

    Parameters
    ----------
    root : Path
        temp root directory
    stale_days : int
        age threshold for staleness; must be >= 0
    now : datetime | None
        current UTC time; defaults to system now

    Returns
    -------
    AuditReport
        categorized audit results

    Raises
    ------
    ValueError
        if stale_days < 0
    """
    if stale_days < 0:
        raise ValueError("--stale-days must be >= 0")

    now = now or datetime.now(timezone.utc)
    invalid_dirs: list[RunDirectory] = []
    empty_run_dirs: list[RunDirectory] = []
    retained_failure_dirs: list[RunDirectory] = []
    stale_run_dirs: list[RunDirectory] = []
    active_run_dirs: list[RunDirectory] = []

    for path in iter_temp_directories(root):
        run_dir = build_run_directory(path, now=now)
        if not run_dir.is_valid_name:
            invalid_dirs.append(run_dir)
        elif run_dir.is_empty:
            empty_run_dirs.append(run_dir)
        elif run_dir.is_retained_failure:
            retained_failure_dirs.append(run_dir)
        elif run_dir.age_days >= stale_days:
            stale_run_dirs.append(run_dir)
        else:
            active_run_dirs.append(run_dir)

    return AuditReport(
        invalid_dirs=invalid_dirs,
        empty_run_dirs=empty_run_dirs,
        retained_failure_dirs=retained_failure_dirs,
        stale_run_dirs=stale_run_dirs,
        active_run_dirs=active_run_dirs,
    )


def delete_run_directories(run_dirs: Iterable[RunDirectory], root: Path) -> list[Path]:
    """
    Physically remove specified run directories from the filesystem.

    purpose: filesystem cleanup
    preconditions: all run_dirs must be descendants of root
    postconditions: target directories are deleted; returns list of deleted paths
    mutates: filesystem (recursive deletion)
    reads: filesystem (existence check)
    writes: filesystem (directory removal)
    external_io: fs
    determinism: input-dependent
    idempotency: no (directories are removed)
    concurrency: not thread-safe (external mutation)
    ordering: sequential
    aliasing: none
    security: enforces temp-descendant constraint
    coupling: minimal

    Parameters
    ----------
    run_dirs : Iterable[RunDirectory]
        directories to remove
    root : Path
        authoritative temp root for safety checks

    Returns
    -------
    list[Path]
        successfully deleted directory paths
    """
    deleted: list[Path] = []
    for run_dir in run_dirs:
        assert_temp_descendant(run_dir.path, root)
        if not run_dir.path.exists():
            continue
        shutil.rmtree(run_dir.path)
        deleted.append(run_dir.path)
    return deleted


def print_section(title: str, run_dirs: Iterable[RunDirectory], *, show_reason: bool = False) -> None:
    """
    Standardize console output for an audit report section.

    purpose: UI reporting
    preconditions: none
    postconditions: section data printed to stdout
    mutates: none
    reads: run_dir properties
    writes: stdout
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe (presuming thread-safe stdout)
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    title : str
        section heading
    run_dirs : Iterable[RunDirectory]
        directories to display
    show_reason : bool
        true to include retention reasons in output
    """
    run_dirs = list(run_dirs)
    print(f"{title}: {len(run_dirs)}")
    for run_dir in run_dirs:
        detail = f"{run_dir.path} ({run_dir.age_days}d old)"
        if show_reason and run_dir.retention_reason:
            detail += f" :: {run_dir.retention_reason}"
        print(f" - {detail}")


def main() -> int:
    """
    Execute the primary audit and cleanup workflow.

    purpose: entrypoint
    preconditions: filesystem access to .agent/.temp
    postconditions: returns exit code; optionally modifies filesystem
    mutates: filesystem (when delete flags set)
    reads: terminal arguments; filesystem state
    writes: terminal output; filesystem deletion
    external_io: fs; terminal
    determinism: state-dependent
    idempotency: no
    concurrency: process-local
    ordering: sequential
    aliasing: none
    security: performs descendant checks on all deletions
    coupling: minimal

    Returns
    -------
    int
        0 on success; 1 if temp root missing
    """
    args = parse_args()
    if not TEMP_ROOT.exists():
        print(f"Temp root does not exist: {TEMP_ROOT}", file=sys.stderr)
        return 1

    report = classify_directories(TEMP_ROOT, stale_days=args.stale_days)
    delete_mode = any([args.delete_empty, args.delete_stale, args.delete_retained])

    print(f"Temp root: {TEMP_ROOT}")
    print(f"Mode: {'destructive' if delete_mode else 'dry-run'}")
    print(f"Stale threshold (days): {args.stale_days}")
    print_section("Invalid directories", report.invalid_dirs)
    print_section("Empty run directories", report.empty_run_dirs)
    print_section(
        "Retained failure directories",
        report.retained_failure_dirs,
        show_reason=True,
    )
    print_section("Stale run directories", report.stale_run_dirs)
    print_section("Active run directories", report.active_run_dirs)

    if not delete_mode:
        return 0

    deleted_paths: list[Path] = []
    if args.delete_empty:
        deleted_paths.extend(delete_run_directories(report.empty_run_dirs, TEMP_ROOT))
    if args.delete_stale:
        deleted_paths.extend(delete_run_directories(report.stale_run_dirs, TEMP_ROOT))
    if args.delete_retained:
        deleted_paths.extend(
            delete_run_directories(report.retained_failure_dirs, TEMP_ROOT)
        )

    print(f"Deleted directories: {len(deleted_paths)}")
    for path in deleted_paths:
        print(f" - {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
