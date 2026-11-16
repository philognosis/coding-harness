# Agentic starter kit v2 - structure over prose

A harness you drop into a repository so Claude Code and Cursor work the same
way every session. v2 moves knowledge out of markdown and into the strongest
form that can hold it: types and state machines first, then static checks,
then things that run, and prose last.

## What changed from v1

| Added or changed | What it does |
| --- | --- |
| `scripts/codemap.py` | Generates `docs/CODEMAP.md` from the source: modules, public functions, routes, exports, and a state diagram for every `TRANSITIONS` table. `--check` fails CI when it is stale |
| `.claude/rules/structure.md` | Standards for types, state machines, boundaries and leaving nothing misleading behind |
| `/model` skill + `reference/` | Design types, states and boundaries before behaviour; a tested state-machine pattern with property-based tests |
| `/learn` skill | Now a ladder: redesign, static check, runtime check, prose, in that order, and clean up old examples |
| `lint-rules/` + `sgconfig.yml` | Project-specific ast-grep rules whose messages teach the fix |
| `/blueprint`, `/build`, `/gate`, `reviewer` | Read the map, build on the model, delete what is replaced, require evidence |
| `protect_files.py` | Also blocks hand edits to `docs/CODEMAP.md` and asks before changing `evals/golden/` |
| `AGENTS.md` | No prose description of the code; a "Structure first" section instead |

## Install

```bash
bash install.sh /path/to/your/repo     # copies files, never overwrites
cd /path/to/your/repo
python3 scripts/sync_agent_config.py   # generates .cursor/ from .claude/
python3 scripts/codemap.py             # generates docs/CODEMAP.md
```

Upgrading from v1: `install.sh` skips files that exist, so copy these over by
hand after reviewing the diff: `AGENTS.md`, `.claude/skills/{learn,blueprint,build,gate}/SKILL.md`,
`.claude/agents/reviewer.md`, `.claude/hooks/protect_files.py`, `scripts/check.sh`.

Requirements: Python 3.10+, git, `uv` / `pnpm` for your stacks. Optional but
recommended: `uv tool install ast-grep-cli` for `lint-rules/`, and
`uv add --dev hypothesis import-linter` in Python projects.

## Daily use

```text
/frame add rate limiting to the agent gateway
/ingest token bucket vs sliding window for async Python
/model docs/specs/rate-limiting.md        <- confirm the state diagram
/blueprint docs/specs/rate-limiting.md
/build
/gate
/wrap
```

## Check it works

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | python3 .claude/hooks/guard_bash.py; echo "exit $?"
# expected: a "Blocked by guard_bash" message and exit 2

python3 scripts/codemap.py && python3 scripts/codemap.py --check
# expected: "Wrote docs/CODEMAP.md", then "up to date"
```
