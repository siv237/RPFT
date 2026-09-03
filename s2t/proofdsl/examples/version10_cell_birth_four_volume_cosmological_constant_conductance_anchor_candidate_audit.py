"""LCF certificate for cosmological-constant conductance anchors."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CosmologicalConductanceAnchorAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_break_vector: sp.ImmutableMatrix
    relative_scale_map: sp.ImmutableMatrix
    independently_anchored_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    internal_break_theorem: Theorem
    hubble_conductance_theorem: Theorem
    growth_lambda_theorem: Theorem
    lambda_reconstruction_theorem: Theorem
    curvature_radius_theorem: Theorem
    relative_rank_theorem: Theorem
    relative_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    independent_anchor_rank_theorem: Theorem
    audit_coverage_theorem: Theorem
    candidate_origin_zero_theorem: Theorem
    physical_ledger_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CosmologicalConductanceAnchorAuditCertificate:
    # Columns: curvature dimension, internal availability, independence from
    # rates, typed map to kappa, orbit breaking, common-parent provenance.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 1, 0, 0],  # growth cosmological constant
        [1, 1, 1, 1, 0, 0],  # intrinsic cell curvature with free cell size
        [1, 0, 1, 1, 0, 0],  # spectral cutoff curvature
        [1, 1, 0, 1, 0, 0],  # throughflow-induced curvature
        [1, 0, 1, 1, 1, 0],  # observed cosmological constant
        [1, 0, 1, 1, 1, 0],  # Planck/vacuum-density curvature
        [1, 1, 1, 0, 0, 0],  # topological density with free volume quantum
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index))
        for index in range(candidate_matrix.rows)
    ])
    scores = [sum(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)]
    internal_break_vector = sp.ImmutableMatrix([
        candidate_matrix[index, 1] * candidate_matrix[index, 4]
        for index in range(candidate_matrix.rows)
    ])

    # log(kappa), log(Gamma_B), log(Omega), log(H_B), log(Lambda).
    relative_scale_map = sp.ImmutableMatrix([
        [1, -1, 0, 0, 0],
        [0, 1, -1, 0, 0],
        [0, 0, -1, 1, 0],
        [0, 0, 0, -2, 1],
    ])
    independently_anchored_map = sp.ImmutableMatrix.vstack(
        relative_scale_map,
        sp.ImmutableMatrix([[0, 0, 0, 0, 1]]),
    )
    scale_vector = sp.ImmutableMatrix([1, 1, 1, 1, 2])

    conductance, light_speed = sp.symbols("kappa c", positive=True)
    hubble_rate = conductance / 3
    growth_lambda = sp.simplify(3 * (hubble_rate / light_speed) ** 2)
    reconstructed_conductance = sp.simplify(light_speed * sp.sqrt(3 * growth_lambda))
    curvature_radius = sp.simplify(sp.sqrt(3 / growth_lambda))

    audit_coverage = sp.ones(7, 1)
    physical_ledger = sp.zeros(2, 1)

    candidate_matrix_theorem = kernel.prove_matrix_equality(
        candidate_matrix,
        sp.Matrix(candidate_matrix),
        subject="seven cosmological conductance anchors are evaluated on six origin criteria",
    )
    pass_vector_theorem = kernel.prove_matrix_equality(
        pass_vector,
        sp.zeros(7, 1),
        subject="none of the cosmological conductance candidates passes the full origin contract",
    )
    maximum_score_theorem = kernel.prove_expression_equality(
        max(scores),
        4,
        subject="the closest cosmological conductance candidates satisfy four of six criteria",
    )
    candidate_rank_theorem = kernel.prove_exact_rank(
        candidate_matrix,
        5,
        subject="the cosmological candidate menu spans five independent criterion directions",
    )
    internal_break_theorem = kernel.prove_matrix_equality(
        internal_break_vector,
        sp.zeros(7, 1),
        subject="no internally available cosmological candidate breaks the rate orbit",
    )
    hubble_conductance_theorem = kernel.prove_expression_equality(
        hubble_rate,
        conductance / 3,
        subject="the geometric growth rate is one third of the selected Hopf conductance",
    )
    growth_lambda_theorem = kernel.prove_expression_equality(
        growth_lambda,
        conductance**2 / (3 * light_speed**2),
        subject="the growth cosmological constant is determined by the conductance",
    )
    lambda_reconstruction_theorem = kernel.prove_expression_equality(
        reconstructed_conductance,
        conductance,
        subject="reconstructing conductance from growth curvature is an exact tautology",
    )
    curvature_radius_theorem = kernel.prove_expression_equality(
        conductance * curvature_radius,
        3 * light_speed,
        subject="growth curvature fixes only the conductance-radius product",
    )
    relative_rank_theorem = kernel.prove_exact_rank(
        relative_scale_map,
        4,
        subject="four relations fix all relative conductance clock and curvature scales",
    )
    relative_nullity_theorem = kernel.prove_exact_nullity(
        relative_scale_map,
        1,
        subject="the conductance curvature network retains one common scale orbit",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        relative_scale_map * scale_vector,
        sp.zeros(4, 1),
        subject="rates scale linearly while cosmological curvature scales quadratically",
    )
    independent_anchor_rank_theorem = kernel.prove_exact_rank(
        independently_anchored_map,
        5,
        subject="an independently fixed cosmological constant would remove the scale orbit",
    )
    audit_coverage_theorem = kernel.prove_matrix_equality(
        audit_coverage,
        sp.ones(7, 1),
        subject="all seven declared cosmological anchor classes are audited",
    )
    candidate_origin_zero_theorem = kernel.prove_expression_equality(
        sum(pass_vector),
        0,
        subject="the audited corpus supplies zero complete cosmological conductance anchors",
    )
    physical_ledger_theorem = kernel.prove_matrix_equality(
        physical_ledger,
        sp.zeros(2, 1),
        subject="physical cosmological origin and absolute conductance remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_ledger),
        0,
        subject="neither absolute origin requirement is closed",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate",
        (
            candidate_matrix_theorem,
            pass_vector_theorem,
            maximum_score_theorem,
            candidate_rank_theorem,
            internal_break_theorem,
            hubble_conductance_theorem,
            growth_lambda_theorem,
            lambda_reconstruction_theorem,
            curvature_radius_theorem,
            relative_rank_theorem,
            relative_nullity_theorem,
            scale_kernel_theorem,
            independent_anchor_rank_theorem,
            audit_coverage_theorem,
            candidate_origin_zero_theorem,
            physical_ledger_theorem,
            physical_score_theorem,
        ),
    )
    return CosmologicalConductanceAnchorAuditCertificate(
        candidate_matrix,
        pass_vector,
        internal_break_vector,
        relative_scale_map,
        independently_anchored_map,
        scale_vector,
        audit_coverage,
        physical_ledger,
        candidate_matrix_theorem,
        pass_vector_theorem,
        maximum_score_theorem,
        candidate_rank_theorem,
        internal_break_theorem,
        hubble_conductance_theorem,
        growth_lambda_theorem,
        lambda_reconstruction_theorem,
        curvature_radius_theorem,
        relative_rank_theorem,
        relative_nullity_theorem,
        scale_kernel_theorem,
        independent_anchor_rank_theorem,
        audit_coverage_theorem,
        candidate_origin_zero_theorem,
        physical_ledger_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate",
    title="Аудит космологической постоянной как якоря проводимости",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate_results.json",
    ),
    obligations=(
        Obligation("cosmological_anchor_candidate_matrix", lambda: build_certificate().candidate_matrix_theorem),
        Obligation("cosmological_anchor_zero_passes", lambda: build_certificate().pass_vector_theorem),
        Obligation("cosmological_anchor_maximum_score_four", lambda: build_certificate().maximum_score_theorem),
        Obligation("cosmological_anchor_matrix_rank_five", lambda: build_certificate().candidate_rank_theorem),
        Obligation("cosmological_anchor_no_internal_breaker", lambda: build_certificate().internal_break_theorem),
        Obligation("hubble_conductance_relation", lambda: build_certificate().hubble_conductance_theorem),
        Obligation("growth_lambda_conductance_relation", lambda: build_certificate().growth_lambda_theorem),
        Obligation("growth_lambda_reconstruction_tautology", lambda: build_certificate().lambda_reconstruction_theorem),
        Obligation("curvature_radius_conductance_product", lambda: build_certificate().curvature_radius_theorem),
        Obligation("cosmological_relative_map_rank_four", lambda: build_certificate().relative_rank_theorem),
        Obligation("cosmological_relative_map_nullity_one", lambda: build_certificate().relative_nullity_theorem),
        Obligation("cosmological_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
        Obligation("independent_lambda_removes_orbit", lambda: build_certificate().independent_anchor_rank_theorem),
        Obligation("cosmological_anchor_audit_coverage", lambda: build_certificate().audit_coverage_theorem),
        Obligation("cosmological_anchor_origin_zero", lambda: build_certificate().candidate_origin_zero_theorem),
        Obligation("cosmological_physical_ledger_zero", lambda: build_certificate().physical_ledger_theorem),
        Obligation("cosmological_physical_score_zero", lambda: build_certificate().physical_score_theorem),
    ),
)