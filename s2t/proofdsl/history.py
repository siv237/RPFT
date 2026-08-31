"""Typed finite Page--Wootters histories built from Kraus dilations."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .channel import KrausChannel
from .structures import exact_matrix


@dataclass(frozen=True, slots=True)
class KrausHistory:
    """A finite clock history with one fresh Kraus environment per tick.

    The object stores no external time coordinate.  Its integer ``steps`` is
    the dimension of the finite clock record to be conditioned upon.
    """

    name: str
    channel: KrausChannel
    initial_state: sp.ImmutableMatrix
    steps: int

    def __init__(
        self,
        name: str,
        channel: KrausChannel,
        initial_state: sp.MatrixBase,
        steps: int,
    ) -> None:
        state = exact_matrix(initial_state)
        dimension = channel.space.dimension
        if not name:
            raise ValueError("a history needs a name")
        if steps < 1:
            raise ValueError("a history needs at least one clock transition")
        if state.shape != (dimension, dimension):
            raise ValueError("the initial state lives on the wrong system space")
        if state != state.H:
            raise ValueError("the initial state must be Hermitian")
        if sp.simplify(sp.trace(state) - 1) != 0:
            raise ValueError("the initial state must have unit trace")
        if state.is_positive_semidefinite is not True:
            raise ValueError("the initial state must be exactly positive semidefinite")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "channel", channel)
        object.__setattr__(self, "initial_state", state)
        object.__setattr__(self, "steps", steps)

    @property
    def clock_dimension(self) -> int:
        return self.steps + 1

    @property
    def environment_dimension(self) -> int:
        return len(self.channel.kraus)

    def branch_count(self, step: int) -> int:
        if not 0 <= step <= self.steps:
            raise IndexError(step)
        return self.environment_dimension**step

    def iterated_state(self, step: int) -> sp.ImmutableMatrix:
        if not 0 <= step <= self.steps:
            raise IndexError(step)
        state = self.initial_state
        for _ in range(step):
            state = self.channel.act_state(state)
        return state

    def branch_reduced_state(self, step: int) -> sp.ImmutableMatrix:
        """Trace all fresh environments by summing exact Kraus branches."""

        if not 0 <= step <= self.steps:
            raise IndexError(step)
        branches = (self.initial_state,)
        for _ in range(step):
            next_branches = []
            for branch in branches:
                for operator in self.channel.kraus:
                    image = sp.ImmutableMatrix(
                        (operator.matrix * branch * operator.matrix.H).applyfunc(
                            sp.simplify
                        )
                    )
                    if image != sp.zeros(self.channel.space.dimension):
                        next_branches.append(image)
            branches = tuple(next_branches)
        return sp.ImmutableMatrix(
            sum(branches, sp.zeros(self.channel.space.dimension)).applyfunc(sp.simplify)
        )