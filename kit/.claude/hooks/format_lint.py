#!/usr/bin/env python3
"""PostToolUse hook (Edit|Write): format the edited file, then lint it.

Formatting is applied silently. Lint errors that cannot be auto-fixed are sent
back to the agent (exit code 2), so it fixes them in the same turn instead of
discovering them at the end.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

PYTHON_SUFFIXES = {".py"}
WEB_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs"}
LINT_VIOLATIONS_EXIT_CODE = 1  # Both ruff and eslint use 1 for "violations found".


def find_up(start: Path, marker: str) -> Path | None:
    """Return the nearest ancestor directory of `start` that contains `marker`."""
    for directory in [start, *start.parents]:
        if (directory / marker).exists():
            return directory
    return None


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=45)


def lint_python(file: Path) -> str | None:
    root = find_up(file.parent, "pyproject.toml")
    if root is None or shutil.which("uv") is None:
        return None
    run(["uv", "run", "--quiet", "ruff", "format", str(file)], root)
    result = run(["uv", "run", "--quiet", "ruff", "check", "--fix", str(file)], root)
    if result.returncode == LINT_VIOLATIONS_EXIT_CODE:
        return result.stdout or result.stderr
    return None


def lint_web(file: Path) -> str | None:
    root = find_up(file.parent, "package.json")
    if root is None:
        return None
    eslint = root / "node_modules" / ".bin" / "eslint"
    if not eslint.exists():
        return None
    result = run([str(eslint), "--fix", str(file)], root)
    if result.returncode == LINT_VIOLATIONS_EXIT_CODE:
        return result.stdout or result.stderr
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    raw_path = (event.get("tool_input") or {}).get("file_path", "")
    file = Path(raw_path)
    if not raw_path or not file.is_file():
        return 0

    try:
        if file.suffix in PYTHON_SUFFIXES:
            problems = lint_python(file)
        elif file.suffix in WEB_SUFFIXES:
            problems = lint_web(file)
        else:
            problems = None
    except (subprocess.TimeoutExpired, OSError):
        return 0  # A slow or missing tool must not block the edit.

    if problems:
        print(f"Lint errors in {file.name}; fix them now:\n{problems[-3000:]}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
