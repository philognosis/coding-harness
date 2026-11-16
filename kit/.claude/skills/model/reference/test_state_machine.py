"""Reference tests for a state machine: structure checks plus a property-based walk.

Hypothesis tries many random sequences of moves, so the machine is tested
against paths nobody thought to write down.
"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from state_machine import INITIAL_STATE, TRANSITIONS, IllegalTransition, RunState, is_terminal, transition


def reachable_from(start: RunState) -> set[RunState]:
    seen, frontier = {start}, [start]
    while frontier:
        for target in TRANSITIONS[frontier.pop()]:
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    return seen


def test_every_state_has_a_row_in_the_table() -> None:
    assert set(TRANSITIONS) == set(RunState)


def test_every_state_is_reachable_from_the_initial_state() -> None:
    assert reachable_from(INITIAL_STATE) == set(RunState)


def test_a_terminal_state_is_reachable_from_every_state() -> None:
    for state in RunState:
        assert any(is_terminal(reached) for reached in reachable_from(state))


@given(st.lists(st.sampled_from(list(RunState)), max_size=30))
def test_any_sequence_of_moves_is_either_legal_or_rejected(attempts: list[RunState]) -> None:
    state = INITIAL_STATE

    for target in attempts:
        if target in TRANSITIONS[state]:
            state = transition(state, target)
        else:
            with pytest.raises(IllegalTransition):
                transition(state, target)

    assert state in RunState
