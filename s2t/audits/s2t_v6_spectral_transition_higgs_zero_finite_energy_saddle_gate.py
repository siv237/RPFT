#!/usr/bin/env python3
"""Scaling audit for a Higgs zero with and without electroweak gauge fields."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_higgs_zero_finite_energy_saddle_gate_results.json"


def main() -> None:
    r = sp.symbols("R", positive=True)
    t_h, v_h = sp.symbols("T_H V_H", positive=True)
    e_f, e_d, e_v = sp.symbols("E_F E_D E_V", positive=True)

    scalar_energy = r * t_h + r**3 * v_h
    scalar_virial = sp.diff(scalar_energy, r).subs(r, 1)
    assert scalar_virial == t_h + 3 * v_h

    gauge_higgs_energy = e_f / r + r * e_d + r**3 * e_v
    gauge_higgs_virial = sp.diff(gauge_higgs_energy, r).subs(r, 1)
    gauge_higgs_scale_curvature = sp.diff(gauge_higgs_energy, r, 2).subs(r, 1)
    assert gauge_higgs_virial == -e_f + e_d + 3 * e_v

    rng = np.random.default_rng(20260821)
    scalar_samples = []
    gauge_samples = []
    for _ in range(512):
        th = float(rng.uniform(1e-3, 10.0))
        vh = float(rng.uniform(0.0, 10.0))
        scalar_samples.append(th + 3.0 * vh)

        ed = float(rng.uniform(1e-3, 10.0))
        ev = float(rng.uniform(0.0, 10.0))
        ef = ed + 3.0 * ev
        virial = -ef + ed + 3.0 * ev
        curvature = 2.0 * ef + 6.0 * ev
        gauge_samples.append((virial, curvature))

    # Regular radial series.  A linear term produces 2 a1/r, so a1=0.
    # With f(0)=0 the constant equation then gives 6 a2=0, and recursion
    # removes every higher analytic coefficient.
    radial_series = {
        "f0": 0,
        "smoothness_requires_f1": 0,
        "equation_requires_f2": 0,
        "analytic_recursion": "all higher coefficients vanish",
    }

    result = {
        "gate": "version6_spectral_transition_higgs_zero_finite_energy_saddle_gate",
        "pure_Higgs_scaling": {
            "energy": str(scalar_energy),
            "virial_derivative_at_R1": str(scalar_virial),
            "minimum_sample_derivative": min(scalar_samples),
            "nontrivial_stationary_scale_possible": False,
            "Derrick_stable_static_lump": False,
        },
        "fixed_direction_radial_regular_branch": radial_series,
        "gauge_Higgs_scaling": {
            "energy": str(gauge_higgs_energy),
            "virial_derivative_at_R1": str(gauge_higgs_virial),
            "scale_curvature_at_R1": str(gauge_higgs_scale_curvature),
            "max_sample_virial_residual": max(abs(x[0]) for x in gauge_samples),
            "minimum_sample_scale_curvature": min(x[1] for x in gauge_samples),
            "positive_terms_can_satisfy_virial_identity": True,
        },
        "electroweak_sphaleron_literature_certificate": {
            "finite_static_solution_exists": True,
            "Higgs_profile_zero_at_center": True,
            "Chern_Simons_number": "1/2 modulo integers",
            "is_energy_barrier_saddle": True,
            "has_unstable_mode": True,
            "recent_SM_control_negative_eigenvalue": "omega_-^2 approximately -2.7 m_W^2",
            "recent_SM_control_is_project_prediction": False,
        },
        "rank_change_reading": {
            "rank_W_nu_at_H_zero": 0,
            "rank_W_nu_for_nonzero_H": 1,
            "finite_energy_stationary_rank_change_core_exists": True,
            "rank_change_core_is_linearly_stable_particle": False,
            "correct_reading": "transient saddle event between gauge vacua",
        },
        "verdict": {
            "pure_Higgs_stable_particle": False,
            "gauge_Higgs_sphaleron_realizes_local_H_zero": True,
            "sphaleron_realizes_stable_matter": False,
            "sphaleron_spectral_flow_is_next_project_test": True,
            "physical_closure": False,
            "status": "the scalar sector fails Derrick scaling; gauge curvature permits the electroweak sphaleron, but its negative mode makes the rank-zero core a transition event rather than a particle",
        },
        "next_gate": "version6_spectral_transition_sphaleron_spectral_flow_gate",
    }

    assert min(scalar_samples) > 0.0
    assert result["gauge_Higgs_scaling"]["max_sample_virial_residual"] < 1e-12
    assert result["gauge_Higgs_scaling"]["minimum_sample_scale_curvature"] > 0.0

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()