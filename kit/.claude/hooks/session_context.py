#!/usr/bin/env python3
"""SessionStart hook: put the project's current state in front of the agent.

Whatever this prints is added to the session's context, so keep it short:
goals, the active plan, recent decisions and recent lessons.
"""

import os
import re
import sys
from pathlib import Path

MAX_GOAL_LINES = 30
MAX_DECISIONS = 6
MAX_LESSONS = 8


def read_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def first_heading(path: Path) -> str:
    for line in read_lines(path):
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def active_plans(plans_dir: Path) -> list[str]:
    """Plans with unticked checkboxes, as 'file (done/total)'."""
    summaries = []
    for plan in sorted(plans_dir.glob("*.md")):
        if plan.name.startswith("_"):
            continue
        text = "\n".join(read_lines(plan))
        done = len(re.findall(r"^\s*- \[x\]", text, re.MULTILINE | re.IGNORECASE))
        todo = len(re.findall(r"^\s*- \[ \]", text, re.MULTILINE))
        if todo:
            summaries.append(f"- docs/plans/{plan.name} ({done}/{done + todo} steps done)")
    return summaries


def main() -> int:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
    docs = root / "docs"
    sections: list[str] = []

    goals = [line for line in read_lines(docs / "GOALS.md") if line.strip()][:MAX_GOAL_LINES]
    if goals:
        sections.append("## Goals (docs/GOALS.md)\n" + "\n".join(goals))

    plans = active_plans(docs / "plans") if (docs / "plans").is_dir() else []
    if plans:
        sections.append("## Plans in progress\n" + "\n".join(plans))

    decisions = sorted(
        (path for path in (docs / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md") if not path.name.startswith("0000")),
        reverse=True,
    )
    if decisions:
        titles = [f"- {path.name}: {first_heading(path)}" for path in decisions[:MAX_DECISIONS]]
        sections.append("## Latest decisions (docs/decisions/)\n" + "\n".join(titles))

    lessons = [line for line in read_lines(docs / "LESSONS.md") if line.startswith("- ")]
    if lessons:
        sections.append("## Recent lessons (docs/LESSONS.md)\n" + "\n".join(lessons[-MAX_LESSONS:]))

    if sections:
        print("# Project state\n\n" + "\n\n".join(sections))
    return 0


if __name__ == "__main__":
    sys.exit(main())
