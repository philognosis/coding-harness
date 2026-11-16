# AGENTS.md

<!-- Canonical instructions for every coding agent (Claude Code, Cursor, Codex, ...).
     Keep under 100 lines. This file holds intent and procedure only.
     What the code contains is in docs/CODEMAP.md, generated from the source. -->

## Project

- **What it is:** <one sentence: what this system does and for whom>
- **Stack:** <e.g. Python 3.13 + FastAPI (uv) in `api/`, Next.js + Tailwind (pnpm) in `<name>-ui/`>
- **Code map:** `docs/CODEMAP.md` - modules, public functions, routes and state
  diagrams. Generated; never edit it, never describe the code in prose instead.
- **Current goals:** see `docs/GOALS.md`. Read it before proposing scope.

## Commands

| Task | Command |
| --- | --- |
| Verify everything (lint, types, tests, build, map) | `bash scripts/check.sh` |
| Fast verify (lint + types only) | `bash scripts/check.sh --quick` |
| Regenerate the code map | `python3 scripts/codemap.py` |
| Python deps | `uv add <pkg>` / `uv sync` (never `pip install`) |
| Run API | `uv run fastapi dev` |
| UI deps / dev / build | `pnpm install` / `pnpm dev` / `pnpm build` (never `npm` or `yarn`) |

## How we work

Every non-trivial change follows the same loop. Each step is a skill in
`.claude/skills/<name>/SKILL.md`; run it as `/name`, or read the file and follow it.

1. `/frame` - turn the idea into a spec in `docs/specs/`. No code yet.
2. `/ingest` - research unknowns; notes land in `docs/knowledge/` with sources.
3. `/model` - types, states and boundaries first; confirm the state diagram.
4. `/blueprint` - write a step-by-step plan in `docs/plans/`. Wait for approval.
5. `/build` - implement one step at a time; each step has its own check.
6. `/gate` - fresh-context review against the spec, with evidence it runs.
7. `/wrap` - record decisions, lessons and the handoff note.

Trivial changes (typo, rename, one-line fix) skip to step 5. If you cannot
describe the diff in one sentence, it is not trivial.

Side skills: `/decide` (decision matrix + ADR), `/learn` (move a correction to
the strongest form that holds it), `/radar` (scan what changed in our stack).

## Structure first

When something goes wrong, fix it at the highest rung that can hold the fix:

1. Redesign so the mistake cannot be written (type, state machine, boundary).
2. A static check (linter, type checker, `lint-rules/`, import contract).
3. Something that runs (test, property test, eval, hook).
4. Prose (a rule or a skill). Last, because it can be skipped.

The repo is what you learn from, so leave it worth copying: delete what you
replace, and never leave a workaround without removing its cause.

## Boundaries

- Never read, print or edit `.env` files. Config keys are documented in `.env.example`.
- Never push to `main`, force-push, or commit with `--no-verify`.
- Never edit lock files by hand, or an accepted ADR (a change of mind is a new ADR).
- Never add a dependency, a new service, or a new top-level folder without `/decide`.
- Never weaken a test, an eval, a lint rule or a type check to make a change pass.
- Stay inside the plan. Out-of-scope improvements go in the plan's "Later" list.

## Memory

| Question | Where to look |
| --- | --- |
| What is in the code, and how do its states move? | `docs/CODEMAP.md` (generated) |
| What are we trying to achieve, and what is out of scope? | `docs/GOALS.md` |
| Why is it built this way? | `docs/decisions/` (ADRs, index in its README) |
| What have we learned the hard way? | `docs/LESSONS.md` |
| What is new in our stack, and what are we trialling? | `docs/RADAR.md` |
| What do we know about topic X? | `docs/knowledge/` |

Before choosing between options, search `docs/decisions/` first. If a decision
exists, follow it or propose a superseding ADR; do not silently diverge.

## Definition of done

- `bash scripts/check.sh` passes, and you say so with the output's last lines.
- Each acceptance criterion has evidence: a test, an eval score, command
  output, or a screenshot of the running app.
- Plan checkboxes are ticked; decisions and lessons are recorded.
- You report what you did not do or could not verify.
