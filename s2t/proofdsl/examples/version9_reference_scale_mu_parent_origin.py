"""LCF certificate for the physical reference-scale mu origin audit."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class ReferenceScaleMuParentOriginCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    relative_scale_map: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    typed_map_theorem: Theorem
    relative_map_rank_theorem: Theorem
    relative_map_nullity_theorem: Theorem
    common_scale_kernel_theorem: Theorem
    kms_scaling_theorem: Theorem
    clock_scaling_theorem: Theorem
    radius_scaling_theorem: Theorem
    zero_origin_count_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ReferenceScaleMuParentOriginCertificate:
    candidate_matrix = sp.ImmutableMatrix([
        [1, 0, 0, 0, 1],  # inverse KMS temperature
        [1, 0, 0, 0, 1],  # clock energy
        [1, 0, 0, 0, 1],  # reservoir cutoff
        [1, 0, 0, 0, 1],  # inverse compactification radius
        [1, 0, 0, 0, 1],  # spectral Dirac scale
        [1, 0, 0, 1, 0],  # observed mass
        [0, 1, 0, 0, 1],  # dimensionless vacuum Hessian gap
        [1, 0, 0, 1, 1],  # dimensional transmutation without derived beta data
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index))
        for index in range(candidate_matrix.rows)
    ])
    scores = [sum(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)]

    relative_scale_map = sp.zeros(7, 8)
    for index in range(7):
        relative_scale_map[index, 0] = -1
        relative_scale_map[index, index + 1] = 1
    relative_scale_map = sp.ImmutableMatrix(relative_scale_map)

    mu, beta, energy, tick, hbar, radius, light_speed, scale = sp.symbols(
        "mu beta E tau hbar R c s", positive=True
    )

    candidate_matrix_theorem = kernel.prove_matrix_equality(
        candidate_matrix,
        sp.Matrix(candidate_matrix),
        subject="eight reference scale candidates are evaluated on five origin criteria",
    )
    pass_vector_theorem = kernel.prove_matrix_equality(
        pass_vector,
        sp.zeros(8, 1),
        subject="none of the eight candidates passes the full physical origin contract",
    )
    maximum_score_theorem = kernel.prove_expression_equality(
        max(scores),
        3,
        subject="dimensional transmutation is the closest candidate with three of five criteria",
    )
    candidate_rank_theorem = kernel.prove_exact_rank(
        candidate_matrix,
        4,
        subject="the audited candidates span only four of five origin criteria",
    )
    typed_map_theorem = kernel.prove_matrix_equality(
        candidate_matrix[:, 2],
        sp.zeros(8, 1),
        subject="no candidate has a derived typed map into the Gaussian carrier",
    )
    relative_map_rank_theorem = kernel.prove_exact_rank(
        relative_scale_map,
        7,
        subject="seven energy ratios determine only relative scales",
    )
    relative_map_nullity_theorem = kernel.prove_exact_nullity(
        relative_scale_map,
        1,
        subject="one common absolute energy scale remains invisible",
    )
    common_scale_kernel_theorem = kernel.prove_matrix_equality(
        relative_scale_map * sp.ones(8, 1),
        sp.zeros(7, 1),
        subject="common rescaling is the exact kernel of all relative calibrations",
    )
    kms_scaling_theorem = kernel.prove_expression_equality(
        scale * mu * (beta / scale),
        mu * beta,
        subject="inverse temperature compensates a common energy rescaling",
    )
    clock_scaling_theorem = kernel.prove_expression_equality(
        scale * energy * (tick / scale) / hbar,
        energy * tick / hbar,
        subject="clock phase remains dimensionless under common energy rescaling",
    )
    radius_scaling_theorem = kernel.prove_expression_equality(
        scale * mu * (radius / scale) / (hbar * light_speed),
        mu * radius / (hbar * light_speed),
        subject="inverse radius calibration also leaves a common scale orbit",
    )
    zero_origin_count_theorem = kernel.prove_expression_equality(
        sum(pass_vector),
        0,
        subject="the current corpus supplies zero physical reference scale origins",
    )
    gate_theorem = kernel.prove_gate(
        "version9_physical_reopening_reference_scale_mu_parent_origin_gate",
        (
            candidate_matrix_theorem,
            pass_vector_theorem,
            maximum_score_theorem,
            candidate_rank_theorem,
            typed_map_theorem,
            relative_map_rank_theorem,
            relative_map_nullity_theorem,
            common_scale_kernel_theorem,
            kms_scaling_theorem,
            clock_scaling_theorem,
            radius_scaling_theorem,
            zero_origin_count_theorem,
        ),
    )
    return ReferenceScaleMuParentOriginCertificate(
        candidate_matrix=candidate_matrix,
        pass_vector=pass_vector,
        relative_scale_map=relative_scale_map,
        candidate_matrix_theorem=candidate_matrix_theorem,
        pass_vector_theorem=pass_vector_theorem,
        maximum_score_theorem=maximum_score_theorem,
        candidate_rank_theorem=candidate_rank_theorem,
        typed_map_theorem=typed_map_theorem,
        relative_map_rank_theorem=relative_map_rank_theorem,
        relative_map_nullity_theorem=relative_map_nullity_theorem,
        common_scale_kernel_theorem=common_scale_kernel_theorem,
        kms_scaling_theorem=kms_scaling_theorem,
        clock_scaling_theorem=clock_scaling_theorem,
        radius_scaling_theorem=radius_scaling_theorem,
        zero_origin_count_theorem=zero_origin_count_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_physical_reopening_reference_scale_mu_parent_origin_gate",
    title="Parent-origin физического reference scale mu",
    source_paths=(
        "s2t/gates/version9_physical_reopening_reference_scale_mu_parent_origin_gate.tex",
        "s2t/results/s2t_v9_physical_reopening_reference_scale_mu_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("eight_candidate_contract_matrix", lambda: build_certificate().candidate_matrix_theorem),
        Obligation("zero_passing_candidates", lambda: build_certificate().pass_vector_theorem),
        Obligation("maximum_candidate_score_three", lambda: build_certificate().maximum_score_theorem),
        Obligation("candidate_criterion_rank_four", lambda: build_certificate().candidate_rank_theorem),
        Obligation("typed_gaussian_map_absent", lambda: build_certificate().typed_map_theorem),
        Obligation("relative_scale_map_rank_seven", lambda: build_certificate().relative_map_rank_theorem),
        Obligation("relative_scale_map_nullity_one", lambda: build_certificate().relative_map_nullity_theorem),
        Obligation("common_scale_kernel", lambda: build_certificate().common_scale_kernel_theorem),
        Obligation("kms_energy_temperature_invariance", lambda: build_certificate().kms_scaling_theorem),
        Obligation("clock_energy_time_invariance", lambda: build_certificate().clock_scaling_theorem),
        Obligation("inverse_radius_scale_invariance", lambda: build_certificate().radius_scaling_theorem),
        Obligation("physical_reference_scale_origin_zero", lambda: build_certificate().zero_origin_count_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)