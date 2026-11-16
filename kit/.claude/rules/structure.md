---
paths:
  - "**/*.py"
  - "**/*.ts"
  - "**/*.tsx"
---

# Structure standards

The code is the main thing the next agent reads and copies. Design it so a
mistake cannot be written, before reaching for a rule that asks nicely.

## Make illegal states unrepresentable

- A value that can only be one of a few things is an `Enum` (Python) or a
  union of string literals (TypeScript). Never a bare `str` checked with `==`.
- Data that differs by state is a discriminated union: one model per state,
  tagged by a literal field. No model with optional fields that are "only set
  when status is X".
- Parse at the boundary into a precise type, then trust the type inside.
  Functions deep in the code do not re-validate.
- Handle every case: `match` with `assert_never` (Python), a `switch` with a
  `never` default (TypeScript). Adding a state must break the build until every
  handler knows about it.

## State machines

Use one when something has three or more states and the order of moves
matters: an agent run, a chat turn, a job, an approval, a candidate pipeline.

- One `Enum` of states, one module-level `TRANSITIONS` table, one `transition()`
  function. Nothing else assigns the state field.
- The table is data, so `scripts/codemap.py` draws it and tests walk it. Pattern
  and tests: `.claude/skills/model/reference/`.
- Side effects hang off transitions, not off scattered `if status ==` checks.
- Do not build one for plain request/response code or a linear pipeline. A
  function that takes input and returns output needs no machine.

## Boundaries

- Dependencies point one way: routes -> services -> clients/repositories.
  Core logic imports no web framework, no agent SDK and no database driver.
- Each direction that must not be imported is enforced by a tool
  (`import-linter` contracts in Python, `no-restricted-imports` in ESLint),
  not by this sentence. If the contract is missing, add it.
- One way to do each thing. Before adding a helper, client or pattern, search
  for the existing one. Two ways to do something is a bug in the codebase.

## Leave nothing misleading behind

- Delete what you replace in the same change: the old function, its tests,
  its feature flag. Deprecated code left in place gets copied.
- No workaround without removing its cause or opening an ADR. A `sleep`, a
  retry-until-it-works or a `# type: ignore` is a pattern the next agent will
  repeat.
- Comments say why, in one line, only when the code cannot. A comment that
  warns "do not do X" becomes a lint rule in `lint-rules/` instead.
- Docstrings on agent tools, MCP tools and API routes are part of the
  interface: the model or the client reads them. Keep those accurate and
  complete.

## Knowledge about the code

- Never write a markdown description of what the code contains. Run
  `python3 scripts/codemap.py`; `docs/CODEMAP.md` is generated from the source.
- Markdown holds what code cannot: goals, decisions and their reasons, specs.
