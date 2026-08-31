"""Exact SymPy calculations that do not themselves mint theorem values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp

from .kernel import ProofError
from .structures import MatrixRepresentation, exact_matrix


@dataclass(frozen=True, slots=True)
class IntertwinerSolution:
    source_dimension: int
    target_dimension: int
    basis: tuple[sp.ImmutableMatrix, ...]

    @property
    def dimension(self) -> int:
        return len(self.basis)


def exact_rank(matrix: sp.MatrixBase | Sequence[Sequence[object]]) -> int:
    return int(exact_matrix(matrix).rank())


def solve_intertwiners(
    source: MatrixRepresentation, target: MatrixRepresentation
) -> IntertwinerSolution:
    if source.generator_names != target.generator_names:
        raise ProofError("generator sets must agree")
    m = target.space.dimension
    n = source.space.dimension
    constraints = []
    for name in source.generator_names:
        left = target.generator(name)
        right = source.generator(name)
        constraints.append(
            sp.kronecker_product(sp.eye(n), left)
            - sp.kronecker_product(right.T, sp.eye(m))
        )
    system = sp.Matrix.vstack(*constraints)
    vectors = system.nullspace()
    basis = tuple(
        sp.ImmutableMatrix(
            m,
            n,
            lambda row, column: vector[row + m * column],
        )
        for vector in vectors
    )
    return IntertwinerSolution(n, m, basis)