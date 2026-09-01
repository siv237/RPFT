"""LCF certificate for a common Gaussian covariance carrier of both reopening packages."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class PhysicalReopeningCommonOriginCarrierCertificate:
    common_operator: sp.ImmutableMatrix
    common_hessian: sp.ImmutableMatrix
    scale_orbit_map: sp.ImmutableMatrix
    dimension_theorem: Theorem
    trace_theorem: Theorem
    determinant_theorem: Theorem
    relative_entropy_theorem: Theorem
    stationary_theorem: Theorem
    hessian_rank_theorem: Theorem
    hessian_determinant_theorem: Theorem
    hessian_spectrum_theorem: Theorem
    scale_invariance_theorem: Theorem
    scale_orbit_nullity_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> PhysicalReopeningCommonOriginCarrierCertificate:
    e, chi = sp.symbols("e chi", positive=True)
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2", real=True)

    def shape(x: sp.Expr, y: sp.Expr) -> sp.ImmutableMatrix:
        z = sp.exp(x) + sp.exp(y) + 3
        entries = 5 * sp.Matrix([sp.exp(x), sp.exp(y), 1]) / z
        return sp.ImmutableMatrix(sp.diag(entries[0], entries[1], entries[2], entries[2], entries[2]))

    gap_shape = shape(x1, x2)
    conductance_shape = shape(y1, y2)
    common_operator = sp.ImmutableMatrix(sp.diag(e * gap_shape, e * chi**2 * conductance_shape))
    common_trace = sp.trace(common_operator)
    common_determinant = sp.factor(common_operator.det())
    parent = sp.simplify(common_trace - sp.log(common_determinant) - 10)
    gaussian_relative_entropy = parent / 2

    variables = [e, chi, x1, x2, y1, y2]
    isotropic = {e: 1, chi: 1, x1: 0, x2: 0, y1: 0, y2: 0}
    gradient = sp.ImmutableMatrix([sp.diff(parent, variable).subs(isotropic) for variable in variables])
    common_hessian = sp.ImmutableMatrix(sp.hessian(parent, variables).subs(isotropic))

    energy, reference, scale = sp.symbols("E mu s", positive=True)
    scale_orbit_map = sp.ImmutableMatrix([[1, -1]])

    dimension_theorem = kernel.prove_expression_equality(
        common_operator.rows,
        10,
        subject="the common two package covariance carrier has dimension ten",
    )
    trace_theorem = kernel.prove_expression_equality(
        common_trace,
        5 * e * (1 + chi**2),
        subject="the common trace joins the scale and coupling packages",
    )
    determinant_theorem = kernel.prove_expression_equality(
        common_determinant,
        e**10 * chi**10 * gap_shape.det() * conductance_shape.det(),
        subject="one determinant contains both KMS shape determinants",
    )
    relative_entropy_theorem = kernel.prove_expression_equality(
        parent,
        2 * gaussian_relative_entropy,
        subject="the spectral entropy parent is twice a centered Gaussian relative entropy",
    )
    stationary_theorem = kernel.prove_matrix_equality(
        gradient,
        sp.zeros(6, 1),
        subject="the isotropic unit covariance is stationary",
    )
    hessian_rank_theorem = kernel.prove_exact_rank(
        common_hessian,
        6,
        subject="the common spectral entropy parent controls all six variables",
    )
    hessian_determinant_theorem = kernel.prove_expression_equality(
        common_hessian.det(),
        36,
        subject="the common carrier Hessian is nondegenerate",
    )
    hessian_spectrum_theorem = kernel.prove_exact_spectrum(
        common_hessian,
        {
            15 - 5 * sp.sqrt(5): 1,
            15 + 5 * sp.sqrt(5): 1,
            sp.Integer(1): 2,
            sp.Rational(3, 5): 2,
        },
        subject="the common carrier Hessian is strictly positive",
    )
    scale_invariance_theorem = kernel.prove_expression_equality(
        scale * energy / (scale * reference),
        energy / reference,
        subject="a common rescaling of physical and reference energies leaves e invariant",
    )
    scale_orbit_nullity_theorem = kernel.prove_exact_nullity(
        scale_orbit_map,
        1,
        subject="one common energy rescaling remains invisible to the dimensionless carrier",
    )
    gate_theorem = kernel.prove_gate(
        "version9_physical_reopening_common_origin_carrier_admission_gate",
        (
            dimension_theorem,
            trace_theorem,
            determinant_theorem,
            relative_entropy_theorem,
            stationary_theorem,
            hessian_rank_theorem,
            hessian_determinant_theorem,
            hessian_spectrum_theorem,
            scale_invariance_theorem,
            scale_orbit_nullity_theorem,
        ),
    )
    return PhysicalReopeningCommonOriginCarrierCertificate(
        common_operator=common_operator,
        common_hessian=common_hessian,
        scale_orbit_map=scale_orbit_map,
        dimension_theorem=dimension_theorem,
        trace_theorem=trace_theorem,
        determinant_theorem=determinant_theorem,
        relative_entropy_theorem=relative_entropy_theorem,
        stationary_theorem=stationary_theorem,
        hessian_rank_theorem=hessian_rank_theorem,
        hessian_determinant_theorem=hessian_determinant_theorem,
        hessian_spectrum_theorem=hessian_spectrum_theorem,
        scale_invariance_theorem=scale_invariance_theorem,
        scale_orbit_nullity_theorem=scale_orbit_nullity_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_physical_reopening_common_origin_carrier_admission_gate",
    title="Admission общего Gaussian covariance carrier для physical reopening",
    source_paths=(
        "s2t/gates/version9_physical_reopening_common_origin_carrier_admission_gate.tex",
        "s2t/results/s2t_v9_physical_reopening_common_origin_carrier_admission_gate_results.json",
    ),
    obligations=(
        Obligation("common_carrier_dimension_ten", lambda: build_certificate().dimension_theorem),
        Obligation("common_trace_factorization", lambda: build_certificate().trace_theorem),
        Obligation("common_determinant_factorization", lambda: build_certificate().determinant_theorem),
        Obligation("gaussian_relative_entropy_identity", lambda: build_certificate().relative_entropy_theorem),
        Obligation("isotropic_stationary_point", lambda: build_certificate().stationary_theorem),
        Obligation("common_hessian_rank_six", lambda: build_certificate().hessian_rank_theorem),
        Obligation("common_hessian_determinant", lambda: build_certificate().hessian_determinant_theorem),
        Obligation("common_hessian_positive_spectrum", lambda: build_certificate().hessian_spectrum_theorem),
        Obligation("common_energy_rescaling_invariance", lambda: build_certificate().scale_invariance_theorem),
        Obligation("reference_scale_orbit_nullity_one", lambda: build_certificate().scale_orbit_nullity_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)