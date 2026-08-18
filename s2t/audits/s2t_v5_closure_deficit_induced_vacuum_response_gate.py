#!/usr/bin/env python3
"""Audit the finite-rank vacuum response of the closure defect."""
from __future__ import annotations

import json
import math
from pathlib import Path


def response(mass: float, gap: float = 1.0) -> float:
    return (1.0 / 7.0) * math.log1p(gap / (mass * mass))


def radial_response(radius: float, mass: float) -> float:
    return response(mass, 1.0 / (radius * radius))


def main() -> None:
    heat_samples = []
    for t in (0.001, 0.01, 0.1, 1.0, 10.0):
        heat_samples.append(
            {
                "t": t,
                "normalized_heat_response": (1.0 / 7.0) * (1.0 - math.exp(-t)),
            }
        )

    mass_samples = []
    for mass in (0.01, 0.1, 0.5, 1.0, 10.0):
        mass_samples.append({"mass": mass, "response": response(mass)})

    radii = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0)
    radius_samples = [
        {"radius": radius, "response_at_mass_1": radial_response(radius, 1.0)}
        for radius in radii
    ]

    result = {
        "gate": "version5_closure_deficit_induced_vacuum_response_gate",
        "finite_rank_heat_kernel": {
            "identity": "exp(-t H_def)-exp(-t H_closed)=(1-exp(-t)) P_def",
            "defect_rank_per_branch": 15,
            "coefficient_dimension_per_branch": 105,
            "samples": heat_samples,
            "ultraviolet_limit": 0.0,
            "infrared_limit": 1 / 7,
        },
        "relative_determinant": {
            "formula": "(1/7) log((m^2+a)/m^2)",
            "unit_gap_mass_samples": mass_samples,
            "finite_for_positive_mass": True,
            "massless_limit": "positive infinity",
            "large_mass_limit": 0.0,
            "local_counterterm_needed": False,
        },
        "scale_test": {
            "gap": "a(R)=R^-2",
            "samples": radius_samples,
            "strictly_decreasing_with_radius": all(
                radius_samples[i]["response_at_mass_1"]
                > radius_samples[i + 1]["response_at_mass_1"]
                for i in range(len(radius_samples) - 1)
            ),
            "finite_stationary_radius": False,
        },
        "real_pair": {
            "signed_index_supertrace": "cancels between -15 and +15",
            "positive_defect_rank": 30,
            "total_dimension": 210,
            "positive_modulus_weight": 30 / 210,
            "measure_orientation_derived": False,
        },
        "causal_chain": [
            "nonzero KO class",
            "unavoidable compact defect",
            "finite relative vacuum response",
        ],
        "verdict": {
            "universal_relative_response": True,
            "absolute_energy": False,
            "mass_gap_derived": False,
            "finite_radius": False,
            "physical_closure": False,
            "next_gate": "version5_eta_wzw_real_pair_phase_gate",
        },
    }

    assert abs(heat_samples[-1]["normalized_heat_response"] - 1 / 7) < 1e-5
    assert all(
        mass_samples[i]["response"] > mass_samples[i + 1]["response"]
        for i in range(len(mass_samples) - 1)
    )
    assert result["scale_test"]["strictly_decreasing_with_radius"]
    assert result["real_pair"]["positive_modulus_weight"] == 1 / 7

    out = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "s2t_v5_closure_deficit_induced_vacuum_response_gate_results.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()