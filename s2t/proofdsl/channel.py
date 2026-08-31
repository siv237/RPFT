"""Type-safe finite-dimensional Kraus channels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp

from .kernel import Theorem, kernel
from .structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class KrausChannel:
    name: str
    space: Space
    kraus: tuple[Morphism, ...]
    theorem: Theorem

    @classmethod
    def make(cls, name: str, kraus: Iterable[Morphism]) -> "KrausChannel":
        operators = tuple(kraus)
        if not operators:
            raise ValueError("a Kraus channel needs at least one operator")
        provisional = object.__new__(cls)
        object.__setattr__(provisional, "name", name)
        object.__setattr__(provisional, "space", operators[0].source)
        object.__setattr__(provisional, "kraus", operators)
        theorem = kernel.prove_kraus_channel_well_formed(provisional)
        object.__setattr__(provisional, "theorem", theorem)
        return provisional

    def act(self, observable: sp.MatrixBase) -> sp.ImmutableMatrix:
        value = sp.ImmutableMatrix(observable)
        expected = (self.space.dimension, self.space.dimension)
        if value.shape != expected:
            raise ValueError(f"observable shape must be {expected}")
        image = sum(
            (operator.matrix.H * value * operator.matrix for operator in self.kraus),
            sp.zeros(self.space.dimension),
        )
        return sp.ImmutableMatrix(image.applyfunc(sp.simplify))

    def act_state(self, state: sp.MatrixBase) -> sp.ImmutableMatrix:
        """Schrodinger-picture dual action ``rho -> sum K rho K†``."""

        value = sp.ImmutableMatrix(state)
        expected = (self.space.dimension, self.space.dimension)
        if value.shape != expected:
            raise ValueError(f"state shape must be {expected}")
        image = sum(
            (operator.matrix * value * operator.matrix.H for operator in self.kraus),
            sp.zeros(self.space.dimension),
        )
        return sp.ImmutableMatrix(image.applyfunc(sp.simplify))