"""LCF certificate for the Mathai--Quillen shift-symmetry parent-origin gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class MathaiQuillenShiftSymmetryParentOriginCertificate:
    effective_hessian: sp.ImmutableMatrix
    required_shift: sp.ImmutableMatrix
    inherited_flat_basis: sp.ImmutableMatrix
    ordinary_gauge_tangent_at_origin: sp.ImmutableMatrix
    difference_map: sp.ImmutableMatrix
    diagonal_shift: sp.ImmutableMatrix
    stueckelberg_hessian: sp.ImmutableMatrix
    physical_inclusion: sp.ImmutableMatrix
    gauge_fixing_operator: sp.ImmutableMatrix
    inherited_stueckelberg_injection: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    inherited_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> MathaiQuillenShiftSymmetryParentOriginCertificate:
    g = sp.diag(40, 40, 0, 48, 48, 0, 40, 40)
    identity = sp.eye(8)
    zero = sp.zeros(8)
    required_shift = sp.ImmutableMatrix(identity)
    inherited_flat_basis = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([0, 0, 1, 0, 0, 0, 0, 0]),
        sp.ImmutableMatrix([0, 0, 0, 0, 0, 1, 0, 0]),
    )
    ordinary_gauge_tangent_at_origin = sp.ImmutableMatrix.zeros(8, 8)
    difference_map = sp.ImmutableMatrix(sp.Matrix.hstack(identity, -identity))
    diagonal_shift = sp.ImmutableMatrix(sp.Matrix.vstack(identity, identity))
    stueckelberg_hessian = sp.ImmutableMatrix(difference_map.T * g * difference_map)
    physical_inclusion = sp.ImmutableMatrix(sp.Matrix.vstack(identity, zero))
    q = sp.diag(3, -3, 7, 1, -1, -7, 3, -3)
    gauge_fixing_operator = sp.ImmutableMatrix(q)
    inherited_stueckelberg_injection = sp.ImmutableMatrix.zeros(16, 8)
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 1, 1, 1, 0])
    inherited_status = sp.ImmutableMatrix([1, 0, 0, 1, 1, 0, 0])

    theorems = (
        kernel.prove_exact_rank(g, 6, subject="effective Sigma Hessian has rank six"),
        kernel.prove_expression_equality(8 - g.rank(), 2, subject="effective Sigma Hessian has nullity two"),
        kernel.prove_exact_rank(required_shift, 8, subject="Mathai--Quillen shift requires rank eight"),
        kernel.prove_exact_rank(g * required_shift, 6, subject="full Sigma translation breaks six Hessian directions"),
        kernel.prove_exact_rank(inherited_flat_basis, 2, subject="quadratic flat translation subspace has rank two"),
        kernel.prove_matrix_equality(g * inherited_flat_basis, sp.zeros(8, 2), subject="the two inherited quadratic flat directions lie in the Hessian kernel"),
        kernel.prove_exact_rank(ordinary_gauge_tangent_at_origin, 0, subject="ordinary gauge action has zero translational tangent at the origin"),
        kernel.prove_exact_rank(difference_map, 8, subject="Stueckelberg difference map has rank eight"),
        kernel.prove_exact_rank(diagonal_shift, 8, subject="conditional diagonal shift orbit has rank eight"),
        kernel.prove_matrix_equality(difference_map * diagonal_shift, sp.zeros(8), subject="difference coordinate is invariant under diagonal shifts"),
        kernel.prove_matrix_equality(stueckelberg_hessian * diagonal_shift, sp.zeros(16, 8), subject="conditional doubled Hessian preserves the full shift"),
        kernel.prove_exact_rank(stueckelberg_hessian, 6, subject="conditional Stueckelberg Hessian has rank six"),
        kernel.prove_expression_equality(16 - stueckelberg_hessian.rank(), 10, subject="conditional Stueckelberg Hessian has nullity ten"),
        kernel.prove_matrix_equality(physical_inclusion.T * stueckelberg_hessian * physical_inclusion, g, subject="unitary gauge recovers the original Sigma Hessian"),
        kernel.prove_exact_rank(gauge_fixing_operator, 8, subject="Q gauge fixing gives a nondegenerate FP operator"),
        kernel.prove_expression_equality(gauge_fixing_operator.det(), 3969, subject="FP determinant equals the Thom odd determinant"),
        kernel.prove_exact_rank(inherited_stueckelberg_injection, 0, subject="current parent supplies no independent Stueckelberg copy"),
        kernel.prove_expression_equality(sum(conditional_status), 6, subject="conditional shift parent closes six of seven criteria"),
        kernel.prove_expression_equality(sum(inherited_status), 3, subject="inherited shift parent closes three of seven criteria"),
        kernel.prove_positive_expression(required_shift.rank() - inherited_flat_basis.rank(), subject="full shift rank exceeds the quadratic flat subspace"),
        kernel.prove_expression_equality(required_shift.rank() - inherited_flat_basis.rank(), 6, subject="quadratic shift-rank deficit is six"),
        kernel.prove_matrix_equality(inherited_status + sp.ImmutableMatrix([0, 1, 1, 0, 0, 1, 0]), conditional_status, subject="conditional completion differs by shift, invariance, and BRST sectors"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate",
        theorems,
    )
    return MathaiQuillenShiftSymmetryParentOriginCertificate(
        sp.ImmutableMatrix(g), required_shift, inherited_flat_basis,
        ordinary_gauge_tangent_at_origin, difference_map, diagonal_shift,
        stueckelberg_hessian, physical_inclusion, gauge_fixing_operator,
        inherited_stueckelberg_injection, conditional_status,
        inherited_status, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate",
    title="Происхождение shift-симметрии Mathai--Quillen-пары",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_mathai_quillen_shift_symmetry_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)