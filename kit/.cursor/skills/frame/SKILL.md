---
name: frame
description: Turn a rough idea into a written spec before any code is written. Use at the start of a feature, a fix with unclear scope, or any request described in a sentence or two.
argument-hint: "[idea, ticket or problem]"
---

# Frame: idea to spec

Input: $ARGUMENTS

Write no code in this skill. The output is one file: `docs/specs/<slug>.md`.

1. **Ground it.** Read `docs/GOALS.md`. Search `docs/decisions/` and `docs/specs/`
   for related work. If the idea conflicts with a goal, a non-goal or an accepted
   decision, say so before anything else.
2. **Look before asking.** Read the code the idea touches, so you only ask what
   the repo cannot answer.
3. **Ask once.** Put up to five questions in a single message. Ask only those
   whose answer would change the design. For each, give your default so the user
   can reply "defaults".
4. **Write the spec** from `docs/specs/_template.md`. Acceptance criteria must be
   checkable: each names the command, test or observation that proves it.
5. **List unknowns.** Anything you would have to guess goes under "Open
   questions", with a note on whether `/ingest` (research) or `/decide`
   (a choice between options) resolves it.
6. **Stop.** Show the spec path and a five-line summary. Ask for approval or edits.
   The next step is `/ingest` if unknowns remain, otherwise `/blueprint`.
