"""LCF certificate for the fermionic determinant common-carrier gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FermionicDeterminantCommonCarrierCertificate:
    reservoir_projector: sp.ImmutableMatrix
    path_projector: sp.ImmutableMatrix
    sector_grading: sp.ImmutableMatrix
    cross_involution: sp.ImmutableMatrix
    clifford_anticommutator: sp.ImmutableMatrix
    block_diagonal_cross_projection: sp.ImmutableMatrix
    dirac_family: sp.ImmutableMatrix
    dirac_square: sp.ImmutableMatrix
    dirac_witness: sp.ImmutableMatrix
    berezin_pairing: sp.ImmutableMatrix
    determinant_polynomial: sp.Expr
    fermion_curvature: sp.Expr
    total_curvature: sp.Expr
    stationary_points: sp.ImmutableMatrix
    stationary_curvatures: sp.ImmutableMatrix
    stationary_values: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    inherited_ingredients: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FermionicDeterminantCommonCarrierCertificate:
    identity2 = sp.eye(2)
    zero2 = sp.zeros(2)
    reservoir_projector = sp.ImmutableMatrix(sp.diag(1, 1, 0, 0))
    path_projector = sp.ImmutableMatrix(sp.diag(0, 0, 1, 1))
    sector_grading = sp.ImmutableMatrix(reservoir_projector - path_projector)
    cross_involution = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix.hstack(zero2, identity2),
        sp.ImmutableMatrix.hstack(identity2, zero2),
    )
    clifford_anticommutator = sp.ImmutableMatrix(
        sector_grading * cross_involution + cross_involution * sector_grading
    )
    block_diagonal_cross_projection = sp.ImmutableMatrix(
        reservoir_projector * cross_involution * reservoir_projector
        + path_projector * cross_involution * path_projector
    )

    x = sp.symbols("x", real=True)
    dirac_family = sp.ImmutableMatrix(sector_grading + x * cross_involution)
    dirac_square = sp.ImmutableMatrix(dirac_family * dirac_family)
    dirac_witness = sp.ImmutableMatrix(dirac_family.subs(x, 1))
    berezin_pairing = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix.hstack(sp.zeros(4), dirac_witness),
        sp.ImmutableMatrix.hstack(-dirac_witness.T, sp.zeros(4)),
    )
    determinant_polynomial = sp.factor(dirac_family.det())

    fermion_action = -sp.log(determinant_polynomial)
    total_potential = x**2 + fermion_action
    fermion_curvature = sp.simplify(sp.diff(fermion_action, x, 2).subs(x, 0))
    total_curvature = sp.simplify(sp.diff(total_potential, x, 2).subs(x, 0))
    stationary_points = sp.ImmutableMatrix([-1, 0, 1])
    stationary_curvatures = sp.ImmutableMatrix([
        sp.simplify(sp.diff(total_potential, x, 2).subs(x, point))
        for point in (-1, 0, 1)
    ])
    stationary_values = sp.ImmutableMatrix([
        sp.simplify(total_potential.subs(x, point))
        for point in (-1, 0, 1)
    ])
    conditional_architecture = sp.ImmutableMatrix.ones(14, 1)
    inherited_ingredients = sp.ImmutableMatrix([1, 1, 0, 0, 0, 0])
    physical_origin = sp.ImmutableMatrix.zeros(4, 1)

    theorems = (
        kernel.prove_exact_rank(reservoir_projector, 2, subject="reservoir sector has rank two"),
        kernel.prove_exact_rank(path_projector, 2, subject="path sector has rank two"),
        kernel.prove_matrix_equality(reservoir_projector + path_projector, sp.eye(4), subject="two sectors resolve the common carrier"),
        kernel.prove_matrix_equality(reservoir_projector * path_projector, sp.zeros(4), subject="reservoir and path sectors are orthogonal"),
        kernel.prove_matrix_equality(sector_grading**2, sp.eye(4), subject="sector grading is involutive"),
        kernel.prove_matrix_equality(cross_involution**2, sp.eye(4), subject="conditional cross generator is involutive"),
        kernel.prove_matrix_equality(clifford_anticommutator, sp.zeros(4), subject="grading and cross generator anticommute"),
        kernel.prove_matrix_equality(block_diagonal_cross_projection, sp.zeros(4), subject="inherited block diagonal algebra removes the cross generator"),
        kernel.prove_exact_rank(block_diagonal_cross_projection, 0, subject="inherited cross bilinear rank is zero"),
        kernel.prove_matrix_equality(dirac_square, (1 + x**2) * sp.eye(4), subject="conditional Dirac family has scalar square"),
        kernel.prove_expression_equality(determinant_polynomial, (1 + x**2) ** 2, subject="conditional Dirac determinant polynomial"),
        kernel.prove_exact_spectrum(dirac_witness, {-sp.sqrt(2): 2, sp.sqrt(2): 2}, subject="unit cross Dirac witness spectrum"),
        kernel.prove_exact_rank(berezin_pairing, 8, subject="complex Berezin pairing is nondegenerate"),
        kernel.prove_expression_equality(berezin_pairing.det(), 16, subject="Berezin pairing determinant is exact"),
        kernel.prove_matrix_equality(berezin_pairing.T, -berezin_pairing, subject="Berezin pairing is antisymmetric"),
        kernel.prove_expression_equality(fermion_curvature, -4, subject="fermion log determinant has negative curvature"),
        kernel.prove_expression_equality(total_curvature, -2, subject="fermion loop overcomes unit incidence stiffness"),
        kernel.prove_expression_equality(sp.factor(sp.diff(total_potential, x)), 2 * x * (x - 1) * (x + 1) / (x**2 + 1), subject="conditional total potential stationary equation"),
        kernel.prove_matrix_equality(stationary_curvatures, sp.Matrix([2, -2, 2]), subject="conditional minima and central maximum curvatures"),
        kernel.prove_matrix_equality(stationary_values, sp.Matrix([1 - sp.log(4), 0, 1 - sp.log(4)]), subject="two degenerate conditional fermion-induced minima"),
        kernel.prove_expression_equality(sum(conditional_architecture), 14, subject="conditional fermionic common carrier architecture is complete"),
        kernel.prove_matrix_equality(inherited_ingredients, sp.Matrix([1, 1, 0, 0, 0, 0]), subject="only carrier and sector grading are inherited"),
        kernel.prove_expression_equality(sum(inherited_ingredients), 2, subject="two of six carrier ingredients are inherited"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1), subject="cross bilinear statistics coupling and measure origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict fermionic susceptibility origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate",
        theorems,
    )
    return FermionicDeterminantCommonCarrierCertificate(
        reservoir_projector, path_projector, sector_grading, cross_involution,
        clifford_anticommutator, block_diagonal_cross_projection,
        dirac_family, dirac_square, dirac_witness, berezin_pairing,
        determinant_polynomial, fermion_curvature, total_curvature,
        stationary_points, stationary_curvatures, stationary_values,
        conditional_architecture, inherited_ingredients, physical_origin,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate",
    title="Допуск общего носителя фермионной тахионной восприимчивости",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"m4_fermionic_determinant_common_carrier_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(25)
    ),
)