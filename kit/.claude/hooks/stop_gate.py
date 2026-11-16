#!/usr/bin/env python3
"""Stop hook: the agent may not finish while the quick checks fail.

If code changed and `scripts/check.sh --quick` fails, the agent is sent back
to work once with the failure output. `stop_hook_active` prevents a loop: on
the second attempt the agent is allowed to stop and must report the failure.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

CODE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".toml", ".json", ".css"}


def changed_code_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        return []
    paths = [line[3:].strip() for line in result.stdout.splitlines() if len(line) > 3]
    return [path for path in paths if Path(path).suffix in CODE_SUFFIXES]


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if event.get("stop_hook_active"):
        return 0

    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")
    check_script = root / "scripts" / "check.sh"
    if not check_script.exists():
        return 0

    try:
        if not changed_code_files(root):
            return 0
        result = subprocess.run(
            ["bash", str(check_script), "--quick"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=150,
        )
    except (subprocess.TimeoutExpired, OSError):
        return 0

    if result.returncode != 0:
        tail = "\n".join((result.stdout + result.stderr).splitlines()[-40:])
        print(
            "Quick checks fail. Fix them, or stop and report exactly what blocks you:\n" + tail,
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
