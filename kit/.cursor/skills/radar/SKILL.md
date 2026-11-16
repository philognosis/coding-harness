---
name: radar
description: Scan for what changed in the project's stack and agent tooling, and update docs/RADAR.md with dated, sourced findings and proposed experiments. Run weekly or on request.
disable-model-invocation: true
argument-hint: "[optional focus area]"
---

# Radar: stay current on purpose

Focus: $ARGUMENTS (default: everything on the watchlist)

This skill changes `docs/RADAR.md` only. It never touches code or dependencies.

1. **Read** `docs/RADAR.md` (watchlist, current rings, last scan date) and the
   pinned versions in `pyproject.toml` / `package.json`.
2. **Scan primary sources** for each watchlist item since the last scan date:
   release notes, changelogs, official blogs, deprecation notices, security
   advisories. For agent tooling, read the Claude Code and Cursor changelogs and
   the docs pages for rules, skills, hooks and subagents.
3. **Filter hard.** Keep an item only if it would change how we build, removes
   a workaround we carry, deprecates something we use, or fixes a security issue.
   Everything else is noise; do not list it.
4. **Classify** each kept item:
   - `adopt` - proven, low risk, do it in the next plan.
   - `trial` - promising; propose a time-boxed experiment on a branch.
   - `assess` - worth an `/ingest` note before deciding.
   - `hold` - we looked and are not doing it; one line of why.
5. **Check the harness.** Compare what the tools now offer with what
   `AGENTS.md`, rules, skills and hooks do. List anything our kit works around
   that is now native, and anything in the kit that the docs now contradict.
6. **Update `docs/RADAR.md`**: new dated entry at the top with source links, ring
   changes, and at most three proposed experiments, each with a hypothesis, a
   time box and a success measure.
7. **Report** in ten lines or fewer: what changed, what you propose, what needs
   a decision (`/decide`).
