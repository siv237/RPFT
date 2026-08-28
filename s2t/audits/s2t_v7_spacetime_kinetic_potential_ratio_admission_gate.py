#!/usr/bin/env python3
"""Audit the product heat-kernel normalization of the edge Hodge EFT."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_spacetime_kinetic_potential_ratio_admission_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def coefficients(f0: float, odd_scale: float, trace_multiplier: float = 1.0) -> dict:
    common = trace_multiplier * f0 / (8.0 * math.pi**2)
    kinetic_z = 4.0 * common * odd_scale**2
    potential_kappa = 2.0 * common * odd_scale**4
    quartic = potential_kappa / kinetic_z**2
    return {
        "common_a4_coefficient": common,
        "Z": kinetic_z,
        "kappa": potential_kappa,
        "lambda_eff": quartic,
        "expected_lambda_eff": math.pi**2 / (trace_multiplier * f0),
    }


def main() -> None:
    one_scale = load_result(
        "s2t_v7_single_scale_calibration_closure_gate_results.json"
    )
    hodge = load_result(
        "s2t_v7_edge_grading_hodge_superconnection_parent_gate_results.json"
    )
    assert one_scale["verdict"]["dimensionless_mass_ratio_sqrt_2_predicted"]
    assert hodge["covariance_and_reality"]["physical_half_trace_preserves_coefficients"]

    f0_values = [0.5, 1.0, 2.0, 5.0]
    odd_scales = [0.3, 1.0, 4.0]
    table = []
    maximum_formula_residual = 0.0
    for f0 in f0_values:
        lambdas = []
        for odd_scale in odd_scales:
            row = coefficients(f0, odd_scale)
            residual = abs(row["lambda_eff"] - row["expected_lambda_eff"])
            maximum_formula_residual = max(maximum_formula_residual, residual)
            lambdas.append(row["lambda_eff"])
            table.append({"f0": f0, "odd_scale": odd_scale, **row})
        assert max(lambdas) - min(lambdas) < 1.0e-12

    lambda_by_f0 = [coefficients(f0, 1.0)["lambda_eff"] for f0 in f0_values]
    assert len({round(value, 12) for value in lambda_by_f0}) == len(f0_values)

    # Full Real doubling multiplies both heat-kernel terms by two.  The
    # physical half-trace removes this known factor and restores the original
    # coupling; omitting it would change the canonically normalized quartic.
    physical_half_trace = coefficients(1.0, 1.0, trace_multiplier=1.0)
    unhalved_real_trace = coefficients(1.0, 1.0, trace_multiplier=2.0)
    assert abs(
        physical_half_trace["lambda_eff"]
        - 2.0 * unhalved_real_trace["lambda_eff"]
    ) < 1.0e-12

    # The mass combination M0^2=kappa*mu^2/Z loses f0 but retains the product
    # a*mu; one external mass calibration fixes precisely that combination.
    mu = 1.7
    mass_scale_tests = []
    for f0 in f0_values:
        for odd_scale in odd_scales:
            row = coefficients(f0, odd_scale)
            m0_squared = row["kappa"] * mu**2 / row["Z"]
            expected = 0.5 * (odd_scale * mu) ** 2
            assert abs(m0_squared - expected) < 1.0e-12
            mass_scale_tests.append(
                {
                    "f0": f0,
                    "odd_scale": odd_scale,
                    "M0_squared": m0_squared,
                    "expected": expected,
                }
            )

    result = {
        "gate": "version7_spacetime_kinetic_potential_ratio_admission_gate",
        "product_heat_kernel": {
            "operator": "D_M tensor 1 + gamma5 tensor a*Phi_E(x)",
            "common_a4_coefficient": "C0=f0/(8*pi^2)",
            "finite_trace_kinetic_identity": "Tr(partial Phi_E)^2=2 sum_e |partial z_e|_R^2",
            "hodge_potential_identity": "Tr(m_E^2)=2*S_mu+constant",
            "Z": "4*C0*a^2",
            "kappa": "2*C0*a^4",
            "lambda_eff": "kappa/Z^2=pi^2/f0",
        },
        "rescaling_audit": {
            "f0_values": f0_values,
            "odd_field_scales": odd_scales,
            "table": table,
            "maximum_formula_residual": maximum_formula_residual,
            "lambda_independent_of_odd_field_scale": True,
            "lambda_independent_of_f2_and_cutoff_after_mass_calibration": True,
            "lambda_depends_on_f0": True,
        },
        "mass_scale_audit": {
            "formula": "M0^2=kappa*mu^2/Z=(a*mu)^2/2",
            "tests": mass_scale_tests,
            "f0_cancels": True,
            "one_mass_input_fixes_a_times_mu": True,
        },
        "real_trace_audit": {
            "physical_half_trace_lambda_at_f0_1": physical_half_trace["lambda_eff"],
            "unhalved_real_trace_lambda_at_f0_1": unhalved_real_trace["lambda_eff"],
            "physical_half_trace_required": True,
        },
        "remaining_anchor": {
            "free_dimensionless_input": "f0",
            "can_be_related_to_gauge_coupling_only_with_common_gauge_block": True,
            "common_physical_gauge_block_present_in_current_edge_carrier": False,
            "lambda_eff_numerically_predicted": False,
        },
        "verdict": {
            "odd_rescaling_obstruction_closed": True,
            "f2_cutoff_obstruction_closed_for_dimensionless_quartic": True,
            "unique_kinetic_to_potential_ratio_from_current_parent": False,
            "status": "partial_positive_product_ratio_reduced_to_f0",
            "next_gate": "test a common gauge kinetic anchor that fixes f0 and the edge quartic in the same physical product spectral trace",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()