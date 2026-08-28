#!/usr/bin/env python3
"""Audit the classical color-singlet composite cycle route."""

import hashlib
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    qy, xu, xe, ly = sp.symbols("qy xu xe ly", real=True)
    kappa, mass2 = sp.symbols("kappa mass2", positive=True)
    variables = (qy, xu, xe, ly)

    cycle = qy * xu * xe * ly
    origin = {v: 0 for v in variables}
    cycle_hessian = sp.hessian(cycle, variables).subs(origin)
    massive_potential = mass2 * sum(v**2 for v in variables) - 2 * kappa * cycle
    massive_hessian = sp.hessian(massive_potential, variables).subs(origin)

    result = {
        "gate": "version7_color_preserving_composite_cycle_parent_gate",
        "rooted_cycle": {
            "full_word": "Q_Lu_R * u_RX_L * X_Le_R * e_RL_L * L_LY_R * Y_RQ_L",
            "frozen_H15_roots": ["Q_Lu_R", "e_RL_L"],
            "new_field_word": "u_RX_L * X_Le_R * L_LY_R * Y_RQ_L",
            "new_field_degree": int(sp.Poly(cycle, variables).total_degree()),
            "colored_factors": ["u_RX_L", "Y_RQ_L"],
            "gauge_singlet_as_closed_word": True,
        },
        "local_origin_audit": {
            "gradient_at_origin": [str(sp.diff(cycle, v).subs(origin)) for v in variables],
            "hessian_at_origin": [[str(value) for value in row] for row in cycle_hessian.tolist()],
            "cycle_creates_quadratic_instability": False,
            "positive_mass_hessian": [[str(value) for value in row] for row in massive_hessian.tolist()],
            "positive_mass_origin_remains_locally_stable": True,
        },
        "nonzero_composite_audit": {
            "product_nonzero_implies_every_factor_nonzero": True,
            "nonzero_cycle_implies_colored_factors_nonzero": True,
            "fundamental_color_preserved_if_colored_factors_nonzero": False,
            "independent_sigma_with_constraint_sigma_equals_cycle_repairs_problem": False,
        },
        "scope_boundary": {
            "classical_analytic_cycle_parent_admitted": False,
            "quantum_composite_condensate_tested": False,
            "virtual_heavy_bridge_route_tested": False,
            "required_new_ingredient": "a quantum determinant or Schur-complement integration of massive colored bridges with zero one-point functions",
        },
        "verdict": {
            "status": "classical_composite_cycle_no_go",
            "next_gate": "version7_virtual_colored_bridge_schur_complement_gate",
        },
    }

    out = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_color_preserving_composite_cycle_parent_gate_results.json"
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(output, encoding="utf-8")
    print(out)
    print(hashlib.sha256(output.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()