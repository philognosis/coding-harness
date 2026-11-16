---
name: blueprint
description: Turn an approved spec into a step-by-step implementation plan with a verification for every step. Use after /frame and before writing code for anything larger than a one-line change.
argument-hint: "[spec file or feature name]"
---

# Blueprint: spec to plan

Spec: $ARGUMENTS

Stay read-only (plan mode) until the user approves. The output is one file:
`docs/plans/<slug>.md`, from `docs/plans/_template.md`.

1. **Read** the spec, `docs/GOALS.md`, relevant ADRs and knowledge notes.
2. **Explore** from `docs/CODEMAP.md` (regenerate it first), then the code paths the change touches. Delegate wide searches to a
   read-only subagent. Note the existing patterns the change must follow, with
   file paths.
3. **Surface decisions.** Any choice with two or more viable options that would
   be costly to reverse (dependency, data model, public interface, agent
   topology) goes through `/decide` first. Do not bury it in a step.
4. **Slice the work** into steps that each:
   - leave the repo working and committable,
   - change one concern in a handful of files,
   - name its files and the command or test that proves it works.
   Order: the structure from `/model` (types, transition table, contracts), then
   tests, then implementation, then wiring. If the feature has a lifecycle and
   `/model` has not run, stop and run it.
5. **Write the plan**: context in five lines, steps as checkboxes, a risk list
   with the mitigation for each, and a "Later" list for anything out of scope.
6. **Check the plan against the spec**: every acceptance criterion maps to at
   least one step's verification. Say which criteria are not covered and why.
7. **Stop.** Show the plan path and the step list. Wait for approval before `/build`.
