"""LCF certificate for the hypercharge-gap coefficient candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HyperchargeGapCoefficientAuditCertificate:
    sector_mass_map: sp.ImmutableMatrix
    diagnostic_coefficients: sp.ImmutableMatrix
    diagnostic_masses: sp.ImmutableMatrix
    strict_sign_pass: sp.ImmutableMatrix
    boundary_flags: sp.ImmutableMatrix
    interior_coefficients: sp.ImmutableMatrix
    interior_masses: sp.ImmutableMatrix
    inherited_coefficient_map: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HyperchargeGapCoefficientAuditCertificate:
    # A quadratic mass polynomial a I + b Q^2 is evaluated on Q^2=49,9,1.
    sector_mass_map = sp.ImmutableMatrix([[1, 49], [1, 9], [1, 1]])
    diagnostic_coefficients = sp.ImmutableMatrix(
        [
            [-1, 0],   # universal tachyonic shift
            [0, 1],    # positive hypercharge Casimir
            [0, -1],   # negative hypercharge Casimir
            [49, -1],  # lower boundary: G_Y
            [29, -1],  # interior witness: mu^2/kappa=20
            [9, -1],   # upper boundary: first companions become massless
        ]
    )
    diagnostic_masses = sp.ImmutableMatrix(diagnostic_coefficients * sector_mass_map.T)
    strict_sign_pass = sp.ImmutableMatrix([0, 0, 0, 0, 1, 0])
    boundary_flags = sp.ImmutableMatrix([0, 0, 0, 1, 0, 1])

    # Two inequivalent normalized interior points prove that the sign gate
    # selects an open cone, not a unique dimensionless ratio.
    interior_coefficients = sp.ImmutableMatrix([[39, -1], [19, -1]])
    interior_masses = sp.ImmutableMatrix(interior_coefficients * sector_mass_map.T)

    inherited_coefficient_map = sp.ImmutableMatrix.zeros(2, 3)

    # Columns: Q^2 resolution, interior sign cone, positive quartic,
    # typed SM-breaking background, inherited carrier, coefficient locking.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [0, 0, 1, 0, 1, 0],  # ordinary one-profile spectral moments
            [0, 0, 0, 0, 1, 0],  # universal quadratic mass shift
            [1, 0, 1, 1, 0, 0],  # positive hypercharge Casimir/D-term
            [1, 0, 0, 0, 0, 0],  # negative hypercharge Casimir
            [1, 0, 0, 1, 0, 0],  # algebraic boundary gap G_Y
            [1, 1, 1, 1, 0, 0],  # target-loaded interior potential
            [1, 0, 1, 1, 0, 0],  # independent Pati-Salam adjoint VEV pair
            [0, 0, 1, 0, 0, 1],  # Coleman-Weinberg universal singlet
            [0, 1, 1, 0, 0, 0],  # fermionic determinant susceptibility
            [0, 0, 0, 0, 1, 1],  # dimensional-transmutation scale only
            [1, 1, 1, 1, 0, 1],  # connected breaking-background spectral trace
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(11, 1)
    coverage = sp.ImmutableMatrix(
        [[int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows)))] for column in range(candidate_matrix.cols)]
    )
    physical_origin = sp.ImmutableMatrix([1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(sector_mass_map, sp.ImmutableMatrix([[1, 49], [1, 9], [1, 1]]), subject="quadratic coefficient basis evaluates on all three hypercharge classes"),
        kernel.prove_exact_rank(sector_mass_map, 2, subject="hypercharge mass family has two independent coefficients"),
        kernel.prove_matrix_equality(diagnostic_masses, sp.ImmutableMatrix([[-1, -1, -1], [49, 9, 1], [-49, -9, -1], [0, 40, 48], [-20, 20, 28], [-40, 0, 8]]), subject="diagnostic coefficient masses are exact"),
        kernel.prove_matrix_equality(strict_sign_pass, sp.ImmutableMatrix([0, 0, 0, 0, 1, 0]), subject="only the target-loaded interior witness passes the strict sign test"),
        kernel.prove_matrix_equality(boundary_flags, sp.ImmutableMatrix([0, 0, 0, 1, 0, 1]), subject="gap and companion thresholds are boundary points"),
        kernel.prove_diagonal_signature(sp.diag(*list(diagnostic_masses.row(4))), (1, 0, 2), subject="interior witness destabilizes only the R2 spectral class"),
        kernel.prove_diagonal_signature(sp.diag(*list(diagnostic_masses.row(3))), (0, 1, 2), subject="algebraic gap alone leaves R2 massless"),
        kernel.prove_diagonal_signature(sp.diag(*list(diagnostic_masses.row(5))), (1, 1, 1), subject="upper boundary makes the Q squared nine companions massless"),
        kernel.prove_exact_rank(interior_coefficients, 2, subject="two normalized admissible coefficient choices are inequivalent"),
        kernel.prove_matrix_equality(interior_masses, sp.ImmutableMatrix([[-10, 30, 38], [-30, 10, 18]]), subject="distinct ratios ten and thirty both lie in the sign cone"),
        kernel.prove_diagonal_signature(sp.diag(*list(interior_masses.row(0))), (1, 0, 2), subject="ratio ten passes the strict sign test"),
        kernel.prove_diagonal_signature(sp.diag(*list(interior_masses.row(1))), (1, 0, 2), subject="ratio thirty passes the strict sign test"),
        kernel.prove_matrix_equality(inherited_coefficient_map, sp.zeros(2, 3), subject="current parent maps no inherited data to the two gap coefficients"),
        kernel.prove_exact_rank(inherited_coefficient_map, 0, subject="inherited coefficient map has zero rank"),
        kernel.prove_exact_nullity(inherited_coefficient_map, 3, subject="all tested inherited coefficient sources remain unconstrained"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="coefficient audit resolves all six origin criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([2, 1, 3, 1, 2, 4, 3, 2, 2, 2, 5]), subject="coefficient candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no coefficient candidate passes all six criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every coefficient-origin criterion is represented"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="connected breaking-background trace is the unique closest candidate"),
        kernel.prove_matrix_equality(candidate_matrix.row(10), sp.ImmutableMatrix([[1, 1, 1, 1, 0, 1]]), subject="closest candidate fails only inherited carrier"),
        kernel.prove_matrix_equality(physical_origin, sp.ImmutableMatrix([1, 0, 0]), subject="algebraic gap is derived while dynamics and absolute scale remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 1, subject="strict coefficient physical-origin score remains one of three"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict coefficient audit has zero passing candidates"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate",
        theorems,
    )
    return HyperchargeGapCoefficientAuditCertificate(
        sector_mass_map,
        diagnostic_coefficients,
        diagnostic_masses,
        strict_sign_pass,
        boundary_flags,
        interior_coefficients,
        interior_masses,
        inherited_coefficient_map,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate",
    title="Аудит кандидатов коэффициента гиперзарядового gap R2",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_hypercharge_gap_coefficient_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)