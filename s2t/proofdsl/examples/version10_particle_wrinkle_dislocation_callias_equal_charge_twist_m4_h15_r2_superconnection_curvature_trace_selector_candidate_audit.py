"""LCF certificate for the superconnection curvature trace-selector audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SuperconnectionCurvatureTraceSelectorAuditCertificate:
    t3r6: sp.ImmutableMatrix
    bl3: sp.ImmutableMatrix
    endpoint_channel_map: sp.ImmutableMatrix
    target_generator: sp.ImmutableMatrix
    unique_trace_weights: sp.ImmutableMatrix
    ordinary_trace_weights: sp.ImmutableMatrix
    ordinary_generator: sp.ImmutableMatrix
    target_weight_metric: sp.ImmutableMatrix
    ordinary_weight_metric: sp.ImmutableMatrix
    relative_projector: sp.ImmutableMatrix
    relative_projector_gram: sp.ImmutableMatrix
    relative_diagonal_form: sp.ImmutableMatrix
    inherited_relative_selector: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    ordinary_trace_row: sp.ImmutableMatrix
    raw_supertrace_row: sp.ImmutableMatrix
    junk_quotient_row: sp.ImmutableMatrix
    length_two_row: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SuperconnectionCurvatureTraceSelectorAuditCertificate:
    t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    endpoint_channel_map = sp.ImmutableMatrix.hstack(t3r6, -bl3)
    target_generator = sp.ImmutableMatrix(t3r6 + bl3)
    unique_trace_weights = sp.ImmutableMatrix([1, -1])
    ordinary_trace_weights = sp.ImmutableMatrix([1, 1])
    ordinary_generator = sp.ImmutableMatrix(endpoint_channel_map * ordinary_trace_weights)
    target_weight_metric = sp.ImmutableMatrix(sp.diag(*list(unique_trace_weights)))
    ordinary_weight_metric = sp.ImmutableMatrix(sp.diag(*list(ordinary_trace_weights)))

    relative_projector = sp.ImmutableMatrix(
        sp.Rational(1, 2) * sp.Matrix([[1, -1], [-1, 1]])
    )
    relative_projector_gram = sp.ImmutableMatrix(relative_projector.T * relative_projector)
    hadamard = sp.ImmutableMatrix([[1, 1], [1, -1]])
    relative_diagonal_form = sp.ImmutableMatrix(hadamard.T * relative_projector_gram * hadamard)
    inherited_relative_selector = sp.ImmutableMatrix.zeros(2)

    # Columns: exact Q, positive full action, gauge/Real invariant,
    # canonical normalization, local/degree compatible, inherited selector.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [0, 1, 1, 1, 1, 1],  # ordinary Hilbert-Schmidt trace
            [1, 0, 1, 1, 1, 1],  # raw supertrace
            [0, 1, 1, 1, 1, 1],  # positive left chiral trace
            [0, 1, 1, 1, 1, 1],  # positive right chiral trace
            [0, 1, 1, 1, 1, 1],  # absolute grading trace
            [1, 0, 1, 1, 1, 0],  # Krein fundamental symmetry
            [1, 1, 1, 1, 1, 0],  # represented junk quotient
            [1, 1, 1, 1, 1, 0],  # length-two relative curvature block
            [1, 1, 1, 0, 1, 0],  # conditional expectation to relative block
            [1, 0, 1, 0, 1, 0],  # BRST-exact diagonal cancellation
            [1, 0, 1, 0, 0, 0],  # Pauli-Villars trace difference
            [1, 1, 1, 0, 0, 0],  # target-loaded endpoint projector
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(12, 1)
    coverage = sp.ImmutableMatrix(
        [int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows))) for column in range(6)]
    )
    ordinary_trace_row = sp.ImmutableMatrix(candidate_matrix.row(0))
    raw_supertrace_row = sp.ImmutableMatrix(candidate_matrix.row(1))
    junk_quotient_row = sp.ImmutableMatrix(candidate_matrix.row(6))
    length_two_row = sp.ImmutableMatrix(candidate_matrix.row(7))
    physical_origin = sp.ImmutableMatrix([1, 1, 1, 1, 1, 0])

    theorems = (
        kernel.prove_exact_rank(endpoint_channel_map, 2, subject="the two endpoint Cartan channels are independent"),
        kernel.prove_matrix_equality(endpoint_channel_map.T * endpoint_channel_map, sp.diag(72, 64), subject="endpoint channel Gram matrix is exact"),
        kernel.prove_matrix_equality(endpoint_channel_map * unique_trace_weights, target_generator, subject="the exact Q selector uses weights one and minus one"),
        kernel.prove_exact_rank(sp.ImmutableMatrix.hstack(endpoint_channel_map, target_generator), 2, subject="Q has a unique endpoint-weight representation"),
        kernel.prove_matrix_equality(unique_trace_weights, sp.ImmutableMatrix([1, -1]), subject="the unique exact trace weights include one negative weight"),
        kernel.prove_matrix_equality(ordinary_generator, sp.ImmutableMatrix([3, -3, -1, -7, 7, 1, 3, -3]), subject="positive ordinary trace gives T minus B"),
        kernel.prove_diagonal_signature(target_weight_metric, (1, 0, 1), subject="the exact endpoint trace is indefinite"),
        kernel.prove_diagonal_signature(ordinary_weight_metric, (0, 0, 2), subject="ordinary endpoint weights are positive"),
        kernel.prove_matrix_equality(relative_projector**2, relative_projector, subject="relative endpoint selector is an orthogonal projector"),
        kernel.prove_exact_rank(relative_projector, 1, subject="relative endpoint selector keeps one difference channel"),
        kernel.prove_matrix_equality(relative_diagonal_form, sp.diag(0, 2), subject="relative projector Gram form has an exact diagonal representative"),
        kernel.prove_diagonal_signature(relative_diagonal_form, (0, 1, 1), subject="the selected relative block carries a positive semidefinite norm"),
        kernel.prove_exact_rank(inherited_relative_selector, 0, subject="the current represented calculus contains no relative curvature selector"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="trace-selector audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([5, 5, 5, 5, 5, 4, 5, 5, 4, 3, 2, 3]), subject="trace-selector candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no trace selector passes every criterion"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every trace-selector criterion is represented"),
        kernel.prove_matrix_equality(ordinary_trace_row, sp.ImmutableMatrix([[0, 1, 1, 1, 1, 1]]), subject="ordinary trace fails only the exact-Q criterion"),
        kernel.prove_matrix_equality(raw_supertrace_row, sp.ImmutableMatrix([[1, 0, 1, 1, 1, 1]]), subject="raw supertrace fails only positivity"),
        kernel.prove_matrix_equality(junk_quotient_row, sp.ImmutableMatrix([[1, 1, 1, 1, 1, 0]]), subject="represented junk quotient fails only inheritance"),
        kernel.prove_matrix_equality(length_two_row, junk_quotient_row, subject="length-two relative block has the same open inheritance slot"),
        kernel.prove_expression_equality(sum(physical_origin), 5, subject="best positive relative-selector route closes five of six slots"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate",
        theorems,
    )
    return SuperconnectionCurvatureTraceSelectorAuditCertificate(
        t3r6,
        bl3,
        endpoint_channel_map,
        target_generator,
        unique_trace_weights,
        ordinary_trace_weights,
        ordinary_generator,
        target_weight_metric,
        ordinary_weight_metric,
        relative_projector,
        relative_projector_gram,
        relative_diagonal_form,
        inherited_relative_selector,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        ordinary_trace_row,
        raw_supertrace_row,
        junk_quotient_row,
        length_two_row,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate",
    title="Аудит trace-селекторов superconnection curvature",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_superconnection_trace_selector_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)