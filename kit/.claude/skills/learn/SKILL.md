---
name: learn
description: Turn a correction, repeated mistake or review finding into the strongest permanent form available, so it never needs saying again. Use when the user corrects the agent, says "always" or "never", or the same issue appears twice.
argument-hint: "[the correction or lesson]"
---

# Learn: correction to the strongest form that holds it

Lesson: $ARGUMENTS (if empty, review this session for corrections the user made)

Ask these questions in order and stop at the first yes. Each rung down is
weaker: easier to write, easier for an agent to skip.

| # | Question | Home | Strength |
| --- | --- | --- | --- |
| 1 | Can the code be redesigned so the mistake cannot be written? | A type, an Enum, a state-machine transition, a narrower function signature, a module boundary | Impossible to get wrong |
| 2 | Can a static check catch it? | Ruff / ESLint config, a rule in `lint-rules/` with a teaching `note`, the type checker's strict mode, an import contract | Caught in seconds |
| 3 | Can running something catch it? | A test, a property-based test, an eval case in `evals/`, a pattern in `.claude/hooks/` | Caught before finishing |
| 4 | Is it a procedure or a judgment call? | A line in a skill, or a path-scoped rule in `.claude/rules/` | Advice, loaded when relevant |
| 5 | Is it a reason, a goal or a choice? | ADR via `/decide`, or `docs/GOALS.md` | The why; code cannot hold it |
| 6 | Not sure yet? | One bullet in `docs/LESSONS.md` | Promoted if it recurs |

Then:

1. **Clean up the examples.** Search the repo for existing instances of the
   mistake and fix or delete them in the same change. Agents copy what they
   find; a rule with old violations left in place loses to the examples.
2. **Write the smallest edit** at the chosen rung. For a lint rule, the message
   says what to do instead and the note says why.
3. **Remove what it replaces.** If a prose rule now has a check, delete the
   prose. Instruction files must not grow by default.
4. **Promote on recurrence.** A lesson already in `docs/LESSONS.md`, or a prose
   rule the agent broke anyway, moves up at least one rung.
5. **Regenerate**: `python3 scripts/codemap.py` if structure changed,
   `python3 scripts/sync_agent_config.py` if rules or skills changed.
6. **Show the diff** and say which rung the lesson now lives on, and why not
   the one above it.

`docs/LESSONS.md` bullets use the form: `- <date> - <lesson> (source: <PR, file or session>)`.
