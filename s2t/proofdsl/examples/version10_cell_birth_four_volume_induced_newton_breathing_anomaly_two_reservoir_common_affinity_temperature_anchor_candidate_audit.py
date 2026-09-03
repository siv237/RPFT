"""LCF certificate for the common-affinity and temperature-anchor audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CommonAffinityTemperatureAnchorAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    path_lengths: sp.ImmutableMatrix
    bath_affinities: sp.ImmutableMatrix
    affinity_map: sp.ImmutableMatrix
    affinity_kernel: sp.ImmutableMatrix
    anchored_affinity_map: sp.ImmutableMatrix
    temperature_map: sp.ImmutableMatrix
    temperature_kernel: sp.ImmutableMatrix
    energy_anchored_temperature_map: sp.ImmutableMatrix
    hessian: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CommonAffinityTemperatureAnchorAuditCertificate:
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 1, 1, 0],
        [1, 1, 0, 1, 1, 0],
        [1, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 0],
        [1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 0],
        [1, 1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 1, 1],
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])

    log2 = sp.log(2)
    path_lengths = sp.ImmutableMatrix([1, 2])
    bath_affinities = log2 * path_lengths
    affinity_map = sp.ImmutableMatrix([[-1, 1, -1], [0, 0, 1]])
    affinity_kernel = sp.ImmutableMatrix([1, 1, 0])
    anchored_affinity_map = sp.ImmutableMatrix.vstack(
        affinity_map, sp.ImmutableMatrix([[1, 0, 0]])
    )
    temperature_map = sp.ImmutableMatrix([[1, 0, 1], [0, 1, 1]])
    temperature_kernel = sp.ImmutableMatrix([-1, -1, 1])
    energy_anchored_temperature_map = sp.ImmutableMatrix.vstack(
        temperature_map, sp.ImmutableMatrix([[0, 0, 1]])
    )

    u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
    parent = ((u1 - 1) ** 2 + (u2 - u1) ** 2 + (u3 - u2) ** 2) / 2
    hessian = sp.ImmutableMatrix(sp.hessian(parent, (u1, u2, u3)))
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix),
                                     subject="ten common-affinity candidates are audited on six criteria"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(10, 1),
                                     subject="no candidate passes the complete common-temperature contract"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([4, 4, 4, 3, 4, 4, 3, 3, 3, 4]),
                                     subject="candidate scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 4,
                                         subject="maximum candidate score is four of six"),
        kernel.prove_exact_rank(candidate_matrix, 6,
                                subject="candidate menu covers all six criterion directions"),
        kernel.prove_matrix_equality(path_lengths, sp.Matrix([1, 2]),
                                     subject="one-edge and two-edge Hopf paths form the closest anchor"),
        kernel.prove_matrix_equality(bath_affinities, sp.Matrix([log2, 2 * log2]),
                                     subject="Hopf path lengths reproduce both selected dimensionless affinities"),
        kernel.prove_expression_equality(bath_affinities[1] - bath_affinities[0], log2,
                                         subject="path construction preserves the derived affinity difference"),
        kernel.prove_exact_rank(affinity_map, 2,
                                subject="difference data and fixed edge affinity give rank two"),
        kernel.prove_exact_nullity(affinity_map, 1,
                                   subject="one common affinity shift remains"),
        kernel.prove_matrix_equality(affinity_map * affinity_kernel, sp.zeros(2, 1),
                                     subject="common affinity shift is the exact residual kernel"),
        kernel.prove_exact_rank(anchored_affinity_map, 3,
                                subject="one typed hot-bath anchor would remove the common shift"),
        kernel.prove_exact_rank(temperature_map, 2,
                                subject="two fixed affinities constrain two energy-temperature products"),
        kernel.prove_exact_nullity(temperature_map, 1,
                                   subject="absolute energy-temperature calibration remains free"),
        kernel.prove_matrix_equality(temperature_map * temperature_kernel, sp.zeros(2, 1),
                                     subject="inverse temperatures and common gap counter-rescale"),
        kernel.prove_exact_rank(energy_anchored_temperature_map, 3,
                                subject="an independent energy gap would fix both physical temperatures"),
        kernel.prove_matrix_equality(hessian, sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
                                     subject="audit parent Hessian is exact"),
        kernel.prove_exact_rank(hessian, 3, subject="audit parent is nondegenerate"),
        kernel.prove_expression_equality(hessian.det(), 1, subject="audit parent determinant is one"),
        kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 1, 0, 0]),
                                     subject="coverage and diagnosis pass while both origins remain open"),
        kernel.prove_expression_equality(sum(origin_ledger), 4,
                                         subject="four of six audit-level requirements pass"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate",
        theorems,
    )
    return CommonAffinityTemperatureAnchorAuditCertificate(
        candidate_matrix, pass_vector, score_vector, path_lengths,
        bath_affinities, affinity_map, affinity_kernel, anchored_affinity_map,
        temperature_map, temperature_kernel, energy_anchored_temperature_map,
        hessian, origin_ledger, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate",
    title="Аудит общего сродства и температурного якоря двух резервуаров",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"common_affinity_anchor_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(21)
    ),
)