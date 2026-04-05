#!/usr/bin/env python3
"""
Analyze explicit Python targets for documentation rewrite eligibility.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

ENCODING_PATTERN = re.compile(r"coding[:=]\s*[-\w.]+", re.IGNORECASE)
DIRECTIVE_PATTERNS = (
    re.compile(r"^noqa(?::.*)?$", re.IGNORECASE),
    re.compile(r"^type:\s*ignore(?:\[.*\])?.*$", re.IGNORECASE),
    re.compile(r"^pragma:\s*no\s*cover\b.*$", re.IGNORECASE),
    re.compile(r"^pyright:\s*.*$", re.IGNORECASE),
    re.compile(r"^pylint:\s*.*$", re.IGNORECASE),
    re.compile(r"^ruff:\s*.*$", re.IGNORECASE),
    re.compile(r"^fmt:\s*(?:on|off|skip)\b.*$", re.IGNORECASE),
    re.compile(r"^isort:\s*.*$", re.IGNORECASE),
)


@dataclass(slots=True)
class AnalysisResult:
    path: str
    eligible: bool
    parse_ok: bool
    hard_exclusions: list[str] = field(default_factory=list)
    module_docstring_present: bool = False
    public_class_count: int = 0
    public_function_count: int = 0
    docstring_count: int = 0
    comment_count: int = 0
    directive_comment_count: int = 0
    preserve_sensitive: bool = False
    preserve_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "eligible": self.eligible,
            "parse_ok": self.parse_ok,
            "hard_exclusions": self.hard_exclusions,
            "module_docstring_present": self.module_docstring_present,
            "public_class_count": self.public_class_count,
            "public_function_count": self.public_function_count,
            "docstring_count": self.docstring_count,
            "comment_count": self.comment_count,
            "directive_comment_count": self.directive_comment_count,
            "preserve_sensitive": self.preserve_sensitive,
            "preserve_reasons": self.preserve_reasons,
        }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def contains_sequence(parts: tuple[str, ...], sequence: tuple[str, ...]) -> bool:
    lowered_parts = tuple(part.lower() for part in parts)
    lowered_sequence = tuple(part.lower() for part in sequence)
    width = len(lowered_sequence)
    for index in range(0, len(lowered_parts) - width + 1):
        if lowered_parts[index : index + width] == lowered_sequence:
            return True
    return False


def is_directive_comment(comment_text: str, line_number: int) -> bool:
    stripped = comment_text.strip()
    if line_number == 1 and stripped.startswith("#!"):
        return True
    if line_number <= 2 and ENCODING_PATTERN.search(stripped):
        return True
    if not stripped.startswith("#"):
        return False

    body = stripped[1:].strip()
    return any(pattern.match(body) for pattern in DIRECTIVE_PATTERNS)


def collect_hard_exclusions(path: Path) -> list[str]:
    exclusions: list[str] = []
    parts = path.parts
    lowered_parts = {part.lower() for part in parts}

    if path.suffix.lower() != ".py":
        exclusions.append("non_python_target")
    if path.exists() and path.is_dir():
        exclusions.append("directory_targets_not_supported")
    if ".archive" in lowered_parts:
        exclusions.append("archive_target")
    if ".venv" in lowered_parts:
        exclusions.append("virtualenv_target")
    if "__pycache__" in lowered_parts:
        exclusions.append("pycache_target")
    if contains_sequence(parts, (".agent", ".temp")):
        exclusions.append("managed_temp_target")
    if contains_sequence(parts, ("resources", "schema")):
        exclusions.append("schema_mirror_target")
    if any(part.lower().endswith(".skill") for part in parts):
        exclusions.append("packaged_skill_surface")
    if not path.exists():
        exclusions.append("missing_target")

    return exclusions


def scan_comments(source: str) -> tuple[int, int]:
    comment_count = 0
    directive_count = 0
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type != tokenize.COMMENT:
                continue
            comment_count += 1
            if is_directive_comment(token.string, token.start[0]):
                directive_count += 1
    except tokenize.TokenError:
        pass
    return comment_count, directive_count


def count_docstrings(tree: ast.Module) -> tuple[bool, int]:
    module_docstring_present = bool(ast.get_docstring(tree, clean=False))
    count = 1 if module_docstring_present else 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(
            node, clean=False
        ):
            count += 1

    return module_docstring_present, count


def analyze_target(raw_target: str | Path) -> AnalysisResult:
    path = Path(raw_target).resolve()
    hard_exclusions = collect_hard_exclusions(path)
    result = AnalysisResult(
        path=path.as_posix(),
        eligible=not hard_exclusions,
        parse_ok=False,
        hard_exclusions=hard_exclusions,
    )

    if not result.eligible:
        return result

    try:
        source = read_text(path)
    except OSError:
        result.hard_exclusions.append("unreadable_target")
        result.eligible = False
        return result

    result.comment_count, result.directive_comment_count = scan_comments(source)
    non_directive_comment_count = result.comment_count - result.directive_comment_count

    try:
        tree = ast.parse(source)
    except SyntaxError:
        result.parse_ok = False
    else:
        result.parse_ok = True
        result.module_docstring_present, result.docstring_count = count_docstrings(tree)
        result.public_class_count = sum(
            1 for node in tree.body if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        )
        result.public_function_count = sum(
            1
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")
        )

    if result.docstring_count:
        result.preserve_reasons.append(f"{result.docstring_count} existing docstring(s)")
    if non_directive_comment_count:
        result.preserve_reasons.append(f"{non_directive_comment_count} non-directive comment(s)")

    result.preserve_sensitive = bool(result.preserve_reasons)
    return result


def analyze_targets(targets: list[str | Path]) -> list[AnalysisResult]:
    return [analyze_target(target) for target in targets]


def render_text(results: list[AnalysisResult]) -> str:
    rendered_blocks: list[str] = []
    for result in results:
        reasons = result.preserve_reasons or ["none"]
        rendered_blocks.extend(
            [
                f"path: {result.path}",
                f"eligible: {str(result.eligible).lower()}",
                f"parse_ok: {str(result.parse_ok).lower()}",
                f"hard_exclusions: {', '.join(result.hard_exclusions) if result.hard_exclusions else 'none'}",
                f"module_docstring_present: {str(result.module_docstring_present).lower()}",
                f"public_class_count: {result.public_class_count}",
                f"public_function_count: {result.public_function_count}",
                f"docstring_count: {result.docstring_count}",
                f"comment_count: {result.comment_count}",
                f"directive_comment_count: {result.directive_comment_count}",
                f"preserve_sensitive: {str(result.preserve_sensitive).lower()}",
                "preserve_reasons:",
                *[f"  - {reason}" for reason in reasons],
                "",
            ]
        )
    return "\n".join(rendered_blocks).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze explicit Python targets for documentation rewrite eligibility.")
    parser.add_argument("targets", nargs="+", help="Explicit Python file target(s).")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = analyze_targets(args.targets)
    if args.json:
        print(json.dumps([result.to_dict() for result in results], indent=2, ensure_ascii=False))
    else:
        print(render_text(results), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
