"""Type-safe finite-dimensional GKSL/Lindblad constructors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp

from .kernel import Theorem, kernel
from .structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class LindbladGenerator:
    name: str
    space: Space
    hamiltonian: Morphism
    jumps: tuple[Morphism, ...]
    rates: tuple[sp.Expr, ...]
    theorem: Theorem

    @classmethod
    def make(
        cls,
        name: str,
        hamiltonian: Morphism,
        jumps: Iterable[Morphism],
        rates: Iterable[object],
    ) -> "LindbladGenerator":
        jump_tuple = tuple(jumps)
        rate_tuple = tuple(sp.sympify(rate) for rate in rates)
        if len(jump_tuple) != len(rate_tuple):
            raise ValueError("jumps and rates must have equal lengths")
        if not hamiltonian.is_endomorphism:
            raise TypeError("Hamiltonian must be an endomorphism")
        provisional = object.__new__(cls)
        object.__setattr__(provisional, "name", name)
        object.__setattr__(provisional, "space", hamiltonian.source)
        object.__setattr__(provisional, "hamiltonian", hamiltonian)
        object.__setattr__(provisional, "jumps", jump_tuple)
        object.__setattr__(provisional, "rates", rate_tuple)
        theorem = kernel.prove_gksl_well_formed(provisional)
        object.__setattr__(provisional, "theorem", theorem)
        return provisional

    def act(self, density_matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
        rho = sp.ImmutableMatrix(density_matrix)
        expected = (self.space.dimension, self.space.dimension)
        if rho.shape != expected:
            raise ValueError(f"density matrix shape must be {expected}")
        h = self.hamiltonian.matrix
        value = -sp.I * (h * rho - rho * h)
        for jump, rate in zip(self.jumps, self.rates):
            operator = jump.matrix
            square = operator.H * operator
            value += rate * (
                operator * rho * operator.H
                - sp.Rational(1, 2) * (square * rho + rho * square)
            )
        return sp.ImmutableMatrix(value.applyfunc(sp.simplify))