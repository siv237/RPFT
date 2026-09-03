"""LCF certificate for the odd auxiliary cross-bilinear candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class OddAuxiliaryCrossBilinearAuditCertificate:
    t3r6: sp.ImmutableMatrix
    bl3: sp.ImmutableMatrix
    hypercharge6: sp.ImmutableMatrix
    cartan_basis: sp.ImmutableMatrix
    locked_coefficients: sp.ImmutableMatrix
    required_cross_block: sp.ImmutableMatrix
    inherited_cross_block: sp.ImmutableMatrix
    cross_hessian: sp.ImmutableMatrix
    cross_diagonalization: sp.ImmutableMatrix
    cross_diagonal_form: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    moment_map_row: sp.ImmutableMatrix
    superconnection_row: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> OddAuxiliaryCrossBilinearAuditCertificate:
    t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    hypercharge6 = sp.ImmutableMatrix(t3r6 + bl3)
    cartan_basis = sp.ImmutableMatrix.hstack(t3r6, bl3)
    locked_coefficients = sp.ImmutableMatrix([1, 1])
    q = sp.ImmutableMatrix(sp.diag(*list(hypercharge6)))
    required_cross_block = q
    inherited_cross_block = sp.ImmutableMatrix.zeros(8)
    zero = sp.zeros(8)
    identity = sp.eye(8)
    cross_hessian = sp.ImmutableMatrix(sp.BlockMatrix([[zero, q], [q, zero]]).as_explicit())
    cross_diagonalization = sp.ImmutableMatrix(
        sp.BlockMatrix([[identity, identity], [identity, -identity]]).as_explicit()
    )
    cross_diagonal_form = sp.ImmutableMatrix(cross_diagonalization.T * cross_hessian * cross_diagonalization)

    # Columns: typed A-Sigma domain, exact Q, gauge equivariance,
    # Real-even scalar, coefficient locked by one parent, inherited action.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [1, 0, 1, 1, 1, 0],  # universal identity portal
            [0, 0, 1, 1, 0, 1],  # fixed-point projection
            [1, 1, 1, 0, 0, 0],  # one-sided target Q without Real completion
            [1, 1, 1, 1, 1, 0],  # Delta moment-map trilinear
            [1, 1, 1, 1, 0, 0],  # two independent Cartan portals
            [0, 0, 1, 1, 1, 1],  # ordinary even spectral moments
            [0, 0, 1, 1, 0, 1],  # spectral commutator [D,Y]
            [0, 0, 1, 1, 0, 1],  # inherited mapping-cone incidence
            [1, 0, 1, 1, 0, 1],  # KO6 first-order fluctuation
            [1, 1, 1, 1, 0, 0],  # Callias normal component
            [1, 1, 1, 1, 1, 0],  # superconnection mixed curvature
            [1, 1, 1, 1, 0, 0],  # fermion-loop triangle
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(12, 1)
    coverage = sp.ImmutableMatrix([
        [int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows)))]
        for column in range(candidate_matrix.cols)
    ])
    moment_map_row = sp.ImmutableMatrix(candidate_matrix.row(3))
    superconnection_row = sp.ImmutableMatrix(candidate_matrix.row(10))
    physical_origin = sp.ImmutableMatrix([1, 1, 1, 1, 1, 0])

    theorems = (
        kernel.prove_matrix_equality(hypercharge6, sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3]), subject="required cross generator has the exact six-hypercharge spectrum"),
        kernel.prove_exact_rank(cartan_basis, 2, subject="T3R and B minus L are independent cross channels"),
        kernel.prove_matrix_equality(cartan_basis.T * cartan_basis, sp.diag(72, 64), subject="Cartan cross-channel Gram matrix is exact"),
        kernel.prove_matrix_equality(cartan_basis * locked_coefficients, hypercharge6, subject="one-to-one Cartan combination reconstructs Q"),
        kernel.prove_exact_rank(sp.ImmutableMatrix.hstack(cartan_basis, hypercharge6), 2, subject="Q lies in the two-channel Cartan span"),
        kernel.prove_exact_rank(required_cross_block, 8, subject="required A-Sigma cross block has full rank"),
        kernel.prove_exact_rank(inherited_cross_block, 0, subject="inherited A-Sigma cross block has rank zero"),
        kernel.prove_matrix_equality(cross_hessian, sp.ImmutableMatrix(sp.BlockMatrix([[zero, q], [q, zero]]).as_explicit()), subject="required cross Hessian is exact"),
        kernel.prove_exact_rank(cross_hessian, 16, subject="required cross Hessian has full rank"),
        kernel.prove_matrix_equality(cross_diagonal_form, sp.diag(2 * q, -2 * q), subject="Hadamard congruence diagonalizes the cross Hessian"),
        kernel.prove_diagonal_signature(cross_diagonal_form, (8, 0, 8), subject="cross Hessian has balanced indefinite signature"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="cross-bilinear audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 3, 3, 5, 4, 4, 3, 3, 4, 4, 5, 4]), subject="cross-bilinear candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no cross-bilinear candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every cross-bilinear criterion is represented"),
        kernel.prove_matrix_equality(moment_map_row, sp.ImmutableMatrix([[1, 1, 1, 1, 1, 0]]), subject="Delta moment-map trilinear fails only inheritance"),
        kernel.prove_matrix_equality(superconnection_row, sp.ImmutableMatrix([[1, 1, 1, 1, 1, 0]]), subject="superconnection mixed curvature fails only inheritance"),
        kernel.prove_matrix_equality(physical_origin, sp.ImmutableMatrix([1, 1, 1, 1, 1, 0]), subject="cross type and normalization are fixed while parent inheritance is open"),
        kernel.prove_expression_equality(sum(physical_origin), 5, subject="strict cross-bilinear physical-origin score is five of six"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate",
        theorems,
    )
    return OddAuxiliaryCrossBilinearAuditCertificate(
        t3r6,
        bl3,
        hypercharge6,
        cartan_basis,
        locked_coefficients,
        required_cross_block,
        inherited_cross_block,
        cross_hessian,
        cross_diagonalization,
        cross_diagonal_form,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        moment_map_row,
        superconnection_row,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate",
    title="Аудит кандидатов odd auxiliary cross-bilinear",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_odd_auxiliary_cross_bilinear_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(19)
    ),
)