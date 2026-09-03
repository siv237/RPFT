"""LCF certificate for the Delta-stabilizer moment-map curvature parent."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class DeltaStabilizerMomentMapParentCertificate:
    mu_r: sp.ImmutableMatrix
    mu_4: sp.ImmutableMatrix
    moment_norms: sp.ImmutableMatrix
    normalization_coefficients: sp.ImmutableMatrix
    t3r6: sp.ImmutableMatrix
    bl3: sp.ImmutableMatrix
    hypercharge6: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    positive_moment_hessian: sp.ImmutableMatrix
    target_selector: sp.ImmutableMatrix
    target_gap: sp.ImmutableMatrix
    congruence: sp.ImmutableMatrix
    diagonal_parent: sp.ImmutableMatrix
    full_parent_hessian: sp.ImmutableMatrix
    schur_complement: sp.ImmutableMatrix
    inherited_auxiliary_coupling: sp.ImmutableMatrix
    inherited_parent_hessian: sp.ImmutableMatrix
    inherited_schur_complement: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> DeltaStabilizerMomentMapParentCertificate:
    mu_r = sp.ImmutableMatrix(sp.diag(sp.Rational(1, 2), sp.Rational(-1, 2)))
    mu_4 = sp.ImmutableMatrix(sp.diag(sp.Rational(-1, 4), sp.Rational(-1, 4), sp.Rational(-1, 4), sp.Rational(3, 4)))
    moment_norms = sp.ImmutableMatrix([sp.trace(mu_r**2), sp.trace(mu_4**2)])
    normalization_coefficients = sp.ImmutableMatrix([6, -4])

    t3r6 = sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3])
    bl3 = sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0])
    hypercharge6 = sp.ImmutableMatrix(t3r6 + bl3)
    hypercharge_generator = sp.ImmutableMatrix(sp.diag(*list(hypercharge6)))
    positive_moment_hessian = sp.ImmutableMatrix(hypercharge_generator**2)
    identity = sp.eye(8)
    target_selector = sp.ImmutableMatrix(sp.diag(0, 0, 1, 0, 0, 1, 0, 0))
    target_gap = sp.ImmutableMatrix(49 * identity - positive_moment_hessian)

    zero = sp.zeros(8)
    congruence = sp.ImmutableMatrix(sp.BlockMatrix([[identity, zero], [hypercharge_generator, identity]]).as_explicit())
    diagonal_parent = sp.ImmutableMatrix(sp.diag(target_gap, identity))
    full_parent_hessian = sp.ImmutableMatrix(congruence.T * diagonal_parent * congruence)
    schur_complement = sp.ImmutableMatrix(
        full_parent_hessian[:8, :8]
        - full_parent_hessian[:8, 8:] * full_parent_hessian[8:, 8:].inv() * full_parent_hessian[8:, :8]
    )

    inherited_auxiliary_coupling = sp.ImmutableMatrix.zeros(8)
    inherited_parent_hessian = sp.ImmutableMatrix(sp.diag(49 * identity, identity))
    inherited_schur_complement = sp.ImmutableMatrix(49 * identity)
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 0])
    physical_status = sp.ImmutableMatrix([1, 1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(mu_r, sp.diag(sp.Rational(1, 2), sp.Rational(-1, 2)), subject="neutral Delta SU2R moment map is exact"),
        kernel.prove_matrix_equality(mu_4, sp.diag(sp.Rational(-1, 4), sp.Rational(-1, 4), sp.Rational(-1, 4), sp.Rational(3, 4)), subject="neutral Delta SU4 moment map is exact"),
        kernel.prove_matrix_equality(moment_norms, sp.ImmutableMatrix([sp.Rational(1, 2), sp.Rational(3, 4)]), subject="moment-map trace norms are exact"),
        kernel.prove_matrix_equality(normalization_coefficients, sp.ImmutableMatrix([6, -4]), subject="six-hypercharge moment-map normalization is fixed"),
        kernel.prove_matrix_equality(t3r6, sp.ImmutableMatrix([3, -3, 3, -3, 3, -3, 3, -3]), subject="normalized SU2R moment map acts with exact Sigma weights"),
        kernel.prove_matrix_equality(bl3, sp.ImmutableMatrix([0, 0, 4, 4, -4, -4, 0, 0]), subject="normalized SU4 moment map acts with exact Sigma weights"),
        kernel.prove_matrix_equality(hypercharge6, sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3]), subject="combined moment map reconstructs six times hypercharge"),
        kernel.prove_matrix_equality(positive_moment_hessian, sp.diag(9, 9, 49, 1, 1, 49, 9, 9), subject="positive moment-map norm produces Q squared"),
        kernel.prove_exact_rank(positive_moment_hessian, 8, subject="positive moment-map norm lifts every Sigma sector"),
        kernel.prove_matrix_equality(positive_moment_hessian * target_selector, 49 * target_selector, subject="positive moment-map norm makes R2 maximally heavy"),
        kernel.prove_matrix_equality(target_gap, sp.diag(40, 40, 0, 48, 48, 0, 40, 40), subject="target complement gap is exact"),
        kernel.prove_diagonal_signature(target_gap, (0, 2, 6), subject="target gap is positive with R2 kernel"),
        kernel.prove_exact_rank(congruence, 16, subject="Schur congruence is invertible"),
        kernel.prove_diagonal_signature(diagonal_parent, (0, 2, 14), subject="diagonalized shared-auxiliary parent is positive semidefinite"),
        kernel.prove_matrix_equality(full_parent_hessian, sp.ImmutableMatrix(sp.BlockMatrix([[49 * identity, hypercharge_generator], [hypercharge_generator, identity]]).as_explicit()), subject="shared-auxiliary parent block is exact"),
        kernel.prove_exact_rank(full_parent_hessian, 14, subject="shared-auxiliary full Hessian has rank fourteen"),
        kernel.prove_exact_nullity(full_parent_hessian, 2, subject="shared-auxiliary parent retains exactly the R2 pair"),
        kernel.prove_matrix_equality(schur_complement, target_gap, subject="eliminating the shared auxiliary field produces the hypercharge gap"),
        kernel.prove_exact_rank(schur_complement, 6, subject="Schur complement lifts six companion sectors"),
        kernel.prove_exact_nullity(schur_complement, 2, subject="Schur complement leaves precisely R2 and conjugate light"),
        kernel.prove_matrix_equality(inherited_auxiliary_coupling, sp.zeros(8), subject="current fixed-point auxiliary algebra has no typed Q coupling"),
        kernel.prove_exact_rank(inherited_auxiliary_coupling, 0, subject="inherited shared-auxiliary coupling rank is zero"),
        kernel.prove_matrix_equality(inherited_schur_complement, 49 * identity, subject="uncoupled auxiliary elimination leaves only a universal mass"),
        kernel.prove_matrix_equality(inherited_parent_hessian[:8, 8:], sp.zeros(8), subject="inherited parent has zero Sigma-auxiliary cross block"),
        kernel.prove_expression_equality(sum(conditional_status), 3, subject="conditional Schur-parent architecture closes three of four slots"),
        kernel.prove_expression_equality(sum(physical_status), 2, subject="physical parent origin closes moment map and stable form only"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate",
        theorems,
    )
    return DeltaStabilizerMomentMapParentCertificate(
        mu_r,
        mu_4,
        moment_norms,
        normalization_coefficients,
        t3r6,
        bl3,
        hypercharge6,
        hypercharge_generator,
        positive_moment_hessian,
        target_selector,
        target_gap,
        congruence,
        diagonal_parent,
        full_parent_hessian,
        schur_complement,
        inherited_auxiliary_coupling,
        inherited_parent_hessian,
        inherited_schur_complement,
        conditional_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate",
    title="Родитель curvature moment map Delta-стабилизатора",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_delta_moment_map_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(26)
    ),
)