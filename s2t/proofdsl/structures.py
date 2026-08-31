"""Typed spaces, representations and morphisms for the S2T proof eDSL."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import sympy as sp

from .kernel import ProofError


def exact_matrix(value: sp.MatrixBase | Sequence[Sequence[object]]) -> sp.ImmutableMatrix:
    matrix = sp.ImmutableMatrix(value)
    if matrix.atoms(sp.Float):
        raise ProofError("use Rational, Integer or exact algebraic values, not Float")
    return matrix


@dataclass(frozen=True, slots=True)
class Space:
    name: str
    dimension: int
    scalar_field: str = "C"

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("a space must have a name")
        if self.dimension <= 0:
            raise ValueError("space dimension must be positive")
        if self.scalar_field not in {"R", "C"}:
            raise ValueError("the MVP supports only R and C")


@dataclass(frozen=True, slots=True)
class Morphism:
    name: str
    source: Space
    target: Space
    matrix: sp.ImmutableMatrix

    def __init__(
        self,
        name: str,
        source: Space,
        target: Space,
        matrix: sp.MatrixBase | Sequence[Sequence[object]],
    ) -> None:
        value = exact_matrix(matrix)
        expected = (target.dimension, source.dimension)
        if value.shape != expected:
            raise ValueError(f"matrix shape {value.shape} does not realize {expected}")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "target", target)
        object.__setattr__(self, "matrix", value)

    @property
    def is_endomorphism(self) -> bool:
        return self.source == self.target

    @property
    def dagger(self) -> "Morphism":
        return Morphism(f"{self.name}†", self.target, self.source, self.matrix.H)

    def then(self, after: "Morphism", *, name: str | None = None) -> "Morphism":
        if self.target != after.source:
            raise TypeError(
                f"cannot compose {self.source.name}->{self.target.name} with "
                f"{after.source.name}->{after.target.name}"
            )
        return Morphism(
            name or f"{after.name}∘{self.name}",
            self.source,
            after.target,
            after.matrix * self.matrix,
        )


@dataclass(frozen=True, slots=True)
class MatrixRepresentation:
    name: str
    space: Space
    generators: tuple[tuple[str, sp.ImmutableMatrix], ...]

    def __init__(
        self,
        name: str,
        space: Space,
        generators: Iterable[tuple[str, sp.MatrixBase | Sequence[Sequence[object]]]],
    ) -> None:
        checked = []
        seen = set()
        for generator_name, raw in generators:
            if generator_name in seen:
                raise ValueError(f"duplicate generator {generator_name}")
            seen.add(generator_name)
            matrix = exact_matrix(raw)
            if matrix.shape != (space.dimension, space.dimension):
                raise ValueError(f"generator {generator_name} has the wrong shape")
            checked.append((generator_name, matrix))
        if not checked:
            raise ValueError("a representation needs at least one generator")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "space", space)
        object.__setattr__(self, "generators", tuple(checked))

    @property
    def generator_names(self) -> tuple[str, ...]:
        return tuple(name for name, _ in self.generators)

    def generator(self, name: str) -> sp.ImmutableMatrix:
        for generator_name, matrix in self.generators:
            if generator_name == name:
                return matrix
        raise KeyError(name)


@dataclass(frozen=True, slots=True, order=True)
class Irrep:
    """Exact identifier for one irreducible gauge representation."""

    group: str
    label: str
    dimension: int

    def __post_init__(self) -> None:
        if self.dimension <= 0:
            raise ValueError("irrep dimension must be positive")


@dataclass(frozen=True, slots=True)
class IsotypicBlock:
    irrep: Irrep
    multiplicity: int = 1

    def __post_init__(self) -> None:
        if self.multiplicity <= 0:
            raise ValueError("multiplicity must be positive")

    @property
    def dimension(self) -> int:
        return self.irrep.dimension * self.multiplicity


@dataclass(frozen=True, slots=True)
class SemisimpleRepresentation:
    name: str
    space: Space
    blocks: tuple[IsotypicBlock, ...]

    def __init__(
        self, name: str, space: Space, blocks: Iterable[IsotypicBlock]
    ) -> None:
        merged: dict[Irrep, int] = {}
        for block in blocks:
            merged[block.irrep] = merged.get(block.irrep, 0) + block.multiplicity
        canonical = tuple(
            IsotypicBlock(irrep, multiplicity)
            for irrep, multiplicity in sorted(merged.items())
        )
        total = sum(block.dimension for block in canonical)
        if total != space.dimension:
            raise ValueError(
                f"isotypic dimensions sum to {total}, expected {space.dimension}"
            )
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "space", space)
        object.__setattr__(self, "blocks", canonical)

    def multiplicity(self, irrep: Irrep) -> int:
        return next(
            (block.multiplicity for block in self.blocks if block.irrep == irrep),
            0,
        )


@dataclass(frozen=True, slots=True)
class IntertwinerProfile:
    hom_dimension: int
    maximum_rank: int
    shared_blocks: tuple[tuple[str, int, int, int], ...]


def intertwiner_profile(
    source: SemisimpleRepresentation, target: SemisimpleRepresentation
) -> IntertwinerProfile:
    """Exact Schur-lemma profile of ``Hom_G(source, target)``."""

    hom_dimension = 0
    maximum_rank = 0
    shared = []
    for source_block in source.blocks:
        target_multiplicity = target.multiplicity(source_block.irrep)
        if target_multiplicity == 0:
            continue
        hom_dimension += source_block.multiplicity * target_multiplicity
        maximum_rank += source_block.irrep.dimension * min(
            source_block.multiplicity, target_multiplicity
        )
        shared.append(
            (
                source_block.irrep.label,
                source_block.irrep.dimension,
                source_block.multiplicity,
                target_multiplicity,
            )
        )
    return IntertwinerProfile(hom_dimension, maximum_rank, tuple(shared))