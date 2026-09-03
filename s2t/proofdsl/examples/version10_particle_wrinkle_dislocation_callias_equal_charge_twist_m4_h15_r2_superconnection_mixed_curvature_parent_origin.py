"""LCF certificate for the superconnection mixed-curvature parent origin."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SuperconnectionMixedCurvatureParentCertificate:
    t3r6: sp.ImmutableMatrix
    bl3: sp.ImmutableMatrix
    left_endpoint_moment: sp.ImmutableMatrix
    right_endpoint_moment: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    ordinary_generator: sp.ImmutableMatrix
    grading: sp.ImmutableMatrix
    background_curvature: sp.ImmutableMatrix
    unit_odd_field: sp.ImmutableMatrix
    oddness_residual: sp.ImmutableMatrix
    graded_polarization: sp.ImmutableMatrix
    ordinary_polarization: sp.ImmutableMatrix
    polarization_defect: sp.ImmutableMatrix
    graded_trace_metric: sp.ImmutableMatrix
    ordinary_trace_metric: sp.ImmutableMatrix
    inherited_auxiliary_embedding: sp.ImmutableMatrix
    conditional_auxiliary_embedding: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


def _odd_field(vector: sp.MatrixBase) -> sp.ImmutableMatrix:
    diagonal = sp.diag(*list(vector))
    zero = sp.zeros(8)
    return sp.ImmutableMatrix(sp.BlockMatrix([[zero, diagonal], [diagonal, zero]]).as_explicit())


@lru_cache(maxsize=1)
def build_certificate() -> SuperconnectionMixedCurvatureParentCertificate:
    t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    left_endpoint_moment = sp.ImmutableMatrix(sp.diag(*list(t3r6)))
    right_endpoint_moment = sp.ImmutableMatrix(sp.diag(*list(-bl3)))
    hypercharge_generator = sp.ImmutableMatrix(left_endpoint_moment - right_endpoint_moment)
    ordinary_generator = sp.ImmutableMatrix(left_endpoint_moment + right_endpoint_moment)

    identity8 = sp.eye(8)
    zero8 = sp.zeros(8)
    grading = sp.ImmutableMatrix(sp.diag(identity8, -identity8))
    background_curvature = sp.ImmutableMatrix(sp.diag(left_endpoint_moment, right_endpoint_moment))
    unit_odd_field = _odd_field(sp.ones(8, 1))
    oddness_residual = sp.ImmutableMatrix(grading * unit_odd_field + unit_odd_field * grading)

    graded_entries = []
    ordinary_entries = []
    basis_fields = []
    for index in range(8):
        vector = sp.zeros(8, 1)
        vector[index] = 1
        basis_fields.append(_odd_field(vector))
    for row in range(8):
        graded_row = []
        ordinary_row = []
        for column in range(8):
            polarization = (
                basis_fields[row] * basis_fields[column]
                + basis_fields[column] * basis_fields[row]
            ) / 2
            graded_row.append(sp.trace(grading * background_curvature * polarization))
            ordinary_row.append(sp.trace(background_curvature * polarization))
        graded_entries.append(graded_row)
        ordinary_entries.append(ordinary_row)
    graded_polarization = sp.ImmutableMatrix(graded_entries)
    ordinary_polarization = sp.ImmutableMatrix(ordinary_entries)
    polarization_defect = sp.ImmutableMatrix(graded_polarization - ordinary_polarization)

    graded_trace_metric = grading
    ordinary_trace_metric = sp.ImmutableMatrix(sp.eye(16))
    inherited_auxiliary_embedding = sp.ImmutableMatrix.zeros(8)
    conditional_auxiliary_embedding = sp.ImmutableMatrix(sp.eye(8))

    # Slots: exact Q, odd/Real typing, canonical coefficient, inherited grading,
    # positive full trace, inherited A_Sigma support.
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])
    physical_status = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])

    expected_q = sp.diag(3, -3, 7, 1, -1, -7, 3, -3)
    expected_ordinary = sp.diag(3, -3, -1, -7, 7, 1, 3, -3)
    theorems = (
        kernel.prove_matrix_equality(hypercharge_generator, expected_q, subject="graded endpoint difference reconstructs six-hypercharge"),
        kernel.prove_exact_rank(hypercharge_generator, 8, subject="graded superconnection cross generator has full rank"),
        kernel.prove_matrix_equality(ordinary_generator, expected_ordinary, subject="ordinary endpoint sum has the wrong Cartan signs"),
        kernel.prove_matrix_equality(grading * background_curvature - background_curvature * grading, sp.zeros(16), subject="Delta background curvature is even"),
        kernel.prove_matrix_equality(unit_odd_field.T, unit_odd_field, subject="the common off-diagonal field is Real self-adjoint"),
        kernel.prove_matrix_equality(oddness_residual, sp.zeros(16), subject="the common off-diagonal field is grading odd"),
        kernel.prove_matrix_equality(graded_polarization, hypercharge_generator, subject="graded curvature polarization gives exactly A transpose Q Sigma"),
        kernel.prove_exact_rank(graded_polarization, 8, subject="graded mixed-curvature pairing covers every Sigma sector"),
        kernel.prove_matrix_equality(ordinary_polarization, ordinary_generator, subject="positive ordinary trace gives the endpoint sum instead"),
        kernel.prove_matrix_equality(polarization_defect, 2 * sp.diag(*list(bl3)), subject="ordinary and graded traces differ by the full B minus L channel"),
        kernel.prove_exact_rank(polarization_defect, 4, subject="the positive-trace defect affects four Sigma sectors"),
        kernel.prove_diagonal_signature(graded_trace_metric, (8, 0, 8), subject="the exact graded trace pairing is indefinite"),
        kernel.prove_diagonal_signature(ordinary_trace_metric, (0, 0, 16), subject="the Hilbert-Schmidt trace pairing is positive definite"),
        kernel.prove_exact_rank(inherited_auxiliary_embedding, 0, subject="current superconnection has no inherited A-Sigma arrow"),
        kernel.prove_exact_rank(conditional_auxiliary_embedding, 8, subject="the conditional odd arrow supplies the full required support"),
        kernel.prove_matrix_equality(graded_polarization - hypercharge_generator, sp.zeros(8), subject="no independent Cartan coefficient remains in graded polarization"),
        kernel.prove_matrix_equality(ordinary_polarization - hypercharge_generator, -2 * sp.diag(*list(bl3)), subject="positive ordinary trace cannot replace the graded selector"),
        kernel.prove_expression_equality(sum(conditional_status), 4, subject="conditional superconnection closes four of six origin slots"),
        kernel.prove_expression_equality(sum(physical_status), 4, subject="physical superconnection origin remains four of six"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate",
        theorems,
    )
    return SuperconnectionMixedCurvatureParentCertificate(
        t3r6,
        bl3,
        left_endpoint_moment,
        right_endpoint_moment,
        hypercharge_generator,
        ordinary_generator,
        grading,
        background_curvature,
        unit_odd_field,
        oddness_residual,
        graded_polarization,
        ordinary_polarization,
        polarization_defect,
        graded_trace_metric,
        ordinary_trace_metric,
        inherited_auxiliary_embedding,
        conditional_auxiliary_embedding,
        conditional_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate",
    title="Родитель mixed superconnection curvature",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_superconnection_mixed_curvature_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(19)
    ),
)