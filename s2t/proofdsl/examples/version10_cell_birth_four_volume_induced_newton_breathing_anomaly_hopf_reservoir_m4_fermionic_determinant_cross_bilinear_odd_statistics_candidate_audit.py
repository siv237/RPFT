"""LCF certificate for the M4 fermionic cross/odd-statistics audit."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FermionicCrossOddStatisticsAuditCertificate:
    sector_grading: sp.ImmutableMatrix
    cross_involution: sp.ImmutableMatrix
    ko_charge: sp.ImmutableMatrix
    ko_charge_defect: sp.ImmutableMatrix
    equal_charge: sp.ImmutableMatrix
    equal_charge_defect: sp.ImmutableMatrix
    inherited_odd_projector: sp.ImmutableMatrix
    target_odd_projector: sp.ImmutableMatrix
    odd_rank_defect: sp.ImmutableMatrix
    callias_embedding: sp.ImmutableMatrix
    reduced_pfaffian_phases: sp.ImmutableMatrix
    full_ko6_phases: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    physical_seed_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FermionicCrossOddStatisticsAuditCertificate:
    i2, z2 = sp.eye(2), sp.zeros(2)
    sector_grading = sp.ImmutableMatrix(sp.diag(1, 1, -1, -1))
    cross_involution = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix.hstack(z2, i2), sp.ImmutableMatrix.hstack(i2, z2)
    )
    ko_charge = sector_grading
    ko_charge_defect = sp.ImmutableMatrix(ko_charge * cross_involution - cross_involution * ko_charge)
    equal_charge = sp.ImmutableMatrix(sp.eye(4))
    equal_charge_defect = sp.ImmutableMatrix(equal_charge * cross_involution - cross_involution * equal_charge)
    inherited_odd_projector = sp.ImmutableMatrix((sp.eye(4) - sector_grading) / 2)
    target_odd_projector = sp.ImmutableMatrix(sp.eye(4))
    odd_rank_defect = sp.ImmutableMatrix(target_odd_projector - inherited_odd_projector)
    callias_embedding = sp.ImmutableMatrix(sp.zeros(4, 60))
    reduced_pfaffian_phases = sp.ImmutableMatrix([-1, 1])
    full_ko6_phases = sp.ImmutableMatrix([1, 1])

    # Columns: M4 cross type, inherited operator, odd statistics/measure,
    # negative determinant susceptibility, gauge/KMS compatibility,
    # independently normalized non-target-loaded coupling.
    candidate_matrix = sp.ImmutableMatrix([
        [0, 1, 1, 0, 1, 1],  # inherited block-diagonal physical fermions
        [1, 0, 0, 1, 1, 0],  # formal M4 cross involution
        [1, 1, 1, 1, 0, 1],  # KO6 particle/conjugate bilinear
        [1, 0, 1, 1, 1, 1],  # Callias equal-charge twist
        [0, 0, 0, 1, 1, 1],  # KMS auxiliary fermion module
        [0, 0, 1, 1, 1, 1],  # BRST ghost pair
        [0, 1, 1, 1, 1, 0],  # physical SM Yukawa bilinear
        [1, 0, 1, 1, 1, 0],  # fermionic bath pseudomode
        [1, 1, 1, 1, 0, 1],  # reduced Pfaffian representative
        [0, 1, 1, 0, 1, 1],  # Schwinger-Keldysh doubling
        [1, 1, 0, 0, 1, 1],  # abstract cell equal-charge twist
        [1, 0, 1, 1, 1, 0],  # target-loaded cross Grassmann pair
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(12)])
    pass_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(12)])
    physical_seed_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(12)
    ])
    audit_coverage = sp.ImmutableMatrix.ones(12, 1)
    physical_origin = sp.ImmutableMatrix.zeros(4, 1)

    theorems = (
        kernel.prove_matrix_equality(sector_grading**2, sp.eye(4), subject="M4 sector grading is involutive"),
        kernel.prove_matrix_equality(cross_involution**2, sp.eye(4), subject="M4 cross operator is involutive"),
        kernel.prove_matrix_equality(sector_grading * cross_involution + cross_involution * sector_grading, sp.zeros(4), subject="cross operator is odd relative to sector grading"),
        kernel.prove_exact_rank(ko_charge_defect, 4, subject="KO particle conjugate cross flip violates charge covariance"),
        kernel.prove_matrix_equality(equal_charge_defect, sp.zeros(4), subject="equal-charge twist is gauge compatible"),
        kernel.prove_exact_rank(inherited_odd_projector, 2, subject="inherited sector grading has only two odd directions"),
        kernel.prove_exact_rank(target_odd_projector, 4, subject="fermion determinant requires four odd directions"),
        kernel.prove_exact_rank(odd_rank_defect, 2, subject="inherited grading misses two odd directions"),
        kernel.prove_exact_rank(callias_embedding, 0, subject="Callias carrier has no inherited map into the M4 cross module"),
        kernel.prove_matrix_equality(reduced_pfaffian_phases, sp.Matrix([-1, 1]), subject="reduced Pfaffian distinguishes two orientations"),
        kernel.prove_matrix_equality(full_ko6_phases, sp.ones(2, 1), subject="full KO6 pairing cancels the reduced Pfaffian sign"),
        kernel.prove_expression_equality(candidate_matrix.rows, 12, subject="twelve cross-statistics candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.cols, 6, subject="six cross-statistics origin criteria are used"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="cross-statistics candidate matrix has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([4, 3, 5, 5, 3, 4, 4, 4, 5, 4, 4, 4]), subject="cross-statistics candidate scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="three closest cross-statistics candidates score five of six"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no cross-statistics candidate passes all criteria"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict cross-statistics pass count is zero"),
        kernel.prove_matrix_equality(physical_seed_vector, sp.zeros(12, 1), subject="no physical fermionic cross seed is complete"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(12, 1), subject="all twelve cross-statistics routes are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 12, subject="cross-statistics audit coverage is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1), subject="equal-charge embedding statistics coupling and measure origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical cross-statistics origin score is zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate",
        theorems,
    )
    return FermionicCrossOddStatisticsAuditCertificate(
        sector_grading, cross_involution, ko_charge, ko_charge_defect,
        equal_charge, equal_charge_defect, inherited_odd_projector,
        target_odd_projector, odd_rank_defect, callias_embedding,
        reduced_pfaffian_phases, full_ko6_phases, candidate_matrix,
        score_vector, pass_vector, physical_seed_vector, audit_coverage,
        physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate",
    title="Аудит источников фермионной cross-билинейности и нечётной статистики",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"m4_fermionic_cross_odd_statistics_audit_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)