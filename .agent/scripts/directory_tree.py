#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a directory tree with filtering, labeling, and reporting.

This script creates a visual representation of directory structures. It
provides extensive options for filtering files/folders and adding detailed
labels about sizes, dates, file counts, and more, adhering to functional
programming principles where practical.

It can be used as a module or as a command-line utility (though
command-line argument parsing is not implemented in this version).
Default execution of `main()` will generate `directory_tree.txt` in the
current directory.

Command-Line Usage
------------------
**Run script to generate tree file (default output: directory_tree.txt):**

.. code-block:: bash

    # Generate tree of current directory to file
    python directory_tree.py

    # View the generated tree
    cat directory_tree.txt        # Linux/macOS
    type directory_tree.txt       # Windows

**Quick terminal output using Python one-liner:**

.. code-block:: bash

    # Print tree directly to terminal (no file created)
    python -c "exec(open('directory_tree.py').read()); print('\\n'.join(generate_dir_tree('.')))"

    # Print tree with ASCII characters for legacy terminals
    python -c "exec(open('directory_tree.py').read()); print('\\n'.join(generate_dir_tree('.', use_ascii=True)))"

**Redirect output to custom file:**

.. code-block:: bash

    # Generate tree and redirect to custom filename
    python -c "exec(open('directory_tree.py').read()); print('\\n'.join(generate_dir_tree('my_project')))" > my_tree.txt

Module Usage
------------
**Basic usage - generate tree of current directory:**

>>> from pathlib import Path
>>> # Import using importlib for hyphenated filename
>>> import importlib.util
>>> spec = importlib.util.spec_from_file_location(
...     "directory_tree", Path("directory_tree.py")
... )
>>> module = importlib.util.module_from_spec(spec)
>>> # spec.loader.exec_module(module)  # Execute to load
>>> # tree_lines = module.generate_dir_tree(".")
>>> # for line in tree_lines[:5]: print(line)

**Generate tree with filtering and custom options:**

>>> # Exclude .git and __pycache__, show only Python files
>>> # tree = generate_dir_tree(
>>> #     root_dir="my_project",
>>> #     include_files=r"\\.py$",
>>> #     exclude_folders=[r"\\.git", r"__pycache__"],
>>> #     show_file_dates=True,
>>> #     use_ascii=True  # For legacy terminals
>>> # )

**Write tree directly to file:**

>>> # write_dir_tree("output.txt", root_dir=".", show_sizes=True)

**Access tree style prefixes programmatically:**

>>> # from directory_tree import TreeStyle
>>> # print(TreeStyle.UTF8.value.middle)  # "├── "
>>> # print(TreeStyle.ASCII.value.middle)  # "+-- "
"""

import os
import re
from enum import Enum
import datetime
from pathlib import Path
from typing import (
    Any, List, Optional, Pattern, Tuple, Union, Set, NamedTuple
)

# --- Type Aliases ---
PatternInputType = Union[str, List[str], Pattern]
# dev_t, ino_t
DeviceInode = Tuple[int, int]


class TreePrefixes(NamedTuple):
    """
    Container for tree-drawing prefix characters.

    Attributes
    ----------
    middle : str
        Prefix for non-last items at current level (e.g., "├── " or "+-- ").
    last : str
        Prefix for the last item at current level (e.g., "└── " or "`-- ").
    parent_middle : str
        Continuation prefix when parent was not last (e.g., "│   " or "|   ").
    parent_last : str
        Continuation prefix when parent was last (e.g., "    ").
    """
    middle: str
    last: str
    parent_middle: str
    parent_last: str


class TreeStyle(Enum):
    """
    Tree-drawing character style options.

    This enum provides pre-configured `TreePrefixes` for rendering directory
    trees with either Unicode box-drawing characters or ASCII-safe alternatives.

    Attributes
    ----------
    UTF8 : TreePrefixes
        Unicode box-drawing characters (├, └, │). Default for modern terminals
        with UTF-8 support. Produces visually appealing output.
    ASCII : TreePrefixes
        ASCII-safe characters (+, `, |). Compatible with legacy terminals,
        older systems, or environments with limited Unicode support.

    Examples
    --------
    >>> TreeStyle.UTF8.value.middle
    '├── '
    >>> TreeStyle.ASCII.value.last
    '`-- '
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
    Return the appropriate tree prefix character set.

    Parameters
    ----------
    use_ascii : bool, default False
        If True, return ASCII-safe characters for legacy terminal compatibility.
        If False, return UTF-8 box-drawing characters.

    Returns
    -------
    TreePrefixes
        NamedTuple containing the four prefix strings.
    """
    return TreeStyle.ASCII.value if use_ascii else TreeStyle.UTF8.value


def _configure_console_encoding() -> None:
    """
    Configure console stdout for UTF-8 output if necessary.

    On Windows systems with non-UTF-8 console encoding (e.g., CP437, CP1252),
    this wraps sys.stdout to handle UTF-8 characters gracefully. Characters
    that cannot be encoded are replaced with a placeholder to prevent crashes.

    This function should be called once at program startup before any
    print statements that may contain non-ASCII characters.

    Notes
    -----
    This function has no effect if:
    - stdout is already UTF-8 encoded
    - stdout is None (e.g., in some embedded environments)
    - stdout lacks a buffer attribute (e.g., some IDE consoles)
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
        pass  # stdout may not have buffer in some environments

class TreeConfig(NamedTuple):
    """
    Configuration for tree generation.

    This NamedTuple holds all resolved settings that guide the tree
    generation process, including filter patterns, display preferences,
    and behavior for special file system entities like symbolic links.

    Attributes
    ----------
    root_path : Path
        Resolved absolute path of the root directory for traversal.
    include_all_pattern : Pattern
        Compiled regex pattern to include any path by name. Applied if
        more specific file/folder include patterns do not cause exclusion.
    exclude_all_pattern : Pattern
        Compiled regex pattern to exclude any path by name. Takes precedence
        over include patterns.
    include_files_pattern : Pattern
        Compiled regex pattern to include files by name.
    exclude_files_pattern : Pattern
        Compiled regex pattern to exclude files by name. Takes precedence.
    include_folders_pattern : Pattern
        Compiled regex pattern to include folders by name.
    exclude_folders_pattern : Pattern
        Compiled regex pattern to exclude folders by name. Takes precedence.
    show_sizes_files : bool
        Whether to display sizes for files.
    show_dates_files : bool
        Whether to display modification dates for files.
    show_sizes_folders : bool
        Whether to display total sizes for folders (recursive).
    show_dates_folders : bool
        Whether to display modification dates for folders themselves.
    show_folder_file_count : bool
        Whether to show count of immediate files within a folder.
    show_folder_total_file_count : bool
        Whether to show count of all files recursively within a folder.
    show_folder_subfolder_count : bool
        Whether to show count of immediate subfolders within a folder.
    follow_symlinks : bool
        If True, symlinks to directories will be traversed. If False,
        they are treated as link entries, not directories.
    mark_symlinks : bool
        If True, symlink entries will be marked with '-> target'.
    mark_circular : bool
        If True, circular references (e.g., symlink pointing to an ancestor)
        will be marked as '[CIRCULAR]' and not traversed further.
    mark_errors : bool
        If True, errors encountered (e.g., permission denied) will be
        marked in the tree.
    hide_symlinks : bool
        If True, all symbolic links will be completely omitted from the tree.
        This takes precedence over include/exclude patterns for symlinks.
    hide_circular_refs : bool
        If True, when a circular reference target is encountered, it will be
        omitted from the tree instead of being marked '[CIRCULAR]'.
    prefixes : TreePrefixes
        The tree-drawing character set (UTF-8 or ASCII) to use for
        generating tree line prefixes.
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
    Holds processed information about a path.

    This structure aggregates details obtained by inspecting a file system
    path, such as its type, size, modification time, and symlink status.

    Attributes
    ----------
    path : Path
        The `pathlib.Path` object for this entry.
    name : str
        The base name of the file or directory.
    is_dir : bool
        True if the path is a directory. For symlinks, this depends on
        `TreeConfig.follow_symlinks` and whether the link is dangling.
        If not following symlinks, symlinks to directories have `is_dir=False`.
    is_file : bool
        True if the path is a file. For symlinks, this reflects the target's
        type if `TreeConfig.follow_symlinks` is true and the link is not
        dangling.
    is_symlink : bool
        True if the path itself is a symbolic link.
    size_bytes : Optional[int]
        Size in bytes. For symlinks, this is the size of the link itself if
        not following, or the target's size if following and not dangling.
        None if an error occurred or not applicable (e.g., dangling symlink
        being followed).
    mod_time : Optional[float]
        Last modification time as a POSIX timestamp. Similar symlink logic
        to `size_bytes`. None if an error occurred.
    symlink_target : Optional[str]
        The target path of the symlink, if `is_symlink` is True.
        None otherwise.
    is_dangling_symlink : bool
        True if `is_symlink` is True and the symlink's target does not exist.
    access_error : Optional[str]
        A description of any `OSError` encountered while accessing path info.
        None if no error.
    dev_ino : Optional[DeviceInode]
        A tuple of (device ID, inode number) used for circular reference
        detection. None if an error occurred.
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
    Aggregated statistics for a directory subtree.

    These stats are calculated recursively for each directory.

    Attributes
    ----------
    recursive_size_bytes : int
        Total size of all files within this directory and its subdirectories.
    recursive_files_count : int
        Total number of files within this directory and its subdirectories.
    immediate_files_count : int
        Number of files directly within this directory (not in subdirectories).
    immediate_folders_count : int
        Number of subfolders directly within this directory.
    """
    recursive_size_bytes: int
    recursive_files_count: int
    immediate_files_count: int
    immediate_folders_count: int


# ───────────── Private Helper Functions: Compilation & Formatting ─────────────

def _compile_regex_pattern(
    pattern_input: Optional[PatternInputType]
) -> Pattern:
    """
    Compile input into a regex Pattern object.

    An empty or None input results in a pattern that matches nothing.
    This function is used to prepare regex patterns for filtering.

    Parameters
    ----------
    pattern_input : Optional[PatternInputType]
        The input to compile. Can be:
        - A string (single regex pattern).
        - A list of strings (ORed together into a single pattern).
        - An existing `re.Pattern` object (returned as is).
        - `None` (results in a "match nothing" pattern).
        If an empty list is provided, it also results in a "match nothing"
        pattern.

    Returns
    -------
    re.Pattern
        A compiled regex pattern. For `None` or empty input, this pattern
        is `(?!)`, which matches nothing.

    Raises
    ------
    TypeError
        If `pattern_input` is not one of the allowed types.
    ValueError
        If `pattern_input` is a string or list containing an invalid regex.

    Examples
    --------
    >>> _compile_regex_pattern(r"\\.txt$").pattern
    '\\\\.txt$'
    >>> _compile_regex_pattern(["\\.py$", "\\.pyc$"]).pattern
    '(\\\\.py$)|(\\\\.pyc$)'
    >>> _compile_regex_pattern(None).pattern
    '(?!)'
    """
    if pattern_input is None:
        return re.compile("(?!)")  # Match nothing
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
            return re.compile("(?!)")  # Match nothing if list is empty
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
    Convert bytes to a human-readable string with units (B, KB, MB, GB, TB, PB).

    Parameters
    ----------
    size_bytes : int
        Size in bytes.

    Returns
    -------
    str
        Human-readable size string (e.g., "1.5 MB", "100 B").
        Returns "N/A" if `size_bytes` is negative.

    Examples
    --------
    >>> _format_size_human_readable(100)
    '100 B'
    >>> _format_size_human_readable(1024)
    '1.0 KB'
    >>> _format_size_human_readable(1536)
    '1.5 KB'
    >>> _format_size_human_readable(0)
    '0 B'
    >>> _format_size_human_readable(-1)
    'N/A'
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
    Convert POSIX timestamp to 'YYYY-MM-DD HH:MM:SS' string.

    Parameters
    ----------
    timestamp : float
        POSIX timestamp (seconds since the epoch).

    Returns
    -------
    str
        Formatted date string. Returns "[Invalid Date]" if the timestamp
        causes a `ValueError`.

    Examples
    --------
    >>> import time
    >>> _format_date_iso(time.time()) # doctest: +ELLIPSIS
    '...-...'
    >>> # The exact output for timestamp 0 depends on the system's timezone.
    >>> # For UTC, it's '1970-01-01 00:00:00'. In US timezones, it's '1969-12-31 ...'.
    >>> isinstance(_format_date_iso(0), str)
    True
    """
    try:
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError: # pragma: no cover
        return "[Invalid Date]"

# ───────────── Private Helper Functions: Filesystem & Path Logic ─────────────

def _get_path_details(
    path_obj: Path,
    config: TreeConfig
) -> PathDetails:
    """
    Gather detailed information about a given path.

    This function inspects a `Path` object and collects various attributes
    like its name, type (file/directory), symlink status, size, and
    modification time, considering the script's configuration (e.g.,
    `follow_symlinks`).

    Parameters
    ----------
    path_obj : Path
        The `pathlib.Path` object to inspect.
    config : TreeConfig
        The script's configuration, which influences how symlinks are
        handled and what information is retrieved.

    Returns
    -------
    PathDetails
        A NamedTuple containing resolved details about the path.
        If an `OSError` occurs (e.g., permission denied), `access_error`
        will be populated, and other fields might be `None` or default.
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
            # Path.exists() resolves symlinks. If it doesn't exist after resolution, it's dangling.
            if not path_obj.exists():
                _is_dangling_symlink = True

        # Determine stat object based on symlink following policy
        # Path.stat() follows symlinks, Path.lstat() does not.
        stat_target_path = path_obj
        if is_symlink_itself and not config.follow_symlinks:
            # If not following, stat the link itself.
            stat_obj = stat_target_path.lstat()
        else:
            # If not a symlink, or following symlinks (even if dangling, stat() will try).
            # For a dangling symlink being followed, stat() will raise OSError.
            stat_obj = stat_target_path.stat()

        _size_bytes = stat_obj.st_size
        _mod_time = stat_obj.st_mtime
        _dev_ino = (stat_obj.st_dev, stat_obj.st_ino)

        # Determine is_dir and is_file
        if is_symlink_itself:
            if config.follow_symlinks:
                if not _is_dangling_symlink:
                    # Followed, not dangling: type is target's type (Path.is_dir/file follow symlinks)
                    _is_dir = path_obj.is_dir()
                    _is_file = path_obj.is_file()
                else:
                    # Followed, but dangling: it's effectively not a dir nor a file for traversal
                    _is_dir = False
                    _is_file = False
            else:
                # Not following symlinks: it's never a directory to enter.
                _is_dir = False
                # It's a file-like entry if it points to a file (Path.is_file() checks target)
                # and isn't dangling.
                _is_file = path_obj.is_file() if not _is_dangling_symlink else False
        else:
            # Not a symlink: straightforward type check
            _is_dir = path_obj.is_dir()
            _is_file = path_obj.is_file()

    except OSError as e:
        _access_error = e.strerror
        # If stat failed, types might still be determinable or are unknown (False)
        # Attempt to get type even if stat failed (e.g. for a dangling symlink target check)
        try:
            if is_symlink_itself:
                if config.follow_symlinks:
                    if not _is_dangling_symlink: # already checked path_obj.exists()
                        _is_dir = path_obj.is_dir()
                        _is_file = path_obj.is_file()
                    # else _is_dir, _is_file remain False (dangling)
                else: # Not following
                    _is_dir = False
                    _is_file = path_obj.is_file() if not _is_dangling_symlink else False
            else: # Not a symlink, but stat failed
                 _is_dir = path_obj.is_dir()
                 _is_file = path_obj.is_file()
        except OSError:  # pragma: no cover
            pass  # is_dir/is_file failure; _is_dir, _is_file remain False

        # Ensure dangling state is confirmed if stat on followed link failed
        if is_symlink_itself and config.follow_symlinks and not path_obj.exists():
            _is_dangling_symlink = True
            _size_bytes = None # No size for dangling target
            _mod_time = None   # No mod_time for dangling target


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
    Determine if a path should be excluded based on configuration.

    This function applies filtering rules in a specific order:
    1. Hard Hiding Rules: `hide_symlinks`.
    2. Exclusion Rules: Specific (file/folder) exclude patterns, then general exclude.
    3. Inclusion Rules: Path must match specific include, then general include.

    Parameters
    ----------
    details : PathDetails
        Information about the path to check.
    config : TreeConfig
        Configuration containing compiled filter patterns and hiding options.

    Returns
    -------
    bool
        True if the path should be filtered out (omitted from the tree),
        False otherwise.
    """
    # 1. Hard Hiding Rules
    if config.hide_symlinks and details.is_symlink:
        return True  # Filter out if hiding all symlinks and this is a symlink

    name_to_check = details.name
    is_dir_type_for_filtering = details.is_dir

    # Determine which specific patterns to use
    effective_include_pattern = (
        config.include_folders_pattern
        if is_dir_type_for_filtering else config.include_files_pattern
    )
    effective_exclude_pattern = (
        config.exclude_folders_pattern
        if is_dir_type_for_filtering else config.exclude_files_pattern
    )

    # 2. Check specific exclusion (if distinct from general)
    if effective_exclude_pattern is not config.exclude_all_pattern and \
       effective_exclude_pattern.pattern != config.exclude_all_pattern.pattern:
        if effective_exclude_pattern.search(name_to_check):
            return True

    # 3. Check general exclusion
    if config.exclude_all_pattern.search(name_to_check):
        return True

    # 4. Check specific inclusion (if distinct from general)
    if effective_include_pattern is not config.include_all_pattern and \
       effective_include_pattern.pattern != config.include_all_pattern.pattern:
        if not effective_include_pattern.search(name_to_check):
            return True

    # 5. Check general inclusion
    if not config.include_all_pattern.search(name_to_check):
        return True

    return False  # Not filtered out


def _build_labels_string(
    details: PathDetails,
    stats: SubtreeStats,
    config: TreeConfig,
    is_circular_ref: bool = False
) -> str:
    """
    Construct the label string (e.g., "[size, date, counts]") for a path.

    Labels are appended to the path name in the tree, providing additional
    information based on the `TreeConfig` settings.

    Parameters
    ----------
    details : PathDetails
        Information about the current path.
    stats : SubtreeStats
        Aggregated stats for this path's subtree (relevant for folders).
    config : TreeConfig
        Script configuration determining which labels are visible.
    is_circular_ref : bool, optional
        True if this path is a detected circular reference target and
        should be marked (and `config.hide_circular_refs` is False).
        Default is False.

    Returns
    -------
    str
        The formatted label string (e.g., " [1.2 MB, 3 files]"),
        or an empty string if no labels are applicable.
    """
    labels: List[str] = []

    if config.mark_symlinks and details.is_symlink and not config.hide_symlinks:
        target_str = details.symlink_target if details.symlink_target is not None else "unknown"
        link_label = f"-> {target_str}"
        if details.is_dangling_symlink:
            link_label += " [DANGLING]"
        labels.append(link_label)

    if config.mark_circular and is_circular_ref: # No need to check hide_circular_refs here, already handled
        labels.append("[CIRCULAR]")
    elif config.mark_errors and details.access_error: # elif ensures error not shown if circular takes precedence
        labels.append(f"[ERROR: {details.access_error}]")

    is_effectively_file_for_labels = details.is_file or \
        (details.is_symlink and not details.is_dir and not details.is_dangling_symlink)

    if is_effectively_file_for_labels:
        if config.show_sizes_files and details.size_bytes is not None:
            labels.append(_format_size_human_readable(details.size_bytes))
        if config.show_dates_files and details.mod_time is not None:
            labels.append(_format_date_iso(details.mod_time))
    elif details.is_dir:
        if config.show_sizes_folders and details.size_bytes is not None: # Folder size is its own stat for total.
            labels.append(_format_size_human_readable(stats.recursive_size_bytes))
        if config.show_dates_folders and details.mod_time is not None:
             labels.append(_format_date_iso(details.mod_time)) # Mod time of the dir itself
        if config.show_folder_file_count:
            labels.append(f"{stats.immediate_files_count} files")
        if config.show_folder_subfolder_count:
            labels.append(f"{stats.immediate_folders_count} dirs")
        if config.show_folder_total_file_count:
            labels.append(f"{stats.recursive_files_count} total files")

    return f" [{', '.join(labels)}]" if labels else ""


# ───────────── Private Helper Functions: Core Traversal Logic ─────────────

def _generate_tree_recursive(
    current_path_details: PathDetails,
    current_prefix: str,
    config: TreeConfig,
    visited_dev_inos: Set[DeviceInode]
) -> Tuple[List[str], SubtreeStats]:
    """
    Recursively generate tree lines and stats for current_path and children.

    This is the core engine for traversing the directory structure. It
    handles the generation of graphical prefixes, collects statistics,
    manages circular reference detection, and recursively calls itself
    for subdirectories.

    Parameters
    ----------
    current_path_details : PathDetails
        Details of the current path being processed.
    current_prefix : str
        The graphical prefix string (e.g., "├── ", "│   └── ") for the
        current item's line in the tree. For the root, this is empty.
    config : TreeConfig
        The script's overall configuration.
    visited_dev_inos : Set[DeviceInode]
        A set of (device, inode) tuples tracking visited directories in the
        current traversal path to detect circular references. A copy is
        passed down to separate traversal branches.

    Returns
    -------
    Tuple[List[str], SubtreeStats]
        - A list of strings, where each string is a line in the tree
          for the current path and its descendants.
        - Aggregated `SubtreeStats` for the subtree rooted at `current_path`.
    """
    lines: List[str] = []
    current_recursive_size = 0
    current_recursive_files = 0

    is_file_like_for_stats = current_path_details.is_file or \
        (current_path_details.is_symlink and
         not current_path_details.is_dir and # Symlink to something not a dir
         not current_path_details.is_dangling_symlink and # and not dangling
         (config.follow_symlinks or current_path_details.size_bytes is not None)) # and followed, or has link size

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
        elif current_path_details.dev_ino: # Not circular yet, add if valid dev_ino
            visited_dev_inos.add(current_path_details.dev_ino)

        if not (is_circular_target and config.hide_circular_refs): # Proceed if not hidden
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
                # This makes the error line look like a child of `current_path_details`
                # The indent for children of the current item, assuming current is last/only.
                indent_for_error_line_children = config.prefixes.parent_last
                connector_for_error_line = config.prefixes.last
                error_line_prefix = parent_line_prefix_segment + indent_for_error_line_children + connector_for_error_line
                children_lines.append(error_line_prefix + f"[ERROR listing contents: {error_listing_children}]")
            else:
                # Collect details in single pass (avoids duplicate stat calls)
                all_child_details = [
                    _get_path_details(child_path_obj, config)
                    for child_path_obj in raw_children_paths
                ]
                # Sort using already-cached is_dir values
                all_child_details.sort(
                    key=lambda d: (not d.is_dir, d.name.lower())
                )
                # Filter after sorting
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

                    if not is_circular_target: # Don't recurse from an already identified circular target node
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


# --- Public API Functions ---

def generate_dir_tree(
    root_dir: Union[str, Path] = ".",
    include: Optional[PatternInputType] = ".*", # Default ".*"
    include_files: Optional[PatternInputType] = None,
    include_folders: Optional[PatternInputType] = None,
    exclude: Optional[PatternInputType] = "(?!)", # Default "(?!)"
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
    Build a directory tree as a list of strings.

    This is the core logic function that traverses directories, applies
    filters, integrates labels, and formats the output according to the
    provided options.

    Parameters
    ----------
    root_dir : Union[str, Path], optional
        Root path for traversal. Default is current directory ".".
        Example: ".", "/mnt/data", Path("project_root")
    include : Optional[PatternInputType], optional
        Regex or list of patterns to include all nodes (files/folders).
        Default: ".*" (include everything).
        Example: r"\\.txt$" to include only text files globally.
    include_files : Optional[PatternInputType], optional
        File-specific include patterns. If None, the `include` pattern is
        effectively used for files. Default: None.
        Example: r"^report_.*\\.pdf$"
    include_folders : Optional[PatternInputType], optional
        Folder-specific include patterns. If None, the `include` pattern
        is effectively used for folders. Default: None.
        Example: ["src", "docs"]
    exclude : Optional[PatternInputType], optional
        Regex or list of patterns to exclude all nodes. Takes precedence
        over include patterns. Default: "(?!)" (matches nothing, so exclude nothing).
        Example: r"__pycache__"
    exclude_files : Optional[PatternInputType], optional
        File-specific exclude patterns. If None, the `exclude` pattern
        is effectively used for files. Default: None.
        Example: r"\\.tmp$"
    exclude_folders : Optional[PatternInputType], optional
        Folder-specific exclude patterns. If None, the `exclude` pattern
        is effectively used for folders. Default: None.
        Example: [r"\\.git", r"\\.svn"]
    show_sizes : bool, optional
        General flag to display sizes. For files, this is the primary control
        unless `show_file_sizes` provides a specific override. For folders,
        this acts as a fallback if `show_folder_total_size` is not specified.
        Default: True.
    show_dates : bool, optional
        General flag to display modification dates. Works similarly to
        `show_sizes` for files (overridden by `show_file_dates`) and folders.
        Default: False.
    show_file_sizes : Optional[bool], optional
        Override `show_sizes` specifically for files. If None, `show_sizes`
        is used for files. Default: None.
    show_file_dates : Optional[bool], optional
        Override `show_dates` specifically for files. If None, `show_dates`
        is used for files. Default: None.
    show_folder_file_count : bool, optional
        Show count of top-level files per folder. Default: True.
    show_folder_total_file_count : bool, optional
        Show recursive (total) file count per folder. Default: False.
    show_folder_subfolder_count : bool, optional
        Show count of top-level subfolders. Default: True.
    show_folder_total_size : Optional[bool], optional
        Display total recursive size for folders.
        If True or False, this explicitly sets folder size visibility.
        If None (default), folder size visibility is determined by the
        general `show_sizes` flag. Default: None.
    follow_symlinks : bool, optional
        Whether to recurse into symlinked directories. If False, symlinks
        to directories are listed as links but not traversed. Default: True.
    mark_symlinks : bool, optional
        Whether to mark symlink nodes and show their target path
        (e.g., "link_name -> /path/to/target"). Default: True.
        Only applies if `hide_symlinks` is False.
    mark_circular : bool, optional
        Whether to label circular references (e.g., "[CIRCULAR]").
        Traversal stops at circular references. Default: True.
        Only applies if `hide_circular_refs` is False.
    mark_errors : bool, optional
        Whether to label error points (e.g., "[ERROR: Permission denied]").
        Default: True.
    hide_symlinks : bool, optional
        If True, all symbolic links are completely omitted from the tree.
        This takes precedence over include/exclude patterns and marking.
        Default: False.
    hide_circular_refs : bool, optional
        If True, directory entries that are targets of circular references
        are omitted from the tree instead of being marked "[CIRCULAR]".
        Default: False.
    use_ascii : bool, optional
        If True, use ASCII-safe characters (+, `, |) for tree drawing instead
        of UTF-8 box-drawing characters (├, └, │). Useful for legacy terminals
        or systems with limited Unicode support. Default: False (use UTF-8).

    Returns
    -------
    List[str]
        A list of strings, where each string is a line of the tree.
        If the root directory cannot be resolved, returns a list with a
        single error message string.

    Examples
    --------
    >>> # To generate a tree (output depends on filesystem):
    >>> # tree_lines = ascii_dir_tree(".")
    >>> # for line in tree_lines: print(line)

    >>> # Example: Show only .py files, exclude .venv, show dates for files
    >>> # ascii_dir_tree(root_dir="my_project",
    ... #                include_files=r"\\.py$",
    ... #                exclude_folders=r"\\.venv",
    ... #                show_file_dates=True,
    ... #                show_sizes=False) # Turn off general sizes if only file dates are wanted

    >>> # Example: Hide all symlinks and .git folders, show folder total sizes
    >>> # ascii_dir_tree(root_dir="another_project",
    ... #                hide_symlinks=True,
    ... #                exclude_folders=r"\\.git",
    ... #                show_folder_total_size=True)
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
    effective_show_folder_dates = show_dates # Folder dates use general flag

    # Compile base general patterns
    # Ensure a valid default if None is passed for general include/exclude
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
        # Append "/" if it's a directory and not already ending with it
        # resolved_root_dir.is_dir() checks the actual path type
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
    Generate a directory tree and write it to a file.

    This is a user-facing wrapper function. It calls the core `generate_dir_tree`
    function to generate the tree lines and then saves the output to the
    specified file. All `*args` and `**kwargs` are passed directly to
    `generate_dir_tree`, allowing full configuration of the tree generation.

    Parameters
    ----------
    outfile : Union[str, Path], optional
        The output file path (e.g., "directory_tree.txt") where the
        directory tree will be saved. Default is "directory_tree.txt".
    *args
        Positional arguments forwarded to `generate_dir_tree`.
    **kwargs
        Keyword arguments forwarded to `generate_dir_tree`. This allows access
        to all options of `generate_dir_tree`, such as `root_dir`, `include`,
        `exclude`, `show_sizes`, `hide_symlinks`, `use_ascii`, etc.

    Returns
    -------
    None
        This function writes to a file and does not return a value directly.
        Prints an error message to stderr if writing to the file fails.

    Examples
    --------
    >>> # Generate a tree of the current directory and save to "mytree.txt"
    >>> # write_dir_tree("mytree.txt")  # This would create the file

    >>> # Generate a tree of "/var/log" (if accessible), showing dates,
    >>> # and save to "logs_tree.txt"
    >>> # write_dir_tree("logs_tree.txt", root_dir="/var/log", show_dates=True)

    >>> # Generate a tree hiding .git folders and all symlinks
    >>> # write_dir_tree(root_dir="my_project",
    ... #                exclude_folders=r"\\.git",
    ... #                hide_symlinks=True)

    >>> # Generate an ASCII-only tree for legacy terminals
    >>> # write_dir_tree("tree.txt", use_ascii=True)
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
    Main entry point: write the default directory tree.

    Invokes `write_dir_tree` (the wrapper function) with its default
    parameters. This will generate a tree of the current working
    directory (".") with default display options and save it to
    "directory_tree.txt".
    """
    _configure_console_encoding()
    print("Generating default directory tree for '.' to 'directory_tree.txt'...")
    write_dir_tree(outfile="directory_tree.txt")
    print("Default tree generation complete. Check 'directory_tree.txt'.")


if __name__ == "__main__":
    main()
