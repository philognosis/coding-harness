---
name: ingest
description: Research a topic, library, API or technique and save sourced notes to docs/knowledge. Use when a spec has unknowns, before adopting a dependency, or when the user shares a link, paper or doc to learn from.
argument-hint: "[topic, URL or question]"
---

# Ingest: research to reusable knowledge

Topic: $ARGUMENTS

Do the reading in the `researcher` subagent (or a fresh context) so only the
conclusions return to the main conversation.

1. **Check what we know.** Look for `docs/knowledge/<topic>.md` and related ADRs.
   If a note exists and is under 60 days old, update it instead of starting over.
2. **Go to primary sources.** Official docs, changelogs, source code, papers.
   Use blog posts only to find primary sources. Prefer the version pinned in our
   lock files; note when the latest version differs.
3. **Verify by running** when cheap: a ten-line script in a scratch directory
   beats a paragraph of documentation. Delete the scratch afterwards.
4. **Write `docs/knowledge/<topic>.md`** with these sections:
   - `Answer` - three to six lines: what it is and what it means for this project.
   - `Facts` - bullets, each with a source link and the version it applies to.
   - `How we would use it` - a minimal example in our stack and conventions.
   - `Risks and limits` - maturity, licence, lock-in, cost, known issues.
   - `Open questions` - what could not be confirmed.
   - Header line: `Checked: <date>` and the versions examined.
5. **Separate fact from inference.** Anything not confirmed by a source or a run
   is labelled "unverified".
6. **Report** the answer in five lines and name the next step: `/decide` if this
   feeds a choice, `/blueprint` if the way forward is clear.

Never add the dependency or change project code from this skill.
