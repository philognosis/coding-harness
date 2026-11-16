---
paths:
  - "**/tests/**"
  - "**/test_*.py"
  - "**/*.test.{ts,tsx}"
---

# Testing standards

- A test name states the behaviour: `test_expired_token_is_rejected`, not `test_auth_2`.
- Arrange, act, assert, in that order, separated by blank lines. One behaviour per test.
- Test through public interfaces (HTTP route, service function, rendered component).
  Do not assert on private helpers or call order unless that is the contract.
- A bug fix starts with a test that fails for the reported reason.
- Mock at the boundary only: network, clock, randomness, LLM calls. Never mock the
  unit under test.
- LLM and agent behaviour is tested with recorded fixtures or evals in `evals/`,
  never with live model calls in the unit suite.
- Never delete, skip or loosen a failing test to get green. If the test is wrong,
  say why and change it in its own commit.
- FastAPI: use `httpx.AsyncClient` with the app's ASGI transport and dependency
  overrides, not a running server.
