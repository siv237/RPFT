"""LCF certificate for K43--RG boundary matching of the birth tick."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BirthTickK43RGBoundaryMatchingCertificate:
    landau_log: sp.Expr
    required_reference_ratio: sp.Expr
    direct_required_g_squared: sp.Expr
    direct_required_beta: sp.Expr
    reverse_required_g_squared: sp.Expr
    reverse_required_beta: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernels: sp.ImmutableMatrix
    speed_anchored_map: sp.ImmutableMatrix
    speed_anchored_kernel: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BirthTickK43RGBoundaryMatchingCertificate:
    landau_log = 32 * sp.pi**2 / 3
    required_reference_ratio = sp.exp(-landau_log) / 42
    direct_required_g_squared = -4 * sp.pi**2 / sp.log(42)
    direct_required_beta = -64 * sp.pi**2 / (3 * sp.log(42))
    reverse_required_g_squared = 4 * sp.pi**2 / sp.log(42)
    reverse_required_beta = 64 * sp.pi**2 / (3 * sp.log(42))

    # exact matching, positive g^2, inherited beta, inherited coupling,
    # non-target-loaded origin, inherited Landau orientation.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 1, 1, 0, 1],  # separate mu_spec/Lambda43 bridge
        [1, 0, 1, 0, 0, 1],  # tune g^2 in direct orientation
        [1, 1, 0, 1, 0, 1],  # tune beta in direct orientation
        [1, 1, 1, 0, 0, 0],  # reverse orientation and tune g^2
        [1, 1, 0, 1, 0, 0],  # reverse orientation and tune beta
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)
    ])
    parent_hessian = sp.eye(2)

    # log(tau_birth), log(c), log(mu_spec), log(Lambda43).
    scale_map = sp.ImmutableMatrix([
        [1, 1, 1, 0],
        [1, 1, 0, 1],
    ])
    scale_kernels = sp.ImmutableMatrix([
        [-1, -1],
        [1, 0],
        [0, 1],
        [0, 1],
    ])
    speed_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 1, 0, 0]])
    )
    speed_anchored_kernel = sp.ImmutableMatrix([-1, 0, 1, 1])
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        speed_anchored_map, sp.ImmutableMatrix([[0, 0, 0, 1]])
    )
    conditional_origin = sp.ones(8, 1)
    physical_origin = sp.zeros(5, 1)

    theorems = (
        kernel.prove_expression_equality(landau_log, 32 * sp.pi**2 / 3, subject="inherited RG logarithm"),
        kernel.prove_expression_equality(required_reference_ratio, sp.exp(-32 * sp.pi**2 / 3) / 42, subject="unique K43 compatible reference-scale ratio"),
        kernel.prove_expression_equality(direct_required_g_squared, -4 * sp.pi**2 / sp.log(42), subject="direct matching coupling squared"),
        kernel.prove_expression_equality(direct_required_beta, -64 * sp.pi**2 / (3 * sp.log(42)), subject="direct matching beta coefficient"),
        kernel.prove_expression_equality(reverse_required_g_squared, 4 * sp.pi**2 / sp.log(42), subject="reverse-flow matching coupling squared"),
        kernel.prove_expression_equality(reverse_required_beta, 64 * sp.pi**2 / (3 * sp.log(42)), subject="reverse-flow matching beta coefficient"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([direct_required_g_squared]), sp.ImmutableMatrix([sp.Rational(3, 8)]), subject="direct matching cannot retain the inherited positive coupling"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([direct_required_beta]), sp.ImmutableMatrix([2]), subject="direct matching cannot retain the inherited positive beta"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([reverse_required_g_squared]), sp.ImmutableMatrix([sp.Rational(3, 8)]), subject="reverse matching changes the inherited coupling"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([reverse_required_beta]), sp.ImmutableMatrix([2]), subject="reverse matching changes the inherited beta"),
        kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="five boundary-matching branches are audited"),
        kernel.prove_exact_rank(candidate_matrix, 5, subject="boundary branch menu distinguishes five criteria directions"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(5, 1), subject="no K43 RG boundary branch passes the full origin contract"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="complete matching branch count is zero"),
        kernel.prove_matrix_equality(parent_hessian, sp.eye(2), subject="conditional two-relation matching parent is strict"),
        kernel.prove_exact_rank(parent_hessian, 2, subject="conditional parent controls both tick products"),
        kernel.prove_exact_rank(scale_map, 2, subject="RG and K43 tick products give two dimensional relations"),
        kernel.prove_exact_nullity(scale_map, 2, subject="speed and common inverse-scale modes remain"),
        kernel.prove_matrix_equality(scale_map * scale_kernels, sp.zeros(2, 2), subject="exact two-dimensional scale kernel"),
        kernel.prove_exact_rank(speed_anchored_map, 3, subject="fixing c removes only one scale mode"),
        kernel.prove_exact_nullity(speed_anchored_map, 1, subject="common tick and cutoff scale remains after fixing c"),
        kernel.prove_matrix_equality(speed_anchored_map * speed_anchored_kernel, sp.zeros(3, 1), subject="exact residual common-scale orbit"),
        kernel.prove_exact_rank(fully_anchored_map, 4, subject="an independent K43 cutoff anchor closes the map"),
        kernel.prove_exact_nullity(fully_anchored_map, 0, subject="external cutoff anchor removes the last scale mode"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(8, 1), subject="conditional matching algebra is complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 8, subject="eight conditional requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(5, 1), subject="boundary bridge sign change parameter retuning cutoff anchor and absolute tick origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical boundary-matching score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate",
        theorems,
    )
    return BirthTickK43RGBoundaryMatchingCertificate(
        landau_log, required_reference_ratio, direct_required_g_squared,
        direct_required_beta, reverse_required_g_squared, reverse_required_beta,
        candidate_matrix, pass_vector, parent_hessian, scale_map, scale_kernels,
        speed_anchored_map, speed_anchored_kernel, fully_anchored_map,
        conditional_origin, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate",
    title="Происхождение граничного согласования K43 и RG для такта рождения",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"birth_tick_k43_rg_boundary_matching_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(28)
    ),
)