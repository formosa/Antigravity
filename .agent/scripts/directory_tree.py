#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate visual directory tree representations with filtering and statistics.

role: directory tree generation and reporting utility
entrypoints: generate_dir_tree, write_dir_tree, main
reads: filesystem metadata, directory structures
writes: directory tree text artifacts
external_io: fs
state_model: stateless
failure_surface: OSError, re.error
coupling: minimal
determinism: input-dependent
concurrency: not thread-safe
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
    Container for tree-drawing prefix characters.

    role: structural prefix storage
    lifecycle: construction via NamedTuple
    mutability: immutable
    concurrency: thread-safe
    serialization: serializable

    Attributes
    ----------
    middle : str
        prefix for non-last child items
    last : str
        prefix for last child item
    parent_middle : str
        continuation prefix for non-last parent
    parent_last : str
        continuation prefix for last parent
    """

    middle: str
    last: str
    parent_middle: str
    parent_last: str

class TreeStyle(Enum):
    """
    Character style definitions for tree rendering.

    role: style configuration provider
    lifecycle: static enumeration
    mutability: immutable
    concurrency: thread-safe

    Attributes
    ----------
    UTF8 : TreePrefixes
        Unicode box-drawing characters
    ASCII : TreePrefixes
        ASCII-safe replacement characters
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
    Select character set for tree visualization.

    purpose: style resolution
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe

    Parameters
    ----------
    use_ascii : bool
        toggle for ASCII instead of UTF-8; default False

    Returns
    -------
    TreePrefixes
        resolved prefix container
    """

    return TreeStyle.ASCII.value if use_ascii else TreeStyle.UTF8.value

def _configure_console_encoding() -> None:
    """
    Configure stdout for UTF-8 compatibility on Windows.

    purpose: environment normalization
    preconditions: none
    postconditions: sys.stdout may be wrapped in TextIOWrapper
    mutates: sys.stdout
    reads: sys.stdout.encoding
    writes: none
    external_io: none
    determinism: state-dependent
    idempotency: yes
    concurrency: not thread-safe
    security: none
    complexity: low

    Notes
    -----
    noop if stdout is None or already UTF-8
    prevent crashes on CP437/CP1252 consoles
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
    Consolidated configuration for tree traversal and rendering.

    role: configuration carrier
    lifecycle: construction-bound
    mutability: immutable
    concurrency: thread-safe

    Attributes
    ----------
    root_path : Path
        normalized absolute traversal root
    include_all_pattern : Pattern
        global inclusion regex
    exclude_all_pattern : Pattern
        global exclusion regex
    include_files_pattern : Pattern
        file-specific inclusion regex
    exclude_files_pattern : Pattern
        file-specific exclusion regex
    include_folders_pattern : Pattern
        folder-specific inclusion regex
    exclude_folders_pattern : Pattern
        folder-specific exclusion regex
    show_sizes_files : bool
        toggle for file size labels
    show_dates_files : bool
        toggle for file date labels
    show_sizes_folders : bool
        toggle for folder size labels
    show_dates_folders : bool
        toggle for folder date labels
    show_folder_file_count : bool
        toggle for immediate file count
    show_folder_total_file_count : bool
        toggle for recursive file count
    show_folder_subfolder_count : bool
        toggle for immediate folder count
    follow_symlinks : bool
        toggle for directory symlink traversal
    mark_symlinks : bool
        toggle for symlink target labeling
    mark_circular : bool
        toggle for circular reference marking
    mark_errors : bool
        toggle for access error marking
    hide_symlinks : bool
        toggle for symlink omission
    hide_circular_refs : bool
        toggle for circular reference omission
    prefixes : TreePrefixes
        resolved character set
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
    Resolved filesystem metadata for a single path.

    role: path metadata container
    lifecycle: per-path instantiation
    mutability: immutable
    concurrency: thread-safe

    Attributes
    ----------
    path : Path
        original path object
    name : str
        resolved base name
    is_dir : bool
        directory status
    is_file : bool
        file status
    is_symlink : bool
        symlink status
    size_bytes : Optional[int]
        size in bytes; None on error
    mod_time : Optional[float]
        mtime timestamp; None on error
    symlink_target : Optional[str]
        resolved symlink destination; None if not link
    is_dangling_symlink : bool
        link target presence status
    access_error : Optional[str]
        OSError description; None if success
    dev_ino : Optional[DeviceInode]
        filesystem identity (device, inode)
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
    Aggregated traversal statistics for a directory subtree.

    role: recursive statistics container
    lifecycle: per-directory aggregation
    mutability: immutable
    concurrency: thread-safe

    Attributes
    ----------
    recursive_size_bytes : int
        total byte size of subtree
    recursive_files_count : int
        total file count in subtree
    immediate_files_count : int
        file count in immediate directory
    immediate_folders_count : int
        folder count in immediate directory
    """

    recursive_size_bytes: int
    recursive_files_count: int
    immediate_files_count: int
    immediate_folders_count: int

def _compile_regex_pattern(
    pattern_input: Optional[PatternInputType]
) -> Pattern:
    """
    Compile flexible input into a unified regex Pattern.

    purpose: pattern normalization
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    complexity: O(N) where N is pattern length

    Parameters
    ----------
    pattern_input : Optional[PatternInputType]
        string, list of strings, or Pattern object

    Returns
    -------
    Pattern
        compiled regex object; (?!) (match-nothing) for None/empty

    Raises
    ------
    re.error
        on invalid regex syntax
    TypeError
        on unsupported input type
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
    Convert bytes to a binary-prefixed human-readable string.

    purpose: metric formatting
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe

    Parameters
    ----------
    size_bytes : int
        input size in bytes

    Returns
    -------
    str
        formatted string (e.g. "1.5 MB"); "N/A" if negative
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
    Convert POSIX timestamp to standard ISO-like string.

    purpose: temporal formatting
    preconditions: none
    postconditions: none
    mutates: none
    reads: system timezone
    writes: none
    external_io: none
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe

    Parameters
    ----------
    timestamp : float
        seconds since epoch

    Returns
    -------
    str
        YYYY-MM-DD HH:MM:SS; [Invalid Date] on conversion failure
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
    Acquire comprehensive metadata for a specific path.

    purpose: metadata retrieval
    preconditions: path_obj is a valid Path
    postconditions: none
    mutates: none
    reads: filesystem metadata (stat, lstat, readlink)
    writes: none
    external_io: fs
    failure_surface: OSError (captured in access_error)
    determinism: state-dependent (fs state)
    idempotency: yes
    concurrency: thread-safe

    Parameters
    ----------
    path_obj : Path
        target filesystem path
    config : TreeConfig
        traversal policy

    Returns
    -------
    PathDetails
        resolved metadata; access_error is non-None on failure
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
        # RATIONALE: lstat preserves link identity; stat resolves to target
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
    Evaluate path exclusion against hierarchical filter policy.

    purpose: exclusion resolution
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    failure_surface: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe

    Parameters
    ----------
    details : PathDetails
        metadata of current path
    config : TreeConfig
        filter patterns and hiding toggles

    Returns
    -------
    bool
        True if filtered out; False if included
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
    Generate the visual metadata suffix for a tree entry.

    purpose: label formatting
    preconditions: none
    postconditions: none
    mutates: none
    reads: none
    writes: none
    external_io: none
    failure_surface: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe

    Parameters
    ----------
    details : PathDetails
        metadata of current path
    stats : SubtreeStats
        recursive subtree metadata
    config : TreeConfig
        display preferences
    is_circular_ref : bool
        toggle for circular reference marking

    Returns
    -------
    str
        formatted label (e.g. "[1.2 KB, 3 files]"); empty if no labels
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
    Perform hierarchical traversal to generate tree visualization and stats.

    purpose: core recursive traversal
    preconditions: current_path_details is valid
    postconditions: subtree line list and stats
    mutates: none
    reads: directory children (iterdir)
    writes: none
    external_io: fs
    failure_surface: OSError (captured; marked in tree)
    determinism: fs-state-dependent
    idempotency: yes
    concurrency: thread-safe
    security: trust-boundary crossings in symlink traversal
    complexity: O(N) where N is total objects in subtree

    Parameters
    ----------
    current_path_details : PathDetails
        metadata of traversal root
    current_prefix : str
        accumulated line indent + connection graphical prefix
    config : TreeConfig
        traversal policy
    visited_dev_inos : Set[DeviceInode]
        identity set for circularity detection

    Returns
    -------
    Tuple[List[str], SubtreeStats]
        tree lines and aggregated metrics
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

        # INVARIANT: prevents infinite recursion in cyclical filesystems
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

                # RATIONALE: depth-first search requires child-first sorting for tree stability
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
    Public entrypoint for generating a visual directory tree.

    purpose: high-level rendering orchestration
    preconditions: root_dir exists and is readable
    postconditions: list of tree strings
    mutates: none
    reads: filesystem metadata, traversal root
    writes: none
    external_io: fs
    failure_surface: OSError, re.error
    determinism: fs-state-dependent
    idempotency: yes
    concurrency: thread-safe
    security: trust-boundary crossings in symlink traversal
    complexity: O(N) where N is total objects in subtree

    Parameters
    ----------
    root_dir : Union[str, Path]
        traversal root; default "."
    include : Optional[PatternInputType]
        global inclusion regex
    include_files : Optional[PatternInputType]
        file-specific inclusion regex
    include_folders : Optional[PatternInputType]
        folder-specific inclusion regex
    exclude : Optional[PatternInputType]
        global exclusion regex
    exclude_files : Optional[PatternInputType]
        file-specific exclusion regex
    exclude_folders : Optional[PatternInputType]
        folder-specific exclusion regex
    show_sizes : bool
        global size visibility
    show_dates : bool
        global date visibility
    show_file_sizes : Optional[bool]
        override size visibility for files
    show_file_dates : Optional[bool]
        override date visibility for files
    show_folder_file_count : bool
        toggle folder file counting
    show_folder_total_file_count : bool
        toggle total file counting in subtree
    show_folder_subfolder_count : bool
        toggle folder subfolder counting
    show_folder_total_size : Optional[bool]
        recursive size calculation for folders
    follow_symlinks : bool
        symlink traversal toggle
    mark_symlinks : bool
        target labeling toggle
    mark_circular : bool
        circularity labeling toggle
    mark_errors : bool
        access-error labeling toggle
    hide_symlinks : bool
        symlink omission toggle
    hide_circular_refs : bool
        circularity omission toggle
    use_ascii : bool
        ASCII rendering toggle

    Returns
    -------
    List[str]
        sequence of tree lines for display or persistence
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
    Generate directory tree and persist to a file.

    purpose: high-level persistence orchestration
    preconditions: outfile path is writable
    postconditions: file contains serialized tree
    mutates: none
    reads: filesystem metadata
    writes: file contents
    external_io: fs
    failure_surface: OSError
    determinism: fs-state-dependent
    idempotency: no (overwrites)
    concurrency: not thread-safe (due to potential shared output collision)
    complexity: O(N) where N is objects in tree

    Parameters
    ----------
    outfile : Union[str, Path]
        target destination path
    *args : Any
        forwarded to generate_dir_tree
    **kwargs : Any
        forwarded to generate_dir_tree
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
    Standard CLI entrypoint for directory tree generation.

    purpose: top-level orchestration
    preconditions: none
    postconditions: none
    mutates: stdout, local directory_tree.txt
    reads: current working directory
    writes: output file
    external_io: fs, stdout
    failure_surface: OSError
    determinism: fs-state-dependent
    idempotency: no
    concurrency: not thread-safe
    """

    _configure_console_encoding()
    print("Generating default directory tree for '.' to 'directory_tree.txt'...")
    write_dir_tree(outfile="directory_tree.txt")
    print("Default tree generation complete. Check 'directory_tree.txt'.")

if __name__ == "__main__":
    main()
