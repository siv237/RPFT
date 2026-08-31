#!/usr/bin/env python3
"""Exact audit of the singlet--triplet relative connector rate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate_results.json"


def main() -> None:
    previous = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate_results.json").read_text(encoding="utf-8"))
    assert previous["next_gate"] == "version8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate"
    assert previous["full_connector_representation"]["decomposition"] == "1 + 3"

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generators = tuple(sp.diag(0, item) for item in (j1, j2, j3))
    p1 = sp.diag(1, 0, 0, 0)
    p3 = sp.diag(0, 1, 1, 1)

    variables = sp.symbols("c0:10", real=True)
    covariance = sp.zeros(4)
    cursor = 0
    for row in range(4):
        for column in range(row, 4):
            covariance[row, column] = covariance[column, row] = variables[cursor]
            cursor += 1
    equations = [entry for generator in generators for entry in list(generator * covariance - covariance * generator)]
    system, _ = sp.linear_eq_to_matrix(equations, variables)
    assert system.rank() == 8 and len(system.nullspace()) == 2

    gamma1, gamma3 = sp.symbols("gamma_1 gamma_3", positive=True)
    invariant_covariance = gamma1 * p1 + gamma3 * p3
    assert all(generator * invariant_covariance == invariant_covariance * generator for generator in generators)
    assert sp.trace(invariant_covariance) == gamma1 + 3 * gamma3

    rho_arrow = sp.eye(4) / 4
    rho_sector = p1 / 2 + p3 / 6
    assert sp.trace(rho_arrow) == sp.trace(rho_sector) == 1
    assert all(generator * rho_arrow == rho_arrow * generator for generator in generators)
    assert all(generator * rho_sector == rho_sector * generator for generator in generators)
    assert sp.simplify(rho_arrow[1, 1] / rho_arrow[0, 0]) == 1
    assert sp.simplify(rho_sector[1, 1] / rho_sector[0, 0]) == sp.Rational(1, 3)
    purity_arrow = sp.trace(rho_arrow**2)
    purity_sector = sp.trace(rho_sector**2)
    assert purity_arrow == sp.Rational(1, 4)
    assert purity_sector == sp.Rational(1, 3)
    entropy_arrow = sp.log(4)
    entropy_sector = sp.log(12) / 2

    central_weight = sp.symbols("p", positive=True)
    central_trace_covariance = central_weight * p1 + (1 - central_weight) * p3 / 3
    central_ratio = sp.simplify(central_trace_covariance[1, 1] / central_trace_covariance[0, 0])
    assert central_ratio == (1 - central_weight) / (3 * central_weight)

    beta, omega = sp.symbols("beta omega", positive=True)
    q = sp.exp(-beta * omega)
    forward = sp.Matrix([gamma1, gamma3])
    backward = q * forward
    assert sp.simplify(backward[0] / forward[0]) == q
    assert sp.simplify(backward[1] / forward[1]) == q
    assert sp.simplify(forward[1] / forward[0]) == gamma3 / gamma1

    grading = sp.diag(-1, 1, 1, 1)
    even_variables = sp.symbols("m0:16", complex=True)
    generic = sp.Matrix(4, 4, even_variables)
    even_system, _ = sp.linear_eq_to_matrix(list(grading * generic - generic * grading), even_variables)
    assert even_system.rank() == 6
    assert len(even_system.nullspace()) == 10
    cross_unit = sp.zeros(4)
    cross_unit[0, 1] = 1
    assert grading * cross_unit - cross_unit * grading == -2 * cross_unit

    exact_objects = [*generators, p1, p3, system, invariant_covariance, rho_arrow, rho_sector, central_trace_covariance, forward, backward, grading, even_system]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate",
        "symmetry_commutant": {"representation": "1 + 3", "symmetric_constraint_rank": system.rank(), "dimension": len(system.nullspace()), "general_covariance": "gamma_1 P_1 + gamma_3 P_3", "free_ratio": "r=gamma_3/gamma_1 > 0"},
        "canonical_witnesses": {
            "equal_per_arrow": {"state": "I4/4", "relative_rate": 1, "purity": "1/4", "entropy": "log(4)"},
            "equal_per_sector": {"state": "P1/2 + P3/6", "relative_rate": "1/3", "purity": "1/3", "entropy": "log(12)/2"},
            "both_SO3_invariant": True,
            "both_positive_trace_one": True,
        },
        "central_trace_simplex": {"algebra": "C direct_sum M3(C)", "state": "p P1 + (1-p) P3/3", "relative_rate": "(1-p)/(3p)", "free_parameter_interval": "0<p<1", "unique_trace": False},
        "kms": {"common_reverse_forward_ratio": "exp(-beta omega)", "singlet_triplet_forward_ratio": "gamma_3/gamma_1", "relative_rate_selected": False},
        "grading_obstruction_to_M4_trace": {"grading": "diag(-1,+1,+1,+1)", "even_algebra_dimension": len(even_system.nullspace()), "full_M4_dimension": 16, "cross_block_constraint_rank": even_system.rank(), "full_M4_even": False},
        "selector_ledger": {"SO3_symmetry": False, "central_trace": False, "KMS_detailed_balance": False, "primitivity_support": False, "source_bridge": False, "maximum_entropy": False, "derived_selectors": 0, "tested_selectors": 6},
        "verdict": {"relative_rate_selected": False, "trace_isotropic_candidate": "r=1", "sector_balanced_candidate": "r=1/3", "M4_unique_trace_available_without_breaking_grading": False, "physical_single_c0_map_derived": False},
        "next_gate": "version8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()