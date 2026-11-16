---
name: gate
description: Review the current branch against its spec, plan and project standards using a fresh context, then fix what the review finds. Use after /build, before opening a pull request, or when asked to review changes.
argument-hint: "[base branch, default main]"
---

# Gate: independent review before merge

Base: $ARGUMENTS (default `main`)

1. **Collect** the diff against the base branch, the spec and the plan.
   Gather evidence that it runs: test output, eval scores, and for UI changes a
   screenshot of the running app per acceptance criterion (Playwright or the
   browser tool). A claim without evidence counts as not verified.
2. **Review in a fresh context.** Hand the `reviewer` subagent the diff, the
   spec path and the plan path. Do not explain your implementation choices to it;
   it should judge the code as written.
3. **Triage the findings** it returns:
   - `blocker` - wrong behaviour, unmet acceptance criterion, security or data
     risk, broken standard. Fix now.
   - `should` - maintainability or clarity problem. Fix now unless it widens scope.
   - `note` - taste or future work. Add to the plan's "Later" list.
4. **Fix** blockers and shoulds, each with its own verification. Re-run
   `bash scripts/check.sh`.
5. **Second pass** only on the files you changed in step 4.
6. **Report**: acceptance criteria with the evidence for each, findings fixed,
   findings deferred, and anything not verified. Then run `/wrap`.

If the review contradicts an accepted ADR, the ADR wins; record the disagreement
in `docs/LESSONS.md` and raise it with the user.
