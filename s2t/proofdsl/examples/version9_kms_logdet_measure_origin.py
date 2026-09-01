"""LCF certificate for the algebraic core of the KMS logdet measure gate."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSLogdetMeasureOriginCertificate:
    type_operator: sp.ImmutableMatrix
    doubled_operator: sp.ImmutableMatrix
    chart_jacobian: sp.ImmutableMatrix
    determinant_theorem: Theorem
    single_degree_theorem: Theorem
    doubled_determinant_theorem: Theorem
    doubled_degree_theorem: Theorem
    fermionic_sign_theorem: Theorem
    bosonic_sign_theorem: Theorem
    real_bosonic_sign_theorem: Theorem
    chart_jacobian_theorem: Theorem
    chart_ratio_theorem: Theorem
    chart_mismatch_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSLogdetMeasureOriginCertificate:
    rs, ra, rt = sp.symbols("r_s r_a r_t", positive=True)
    type_operator = sp.ImmutableMatrix(sp.diag(rs, ra, rt, rt, rt))
    determinant = rs * ra * rt**3

    ss, sa, st = sp.symbols("s_s s_a s_t", positive=True)
    second_operator = sp.ImmutableMatrix(sp.diag(ss, sa, st, st, st))
    doubled_operator = sp.ImmutableMatrix(sp.diag(type_operator, second_operator))
    second_determinant = ss * sa * st**3

    dtheta, dkappa = sp.symbols("d_theta d_kappa", positive=True)
    target_action = -sp.log(dtheta) - sp.log(dkappa)
    fermionic_action = -sp.log(dtheta * dkappa)
    bosonic_action = sp.log(dtheta * dkappa)
    real_bosonic_action = sp.log(dtheta * dkappa) / 2

    u, v = sp.symbols("u v", real=True)
    z = sp.exp(u) + sp.exp(v) + 3
    chart_rs = 5 * sp.exp(u) / z
    chart_ra = 5 * sp.exp(v) / z
    chart_rt = 5 / z
    chart_jacobian = sp.ImmutableMatrix([
        [sp.diff(chart_rs, u), sp.diff(chart_rs, v)],
        [sp.diff(chart_ra, u), sp.diff(chart_ra, v)],
    ])
    chart_determinant = sp.simplify(chart_jacobian.det())
    target_chart_determinant = sp.simplify(chart_rs * chart_ra * chart_rt**3)
    jacobian_ratio = sp.simplify(target_chart_determinant / chart_determinant)

    determinant_theorem = kernel.prove_expression_equality(
        type_operator.det(),
        determinant,
        subject="one KMS type determinant has multiplicities one one three",
    )
    single_degree_theorem = kernel.prove_expression_equality(
        sp.Poly(determinant, rs, ra, rt).total_degree(),
        5,
        subject="one determinant carrier has homogeneous degree five",
    )
    doubled_determinant_theorem = kernel.prove_expression_equality(
        doubled_operator.det(),
        determinant * second_determinant,
        subject="block determinant factors into gap and conductance packages",
    )
    doubled_degree_theorem = kernel.prove_expression_equality(
        sp.Poly(doubled_operator.det(), rs, ra, rt, ss, sa, st).total_degree(),
        10,
        subject="two independent determinant carriers have total degree ten",
    )
    fermionic_sign_theorem = kernel.prove_expression_equality(
        fermionic_action,
        target_action,
        subject="complex fermionic determinant gives the target effective sign",
    )
    bosonic_sign_theorem = kernel.prove_expression_equality(
        bosonic_action,
        -target_action,
        subject="complex bosonic determinant gives the opposite effective sign",
    )
    real_bosonic_sign_theorem = kernel.prove_expression_equality(
        real_bosonic_action,
        -target_action / 2,
        subject="real bosonic determinant gives the opposite half sign",
    )
    chart_jacobian_theorem = kernel.prove_expression_equality(
        chart_determinant,
        sp.Rational(3, 5) * chart_rs * chart_ra * chart_rt,
        subject="log ratio chart Jacobian contains only one triplet power",
    )
    chart_ratio_theorem = kernel.prove_expression_equality(
        jacobian_ratio,
        sp.Rational(5, 3) * chart_rt**2,
        subject="target determinant differs from chart Jacobian by two triplet powers",
    )
    chart_mismatch_theorem = kernel.prove_expression_nonconstant(
        jacobian_ratio,
        u,
        subject="coordinate Jacobian cannot equal the invariant determinant measure",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_relative_shape_logdet_parent_"
        "measure_origin_gate",
        (
            determinant_theorem,
            single_degree_theorem,
            doubled_determinant_theorem,
            doubled_degree_theorem,
            fermionic_sign_theorem,
            bosonic_sign_theorem,
            real_bosonic_sign_theorem,
            chart_jacobian_theorem,
            chart_ratio_theorem,
            chart_mismatch_theorem,
        ),
    )
    return KMSLogdetMeasureOriginCertificate(
        type_operator=type_operator,
        doubled_operator=doubled_operator,
        chart_jacobian=chart_jacobian,
        determinant_theorem=determinant_theorem,
        single_degree_theorem=single_degree_theorem,
        doubled_determinant_theorem=doubled_determinant_theorem,
        doubled_degree_theorem=doubled_degree_theorem,
        fermionic_sign_theorem=fermionic_sign_theorem,
        bosonic_sign_theorem=bosonic_sign_theorem,
        real_bosonic_sign_theorem=real_bosonic_sign_theorem,
        chart_jacobian_theorem=chart_jacobian_theorem,
        chart_ratio_theorem=chart_ratio_theorem,
        chart_mismatch_theorem=chart_mismatch_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_relative_shape_logdet_parent_"
        "measure_origin_gate"
    ),
    title="Происхождение invariant logdet parent из меры",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_relative_shape_logdet_"
        "parent_measure_origin_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_relative_shape_logdet_"
        "parent_measure_origin_gate_results.json",
    ),
    obligations=(
        Obligation("type_determinant_113", lambda: build_certificate().determinant_theorem),
        Obligation("single_carrier_degree_five", lambda: build_certificate().single_degree_theorem),
        Obligation("doubled_block_determinant", lambda: build_certificate().doubled_determinant_theorem),
        Obligation("doubled_carrier_degree_ten", lambda: build_certificate().doubled_degree_theorem),
        Obligation("fermionic_effective_sign", lambda: build_certificate().fermionic_sign_theorem),
        Obligation("complex_bosonic_opposite_sign", lambda: build_certificate().bosonic_sign_theorem),
        Obligation("real_bosonic_opposite_half_sign", lambda: build_certificate().real_bosonic_sign_theorem),
        Obligation("log_ratio_chart_jacobian", lambda: build_certificate().chart_jacobian_theorem),
        Obligation("chart_to_target_ratio", lambda: build_certificate().chart_ratio_theorem),
        Obligation("chart_measure_mismatch", lambda: build_certificate().chart_mismatch_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)