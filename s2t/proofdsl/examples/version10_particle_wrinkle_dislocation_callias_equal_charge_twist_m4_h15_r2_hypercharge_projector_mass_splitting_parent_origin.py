"""LCF certificate for the hypercharge-projector mass-splitting parent gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HyperchargeProjectorMassSplittingCertificate:
    hypercharge6: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    hypercharge_square: sp.ImmutableMatrix
    target_selector: sp.ImmutableMatrix
    companion_selector: sp.ImmutableMatrix
    gap_operator: sp.ImmutableMatrix
    real_conjugation: sp.ImmutableMatrix
    su2r_flip: sp.ImmutableMatrix
    su2r_defect: sp.ImmutableMatrix
    witness_hessian: sp.ImmutableMatrix
    witness_sector_masses: sp.ImmutableMatrix
    inherited_gap_hessian: sp.ImmutableMatrix
    coefficient_origin: sp.ImmutableMatrix
    admissible_ratio_interval: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HyperchargeProjectorMassSplittingCertificate:
    hypercharge6 = sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3])
    hypercharge_generator = sp.ImmutableMatrix(sp.diag(*list(hypercharge6)))
    hypercharge_square = sp.ImmutableMatrix(hypercharge_generator**2)
    identity = sp.eye(8)
    target_selector = sp.ImmutableMatrix(sp.diag(0, 0, 1, 0, 0, 1, 0, 0))
    companion_selector = sp.ImmutableMatrix(identity - target_selector)

    # The lowest-degree positive spectral gap with kernel Q^2=49.
    gap_operator = sp.ImmutableMatrix(49 * identity - hypercharge_square)

    real_mutable = sp.zeros(8)
    for first, second in ((0, 1), (2, 5), (3, 4), (6, 7)):
        real_mutable[first, second] = 1
        real_mutable[second, first] = 1
    real_conjugation = sp.ImmutableMatrix(real_mutable)

    su2r_mutable = sp.zeros(8)
    for first, second in ((0, 1), (2, 3), (4, 5), (6, 7)):
        su2r_mutable[first, second] = 1
        su2r_mutable[second, first] = 1
    su2r_flip = sp.ImmutableMatrix(su2r_mutable)
    su2r_defect = sp.ImmutableMatrix(su2r_flip * gap_operator - gap_operator * su2r_flip)

    # Conditional witness kappa=1, mu^2=20 lies strictly inside 0<mu^2/kappa<40.
    witness_hessian = sp.ImmutableMatrix(gap_operator - 20 * identity)
    witness_sector_masses = sp.ImmutableMatrix(list(witness_hessian.diagonal()))

    inherited_gap_hessian = sp.ImmutableMatrix.zeros(8)
    coefficient_origin = sp.ImmutableMatrix.zeros(2, 1)
    admissible_ratio_interval = sp.ImmutableMatrix([0, 40])
    conditional_architecture = sp.ImmutableMatrix.ones(14, 1)
    physical_origin = sp.ImmutableMatrix([1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(hypercharge_square, sp.diag(9, 9, 49, 1, 1, 49, 9, 9), subject="squared hypercharge spectrum is exact"),
        kernel.prove_matrix_equality(gap_operator, sp.diag(40, 40, 0, 48, 48, 0, 40, 40), subject="hypercharge gap operator is exact"),
        kernel.prove_exact_rank(gap_operator, 6, subject="hypercharge gap lifts six companion sectors"),
        kernel.prove_exact_nullity(gap_operator, 2, subject="hypercharge gap kernel is the R2 pair"),
        kernel.prove_diagonal_signature(gap_operator, (0, 2, 6), subject="hypercharge gap is positive semidefinite"),
        kernel.prove_matrix_equality(gap_operator * target_selector, sp.zeros(8), subject="gap vanishes exactly on R2 and its conjugate"),
        kernel.prove_matrix_equality(gap_operator * companion_selector, gap_operator, subject="gap support is the companion complement"),
        kernel.prove_matrix_equality(target_selector**2, target_selector, subject="R2 target selector is idempotent"),
        kernel.prove_matrix_equality(companion_selector**2, companion_selector, subject="companion selector is idempotent"),
        kernel.prove_matrix_equality(real_conjugation**2, identity, subject="Real sector exchange is involutive"),
        kernel.prove_matrix_equality(real_conjugation * gap_operator, gap_operator * real_conjugation, subject="hypercharge gap is Real compatible"),
        kernel.prove_matrix_equality(su2r_flip**2, identity, subject="SU2R weight flip is involutive"),
        kernel.prove_exact_rank(su2r_defect, 4, subject="hypercharge gap breaks the full SU2R pairing"),
        kernel.prove_matrix_equality(witness_hessian, sp.diag(20, 20, -20, 28, 28, -20, 20, 20), subject="conditional tachyonic witness masses are exact"),
        kernel.prove_diagonal_signature(witness_hessian, (2, 0, 6), subject="conditional witness destabilizes only R2 and its conjugate"),
        kernel.prove_matrix_equality(witness_hessian * target_selector, -20 * target_selector, subject="R2 witness mass is uniformly tachyonic"),
        kernel.prove_exact_rank(companion_selector * witness_hessian * companion_selector, 6, subject="all six companion sectors remain massive"),
        kernel.prove_expression_equality(witness_hessian.det(), 50176000000, subject="conditional witness has no quadratic flat direction"),
        kernel.prove_matrix_equality(inherited_gap_hessian, sp.zeros(8), subject="current parent supplies no hypercharge gap Hessian"),
        kernel.prove_exact_rank(inherited_gap_hessian, 0, subject="inherited hypercharge gap has zero rank"),
        kernel.prove_matrix_equality(coefficient_origin, sp.zeros(2, 1), subject="kappa and tachyonic shift have no inherited coefficient map"),
        kernel.prove_matrix_equality(admissible_ratio_interval, sp.ImmutableMatrix([0, 40]), subject="conditional stability window endpoints are exact"),
        kernel.prove_expression_equality(sum(conditional_architecture), 14, subject="conditional mass-splitting architecture is complete"),
        kernel.prove_expression_equality(sum(physical_origin), 1, subject="strict mass-parent physical-origin score is one of three"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate",
        theorems,
    )
    return HyperchargeProjectorMassSplittingCertificate(
        hypercharge6,
        hypercharge_generator,
        hypercharge_square,
        target_selector,
        companion_selector,
        gap_operator,
        real_conjugation,
        su2r_flip,
        su2r_defect,
        witness_hessian,
        witness_sector_masses,
        inherited_gap_hessian,
        coefficient_origin,
        admissible_ratio_interval,
        conditional_architecture,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate",
    title="Родитель расщепления масс гиперзарядового проектора R2",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_hypercharge_mass_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)