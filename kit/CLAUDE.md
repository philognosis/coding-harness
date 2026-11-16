@AGENTS.md

## Claude Code

- Use plan mode for `/blueprint`; do not edit files until the plan is approved.
- Delegate wide codebase searches to the `Explore` subagent and external research
  to the `researcher` subagent, so the main context holds only conclusions.
- Reviews run in the `reviewer` subagent: it has not seen the build, so it does
  not inherit its assumptions.
- When a hook blocks you, read its message and change approach. Do not look for
  another route to the same action.
- After two failed attempts at the same fix, stop and report what you tried.
