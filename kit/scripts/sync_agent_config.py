#!/usr/bin/env python3
"""Generate Cursor config from the Claude Code config, so rules are written once.

Source of truth          Generated
.claude/rules/*.md   ->  .cursor/rules/*.mdc   (paths -> globs)
.claude/skills/*     ->  .cursor/skills/*      (copied as-is)
.claude/agents/*.md  ->  .cursor/agents/*.md   (copied as-is)

Run after editing any rule, skill or agent:  python3 scripts/sync_agent_config.py
Run with --check in CI to fail when the generated files are stale.
"""

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT / ".claude"
CURSOR = ROOT / ".cursor"
GENERATED_NOTE = "<!-- Generated from .claude/rules by scripts/sync_agent_config.py. Edit the source. -->"


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """Return (frontmatter lines, body). Frontmatter is the block between leading '---' lines."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :]).lstrip("\n")
    return [], text


def parse_paths(frontmatter: list[str]) -> list[str]:
    """Read the `paths:` list from simple YAML frontmatter without a YAML dependency."""
    paths: list[str] = []
    in_paths = False
    for line in frontmatter:
        if line.startswith("paths:"):
            in_paths = True
            continue
        if in_paths and line.strip().startswith("- "):
            paths.append(line.strip()[2:].strip().strip("\"'"))
        elif line.strip():
            in_paths = False
    return paths


def first_heading(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def render_cursor_rule(source: Path) -> str:
    frontmatter, body = split_frontmatter(source.read_text(encoding="utf-8"))
    globs = parse_paths(frontmatter)
    header = [
        "---",
        f"description: {first_heading(body, source.stem)}",
        f"globs: {','.join(globs)}" if globs else "globs:",
        f"alwaysApply: {'false' if globs else 'true'}",
        "---",
        "",
        GENERATED_NOTE,
        "",
    ]
    return "\n".join(header) + body.rstrip("\n") + "\n"


def sync_rules(check_only: bool) -> list[str]:
    stale: list[str] = []
    target_dir = CURSOR / "rules"
    for source in sorted((CLAUDE / "rules").glob("*.md")):
        target = target_dir / f"{source.stem}.mdc"
        rendered = render_cursor_rule(source)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current != rendered:
            stale.append(str(target.relative_to(ROOT)))
            if not check_only:
                target_dir.mkdir(parents=True, exist_ok=True)
                target.write_text(rendered, encoding="utf-8")
    return stale


def trees_differ(source: Path, target: Path) -> bool:
    if not target.exists():
        return True
    comparison = filecmp.dircmp(source, target)
    if comparison.left_only or comparison.right_only or comparison.diff_files:
        return True
    return any(trees_differ(source / name, target / name) for name in comparison.common_dirs)


def sync_tree(name: str, check_only: bool) -> list[str]:
    source, target = CLAUDE / name, CURSOR / name
    if not source.is_dir() or not trees_differ(source, target):
        return []
    if not check_only:
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    return [str(target.relative_to(ROOT))]


def main() -> int:
    check_only = "--check" in sys.argv
    stale = sync_rules(check_only) + sync_tree("skills", check_only) + sync_tree("agents", check_only)

    if check_only and stale:
        print("Cursor config is stale. Run: python3 scripts/sync_agent_config.py")
        print("\n".join(f"  {path}" for path in stale))
        return 1
    print(f"{'Checked' if check_only else 'Synced'} Cursor config; {len(stale)} path(s) changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
