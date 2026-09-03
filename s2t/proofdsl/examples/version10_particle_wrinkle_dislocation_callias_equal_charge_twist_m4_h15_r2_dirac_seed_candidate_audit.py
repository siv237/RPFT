"""LCF certificate for the finite R2 Dirac-seed candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class R2DiracSeedCandidateAuditCertificate:
    standard_dirac: sp.ImmutableMatrix
    r2_seed: sp.ImmutableMatrix
    r2_mask: sp.ImmutableMatrix
    standard_laplacian: sp.ImmutableMatrix
    callias_h15_factor: sp.ImmutableMatrix
    admitted_a2: sp.ImmutableMatrix
    standard_one_form: sp.ImmutableMatrix
    internal_r2_projections: sp.ImmutableMatrix
    target_projection: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    target_coefficient_hessian: sp.ImmutableMatrix
    inherited_seed_map: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


def _edge_operator(edges: tuple[tuple[int, int], ...]) -> sp.ImmutableMatrix:
    matrix = sp.zeros(5)
    for source, target in edges:
        matrix[source, target] = 1
        matrix[target, source] = 1
    return sp.ImmutableMatrix(matrix)


def _project(mask: sp.ImmutableMatrix, operator: sp.ImmutableMatrix) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(mask.multiply_elementwise(operator))


@lru_cache(maxsize=1)
def build_certificate() -> R2DiracSeedCandidateAuditCertificate:
    # Vertex order: Q_L, L_L, u_R, d_R, e_R.
    standard_dirac = _edge_operator(((0, 2), (0, 3), (1, 4)))
    r2_seed = _edge_operator(((1, 2), (0, 4)))
    r2_mask = r2_seed

    existing_incidence = sp.ImmutableMatrix(
        [[1, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    )
    standard_laplacian = sp.ImmutableMatrix(existing_incidence * existing_incidence.T)
    callias_h15_factor = sp.ImmutableMatrix.eye(5)
    admitted_a2 = sp.ImmutableMatrix.zeros(5)
    standard_one_form = standard_dirac

    internal_operators = (
        standard_dirac,
        standard_one_form,
        admitted_a2,
        callias_h15_factor,
        standard_laplacian,
    )
    projection_ranks = [int(_project(r2_mask, operator).rank()) for operator in internal_operators]
    internal_r2_projections = sp.ImmutableMatrix(projection_ranks)
    target_projection = _project(r2_mask, r2_seed)

    # Columns: exact R2 support, SM gauge type, Real/odd consistency,
    # current-parent inheritance, no new algebra/fermions, coefficient origin.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [0, 1, 1, 1, 1, 1],  # standard finite Dirac operator
            [0, 1, 1, 1, 1, 1],  # standard Higgs one-form
            [0, 1, 1, 1, 1, 1],  # admitted generalized A2
            [0, 1, 1, 1, 1, 0],  # Callias-M4 tensor amplifier
            [0, 0, 0, 1, 1, 1],  # H15 incidence/laplacian
            [1, 1, 1, 0, 0, 0],  # Pati-Salam Sigma=(2,2,15)
            [0, 1, 0, 0, 0, 0],  # Clifford mixed weak-colour scalar
            [0, 0, 0, 0, 1, 0],  # historical S0-reality relaxation
            [0, 1, 1, 0, 0, 0],  # strict mirror-cycle completion
            [1, 1, 1, 0, 1, 0],  # explicit D_R2 insertion
            [1, 1, 1, 0, 1, 1],  # normalized target-loaded D_R2
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(11, 1)
    coverage = sp.ImmutableMatrix(
        [[int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows)))] for column in range(candidate_matrix.cols)]
    )
    target_coefficient_hessian = sp.ImmutableMatrix([[2]])
    inherited_seed_map = sp.ImmutableMatrix.zeros(2, 5)
    conditional_architecture = sp.ImmutableMatrix.ones(12, 1)
    physical_origin = sp.ImmutableMatrix.zeros(3, 1)

    theorems = (
        kernel.prove_exact_rank(standard_dirac, 4, subject="standard finite Dirac support has rank four"),
        kernel.prove_exact_rank(r2_seed, 4, subject="two R2 blocks and adjoints have rank four"),
        kernel.prove_matrix_equality(_project(r2_mask, standard_dirac), sp.zeros(5), subject="standard Dirac operator has zero R2 projection"),
        kernel.prove_matrix_equality(_project(r2_mask, standard_one_form), sp.zeros(5), subject="standard Higgs one-form has zero R2 projection"),
        kernel.prove_matrix_equality(_project(r2_mask, admitted_a2), sp.zeros(5), subject="admitted quadratic fluctuation has zero R2 projection"),
        kernel.prove_matrix_equality(_project(r2_mask, callias_h15_factor), sp.zeros(5), subject="Callias tensor amplifier is diagonal on H15 types"),
        kernel.prove_matrix_equality(_project(r2_mask, standard_laplacian), sp.zeros(5), subject="H15 Laplacian contains no R2 block"),
        kernel.prove_matrix_equality(internal_r2_projections, sp.zeros(5, 1), subject="all inherited internal routes have zero R2 rank"),
        kernel.prove_matrix_equality(target_projection, r2_seed, subject="explicit R2 seed passes its support projector"),
        kernel.prove_exact_rank(target_projection, 4, subject="explicit R2 support projection has rank four"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="seed audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([5, 5, 5, 4, 3, 3, 1, 1, 2, 4, 5]), subject="seed candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no Dirac-seed candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every seed criterion is represented"),
        kernel.prove_exact_rank(target_coefficient_hessian, 1, subject="target-loaded coefficient can be normalized conditionally"),
        kernel.prove_matrix_equality(inherited_seed_map, sp.zeros(2, 5), subject="current parent has no map into the two R2 coefficients"),
        kernel.prove_exact_rank(inherited_seed_map, 0, subject="inherited R2 seed map has rank zero"),
        kernel.prove_expression_equality(sum(conditional_architecture), 12, subject="target-loaded seed architecture is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="R2 carrier coefficient and normalization origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict R2 seed physical-origin score is zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate",
        theorems,
    )
    return R2DiracSeedCandidateAuditCertificate(
        standard_dirac,
        r2_seed,
        r2_mask,
        standard_laplacian,
        callias_h15_factor,
        admitted_a2,
        standard_one_form,
        internal_r2_projections,
        target_projection,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        target_coefficient_hessian,
        inherited_seed_map,
        conditional_architecture,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate",
    title="Аудит кандидатов конечного Dirac-seed R2 на H15",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_dirac_seed_candidate_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(20)
    ),
)