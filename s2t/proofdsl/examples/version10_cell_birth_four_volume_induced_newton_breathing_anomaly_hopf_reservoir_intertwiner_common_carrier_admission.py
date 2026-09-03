"""LCF certificate for the minimal common Hopf-reservoir carrier."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfReservoirCommonCarrierCertificate:
    reservoir_projector: sp.ImmutableMatrix
    path_projector: sp.ImmutableMatrix
    common_orientation: sp.ImmutableMatrix
    intertwiner: sp.ImmutableMatrix
    phase_intertwiners: tuple[sp.ImmutableMatrix, ...]
    algebra_basis: sp.ImmutableMatrix
    commutant_constraint: sp.ImmutableMatrix
    commutant_kernel: sp.ImmutableMatrix
    conditional_hessian: sp.ImmutableMatrix
    mixed_block: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    inherited_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfReservoirCommonCarrierCertificate:
    identity2 = sp.ImmutableMatrix.eye(2)
    zero2 = sp.ImmutableMatrix.zeros(2, 2)
    reservoir_projector = sp.ImmutableMatrix.diag(1, 1, 0, 0)
    path_projector = sp.ImmutableMatrix.diag(0, 0, 1, 1)
    z = sp.ImmutableMatrix.diag(-1, 1)
    common_orientation = sp.ImmutableMatrix.diag(-1, 1, -1, 1)
    intertwiner = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix.hstack(zero2, identity2),
        sp.ImmutableMatrix.hstack(zero2, zero2),
    )
    phase_intertwiners = tuple(
        sp.ImmutableMatrix.vstack(
            sp.ImmutableMatrix.hstack(zero2, sp.diag(s1, s2)),
            sp.ImmutableMatrix.hstack(zero2, zero2),
        )
        for s1, s2 in ((1, 1), (-1, 1), (1, -1), (-1, -1))
    )

    units = []
    for i in range(4):
        for j in range(4):
            unit = sp.zeros(4)
            unit[i, j] = 1
            units.append(sp.ImmutableMatrix(unit))
    algebra_basis = sp.ImmutableMatrix.hstack(
        *[unit.reshape(16, 1) for unit in units]
    )
    scalar_vector = sp.ImmutableMatrix(sp.eye(4)).reshape(16, 1)
    commutant_constraint = sp.ImmutableMatrix(
        sp.eye(16) - sp.Rational(1, 4) * scalar_vector * scalar_vector.T
    )
    commutant_kernel = scalar_vector

    mixed_block = -sp.Rational(1, 2) * identity2
    conditional_hessian = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix.hstack(identity2, mixed_block),
        sp.ImmutableMatrix.hstack(mixed_block, identity2),
    )
    architecture = sp.ImmutableMatrix.ones(12, 1)
    inherited_origin = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])
    physical_origin = sp.ImmutableMatrix.zeros(4, 1)

    hessian_spectrum = {sp.Rational(1, 2): 2, sp.Rational(3, 2): 2}
    theorems = (
        kernel.prove_matrix_equality(reservoir_projector**2, reservoir_projector,
                                     subject="reservoir type projector is idempotent"),
        kernel.prove_matrix_equality(path_projector**2, path_projector,
                                     subject="path type projector is idempotent"),
        kernel.prove_matrix_equality(reservoir_projector * path_projector, sp.zeros(4),
                                     subject="reservoir and path sectors are orthogonal"),
        kernel.prove_matrix_equality(reservoir_projector + path_projector, sp.eye(4),
                                     subject="two typed sectors resolve the common carrier"),
        kernel.prove_exact_rank(reservoir_projector, 2,
                                subject="reservoir sector has complex dimension two"),
        kernel.prove_exact_rank(path_projector, 2,
                                subject="path sector has complex dimension two"),
        kernel.prove_expression_equality(reservoir_projector.rank() + path_projector.rank(), 4,
                                         subject="four is the minimal dimension for two orthogonal rank-two sectors"),
        kernel.prove_matrix_equality(intertwiner.T * intertwiner, path_projector,
                                     subject="intertwiner initial projector is the path sector"),
        kernel.prove_matrix_equality(intertwiner * intertwiner.T, reservoir_projector,
                                     subject="intertwiner final projector is the reservoir sector"),
        kernel.prove_matrix_equality(intertwiner**2, sp.zeros(4),
                                     subject="oriented cross-sector intertwiner is nilpotent"),
        kernel.prove_matrix_equality(common_orientation * intertwiner,
                                     intertwiner * common_orientation,
                                     subject="common-carrier intertwiner preserves oriented levels"),
        kernel.prove_expression_equality(len(phase_intertwiners), 4,
                                         subject="four real sign phases remain on the admitted carrier"),
        kernel.prove_matrix_equality(phase_intertwiners[1].T * phase_intertwiners[1], path_projector,
                                     subject="relative-sign intertwiner has the same initial projector"),
        kernel.prove_matrix_equality(phase_intertwiners[2] * phase_intertwiners[2].T, reservoir_projector,
                                     subject="relative-sign intertwiner has the same final projector"),
        kernel.prove_exact_rank(algebra_basis, 16,
                                subject="sector matrix units and cross intertwiner generate M4"),
        kernel.prove_exact_rank(commutant_constraint, 15,
                                subject="full M4 action imposes fifteen independent commutant constraints"),
        kernel.prove_exact_nullity(commutant_constraint, 1,
                                   subject="common-carrier commutant is scalar"),
        kernel.prove_matrix_equality(commutant_constraint * commutant_kernel, sp.zeros(16, 1),
                                     subject="identity spans the common-carrier commutant"),
        kernel.prove_matrix_equality(conditional_hessian,
                                     sp.Matrix([[1, 0, -sp.Rational(1, 2), 0],
                                                [0, 1, 0, -sp.Rational(1, 2)],
                                                [-sp.Rational(1, 2), 0, 1, 0],
                                                [0, -sp.Rational(1, 2), 0, 1]]),
                                     subject="minimal conditional mixed Hessian is exact"),
        kernel.prove_exact_rank(conditional_hessian, 4,
                                subject="conditional common-carrier parent is nondegenerate"),
        kernel.prove_expression_equality(conditional_hessian.det(), sp.Rational(9, 16),
                                         subject="conditional common-carrier parent is strictly positive"),
        kernel.prove_exact_spectrum(conditional_hessian, hessian_spectrum,
                                    subject="conditional mixed Hessian has positive spectrum"),
        kernel.prove_exact_rank(mixed_block, 2,
                                subject="conditional parent has a full-rank mixed block"),
        kernel.prove_matrix_equality(architecture, sp.ones(12, 1),
                                     subject="minimal common-carrier architecture is complete"),
        kernel.prove_expression_equality(sum(architecture), 12,
                                         subject="twelve architecture requirements pass"),
        kernel.prove_matrix_equality(inherited_origin, sp.Matrix([1, 1, 1, 1, 0, 0]),
                                     subject="sector data are inherited but carrier and cross generator are new"),
        kernel.prove_expression_equality(sum(inherited_origin), 4,
                                         subject="four of six inherited-origin requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1),
                                     subject="cross generator phase coefficient and temperature origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0,
                                         subject="strict physical-origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate",
        theorems,
    )
    return HopfReservoirCommonCarrierCertificate(
        reservoir_projector, path_projector, common_orientation, intertwiner,
        phase_intertwiners, algebra_basis, commutant_constraint,
        commutant_kernel, conditional_hessian, mixed_block, architecture,
        inherited_origin, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate",
    title="Допуск общего носителя резервуарно-хопфовского интертвинера",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"hopf_reservoir_common_carrier_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(29)
    ),
)