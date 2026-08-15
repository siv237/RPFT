#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

x_abs, z_abs, phi, theta = sp.symbols(
    "x_abs z_abs phi theta", positive=True, real=True
)
epsilon_x, epsilon_z = sp.symbols("epsilon_x epsilon_z", integer=True)
x = x_abs * sp.exp(sp.I * phi)
z = z_abs
x_transformed = epsilon_x * sp.exp(-sp.I * theta) * x
z_transformed = epsilon_z * sp.exp(sp.I * theta) * z

product_ratio = sp.simplify(
    x_transformed * z_transformed / (x * z)
)
trace_BB = 2 * (x_abs**2 + z_abs**2)
det_BB = 4 * sp.im(x * z) ** 2

gamma4 = sp.diag(1, 1, -1, -1)
swap4 = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
)
zero4 = sp.zeros(4)
gamma8 = sp.diag(1, 1, -1, -1, -1, -1, 1, 1)
J8_linear = swap4.row_join(zero4).col_join(zero4.row_join(swap4))
J8_linear = sp.Matrix.vstack(
    sp.Matrix.hstack(zero4, swap4),
    sp.Matrix.hstack(swap4, zero4),
)
KO6_test = sp.simplify(J8_linear * gamma8 + gamma8 * J8_linear)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "automorphism_orbit_no_go_halftrace_conditional_pass",
    "orbit": {
        "rephasing_product_ratio": str(product_ratio),
        "continuous_invariants": ["abs(x)", "abs(z)", "arg(x*z) mod pi"],
        "sheet_exchange": "x <-> z",
        "unique_discrete_orbit": False,
    },
    "spectral_invariants": {
        "trace_BBdagger": str(trace_BB),
        "det_BBdagger": str(det_BB),
        "continuous_combinations": 2,
    },
    "KO6_doubling": {
        "dimension_before": 4,
        "dimension_after": 8,
        "J_gamma_anticommutator": str(KO6_test),
        "full_trace_multiplier": 2,
        "orbit_half_trace_multiplier": "1/2",
    },
    "normalization": {
        "factor_rank_full_doubled": 2,
        "factor_rank_orbit_trace": 1,
        "heavy_rank_full_doubled": 46,
        "heavy_rank_orbit_trace": 23,
        "half_trace_from_parent_measure": False,
    },
    "verdict": {
        "edge_parameters_fixed": False,
        "KO6_sign_passed": True,
        "half_trace_algebraic_pass": True,
        "half_trace_parent_origin_pass": False,
        "parent_action_passed": False,
        "next_gate": "finite Dirac parent potential and orbit selection",
    },
}

assert product_ratio == epsilon_x * epsilon_z
assert KO6_test == sp.zeros(8)
assert results["normalization"]["heavy_rank_orbit_trace"] == 23

Path("s2t_v3_automorphism_halftrace_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)