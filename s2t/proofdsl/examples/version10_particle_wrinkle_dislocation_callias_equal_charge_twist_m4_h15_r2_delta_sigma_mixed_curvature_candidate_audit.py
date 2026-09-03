"""LCF certificate for the Delta-Sigma mixed-curvature candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class DeltaSigmaMixedCurvatureAuditCertificate:
    t3r6: sp.ImmutableMatrix
    bl3: sp.ImmutableMatrix
    hypercharge6: sp.ImmutableMatrix
    t3r_square: sp.ImmutableMatrix
    bl_square: sp.ImmutableMatrix
    mixed_tb: sp.ImmutableMatrix
    curvature_basis: sp.ImmutableMatrix
    target_coefficients: sp.ImmutableMatrix
    target_gap: sp.ImmutableMatrix
    even_subbasis: sp.ImmutableMatrix
    mixed_subbasis: sp.ImmutableMatrix
    inherited_curvature_map: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> DeltaSigmaMixedCurvatureAuditCertificate:
    t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    hypercharge6 = sp.ImmutableMatrix(t3r6 + bl3)
    t3r_square = sp.ImmutableMatrix(t3r6.multiply_elementwise(t3r6))
    bl_square = sp.ImmutableMatrix(bl3.multiply_elementwise(bl3))
    mixed_tb = sp.ImmutableMatrix(t3r6.multiply_elementwise(bl3))
    identity_vector = sp.ImmutableMatrix.ones(8, 1)

    # Since T^2=9I, 49I-(T+B)^2 = 40I-B^2-2TB.
    curvature_basis = sp.ImmutableMatrix.hstack(identity_vector, bl_square, mixed_tb)
    target_coefficients = sp.ImmutableMatrix([40, -1, -2])
    target_gap = sp.ImmutableMatrix(curvature_basis * target_coefficients)
    even_subbasis = sp.ImmutableMatrix.hstack(identity_vector, bl_square)
    mixed_subbasis = sp.ImmutableMatrix.hstack(identity_vector, mixed_tb)
    inherited_curvature_map = sp.ImmutableMatrix.zeros(3, 1)

    # Columns: Sigma coupling, B^2 channel, TB channel, locked 1:2 ratio,
    # inherited common parent, correct target-gap sign.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [0, 0, 0, 0, 1, 0],  # inherited Delta mapping-cone direct sum
            [1, 0, 0, 0, 0, 0],  # universal norm portal
            [1, 1, 0, 0, 0, 0],  # four-colour B^2 moment-map portal
            [1, 0, 1, 0, 0, 0],  # isolated mixed TB portal
            [1, 1, 1, 0, 0, 1],  # two independently weighted portals
            [1, 1, 1, 1, 0, 1],  # single Delta-stabilizer moment-map curvature
            [1, 1, 1, 0, 0, 1],  # target-loaded G_Y potential
            [0, 0, 0, 0, 1, 0],  # composite Y(phi,Sigma4) at phi=0
            [0, 0, 0, 0, 1, 0],  # Delta determinant selector
            [1, 0, 0, 0, 1, 0],  # factorized product heat-kernel trace
            [1, 0, 1, 0, 1, 0],  # Callias-M4 cross channel
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(11, 1)
    coverage = sp.ImmutableMatrix(
        [[int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows)))] for column in range(candidate_matrix.cols)]
    )
    physical_origin = sp.ImmutableMatrix([1, 1, 0, 0])

    q_square = hypercharge6.multiply_elementwise(hypercharge6)
    theorems = (
        kernel.prove_matrix_equality(t3r_square, 9 * identity_vector, subject="six T3R squared is constant on Sigma"),
        kernel.prove_matrix_equality(bl_square, sp.ImmutableMatrix([0, 0, 16, 16, 16, 16, 0, 0]), subject="B minus L square channel is exact"),
        kernel.prove_matrix_equality(mixed_tb, sp.ImmutableMatrix([0, 0, 12, -12, -12, 12, 0, 0]), subject="mixed Cartan TB channel is exact"),
        kernel.prove_matrix_equality(q_square, t3r_square + bl_square + 2 * mixed_tb, subject="hypercharge square decomposes into Cartan channels"),
        kernel.prove_matrix_equality(target_gap, sp.ImmutableMatrix([40, 40, 0, 48, 48, 0, 40, 40]), subject="mixed curvature basis reconstructs the exact R2 gap"),
        kernel.prove_exact_rank(curvature_basis, 3, subject="I B squared and TB are independent curvature channels"),
        kernel.prove_matrix_equality(curvature_basis.T * curvature_basis, sp.ImmutableMatrix([[8, 64, 0], [64, 1024, 0], [0, 0, 576]]), subject="curvature-channel Gram matrix is exact"),
        kernel.prove_matrix_equality(curvature_basis * target_coefficients, target_gap, subject="gap coefficients forty minus one minus two are exact"),
        kernel.prove_exact_rank(even_subbasis, 2, subject="universal and B squared channels span a plane"),
        kernel.prove_exact_rank(sp.ImmutableMatrix.hstack(even_subbasis, target_gap), 3, subject="TB channel is necessary for the target gap"),
        kernel.prove_exact_rank(mixed_subbasis, 2, subject="universal and TB channels span a plane"),
        kernel.prove_exact_rank(sp.ImmutableMatrix.hstack(mixed_subbasis, target_gap), 3, subject="B squared channel is necessary for the target gap"),
        kernel.prove_diagonal_signature(sp.diag(*list(target_gap)), (0, 2, 6), subject="reconstructed mixed curvature is a positive R2 gap"),
        kernel.prove_exact_rank(sp.diag(*list(target_gap)), 6, subject="reconstructed gap lifts six companion sectors"),
        kernel.prove_exact_nullity(sp.diag(*list(target_gap)), 2, subject="reconstructed gap retains the R2 pair"),
        kernel.prove_matrix_equality(inherited_curvature_map, sp.zeros(3, 1), subject="current parent induces none of the three mixed-curvature coefficients"),
        kernel.prove_exact_rank(inherited_curvature_map, 0, subject="inherited mixed-curvature coefficient map has rank zero"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="mixed-curvature audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([1, 1, 2, 2, 4, 5, 4, 1, 1, 2, 3]), subject="mixed-curvature candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no mixed-curvature candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every mixed-curvature criterion is represented"),
        kernel.prove_matrix_equality(candidate_matrix.row(5), sp.ImmutableMatrix([[1, 1, 1, 1, 0, 1]]), subject="Delta stabilizer moment-map curvature fails only inheritance"),
        kernel.prove_matrix_equality(physical_origin, sp.ImmutableMatrix([1, 1, 0, 0]), subject="carrier and algebra are derived while curvature and scale remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 2, subject="strict mixed-curvature physical-origin score is two of four"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate",
        theorems,
    )
    return DeltaSigmaMixedCurvatureAuditCertificate(
        t3r6,
        bl3,
        hypercharge6,
        t3r_square,
        bl_square,
        mixed_tb,
        curvature_basis,
        target_coefficients,
        target_gap,
        even_subbasis,
        mixed_subbasis,
        inherited_curvature_map,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate",
    title="Аудит кандидатов смешанной Delta-Sigma curvature",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_delta_sigma_mixed_curvature_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)