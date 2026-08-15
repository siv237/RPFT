#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

c_A, c_sigma, delta_kk = sp.symbols(
    "c_A c_sigma delta_kk", real=True
)

finite_numerator = sp.Integer(40)
gauge_ghost_numerator = 3 * c_A**2
dilaton_numerator = c_sigma**2
full_numerator = sp.expand(
    finite_numerator
    + gauge_ghost_numerator
    + dilaton_numerator
    + delta_kk
)
B_full = full_numerator / (64 * sp.pi**2)

positive_branch = sp.simplify(B_full.subs({c_A: 0, c_sigma: 0, delta_kk: 0}))
negative_branch = sp.simplify(B_full.subs({c_A: 0, c_sigma: 0, delta_kk: -41}))

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "gauge_ghost_nonnegative_kk_completion_underspecified",
    "ledger": {
        "finite_numerator": int(finite_numerator),
        "gauge_ghost_numerator": str(gauge_ghost_numerator),
        "dilaton_numerator": str(dilaton_numerator),
        "kk_numerator": str(delta_kk),
        "full_numerator": str(full_numerator),
        "B_full": str(B_full),
    },
    "derived": {
        "finite_seed_positive": True,
        "massive_unitary_vector_weight": 3,
        "gauge_ghost_contribution_nonnegative": True,
        "gauge_mass_ratio_derived": False,
        "kk_finite_part_derived": False,
    },
    "sign_audit": {
        "zero_correction_branch": str(positive_branch),
        "negative_unspecified_kk_example": str(negative_branch),
        "sign_fixed_by_current_axioms": False,
    },
    "missing_specification": [
        "physical gauge quotient",
        "canonical gauge coupling",
        "BV/BRST complex",
        "field-specific KK Hessians",
        "spin and flat-bundle branches",
        "common finite-part prescription",
    ],
    "verdict": {
        "full_B_computed": False,
        "finite_parent_block_retained": True,
        "next_gate": "full fluctuated product Dirac and BV complex",
    },
}

assert positive_branch == sp.Rational(5, 8) / sp.pi**2
assert negative_branch == -sp.Rational(1, 64) / sp.pi**2
assert sp.diff(gauge_ghost_numerator, c_A, 2) == 6

Path("s2t_v3_gauge_ghost_kk_completion_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)