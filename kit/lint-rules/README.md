# Project lint rules

One YAML file per rule, run by [ast-grep](https://ast-grep.github.io) through
`scripts/check.sh`. This is where a repeated agent mistake goes once a machine
can detect it: the rule blocks the mistake, and its `note` teaches the fix at
the moment the agent makes it.

## Adding a rule

1. Copy `no-env-outside-config.yml` and change `id`, `language`, `rule`.
2. Write `message` as the instruction and `note` as the reason plus the fix.
   The agent reads both, so say what to do instead, not only what is wrong.
3. Run `ast-grep scan` and confirm it fires on a bad example and stays quiet
   on a good one.
4. Fix or delete every existing violation in the same change. A rule with
   old exceptions teaches the agent that exceptions are normal.

Use the language's own linter first. Ruff and ESLint already cover most
general rules; this folder is for rules about *this* project's design.
