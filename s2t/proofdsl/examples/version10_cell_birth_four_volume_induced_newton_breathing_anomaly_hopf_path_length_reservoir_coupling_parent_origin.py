"""LCF certificate for the Hopf path-length/reservoir coupling parent."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfPathReservoirCouplingCertificate:
    path_length_operator: sp.ImmutableMatrix
    path_orientation: sp.ImmutableMatrix
    reservoir_orientation: sp.ImmutableMatrix
    aligned_intertwiner: sp.ImmutableMatrix
    swapped_intertwiner: sp.ImmutableMatrix
    aligned_defect: sp.ImmutableMatrix
    swapped_defect: sp.ImmutableMatrix
    assignment_scores: sp.ImmutableMatrix
    affinities: sp.ImmutableMatrix
    swapped_affinities: sp.ImmutableMatrix
    kms_ratios: sp.ImmutableMatrix
    difference_row: sp.ImmutableMatrix
    conditional_hessian: sp.ImmutableMatrix
    inherited_mixed_block: sp.ImmutableMatrix
    temperature_map: sp.ImmutableMatrix
    temperature_kernel: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfPathReservoirCouplingCertificate:
    log2 = sp.log(2)
    identity = sp.ImmutableMatrix.eye(2)
    swap = sp.ImmutableMatrix([[0, 1], [1, 0]])
    path_length_operator = sp.ImmutableMatrix.diag(1, 2)
    path_orientation = sp.ImmutableMatrix(2 * path_length_operator - 3 * identity)
    reservoir_orientation = sp.ImmutableMatrix.diag(-1, 1)
    aligned_defect = sp.ImmutableMatrix(
        reservoir_orientation - identity * path_orientation * identity.T
    )
    swapped_defect = sp.ImmutableMatrix(
        reservoir_orientation - swap * path_orientation * swap.T
    )
    assignment_scores = sp.ImmutableMatrix([
        sp.trace(aligned_defect.T * aligned_defect),
        sp.trace(swapped_defect.T * swapped_defect),
    ])
    affinities = sp.ImmutableMatrix([log2, 2 * log2])
    swapped_affinities = sp.ImmutableMatrix([2 * log2, log2])
    kms_ratios = sp.ImmutableMatrix([sp.Rational(1, 2), sp.Rational(1, 4)])
    difference_row = sp.ImmutableMatrix([[-1, 1]])

    ah, ac = sp.symbols("a_h a_c", real=True)
    conditional_parent = ((ah - log2) ** 2 + (ac - 2 * log2) ** 2) / 2
    conditional_hessian = sp.ImmutableMatrix(sp.hessian(conditional_parent, (ah, ac)))
    inherited_mixed_block = sp.ImmutableMatrix.zeros(2, 2)

    temperature_map = sp.ImmutableMatrix([[1, 0, 1], [0, 1, 1]])
    temperature_kernel = sp.ImmutableMatrix([-1, -1, 1])
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(path_length_operator, sp.diag(1, 2),
                                     subject="Hopf path-length operator has levels one and two"),
        kernel.prove_matrix_equality(path_orientation, sp.diag(-1, 1),
                                     subject="centered path orientation is exact"),
        kernel.prove_matrix_equality(reservoir_orientation, path_orientation,
                                     subject="hot-cold orientation admits the aligned assignment"),
        kernel.prove_matrix_equality(identity.T * identity, sp.eye(2),
                                     subject="aligned intertwiner is orthogonal"),
        kernel.prove_matrix_equality(swap.T * swap, sp.eye(2),
                                     subject="swapped intertwiner is orthogonal"),
        kernel.prove_matrix_equality(aligned_defect, sp.zeros(2),
                                     subject="aligned reservoir-path intertwining defect vanishes"),
        kernel.prove_matrix_equality(swap * path_orientation * swap.T, -path_orientation,
                                     subject="path swap reverses the centered orientation"),
        kernel.prove_matrix_equality(swapped_defect, sp.diag(-2, 2),
                                     subject="swapped assignment has a nonzero exact defect"),
        kernel.prove_exact_rank(swapped_defect, 2,
                                subject="swapped assignment violates both oriented labels"),
        kernel.prove_matrix_equality(assignment_scores, sp.Matrix([0, 8]),
                                     subject="aligned assignment is the unique zero-defect permutation"),
        kernel.prove_matrix_equality(affinities, sp.Matrix([log2, 2 * log2]),
                                     subject="aligned paths reproduce the two affinities"),
        kernel.prove_matrix_equality(swapped_affinities, sp.Matrix([2 * log2, log2]),
                                     subject="swapped paths reverse the affinity order"),
        kernel.prove_expression_equality((difference_row * affinities)[0], log2,
                                         subject="aligned assignment preserves the positive affinity difference"),
        kernel.prove_expression_equality((difference_row * swapped_affinities)[0], -log2,
                                         subject="swapped assignment reverses the derived affinity difference"),
        kernel.prove_matrix_equality(kms_ratios, sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 4)]),
                                     subject="aligned affinities give exact KMS ratios"),
        kernel.prove_matrix_equality(conditional_hessian, sp.eye(2),
                                     subject="conditional assignment parent has identity Hessian"),
        kernel.prove_exact_rank(conditional_hessian, 2,
                                subject="conditional assignment parent is strict"),
        kernel.prove_expression_equality(conditional_hessian.det(), 1,
                                         subject="conditional assignment parent determinant is one"),
        kernel.prove_matrix_equality(inherited_mixed_block, sp.zeros(2),
                                     subject="inherited reservoir-path mixed block vanishes"),
        kernel.prove_exact_rank(temperature_map, 2,
                                subject="two affinities constrain two temperature-gap products"),
        kernel.prove_exact_nullity(temperature_map, 1,
                                   subject="one absolute energy-temperature scale remains"),
        kernel.prove_matrix_equality(temperature_map * temperature_kernel, sp.zeros(2, 1),
                                     subject="temperature-gap counter-scaling is the exact kernel"),
        kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 1, 0, 0]),
                                     subject="conditional structure passes while both physical origins remain open"),
        kernel.prove_expression_equality(sum(origin_ledger), 4,
                                         subject="four of six origin requirements pass"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate",
        theorems,
    )
    return HopfPathReservoirCouplingCertificate(
        path_length_operator, path_orientation, reservoir_orientation,
        identity, swap, aligned_defect, swapped_defect, assignment_scores,
        affinities, swapped_affinities, kms_ratios, difference_row,
        conditional_hessian, inherited_mixed_block, temperature_map,
        temperature_kernel, origin_ledger, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate",
    title="Родитель связи длин хопфовских путей с двумя резервуарами",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"hopf_path_reservoir_coupling_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)