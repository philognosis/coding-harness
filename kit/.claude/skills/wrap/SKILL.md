---
name: wrap
description: Close a work session cleanly by recording progress, decisions, lessons and a handoff note so the next session starts without re-explaining. Use at the end of a session, before /clear, or before handing work to another agent.
---

# Wrap: leave the repo ready for the next session

1. **State of the work.** Tick completed steps in the active plan. Under the
   plan's `Handoff` heading, replace the note with: what was done, what is in
   progress (with file paths), the exact next action, and anything surprising.
2. **Decisions.** List choices made this session that are not in an ADR. For
   each that would be costly to reverse or that a future reader would question,
   propose `/decide`; do not write the ADR without the user's confirmation.
3. **Lessons.** For each correction the user gave this session, run the `/learn`
   procedure. Ask before adding anything to `AGENTS.md`.
4. **Goals.** If the session finished or changed a goal, propose the edit to
   `docs/GOALS.md`.
5. **Repo hygiene.** Show `git status`. Uncommitted work is either committed
   on the branch or listed in the handoff note. Delete scratch files.
6. **Teach back.** Name the one or two techniques, APIs or patterns used this
   session that the user is least likely to have used before. For each: three
   lines on what it is, why it was chosen here, and the file to read to see it.
7. **Report** in six lines: done, not done, next action, new decisions, new
   lessons, open questions for the user.
