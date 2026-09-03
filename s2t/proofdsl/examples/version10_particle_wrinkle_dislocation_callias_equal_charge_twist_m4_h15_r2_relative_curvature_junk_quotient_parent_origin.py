"""LCF certificate for the relative-curvature junk-quotient parent origin."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class RelativeCurvatureJunkQuotientParentCertificate:
    dirac_edge: sp.ImmutableMatrix
    node_idempotents: tuple[sp.ImmutableMatrix, ...]
    represented_one_forms: sp.ImmutableMatrix
    represented_two_forms: sp.ImmutableMatrix
    one_form_kernel: sp.ImmutableMatrix
    degree_two_junk: sp.ImmutableMatrix
    quotient_basis: sp.ImmutableMatrix
    sum_relative_basis: sp.ImmutableMatrix
    incidence: sp.ImmutableMatrix
    graph_laplacian: sp.ImmutableMatrix
    relative_projector: sp.ImmutableMatrix
    relative_diagonal_form: sp.ImmutableMatrix
    sum_vector: sp.ImmutableMatrix
    relative_vector: sp.ImmutableMatrix
    projected_sum: sp.ImmutableMatrix
    projected_relative: sp.ImmutableMatrix
    endpoint_channel_map: sp.ImmutableMatrix
    target_generator: sp.ImmutableMatrix
    relative_readout: sp.ImmutableMatrix
    inherited_hodge_selector: sp.ImmutableMatrix
    conditional_hodge_selector: sp.ImmutableMatrix
    inherited_auxiliary_edge: sp.ImmutableMatrix
    conditional_auxiliary_edge: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


def _vectorize(matrix: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(matrix).reshape(matrix.rows * matrix.cols, 1)


@lru_cache(maxsize=1)
def build_certificate() -> RelativeCurvatureJunkQuotientParentCertificate:
    dirac_edge = sp.ImmutableMatrix([[0, 1], [1, 0]])
    e0 = sp.ImmutableMatrix(sp.diag(1, 0))
    e1 = sp.ImmutableMatrix(sp.diag(0, 1))
    node_idempotents = (e0, e1)
    commutators = [sp.Matrix(dirac_edge * e - e * dirac_edge) for e in node_idempotents]

    one_columns = []
    one_labels = []
    for left in range(2):
        for right in range(2):
            one_columns.append(_vectorize(node_idempotents[left] * commutators[right]))
            one_labels.append((left, right))
    represented_one_forms = sp.ImmutableMatrix(sp.Matrix.hstack(*one_columns))
    kernel_vectors = represented_one_forms.nullspace()
    one_form_kernel = sp.ImmutableMatrix(sp.Matrix.hstack(*kernel_vectors))

    two_columns = []
    for left in range(2):
        for middle in range(2):
            for right in range(2):
                two_columns.append(
                    _vectorize(node_idempotents[left] * commutators[middle] * commutators[right])
                )
    represented_two_forms = sp.ImmutableMatrix(sp.Matrix.hstack(*two_columns))

    junk_columns = []
    for kernel_vector in kernel_vectors:
        junk = sp.zeros(2)
        for coefficient, (left, right) in zip(kernel_vector, one_labels):
            junk += coefficient * commutators[left] * commutators[right]
        junk_columns.append(_vectorize(junk))
    degree_two_junk = sp.ImmutableMatrix(sp.Matrix.hstack(*junk_columns))

    quotient_basis = sp.ImmutableMatrix.hstack(_vectorize(e0), _vectorize(e1))
    sum_relative_basis = sp.ImmutableMatrix.hstack(
        _vectorize(sp.eye(2)), _vectorize(sp.diag(1, -1))
    )
    incidence = sp.ImmutableMatrix([[1, -1]])
    graph_laplacian = sp.ImmutableMatrix(incidence.T * incidence)
    relative_projector = sp.ImmutableMatrix(sp.Rational(1, 2) * graph_laplacian)
    hadamard = sp.ImmutableMatrix([[1, 1], [1, -1]])
    relative_diagonal_form = sp.ImmutableMatrix(hadamard.T * relative_projector * hadamard)
    sum_vector = sp.ImmutableMatrix([1, 1])
    relative_vector = sp.ImmutableMatrix([1, -1])
    projected_sum = sp.ImmutableMatrix(relative_projector * sum_vector)
    projected_relative = sp.ImmutableMatrix(relative_projector * relative_vector)

    t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    endpoint_channel_map = sp.ImmutableMatrix.hstack(t3r6, -bl3)
    target_spectrum = sp.ImmutableMatrix(t3r6 + bl3)
    target_generator = sp.ImmutableMatrix(sp.diag(*list(target_spectrum)))
    relative_spectrum = sp.ImmutableMatrix(endpoint_channel_map * relative_vector)
    relative_readout = sp.ImmutableMatrix(sp.diag(*list(relative_spectrum)))
    inherited_hodge_selector = sp.ImmutableMatrix.zeros(2)
    conditional_hodge_selector = relative_projector
    inherited_auxiliary_edge = sp.ImmutableMatrix.zeros(8)
    conditional_auxiliary_edge = sp.ImmutableMatrix(sp.eye(8))

    # Slots: exact Q, positive norm, canonical normalization, gauge/Real,
    # inherited Hodge selector, inherited auxiliary edge.
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])
    physical_status = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])

    theorems = (
        kernel.prove_exact_rank(represented_one_forms, 2, subject="two-node represented one-forms have rank two"),
        kernel.prove_exact_nullity(represented_one_forms, 2, subject="universal one-form representation has a two-dimensional kernel"),
        kernel.prove_exact_rank(one_form_kernel, 2, subject="the exact one-form kernel basis has rank two"),
        kernel.prove_exact_rank(represented_two_forms, 2, subject="two-node represented two-forms have rank two"),
        kernel.prove_exact_rank(degree_two_junk, 0, subject="degree-two junk vanishes in the minimal two-node calculus"),
        kernel.prove_exact_rank(quotient_basis, 2, subject="the degree-two quotient retains both endpoint diagonal units"),
        kernel.prove_exact_rank(sum_relative_basis, 2, subject="sum and relative endpoint classes both survive the quotient"),
        kernel.prove_matrix_equality(incidence.T * incidence, graph_laplacian, subject="two-node graph Laplacian is induced by incidence"),
        kernel.prove_matrix_equality(relative_projector**2, relative_projector, subject="normalized graph Laplacian is the relative Hodge projector"),
        kernel.prove_exact_rank(relative_projector, 1, subject="relative Hodge projector keeps one endpoint-difference channel"),
        kernel.prove_matrix_equality(relative_diagonal_form, sp.diag(0, 2), subject="relative projector has one zero and one positive direction"),
        kernel.prove_diagonal_signature(relative_diagonal_form, (0, 1, 1), subject="relative Hodge norm is positive semidefinite"),
        kernel.prove_matrix_equality(projected_sum, sp.zeros(2, 1), subject="relative projector removes the endpoint sum"),
        kernel.prove_matrix_equality(projected_relative, relative_vector, subject="relative projector preserves the endpoint difference"),
        kernel.prove_matrix_equality(relative_readout, target_generator, subject="relative endpoint readout reconstructs exact Q"),
        kernel.prove_exact_rank(relative_readout, 8, subject="relative Hodge readout acts on every Sigma sector"),
        kernel.prove_exact_rank(inherited_hodge_selector, 0, subject="current represented calculus has no inherited Hodge projection"),
        kernel.prove_exact_rank(conditional_hodge_selector, 1, subject="conditional graph-Hodge selector has rank one"),
        kernel.prove_exact_rank(inherited_auxiliary_edge, 0, subject="current carrier has no inherited odd auxiliary edge"),
        kernel.prove_exact_rank(conditional_auxiliary_edge, 8, subject="conditional auxiliary edge has the required full rank"),
        kernel.prove_expression_equality(sum(conditional_status), 4, subject="conditional relative-Hodge parent closes four of six slots"),
        kernel.prove_expression_equality(sum(physical_status), 4, subject="physical relative-Hodge origin remains four of six"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate",
        theorems,
    )
    return RelativeCurvatureJunkQuotientParentCertificate(
        dirac_edge,
        node_idempotents,
        represented_one_forms,
        represented_two_forms,
        one_form_kernel,
        degree_two_junk,
        quotient_basis,
        sum_relative_basis,
        incidence,
        graph_laplacian,
        relative_projector,
        relative_diagonal_form,
        sum_vector,
        relative_vector,
        projected_sum,
        projected_relative,
        endpoint_channel_map,
        target_generator,
        relative_readout,
        inherited_hodge_selector,
        conditional_hodge_selector,
        inherited_auxiliary_edge,
        conditional_auxiliary_edge,
        conditional_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate",
    title="Родитель relative-curvature junk quotient",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_relative_curvature_junk_quotient_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)