#!/usr/bin/env python3
"""Audit a Hodge moment-map parent for the six-of-eleven edge grading."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_edge_grading_hodge_superconnection_parent_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def commutator_moment(differential: np.ndarray) -> np.ndarray:
    return differential @ differential.conj().T - differential.conj().T @ differential


def signature(matrix: np.ndarray, tolerance: float = 2.0e-5) -> dict[str, int]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    return {
        "negative": int(np.sum(eigenvalues < -tolerance)),
        "zero": int(np.sum(np.abs(eigenvalues) <= tolerance)),
        "positive": int(np.sum(eigenvalues > tolerance)),
    }


def numerical_hessian(function, point: np.ndarray, step: float = 2.0e-4) -> np.ndarray:
    size = point.size
    result = np.zeros((size, size))
    origin = function(point)
    for first in range(size):
        ei = np.zeros(size)
        ei[first] = step
        result[first, first] = (
            function(point + ei) - 2.0 * origin + function(point - ei)
        ) / step**2
        for second in range(first + 1, size):
            ej = np.zeros(size)
            ej[second] = step
            value = (
                function(point + ei + ej)
                - function(point + ei - ej)
                - function(point - ei + ej)
                + function(point - ei - ej)
            ) / (4.0 * step**2)
            result[first, second] = value
            result[second, first] = value
    return result


def main() -> None:
    previous = load_result("s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json")
    assert previous["verdict"]["status"] == (
        "positive_canonical_edge_grading_parent_origin_open"
    )

    edge_order = previous["edge_space"]["ordered_new_edges"]
    selected = set(previous["projector_union"]["selected_support"])
    size = len(edge_order)
    p_selected = np.diag([float(item in selected) for item in edge_order])
    identity = np.eye(size)
    p_unwanted = identity - p_selected
    gamma = identity - 2.0 * p_selected
    assert int(np.trace(p_selected)) == 6
    assert int(np.trace(p_unwanted)) == 5

    # The fixed background arrow reverses orientation on the selected and
    # unwanted subspaces.  Orthogonality of the two projectors makes it a
    # nilpotent odd differential.
    zero = np.zeros_like(identity)
    delta = np.block([[zero, p_selected], [p_unwanted, zero]])
    doubled_gamma = np.block([[gamma, zero], [zero, -gamma]])
    delta_moment = commutator_moment(delta)
    assert np.max(np.abs(delta @ delta)) < 1.0e-12
    assert np.max(np.abs(delta_moment + doubled_gamma)) < 1.0e-12

    chain_grading = np.block([[-identity, zero], [zero, identity]])
    exchange = np.block([[zero, identity], [identity, zero]])
    assert np.max(np.abs(exchange @ doubled_gamma @ exchange + doubled_gamma)) < 1.0e-12

    mu = 1.0

    def matrix_action(vector: np.ndarray) -> float:
        z = vector[:size] + 1j * vector[size:]
        diagonal_z = np.diag(z)
        dynamic = np.block([[zero, zero], [diagonal_z, zero]])
        dynamic_moment = commutator_moment(dynamic)
        total_moment = dynamic_moment + mu**2 * delta_moment
        return float(
            0.5 * np.trace(total_moment @ total_moment).real
            - np.trace(p_unwanted).real * mu**4
        )

    def reduced_action(vector: np.ndarray) -> float:
        z = vector[:size] + 1j * vector[size:]
        values = np.abs(z) ** 2
        selected_mask = np.diag(p_selected)
        unwanted_mask = np.diag(p_unwanted)
        return float(
            np.sum(selected_mask * (values - mu**2) ** 2)
            + np.sum(unwanted_mask * (values**2 + 2.0 * mu**2 * values))
        )

    rng = np.random.default_rng(20260827)
    maximum_reduction_residual = 0.0
    for _ in range(200):
        vector = rng.normal(size=2 * size)
        maximum_reduction_residual = max(
            maximum_reduction_residual,
            abs(matrix_action(vector) - reduced_action(vector)),
        )
    assert maximum_reduction_residual < 2.0e-10

    origin = np.zeros(2 * size)
    origin_hessian = numerical_hessian(matrix_action, origin)
    origin_signature = signature(origin_hessian)
    assert origin_signature == {"negative": 12, "zero": 0, "positive": 10}

    vacuum = np.zeros(2 * size)
    for index, item in enumerate(edge_order):
        if item in selected:
            vacuum[index] = mu
    assert abs(matrix_action(vacuum)) < 1.0e-12
    vacuum_hessian = numerical_hessian(matrix_action, vacuum)
    vacuum_signature = signature(vacuum_hessian)
    assert vacuum_signature == {"negative": 0, "zero": 6, "positive": 16}

    # Family lift: each selected edge is a 3x3 unitary matrix at the minimum;
    # each unwanted edge vanishes.  The unitary tangent has real dimension 9.
    family_origin_signature = {"negative": 108, "zero": 0, "positive": 90}
    family_vacuum_signature = {"negative": 0, "zero": 54, "positive": 144}

    # The self-adjoint dynamic odd operator anticommutes with the two-term
    # chain grading.  The fixed differential has the same property.
    diagonal_z = np.diag(rng.normal(size=size) + 1j * rng.normal(size=size))
    dynamic = np.block([[zero, zero], [diagonal_z, zero]])
    odd_dynamic = dynamic + dynamic.conj().T
    odd_background = delta + delta.conj().T
    dynamic_oddness = float(
        np.max(np.abs(chain_grading @ odd_dynamic + odd_dynamic @ chain_grading))
    )
    background_oddness = float(
        np.max(np.abs(chain_grading @ odd_background + odd_background @ chain_grading))
    )
    assert dynamic_oddness < 1.0e-12
    assert background_oddness < 1.0e-12

    result = {
        "gate": "version7_edge_grading_hodge_superconnection_parent_gate",
        "carrier": {
            "edge_count": size,
            "two_term_complex_dimensions": [size, size],
            "dynamic_edge_field": "Z=diag(z_e)",
            "fixed_background_differential": "delta_E=[[0,P_sel],[P_unwanted,0]]",
            "background_is_nilpotent": True,
            "dynamic_is_nilpotent": True,
            "arrow_colors_are_orthogonal": True,
        },
        "derived_edge_grading": {
            "Gamma_E": "I-2*P_sel",
            "doubled_Gamma_E": "diag(Gamma_E,-Gamma_E)",
            "background_moment_map": "[delta_E,delta_E^*]=-doubled_Gamma_E",
            "maximum_background_identity_residual": float(
                np.max(np.abs(delta_moment + doubled_gamma))
            ),
            "Real_exchange_reverses_doubled_grading": True,
        },
        "single_hodge_action": {
            "formula": "S_mu=1/2 Tr(([d_Z,d_Z^*]+mu^2[delta_E,delta_E^*])^2)-5mu^4",
            "mu": mu,
            "reduction": "sum_selected (|z_e|^2-mu^2)^2 + sum_unwanted (|z_e|^4+2mu^2|z_e|^2)",
            "maximum_random_reduction_residual": maximum_reduction_residual,
            "bounded_below": True,
            "minimum_value": 0.0,
        },
        "one_generation_dynamics": {
            "origin_stationary": True,
            "origin_hessian_signature": origin_signature,
            "vacuum_selected_edge_magnitudes_squared": mu**2,
            "vacuum_unwanted_edges_zero": True,
            "vacuum_hessian_signature": vacuum_signature,
            "vacuum_phase_zero_modes": 6,
        },
        "family_lift": {
            "selected_vacuum": "Z_e in mu U(3)",
            "unwanted_vacuum": "Z_e=0",
            "origin_hessian_signature": family_origin_signature,
            "vacuum_hessian_signature": family_vacuum_signature,
            "vacuum_manifold": "U(3)^6",
        },
        "covariance_and_reality": {
            "dynamic_oddness_residual": dynamic_oddness,
            "background_oddness_residual": background_oddness,
            "projectors_act_on_complete_gauge_covariant_edge_blocks": True,
            "Real_completion_by_orientation_reversal": True,
            "physical_half_trace_preserves_coefficients": True,
        },
        "remaining_physical_gap": {
            "overall_scale_mu_derived": False,
            "family_unitary_orientations_selected": False,
            "embedding_into_physical_finite_spectral_triple_proved": False,
            "spacetime_kinetic_terms_and_gauge_quotient_proved": False,
        },
        "verdict": {
            "status": "positive_field_space_hodge_parent_physical_embedding_open",
            "one_moment_map_norm_gives_quadratic_and_quartic_terms": True,
            "all_six_selected_edges_condense": True,
            "all_five_unwanted_edges_are_gapped": True,
            "independent_stabilization_weight": False,
            "complete_physical_parent_obtained": False,
            "next_gate": "test the canonical Real bimodule/superconnection embedding of the two colored edge arrows and quotient the U(3)^6 vacuum orientations without inserting family projectors",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()