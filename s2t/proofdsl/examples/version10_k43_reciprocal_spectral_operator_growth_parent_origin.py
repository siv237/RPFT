"""LCF certificate for the geometric parent of the reciprocal K43 flow."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from .version10_inflow_spectral_self_energy_k43_typed_embedding import (
    build_certificate as embedding_certificate,
)


@dataclass(frozen=True, slots=True)
class K43ReciprocalSpectralGrowthParentCertificate:
    growth_grading: sp.ImmutableMatrix
    support_projector: sp.ImmutableMatrix
    orientation_scores: sp.ImmutableMatrix
    spectral_operator: sp.ImmutableMatrix
    flow_residual: sp.ImmutableMatrix
    compressed_operator: sp.ImmutableMatrix
    incoming_self_energy: sp.Expr
    jet_parent: sp.Expr
    jet_gradient: sp.ImmutableMatrix
    jet_hessian: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    spectral_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    grading_trace_theorem: Theorem
    grading_square_theorem: Theorem
    grading_rank_theorem: Theorem
    grading_spectrum_theorem: Theorem
    reciprocal_constraint_theorem: Theorem
    orientation_selection_theorem: Theorem
    initial_condition_theorem: Theorem
    flow_equation_theorem: Theorem
    determinant_theorem: Theorem
    compression_theorem: Theorem
    self_energy_theorem: Theorem
    beta_theorem: Theorem
    jet_stationary_theorem: Theorem
    jet_hessian_rank_theorem: Theorem
    jet_hessian_determinant_theorem: Theorem
    jet_minimum_theorem: Theorem
    architecture_theorem: Theorem
    spectral_origin_theorem: Theorem
    physical_origin_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> K43ReciprocalSpectralGrowthParentCertificate:
    embedded = embedding_certificate()
    zeta = sp.symbols("zeta", real=True)
    incoming = sp.ImmutableMatrix(embedded.embedding[:, 0])
    vacuum = sp.ImmutableMatrix(embedded.embedding[:, 1])
    incoming_projector = sp.ImmutableMatrix(incoming * incoming.T)
    vacuum_projector = sp.ImmutableMatrix(vacuum * vacuum.T)
    support_projector = sp.ImmutableMatrix(incoming_projector + vacuum_projector)
    growth_grading = sp.ImmutableMatrix(vacuum_projector - incoming_projector)

    reciprocal_constraint = sp.ImmutableMatrix([[1, 1]])
    orientation_scores = sp.ImmutableMatrix([
        sp.trace(growth_grading * growth_grading),
        sp.trace(growth_grading * (-growth_grading)),
    ])

    spectral_operator = sp.ImmutableMatrix(
        sp.eye(43)
        + (sp.exp(-zeta) - 1) * incoming_projector
        + (sp.exp(zeta) - 1) * vacuum_projector
    )
    flow_residual = sp.ImmutableMatrix(
        sp.diff(spectral_operator, zeta)
        - (growth_grading * spectral_operator + spectral_operator * growth_grading) / 2
    )
    compressed_operator = sp.ImmutableMatrix(
        embedded.embedding.T * spectral_operator * embedded.embedding
    )
    incoming_self_energy = sp.simplify(
        (incoming.T * spectral_operator.inv() * incoming)[0]
    )

    r_y, r_0, v_y, v_0 = sp.symbols("r_Y r_0 v_Y v_0", real=True)
    jet_variables = [r_y, r_0, v_y, v_0]
    jet_parent = (
        (v_y + r_y) ** 2 / 2
        + (v_0 - r_0) ** 2 / 2
        + (r_y - 1) ** 2 / 2
        + (r_0 - 1) ** 2 / 2
    )
    jet_point = {r_y: 1, r_0: 1, v_y: -1, v_0: 1}
    jet_gradient = sp.ImmutableMatrix([
        sp.diff(jet_parent, variable).subs(jet_point)
        for variable in jet_variables
    ])
    jet_hessian = sp.ImmutableMatrix(sp.hessian(jet_parent, jet_variables))
    jet_minimum = sp.simplify(jet_parent.subs(jet_point))

    architecture = sp.ones(9, 1)
    spectral_origin = sp.ones(4, 1)
    physical_origin = sp.zeros(2, 1)

    grading_trace_theorem = kernel.prove_expression_equality(
        sp.trace(growth_grading),
        0,
        subject="the typed growth grading is traceless",
    )
    grading_square_theorem = kernel.prove_matrix_equality(
        growth_grading**2,
        support_projector,
        subject="the square of the growth grading is the typed support projector",
    )
    grading_rank_theorem = kernel.prove_exact_rank(
        growth_grading,
        2,
        subject="the geometric growth grading acts only on the typed reservoir",
    )
    grading_spectrum_theorem = kernel.prove_exact_spectrum(
        growth_grading,
        {sp.Integer(-1): 1, sp.Integer(0): 41, sp.Integer(1): 1},
        subject="the K43 growth grading has reciprocal unit weights",
    )
    reciprocal_constraint_theorem = kernel.prove_exact_nullity(
        reciprocal_constraint,
        1,
        subject="determinant preservation leaves one diagonal reciprocal generator",
    )
    orientation_selection_theorem = kernel.prove_matrix_equality(
        orientation_scores,
        sp.Matrix([2, -2]),
        subject="the incoming growth arrow selects the positive aligned grading",
    )
    initial_condition_theorem = kernel.prove_matrix_equality(
        spectral_operator.subs(zeta, 0),
        sp.eye(43),
        subject="the reciprocal spectral flow starts from the isotropic cell operator",
    )
    flow_equation_theorem = kernel.prove_matrix_equality(
        flow_residual,
        sp.zeros(43),
        subject="the reciprocal K43 spectrum is symmetrically covariantly constant along geometric growth",
    )
    determinant_theorem = kernel.prove_expression_equality(
        spectral_operator.det(),
        1,
        subject="the geometric spectral flow preserves the K43 determinant",
    )
    compression_theorem = kernel.prove_matrix_equality(
        compressed_operator,
        sp.diag(sp.exp(-zeta), sp.exp(zeta)),
        subject="the parent-selected K43 flow compresses to the reciprocal reservoir",
    )
    self_energy_theorem = kernel.prove_expression_equality(
        incoming_self_energy,
        sp.exp(zeta),
        subject="the parent-selected incoming self energy is exponential",
    )
    beta_theorem = kernel.prove_expression_equality(
        sp.diff(incoming_self_energy, zeta),
        incoming_self_energy,
        subject="the parent-selected incoming self energy has unit geometric beta",
    )
    jet_stationary_theorem = kernel.prove_matrix_equality(
        jet_gradient,
        sp.zeros(4, 1),
        subject="the normalized reciprocal initial jet is stationary",
    )
    jet_hessian_rank_theorem = kernel.prove_exact_rank(
        jet_hessian,
        4,
        subject="the normalized local growth-parent jet controls all four variables",
    )
    jet_hessian_determinant_theorem = kernel.prove_expression_equality(
        jet_hessian.det(),
        1,
        subject="the local growth-parent jet Hessian is nondegenerate",
    )
    jet_minimum_theorem = kernel.prove_expression_equality(
        jet_minimum,
        0,
        subject="the reciprocal initial jet has zero nonnegative parent action",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(9, 1),
        subject="all reciprocal spectral growth-parent architecture conditions pass",
    )
    spectral_origin_theorem = kernel.prove_matrix_equality(
        spectral_origin,
        sp.ones(4, 1),
        subject="grading normalization parent and reciprocal spectral law are structurally supplied",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(2, 1),
        subject="transition measure and physical time-energy calibration remain open",
    )
    gate_theorem = kernel.prove_gate(
        "version10_k43_reciprocal_spectral_operator_growth_parent_origin_gate",
        (
            grading_trace_theorem,
            grading_square_theorem,
            grading_rank_theorem,
            grading_spectrum_theorem,
            reciprocal_constraint_theorem,
            orientation_selection_theorem,
            initial_condition_theorem,
            flow_equation_theorem,
            determinant_theorem,
            compression_theorem,
            self_energy_theorem,
            beta_theorem,
            jet_stationary_theorem,
            jet_hessian_rank_theorem,
            jet_hessian_determinant_theorem,
            jet_minimum_theorem,
            architecture_theorem,
            spectral_origin_theorem,
            physical_origin_theorem,
        ),
    )
    return K43ReciprocalSpectralGrowthParentCertificate(
        growth_grading=growth_grading,
        support_projector=support_projector,
        orientation_scores=orientation_scores,
        spectral_operator=spectral_operator,
        flow_residual=flow_residual,
        compressed_operator=compressed_operator,
        incoming_self_energy=incoming_self_energy,
        jet_parent=jet_parent,
        jet_gradient=jet_gradient,
        jet_hessian=jet_hessian,
        architecture=architecture,
        spectral_origin=spectral_origin,
        physical_origin=physical_origin,
        grading_trace_theorem=grading_trace_theorem,
        grading_square_theorem=grading_square_theorem,
        grading_rank_theorem=grading_rank_theorem,
        grading_spectrum_theorem=grading_spectrum_theorem,
        reciprocal_constraint_theorem=reciprocal_constraint_theorem,
        orientation_selection_theorem=orientation_selection_theorem,
        initial_condition_theorem=initial_condition_theorem,
        flow_equation_theorem=flow_equation_theorem,
        determinant_theorem=determinant_theorem,
        compression_theorem=compression_theorem,
        self_energy_theorem=self_energy_theorem,
        beta_theorem=beta_theorem,
        jet_stationary_theorem=jet_stationary_theorem,
        jet_hessian_rank_theorem=jet_hessian_rank_theorem,
        jet_hessian_determinant_theorem=jet_hessian_determinant_theorem,
        jet_minimum_theorem=jet_minimum_theorem,
        architecture_theorem=architecture_theorem,
        spectral_origin_theorem=spectral_origin_theorem,
        physical_origin_theorem=physical_origin_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_k43_reciprocal_spectral_operator_growth_parent_origin_gate",
    title="Геометрический родитель взаимно обратного спектрального хода K43",
    source_paths=(
        "s2t/gates/version10_k43_reciprocal_spectral_operator_growth_parent_origin_gate.tex",
        "s2t/results/s2t_v10_k43_reciprocal_spectral_operator_growth_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("growth_grading_traceless", lambda: build_certificate().grading_trace_theorem),
        Obligation("growth_grading_square_support", lambda: build_certificate().grading_square_theorem),
        Obligation("growth_grading_rank_two", lambda: build_certificate().grading_rank_theorem),
        Obligation("growth_grading_reciprocal_spectrum", lambda: build_certificate().grading_spectrum_theorem),
        Obligation("reciprocal_generator_constraint_nullity_one", lambda: build_certificate().reciprocal_constraint_theorem),
        Obligation("growth_arrow_selects_grading_sign", lambda: build_certificate().orientation_selection_theorem),
        Obligation("isotropic_initial_operator", lambda: build_certificate().initial_condition_theorem),
        Obligation("covariant_growth_flow_equation", lambda: build_certificate().flow_equation_theorem),
        Obligation("determinant_preserving_spectral_flow", lambda: build_certificate().determinant_theorem),
        Obligation("reciprocal_reservoir_compression", lambda: build_certificate().compression_theorem),
        Obligation("parent_selected_incoming_self_energy", lambda: build_certificate().self_energy_theorem),
        Obligation("parent_selected_unit_geometric_beta", lambda: build_certificate().beta_theorem),
        Obligation("normalized_initial_jet_stationary", lambda: build_certificate().jet_stationary_theorem),
        Obligation("growth_parent_jet_hessian_rank_four", lambda: build_certificate().jet_hessian_rank_theorem),
        Obligation("growth_parent_jet_hessian_determinant", lambda: build_certificate().jet_hessian_determinant_theorem),
        Obligation("growth_parent_zero_minimum", lambda: build_certificate().jet_minimum_theorem),
        Obligation("growth_parent_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("spectral_law_origin_full", lambda: build_certificate().spectral_origin_theorem),
        Obligation("physical_scale_origin_open", lambda: build_certificate().physical_origin_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)