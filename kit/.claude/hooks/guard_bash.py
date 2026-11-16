#!/usr/bin/env python3
"""PreToolUse hook (Bash): block commands that are destructive or bypass the workflow.

Exit code 2 blocks the command; stderr is shown to the agent as the reason.
Add a (pattern, reason) pair to BLOCKED whenever an agent runs something it
should never run again.
"""

import json
import re
import sys

BLOCKED: list[tuple[str, str]] = [
    (
        r"\brm\s+-[a-zA-Z]*(r[a-zA-Z]*f|f[a-zA-Z]*r)[a-zA-Z]*\s+(/|~|\$HOME|\.|\.\.|\*)(\s|$)",
        "Recursive delete of root, home or the whole repo. Delete specific paths instead.",
    ),
    (
        r"\bgit\s+push\b.*(\s--force(?!-with-lease)|\s-f\b)",
        "Force-push is not allowed. Use --force-with-lease on your own branch, or ask the user.",
    ),
    (
        r"\bgit\s+push\b.*\s(origin\s+)?(main|master)(\s|$)",
        "Never push to main. Push a branch and open a pull request.",
    ),
    (r"--no-verify\b", "Do not skip git hooks. Fix what the hook reports."),
    (
        r"\bgit\s+(reset\s+--hard|clean\s+-[a-zA-Z]*f)",
        "This discards uncommitted work. Ask the user to run it themselves.",
    ),
    (
        r"(^|[;&|]\s*)(cat|less|more|head|tail|bat|source|\.)\s+[^;&|]*\.env(?!\.example)(\.\w+)?(\s|$)",
        "Do not read .env files. Config keys are documented in .env.example.",
    ),
    (
        r"(^|[;&|]\s*)(python3?\s+-m\s+)?pip3?\s+install\b",
        "This project uses uv. Run `uv add <package>` (or `uv add --dev <package>`).",
    ),
    (
        r"(^|[;&|]\s*)(npm\s+(install|i|add)|yarn(\s+add|\s+install|\s*$))\b",
        "This project uses pnpm. Run `pnpm add <package>` or `pnpm install`.",
    ),
    (
        r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z)?sh\b",
        "Do not pipe a download into a shell. Download, show the script, and ask the user.",
    ),
]


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # Never break the session because of a malformed event.

    command = (event.get("tool_input") or {}).get("command", "")
    for pattern, reason in BLOCKED:
        if re.search(pattern, command):
            print(f"Blocked by guard_bash: {reason}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
