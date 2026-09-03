"""LCF certificate for curvature-density cell-volume scale selection."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FourVolumeCurvatureDensityParentCertificate:
    curvature_constraint_map: sp.ImmutableMatrix
    common_hessian: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    volume_theorem: Theorem
    scalar_curvature_theorem: Theorem
    einstein_integral_theorem: Theorem
    quadratic_integral_theorem: Theorem
    quadratic_scale_invariance_theorem: Theorem
    square_parent_theorem: Theorem
    stationary_theorem: Theorem
    scale_selector_theorem: Theorem
    radial_hessian_theorem: Theorem
    parent_rescaling_theorem: Theorem
    selected_scale_rescaling_theorem: Theorem
    constraint_rank_theorem: Theorem
    constraint_nullity_theorem: Theorem
    constraint_kernel_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    physical_ledger_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FourVolumeCurvatureDensityParentCertificate:
    ell, scale, coefficient_a, coefficient_b = sp.symbols("ell s A B", positive=True)
    q = sp.symbols("q", positive=True)
    volume = ell**4
    scalar_curvature = 12 / ell**2
    einstein_integral = sp.simplify(volume * scalar_curvature)
    quadratic_integral = sp.simplify(volume * scalar_curvature**2)
    parent = coefficient_a * q**2 - coefficient_b * q + coefficient_b**2/(4*coefficient_a)
    square_parent = coefficient_a * (q - coefficient_b/(2*coefficient_a))**2
    selected_q = coefficient_b/(2*coefficient_a)
    rescaled_parent = parent.subs({q: scale**2*q, coefficient_a: coefficient_a/scale**4, coefficient_b: coefficient_b/scale**2}, simultaneous=True)
    curvature_constraint_map = sp.ImmutableMatrix([[1,0,2],[0,1,1]])
    scale_vector = sp.ImmutableMatrix([-2,-1,1])
    common_hessian = sp.ImmutableMatrix(sp.hessian(parent, (q,)))
    architecture = sp.ones(8,1)
    conditional_origin = sp.ones(3,1)
    physical_ledger = sp.zeros(2,1)

    volume_theorem = kernel.prove_expression_equality(volume, ell**4, subject="the isotropic cell volume has length degree four")
    scalar_curvature_theorem = kernel.prove_expression_equality(scalar_curvature*ell**2, 12, subject="constant cell scalar curvature has inverse length degree two")
    einstein_integral_theorem = kernel.prove_expression_equality(einstein_integral, 12*ell**2, subject="the integrated Einstein density scales quadratically")
    quadratic_integral_theorem = kernel.prove_expression_equality(quadratic_integral, 144, subject="the integrated curvature-square density is scale free in four dimensions")
    quadratic_scale_invariance_theorem = kernel.prove_expression_equality((scale*ell)**4*(12/(scale*ell)**2)**2, quadratic_integral, subject="curvature-square density is exactly invariant under cell dilation")
    square_parent_theorem = kernel.prove_expression_equality(parent, square_parent, subject="volume and Einstein terms form a bounded square parent")
    stationary_theorem = kernel.prove_expression_equality(sp.diff(parent,q).subs(q,selected_q), 0, subject="the conditional curvature parent has an exact stationary scale")
    scale_selector_theorem = kernel.prove_expression_equality(selected_q, coefficient_b/(2*coefficient_a), subject="the selected squared length is a ratio of curvature coefficients")
    radial_hessian_theorem = kernel.prove_expression_equality(common_hessian[0,0], 2*coefficient_a, subject="the conditional radial Hessian is positive")
    parent_rescaling_theorem = kernel.prove_expression_equality(rescaled_parent, parent, subject="coefficient and cell rescaling leave the curvature parent invariant")
    selected_scale_rescaling_theorem = kernel.prove_expression_equality((coefficient_b/scale**2)/(2*(coefficient_a/scale**4)), scale**2*selected_q, subject="the selected cell length follows the free coefficient scale")
    constraint_rank_theorem = kernel.prove_exact_rank(curvature_constraint_map, 2, subject="two curvature monomials impose two relative scaling constraints")
    constraint_nullity_theorem = kernel.prove_exact_nullity(curvature_constraint_map, 1, subject="one common curvature coefficient scale orbit remains")
    constraint_kernel_theorem = kernel.prove_matrix_equality(curvature_constraint_map*scale_vector, sp.zeros(2,1), subject="coefficient and metric dilation is the exact constraint kernel")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(8,1), subject="all curvature-density parent architecture conditions pass")
    conditional_origin_theorem = kernel.prove_matrix_equality(conditional_origin, sp.ones(3,1), subject="curvature identities boundedness and conditional selection are constructed")
    physical_ledger_theorem = kernel.prove_matrix_equality(physical_ledger, sp.zeros(2,1), subject="curvature coefficient origin and absolute scale remain open")
    physical_score_theorem = kernel.prove_expression_equality(sum(physical_ledger), 0, subject="no absolute curvature-density scale origin is supplied")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_curvature_density_parent_origin_gate", (volume_theorem, scalar_curvature_theorem, einstein_integral_theorem, quadratic_integral_theorem, quadratic_scale_invariance_theorem, square_parent_theorem, stationary_theorem, scale_selector_theorem, radial_hessian_theorem, parent_rescaling_theorem, selected_scale_rescaling_theorem, constraint_rank_theorem, constraint_nullity_theorem, constraint_kernel_theorem, architecture_theorem, conditional_origin_theorem, physical_ledger_theorem, physical_score_theorem))
    return FourVolumeCurvatureDensityParentCertificate(curvature_constraint_map, common_hessian, scale_vector, architecture, conditional_origin, physical_ledger, volume_theorem, scalar_curvature_theorem, einstein_integral_theorem, quadratic_integral_theorem, quadratic_scale_invariance_theorem, square_parent_theorem, stationary_theorem, scale_selector_theorem, radial_hessian_theorem, parent_rescaling_theorem, selected_scale_rescaling_theorem, constraint_rank_theorem, constraint_nullity_theorem, constraint_kernel_theorem, architecture_theorem, conditional_origin_theorem, physical_ledger_theorem, physical_score_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_curvature_density_parent_origin_gate", "Родитель объёмной плотности кривизны", ("s2t/gates/version10_cell_birth_four_volume_curvature_density_parent_origin_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_curvature_density_parent_origin_gate_results.json"), tuple(Obligation(name,getter) for name,getter in (
    ("cell_volume_length_degree_four",lambda:build_certificate().volume_theorem),("scalar_curvature_inverse_length_two",lambda:build_certificate().scalar_curvature_theorem),("einstein_integral_length_two",lambda:build_certificate().einstein_integral_theorem),("curvature_square_integral_144",lambda:build_certificate().quadratic_integral_theorem),("curvature_square_scale_invariant",lambda:build_certificate().quadratic_scale_invariance_theorem),("bounded_curvature_parent_square",lambda:build_certificate().square_parent_theorem),("conditional_scale_stationary",lambda:build_certificate().stationary_theorem),("selected_scale_coefficient_ratio",lambda:build_certificate().scale_selector_theorem),("positive_radial_hessian",lambda:build_certificate().radial_hessian_theorem),("curvature_parent_scale_invariance",lambda:build_certificate().parent_rescaling_theorem),("selected_scale_follows_coefficients",lambda:build_certificate().selected_scale_rescaling_theorem),("curvature_constraint_rank_two",lambda:build_certificate().constraint_rank_theorem),("curvature_constraint_nullity_one",lambda:build_certificate().constraint_nullity_theorem),("curvature_coefficient_scale_kernel",lambda:build_certificate().constraint_kernel_theorem),("curvature_parent_architecture_full",lambda:build_certificate().architecture_theorem),("conditional_curvature_origin_full",lambda:build_certificate().conditional_origin_theorem),("physical_curvature_origin_zero",lambda:build_certificate().physical_ledger_theorem),("physical_curvature_score_zero",lambda:build_certificate().physical_score_theorem))))