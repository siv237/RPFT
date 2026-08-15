#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

fermion_charge_square = sp.Integer(2)
scalar_charge_square = sp.Integer(2)
b = (
    sp.Rational(2, 3) * fermion_charge_square
    + sp.Rational(1, 3) * scalar_charge_square
)
g_squared_matching = sp.Rational(3, 8)
landau_log_ratio = sp.simplify(8 * sp.pi**2 / (b * g_squared_matching))

mu, mu0, rg_time = sp.symbols("mu mu0 rg_time", positive=True)
inverse_g_squared = (
    1 / g_squared_matching
    - b / (8 * sp.pi**2) * sp.log(mu / mu0)
)
inverse_g_squared_in_time = (
    1 / g_squared_matching
    - b / (8 * sp.pi**2) * rg_time
)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "one_absolute_scale_input_unavoidable",
    "charge_ledger": {
        "weyl_charge_square": int(fermion_charge_square),
        "complex_scalar_charge_square": int(scalar_charge_square),
        "one_loop_b": str(b),
    },
    "gauge_running": {
        "beta_g": "b*g^3/(16*pi^2)",
        "nonzero_one_loop_fixed_point": False,
        "spectral_matching_g_squared": str(g_squared_matching),
        "inverse_g_squared_solution": str(inverse_g_squared),
        "landau_log_ratio": str(landau_log_ratio),
        "landau_ratio": "exp(32*pi^2/3)",
    },
    "scale_setting": {
        "dimensional_transmutation_removes_scale_input": False,
        "trace_anomaly_fixes_boundary_condition": False,
        "rg_integration_constant_required": True,
    },
    "status_correction": {
        "g_squared_3_over_8": "matching relation at mu_spec",
        "scale_independent_constant": False,
    },
    "verdict": {
        "minimum_train_scales": 1,
        "next_gate": "one-scale train and dimensionless blind scorecard",
    },
}

assert b == 2
assert landau_log_ratio == sp.Rational(32, 3) * sp.pi**2
assert sp.diff(inverse_g_squared_in_time, rg_time) == -b / (8 * sp.pi**2)

Path("s2t_v3_rg_anomaly_scale_setting_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)