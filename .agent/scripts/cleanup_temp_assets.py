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
    path: Path
    age_days: int
    modified_at: datetime
    is_empty: bool
    is_retained_failure: bool
    retention_reason: str | None
    is_valid_name: bool


@dataclass(frozen=True)
class AuditReport:
    invalid_dirs: list[RunDirectory]
    empty_run_dirs: list[RunDirectory]
    retained_failure_dirs: list[RunDirectory]
    stale_run_dirs: list[RunDirectory]
    active_run_dirs: list[RunDirectory]


def parse_args() -> argparse.Namespace:
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
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def assert_temp_descendant(path: Path, root: Path) -> None:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    if resolved_path == resolved_root or not is_relative_to(resolved_path, resolved_root):
        raise ValueError(f"Refusing to operate outside temp root: {resolved_path}")


def iter_temp_directories(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir() if path.is_dir())


def load_retention_reason(run_dir: Path) -> str | None:
    marker = run_dir / RETAINED_MARKER_NAME
    if not marker.is_file():
        return None

    content = marker.read_text(encoding="utf-8").strip()
    return content or "No reason recorded."


def age_in_days(path: Path, *, now: datetime) -> tuple[int, datetime]:
    modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age_days = int((now - modified_at).total_seconds() // 86400)
    return age_days, modified_at


def build_run_directory(path: Path, *, now: datetime) -> RunDirectory:
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
    deleted: list[Path] = []
    for run_dir in run_dirs:
        assert_temp_descendant(run_dir.path, root)
        if not run_dir.path.exists():
            continue
        shutil.rmtree(run_dir.path)
        deleted.append(run_dir.path)
    return deleted


def print_section(title: str, run_dirs: Iterable[RunDirectory], *, show_reason: bool = False) -> None:
    run_dirs = list(run_dirs)
    print(f"{title}: {len(run_dirs)}")
    for run_dir in run_dirs:
        detail = f"{run_dir.path} ({run_dir.age_days}d old)"
        if show_reason and run_dir.retention_reason:
            detail += f" :: {run_dir.retention_reason}"
        print(f" - {detail}")


def main() -> int:
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
