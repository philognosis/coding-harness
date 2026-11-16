---
name: model
description: Design the types, states and module boundaries for a change before any behaviour is written, so mistakes cannot be expressed. Use after /frame for any feature with a lifecycle, a workflow, more than one actor, or a new module.
argument-hint: "[spec file or feature name]"
---

# Model: spec to structure

Spec: $ARGUMENTS

Write no behaviour in this skill. The output is types, a transition table and
boundary contracts that compile, plus the diagram generated from them.

1. **Read the map, not the prose.** Run `python3 scripts/codemap.py`, then read
   `docs/CODEMAP.md` for the modules the spec touches. Reuse existing types and
   machines before inventing new ones.
2. **List the nouns and their states.** For each thing in the spec with a
   lifecycle, name every state a user or caller can observe, and every move
   between them. Include failure, cancellation and timeout; they are states.
3. **Decide whether it needs a machine.** Three or more states with ordered
   moves: yes. Plain input-to-output: no, a typed function is enough. Say which
   and why in one line.
4. **Write the structure:**
   - an `Enum` (or literal union) per set of states,
   - a `TRANSITIONS` table and a single `transition()` function, following
     `reference/state_machine.py`,
   - one model per state where the data differs (discriminated union),
   - typed input and output models for every new tool, route or MCP tool.
5. **Write the structure's tests** from `reference/test_state_machine.py`: every
   state has a row, every state is reachable, a terminal state is reachable
   from everywhere, and a property-based walk of random moves.
6. **Draw the boundary.** Name which module may import which. Add or extend
   the import contract (`import-linter` / ESLint `no-restricted-imports`) so the
   direction is enforced.
7. **Generate the picture.** Run `python3 scripts/codemap.py` again and show the
   state diagram from `docs/CODEMAP.md`.
8. **Stop.** Ask the user one question: "Is this the behaviour you meant?"
   A wrong arrow here costs a minute; after `/build` it costs a rewrite.
   The next step is `/blueprint`.
