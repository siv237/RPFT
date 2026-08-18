#!/usr/bin/env python3
"""Exact finite obstruction for the Version V reduction triangle."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_reduction_triangle_cocycle_gate_results.json"


def adjacency_star_5():
    matrix = sp.zeros(5)
    for leaf in range(1, 5):
        matrix[0, leaf] = 1
        matrix[leaf, 0] = 1
    return matrix


def adjacency_cycle4_plus_point():
    matrix = sp.zeros(5)
    for left, right in ((0, 1), (1, 2), (2, 3), (3, 0)):
        matrix[left, right] = 1
        matrix[right, left] = 1
    return matrix


lam = sp.symbols("lambda")
star = adjacency_star_5()
cycle_point = adjacency_cycle4_plus_point()

char_star = sp.factor(star.charpoly(lam).as_expr())
char_cycle_point = sp.factor(cycle_point.charpoly(lam).as_expr())
assert sp.expand(char_star - char_cycle_point) == 0
assert sp.expand(char_star - lam**3 * (lam**2 - 4)) == 0

degree_star = sorted([sum(star.row(i)) for i in range(5)], reverse=True)
degree_cycle_point = sorted([sum(cycle_point.row(i)) for i in range(5)], reverse=True)
assert degree_star == [4, 1, 1, 1, 1]
assert degree_cycle_point == [2, 2, 2, 2, 0]
assert degree_star != degree_cycle_point

# Connectivity is checked exactly from powers of I+A: all entries are positive
# iff every pair is joined by a walk of length at most four.
reach_star = sum((star**power for power in range(5)), sp.zeros(5))
reach_cycle_point = sum((cycle_point**power for power in range(5)), sp.zeros(5))
star_connected = all(entry > 0 for entry in reach_star)
cycle_point_connected = all(entry > 0 for entry in reach_cycle_point)
assert star_connected is True
assert cycle_point_connected is False

identity = sp.eye(5)
h_star = 3 * identity - star
h_cycle_point = 3 * identity - cycle_point
h_spectrum_star = sorted([value for value, multiplicity in h_star.eigenvals().items() for _ in range(multiplicity)])
h_spectrum_cycle_point = sorted(
    [value for value, multiplicity in h_cycle_point.eigenvals().items() for _ in range(multiplicity)]
)
assert h_spectrum_star == h_spectrum_cycle_point == [1, 3, 3, 3, 5]

# The heat spectra agree symbolically for arbitrary positive tau because they
# are the exponentials of the same generator eigenvalues.
tau = sp.symbols("tau", positive=True)
heat_spectrum = [sp.exp(-tau * value) for value in h_spectrum_star]
heat_trace = sp.simplify(sum(heat_spectrum))
expected_heat_trace = sp.exp(-tau) + 3 * sp.exp(-3 * tau) + sp.exp(-5 * tau)
assert sp.simplify(heat_trace - expected_heat_trace) == 0

required_sources = {
    "foundational_gate": "s2t/gates/version5_foundational_relative_architecture_gate.tex",
    "heat_dictionary": "s2t/gates/version4_heat_kernel_trace_dictionary_gate.tex",
    "modular_gate": "s2t/gates/version4_modular_endpoint_intertwiner_gate.tex",
    "carrier_measure_gate": "s2t/gates/version5_carrier_measure_freeze_gate.tex",
}
source_presence = {key: (ROOT / value).exists() for key, value in required_sources.items()}
assert all(source_presence.values())

candidates = {
    "operator_logarithm": {
        "recovers": "positive generator on the support",
        "geometry_reconstruction": False,
        "reason": "does not supply coordinate algebra, locality, topology or Dirac sign",
    },
    "gns": {
        "recovers": "cyclic representation from an algebra-state pair",
        "geometry_reconstruction": False,
        "reason": "requires the algebra and supplies no canonical Dirac/locality operator",
    },
    "modular": {
        "recovers": "relative state flow for an algebra-state pair",
        "geometry_reconstruction": False,
        "reason": "does not uniquely select a carrier metric or topology",
    },
    "inverse_spectrum": {
        "recovers": "some invariants or a geometry inside restricted rigid classes",
        "geometry_reconstruction": False,
        "reason": "exact cospectral nonisomorphic counterexample",
    },
    "full_spectral_triple": {
        "recovers": "geometry under reconstruction axioms",
        "geometry_reconstruction": True,
        "reason": "algebra, representation, Dirac and orientation data are already supplied",
        "nontrivial_from_minimal_correlation": False,
    },
    "prior_based_selection": {
        "recovers": "one selected representative",
        "geometry_reconstruction": False,
        "reason": "imports the missing topology/model prior",
    },
}

result = {
    "date": "2026-08-15",
    "gate": "version5_reduction_triangle_cocycle_gate",
    "source_presence": source_presence,
    "exact_cospectral_counterexample": {
        "geometry_1": "connected star K_1,4",
        "geometry_2": "disconnected C_4 plus isolated point",
        "adjacency_characteristic_polynomial": str(char_star),
        "degree_sequence_1": [int(value) for value in degree_star],
        "degree_sequence_2": [int(value) for value in degree_cycle_point],
        "connected_1": star_connected,
        "connected_2": cycle_point_connected,
        "positive_generator_spectrum": [int(value) for value in h_spectrum_star],
        "heat_trace": str(heat_trace),
        "same_all_scalar_spectral_functionals": True,
        "nonisomorphic": True,
    },
    "dirac_square_ambiguity": {
        "identity": "exp(-tau*D^2) = exp(-tau*(-D)^2)",
        "orientation_or_sign_recovered": False,
        "positive_square_root_is_canonical_dirac": False,
    },
    "candidate_classification": candidates,
    "triangle": {
        "T_gs": "partial",
        "T_sc": "operator-level pass",
        "T_cg": "fail on minimal objects",
        "Omega_gsc": "undefined",
    },
    "verdict": {
        "minimal_reduction_triangle": "fail",
        "coefficient_free_nontrivial_T_cg": False,
        "categorical_architecture_pass": False,
        "relative_coboundary_language_retained": True,
        "reason": (
            "weak correlation data underdetermine geometry; enriching them with a full spectral triple "
            "makes the return map tautological rather than generative"
        ),
    },
    "next_gate": {
        "name": "version5_boundary_parent_trace_freeze_gate",
        "question": "can one boundary Hilbert space and trace supply non-tautological locality and gluing data without independent sector weights?",
    },
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))