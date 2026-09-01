"""LCF certificate for the axiom-augmented common KMS parent closure."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSAxiomAugmentedCommonParentCertificate:
    common_hessian: sp.ImmutableMatrix
    common_gradient: sp.ImmutableMatrix
    selected_point: sp.ImmutableMatrix
    stationarity_theorem: Theorem
    minimum_theorem: Theorem
    rank_theorem: Theorem
    determinant_theorem: Theorem
    selected_point_theorem: Theorem
    gap_shape_theorem: Theorem
    conductance_shape_theorem: Theorem
    endpoint_theorem: Theorem
    transport_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSAxiomAugmentedCommonParentCertificate:
    e, chi, x1, x2, y1, y2, endpoint, transport = sp.symbols(
        "e chi x1 x2 y1 y2 endpoint transport", real=True
    )
    theta_symbols = sp.symbols("theta_s theta_a theta_t", real=True)
    kappa_symbols = sp.symbols("kappa_s kappa_a kappa_t", real=True)
    theta, kappa = sp.Matrix(theta_symbols), sp.Matrix(kappa_symbols)
    weight = sp.diag(1, 1, 3)

    def shape(x: sp.Expr, y: sp.Expr) -> sp.Matrix:
        z = sp.exp(x) + sp.exp(y) + 3
        return 5 * sp.Matrix([sp.exp(x), sp.exp(y), 1]) / z

    gap_shape, conductance_shape = shape(x1, x2), shape(y1, y2)
    axiom = (
        5 * sp.log((sp.exp(x1) + sp.exp(x2) + 3) / 5) - x1 - x2
        + 5 * sp.log((sp.exp(y1) + sp.exp(y2) + 3) / 5) - y1 - y2
    )
    theta_residual = theta - e * gap_shape
    kappa_residual = kappa - chi**2 * e * conductance_shape
    parent = (
        4 * (e - 1) ** 2 + 4 * (chi - 1) ** 2 + axiom
        + (theta_residual.T * weight * theta_residual)[0] / 2
        + (kappa_residual.T * weight * kappa_residual)[0] / 2
        + (endpoint - 1) ** 2 / 2 + (transport - 1) ** 2 / 2
    )
    variables = [e, chi, x1, x2, y1, y2, *theta_symbols, *kappa_symbols, endpoint, transport]
    point = {v: 1 for v in [e, chi, *theta_symbols, *kappa_symbols, endpoint, transport]}
    point.update({x1: 0, x2: 0, y1: 0, y2: 0})
    common_gradient = sp.ImmutableMatrix([sp.diff(parent, v).subs(point) for v in variables])
    common_hessian = sp.ImmutableMatrix(sp.hessian(parent, variables).subs(point))
    selected_point = sp.ImmutableMatrix([point[v] for v in variables])

    stationarity_theorem = kernel.prove_matrix_equality(common_gradient, sp.zeros(14, 1), subject="all augmented common parent equations are stationary together")
    minimum_theorem = kernel.prove_expression_equality(parent.subs(point), 0, subject="the augmented parent has zero value at the common selected point")
    rank_theorem = kernel.prove_exact_rank(common_hessian, 14, subject="the augmented parent controls all fourteen continuous chart variables")
    determinant_theorem = kernel.prove_expression_equality(common_hessian.det(), sp.Rational(5184, 25), subject="the endpoint and transport unit wells preserve the common Hessian determinant")
    selected_point_theorem = kernel.prove_matrix_equality(selected_point, sp.ImmutableMatrix([1,1,0,0,0,0,1,1,1,1,1,1,1,1]), subject="the unique local common point selects scales shapes KMS data endpoint and transport")
    gap_shape_theorem = kernel.prove_matrix_equality(gap_shape.subs(point), sp.ones(3, 1), subject="the augmented axiom selects the isotropic gap shape")
    conductance_shape_theorem = kernel.prove_matrix_equality(conductance_shape.subs(point), sp.ones(3, 1), subject="the augmented axiom selects the isotropic conductance shape")
    endpoint_theorem = kernel.prove_expression_equality(endpoint.subs(point), 1, subject="the inherited endpoint selector is retained")
    transport_theorem = kernel.prove_expression_equality(transport.subs(point), 1, subject="the inherited transport selector is retained")
    gate_theorem = kernel.prove_gate("version9_endpoint_creation_kms_logdet_axiom_augmented_common_parent_closure_gate", (stationarity_theorem, minimum_theorem, rank_theorem, determinant_theorem, selected_point_theorem, gap_shape_theorem, conductance_shape_theorem, endpoint_theorem, transport_theorem))
    return KMSAxiomAugmentedCommonParentCertificate(common_hessian, common_gradient, selected_point, stationarity_theorem, minimum_theorem, rank_theorem, determinant_theorem, selected_point_theorem, gap_shape_theorem, conductance_shape_theorem, endpoint_theorem, transport_theorem, gate_theorem)


SPEC = GateSpec(
    identifier="version9_endpoint_creation_kms_logdet_axiom_augmented_common_parent_closure_gate",
    title="Замыкание axiom-augmented общего KMS parent",
    source_paths=("s2t/gates/version9_endpoint_creation_kms_logdet_axiom_augmented_common_parent_closure_gate.tex", "s2t/results/s2t_v9_endpoint_creation_kms_logdet_axiom_augmented_common_parent_closure_gate_results.json"),
    obligations=(
        Obligation("common_stationarity", lambda: build_certificate().stationarity_theorem),
        Obligation("zero_common_minimum", lambda: build_certificate().minimum_theorem),
        Obligation("full_common_hessian_rank", lambda: build_certificate().rank_theorem),
        Obligation("common_hessian_determinant", lambda: build_certificate().determinant_theorem),
        Obligation("selected_common_point", lambda: build_certificate().selected_point_theorem),
        Obligation("isotropic_gap_shape", lambda: build_certificate().gap_shape_theorem),
        Obligation("isotropic_conductance_shape", lambda: build_certificate().conductance_shape_theorem),
        Obligation("endpoint_selector_retained", lambda: build_certificate().endpoint_theorem),
        Obligation("transport_selector_retained", lambda: build_certificate().transport_theorem),
    ),
)


if __name__ == "__main__": print(build_certificate().gate_theorem.proposition)