# 0001 - Record architecture decisions as ADRs in the repo

- Status: accepted
- Date: <YYYY-MM-DD>
- Deciders: <you>
- Supersedes: none

## Context

Coding agents start each session without memory of earlier choices. Without a
written record they re-open settled questions, or quietly choose differently.
Chat history is not searchable by the next session or the next tool.

## Decision

We record every costly-to-reverse decision as a numbered markdown file in
`docs/decisions/`, created through `/decide`. Accepted ADRs are immutable; a
change of mind is a new ADR that supersedes the old one. Agents search this
folder before choosing between options.

Reversibility: two-way door - the files are plain markdown.

## Consequences

- Agents and people can answer "why is it like this?" from the repo.
- Each significant choice costs a few minutes of writing.
- A hook blocks edits to accepted ADRs, so history stays trustworthy.

## Revisit when

The folder passes about 100 records and search stops being enough; then add an
index by topic or move summaries into path-scoped rules.
