#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

chi, radion, alpha, coupling = sp.symbols(
    "chi radion alpha coupling", positive=True
)
B, mu = sp.symbols("B mu", positive=True)

single_field = coupling * chi**4
single_stationary = sp.solve(
    sp.Eq(sp.diff(single_field, chi), 0), chi
)

ratio_potential = coupling * (radion**2 - alpha * chi**2) ** 2
ratio_hessian = sp.simplify(
    sp.hessian(ratio_potential, (chi, radion)).subs(
        {chi: 1, radion: sp.sqrt(alpha)}
    )
)

cw_potential = B * chi**4 * (
    sp.log(chi**2 / mu**2) - sp.Rational(1, 2)
)
cw_first = sp.simplify(sp.diff(cw_potential, chi).subs(chi, mu))
cw_second = sp.simplify(sp.diff(cw_potential, chi, 2).subs(chi, mu))

phi, A = sp.symbols("phi A", positive=True)
dual_potential = A * (sp.exp(2 * phi) + sp.exp(-2 * phi) - 2)
dual_hessian = sp.simplify(sp.diff(dual_potential, phi, 2).subs(phi, 0))

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "classical_scale_no_go_quantum_transmutation_candidate",
    "classical_single_dilaton": {
        "potential": "lambda*chi^4",
        "positive_lambda_nonzero_minimum": False,
        "stationary_points_positive_domain": [
            str(value) for value in single_stationary
        ],
    },
    "classical_two_field": {
        "potential": "lambda*(rho^2-alpha*chi^2)^2",
        "ratio_fixed": "rho/chi=sqrt(alpha)",
        "hessian": str(ratio_hessian),
        "eigenvalues": ["0", "8*alpha*lambda*(alpha+1)"],
        "flat_scale_direction": True,
    },
    "radius_inversion": {
        "potential": "A*(exp(2phi)+exp(-2phi)-2)",
        "minimum_phi": 0,
        "hessian": str(dual_hessian),
        "duality_present_in_current_field_menu": False,
    },
    "coleman_weinberg": {
        "potential": "B*chi^4*(log(chi^2/mu^2)-1/2)",
        "first_derivative_at_mu": str(cw_first),
        "second_derivative_at_mu": str(cw_second),
        "stable_if_B_positive": True,
        "joint_finite_Dirac_minimum": "D_F^2=mu^2 I",
        "selected_edge_modulus": "mu/sqrt(2)",
        "selected_radion": "1/mu",
    },
    "open_quantum_data": {
        "B_computed_from_full_supertrace": False,
        "beta_functions_computed": False,
        "RG_boundary_condition_preregistered": False,
        "dimensionful_observable_predicted": False,
    },
    "verdict": {
        "classical_dilaton_route_passed": False,
        "unproved_duality_route_passed": False,
        "quantum_transmutation_architecture_exists": True,
        "quantum_scale_gate_passed": False,
        "next_gate": "full spectrum supertrace coefficient B",
    },
}

assert single_stationary == []
assert ratio_hessian.eigenvals() == {
    8 * alpha * coupling * (alpha + 1): 1,
    0: 1,
}
assert cw_first == 0
assert cw_second == 8 * B * mu**2
assert dual_hessian == 8 * A

Path("s2t_v3_dilaton_radion_transmutation_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)