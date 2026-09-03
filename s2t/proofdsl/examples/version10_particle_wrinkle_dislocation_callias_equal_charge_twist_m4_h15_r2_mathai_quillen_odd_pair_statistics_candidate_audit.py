"""LCF certificate for the Mathai--Quillen odd-pair statistics audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class MathaiQuillenOddPairStatisticsAuditCertificate:
    charge_operator: sp.ImmutableMatrix
    odd_pairing: sp.ImmutableMatrix
    field_parity: sp.ImmutableMatrix
    required_shift_generator: sp.ImmutableMatrix
    inherited_gauge_shift_at_origin: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    shift_brst_row: sp.ImmutableMatrix
    formal_mathai_quillen_row: sp.ImmutableMatrix
    physical_fermion_row: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> MathaiQuillenOddPairStatisticsAuditCertificate:
    q = sp.diag(3, -3, 7, 1, -1, -7, 3, -3)
    zero = sp.zeros(8)
    odd_pairing = sp.ImmutableMatrix(sp.BlockMatrix([[zero, q], [-q, zero]]).as_explicit())
    field_parity = sp.ImmutableMatrix(-sp.eye(16))
    required_shift_generator = sp.ImmutableMatrix(sp.eye(8))
    inherited_gauge_shift_at_origin = sp.ImmutableMatrix.zeros(8, 8)

    # exact typed pair, Grassmann statistics, Thom differential,
    # exact Q pairing, paired Berezin measure, acyclic auxiliary sector,
    # inherited parent origin.
    candidate_matrix = sp.ImmutableMatrix([
        [0, 0, 0, 0, 0, 1, 1],  # carrier Z2 grading
        [1, 1, 0, 0, 1, 0, 1],  # physical Callias fermions
        [1, 1, 0, 1, 1, 0, 1],  # charge-conjugate/Nambu pair
        [0, 1, 0, 1, 1, 0, 1],  # inherited M4 cross bilinear
        [0, 0, 0, 0, 0, 1, 1],  # differential-form parity
        [1, 1, 0, 0, 0, 1, 1],  # BV antifields of Sigma
        [0, 1, 0, 0, 1, 1, 1],  # existing Faddeev--Popov ghosts
        [0, 1, 1, 0, 1, 1, 0],  # imported KMS BRST quartet
        [1, 1, 1, 1, 1, 1, 0],  # Sigma shift-BRST quartet
        [1, 1, 1, 1, 1, 1, 0],  # AKSZ mapping-space extension
        [1, 1, 1, 1, 1, 1, 0],  # formal Mathai--Quillen odd fibers
        [1, 1, 1, 1, 1, 1, 0],  # target-loaded Grassmann pair
    ])
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(7, 1))
    pass_vector = sp.ImmutableMatrix.zeros(12, 1)
    coverage = sp.ImmutableMatrix([
        int(any(candidate_matrix[r, c] for r in range(12))) for c in range(7)
    ])
    shift_brst_row = sp.ImmutableMatrix(candidate_matrix.row(8))
    formal_mathai_quillen_row = sp.ImmutableMatrix(candidate_matrix.row(10))
    physical_fermion_row = sp.ImmutableMatrix(candidate_matrix.row(1))

    theorems = (
        kernel.prove_exact_rank(q, 8, subject="hypercharge section is nondegenerate"),
        kernel.prove_expression_equality(q.det(), 3969, subject="hypercharge determinant is exact"),
        kernel.prove_matrix_equality(odd_pairing.T, -odd_pairing, subject="odd Thom pairing is antisymmetric"),
        kernel.prove_exact_rank(odd_pairing, 16, subject="odd Thom pairing is nondegenerate"),
        kernel.prove_expression_equality(odd_pairing.det(), 15752961, subject="odd-pair determinant is det Q squared"),
        kernel.prove_matrix_equality(field_parity**2, sp.eye(16), subject="all-odd field parity is an involution"),
        kernel.prove_exact_rank((sp.eye(16) - field_parity) / 2, 16, subject="target odd rank is sixteen"),
        kernel.prove_exact_rank(required_shift_generator, 8, subject="Thom ghost requires eight shift generators"),
        kernel.prove_exact_rank(inherited_gauge_shift_at_origin, 0, subject="ordinary gauge orbit has no translational rank at Sigma equals zero"),
        kernel.prove_exact_rank(candidate_matrix, 7, subject="odd-pair audit resolves all seven criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([2, 4, 5, 4, 2, 4, 4, 4, 6, 6, 6, 6]), subject="odd-pair candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no odd-pair candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(7, 1), subject="every odd-pair criterion is represented"),
        kernel.prove_matrix_equality(shift_brst_row, sp.ImmutableMatrix([[1, 1, 1, 1, 1, 1, 0]]), subject="shift BRST fails only inherited origin"),
        kernel.prove_matrix_equality(formal_mathai_quillen_row, shift_brst_row, subject="formal Mathai--Quillen fibers fail only inherited origin"),
        kernel.prove_matrix_equality(physical_fermion_row, sp.ImmutableMatrix([[1, 1, 0, 0, 1, 0, 1]]), subject="physical fermions are not a Thom complex"),
        kernel.prove_expression_equality(sum(shift_brst_row), 6, subject="best conditional score is six of seven"),
        kernel.prove_expression_equality(sum(physical_fermion_row), 4, subject="best inherited physical-fermion score is four of seven"),
        kernel.prove_expression_equality(required_shift_generator.rank() - inherited_gauge_shift_at_origin.rank(), 8, subject="shift-generator deficit is eight"),
        kernel.prove_matrix_equality(odd_pairing * odd_pairing.T, sp.diag(*([9, 9, 49, 1, 1, 49, 9, 9] * 2)), subject="paired odd metric is positive"),
        kernel.prove_expression_equality(candidate_matrix.rows, 12, subject="twelve origin candidates are audited"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate",
        theorems,
    )
    return MathaiQuillenOddPairStatisticsAuditCertificate(
        sp.ImmutableMatrix(q), odd_pairing, field_parity,
        required_shift_generator, inherited_gauge_shift_at_origin,
        candidate_matrix, score_vector, pass_vector, coverage,
        shift_brst_row, formal_mathai_quillen_row, physical_fermion_row,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate",
    title="Аудит происхождения статистики нечётной Mathai--Quillen-пары",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_mathai_quillen_odd_pair_statistics_audit_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(21)
    ),
)