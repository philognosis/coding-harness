---
name: build
description: Implement an approved plan one step at a time, verifying and committing each step. Use after /blueprint is approved, or to resume a plan in progress.
argument-hint: "[plan file]"
---

# Build: plan to working code

Plan: $ARGUMENTS (if empty, use the plan in `docs/plans/` with unticked steps)

For each unticked step, in order:

1. **Restate** the step and its verification in one line.
2. **Test first** where the behaviour is testable: write the test, run it, see
   it fail for the right reason.
3. **Implement** the smallest change that satisfies the step, following the
   patterns the plan names. Path-scoped rules apply; hooks will format and lint.
4. **Verify** with the step's command. Then run `bash scripts/check.sh --quick`.
5. **Tick the checkbox** in the plan file and commit: one step, one commit,
   message `type(scope): what changed` with the plan step number in the body.

Rules of the loop:

- **Two strikes.** If a step's verification fails twice after real attempts,
  stop. Report what you tried, what you observed and your best hypothesis. Do
  not try a third variation without input.
- **The plan is the contract.** If a step turns out wrong or incomplete, update
  the plan file first, tell the user what changed and why, then continue. Small
  corrections proceed; changes to scope or approach wait for approval.
- **No drive-by work.** Improvements outside the step go in the plan's "Later" list.
- **Delete what you replace.** Old code, its tests and its flags go in the same
  commit. Nothing deprecated is left for the next agent to copy.
- **State changes go through `transition()`.** Never assign a state field directly.
- **Never fake green.** No skipped tests, loosened assertions, `# type: ignore`
  or `eslint-disable` to pass a check, unless the plan says so with a reason.

When every step is ticked: run `python3 scripts/codemap.py`, then
`bash scripts/check.sh` (full), paste its final lines, then run `/gate`.
