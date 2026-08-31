#!/usr/bin/env python3
"""Exact audit of the parent origin of the singlet--triplet central trace weight."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate"

    p = sp.symbols("p", positive=True)
    beta = sp.symbols("beta", positive=True)
    delta = sp.symbols("Delta", real=True)
    p1 = sp.diag(1, 0, 0, 0)
    p3 = sp.diag(0, 1, 1, 1)
    grading = sp.diag(-1, 1, 1, 1)

    rho_p = p * p1 + (1 - p) * p3 / 3
    assert sp.trace(rho_p) == 1
    assert sp.simplify(rho_p[1, 1] / rho_p[0, 0] - (1 - p) / (3 * p)) == 0

    rho_counting = sp.eye(4) / 4
    rho_sector = p1 / 2 + p3 / 6
    assert rho_p.subs(p, sp.Rational(1, 4)) == rho_counting
    assert rho_p.subs(p, sp.Rational(1, 2)) == rho_sector

    central_weight = 4 * p * p1 + sp.Rational(4, 3) * (1 - p) * p3
    assert sp.simplify(central_weight * rho_counting - rho_p) == sp.zeros(4)
    assert grading * central_weight == central_weight * grading

    normalized_supertrace_density = grading / sp.trace(grading)
    assert sp.trace(normalized_supertrace_density) == 1
    assert normalized_supertrace_density[0, 0] == -sp.Rational(1, 2)

    boltzmann = sp.exp(-beta * delta)
    gibbs_p = sp.simplify(1 / (1 + 3 * boltzmann))
    gibbs_r = sp.simplify(boltzmann)
    delta_for_p = sp.log(3 * p / (1 - p)) / beta
    assert sp.simplify(gibbs_p.subs(delta, delta_for_p)) == p
    assert sp.simplify(gibbs_r.subs(delta, delta_for_p)) == (1 - p) / (3 * p)
    assert gibbs_p.subs(delta, 0) == sp.Rational(1, 4)
    assert sp.simplify(gibbs_p.subs(delta, sp.log(3) / beta)) == sp.Rational(1, 2)

    entropy = -p * sp.log(p) - (1 - p) * sp.log((1 - p) / 3)
    entropy_prime = sp.simplify(sp.diff(entropy, p))
    entropy_second = sp.simplify(sp.diff(entropy, p, 2))
    assert sp.simplify(entropy_prime - sp.log((1 - p) / (3 * p))) == 0
    assert sp.simplify(entropy_prime.subs(p, sp.Rational(1, 4))) == 0
    assert sp.simplify(entropy_second + 1 / (p * (1 - p))) == 0

    exact_objects = [p1, p3, grading, rho_p, rho_counting, rho_sector, central_weight, normalized_supertrace_density]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate",
        "central_trace_family": {
            "algebra": "C direct_sum M3(C)",
            "state": "p P1 + (1-p) P3/3",
            "free_parameter_interval": "0<p<1",
            "relative_rate": "(1-p)/(3p)",
        },
        "conditional_candidates": {
            "ambient_counting_trace": {"p": "1/4", "relative_rate": 1, "status": "requires equal microscopic trace density"},
            "equal_sector_weight": {"p": "1/2", "relative_rate": "1/3", "status": "distinct positive central trace"},
            "maximum_entropy": {"p": "1/4", "second_derivative": "-1/(p(1-p))", "status": "principle absent from current parent"},
        },
        "central_reweighting": {
            "density_against_counting_trace": "4p P1 + 4(1-p) P3/3",
            "commutes_with_SO3_and_grading": True,
            "preserves_positive_normalized_state": True,
            "removes_weight_freedom": False,
        },
        "supertrace": {
            "normalized_density": "Gamma/Tr(Gamma)=diag(-1,1,1,1)/2",
            "negative_eigenvalue": "-1/2",
            "positive_state": False,
        },
        "gibbs_parent": {
            "hamiltonian": "epsilon_1 P1 + epsilon_3 P3",
            "gap": "Delta=epsilon_3-epsilon_1",
            "p_of_gap": "1/(1+3 exp(-beta Delta))",
            "relative_rate": "exp(-beta Delta)",
            "gap_for_arbitrary_p": "log(3p/(1-p))/beta",
            "all_central_weights_realized": True,
            "gap_selected_by_current_parent": False,
        },
        "parent_origin_ledger": {
            "old_parent": False,
            "ambient_counting_trace": False,
            "grading_supertrace": False,
            "KMS_Gibbs": False,
            "maximum_entropy": False,
            "endpoint_incidence": False,
            "derived_selectors": 0,
            "tested_sources": 6,
        },
        "verdict": {
            "central_weight_selected": False,
            "conditional_counting_value": "p=1/4",
            "minimal_missing_dimensionless_datum": "beta Delta",
            "physical_single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()