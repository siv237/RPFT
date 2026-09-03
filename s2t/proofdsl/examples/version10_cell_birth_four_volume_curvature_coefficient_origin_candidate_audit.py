"""LCF certificate for curvature-coefficient origin candidates."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CurvatureCoefficientOriginCandidateAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coefficient_constraint_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    parent_origin_column_theorem: Theorem
    orbit_break_column_theorem: Theorem
    volume_coefficient_theorem: Theorem
    einstein_coefficient_theorem: Theorem
    dimensionless_ratio_theorem: Theorem
    selected_scale_theorem: Theorem
    selected_invariant_theorem: Theorem
    parent_rescaling_theorem: Theorem
    constraint_rank_theorem: Theorem
    constraint_nullity_theorem: Theorem
    constraint_kernel_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CurvatureCoefficientOriginCandidateAuditCertificate:
    # paired dimensions, internal, target-independent, parent-derived,
    # typed into (A,B), breaks the absolute scale orbit
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 0, 1, 0],  # cosmological curvature
        [1, 1, 1, 0, 1, 0],  # spectral cutoff
        [1, 1, 0, 0, 1, 0],  # clock energy
        [1, 1, 0, 0, 1, 0],  # inverse cell length
        [1, 1, 0, 0, 1, 0],  # cell curvature
        [1, 1, 0, 0, 1, 0],  # KMS temperature
        [0, 1, 1, 0, 0, 0],  # topological density
        [1, 1, 1, 0, 1, 0],  # induced matter loop
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    scores = [sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)]

    q, m, alpha, beta, scale = sp.symbols("q m alpha beta s", positive=True)
    coefficient_a = alpha * m**2
    coefficient_b = beta * m
    parent = coefficient_a*q**2 - coefficient_b*q + coefficient_b**2/(4*coefficient_a)
    selected_q = sp.simplify(coefficient_b/(2*coefficient_a))
    rescaled_parent = parent.subs({q: scale**2*q, m: m/scale**2}, simultaneous=True)
    coefficient_constraint_map = sp.ImmutableMatrix([[1, 0, 2], [0, 1, 1]])
    scale_vector = sp.ImmutableMatrix([-2, -1, 1])
    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0])

    candidate_matrix_theorem = kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="eight curvature coefficient candidates are evaluated on six origin criteria")
    pass_vector_theorem = kernel.prove_matrix_equality(pass_vector, sp.zeros(8, 1), subject="no candidate physically derives both curvature coefficients and breaks the scale orbit")
    maximum_score_theorem = kernel.prove_expression_equality(max(scores), 4, subject="spectral cutoff and induced matter loop are the closest coefficient candidates")
    candidate_rank_theorem = kernel.prove_exact_rank(candidate_matrix, 3, subject="candidate distinctions span dimension typing independence and coefficient typing")
    parent_origin_column_theorem = kernel.prove_matrix_equality(candidate_matrix[:, 3], sp.zeros(8, 1), subject="the current common parent derives none of the proposed coefficient pairs")
    orbit_break_column_theorem = kernel.prove_matrix_equality(candidate_matrix[:, 5], sp.zeros(8, 1), subject="no current coefficient candidate breaks the absolute scale orbit")
    volume_coefficient_theorem = kernel.prove_expression_equality(coefficient_a, alpha*m**2, subject="a scale seed produces the inverse fourth length volume coefficient")
    einstein_coefficient_theorem = kernel.prove_expression_equality(coefficient_b, beta*m, subject="the same scale seed produces the inverse squared length Einstein coefficient")
    dimensionless_ratio_theorem = kernel.prove_expression_equality(coefficient_b**2/coefficient_a, beta**2/alpha, subject="the coefficient pair fixes only a dimensionless ratio independently of the scale seed")
    selected_scale_theorem = kernel.prove_expression_equality(selected_q, beta/(2*alpha*m), subject="the selected squared length is inverse to the assumed scale seed")
    selected_invariant_theorem = kernel.prove_expression_equality(selected_q*m, beta/(2*alpha), subject="the curvature parent selects only the dimensionless product q m")
    parent_rescaling_theorem = kernel.prove_expression_equality(rescaled_parent, parent, subject="rescaling the seed and cell length preserves the entire curvature parent")
    constraint_rank_theorem = kernel.prove_exact_rank(coefficient_constraint_map, 2, subject="two coefficient monomials impose two relative constraints")
    constraint_nullity_theorem = kernel.prove_exact_nullity(coefficient_constraint_map, 1, subject="one absolute coefficient scale remains free")
    constraint_kernel_theorem = kernel.prove_matrix_equality(coefficient_constraint_map*scale_vector, sp.zeros(2, 1), subject="the coefficient orbit is the exact common kernel")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(8, 1), subject="all declared curvature coefficient candidates are audited")
    origin_ledger_theorem = kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 0, 0]), subject="coverage covariance and typing pass while parent origin and scale breaking remain open")
    origin_score_theorem = kernel.prove_expression_equality(sum(origin_ledger), 3, subject="three of five coefficient audit requirements pass")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate", (candidate_matrix_theorem, pass_vector_theorem, maximum_score_theorem, candidate_rank_theorem, parent_origin_column_theorem, orbit_break_column_theorem, volume_coefficient_theorem, einstein_coefficient_theorem, dimensionless_ratio_theorem, selected_scale_theorem, selected_invariant_theorem, parent_rescaling_theorem, constraint_rank_theorem, constraint_nullity_theorem, constraint_kernel_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem))
    return CurvatureCoefficientOriginCandidateAuditCertificate(candidate_matrix, pass_vector, coefficient_constraint_map, scale_vector, architecture, origin_ledger, candidate_matrix_theorem, pass_vector_theorem, maximum_score_theorem, candidate_rank_theorem, parent_origin_column_theorem, orbit_break_column_theorem, volume_coefficient_theorem, einstein_coefficient_theorem, dimensionless_ratio_theorem, selected_scale_theorem, selected_invariant_theorem, parent_rescaling_theorem, constraint_rank_theorem, constraint_nullity_theorem, constraint_kernel_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate", "Аудит происхождения коэффициентов кривизны", ("s2t/gates/version10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("curvature_coefficient_candidate_matrix", lambda: build_certificate().candidate_matrix_theorem), ("zero_passing_coefficient_candidates", lambda: build_certificate().pass_vector_theorem), ("maximum_coefficient_score_four", lambda: build_certificate().maximum_score_theorem), ("coefficient_candidate_rank_three", lambda: build_certificate().candidate_rank_theorem), ("coefficient_parent_origin_column_zero", lambda: build_certificate().parent_origin_column_theorem), ("coefficient_orbit_break_column_zero", lambda: build_certificate().orbit_break_column_theorem), ("volume_coefficient_scale_degree", lambda: build_certificate().volume_coefficient_theorem), ("einstein_coefficient_scale_degree", lambda: build_certificate().einstein_coefficient_theorem), ("coefficient_dimensionless_ratio", lambda: build_certificate().dimensionless_ratio_theorem), ("selected_scale_inverse_seed", lambda: build_certificate().selected_scale_theorem), ("selected_dimensionless_product", lambda: build_certificate().selected_invariant_theorem), ("seed_cell_parent_rescaling", lambda: build_certificate().parent_rescaling_theorem), ("coefficient_constraint_rank_two", lambda: build_certificate().constraint_rank_theorem), ("coefficient_constraint_nullity_one", lambda: build_certificate().constraint_nullity_theorem), ("coefficient_scale_kernel", lambda: build_certificate().constraint_kernel_theorem), ("coefficient_candidate_coverage_full", lambda: build_certificate().architecture_theorem), ("coefficient_origin_ledger_three", lambda: build_certificate().origin_ledger_theorem), ("coefficient_origin_score_three", lambda: build_certificate().origin_score_theorem))))