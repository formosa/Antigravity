"""
Manage timestamped run directories under .agent/.temp for single-task artifacts.

role: shared temp-workspace helper
entrypoints: utility functions only
reads: .agent/.temp directory state
writes: .agent/.temp run directories and retained-on-failure markers
external_io: fs
state_model: stateless
failure_surface: fs access errors; invalid path containment
coupling: minimal; depends on managed temp naming contract
determinism: input-dependent (filesystem state)
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

from datetime import datetime
import shutil
from pathlib import Path


RETAINED_MARKER_NAME = "retained-on-failure.txt"
TEMP_ROOT = Path(__file__).resolve().parents[1] / ".temp"


def resolve_temp_root(temp_root: str | Path | None = None) -> Path:
    """
    Resolve the authoritative managed temp root.

    purpose: temp-root resolution
    """
    return Path(temp_root).resolve() if temp_root is not None else TEMP_ROOT.resolve()


def assert_temp_descendant(path: str | Path, *, temp_root: str | Path | None = None) -> Path:
    """
    Enforce that a path is a descendant of the managed temp root.

    purpose: path traversal protection
    """
    resolved_root = resolve_temp_root(temp_root)
    resolved_path = Path(path).resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"Managed temp path must stay within {resolved_root}: {resolved_path}") from exc
    if resolved_path == resolved_root:
        raise ValueError(f"Refusing to operate on the managed temp root directly: {resolved_root}")
    return resolved_path


def create_run_dir(
    task_slug: str,
    *,
    temp_root: str | Path | None = None,
    now: datetime | None = None,
) -> Path:
    """
    Create a timestamp-first managed temp run directory with collision suffixing.

    purpose: managed temp directory creation
    """
    if not task_slug or any(char in task_slug for char in "\\/:*?\"<>|"):
        raise ValueError("task_slug must be non-empty and filesystem-safe.")

    resolved_root = resolve_temp_root(temp_root)
    resolved_root.mkdir(parents=True, exist_ok=True)

    timestamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    base_name = f"{timestamp}-{task_slug}"
    candidate = resolved_root / base_name
    suffix = 1
    while candidate.exists():
        candidate = resolved_root / f"{base_name}-{suffix:02d}"
        suffix += 1
    candidate.mkdir(parents=False, exist_ok=False)
    return candidate


def retain_failure(
    run_dir: str | Path,
    reason: str,
    *,
    temp_root: str | Path | None = None,
) -> Path:
    """
    Mark a managed temp run directory for retention after failure.

    purpose: retained-on-failure marker creation
    """
    resolved_run_dir = assert_temp_descendant(run_dir, temp_root=temp_root)
    resolved_run_dir.mkdir(parents=True, exist_ok=True)
    marker_path = resolved_run_dir / RETAINED_MARKER_NAME
    marker_path.write_text((reason.strip() or "No reason recorded.") + "\n", encoding="utf-8")
    return marker_path


def cleanup_run_dir(run_dir: str | Path, *, temp_root: str | Path | None = None) -> None:
    """
    Delete a managed temp run directory after successful completion.

    purpose: managed temp cleanup
    """
    resolved_run_dir = assert_temp_descendant(run_dir, temp_root=temp_root)
    if resolved_run_dir.exists():
        shutil.rmtree(resolved_run_dir)
