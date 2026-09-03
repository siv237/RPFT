"""LCF certificate for the cell-incidence tachyonic-sign parent-origin gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CellIncidenceTachyonicSignCertificate:
    incidence: sp.ImmutableMatrix
    reversed_incidence: sp.ImmutableMatrix
    laplacian: sp.ImmutableMatrix
    reversed_laplacian: sp.ImmutableMatrix
    positive_weight_laplacian: sp.ImmutableMatrix
    adjacency: sp.ImmutableMatrix
    relative_mode: sp.ImmutableMatrix
    stable_auxiliary_hessian: sp.ImmutableMatrix
    stable_schur_complement: sp.Expr
    supercritical_auxiliary_hessian: sp.ImmutableMatrix
    supercritical_schur_complement: sp.Expr
    fermion_vacuum_curvature: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    inherited_derived_negative_seed: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CellIncidenceTachyonicSignCertificate:
    incidence = sp.ImmutableMatrix([[-1], [1]])
    reversed_incidence = -incidence
    laplacian = sp.ImmutableMatrix(incidence * incidence.T)
    reversed_laplacian = sp.ImmutableMatrix(reversed_incidence * reversed_incidence.T)
    positive_weight_laplacian = sp.ImmutableMatrix(3 * laplacian)
    adjacency = sp.ImmutableMatrix([[0, 1], [1, 0]])
    relative_mode = sp.ImmutableMatrix([1, -1])

    # A stable auxiliary field cannot make the Schur complement negative.
    stable_auxiliary_hessian = sp.ImmutableMatrix([[2, 1], [1, 2]])
    stable_schur_complement = sp.simplify(
        stable_auxiliary_hessian[0, 0]
        - stable_auxiliary_hessian[0, 1] ** 2 / stable_auxiliary_hessian[1, 1]
    )

    # A supercritical mixing can do so only because its quadratic parent is
    # already indefinite; a quartic term may bound the full potential later.
    supercritical_auxiliary_hessian = sp.ImmutableMatrix([[2, 2], [2, 1]])
    supercritical_schur_complement = sp.simplify(
        supercritical_auxiliary_hessian[0, 0]
        - supercritical_auxiliary_hessian[0, 1] ** 2
        / supercritical_auxiliary_hessian[1, 1]
    )

    x = sp.symbols("x", real=True)
    fermion_vacuum_energy = -2 * sp.sqrt(1 + x**2)
    fermion_vacuum_curvature = sp.simplify(sp.diff(fermion_vacuum_energy, x, 2).subs(x, 0))

    # Columns: correct relative-incidence type, inherited carrier/operator,
    # actual negative mode, bounded nonlinear completion, parent-derived
    # coefficient without target loading, phase/orientation compatibility.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 1, 1, 1],  # positive incidence stiffness
        [1, 1, 0, 1, 1, 1],  # orientation reversal B -> -B
        [1, 1, 0, 1, 1, 1],  # positive edge reweighting
        [1, 1, 1, 1, 0, 1],  # adjacency quadratic form
        [1, 1, 0, 0, 1, 1],  # antisymmetric boundary form
        [1, 0, 0, 1, 1, 1],  # stable auxiliary Schur complement
        [1, 0, 1, 1, 0, 1],  # supercritical auxiliary mixing
        [1, 0, 1, 1, 1, 1],  # fermionic determinant susceptibility
        [1, 0, 1, 1, 1, 1],  # Callias sign-changing profile
        [1, 0, 1, 1, 0, 0],  # real Higgs rank-change portal
        [0, 1, 1, 1, 1, 0],  # negative common mode of the wrong type
        [1, 1, 1, 1, 0, 1],  # target-loaded minus Laplacian
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    inherited_derived_negative_seed = sp.ImmutableMatrix([
        candidate_matrix[i, 0]
        * candidate_matrix[i, 1]
        * candidate_matrix[i, 2]
        * candidate_matrix[i, 4]
        for i in range(candidate_matrix.rows)
    ])
    audit_coverage = sp.ImmutableMatrix.ones(12, 1)
    physical_origin = sp.ImmutableMatrix.zeros(4, 1)

    theorems = (
        kernel.prove_matrix_equality(incidence, sp.Matrix([[-1], [1]]), subject="minimal oriented cell incidence"),
        kernel.prove_matrix_equality(laplacian, sp.Matrix([[1, -1], [-1, 1]]), subject="minimal incidence Laplacian"),
        kernel.prove_exact_spectrum(laplacian, {sp.Integer(0): 1, sp.Integer(2): 1}, subject="incidence stiffness is nonnegative"),
        kernel.prove_matrix_equality(reversed_laplacian, laplacian, subject="orientation reversal leaves the Laplacian unchanged"),
        kernel.prove_exact_spectrum(positive_weight_laplacian, {sp.Integer(0): 1, sp.Integer(6): 1}, subject="positive edge weight preserves nonnegative sign"),
        kernel.prove_exact_spectrum(adjacency, {sp.Integer(-1): 1, sp.Integer(1): 1}, subject="adjacency has a conditional negative relative mode"),
        kernel.prove_matrix_equality(adjacency * relative_mode, -relative_mode, subject="relative cell mode is the negative adjacency eigenvector"),
        kernel.prove_exact_spectrum(stable_auxiliary_hessian, {sp.Integer(1): 1, sp.Integer(3): 1}, subject="stable auxiliary parent is positive definite"),
        kernel.prove_expression_equality(stable_schur_complement, sp.Rational(3, 2), subject="stable auxiliary Schur complement remains positive"),
        kernel.prove_expression_equality(stable_auxiliary_hessian.det(), 3, subject="stable auxiliary parent determinant is positive"),
        kernel.prove_expression_equality(supercritical_auxiliary_hessian.det(), -2, subject="supercritical auxiliary parent is already indefinite"),
        kernel.prove_exact_spectrum(supercritical_auxiliary_hessian, {(sp.Integer(3) - sp.sqrt(17)) / 2: 1, (sp.Integer(3) + sp.sqrt(17)) / 2: 1}, subject="supercritical parent contains one negative eigenvalue"),
        kernel.prove_expression_equality(supercritical_schur_complement, -2, subject="supercritical mixing induces a negative effective mode"),
        kernel.prove_expression_equality(fermion_vacuum_curvature, -2, subject="fermionic determinant has canonical negative quadratic susceptibility"),
        kernel.prove_expression_equality(candidate_matrix.rows, 12, subject="twelve tachyonic-sign mechanisms are audited"),
        kernel.prove_expression_equality(candidate_matrix.cols, 6, subject="six independent sign-origin criteria are used"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="tachyonic-sign candidate matrix has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([5, 5, 5, 5, 4, 4, 4, 5, 5, 3, 4, 5]), subject="tachyonic-sign candidate scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="best sign candidates remain incomplete"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no tachyonic-sign candidate passes the complete contract"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict tachyonic-sign pass count is zero"),
        kernel.prove_matrix_equality(inherited_derived_negative_seed, sp.zeros(12, 1), subject="no inherited negative incidence mode has a parent-derived coefficient"),
        kernel.prove_expression_equality(sum(inherited_derived_negative_seed), 0, subject="strict inherited derived negative seed count is zero"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(12, 1), subject="all twelve sign mechanisms are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 12, subject="tachyonic-sign audit coverage is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1), subject="fermion carrier coupling threshold and normalization origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical sign-origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate",
        theorems,
    )
    return CellIncidenceTachyonicSignCertificate(
        incidence, reversed_incidence, laplacian, reversed_laplacian,
        positive_weight_laplacian, adjacency, relative_mode,
        stable_auxiliary_hessian, stable_schur_complement,
        supercritical_auxiliary_hessian, supercritical_schur_complement,
        fermion_vacuum_curvature, candidate_matrix, score_vector, pass_vector,
        inherited_derived_negative_seed, audit_coverage, physical_origin,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate",
    title="Родитель тахионного знака клеточной incidence-моды",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"m4_cell_incidence_tachyonic_sign_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(27)
    ),
)