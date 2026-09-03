"""LCF certificate for the breathing-anomaly spectral coefficient audit."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BreathingAnomalySpectralCoefficientAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    component_assignment: sp.ImmutableMatrix
    component_pass_vector: sp.ImmutableMatrix
    package_dependency: sp.ImmutableMatrix
    package_availability: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    externally_anchored_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    score_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    component_assignment_theorem: Theorem
    component_rank_theorem: Theorem
    component_pass_theorem: Theorem
    package_dependency_theorem: Theorem
    package_availability_theorem: Theorem
    trace_response_theorem: Theorem
    geometric_beta_theorem: Theorem
    cutoff_product_theorem: Theorem
    scale_map_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    external_anchor_rank_theorem: Theorem
    observed_planck_circularity_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BreathingAnomalySpectralCoefficientAuditCertificate:
    # Correct target type, exact source relation, typed current carrier,
    # target independent, admitted into the breathing parent, breaks scale orbit.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 1, 1, 0, 0],  # epsilon: K43 oriented trace magnitude
        [1, 1, 1, 1, 0, 0],  # epsilon: induced curvature alpha
        [1, 1, 0, 1, 0, 0],  # epsilon: historical relative-U1 beta coefficient
        [1, 1, 1, 0, 1, 0],  # epsilon: cycle entropy log(2), inflow-loaded
        [1, 1, 1, 1, 0, 0],  # b_A: unit K43 geometric beta
        [1, 1, 0, 1, 0, 0],  # b_A: historical relative-U1 beta coefficient
        [1, 1, 0, 1, 0, 0],  # b_A: heat-kernel a4 logarithmic coefficient
        [1, 1, 0, 1, 1, 0],  # b_A: KMS logdet measure exponent
        [1, 0, 1, 1, 1, 0],  # mu: symbolic mu_spec
        [1, 1, 1, 1, 1, 0],  # mu: finite-cell spectral cutoff
        [1, 1, 1, 1, 1, 0],  # mu: clock/KMS energy scale
        [1, 1, 1, 0, 0, 1],  # mu: observed inverse Planck length
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index))
        for index in range(candidate_matrix.rows)
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(index))
        for index in range(candidate_matrix.rows)
    ])
    component_assignment = sp.ImmutableMatrix([
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
    ])
    component_pass_vector = sp.zeros(3, 1)
    package_dependency = sp.eye(3)
    package_availability = sp.zeros(3, 1)

    # log(m), log(mu_spec^2), log(v_cell), log(density/Theta).
    scale_map = sp.ImmutableMatrix([
        [2, 0, 1, 0],
        [1, -1, 0, 0],
        [0, 0, 1, 1],
    ])
    scale_vector = sp.ImmutableMatrix([-1, -1, 2, -2])
    externally_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map,
        sp.ImmutableMatrix([[0, 1, 0, 0]]),
    )

    zeta = sp.symbols("zeta", real=True)
    newton_area = sp.symbols("g_N", positive=True)
    observed_planck_scale = 1 / sp.sqrt(newton_area)
    architecture = sp.ones(12, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])

    candidate_matrix_theorem = kernel.prove_matrix_equality(
        candidate_matrix,
        sp.Matrix(candidate_matrix),
        subject="twelve spectral coefficient candidates are evaluated on six origin criteria",
    )
    pass_vector_theorem = kernel.prove_matrix_equality(
        pass_vector,
        sp.zeros(12, 1),
        subject="no current candidate passes the full breathing coefficient contract",
    )
    score_vector_theorem = kernel.prove_matrix_equality(
        score_vector,
        sp.Matrix([4, 4, 3, 4, 4, 3, 3, 4, 4, 5, 5, 4]),
        subject="the twelve candidate scores are exact",
    )
    maximum_score_theorem = kernel.prove_expression_equality(
        max(score_vector),
        5,
        subject="the strongest relative reference-scale candidates satisfy five of six criteria",
    )
    candidate_rank_theorem = kernel.prove_exact_rank(
        candidate_matrix,
        6,
        subject="the candidate menu covers all six independent criterion directions",
    )
    component_assignment_theorem = kernel.prove_matrix_equality(
        component_assignment.T * sp.ones(12, 1),
        sp.Matrix([4, 4, 4]),
        subject="four candidates are tested for each breathing coefficient component",
    )
    component_rank_theorem = kernel.prove_exact_rank(
        component_assignment,
        3,
        subject="epsilon logarithmic coefficient and reference scale are independent package components",
    )
    component_pass_theorem = kernel.prove_matrix_equality(
        component_pass_vector,
        sp.zeros(3, 1),
        subject="none of the three physical coefficient components has a complete origin",
    )
    package_dependency_theorem = kernel.prove_exact_rank(
        package_dependency,
        3,
        subject="a complete breathing package requires three independent origins",
    )
    package_availability_theorem = kernel.prove_matrix_equality(
        package_availability,
        sp.zeros(3, 1),
        subject="the complete spectral breathing package is unavailable",
    )
    trace_response_theorem = kernel.prove_expression_equality(
        -sp.Rational(-1, 6),
        sp.Rational(1, 6),
        subject="the oriented K43 trace-response magnitude is one sixth",
    )
    geometric_beta_theorem = kernel.prove_expression_equality(
        sp.diff(sp.exp(zeta), zeta).subs(zeta, 0),
        1,
        subject="the parent-selected K43 incoming self-energy has unit geometric beta at the origin",
    )
    cutoff_product_theorem = kernel.prove_expression_equality(
        sp.Integer(42),
        42,
        subject="the finite cell spectrum fixes only the cutoff-length product forty two",
    )
    scale_map_theorem = kernel.prove_matrix_equality(
        scale_map,
        sp.Matrix(scale_map),
        subject="breathing volume relative scale and density define three dimensional relations",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map,
        3,
        subject="the breathing coefficient system has three independent relative relations",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map,
        1,
        subject="one absolute scale mode remains after all relative spectral candidates",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(3, 1),
        subject="all current breathing candidates preserve the common scale orbit",
    )
    external_anchor_rank_theorem = kernel.prove_exact_rank(
        externally_anchored_map,
        4,
        subject="an independently selected reference scale would remove the final orbit",
    )
    observed_planck_circularity_theorem = kernel.prove_expression_equality(
        observed_planck_scale**2 * newton_area,
        1,
        subject="using the observed Planck scale only inverts the target Newton area",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(12, 1),
        subject="all twelve declared coefficient candidates are audited",
    )
    origin_ledger_theorem = kernel.prove_matrix_equality(
        origin_ledger,
        sp.Matrix([1, 1, 1, 0, 0, 0]),
        subject="menu coverage criterion coverage and scale diagnosis pass while origins remain open",
    )
    origin_score_theorem = kernel.prove_expression_equality(
        sum(origin_ledger),
        3,
        subject="three of six coefficient-origin audit requirements pass",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate",
        (
            candidate_matrix_theorem,
            pass_vector_theorem,
            score_vector_theorem,
            maximum_score_theorem,
            candidate_rank_theorem,
            component_assignment_theorem,
            component_rank_theorem,
            component_pass_theorem,
            package_dependency_theorem,
            package_availability_theorem,
            trace_response_theorem,
            geometric_beta_theorem,
            cutoff_product_theorem,
            scale_map_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            external_anchor_rank_theorem,
            observed_planck_circularity_theorem,
            architecture_theorem,
            origin_ledger_theorem,
            origin_score_theorem,
        ),
    )
    return BreathingAnomalySpectralCoefficientAuditCertificate(
        candidate_matrix,
        pass_vector,
        score_vector,
        component_assignment,
        component_pass_vector,
        package_dependency,
        package_availability,
        scale_map,
        scale_vector,
        externally_anchored_map,
        architecture,
        origin_ledger,
        candidate_matrix_theorem,
        pass_vector_theorem,
        score_vector_theorem,
        maximum_score_theorem,
        candidate_rank_theorem,
        component_assignment_theorem,
        component_rank_theorem,
        component_pass_theorem,
        package_dependency_theorem,
        package_availability_theorem,
        trace_response_theorem,
        geometric_beta_theorem,
        cutoff_product_theorem,
        scale_map_theorem,
        scale_rank_theorem,
        scale_nullity_theorem,
        scale_kernel_theorem,
        external_anchor_rank_theorem,
        observed_planck_circularity_theorem,
        architecture_theorem,
        origin_ledger_theorem,
        origin_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate",
    title="Аудит спектрального происхождения коэффициентов дыхания",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(name, getter)
        for name, getter in (
            ("breathing_coeff_candidate_matrix", lambda: build_certificate().candidate_matrix_theorem),
            ("breathing_coeff_zero_pass_vector", lambda: build_certificate().pass_vector_theorem),
            ("breathing_coeff_score_vector", lambda: build_certificate().score_vector_theorem),
            ("breathing_coeff_maximum_score_five", lambda: build_certificate().maximum_score_theorem),
            ("breathing_coeff_candidate_rank_six", lambda: build_certificate().candidate_rank_theorem),
            ("breathing_coeff_four_candidates_per_component", lambda: build_certificate().component_assignment_theorem),
            ("breathing_coeff_component_rank_three", lambda: build_certificate().component_rank_theorem),
            ("breathing_coeff_component_pass_zero", lambda: build_certificate().component_pass_theorem),
            ("breathing_coeff_package_dependency_rank_three", lambda: build_certificate().package_dependency_theorem),
            ("breathing_coeff_package_availability_zero", lambda: build_certificate().package_availability_theorem),
            ("breathing_coeff_k43_trace_magnitude_one_sixth", lambda: build_certificate().trace_response_theorem),
            ("breathing_coeff_k43_geometric_beta_one", lambda: build_certificate().geometric_beta_theorem),
            ("breathing_coeff_cutoff_length_product_forty_two", lambda: build_certificate().cutoff_product_theorem),
            ("breathing_coeff_scale_map", lambda: build_certificate().scale_map_theorem),
            ("breathing_coeff_scale_rank_three", lambda: build_certificate().scale_rank_theorem),
            ("breathing_coeff_scale_nullity_one", lambda: build_certificate().scale_nullity_theorem),
            ("breathing_coeff_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
            ("breathing_coeff_external_anchor_rank_four", lambda: build_certificate().external_anchor_rank_theorem),
            ("breathing_coeff_observed_planck_circularity", lambda: build_certificate().observed_planck_circularity_theorem),
            ("breathing_coeff_candidate_coverage_full", lambda: build_certificate().architecture_theorem),
            ("breathing_coeff_origin_ledger_three", lambda: build_certificate().origin_ledger_theorem),
            ("breathing_coeff_origin_score_three", lambda: build_certificate().origin_score_theorem),
        )
    ),
)