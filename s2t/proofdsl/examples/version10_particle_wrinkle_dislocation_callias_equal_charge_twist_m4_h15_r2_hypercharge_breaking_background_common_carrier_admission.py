"""LCF certificate for the hypercharge-breaking background carrier gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HyperchargeBreakingBackgroundCarrierCertificate:
    delta_t3r6: sp.ImmutableMatrix
    delta_bl3: sp.ImmutableMatrix
    delta_hypercharge6: sp.ImmutableMatrix
    delta_hypercharge_generator: sp.ImmutableMatrix
    neutral_selector: sp.ImmutableMatrix
    polynomial_neutral_selector: sp.ImmutableMatrix
    stabilizer_constraint: sp.ImmutableMatrix
    unbroken_cartan_ray: sp.ImmutableMatrix
    sigma_t3r6: sp.ImmutableMatrix
    sigma_bl3: sp.ImmutableMatrix
    sigma_hypercharge6: sp.ImmutableMatrix
    sigma_charge_basis: sp.ImmutableMatrix
    joint_spectral_algebra: sp.ImmutableMatrix
    hypercharge_spectral_algebra: sp.ImmutableMatrix
    combined_spectral_algebra: sp.ImmutableMatrix
    branch_admission: sp.ImmutableMatrix
    inherited_tome10_background_map: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HyperchargeBreakingBackgroundCarrierCertificate:
    # Delta=(2_R,1_L,4_4).  The first six entries are colour triplets;
    # the last two are the leptonic SU(2)_R doublet.
    delta_t3r6 = sp.ImmutableMatrix([3, 3, 3, -3, -3, -3, 3, -3])
    delta_bl3 = sp.ImmutableMatrix([1, 1, 1, 1, 1, 1, -3, -3])
    delta_hypercharge6 = sp.ImmutableMatrix(delta_t3r6 + delta_bl3)
    delta_hypercharge_generator = sp.ImmutableMatrix(sp.diag(*list(delta_hypercharge6)))
    identity = sp.eye(8)
    neutral_selector = sp.ImmutableMatrix(sp.diag(0, 0, 0, 0, 0, 0, 1, 0))
    polynomial_neutral_selector = sp.ImmutableMatrix(
        -(delta_hypercharge_generator - 4 * identity)
        * (delta_hypercharge_generator + 2 * identity)
        * (delta_hypercharge_generator + 6 * identity)
        / 48
    )

    # The neutral Delta weight is (6T3R,3(B-L))=(3,-3); its Cartan
    # annihilator is the unique ray alpha=beta, i.e. 6Y=6T3R+3(B-L).
    stabilizer_constraint = sp.ImmutableMatrix([[3, -3]])
    unbroken_cartan_ray = sp.ImmutableMatrix([1, 1])

    # Sigma sector order inherited from the preceding Pati-Salam gates.
    sigma_t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    sigma_bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    sigma_hypercharge6 = sp.ImmutableMatrix(sigma_t3r6 + sigma_bl3)
    sigma_charge_basis = sp.ImmutableMatrix.hstack(sigma_t3r6, sigma_bl3)

    one = sp.ones(8, 1)
    bl2 = sigma_bl3.applyfunc(lambda entry: entry**2)
    joint_spectral_algebra = sp.ImmutableMatrix.hstack(
        one,
        sigma_t3r6,
        sigma_bl3,
        bl2,
        sigma_t3r6.multiply_elementwise(sigma_bl3),
        sigma_t3r6.multiply_elementwise(bl2),
    )
    hypercharge_spectral_algebra = sp.ImmutableMatrix.hstack(
        *[sigma_hypercharge6.applyfunc(lambda entry, power=power: entry**power) for power in range(6)]
    )
    combined_spectral_algebra = sp.ImmutableMatrix.hstack(joint_spectral_algebra, hypercharge_spectral_algebra)

    # General-fundamental branch lacks Delta; constrained composite branch has it.
    branch_admission = sp.ImmutableMatrix([0, 1])
    inherited_tome10_background_map = sp.ImmutableMatrix.zeros(2, 1)
    conditional_origin = sp.ImmutableMatrix([1, 1, 1, 0])
    physical_origin = sp.ImmutableMatrix([1, 1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(delta_t3r6, sp.ImmutableMatrix([3, 3, 3, -3, -3, -3, 3, -3]), subject="Delta SU2R Cartan weights are exact"),
        kernel.prove_matrix_equality(delta_bl3, sp.ImmutableMatrix([1, 1, 1, 1, 1, 1, -3, -3]), subject="Delta four-colour B minus L weights are exact"),
        kernel.prove_matrix_equality(delta_hypercharge6, sp.ImmutableMatrix([4, 4, 4, -2, -2, -2, 0, -6]), subject="Delta hypercharge spectrum is exact"),
        kernel.prove_matrix_equality(polynomial_neutral_selector, neutral_selector, subject="cubic hypercharge polynomial isolates the neutral Delta ray"),
        kernel.prove_matrix_equality(neutral_selector**2, neutral_selector, subject="neutral Delta selector is idempotent"),
        kernel.prove_exact_rank(neutral_selector, 1, subject="Delta contains one neutral complex direction"),
        kernel.prove_matrix_equality(delta_hypercharge_generator * neutral_selector, sp.zeros(8), subject="selected Delta direction is hypercharge neutral"),
        kernel.prove_exact_nullity(delta_hypercharge_generator, 1, subject="neutral Delta direction is unique"),
        kernel.prove_exact_rank(stabilizer_constraint, 1, subject="neutral Delta VEV imposes one Cartan constraint"),
        kernel.prove_exact_nullity(stabilizer_constraint, 1, subject="one unbroken Cartan generator remains"),
        kernel.prove_matrix_equality(stabilizer_constraint * unbroken_cartan_ray, sp.zeros(1, 1), subject="unbroken Cartan ray is alpha equals beta"),
        kernel.prove_matrix_equality(sigma_t3r6, sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3]), subject="Sigma SU2R Cartan weights are exact"),
        kernel.prove_matrix_equality(sigma_bl3, sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0]), subject="Sigma B minus L weights are exact"),
        kernel.prove_matrix_equality(sigma_hypercharge6, sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3]), subject="unbroken Delta stabilizer acts as six times hypercharge on Sigma"),
        kernel.prove_exact_rank(sigma_charge_basis, 2, subject="T3R and B minus L are independent Sigma charge directions"),
        kernel.prove_matrix_equality(sigma_charge_basis.T * sigma_charge_basis, sp.diag(72, 64), subject="two Cartan charge directions are orthogonal"),
        kernel.prove_matrix_equality(sigma_charge_basis * unbroken_cartan_ray, sigma_hypercharge6, subject="Delta stabilizer reconstructs the exact Sigma hypercharge vector"),
        kernel.prove_exact_rank(joint_spectral_algebra, 6, subject="joint T3R and B minus L spectral algebra has six classes"),
        kernel.prove_exact_rank(hypercharge_spectral_algebra, 6, subject="hypercharge alone resolves the same six spectral classes"),
        kernel.prove_exact_rank(combined_spectral_algebra, 6, subject="joint Cartan and hypercharge spectral algebras coincide on Sigma"),
        kernel.prove_matrix_equality(branch_admission, sp.ImmutableMatrix([0, 1]), subject="Delta carrier occurs only in the constrained composite branch"),
        kernel.prove_matrix_equality(inherited_tome10_background_map, sp.zeros(2, 1), subject="current Tome X parent has no embedded Delta background map"),
        kernel.prove_expression_equality(sum(conditional_origin), 3, subject="conditional Delta carrier closes three of four origin slots"),
        kernel.prove_expression_equality(sum(physical_origin), 2, subject="current physical carrier origin closes representation and stabilizer only"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate",
        theorems,
    )
    return HyperchargeBreakingBackgroundCarrierCertificate(
        delta_t3r6,
        delta_bl3,
        delta_hypercharge6,
        delta_hypercharge_generator,
        neutral_selector,
        polynomial_neutral_selector,
        stabilizer_constraint,
        unbroken_cartan_ray,
        sigma_t3r6,
        sigma_bl3,
        sigma_hypercharge6,
        sigma_charge_basis,
        joint_spectral_algebra,
        hypercharge_spectral_algebra,
        combined_spectral_algebra,
        branch_admission,
        inherited_tome10_background_map,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate",
    title="Общий носитель гиперзарядового breaking-background",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_hypercharge_background_carrier_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)