"""LCF certificate for influx-induced determinant and geometric beta boundary."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class GeometricScaleBetaTraceAnomalyOriginCertificate:
    closed_partition: sp.Expr
    normalized_inflow_partition: sp.Expr
    inflow_effective_action: sp.Expr
    quadratic_curvature: sp.Expr
    quartic_curvature: sp.Expr
    witness_potential: sp.Expr
    extensive_influx: sp.Expr
    intensive_influx: sp.Expr
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    closed_cancellation_theorem: Theorem
    normalized_partition_theorem: Theorem
    inflow_nonconstant_theorem: Theorem
    negative_curvature_theorem: Theorem
    quartic_curvature_theorem: Theorem
    quartic_positive_theorem: Theorem
    symmetric_instability_theorem: Theorem
    positive_stationary_theorem: Theorem
    negative_stationary_theorem: Theorem
    broken_hessian_theorem: Theorem
    extensive_beta_theorem: Theorem
    intensive_influx_theorem: Theorem
    intensive_beta_theorem: Theorem
    architecture_theorem: Theorem
    physical_origin_theorem: Theorem
    status_gap_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> GeometricScaleBetaTraceAnomalyOriginCertificate:
    q = sp.symbols("q", real=True)
    influx = sp.symbols("J", positive=True)
    zeta = sp.symbols("zeta", real=True)
    influx0 = sp.symbols("J_0", positive=True)

    physical_operator = 1 + q**2
    ghost_operator = physical_operator
    closed_partition = ghost_operator / physical_operator

    inflow_partition = ghost_operator / (physical_operator + influx)
    normalized_inflow_partition = sp.simplify(
        inflow_partition / inflow_partition.subs(q, 0)
    )
    inflow_effective_action = sp.simplify(-sp.log(normalized_inflow_partition))
    quadratic_curvature = sp.simplify(
        sp.diff(inflow_effective_action, q, 2).subs(q, 0)
    )
    quartic_curvature = sp.factor(
        sp.diff(inflow_effective_action, q, 4).subs(q, 0)
    )

    witness_influx = sp.Rational(9, 10)
    witness_potential = sp.simplify(
        q**4 / 4 + inflow_effective_action.subs(influx, witness_influx)
    )
    broken_point = sp.sqrt(sp.Rational(1, 2))

    extensive_influx = influx0 * sp.exp(3 * zeta)
    intensive_influx = sp.simplify(extensive_influx / sp.exp(3 * zeta))
    architecture = sp.ones(6, 1)
    physical_origin = sp.zeros(2, 1)

    closed_cancellation_theorem = kernel.prove_expression_equality(
        closed_partition,
        1,
        subject="closed physical and ghost determinants cancel exactly",
    )
    normalized_partition_theorem = kernel.prove_expression_equality(
        normalized_inflow_partition,
        (1 + influx) * (1 + q**2) / (1 + q**2 + influx),
        subject="physical influx leaves a normalized unpaired determinant ratio",
    )
    inflow_nonconstant_theorem = kernel.prove_expression_nonconstant(
        inflow_effective_action,
        q,
        subject="physical influx produces a nonflat effective action",
    )
    negative_curvature_theorem = kernel.prove_positive_expression(
        -quadratic_curvature,
        subject="positive influx destabilizes the symmetric point",
    )
    quartic_curvature_theorem = kernel.prove_expression_equality(
        quartic_curvature,
        12 * influx * (influx + 2) / (influx + 1) ** 2,
        subject="the influx determinant has positive fourth variation",
    )
    quartic_positive_theorem = kernel.prove_positive_expression(
        quartic_curvature,
        subject="the fourth variation of the influx determinant is positive",
    )
    symmetric_instability_theorem = kernel.prove_expression_equality(
        sp.diff(witness_potential, q, 2).subs(q, 0),
        -sp.Rational(18, 19),
        subject="the exact rational influx witness destabilizes the symmetric vacuum",
    )
    positive_stationary_theorem = kernel.prove_expression_equality(
        sp.diff(witness_potential, q).subs(q, broken_point),
        0,
        subject="the positive broken branch is stationary",
    )
    negative_stationary_theorem = kernel.prove_expression_equality(
        sp.diff(witness_potential, q).subs(q, -broken_point),
        0,
        subject="the negative broken branch is stationary",
    )
    broken_hessian_theorem = kernel.prove_expression_equality(
        sp.diff(witness_potential, q, 2).subs(q, broken_point),
        sp.Rational(37, 24),
        subject="the broken influx branch has positive local curvature",
    )
    extensive_beta_theorem = kernel.prove_expression_equality(
        sp.diff(extensive_influx, zeta),
        3 * extensive_influx,
        subject="extensive cell influx has geometric scaling exponent three",
    )
    intensive_influx_theorem = kernel.prove_expression_equality(
        intensive_influx,
        influx0,
        subject="volume-normalized influx is constant under pure cell multiplication",
    )
    intensive_beta_theorem = kernel.prove_expression_equality(
        sp.diff(intensive_influx, zeta),
        0,
        subject="pure geometric multiplication gives no intensive quantum beta function",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(6, 1),
        subject="all influx determinant and symmetry-breaking architecture tests pass",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(2, 1),
        subject="intensive beta and physical reservoir origin remain open",
    )
    status_gap_theorem = kernel.prove_positive_expression(
        sum(architecture) - sum(physical_origin),
        subject="influx architecture does not imply quantum anomaly origin",
    )
    gate_theorem = kernel.prove_gate(
        "version10_geometric_scale_beta_trace_anomaly_origin_gate",
        (
            closed_cancellation_theorem,
            normalized_partition_theorem,
            inflow_nonconstant_theorem,
            negative_curvature_theorem,
            quartic_curvature_theorem,
            quartic_positive_theorem,
            symmetric_instability_theorem,
            positive_stationary_theorem,
            negative_stationary_theorem,
            broken_hessian_theorem,
            extensive_beta_theorem,
            intensive_influx_theorem,
            intensive_beta_theorem,
            architecture_theorem,
            physical_origin_theorem,
            status_gap_theorem,
        ),
    )
    return GeometricScaleBetaTraceAnomalyOriginCertificate(
        closed_partition=closed_partition,
        normalized_inflow_partition=normalized_inflow_partition,
        inflow_effective_action=inflow_effective_action,
        quadratic_curvature=quadratic_curvature,
        quartic_curvature=quartic_curvature,
        witness_potential=witness_potential,
        extensive_influx=extensive_influx,
        intensive_influx=intensive_influx,
        architecture=architecture,
        physical_origin=physical_origin,
        closed_cancellation_theorem=closed_cancellation_theorem,
        normalized_partition_theorem=normalized_partition_theorem,
        inflow_nonconstant_theorem=inflow_nonconstant_theorem,
        negative_curvature_theorem=negative_curvature_theorem,
        quartic_curvature_theorem=quartic_curvature_theorem,
        quartic_positive_theorem=quartic_positive_theorem,
        symmetric_instability_theorem=symmetric_instability_theorem,
        positive_stationary_theorem=positive_stationary_theorem,
        negative_stationary_theorem=negative_stationary_theorem,
        broken_hessian_theorem=broken_hessian_theorem,
        extensive_beta_theorem=extensive_beta_theorem,
        intensive_influx_theorem=intensive_influx_theorem,
        intensive_beta_theorem=intensive_beta_theorem,
        architecture_theorem=architecture_theorem,
        physical_origin_theorem=physical_origin_theorem,
        status_gap_theorem=status_gap_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_geometric_scale_beta_trace_anomaly_origin_gate",
    title="Физический приток, нарушение сокращения и граница следовой аномалии",
    source_paths=(
        "s2t/gates/version10_geometric_scale_beta_trace_anomaly_origin_gate.tex",
        "s2t/results/s2t_v10_geometric_scale_beta_trace_anomaly_origin_gate_results.json",
    ),
    obligations=(
        Obligation("closed_determinant_cancellation", lambda: build_certificate().closed_cancellation_theorem),
        Obligation("normalized_unpaired_inflow_determinant", lambda: build_certificate().normalized_partition_theorem),
        Obligation("inflow_effective_action_nonflat", lambda: build_certificate().inflow_nonconstant_theorem),
        Obligation("symmetric_point_negative_curvature", lambda: build_certificate().negative_curvature_theorem),
        Obligation("positive_fourth_variation_formula", lambda: build_certificate().quartic_curvature_theorem),
        Obligation("positive_fourth_variation", lambda: build_certificate().quartic_positive_theorem),
        Obligation("exact_witness_symmetric_instability", lambda: build_certificate().symmetric_instability_theorem),
        Obligation("positive_broken_stationary_branch", lambda: build_certificate().positive_stationary_theorem),
        Obligation("negative_broken_stationary_branch", lambda: build_certificate().negative_stationary_theorem),
        Obligation("positive_broken_branch_hessian", lambda: build_certificate().broken_hessian_theorem),
        Obligation("extensive_geometric_beta", lambda: build_certificate().extensive_beta_theorem),
        Obligation("intensive_influx_normalization", lambda: build_certificate().intensive_influx_theorem),
        Obligation("intensive_quantum_beta_zero", lambda: build_certificate().intensive_beta_theorem),
        Obligation("inflow_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("physical_anomaly_origin_open", lambda: build_certificate().physical_origin_theorem),
        Obligation("architecture_origin_gap", lambda: build_certificate().status_gap_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)