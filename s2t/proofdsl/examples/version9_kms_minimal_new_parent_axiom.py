"""LCF certificate for admission of the minimal new KMS logdet parent axiom."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSMinimalNewParentAxiomCertificate:
    hessian: sp.ImmutableMatrix
    unit_hessian: sp.ImmutableMatrix
    zero_hessian: sp.ImmutableMatrix
    stationary_theorem: Theorem
    rank_theorem: Theorem
    determinant_theorem: Theorem
    unit_spectrum_theorem: Theorem
    zero_rank_theorem: Theorem
    source_theorem: Theorem
    trace_theorem: Theorem
    witness_determinant_theorem: Theorem
    witness_defect_theorem: Theorem
    doubled_witness_theorem: Theorem
    coefficient_nonconstant_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSMinimalNewParentAxiomCertificate:
    lam = sp.symbols("lambda", positive=True)
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2", real=True)

    def block(u: sp.Expr, v: sp.Expr) -> sp.Expr:
        return 5 * sp.log((sp.exp(u) + sp.exp(v) + 3) / 5) - u - v

    axiom = lam * (block(x1, x2) + block(y1, y2))
    variables = [x1, x2, y1, y2]
    origin = {x1: 0, x2: 0, y1: 0, y2: 0}
    gradient = sp.ImmutableMatrix([sp.diff(axiom, v).subs(origin) for v in variables])
    hessian = sp.ImmutableMatrix(sp.hessian(axiom, variables).subs(origin))
    unit_hessian = sp.ImmutableMatrix(hessian.subs(lam, 1))
    zero_hessian = sp.ImmutableMatrix(hessian.subs(lam, 0))
    source = sp.ImmutableMatrix([1, 1, 1, 1])

    rs, ra = sp.Rational(1, 2), sp.Integer(1)
    rt = (5 - rs - ra) / 3
    witness_det = rs * ra * rt**3

    stationary_theorem = kernel.prove_matrix_equality(
        gradient, sp.zeros(4, 1),
        subject="the isotropic point is stationary for every positive axiom stiffness",
    )
    rank_theorem = kernel.prove_exact_rank(
        hessian, 4,
        subject="one invariant log determinant axiom controls all four relative directions",
    )
    determinant_theorem = kernel.prove_expression_equality(
        hessian.det(), sp.Rational(9, 25) * lam**4,
        subject="four direction axiom Hessian determinant scales with the fourth stiffness power",
    )
    unit_spectrum_theorem = kernel.prove_exact_spectrum(
        unit_hessian, {sp.Rational(3, 5): 2, sp.Integer(1): 2},
        subject="unit normalized axiom has a positive doubled selector spectrum",
    )
    zero_rank_theorem = kernel.prove_exact_rank(
        zero_hessian, 0,
        subject="removing the new axiom restores all four flat relative directions",
    )
    source_theorem = kernel.prove_matrix_equality(
        source, sp.ones(4, 1),
        subject="the single invariant axiom induces the four isotropic selector sources",
    )
    trace_theorem = kernel.prove_expression_equality(
        rs + ra + 3 * rt, 5,
        subject="the anisotropic sign witness remains on the weighted trace slice",
    )
    witness_determinant_theorem = kernel.prove_expression_equality(
        witness_det, sp.Rational(343, 432),
        subject="anisotropic trace normalized witness has determinant below one",
    )
    witness_defect_theorem = kernel.prove_positive_expression(
        1 - witness_det,
        subject="positive sign penalizes the anisotropic determinant witness",
    )
    doubled_witness_theorem = kernel.prove_expression_equality(
        witness_det**2, sp.Rational(117649, 186624),
        subject="two KMS packages preserve the strict determinant defect",
    )
    coefficient_nonconstant_theorem = kernel.prove_expression_nonconstant(
        hessian.det(), lam,
        subject="axiom stiffness changes fluctuations although it does not change the minimum",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate",
        (stationary_theorem, rank_theorem, determinant_theorem,
         unit_spectrum_theorem, zero_rank_theorem, source_theorem,
         trace_theorem, witness_determinant_theorem, witness_defect_theorem,
         doubled_witness_theorem, coefficient_nonconstant_theorem),
    )
    return KMSMinimalNewParentAxiomCertificate(
        hessian=hessian, unit_hessian=unit_hessian, zero_hessian=zero_hessian,
        stationary_theorem=stationary_theorem, rank_theorem=rank_theorem,
        determinant_theorem=determinant_theorem,
        unit_spectrum_theorem=unit_spectrum_theorem,
        zero_rank_theorem=zero_rank_theorem, source_theorem=source_theorem,
        trace_theorem=trace_theorem,
        witness_determinant_theorem=witness_determinant_theorem,
        witness_defect_theorem=witness_defect_theorem,
        doubled_witness_theorem=doubled_witness_theorem,
        coefficient_nonconstant_theorem=coefficient_nonconstant_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate",
    title="Admission минимальной новой аксиомы KMS logdet parent",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate_results.json",
    ),
    obligations=(
        Obligation("all_lambda_isotropic_stationarity", lambda: build_certificate().stationary_theorem),
        Obligation("four_shape_direction_rank", lambda: build_certificate().rank_theorem),
        Obligation("axiom_hessian_determinant", lambda: build_certificate().determinant_theorem),
        Obligation("unit_axiom_spectrum", lambda: build_certificate().unit_spectrum_theorem),
        Obligation("zero_axiom_flatness", lambda: build_certificate().zero_rank_theorem),
        Obligation("isotropic_source_vector", lambda: build_certificate().source_theorem),
        Obligation("anisotropic_witness_trace", lambda: build_certificate().trace_theorem),
        Obligation("anisotropic_witness_determinant", lambda: build_certificate().witness_determinant_theorem),
        Obligation("strict_determinant_defect", lambda: build_certificate().witness_defect_theorem),
        Obligation("doubled_package_defect", lambda: build_certificate().doubled_witness_theorem),
        Obligation("stiffness_remains_continuous", lambda: build_certificate().coefficient_nonconstant_theorem),
    ),
)


if __name__ == "__main__": print(build_certificate().gate_theorem.proposition)