#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate and format text-based directory tree representations with configurable filtering and statistics.

role: utility script
entrypoints: generate_dir_tree, write_dir_tree, main
reads: env, files
writes: artifacts
external_io: fs
state_model: stateless
failure_surface: access permissions
coupling: minimal
determinism: external-state-dependent
concurrency: unknown
"""

import os
import re
from enum import Enum
import datetime
from pathlib import Path
from typing import (
    Any, List, Optional, Pattern, Tuple, Union, Set, NamedTuple
)

PatternInputType = Union[str, List[str], Pattern]

DeviceInode = Tuple[int, int]

class TreePrefixes(NamedTuple):
    """
    Define connector string fragments for tree branch rendering.

    role: data container
    lifecycle: static definition
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """

    middle: str
    last: str
    parent_middle: str
    parent_last: str

class TreeStyle(Enum):
    """
    Define available character sets for tree rendering.

    role: enumeration
    lifecycle: static definition
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """

    UTF8 = TreePrefixes(
        middle="├── ", last="└── ",
        parent_middle="│   ", parent_last="    "
    )
    ASCII = TreePrefixes(
        middle="+-- ", last="`-- ",
        parent_middle="|   ", parent_last="    "
    )

def _get_tree_prefixes(use_ascii: bool = False) -> TreePrefixes:
    """
    Select tree rendering prefix palette.

    purpose: character set resolution
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    use_ascii : bool
        selection flag; strict boolean; configures ASCII-only output; defaults to False

    Returns
    -------
    TreePrefixes
        resolved prefix set; non-null; none; passed by reference; stable
    """

    return TreeStyle.ASCII.value if use_ascii else TreeStyle.UTF8.value

def _configure_console_encoding() -> None:
    """
    Coerce standard output to UTF-8 encoding dynamically.

    purpose: stream output normalization
    preconditions: none
    postconditions: sys.stdout supports utf-8 encoding
    mutates: global state
    reads: env
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: external-state-dependent
    idempotency: no
    concurrency: not thread-safe
    ordering: none
    aliasing: globally replaces sys.stdout
    security: none
    coupling: minimal
    """

    import sys
    import io

    if sys.stdout is None:
        return

    try:
        current_encoding = getattr(sys.stdout, 'encoding', None) or ''
        if current_encoding.lower().replace('-', '').replace('_', '') != 'utf8':
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer,
                encoding='utf-8',
                errors='replace',
                line_buffering=True
            )
    except (AttributeError, OSError, TypeError):
        pass

class TreeConfig(NamedTuple):
    """
    Define execution context and runtime flags for tree generation.

    role: data container
    lifecycle: static definition
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """

    root_path: Path
    include_all_pattern: Pattern
    exclude_all_pattern: Pattern
    include_files_pattern: Pattern
    exclude_files_pattern: Pattern
    include_folders_pattern: Pattern
    exclude_folders_pattern: Pattern
    show_sizes_files: bool
    show_dates_files: bool
    show_sizes_folders: bool
    show_dates_folders: bool
    show_folder_file_count: bool
    show_folder_total_file_count: bool
    show_folder_subfolder_count: bool
    follow_symlinks: bool
    mark_symlinks: bool
    mark_circular: bool
    mark_errors: bool
    hide_symlinks: bool
    hide_circular_refs: bool
    prefixes: TreePrefixes

class PathDetails(NamedTuple):
    """
    Store comprehensive metadata and resolved statistics for a filesystem path.

    role: data container
    lifecycle: static definition
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """

    path: Path
    name: str
    is_dir: bool
    is_file: bool
    is_symlink: bool
    size_bytes: Optional[int]
    mod_time: Optional[float]
    symlink_target: Optional[str]
    is_dangling_symlink: bool
    access_error: Optional[str]
    dev_ino: Optional[DeviceInode]

class SubtreeStats(NamedTuple):
    """
    Aggregate recursive filesystem statistics for a branch node.

    role: data container
    lifecycle: static definition
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """

    recursive_size_bytes: int
    recursive_files_count: int
    immediate_files_count: int
    immediate_folders_count: int

def _compile_regex_pattern(
    pattern_input: Optional[PatternInputType]
) -> Pattern:
    """
    Resolve raw strings or lists into compiled regular expressions.

    purpose: regex compilation
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    pattern_input : Optional[PatternInputType]
        source pattern data; accommodates string, list of strings, Pattern, or None; none

    Returns
    -------
    Pattern
        compiled regular expression; non-null; none; owned; stable

    Raises
    ------
    ValueError
        if regex compilation fails on string or list input
    TypeError
        if input is not a recognized pattern type
    """

    if pattern_input is None:
        return re.compile("(?!)")
    if isinstance(pattern_input, Pattern):
        return pattern_input
    if isinstance(pattern_input, str):
        try:
            return re.compile(pattern_input)
        except re.error as e:
            raise ValueError(
                f"Invalid regex pattern '{pattern_input}': {e}"
            ) from e
    if isinstance(pattern_input, list):
        if not pattern_input:
            return re.compile("(?!)")
        joined_pattern = "|".join(f"({p})" for p in pattern_input)
        try:
            return re.compile(joined_pattern)
        except re.error as e:
            raise ValueError(
                f"Invalid regex in pattern list {pattern_input}: {e}"
            ) from e
    raise TypeError(
        f"Pattern must be str, list of str, or re.Pattern, "
        f"not {type(pattern_input)}"
    )

def _format_size_human_readable(size_bytes: int) -> str:
    """
    Convert raw byte count to readable magnitude string.

    purpose: byte string formatting
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    size_bytes : int
        raw item size in bytes; expected zero or positive; none

    Returns
    -------
    str
        formatted string representation of size; non-null; none; owned; stable
    """

    if size_bytes < 0: return "N/A"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size_bytes)
    for unit in units:
        if abs(size) < 1024.0 or unit == "PB":
            break
        size /= 1024.0
    return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"

def _format_date_iso(timestamp: float) -> str:
    """
    Format epoch timestamp into ISO 8601 string.

    purpose: timestamp string formatting
    preconditions: valid float timestamp
    postconditions: valid ISO date string returned
    mutates: none
    reads: none
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    timestamp : float
        epoch float timestamp; represents modification time; none

    Returns
    -------
    str
        ISO 8601 subset formatted string or error placeholder; non-null; none; owned; stable
    """

    try:
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError: # pragma: no cover
        return "[Invalid Date]"

def _get_path_details(
    path_obj: Path,
    config: TreeConfig
) -> PathDetails:
    """
    Interrogate filesystem metrics and resolve entity metadata safely.

    purpose: entity metadata interception
    preconditions: valid Path and TreeConfig
    postconditions: complete PathDetails snapshot returned
    mutates: none
    reads: fs state, config
    writes: none
    external_io: fs
    network: none
    subprocess: none
    determinism: external-state-dependent
    idempotency: no
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: stat resolution
    coupling: minimal

    Parameters
    ----------
    path_obj : Path
        active target representation; none; none; none
    config : TreeConfig
        execution flags affecting stat and link follow logic; none; none; none

    Returns
    -------
    PathDetails
        compiled metadata artifact; non-null; none; owned; stable
    """

    name = path_obj.name if path_obj.name else str(path_obj)
    _is_dir: bool = False
    _is_file: bool = False
    _size_bytes: Optional[int] = None
    _mod_time: Optional[float] = None
    _dev_ino: Optional[DeviceInode] = None
    _symlink_target: Optional[str] = None
    _is_dangling_symlink: bool = False
    _access_error: Optional[str] = None

    is_symlink_itself = path_obj.is_symlink()

    try:
        if is_symlink_itself:
            _symlink_target = os.readlink(path_obj)

            if not path_obj.exists():
                _is_dangling_symlink = True

        stat_target_path = path_obj

        if is_symlink_itself and not config.follow_symlinks:

            stat_obj = stat_target_path.lstat()
        else:

            stat_obj = stat_target_path.stat()

        _size_bytes = stat_obj.st_size
        _mod_time = stat_obj.st_mtime
        _dev_ino = (stat_obj.st_dev, stat_obj.st_ino)

        if is_symlink_itself:
            if config.follow_symlinks:
                if not _is_dangling_symlink:

                    _is_dir = path_obj.is_dir()
                    _is_file = path_obj.is_file()
                else:

                    _is_dir = False
                    _is_file = False
            else:

                _is_dir = False

                _is_file = path_obj.is_file() if not _is_dangling_symlink else False
        else:

            _is_dir = path_obj.is_dir()
            _is_file = path_obj.is_file()

    except OSError as e:
        _access_error = e.strerror

        try:
            if is_symlink_itself:
                if config.follow_symlinks:
                    if not _is_dangling_symlink:
                        _is_dir = path_obj.is_dir()
                        _is_file = path_obj.is_file()

                else:
                    _is_dir = False
                    _is_file = path_obj.is_file() if not _is_dangling_symlink else False
            else:
                 _is_dir = path_obj.is_dir()
                 _is_file = path_obj.is_file()
        except OSError:  # pragma: no cover
            pass

        if is_symlink_itself and config.follow_symlinks and not path_obj.exists():
            _is_dangling_symlink = True
            _size_bytes = None
            _mod_time = None

    return PathDetails(
        path=path_obj, name=name, is_dir=_is_dir, is_file=_is_file,
        is_symlink=is_symlink_itself, size_bytes=_size_bytes, mod_time=_mod_time,
        symlink_target=_symlink_target,
        is_dangling_symlink=_is_dangling_symlink,
        access_error=_access_error, dev_ino=_dev_ino
    )

def _is_path_filtered_out(
    details: PathDetails,
    config: TreeConfig
) -> bool:
    """
    Evaluate exclusion regex logic against path metadata.

    purpose: artifact exclusion gating
    preconditions: valid PathDetails and TreeConfig
    postconditions: none
    mutates: none
    reads: config patterns
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    details : PathDetails
        evaluated artifact metadata; none; none; none
    config : TreeConfig
        execution context housing compiled exclusion rules; none; none; none

    Returns
    -------
    bool
        true if entity meets exclusion criteria, false otherwise; non-null; none; primitive; stable
    """

    if config.hide_symlinks and details.is_symlink:
        return True

    name_to_check = details.name
    is_dir_type_for_filtering = details.is_dir

    effective_include_pattern = (
        config.include_folders_pattern
        if is_dir_type_for_filtering else config.include_files_pattern
    )
    effective_exclude_pattern = (
        config.exclude_folders_pattern
        if is_dir_type_for_filtering else config.exclude_files_pattern
    )

    if effective_exclude_pattern is not config.exclude_all_pattern and \
       effective_exclude_pattern.pattern != config.exclude_all_pattern.pattern:
        if effective_exclude_pattern.search(name_to_check):
            return True

    if config.exclude_all_pattern.search(name_to_check):
        return True

    if effective_include_pattern is not config.include_all_pattern and \
       effective_include_pattern.pattern != config.include_all_pattern.pattern:
        if not effective_include_pattern.search(name_to_check):
            return True

    if not config.include_all_pattern.search(name_to_check):
        return True

    return False

def _build_labels_string(
    details: PathDetails,
    stats: SubtreeStats,
    config: TreeConfig,
    is_circular_ref: bool = False
) -> str:
    """
    Compile formatted annotation suffixes for a path entry.

    purpose: annotation string compilation
    preconditions: none
    postconditions: none
    mutates: none
    reads: config, stat metadata
    writes: none
    external_io: none
    network: none
    subprocess: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    details : PathDetails
        evaluated artifact metadata; none; none; none
    stats : SubtreeStats
        aggregated recursive stat rollup; none; none; none
    config : TreeConfig
        execution flags; none; none; none
    is_circular_ref : bool
        circular reference loop flag; strict boolean; none; defaults to False

    Returns
    -------
    str
        formatted suffix enclosing active annotations; non-null; none; owned; stable
    """

    labels: List[str] = []

    if config.mark_symlinks and details.is_symlink and not config.hide_symlinks:
        target_str = details.symlink_target if details.symlink_target is not None else "unknown"
        link_label = f"-> {target_str}"
        if details.is_dangling_symlink:
            link_label += " [DANGLING]"
        labels.append(link_label)

    if config.mark_circular and is_circular_ref:
        labels.append("[CIRCULAR]")
    elif config.mark_errors and details.access_error:
        labels.append(f"[ERROR: {details.access_error}]")

    is_effectively_file_for_labels = details.is_file or \
        (details.is_symlink and not details.is_dir and not details.is_dangling_symlink)

    if is_effectively_file_for_labels:
        if config.show_sizes_files and details.size_bytes is not None:
            labels.append(_format_size_human_readable(details.size_bytes))
        if config.show_dates_files and details.mod_time is not None:
            labels.append(_format_date_iso(details.mod_time))
    elif details.is_dir:
        if config.show_sizes_folders and details.size_bytes is not None:
            labels.append(_format_size_human_readable(stats.recursive_size_bytes))
        if config.show_dates_folders and details.mod_time is not None:
             labels.append(_format_date_iso(details.mod_time))
        if config.show_folder_file_count:
            labels.append(f"{stats.immediate_files_count} files")
        if config.show_folder_subfolder_count:
            labels.append(f"{stats.immediate_folders_count} dirs")
        if config.show_folder_total_file_count:
            labels.append(f"{stats.recursive_files_count} total files")

    return f" [{', '.join(labels)}]" if labels else ""

def _generate_tree_recursive(
    current_path_details: PathDetails,
    current_prefix: str,
    config: TreeConfig,
    visited_dev_inos: Set[DeviceInode]
) -> Tuple[List[str], SubtreeStats]:
    """
    Traverse filesystem iteratively to construct textual hierarchy.

    purpose: recursive hierarchy generation
    preconditions: visited_dev_inos initialized
    postconditions: none
    mutates: visited_dev_inos
    reads: fs state, config logic
    writes: none
    external_io: fs
    network: none
    subprocess: none
    determinism: external-state-dependent
    idempotency: no
    concurrency: not thread-safe
    ordering: lexicographical by dir flag then name
    aliasing: none
    security: bounds iteration against device nodes
    coupling: minimal

    Parameters
    ----------
    current_path_details : PathDetails
        active root element metadata; none; none; none
    current_prefix : str
        accumulated line-prefix text; none; none; none
    config : TreeConfig
        execution and filtering context; none; none; none
    visited_dev_inos : Set[DeviceInode]
        circular recursion watchdog tracking; none; none; none

    Returns
    -------
    Tuple[List[str], SubtreeStats]
        tree string accumulation and aggregate metrics; non-null; ordered; none; stable
    """

    lines: List[str] = []
    current_recursive_size = 0
    current_recursive_files = 0

    is_file_like_for_stats = current_path_details.is_file or \
        (current_path_details.is_symlink and
         not current_path_details.is_dir and
         not current_path_details.is_dangling_symlink and
         (config.follow_symlinks or current_path_details.size_bytes is not None))

    if is_file_like_for_stats and current_path_details.size_bytes is not None:
        current_recursive_size = current_path_details.size_bytes
        current_recursive_files = 1

    immediate_files = 0
    immediate_folders = 0
    is_circular_target = False

    entry_line_base = current_prefix + current_path_details.name
    children_lines: List[str] = []

    if current_path_details.is_dir:
        entry_line_base += "/"

        if current_path_details.dev_ino and current_path_details.dev_ino in visited_dev_inos:
            is_circular_target = True
            if config.hide_circular_refs:
                return [], SubtreeStats(0, 0, 0, 0)
        elif current_path_details.dev_ino:
            visited_dev_inos.add(current_path_details.dev_ino)

        if not (is_circular_target and config.hide_circular_refs):
            child_items_to_process: List[PathDetails] = []
            raw_children_paths: List[Path] = []
            error_listing_children: Optional[str] = None

            try:
                raw_children_paths = list(current_path_details.path.iterdir())
            except OSError as e:
                error_listing_children = e.strerror

            if error_listing_children and config.mark_errors:
                if current_prefix.endswith(config.prefixes.middle):
                    parent_line_prefix_segment = current_prefix[:-len(config.prefixes.middle)]
                elif current_prefix.endswith(config.prefixes.last):
                    parent_line_prefix_segment = current_prefix[:-len(config.prefixes.last)]
                else:
                    parent_line_prefix_segment = current_prefix

                indent_for_error_line_children = config.prefixes.parent_last
                connector_for_error_line = config.prefixes.last
                error_line_prefix = parent_line_prefix_segment + indent_for_error_line_children + connector_for_error_line
                children_lines.append(error_line_prefix + f"[ERROR listing contents: {error_listing_children}]")
            else:

                all_child_details = [
                    _get_path_details(child_path_obj, config)
                    for child_path_obj in raw_children_paths
                ]

                all_child_details.sort(
                    key=lambda d: (not d.is_dir, d.name.lower())
                )

                child_items_to_process = [
                    d for d in all_child_details
                    if not _is_path_filtered_out(d, config)
                ]

                num_children_to_render = len(child_items_to_process)
                for i, child_details_item in enumerate(child_items_to_process):
                    is_last_child = (i == num_children_to_render - 1)

                    if current_prefix.endswith(config.prefixes.middle):
                        parent_line_prefix_segment = current_prefix[:-len(config.prefixes.middle)]
                    elif current_prefix.endswith(config.prefixes.last):
                        parent_line_prefix_segment = current_prefix[:-len(config.prefixes.last)]
                    else:
                        parent_line_prefix_segment = current_prefix

                    indent_for_childs_children = config.prefixes.parent_last if is_last_child else config.prefixes.parent_middle
                    connector_for_child = config.prefixes.last if is_last_child else config.prefixes.middle
                    child_line_full_prefix = parent_line_prefix_segment + indent_for_childs_children + connector_for_child

                    if child_details_item.is_dir:
                        immediate_folders += 1
                    elif child_details_item.is_file or \
                        (child_details_item.is_symlink and not child_details_item.is_dangling_symlink and not child_details_item.is_dir):
                        immediate_files += 1

                    if not is_circular_target:
                        sub_lines, sub_stats = _generate_tree_recursive(
                            child_details_item,
                            child_line_full_prefix,
                            config,
                            visited_dev_inos.copy()
                        )
                        children_lines.extend(sub_lines)
                        current_recursive_size += sub_stats.recursive_size_bytes
                        current_recursive_files += sub_stats.recursive_files_count

            if current_path_details.dev_ino and not is_circular_target and current_path_details.dev_ino in visited_dev_inos:
                visited_dev_inos.remove(current_path_details.dev_ino)

    current_item_stats = SubtreeStats(
        recursive_size_bytes=current_recursive_size,
        recursive_files_count=current_recursive_files,
        immediate_files_count=immediate_files,
        immediate_folders_count=immediate_folders
    )

    labels_str = _build_labels_string(
        current_path_details, current_item_stats, config, is_circular_target
    )
    lines.append(entry_line_base + labels_str)
    lines.extend(children_lines)

    return lines, current_item_stats

def generate_dir_tree(
    root_dir: Union[str, Path] = ".",
    include: Optional[PatternInputType] = ".*",
    include_files: Optional[PatternInputType] = None,
    include_folders: Optional[PatternInputType] = None,
    exclude: Optional[PatternInputType] = "(?!)",
    exclude_files: Optional[PatternInputType] = None,
    exclude_folders: Optional[PatternInputType] = None,
    show_sizes: bool = True,
    show_dates: bool = False,
    show_file_sizes: Optional[bool] = None,
    show_file_dates: Optional[bool] = None,
    show_folder_file_count: bool = True,
    show_folder_total_file_count: bool = False,
    show_folder_subfolder_count: bool = True,
    show_folder_total_size: Optional[bool] = None,
    follow_symlinks: bool = True,
    mark_symlinks: bool = True,
    mark_circular: bool = True,
    mark_errors: bool = True,
    hide_symlinks: bool = False,
    hide_circular_refs: bool = False,
    use_ascii: bool = False
) -> List[str]:
    """
    Generate textual directory tree string list.

    purpose: format text-based directory tree representations
    preconditions: none
    postconditions: none
    mutates: none
    reads: files
    writes: none
    external_io: fs
    network: none
    subprocess: none
    determinism: external-state-dependent
    idempotency: no
    concurrency: unknown
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    root_dir : Union[str, Path]
        root directory path; none; none; defaults to "."
    include : Optional[PatternInputType]
        include pattern; none; none; defaults to ".*"
    include_files : Optional[PatternInputType]
        include files pattern; none; none; defaults to None
    include_folders : Optional[PatternInputType]
        include folders pattern; none; none; defaults to None
    exclude : Optional[PatternInputType]
        exclude pattern; none; none; defaults to "(?!)"
    exclude_files : Optional[PatternInputType]
        exclude files pattern; none; none; defaults to None
    exclude_folders : Optional[PatternInputType]
        exclude folders pattern; none; none; defaults to None
    show_sizes : bool
        show sizes flag; strict boolean; none; defaults to True
    show_dates : bool
        show dates flag; strict boolean; none; defaults to False
    show_file_sizes : Optional[bool]
        show file sizes flag; none; none; defaults to None
    show_file_dates : Optional[bool]
        show file dates flag; none; none; defaults to None
    show_folder_file_count : bool
        show folder file count flag; strict boolean; none; defaults to True
    show_folder_total_file_count : bool
        show folder total file count flag; strict boolean; none; defaults to False
    show_folder_subfolder_count : bool
        show folder subfolder count flag; strict boolean; none; defaults to True
    show_folder_total_size : Optional[bool]
        show folder total size flag; none; none; defaults to None
    follow_symlinks : bool
        follow symlinks flag; strict boolean; none; defaults to True
    mark_symlinks : bool
        mark symlinks flag; strict boolean; none; defaults to True
    mark_circular : bool
        mark circular flag; strict boolean; none; defaults to True
    mark_errors : bool
        mark errors flag; strict boolean; none; defaults to True
    hide_symlinks : bool
        hide symlinks flag; strict boolean; none; defaults to False
    hide_circular_refs : bool
        hide circular refs flag; strict boolean; none; defaults to False
    use_ascii : bool
        use ASCII flag; strict boolean; none; defaults to False

    Returns
    -------
    List[str]
        tree lines; non-null; ordered; none; stable
    """

    try:
        resolved_root_dir = Path(root_dir).resolve()
    except OSError as e:
        return [f"Error resolving root directory '{root_dir}': {e.strerror}"]

    effective_show_file_sizes = show_sizes if show_file_sizes is None else show_file_sizes
    effective_show_file_dates = show_dates if show_file_dates is None else show_file_dates

    if show_folder_total_size is not None:
        effective_show_folder_sizes = show_folder_total_size
    else:
        effective_show_folder_sizes = show_sizes
    effective_show_folder_dates = show_dates

    compiled_include_all = _compile_regex_pattern(include if include is not None else ".*")
    compiled_exclude_all = _compile_regex_pattern(exclude if exclude is not None else "(?!)")

    config = TreeConfig(
        root_path=resolved_root_dir,
        include_all_pattern=compiled_include_all,
        exclude_all_pattern=compiled_exclude_all,
        include_files_pattern=_compile_regex_pattern(include_files) if include_files is not None else compiled_include_all,
        exclude_files_pattern=_compile_regex_pattern(exclude_files) if exclude_files is not None else compiled_exclude_all,
        include_folders_pattern=_compile_regex_pattern(include_folders) if include_folders is not None else compiled_include_all,
        exclude_folders_pattern=_compile_regex_pattern(exclude_folders) if exclude_folders is not None else compiled_exclude_all,
        show_sizes_files=effective_show_file_sizes,
        show_dates_files=effective_show_file_dates,
        show_sizes_folders=effective_show_folder_sizes,
        show_dates_folders=effective_show_folder_dates,
        show_folder_file_count=show_folder_file_count,
        show_folder_total_file_count=show_folder_total_file_count,
        show_folder_subfolder_count=show_folder_subfolder_count,
        follow_symlinks=follow_symlinks,
        mark_symlinks=mark_symlinks,
        mark_circular=mark_circular,
        mark_errors=mark_errors,
        hide_symlinks=hide_symlinks,
        hide_circular_refs=hide_circular_refs,
        prefixes=_get_tree_prefixes(use_ascii)
    )

    root_details = _get_path_details(resolved_root_dir, config)

    if _is_path_filtered_out(root_details, config):
        name_display = root_details.name

        if resolved_root_dir.is_dir() and not name_display.endswith("/"):
             name_display += "/"
        return [f"{name_display} [FILTERED]"]

    all_lines, _ = _generate_tree_recursive(
        current_path_details=root_details,
        current_prefix="",
        config=config,
        visited_dev_inos=set()
    )
    return all_lines

def write_dir_tree(
    outfile: Union[str, Path] = "directory_tree.txt",
    *args: Any,
    **kwargs: Any
) -> None:
    """
    Write textual directory tree to file.

    purpose: write textual directory tree string list to out path
    preconditions: none
    postconditions: file exists at out path
    mutates: none
    reads: env, files
    writes: artifacts
    external_io: fs
    network: none
    subprocess: none
    determinism: external-state-dependent
    idempotency: no
    concurrency: not thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    outfile : Union[str, Path]
        output file path; none; none; defaults to "directory_tree.txt"
    *args : Any
        forwarded arguments; none; none; none
    **kwargs : Any
        forwarded arguments; none; none; none
    """

    lines = generate_dir_tree(*args, **kwargs)
    out_path = Path(outfile)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as e:  # pragma: no cover
        print(f"Error: Could not write to output file {out_path}: {e.strerror}", file=os.sys.stderr)

def main() -> None:
    """
    Generate default diagnostic directory tree.

    purpose: generate default tree output to directory_tree.txt
    preconditions: none
    postconditions: directory_tree.txt is written
    mutates: stdio encoding
    reads: env, files
    writes: artifacts
    external_io: fs
    network: none
    subprocess: none
    determinism: external-state-dependent
    idempotency: no
    concurrency: not thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal
    """

    _configure_console_encoding()
    print("Generating default directory tree for '.' to 'directory_tree.txt'...")
    write_dir_tree(outfile="directory_tree.txt")
    print("Default tree generation complete. Check 'directory_tree.txt'.")

if __name__ == "__main__":
    main()
