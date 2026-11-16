#!/usr/bin/env python3
"""PreToolUse hook (Edit|Write): protect files an agent must not change on its own.

- Denies: .env files, lock files, anything inside .git/, the generated code map.
- Asks the user: edits to accepted ADRs, the golden eval set, and the harness itself
  (.claude/settings.json, hooks).
"""

import json
import re
import sys
from pathlib import Path

LOCK_FILES = {"uv.lock", "pnpm-lock.yaml", "package-lock.json", "yarn.lock"}
ADR_PATTERN = re.compile(r"docs/decisions/\d{4}-.+\.md$")
ACCEPTED_PATTERN = re.compile(r"^\s*-?\s*\**status\**\s*:\s*\**accepted", re.IGNORECASE | re.MULTILINE)


def deny(reason: str) -> int:
    print(f"Blocked by protect_files: {reason}", file=sys.stderr)
    return 2


def ask(reason: str) -> int:
    decision = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(decision))
    return 0


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    raw_path = (event.get("tool_input") or {}).get("file_path", "")
    if not raw_path:
        return 0

    path = Path(raw_path)
    posix = path.as_posix()
    name = path.name

    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        return deny("Never edit .env files. Add the key to .env.example and tell the user.")

    if name in LOCK_FILES:
        return deny("Lock files change only through `uv` or `pnpm` commands.")

    if "/.git/" in posix:
        return deny("Do not write inside .git/.")

    if ADR_PATTERN.search(posix) and path.exists():
        if ACCEPTED_PATTERN.search(path.read_text(encoding="utf-8", errors="ignore")):
            return ask(
                "This ADR is accepted. The only valid edit is marking it superseded; "
                "a change of mind is a new ADR (/decide)."
            )

    if posix.endswith("docs/CODEMAP.md"):
        return deny("docs/CODEMAP.md is generated. Run `python3 scripts/codemap.py` instead.")

    if "/evals/golden/" in posix and path.exists():
        return ask("This changes the golden eval set. Approve only if the expected answer was wrong.")

    if posix.endswith(".claude/settings.json") or "/.claude/hooks/" in posix:
        return ask("This changes the agent's own guardrails. Approve only if you asked for it.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
