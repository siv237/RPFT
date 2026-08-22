#!/usr/bin/env python3
"""Audit project-wide fractional determinant/Pfaffian barrier candidates."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np


def residual_curvature(nu: Fraction) -> Fraction:
    return Fraction(-51, 112) + Fraction(9, 2) * nu


def main() -> None:
    upper = Fraction(17, 168)
    candidates = [
        {
            "name": "M300_full_complex_pair",
            "nu": Fraction(30, 300),
            "operator_status": "candidate_requires_product_Dirac_and_R_coupling",
        },
        {
            "name": "M300_real_pfaffian",
            "nu": Fraction(15, 300),
            "operator_status": "candidate_requires_product_KO2_pfaffian",
        },
        {
            "name": "M210_real_pfaffian",
            "nu": Fraction(15, 210),
            "operator_status": "candidate_requires_trace_transport_to_global_parent",
        },
        {
            "name": "M210_full_complex_pair",
            "nu": Fraction(30, 210),
            "operator_status": "derived_positive_modulus_weight_but_too_large_for_instability",
        },
        {
            "name": "periodic_Maxwell_ghost_constant_branch",
            "nu": Fraction(1, 24),
            "operator_status": "wrong_operator_no_map_to_family_logdet",
        },
    ]
    rows = []
    for candidate in candidates:
        nu = candidate["nu"]
        curvature = residual_curvature(nu)
        rows.append(
            {
                "name": candidate["name"],
                "nu": float(nu),
                "nu_exact": str(nu),
                "inside_fractional_window": Fraction(0, 1) < nu < upper,
                "residual_local_curvature": float(curvature),
                "residual_local_curvature_exact": str(curvature),
                "local_instability_survives": curvature < 0,
                "operator_status": candidate["operator_status"],
            }
        )

    rng = np.random.default_rng(20260819)
    matrix_checks = []
    for _ in range(20):
        raw = rng.normal(size=(3, 3))
        state = raw @ raw.T + np.eye(3)
        state /= np.trace(state)
        logdet_state = float(np.linalg.slogdet(state)[1])
        repeated = np.kron(np.eye(15), state)
        zero = np.zeros_like(repeated)
        antisymmetric = np.block([[zero, repeated], [-repeated.T, zero]])
        logdet_antisymmetric = float(np.linalg.slogdet(antisymmetric)[1])
        normalized_log_pfaffian = 0.5 * logdet_antisymmetric / 300.0
        matrix_checks.append(
            {
                "logdet_R": logdet_state,
                "normalized_log_pfaffian": normalized_log_pfaffian,
                "target_one_over_20_logdet_R": logdet_state / 20.0,
                "residual": normalized_log_pfaffian - logdet_state / 20.0,
            }
        )

    result = {
        "gate": "version6_fractional_determinant_measure_origin_gate",
        "admissible_window": {
            "lower": 0.0,
            "upper": float(upper),
            "upper_exact": str(upper),
        },
        "candidate_ledger": rows,
        "exact_relations": {
            "M300_determinant_weight": "30/300=1/10",
            "M300_pfaffian_weight": "15/300=1/20",
            "M210_pfaffian_weight": "15/210=1/14",
            "M210_determinant_weight": "30/210=1/7",
            "distance_from_M300_determinant_to_upper_bound": "17/168-1/10=1/840",
            "M300_determinant_residual_curvature": "-3/560",
            "M300_pfaffian_residual_curvature": "-129/560",
        },
        "matrix_pfaffian_modulus_checks": {
            "family_block": "I15 tensor R",
            "antisymmetric_form": "[[0,M],[-M^T,0]]",
            "identity": "(1/300) log|Pf A_R| = (1/20) log det R",
            "samples": matrix_checks,
            "maximum_residual": max(abs(item["residual"]) for item in matrix_checks),
        },
        "project_archaeology": {
            "M300_unique_normalized_trace_retained": True,
            "M300_coordinate_algebra_derived": False,
            "M210_to_M300_trace_preserving_embedding_derived": False,
            "internal_KO6_real_fermion_integral_sufficient": False,
            "product_total_KO2_required": True,
            "kappa_Cas_1_over_24_has_family_R_operator_map": False,
            "C6_scalar_half_residual_has_family_R_operator_map": False,
        },
        "verdict": {
            "project_contains_coefficients_inside_window": True,
            "fractional_barrier_parent_action_proved": False,
            "strongest_global_candidate": "M300 real Pfaffian nu=1/20 or full determinant nu=1/10",
            "next_gate": "version6_product_ko2_family_pfaffian_operator_gate",
        },
    }

    assert Fraction(1, 10) < upper
    assert upper - Fraction(1, 10) == Fraction(1, 840)
    assert residual_curvature(Fraction(1, 10)) == Fraction(-3, 560)
    assert residual_curvature(Fraction(1, 20)) == Fraction(-129, 560)
    assert residual_curvature(Fraction(1, 14)) == Fraction(-15, 112)
    assert residual_curvature(Fraction(1, 7)) == Fraction(3, 16)
    assert result["matrix_pfaffian_modulus_checks"]["maximum_residual"] < 1e-14

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_fractional_determinant_measure_origin_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()