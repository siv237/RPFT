#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

rp3_scalar_curvature = sp.Integer(6)
s1_scalar_curvature = sp.Integer(0)
product_scalar_curvature = rp3_scalar_curvature + s1_scalar_curvature
lichnerowicz_lower_bound = sp.simplify(product_scalar_curvature / 4)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "dimensional_architecture_must_be_selected_before_kk_sum",
    "architecture_A_base_K": {
        "dimension": 4,
        "interpretation": "K is Euclidean spacetime base",
        "extra_KK_sum_allowed": False,
        "reason": "eigenmodes on K are spacetime determinant modes, not extra species",
    },
    "architecture_B_internal_K": {
        "external_dimension": 4,
        "internal_dimension": 4,
        "total_dimension": 8,
        "heat_kernel_factorization_required": True,
        "flat_external_a4_sufficient": False,
    },
    "spinorial_internal_lift": {
        "R_RP3": int(rp3_scalar_curvature),
        "R_S1": int(s1_scalar_curvature),
        "R_K": int(product_scalar_curvature),
        "lichnerowicz_lower_bound_R_over_4": str(lichnerowicz_lower_bound),
        "harmonic_spinors": 0,
        "finite_fermion_zero_modes_automatic": False,
    },
    "status_of_previous_results": {
        "kappa": 2,
        "g_squared": "3/8",
        "B_zero_finite_gauge": "67/(64*pi^2)",
        "valid_as_4D_zero_mode_effective_action": True,
        "valid_as_full_M4_times_K_compactification": False,
    },
    "verdict": {
        "kk_branch_audit_started": False,
        "reason": "base/internal K ambiguity",
        "next_gate": "select base-K determinant or internal-K zero-mode lift",
    },
}

assert product_scalar_curvature == 6
assert lichnerowicz_lower_bound == sp.Rational(3, 2)
assert results["architecture_A_base_K"]["extra_KK_sum_allowed"] is False
assert results["architecture_B_internal_K"]["total_dimension"] == 8

Path("s2t_v3_dimensional_product_consistency_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)