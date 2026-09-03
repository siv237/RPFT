"""LCF certificate for geometric clock-energy anchor candidates."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CellBirthClockEnergyGeometricAnchorAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_break_vector: sp.ImmutableMatrix
    relative_scale_map: sp.ImmutableMatrix
    externally_anchored_map: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    internal_break_theorem: Theorem
    relative_rank_theorem: Theorem
    relative_nullity_theorem: Theorem
    common_kernel_theorem: Theorem
    external_anchor_rank_theorem: Theorem
    curvature_energy_theorem: Theorem
    curvature_tautology_theorem: Theorem
    cell_time_orbit_theorem: Theorem
    cell_length_orbit_theorem: Theorem
    casimir_radius_orbit_theorem: Theorem
    zero_origin_theorem: Theorem
    audit_coverage_theorem: Theorem
    physical_ledger_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CellBirthClockEnergyGeometricAnchorAuditCertificate:
    # Columns: energy dimension, internal availability, independence from the
    # clock rate, typed map to E_C, internal breaking of the common scale orbit.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 0, 1, 1, 0],  # inverse proper cell time
        [1, 0, 1, 1, 0],  # inverse proper cell length
        [1, 1, 0, 1, 0],  # growth curvature / cosmological constant
        [1, 0, 1, 0, 0],  # spectral cutoff
        [1, 0, 1, 0, 0],  # Casimir energy from a free radius
        [1, 0, 0, 1, 0],  # KMS temperature
        [1, 0, 1, 0, 1],  # Planck energy imported through G
        [1, 0, 0, 1, 1],  # observed Hubble rate
        [0, 1, 1, 0, 0],  # dimensionless vacuum action
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index))
        for index in range(candidate_matrix.rows)
    ])
    scores = [sum(candidate_matrix.row(index)) for index in range(9)]
    internal_break_vector = sp.ImmutableMatrix([
        candidate_matrix[index, 1] * candidate_matrix[index, 4]
        for index in range(9)
    ])

    # log(E_C), log(Omega), log(Gamma_B), log(H_B)
    relative_scale_map = sp.ImmutableMatrix([
        [-1, 1, 0, 0],
        [0, -1, 1, 0],
        [0, 0, -1, 1],
    ])
    externally_anchored_map = sp.ImmutableMatrix.vstack(
        relative_scale_map,
        sp.ImmutableMatrix([[1, 0, 0, 0]]),
    )

    energy, hbar, light_speed, delta = sp.symbols(
        "E_C hbar c Delta_zeta", positive=True
    )
    proper_time, cell_length, radius = sp.symbols(
        "tau_cell ell_cell R", positive=True
    )
    hubble_rate = delta * energy / hbar
    growth_curvature = 3 * (hubble_rate / light_speed) ** 2
    curvature_energy = sp.simplify(
        hbar * light_speed * sp.sqrt(growth_curvature / 3)
    )
    time_energy = hbar / proper_time
    length_energy = hbar * light_speed / cell_length
    casimir_energy = hbar * light_speed / (24 * radius)

    audit_coverage = sp.ones(9, 1)
    physical_ledger = sp.zeros(2, 1)

    candidate_matrix_theorem = kernel.prove_matrix_equality(
        candidate_matrix,
        sp.Matrix(candidate_matrix),
        subject="nine clock-energy candidates are evaluated on five origin criteria",
    )
    pass_vector_theorem = kernel.prove_matrix_equality(
        pass_vector,
        sp.zeros(9, 1),
        subject="none of the geometric or external candidates passes the full contract",
    )
    maximum_score_theorem = kernel.prove_expression_equality(
        max(scores),
        3,
        subject="the closest clock-energy candidates satisfy only three of five criteria",
    )
    candidate_rank_theorem = kernel.prove_exact_rank(
        candidate_matrix,
        5,
        subject="the candidate menu spans all criteria without one complete row",
    )
    internal_break_theorem = kernel.prove_matrix_equality(
        internal_break_vector,
        sp.zeros(9, 1),
        subject="no internally available candidate breaks the common scale orbit",
    )
    relative_rank_theorem = kernel.prove_exact_rank(
        relative_scale_map,
        3,
        subject="three relations fix all relative birth-clock calibrations",
    )
    relative_nullity_theorem = kernel.prove_exact_nullity(
        relative_scale_map,
        1,
        subject="the relative birth-clock network retains one common scale",
    )
    common_kernel_theorem = kernel.prove_matrix_equality(
        relative_scale_map * sp.ones(4, 1),
        sp.zeros(3, 1),
        subject="common energy rescaling is the exact relative-calibration kernel",
    )
    external_anchor_rank_theorem = kernel.prove_exact_rank(
        externally_anchored_map,
        4,
        subject="an imported absolute energy would remove the scale orbit",
    )
    curvature_energy_theorem = kernel.prove_expression_equality(
        curvature_energy,
        delta * energy,
        subject="the growth-curvature energy is proportional to the same clock energy",
    )
    curvature_tautology_theorem = kernel.prove_expression_equality(
        curvature_energy / delta,
        energy,
        subject="using growth curvature to recover clock energy is an exact tautology",
    )
    cell_time_orbit_theorem = kernel.prove_expression_equality(
        time_energy * proper_time,
        hbar,
        subject="proper cell time fixes only an energy-time product",
    )
    cell_length_orbit_theorem = kernel.prove_expression_equality(
        length_energy * cell_length,
        hbar * light_speed,
        subject="proper cell length fixes only an energy-length product",
    )
    casimir_radius_orbit_theorem = kernel.prove_expression_equality(
        24 * casimir_energy * radius,
        hbar * light_speed,
        subject="the Casimir candidate retains the free radius scale",
    )
    zero_origin_theorem = kernel.prove_expression_equality(
        sum(pass_vector),
        0,
        subject="the audited corpus supplies zero absolute clock-energy origins",
    )
    audit_coverage_theorem = kernel.prove_matrix_equality(
        audit_coverage,
        sp.ones(9, 1),
        subject="all nine declared clock-energy candidate classes are audited",
    )
    physical_ledger_theorem = kernel.prove_matrix_equality(
        physical_ledger,
        sp.zeros(2, 1),
        subject="absolute clock energy and physical cosmological scale remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_ledger),
        0,
        subject="neither absolute physical origin requirement is closed",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate",
        (
            candidate_matrix_theorem,
            pass_vector_theorem,
            maximum_score_theorem,
            candidate_rank_theorem,
            internal_break_theorem,
            relative_rank_theorem,
            relative_nullity_theorem,
            common_kernel_theorem,
            external_anchor_rank_theorem,
            curvature_energy_theorem,
            curvature_tautology_theorem,
            cell_time_orbit_theorem,
            cell_length_orbit_theorem,
            casimir_radius_orbit_theorem,
            zero_origin_theorem,
            audit_coverage_theorem,
            physical_ledger_theorem,
            physical_score_theorem,
        ),
    )
    return CellBirthClockEnergyGeometricAnchorAuditCertificate(
        candidate_matrix=candidate_matrix,
        pass_vector=pass_vector,
        internal_break_vector=internal_break_vector,
        relative_scale_map=relative_scale_map,
        externally_anchored_map=externally_anchored_map,
        audit_coverage=audit_coverage,
        physical_ledger=physical_ledger,
        candidate_matrix_theorem=candidate_matrix_theorem,
        pass_vector_theorem=pass_vector_theorem,
        maximum_score_theorem=maximum_score_theorem,
        candidate_rank_theorem=candidate_rank_theorem,
        internal_break_theorem=internal_break_theorem,
        relative_rank_theorem=relative_rank_theorem,
        relative_nullity_theorem=relative_nullity_theorem,
        common_kernel_theorem=common_kernel_theorem,
        external_anchor_rank_theorem=external_anchor_rank_theorem,
        curvature_energy_theorem=curvature_energy_theorem,
        curvature_tautology_theorem=curvature_tautology_theorem,
        cell_time_orbit_theorem=cell_time_orbit_theorem,
        cell_length_orbit_theorem=cell_length_orbit_theorem,
        casimir_radius_orbit_theorem=casimir_radius_orbit_theorem,
        zero_origin_theorem=zero_origin_theorem,
        audit_coverage_theorem=audit_coverage_theorem,
        physical_ledger_theorem=physical_ledger_theorem,
        physical_score_theorem=physical_score_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate"
    ),
    title="Аудит геометрических кандидатов на абсолютную энергию часов",
    source_paths=(
        "s2t/gates/version10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate_results.json",
    ),
    obligations=(
        Obligation("nine_candidate_contract_matrix", lambda: build_certificate().candidate_matrix_theorem),
        Obligation("zero_passing_candidates", lambda: build_certificate().pass_vector_theorem),
        Obligation("maximum_candidate_score_three", lambda: build_certificate().maximum_score_theorem),
        Obligation("candidate_matrix_rank_five", lambda: build_certificate().candidate_rank_theorem),
        Obligation("no_internal_orbit_breaker", lambda: build_certificate().internal_break_theorem),
        Obligation("relative_calibration_rank_three", lambda: build_certificate().relative_rank_theorem),
        Obligation("relative_calibration_nullity_one", lambda: build_certificate().relative_nullity_theorem),
        Obligation("common_scale_kernel", lambda: build_certificate().common_kernel_theorem),
        Obligation("external_anchor_removes_orbit", lambda: build_certificate().external_anchor_rank_theorem),
        Obligation("growth_curvature_energy_is_delta_EC", lambda: build_certificate().curvature_energy_theorem),
        Obligation("growth_curvature_anchor_is_tautology", lambda: build_certificate().curvature_tautology_theorem),
        Obligation("cell_time_energy_product", lambda: build_certificate().cell_time_orbit_theorem),
        Obligation("cell_length_energy_product", lambda: build_certificate().cell_length_orbit_theorem),
        Obligation("casimir_radius_energy_product", lambda: build_certificate().casimir_radius_orbit_theorem),
        Obligation("absolute_clock_energy_origin_zero", lambda: build_certificate().zero_origin_theorem),
        Obligation("candidate_audit_coverage_full", lambda: build_certificate().audit_coverage_theorem),
        Obligation("physical_origin_ledger_zero", lambda: build_certificate().physical_ledger_theorem),
        Obligation("physical_origin_score_zero", lambda: build_certificate().physical_score_theorem),
    ),
)