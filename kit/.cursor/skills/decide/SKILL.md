---
name: decide
description: Compare options with a weighted decision matrix and record the outcome as an ADR. Use before adding a dependency, service or pattern, when choosing between architectures, or whenever two or more viable approaches exist and the choice is costly to reverse.
argument-hint: "[the decision to make]"
---

# Decide: options to a recorded decision

Decision: $ARGUMENTS

1. **Check precedent.** Search `docs/decisions/` for the topic. If an accepted
   ADR covers it, show it and ask whether to follow or supersede it.
2. **State the decision** as a question, with the constraint that forces it now.
3. **List options**: two to four real ones, always including "do nothing / keep
   the current approach". If you only know an option by name, run `/ingest` first.
4. **Set criteria and weights** from `docs/decision-matrix.md`, adjusted to
   `docs/GOALS.md`. Show the weights and let the user change them before scoring.
5. **Score** each option 1-5 per criterion, with a one-line justification and a
   source or file path for every score that is not obvious. Compute weighted totals.
6. **Classify reversibility**: two-way door (cheap to undo) or one-way door
   (data migration, public contract, vendor lock-in). One-way doors need
   explicit user approval, whatever the scores say.
7. **Recommend** one option. If the top two are within 10% of each other, say
   the matrix does not separate them and name the tie-breaker you would use.
8. **Record.** After the user chooses, write `docs/decisions/NNNN-<slug>.md` from
   `0000-template.md` (next free number, status `accepted`, the matrix included)
   and add a line to `docs/decisions/README.md`. If it replaces an earlier ADR,
   set that one's status to `superseded by NNNN` (the only edit allowed on an
   accepted ADR; ask the user to approve the hook prompt).

The user makes the choice. You prepare it.
