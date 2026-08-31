"""Exact common-commutant proof for the Tome VIII fixed algebra."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from ..kernel import Theorem, kernel
from ..structures import Irrep, IsotypicBlock, SemisimpleRepresentation, Space


GROUP = "SU(3)xSU(2)xU(1)"


@dataclass(frozen=True, slots=True)
class FixedAlgebraCertificate:
    gauge_commutant_dimension: int
    full_fixed_dimension: int
    quark_projector_rank: int
    lepton_projector_rank: int
    one_sided_kernel_dimension: int
    gauge_theorem: Theorem
    fixed_theorem: Theorem
    projector_theorem: Theorem


def _endpoint_representations() -> tuple[
    SemisimpleRepresentation, SemisimpleRepresentation
]:
    ql = Irrep(GROUP, "(3,2)_{1/6}", 6)
    weak_lepton = Irrep(GROUP, "(1,2)_{-1/2}", 2)
    singlet_minus_one = Irrep(GROUP, "(1,1)_{-1}", 1)
    up = Irrep(GROUP, "(3,1)_{2/3}", 3)
    down = Irrep(GROUP, "(3,1)_{-1/3}", 3)
    source = SemisimpleRepresentation(
        "source_endpoint",
        Space("E_s", 11),
        (
            IsotypicBlock(ql),
            IsotypicBlock(weak_lepton, 2),
            IsotypicBlock(singlet_minus_one),
        ),
    )
    target = SemisimpleRepresentation(
        "target_endpoint",
        Space("E_t", 10),
        (
            IsotypicBlock(up),
            IsotypicBlock(down),
            IsotypicBlock(singlet_minus_one, 2),
            IsotypicBlock(weak_lepton),
        ),
    )
    return source, target


def physical_incidence() -> sp.ImmutableMatrix:
    matrix = sp.zeros(10, 11)
    for row, column in (
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 1),
        (4, 3),
        (5, 5),
        (6, 7),
        (6, 8),
        (7, 8),
        (8, 6),
        (8, 9),
        (9, 7),
        (9, 10),
    ):
        matrix[row, column] = 1
    return sp.ImmutableMatrix(matrix)


def _gauge_commutant_pair(
    variables: tuple[sp.Symbol, ...],
) -> tuple[sp.Matrix, sp.Matrix]:
    (
        ql,
        up,
        down,
        k11,
        k12,
        k21,
        k22,
        xl,
        l11,
        l12,
        l21,
        l22,
        yr,
    ) = variables
    source = sp.zeros(11)
    source[:6, :6] = ql * sp.eye(6)
    source[6:8, 6:8] = k11 * sp.eye(2)
    source[6:8, 9:11] = k12 * sp.eye(2)
    source[9:11, 6:8] = k21 * sp.eye(2)
    source[9:11, 9:11] = k22 * sp.eye(2)
    source[8, 8] = xl

    target = sp.zeros(10)
    target[:3, :3] = up * sp.eye(3)
    target[3:6, 3:6] = down * sp.eye(3)
    target[6, 6] = l11
    target[6, 7] = l12
    target[7, 6] = l21
    target[7, 7] = l22
    target[8:10, 8:10] = yr * sp.eye(2)
    return source, target


def build_certificate() -> FixedAlgebraCertificate:
    source_rep, target_rep = _endpoint_representations()
    gauge_theorem = kernel.prove_semisimple_commutant_dimension(
        (source_rep, target_rep),
        13,
        subject="block-diagonal endpoint gauge commutant",
    )

    variables = sp.symbols(
        "q_Q u_R d_R k11 k12 k21 k22 x_L l11 l12 l21 l22 y_R"
    )
    source, target = _gauge_commutant_pair(variables)
    incidence = physical_incidence()
    forward = incidence * source - target * incidence
    backward = source * incidence.H - incidence.H * target
    full_system, _ = sp.linear_eq_to_matrix(
        list(forward) + list(backward), variables
    )
    one_sided_system, _ = sp.linear_eq_to_matrix(list(forward), variables)

    quark_coordinates = sp.Matrix([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    lepton_coordinates = sp.Matrix([0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1])
    basis = quark_coordinates.row_join(lepton_coordinates)
    fixed_theorem = kernel.prove_linear_kernel(
        full_system,
        basis,
        subject="joint gauge and self-adjoint linking commutant",
    )
    assert len(one_sided_system.nullspace()) == 4

    quark_source, quark_target = _gauge_commutant_pair(
        tuple(quark_coordinates)
    )
    lepton_source, lepton_target = _gauge_commutant_pair(
        tuple(lepton_coordinates)
    )
    quark = sp.diag(quark_source, quark_target)
    lepton = sp.diag(lepton_source, lepton_target)
    projector_theorem = kernel.prove_complementary_projectors(
        quark,
        lepton,
        expected_ranks=(12, 9),
        subject="quark and lepton/vectorlike endpoint sectors",
    )
    return FixedAlgebraCertificate(
        gauge_commutant_dimension=13,
        full_fixed_dimension=2,
        quark_projector_rank=12,
        lepton_projector_rank=9,
        one_sided_kernel_dimension=4,
        gauge_theorem=gauge_theorem,
        fixed_theorem=fixed_theorem,
        projector_theorem=projector_theorem,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(f"gauge commutant: {certificate.gauge_commutant_dimension}")
    print(f"full fixed algebra: {certificate.full_fixed_dimension}")
    print(
        "projector ranks: "
        f"{certificate.quark_projector_rank}+{certificate.lepton_projector_rank}"
    )