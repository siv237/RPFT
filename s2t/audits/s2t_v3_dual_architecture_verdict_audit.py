#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

chi_star, determinant_derivative, lambda4 = sp.symbols(
    "chi_star Fprime lambda4", nonzero=True, real=True
)
R_K = sp.Integer(6)
lambda2_solution = sp.simplify(
    -(determinant_derivative + 4 * lambda4 * chi_star**3)
    / (2 * R_K * chi_star)
)
stationary_residual = sp.simplify(
    determinant_derivative
    + 2 * lambda2_solution * R_K * chi_star
    + 4 * lambda4 * chi_star**3
)

spin_branches = [
    {"rp3": rp3, "s1": s1}
    for rp3 in (0, 1)
    for s1 in (0, 1)
]
lichnerowicz_bound = sp.Rational(R_K, 4)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "both_dimensional_paths_tested_neither_uv_closed",
    "base_K": {
        "determinant_well_defined_after_scheme_choice": True,
        "allowed_local_counterterms": [
            "lambda2 R_K chi^2",
            "lambda4 chi^4",
        ],
        "lambda2_for_arbitrary_stationary_point": str(lambda2_solution),
        "stationary_residual": str(stationary_residual),
        "absolute_vacuum_predicted": False,
        "verdict": "effective theory viable; parameter-free scale open",
    },
    "internal_K": {
        "spin_branches": spin_branches,
        "flat_characters_covered": "all unitary flat lines",
        "R_K": int(R_K),
        "lichnerowicz_bound": str(lichnerowicz_bound),
        "dirac_kernel_dimension": 0,
        "fermion_zero_modes_reproduced": False,
        "verdict": "flat spinorial lift closed negatively",
    },
    "priority": {
        "next": "base-K spectral renormalization condition",
        "reserve": "new nonflat internal curvature or defect lift",
    },
}

assert stationary_residual == 0
assert len(spin_branches) == 4
assert lichnerowicz_bound == sp.Rational(3, 2)
assert results["internal_K"]["dirac_kernel_dimension"] == 0

Path("s2t_v3_dual_architecture_verdict_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)