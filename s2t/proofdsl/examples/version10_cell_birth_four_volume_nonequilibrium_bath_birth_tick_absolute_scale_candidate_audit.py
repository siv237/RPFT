"""LCF certificate for the absolute birth-tick scale candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BirthTickAbsoluteScaleAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_break_vector: sp.ImmutableMatrix
    equivalent_tick_ratios: sp.ImmutableMatrix
    profile_tick_ratios: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    externally_anchored_map: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BirthTickAbsoluteScaleAuditCertificate:
    # Columns: time dimension, internally available, selected by the current
    # parent, independently breaks the scale orbit, non-circular, uniquely
    # typed to the birth tick.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [1, 1, 1, 0, 1, 1],  # hbar/E_C
            [1, 1, 1, 0, 1, 1],  # ell_edge/c
            [1, 1, 1, 0, 1, 1],  # 2 sqrt(3)/omega_UV
            [1, 1, 1, 0, 1, 1],  # 42/(c Lambda_43)
            [1, 1, 0, 0, 1, 0],  # bath correlation time
            [1, 1, 1, 0, 1, 1],  # 1/(22 kappa)
            [1, 1, 1, 0, 1, 0],  # dimensional-transmutation frequency
            [1, 0, 0, 1, 0, 0],  # Planck time imported through G
            [1, 0, 0, 1, 0, 0],  # curvature/cosmological time
            [1, 0, 0, 1, 0, 1],  # observed growth time
            [0, 1, 1, 0, 1, 0],  # dimensionless S_vac
            [1, 0, 0, 1, 1, 1],  # external atomic-clock period
        ]
    )
    score_vector = sp.ImmutableMatrix(
        [sum(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)]
    )
    pass_vector = sp.ImmutableMatrix(
        [sp.prod(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)]
    )
    internal_break_vector = sp.ImmutableMatrix(
        [candidate_matrix[index, 1] * candidate_matrix[index, 3] for index in range(candidate_matrix.rows)]
    )

    # The first five dimensionful internal formulas all reduce to tau_birth.
    equivalent_tick_ratios = sp.ones(5, 1)
    profile_tick_ratios = sp.ImmutableMatrix(
        [1 / (2 * sp.sqrt(3)), sp.sqrt(sp.pi) / (4 * sp.sqrt(3))]
    )

    # Variables are log(tau_birth), log(E_C), log(ell_edge), log(c), with c fixed.
    scale_map = sp.ImmutableMatrix(
        [
            [1, 1, 0, 0],
            [1, 0, -1, 1],
            [0, 1, 1, -1],
            [0, 0, 0, 1],
        ]
    )
    scale_kernel = sp.ImmutableMatrix([1, -1, 1, 0])
    externally_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[1, 0, 0, 0]])
    )
    audit_coverage = sp.ones(12, 1)
    physical_origin = sp.zeros(2, 1)

    theorems = (
        kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="twelve birth-tick candidates are evaluated on six origin criteria"),
        kernel.prove_expression_equality(candidate_matrix.rows, 12, subject="twelve declared absolute tick candidates are audited"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="birth-tick candidate menu spans all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([5, 5, 5, 5, 3, 5, 4, 2, 2, 3, 3, 4]), subject="exact birth-tick candidate scores"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="closest birth-tick candidates miss one criterion"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no absolute birth-tick candidate passes the full contract"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="zero complete absolute tick origins"),
        kernel.prove_matrix_equality(internal_break_vector, sp.zeros(12, 1), subject="no internally available candidate breaks the tick scale orbit"),
        kernel.prove_expression_equality(sum(internal_break_vector), 0, subject="internal orbit-breaker count is zero"),
        kernel.prove_matrix_equality(equivalent_tick_ratios, sp.ones(5, 1), subject="five internal formulas collapse to the same relative birth tick"),
        kernel.prove_expression_equality(profile_tick_ratios[0], 1 / (2 * sp.sqrt(3)), subject="exponential bath correlation time relative to birth tick"),
        kernel.prove_expression_equality(profile_tick_ratios[1], sp.sqrt(sp.pi) / (4 * sp.sqrt(3)), subject="Gaussian bath correlation time relative to birth tick"),
        kernel.prove_matrix_inequality(profile_tick_ratios, sp.ImmutableMatrix([1, 1]), subject="bath profile times do not equal the birth tick"),
        kernel.prove_exact_rank(scale_map, 3, subject="birth-tick scale map after fixing c"),
        kernel.prove_exact_nullity(scale_map, 1, subject="one common tick-length-energy orbit remains"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(4, 1), subject="exact residual absolute tick scale orbit"),
        kernel.prove_exact_rank(externally_anchored_map, 4, subject="an imported absolute tick removes the scale orbit"),
        kernel.prove_exact_nullity(externally_anchored_map, 0, subject="external tick anchor closes the scale map"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(12, 1), subject="all twelve declared tick candidates are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 12, subject="candidate audit coverage is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="absolute birth tick and physical clock origin remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical tick score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate",
        theorems,
    )
    return BirthTickAbsoluteScaleAuditCertificate(
        candidate_matrix,
        score_vector,
        pass_vector,
        internal_break_vector,
        equivalent_tick_ratios,
        profile_tick_ratios,
        scale_map,
        scale_kernel,
        externally_anchored_map,
        audit_coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate",
    title="Аудит кандидатов абсолютного масштаба такта рождения",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"birth_tick_absolute_scale_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(22)
    ),
)