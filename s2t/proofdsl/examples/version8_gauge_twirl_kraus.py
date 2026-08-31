"""Exact LCF certificate for the gauge-twirled cross-sector Kraus bridge."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..lindblad import LindbladGenerator
from ..structures import Morphism, Space


SOURCE_DIMENSION = 11
TARGET_DIMENSION = 10
ENDPOINT_DIMENSION = SOURCE_DIMENSION + TARGET_DIMENSION


@dataclass(frozen=True, slots=True)
class GaugeTwirlKrausCertificate:
    cross_real_dimension: int
    internal_control_dimension: int
    qlyr_central_matrix: sp.ImmutableMatrix
    xldr_central_matrix: sp.ImmutableMatrix
    cross_central_matrix: sp.ImmutableMatrix
    internal_central_matrix: sp.ImmutableMatrix
    gksl_theorem: Theorem
    unital_theorem: Theorem
    basis_invariance_theorem: Theorem
    gauge_covariance_theorem: Theorem
    qlyr_central_theorem: Theorem
    xldr_central_theorem: Theorem
    cross_central_theorem: Theorem
    cross_kernel_theorem: Theorem
    internal_control_theorem: Theorem
    positive_rate_kernel_theorem: Theorem


def _matrix_unit(rows: int, columns: int, row: int, column: int) -> sp.Matrix:
    value = sp.zeros(rows, columns)
    value[row, column] = 1
    return value


def _realified_arrows(arrows: tuple[sp.MatrixBase, ...]) -> tuple[sp.ImmutableMatrix, ...]:
    result = []
    for arrow in arrows:
        norm_squared = sp.simplify(sp.trace(arrow.H * arrow))
        normalized = sp.ImmutableMatrix(arrow / sp.sqrt(norm_squared))
        result.extend((normalized, sp.ImmutableMatrix(sp.I * normalized)))
    return tuple(result)


def cross_arrow_families() -> tuple[
    tuple[sp.ImmutableMatrix, ...], tuple[sp.ImmutableMatrix, ...]
]:
    qlyr = []
    xldr = []
    for color in range(3):
        qlyr_arrow = sp.zeros(TARGET_DIMENSION, SOURCE_DIMENSION)
        qlyr_arrow[8, 2 * color] = 1
        qlyr_arrow[9, 2 * color + 1] = 1
        qlyr.append(qlyr_arrow)
        xldr.append(_matrix_unit(TARGET_DIMENSION, SOURCE_DIMENSION, 3 + color, 8))
    return _realified_arrows(tuple(qlyr)), _realified_arrows(tuple(xldr))


def internal_control_arrows() -> tuple[sp.ImmutableMatrix, ...]:
    llxr = tuple(
        _matrix_unit(TARGET_DIMENSION, SOURCE_DIMENSION, 7, 6 + weak)
        for weak in range(2)
    )
    yler = tuple(
        _matrix_unit(TARGET_DIMENSION, SOURCE_DIMENSION, 6, 9 + weak)
        for weak in range(2)
    )
    return _realified_arrows(llxr + yler)


def _dirac_jump(arrow: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(ENDPOINT_DIMENSION)
    result[:SOURCE_DIMENSION, SOURCE_DIMENSION:] = arrow.H
    result[SOURCE_DIMENSION:, :SOURCE_DIMENSION] = arrow
    return sp.ImmutableMatrix(result)


def kraus_generator(name: str, arrows: tuple[sp.ImmutableMatrix, ...]) -> LindbladGenerator:
    endpoint = Space("E_s+E_t", ENDPOINT_DIMENSION)
    zero = Morphism(f"H_0^{name}", endpoint, endpoint, sp.zeros(ENDPOINT_DIMENSION))
    jumps = tuple(
        Morphism(f"D_{name}_{index}", endpoint, endpoint, _dirac_jump(arrow))
        for index, arrow in enumerate(arrows)
    )
    return LindbladGenerator.make(name, zero, jumps, [sp.Integer(1)] * len(jumps))


def central_basis() -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix]:
    quark_source = sp.diag(*([1] * 6 + [0] * 5))
    quark_target = sp.diag(*([1] * 6 + [0] * 4))
    quark = sp.diag(quark_source, quark_target)
    lepton = sp.eye(ENDPOINT_DIMENSION) - quark
    return (
        sp.ImmutableMatrix(quark / sp.sqrt(12)),
        sp.ImmutableMatrix(lepton / 3),
    )


def _central_matrix(generator: LindbladGenerator) -> sp.ImmutableMatrix:
    basis = central_basis()
    return sp.ImmutableMatrix(
        [
            [
                sp.simplify(sp.trace(left.H * (-generator.act(right))))
                for right in basis
            ]
            for left in basis
        ]
    )


def _gell_mann_generators() -> tuple[sp.ImmutableMatrix, ...]:
    i = sp.I
    return tuple(
        sp.ImmutableMatrix(item)
        for item in (
            [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
            [[0, -i, 0], [i, 0, 0], [0, 0, 0]],
            [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
            [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
            [[0, 0, -i], [0, 0, 0], [i, 0, 0]],
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            [[0, 0, 0], [0, 0, -i], [0, i, 0]],
            [[1, 0, 0], [0, 1, 0], [0, 0, -2]],
        )
    )


def _pauli_generators() -> tuple[sp.ImmutableMatrix, ...]:
    return (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )


def _endpoint_gauge_generators() -> tuple[sp.ImmutableMatrix, ...]:
    zero3 = sp.zeros(3)
    zero2 = sp.zeros(2)
    generators = []
    for color in _gell_mann_generators():
        source = sp.diag(sp.kronecker_product(color, sp.eye(2)), zero2, 0, zero2)
        target = sp.diag(color, color, 0, 0, zero2)
        generators.append(sp.ImmutableMatrix(sp.diag(source, target)))
    for weak in _pauli_generators():
        source = sp.diag(sp.kronecker_product(sp.eye(3), weak), weak, 0, weak)
        target = sp.diag(zero3, zero3, 0, 0, weak)
        generators.append(sp.ImmutableMatrix(sp.diag(source, target)))
    source_y = sp.diag(
        sp.Rational(1, 6) * sp.eye(6),
        -sp.Rational(1, 2) * sp.eye(2),
        -1,
        -sp.Rational(1, 2) * sp.eye(2),
    )
    target_y = sp.diag(
        sp.Rational(2, 3) * sp.eye(3),
        -sp.Rational(1, 3) * sp.eye(3),
        -1,
        -1,
        -sp.Rational(1, 2) * sp.eye(2),
    )
    generators.append(sp.ImmutableMatrix(sp.diag(source_y, target_y)))
    return tuple(generators)


@lru_cache(maxsize=1)
def build_certificate() -> GaugeTwirlKrausCertificate:
    qlyr_arrows, xldr_arrows = cross_arrow_families()
    internal_arrows = internal_control_arrows()
    cross_arrows = qlyr_arrows + xldr_arrows
    qlyr = kraus_generator("QLYR", qlyr_arrows)
    xldr = kraus_generator("XLdR", xldr_arrows)
    cross = kraus_generator("cross_gauge_twirl", cross_arrows)
    internal = kraus_generator("internal_lepton_control", internal_arrows)

    expected_family = sp.ImmutableMatrix(
        [
            [sp.Rational(1, 2), -1 / sp.sqrt(3)],
            [-1 / sp.sqrt(3), sp.Rational(2, 3)],
        ]
    )
    expected_cross = sp.ImmutableMatrix(
        [[1, -2 / sp.sqrt(3)], [-2 / sp.sqrt(3), sp.Rational(4, 3)]]
    )
    qlyr_matrix = _central_matrix(qlyr)
    xldr_matrix = _central_matrix(xldr)
    cross_matrix = _central_matrix(cross)
    internal_matrix = _central_matrix(internal)

    qlyr_theorem = kernel.prove_matrix_equality(
        qlyr_matrix, expected_family, subject="QLYR central Dirichlet restriction"
    )
    xldr_theorem = kernel.prove_matrix_equality(
        xldr_matrix, expected_family, subject="XLdR central Dirichlet restriction"
    )
    cross_theorem = kernel.prove_matrix_equality(
        cross_matrix, expected_cross, subject="combined cross-sector central restriction"
    )
    cross_kernel = kernel.prove_exact_nullity(
        cross_matrix, 1, subject="cross-sector central fixed line"
    )
    internal_control = kernel.prove_matrix_equality(
        internal_matrix, sp.zeros(2), subject="internal lepton central control"
    )

    qlyr_rate = sp.Symbol("gamma_QLYR", positive=True)
    xldr_rate = sp.Symbol("gamma_XLdR", positive=True)
    positive_rate_matrix = (qlyr_rate + xldr_rate) * expected_family
    positive_rate_kernel = kernel.prove_exact_nullity(
        positive_rate_matrix,
        1,
        subject="central fixed line for all positive cross-family rates",
    )
    basis_invariance = kernel.prove_equal_rate_kraus_basis_invariance(
        cross, subject="complete real cross-arrow Kraus frame"
    )
    frame = tuple(jump.matrix for jump in cross.jumps)
    gauge_covariance = kernel.prove_orthogonal_frame_covariance(
        frame,
        _endpoint_gauge_generators(),
        expected_invariant_dimension=0,
        subject="SU(3) x SU(2) x U(1) cross-arrow jump multiplet",
    )
    unital = kernel.prove_generator_unital(cross)

    return GaugeTwirlKrausCertificate(
        cross_real_dimension=len(cross_arrows),
        internal_control_dimension=len(internal_arrows),
        qlyr_central_matrix=qlyr_matrix,
        xldr_central_matrix=xldr_matrix,
        cross_central_matrix=cross_matrix,
        internal_central_matrix=internal_matrix,
        gksl_theorem=cross.theorem,
        unital_theorem=unital,
        basis_invariance_theorem=basis_invariance,
        gauge_covariance_theorem=gauge_covariance,
        qlyr_central_theorem=qlyr_theorem,
        xldr_central_theorem=xldr_theorem,
        cross_central_theorem=cross_theorem,
        cross_kernel_theorem=cross_kernel,
        internal_control_theorem=internal_control,
        positive_rate_kernel_theorem=positive_rate_kernel,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.cross_central_matrix)
    print(certificate.gauge_covariance_theorem.proposition)