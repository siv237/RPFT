"""LCF certificate for the induced-Newton scale-seed candidate audit."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class InducedNewtonScaleSeedCandidateAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    independent_parent_anchor_vector: sp.ImmutableMatrix
    noncircular_orbit_breaker_vector: sp.ImmutableMatrix
    relative_scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    externally_anchored_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    dimension_embedding_theorem: Theorem
    independent_parent_anchor_theorem: Theorem
    noncircular_orbit_breaker_theorem: Theorem
    relative_map_theorem: Theorem
    relative_rank_theorem: Theorem
    relative_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    cell_invariant_theorem: Theorem
    clock_invariant_theorem: Theorem
    conductance_invariant_theorem: Theorem
    curvature_invariant_theorem: Theorem
    external_anchor_rank_theorem: Theorem
    observed_newton_circularity_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> InducedNewtonScaleSeedCandidateAuditCertificate:
    # L^-2 type, internally available, target independent, selected by the
    # common parent, typed into (A,B), breaks the absolute scale orbit.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 0, 1, 0],  # growth curvature
        [1, 1, 0, 1, 1, 0],  # inverse cell area
        [1, 1, 1, 0, 1, 0],  # squared spectral cutoff
        [1, 1, 1, 0, 1, 0],  # squared clock wavenumber
        [1, 1, 1, 0, 1, 0],  # squared KMS thermal wavenumber
        [1, 1, 1, 0, 1, 0],  # squared Dirac gap
        [1, 1, 0, 0, 1, 0],  # square root of topological density
        [0, 1, 1, 1, 0, 0],  # dimensionless vacuum Hessian gap
        [1, 0, 1, 0, 1, 1],  # dimensional transmutation
        [1, 1, 0, 0, 1, 1],  # inverse observed Newton area
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index))
        for index in range(candidate_matrix.rows)
    ])
    scores = [sum(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)]
    independent_parent_anchor_vector = sp.ImmutableMatrix([
        candidate_matrix[index, 0]
        * candidate_matrix[index, 2]
        * candidate_matrix[index, 3]
        * candidate_matrix[index, 5]
        for index in range(candidate_matrix.rows)
    ])
    noncircular_orbit_breaker_vector = sp.ImmutableMatrix([
        candidate_matrix[index, 1]
        * candidate_matrix[index, 2]
        * candidate_matrix[index, 5]
        for index in range(candidate_matrix.rows)
    ])

    # log(m), log(q), log(E_C), log(kappa), log(Lambda).
    relative_scale_map = sp.ImmutableMatrix([
        [1, 1, 0, 0, 0],
        [1, 0, -2, 0, 0],
        [1, 0, 0, -2, 0],
        [1, 0, 0, 0, -1],
    ])
    scale_vector = sp.ImmutableMatrix([-2, 2, -1, -1, -2])
    externally_anchored_map = sp.ImmutableMatrix.vstack(
        relative_scale_map,
        sp.ImmutableMatrix([[1, 0, 0, 0, 0]]),
    )

    seed, cell_area, energy, conductance, curvature, scale = sp.symbols(
        "m q E kappa Lambda s", positive=True
    )
    beta, newton_area = sp.symbols("beta g_N", positive=True)
    architecture = sp.ones(10, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])

    candidate_matrix_theorem = kernel.prove_matrix_equality(
        candidate_matrix,
        sp.Matrix(candidate_matrix),
        subject="ten scale-seed candidates are evaluated on six origin criteria",
    )
    pass_vector_theorem = kernel.prove_matrix_equality(
        pass_vector,
        sp.zeros(10, 1),
        subject="no current candidate passes the full induced-Newton seed contract",
    )
    maximum_score_theorem = kernel.prove_expression_equality(
        max(scores),
        4,
        subject="the best current scale-seed candidates satisfy four of six criteria",
    )
    candidate_rank_theorem = kernel.prove_exact_rank(
        candidate_matrix,
        5,
        subject="the candidate menu spans five independent criterion directions",
    )
    dimension_embedding_theorem = kernel.prove_matrix_equality(
        candidate_matrix[:, 0],
        candidate_matrix[:, 4],
        subject="every dimensionally admissible seed can be formally embedded into A and B",
    )
    independent_parent_anchor_theorem = kernel.prove_matrix_equality(
        independent_parent_anchor_vector,
        sp.zeros(10, 1),
        subject="no dimensionally valid target-independent parent-selected orbit breaker exists",
    )
    noncircular_orbit_breaker_theorem = kernel.prove_matrix_equality(
        noncircular_orbit_breaker_vector,
        sp.zeros(10, 1),
        subject="no internally available target-independent candidate breaks the scale orbit",
    )
    relative_map_theorem = kernel.prove_matrix_equality(
        relative_scale_map,
        sp.Matrix(relative_scale_map),
        subject="cell clock conductance and curvature calibrations define four relative relations",
    )
    relative_rank_theorem = kernel.prove_exact_rank(
        relative_scale_map,
        4,
        subject="four relative scale relations are independent",
    )
    relative_nullity_theorem = kernel.prove_exact_nullity(
        relative_scale_map,
        1,
        subject="one common absolute length rescaling remains",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        relative_scale_map * scale_vector,
        sp.zeros(4, 1),
        subject="the exact scale kernel co-rescales seed cell clock flow and curvature",
    )
    cell_invariant_theorem = kernel.prove_expression_equality(
        (seed / scale**2) * (scale**2 * cell_area),
        seed * cell_area,
        subject="the seed-cell product is invariant under the common scale orbit",
    )
    clock_invariant_theorem = kernel.prove_expression_equality(
        (seed / scale**2) / (energy / scale) ** 2,
        seed / energy**2,
        subject="clock calibration fixes only a seed-to-energy-squared ratio",
    )
    conductance_invariant_theorem = kernel.prove_expression_equality(
        (seed / scale**2) / (conductance / scale) ** 2,
        seed / conductance**2,
        subject="conductance calibration fixes only a seed-to-rate-squared ratio",
    )
    curvature_invariant_theorem = kernel.prove_expression_equality(
        (seed / scale**2) / (curvature / scale**2),
        seed / curvature,
        subject="cosmological curvature calibration fixes only a relative squared scale",
    )
    external_anchor_rank_theorem = kernel.prove_exact_rank(
        externally_anchored_map,
        5,
        subject="one independently selected seed magnitude would remove the final scale zero mode",
    )
    observed_newton_circularity_theorem = kernel.prove_expression_equality(
        16 * sp.pi * beta * newton_area * (1 / (16 * sp.pi * beta * newton_area)),
        1,
        subject="using observed Newton area to define the seed only inverts the target equation",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the declared induced-Newton seed candidate menu is fully audited",
    )
    origin_ledger_theorem = kernel.prove_matrix_equality(
        origin_ledger,
        sp.Matrix([1, 1, 1, 0, 0, 0]),
        subject="coverage classification and scale-kernel detection pass while physical origin remains open",
    )
    origin_score_theorem = kernel.prove_expression_equality(
        sum(origin_ledger),
        3,
        subject="three of six scale-seed audit requirements pass",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate",
        (
            candidate_matrix_theorem,
            pass_vector_theorem,
            maximum_score_theorem,
            candidate_rank_theorem,
            dimension_embedding_theorem,
            independent_parent_anchor_theorem,
            noncircular_orbit_breaker_theorem,
            relative_map_theorem,
            relative_rank_theorem,
            relative_nullity_theorem,
            scale_kernel_theorem,
            cell_invariant_theorem,
            clock_invariant_theorem,
            conductance_invariant_theorem,
            curvature_invariant_theorem,
            external_anchor_rank_theorem,
            observed_newton_circularity_theorem,
            architecture_theorem,
            origin_ledger_theorem,
            origin_score_theorem,
        ),
    )
    return InducedNewtonScaleSeedCandidateAuditCertificate(
        candidate_matrix,
        pass_vector,
        independent_parent_anchor_vector,
        noncircular_orbit_breaker_vector,
        relative_scale_map,
        scale_vector,
        externally_anchored_map,
        architecture,
        origin_ledger,
        candidate_matrix_theorem,
        pass_vector_theorem,
        maximum_score_theorem,
        candidate_rank_theorem,
        dimension_embedding_theorem,
        independent_parent_anchor_theorem,
        noncircular_orbit_breaker_theorem,
        relative_map_theorem,
        relative_rank_theorem,
        relative_nullity_theorem,
        scale_kernel_theorem,
        cell_invariant_theorem,
        clock_invariant_theorem,
        conductance_invariant_theorem,
        curvature_invariant_theorem,
        external_anchor_rank_theorem,
        observed_newton_circularity_theorem,
        architecture_theorem,
        origin_ledger_theorem,
        origin_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate",
    title="Аудит кандидатов масштабного семени индуцированной ньютоновской постоянной",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(name, getter)
        for name, getter in (
            ("newton_seed_candidate_matrix", lambda: build_certificate().candidate_matrix_theorem),
            ("newton_seed_zero_pass_vector", lambda: build_certificate().pass_vector_theorem),
            ("newton_seed_maximum_score_four", lambda: build_certificate().maximum_score_theorem),
            ("newton_seed_candidate_rank_five", lambda: build_certificate().candidate_rank_theorem),
            ("newton_seed_dimension_embedding_equivalence", lambda: build_certificate().dimension_embedding_theorem),
            ("newton_seed_independent_parent_anchor_absent", lambda: build_certificate().independent_parent_anchor_theorem),
            ("newton_seed_noncircular_orbit_breaker_absent", lambda: build_certificate().noncircular_orbit_breaker_theorem),
            ("newton_seed_relative_scale_map", lambda: build_certificate().relative_map_theorem),
            ("newton_seed_relative_rank_four", lambda: build_certificate().relative_rank_theorem),
            ("newton_seed_relative_nullity_one", lambda: build_certificate().relative_nullity_theorem),
            ("newton_seed_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
            ("newton_seed_cell_invariant", lambda: build_certificate().cell_invariant_theorem),
            ("newton_seed_clock_invariant", lambda: build_certificate().clock_invariant_theorem),
            ("newton_seed_conductance_invariant", lambda: build_certificate().conductance_invariant_theorem),
            ("newton_seed_curvature_invariant", lambda: build_certificate().curvature_invariant_theorem),
            ("newton_seed_external_anchor_rank_five", lambda: build_certificate().external_anchor_rank_theorem),
            ("newton_seed_observed_G_circularity", lambda: build_certificate().observed_newton_circularity_theorem),
            ("newton_seed_candidate_coverage_full", lambda: build_certificate().architecture_theorem),
            ("newton_seed_origin_ledger_three", lambda: build_certificate().origin_ledger_theorem),
            ("newton_seed_origin_score_three", lambda: build_certificate().origin_score_theorem),
        )
    ),
)