#!/usr/bin/env python3
import json
import math
from pathlib import Path

import sympy as sp


def main():
    weight_zero, weight_one, tau_scale = sp.symbols(
        "weight_zero weight_one tau_scale", positive=True
    )
    tau_raw = sp.pi**2 + 2 * sp.pi + sp.Rational(2, 3)
    neutrino_target = 23 + 1 / sp.pi

    tau_norm = tau_scale**2 * weight_zero * tau_raw
    neutrino_norm = 23 * weight_zero + weight_one / sp.pi

    target_solution = sp.solve(
        [
            sp.Eq(tau_norm.subs(tau_scale, 1), tau_raw),
            sp.Eq(neutrino_norm, neutrino_target),
        ],
        [weight_zero, weight_one],
        dict=True,
    )

    results = {
        "date": "2026-08-09",
        "version": "S2T-III",
        "status": "algebraic_two_sector_pass_embedding_origin_open",
        "metric": {
            "zero_form_weight": str(weight_zero),
            "integral_one_form_weight": str(weight_one),
            "factor_blind": True,
            "sector_blind": True,
        },
        "embeddings": {
            "tau": "1_RP3 direct_sum 1_S1 direct_sum P_perp_n",
            "neutrino": "P_H tensor normalized_1_S1 direct_sum P_ker tensor e1",
            "e1_integral_period": 1,
            "tau_background_scale": str(tau_scale),
        },
        "norms": {
            "tau_symbolic": str(tau_norm),
            "neutrino_symbolic": str(neutrino_norm),
            "tau_at_unit_weights_and_scale": float(tau_raw.evalf()),
            "neutrino_at_unit_weights": float(neutrino_target.evalf()),
        },
        "unit_embedding_solution": [
            {str(key): str(value) for key, value in solution.items()}
            for solution in target_solution
        ],
        "field_redefinition_gate": {
            "tau_scale_fixed_by_integral_period": False,
            "tau_scale_fixed_by_L2_normalization": False,
            "tau_scale_fixed_by_current_symmetry": False,
            "neutrino_cycle_scale_fixed_by_integral_period": True,
            "parent_action_passed": False,
        },
        "next_gate": (
            "Derive the tau background scale from a compact phase, canonical "
            "symplectic form, boundary AKSZ pairing, or finite spectral triple."
        ),
    }

    assert target_solution == [{weight_one: 1, weight_zero: 1}]
    assert math.isclose(results["norms"]["tau_at_unit_weights_and_scale"], 16.81945637)
    assert not results["field_redefinition_gate"]["parent_action_passed"]

    Path("s2t_v3_role_graded_hessian_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()