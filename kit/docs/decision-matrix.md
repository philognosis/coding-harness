# Decision matrix

The default criteria and weights `/decide` uses. Weights follow the quality
order in `docs/GOALS.md`; change them there first, then here.

## Criteria

| Criterion | Weight | Score 5 means | Score 1 means |
| --- | --- | --- | --- |
| Fit to goals | 5 | Directly serves a current goal | Serves a non-goal |
| Correctness and safety risk | 5 | Well understood, hard to misuse | Easy to get subtly wrong |
| Maintainability | 4 | Readable by a newcomer in an hour | Needs its author |
| Extensibility and reuse | 4 | Other agents and services plug in unchanged | One-off |
| Maturity and support | 3 | Stable releases, active maintenance, good docs | Pre-1.0, single maintainer |
| Reversibility | 3 | Swap out in a day | Data migration or contract break |
| Delivery effort | 2 | Hours | Weeks |
| Operating cost | 2 | Negligible | Dominates the bill |

## How to score

1. Score each option 1-5 per criterion; write one line of evidence per score.
2. Weighted total = sum of (score x weight). Maximum with default weights: 140.
3. A score of 1 on either weight-5 criterion is a veto, whatever the total.
4. Totals within 10% of each other are a tie: decide on reversibility, then on
   which option teaches us more.

## When a matrix is required

| Situation | Matrix + ADR | Just do it |
| --- | --- | --- |
| New dependency, service, datastore or framework | Yes | |
| Public API, schema or event contract change | Yes | |
| New agent, or a change in how agents are orchestrated | Yes | |
| Model or provider change for an agent | Yes | |
| New top-level folder or cross-cutting pattern | Yes | |
| Choice inside one module, undone in under an hour | | Yes |
| Following an existing ADR or pattern | | Yes |

## Blank matrix

| Criterion | Weight | Option A | Option B | Do nothing |
| --- | --- | --- | --- | --- |
| Fit to goals | 5 | | | |
| Correctness and safety risk | 5 | | | |
| Maintainability | 4 | | | |
| Extensibility and reuse | 4 | | | |
| Maturity and support | 3 | | | |
| Reversibility | 3 | | | |
| Delivery effort | 2 | | | |
| Operating cost | 2 | | | |
| **Weighted total** | | | | |
