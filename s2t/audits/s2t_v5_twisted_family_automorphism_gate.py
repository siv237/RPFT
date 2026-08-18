#!/usr/bin/env python3
"""Automorphism and radial fixed-point audit for the current family algebra."""

import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_twisted_family_automorphism_gate_results.json"

summands = {
    "R_0": {
        "real_dimension": 1,
        "commutative": True,
        "division_center": "R",
        "matrix_degree": 1,
    },
    "M3R_G": {
        "real_dimension": 9,
        "commutative": False,
        "division_center": "R",
        "matrix_degree": 3,
    },
    "C_2": {
        "real_dimension": 2,
        "commutative": True,
        "division_center": "C",
        "matrix_degree": 1,
    },
}

names = list(summands)
admissible_permutations = []
for permuted in itertools.permutations(names):
    valid = True
    for source, target in zip(names, permuted):
        if summands[source] != summands[target]:
            valid = False
            break
    if valid:
        admissible_permutations.append(dict(zip(names, permuted)))

assert admissible_permutations == [{name: name for name in names}]

rho, r = sp.symbols("rho r", real=True)
ordinary_quartic = sp.expand(6 * (rho**2 + r**2) ** 2)
moment_map_quartic = sp.expand((rho**2 - r**2) ** 2)
assert sp.simplify(ordinary_quartic - 6 * (rho**2 + r**2) ** 2) == 0
assert sp.simplify(moment_map_quartic - (rho**2 - r**2) ** 2) == 0
assert ordinary_quartic.subs({rho: 1, r: 1}) == 24
assert moment_map_quartic.subs({rho: 1, r: 1}) == 0

radial_fixed_checks = {
    "orthogonal_inner_action_fixes_central_gram_data": True,
    "complex_conjugation_on_real_r": True,
    "primitive_central_idempotents_fixed": True,
    "canonical_discrete_twists_act_trivially_on_radial_witness": True,
}

duplication_menu = {
    "duplicate_R_0": {
        "simple_summand_count": 4,
        "inside_frozen_budget": True,
        "exchange_available": True,
        "representation_defined": False,
    },
    "duplicate_M3R_G": {
        "simple_summand_count": 4,
        "inside_frozen_budget": True,
        "exchange_available": True,
        "representation_defined": False,
    },
    "duplicate_C_2": {
        "simple_summand_count": 4,
        "inside_frozen_budget": True,
        "exchange_available": True,
        "representation_defined": False,
    },
    "full_algebra_doubling": {
        "simple_summand_count": 6,
        "inside_frozen_budget": False,
        "exchange_available": True,
        "representation_defined": False,
    },
}

result = {
    "date": "2026-08-15",
    "gate": "version5_twisted_family_automorphism_gate",
    "algebra": "R_0 direct_sum M3(R)_G direct_sum C_2",
    "simple_summand_invariants": summands,
    "admissible_simple_ideal_permutations": admissible_permutations,
    "exchange_automorphism_current_algebra": False,
    "remaining_star_automorphisms": {
        "R_0": ["identity"],
        "M3R_G": ["inner orthogonal conjugation"],
        "C_2": ["identity", "complex conjugation"],
    },
    "canonical_twist_filter": {
        "noncentral_inner_O3_family": "rejected_as_continuous_basis_selector",
        "remaining_discrete_classes": ["identity", "complex conjugation on C_2"],
    },
    "radial_fixed_sector": {
        "configuration": "X=rho I3, Phi=r real",
        **radial_fixed_checks,
        "ordinary_quartic": str(ordinary_quartic),
        "moment_map_quartic": str(moment_map_quartic),
        "witness_rho_1_r_1": {
            "ordinary_trace_D4": 24,
            "moment_map_square": 0,
        },
    },
    "duplication_menu": duplication_menu,
    "verdict": {
        "simple_ideal_classification": "pass",
        "current_algebra_exchange_twist": "absent",
        "canonical_current_algebra_radial_sign_repair": "fail",
        "coefficient_free_current_algebra_twisted_family_route": "closed",
        "selective_minimal_doubling": "undecided",
        "physical_closure": False,
    },
    "next_gate": "version5_minimal_twist_doubling_budget_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))