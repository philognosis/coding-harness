"""Reference pattern: an explicit state machine for an agent run.

Copy the shape, not the states. Three parts make illegal moves impossible:
an Enum of states, one TRANSITIONS table, and one function that changes state.
`scripts/codemap.py` draws the table as a diagram in docs/CODEMAP.md.
"""

from enum import Enum


class RunState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


INITIAL_STATE = RunState.QUEUED

TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.QUEUED: frozenset({RunState.RUNNING, RunState.CANCELLED}),
    RunState.RUNNING: frozenset(
        {RunState.WAITING_FOR_APPROVAL, RunState.SUCCEEDED, RunState.FAILED, RunState.CANCELLED}
    ),
    RunState.WAITING_FOR_APPROVAL: frozenset({RunState.RUNNING, RunState.CANCELLED}),
    RunState.SUCCEEDED: frozenset(),
    RunState.FAILED: frozenset(),
    RunState.CANCELLED: frozenset(),
}


class IllegalTransition(Exception):
    def __init__(self, current: RunState, target: RunState) -> None:
        allowed = ", ".join(sorted(state.value for state in TRANSITIONS[current])) or "none (terminal)"
        super().__init__(f"Cannot go from {current.value} to {target.value}. Allowed: {allowed}.")


def transition(current: RunState, target: RunState) -> RunState:
    """The only place a run changes state. Raises IllegalTransition otherwise."""
    if target not in TRANSITIONS[current]:
        raise IllegalTransition(current, target)
    return target


def is_terminal(state: RunState) -> bool:
    return not TRANSITIONS[state]
