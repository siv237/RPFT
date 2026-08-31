"""Exact algebraic certificate for the polar cross-arrow covariance axis."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import sympy as sp

from ..kernel import Theorem, kernel


EXTENSIONS = (sp.sqrt(2), 2 * sp.cos(sp.pi / 7))


@dataclass(frozen=True, slots=True)
class CrossCovarianceCertificate:
    pair_matrix: sp.ImmutableMatrix
    pair_eigenvalues: tuple[sp.Expr, sp.Expr]
    soft_axis_angle_radians: sp.Expr
    polar_theorem: Theorem
    pair_formula_theorem: Theorem
    repetition_theorem: Theorem
    decoupling_theorem: Theorem
    positivity_theorem: Theorem
    common_axis_theorem: Theorem
    anisotropy_theorem: Theorem
    classical_scale_theorem: Theorem
    quantum_scale_theorem: Theorem
    heat_time_theorem: Theorem


class _FieldMatrices:
    """Tiny exact matrix helper over the real algebraic field used here."""

    def __init__(self) -> None:
        self.field = sp.QQ.algebraic_field(*EXTENSIONS)
        self.zero = self.field.zero
        self.one = self.field.one

    def element(self, value: object) -> Any:
        return self.field.from_sympy(sp.sympify(value))

    def zeros(self, rows: int, columns: int) -> list[list[Any]]:
        return [[self.zero for _ in range(columns)] for _ in range(rows)]

    def eye(self, dimension: int) -> list[list[Any]]:
        value = self.zeros(dimension, dimension)
        for index in range(dimension):
            value[index][index] = self.one
        return value

    def add(self, left: list[list[Any]], right: list[list[Any]]) -> list[list[Any]]:
        return [
            [left[i][j] + right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))
        ]

    def subtract(
        self, left: list[list[Any]], right: list[list[Any]]
    ) -> list[list[Any]]:
        return [
            [left[i][j] - right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))
        ]

    def scale(self, scalar: Any, matrix: list[list[Any]]) -> list[list[Any]]:
        return [[scalar * item for item in row] for row in matrix]

    def multiply(
        self, left: list[list[Any]], right: list[list[Any]]
    ) -> list[list[Any]]:
        return [
            [
                sum(
                    (left[i][k] * right[k][j] for k in range(len(right))),
                    self.zero,
                )
                for j in range(len(right[0]))
            ]
            for i in range(len(left))
        ]

    @staticmethod
    def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
        return [list(row) for row in zip(*matrix)]

    def inner(
        self,
        left: tuple[list[list[Any]], list[list[Any]]],
        right: tuple[list[list[Any]], list[list[Any]]],
    ) -> Any:
        return sum(
            (
                left[0][i][j] * right[0][i][j]
                + left[1][i][j] * right[1][i][j]
                for i in range(len(left[0]))
                for j in range(len(left[0][0]))
            ),
            self.zero,
        )

    def to_sympy(self, matrix: list[list[Any]]) -> sp.ImmutableMatrix:
        return sp.ImmutableMatrix(
            [[self.field.to_sympy(item) for item in row] for row in matrix]
        )


def _real_inverse_square_root_and_reference(
    algebra: _FieldMatrices,
) -> tuple[list[list[Any]], list[list[Any]]]:
    field = algebra.field
    block = [
        [algebra.element(2), algebra.one, algebra.one],
        [algebra.one, algebra.one, algebra.zero],
        [algebra.one, algebra.zero, algebra.element(2)],
    ]
    identity = algebra.eye(3)
    eigenvalues = [
        algebra.element(2 + 2 * sp.cos(2 * index * sp.pi / 7))
        for index in (1, 2, 3)
    ]
    inverse_roots = [
        algebra.element(1 / (2 * sp.cos(index * sp.pi / 7)))
        for index in (1, 2, 3)
    ]
    inverse_square_root = algebra.zeros(3, 3)
    for index, (eigenvalue, inverse_root) in enumerate(
        zip(eigenvalues, inverse_roots)
    ):
        projector = identity
        for other_index, other in enumerate(eigenvalues):
            if index == other_index:
                continue
            projector = algebra.scale(
                field.one / (eigenvalue - other),
                algebra.multiply(
                    projector,
                    algebra.subtract(block, algebra.scale(other, identity)),
                ),
            )
        inverse_square_root = algebra.add(
            inverse_square_root, algebra.scale(inverse_root, projector)
        )
    assert all(
        item == algebra.zero
        for row in algebra.subtract(
            algebra.multiply(
                algebra.multiply(inverse_square_root, block), inverse_square_root
            ),
            identity,
        )
        for item in row
    )

    target_inverse_root = algebra.zeros(10, 10)
    for index in range(6):
        target_inverse_root[index][index] = algebra.one
    lepton_indices = (6, 7, 9)
    for i in range(3):
        for j in range(3):
            target_inverse_root[lepton_indices[i]][lepton_indices[j]] = (
                inverse_square_root[i][j]
            )
    target_inverse_root[8][8] = algebra.element(1 / sp.sqrt(2))

    reference = algebra.zeros(10, 11)
    for color in range(3):
        reference[color][2 * color] = algebra.one
        reference[3 + color][2 * color + 1] = algebra.one
    for row, column in ((6, 7), (8, 6), (9, 7), (7, 8), (6, 8), (8, 9), (9, 10)):
        reference[row][column] = algebra.one
    transfer = algebra.multiply(target_inverse_root, reference)
    return transfer, reference


def _variation_basis(
    algebra: _FieldMatrices,
) -> list[tuple[list[list[Any]], int]]:
    def arrow(entries: tuple[tuple[int, int], ...]) -> list[list[Any]]:
        value = algebra.zeros(10, 11)
        for row, column in entries:
            value[row][column] = algebra.one
        return value

    variations: list[tuple[list[list[Any]], int]] = []
    variations.extend(
        (item, 0)
        for item in (
            arrow(tuple((color, 2 * color) for color in range(3))),
            arrow(tuple((3 + color, 2 * color + 1) for color in range(3))),
            arrow(((6, 7),)),
            arrow(((8, 6), (9, 7))),
            arrow(((7, 8),)),
            arrow(((6, 8),)),
            arrow(((8, 9), (9, 10))),
        )
    )
    for color in range(3):
        qlyr = arrow(((8, 2 * color), (9, 2 * color + 1)))
        xldr = arrow(((3 + color, 8),))
        variations.extend(
            ((qlyr, 0), (qlyr, -1), (xldr, 0), (xldr, 1))
        )
    for weak in range(2):
        llxr = arrow(((7, 6 + weak),))
        yler = arrow(((6, 9 + weak),))
        variations.extend(((llxr, 0), (llxr, 1), (yler, 0), (yler, 1)))
    assert len(variations) == 27
    return variations


def _linearized_relative(
    algebra: _FieldMatrices,
    reference: list[list[Any]],
    transfer: list[list[Any]],
    variation: tuple[list[list[Any]], int],
) -> tuple[list[list[Any]], list[list[Any]]]:
    real, imaginary_phase = variation
    zero = algebra.zeros(10, 11)
    if imaginary_phase:
        real_part = zero
        imaginary_part = algebra.scale(algebra.element(imaginary_phase), real)
    else:
        real_part, imaginary_part = real, zero
    reference_t = algebra.transpose(reference)
    real_t = algebra.transpose(real_part)
    imaginary_t = algebra.transpose(imaginary_part)
    source_real = algebra.add(
        algebra.multiply(reference_t, real_part),
        algebra.multiply(real_t, reference),
    )
    source_imaginary = algebra.subtract(
        algebra.multiply(reference_t, imaginary_part),
        algebra.multiply(imaginary_t, reference),
    )
    target_real = algebra.add(
        algebra.multiply(reference, real_t),
        algebra.multiply(real_part, reference_t),
    )
    target_imaginary = algebra.subtract(
        algebra.multiply(imaginary_part, reference_t),
        algebra.multiply(reference, imaginary_t),
    )
    return (
        algebra.subtract(
            algebra.multiply(target_real, transfer),
            algebra.multiply(transfer, source_real),
        ),
        algebra.subtract(
            algebra.multiply(target_imaginary, transfer),
            algebra.multiply(transfer, source_imaginary),
        ),
    )


@lru_cache(maxsize=1)
def _exact_geometry() -> tuple[
    sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix
]:
    algebra = _FieldMatrices()
    transfer, reference = _real_inverse_square_root_and_reference(algebra)
    transfer_transfer_t = algebra.multiply(transfer, algebra.transpose(transfer))
    polar_residual = algebra.subtract(transfer_transfer_t, algebra.eye(10))
    assert all(item == algebra.zero for row in polar_residual for item in row)

    relative = [
        _linearized_relative(algebra, reference, transfer, variation)
        for variation in _variation_basis(algebra)
    ]
    hessian = [
        [algebra.inner(left, right) for right in relative] for left in relative
    ]
    cross_indices = []
    for color in range(3):
        offset = 7 + 4 * color
        cross_indices.extend((offset, offset + 2, offset + 1, offset + 3))
    other_indices = [index for index in range(27) if index not in cross_indices]
    cross = [[hessian[i][j] for j in cross_indices] for i in cross_indices]
    coupling = [[hessian[i][j] for j in other_indices] for i in cross_indices]
    pair = [[cross[i][j] for j in range(2)] for i in range(2)]
    return (
        algebra.to_sympy(transfer),
        algebra.to_sympy(pair),
        algebra.to_sympy(cross),
        algebra.to_sympy(coupling),
    )


@lru_cache(maxsize=1)
def build_certificate() -> CrossCovarianceCertificate:
    transfer, pair, cross, coupling = _exact_geometry()
    cosine = sp.cos(sp.pi / 7)
    expected_pair = sp.ImmutableMatrix(
        [
            [
                sp.Rational(124, 7) - 4 * sp.sqrt(2) - sp.Rational(96, 7) * cosine**2,
                -sp.Rational(6, 7)
                + sp.Rational(32, 7) * cosine
                - sp.Rational(32, 7) * cosine**2,
            ],
            [
                -sp.Rational(6, 7)
                + sp.Rational(32, 7) * cosine
                - sp.Rational(32, 7) * cosine**2,
                sp.Rational(82, 7) - sp.Rational(96, 7) * cosine**2,
            ],
        ]
    )
    pair_formula = kernel.prove_algebraic_field_matrix_equality(
        pair,
        expected_pair,
        extensions=EXTENSIONS,
        subject="exact polar QLYR-XLdR linking pair",
    )
    repetition = kernel.prove_algebraic_field_matrix_equality(
        cross,
        sp.kronecker_product(sp.eye(6), pair),
        extensions=EXTENSIONS,
        subject="six repeated polar cross-arrow pairs",
    )
    decoupling = kernel.prove_algebraic_field_matrix_equality(
        coupling,
        sp.zeros(12, 15),
        extensions=EXTENSIONS,
        subject="cross-arrow decoupling from the other fifteen directions",
    )
    positivity = kernel.prove_positive_definite_symmetric_2x2(
        pair,
        extensions=EXTENSIONS,
        subject="polar cross-arrow pair",
    )

    trace = sp.simplify(sp.trace(pair))
    discriminant = sp.simplify((pair[0, 0] - pair[1, 1]) ** 2 + 4 * pair[0, 1] ** 2)
    eigenvalues = (
        sp.simplify((trace - sp.sqrt(discriminant)) / 2),
        sp.simplify((trace + sp.sqrt(discriminant)) / 2),
    )
    eta = sp.Symbol("eta", positive=True)
    common_axis = kernel.prove_affine_common_spectral_axes(
        pair,
        sp.Rational(32, 5),
        2 * eta,
        subject="all positive-eta covariance functions of the polar pair",
        premises=(positivity,),
    )
    anisotropy_ratio = sp.simplify(
        (sp.Rational(32, 5) + 2 * eta * eigenvalues[1])
        / (sp.Rational(32, 5) + 2 * eta * eigenvalues[0])
    )
    anisotropy = kernel.prove_expression_nonconstant(
        anisotropy_ratio,
        eta,
        subject="normalized classical covariance anisotropy",
    )

    base_rate = sp.Symbol("Gamma_0", positive=True)
    action_scale = sp.Symbol("a", positive=True)
    quantum_scale = sp.Symbol("kappa", positive=True)
    correlation_time = sp.Symbol("tau", positive=True)
    classical_scale = kernel.prove_expression_nonconstant(
        base_rate / action_scale,
        action_scale,
        subject="classical Gaussian Kraus rate",
    )
    quantum_scale_theorem = kernel.prove_expression_nonconstant(
        quantum_scale * base_rate,
        quantum_scale,
        subject="harmonic ground-state Kraus rate",
    )
    heat_rate = sp.exp(-correlation_time * eigenvalues[0]) + sp.exp(
        -correlation_time * eigenvalues[1]
    )
    heat_time = kernel.prove_expression_nonconstant(
        heat_rate,
        correlation_time,
        subject="heat-kernel Kraus rate",
    )

    stiff_angle = sp.atan2(2 * pair[0, 1], pair[0, 0] - pair[1, 1]) / 2
    soft_angle = sp.simplify(stiff_angle + sp.pi / 2)
    polar = kernel.prove_algebraic_field_matrix_equality(
        transfer * transfer.T,
        sp.eye(10),
        extensions=EXTENSIONS,
        subject="exact polar coisometry constructed from the physical reference",
    )
    return CrossCovarianceCertificate(
        pair_matrix=pair,
        pair_eigenvalues=eigenvalues,
        soft_axis_angle_radians=soft_angle,
        polar_theorem=polar,
        pair_formula_theorem=pair_formula,
        repetition_theorem=repetition,
        decoupling_theorem=decoupling,
        positivity_theorem=positivity,
        common_axis_theorem=common_axis,
        anisotropy_theorem=anisotropy,
        classical_scale_theorem=classical_scale,
        quantum_scale_theorem=quantum_scale_theorem,
        heat_time_theorem=heat_time,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.pair_matrix.evalf(12))
    print(sp.N(certificate.soft_axis_angle_radians * 180 / sp.pi, 12))