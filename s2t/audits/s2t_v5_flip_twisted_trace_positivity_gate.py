#!/usr/bin/env python3
"""Positivity and faithfulness audit for a trace twisted by a central flip."""

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_flip_twisted_trace_positivity_gate_results.json"

# Abstract rho-trace weights on the two central idempotents.
w_plus, w_minus = sp.symbols("w_plus w_minus", real=True)

# tau(e_+ e_+) = tau(rho(e_+) e_+) = tau(e_- e_+) = 0,
# and similarly for e_-.
trace_equations = [sp.Eq(w_plus, 0), sp.Eq(w_minus, 0)]
trace_solution = sp.solve(trace_equations, [w_plus, w_minus], dict=True)
assert trace_solution == [{w_minus: 0, w_plus: 0}]

# Explicit left-representation projectors from the real-scalar flip gate.
I3 = np.eye(3)
Z3 = np.zeros((3, 3))


def block_diag(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size))
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


P_plus = block_diag([I3, Z3, Z3, Z3, I3, Z3])
P_minus = block_diag([Z3, Z3, Z3, I3, Z3, Z3])
P_fixed = np.eye(18) - P_plus - P_minus

rank_plus = int(np.linalg.matrix_rank(P_plus))
rank_minus = int(np.linalg.matrix_rank(P_minus))
rank_fixed = int(np.linalg.matrix_rank(P_fixed))
assert (rank_plus, rank_minus, rank_fixed) == (6, 3, 9)

# A sharp rank-15 intertwiner: pair three dimensions in each flipped sector,
# kill the unmatched three-dimensional part of P_plus, and keep the fixed
# complement invertible.
W = np.array(P_fixed, copy=True)
W[0:3, 9:12] = I3
W[9:12, 0:3] = I3

intertwiner_residual_plus = np.linalg.norm(P_plus @ W - W @ P_minus)
intertwiner_residual_minus = np.linalg.norm(P_minus @ W - W @ P_plus)
rank_W = int(np.linalg.matrix_rank(W))
assert intertwiner_residual_plus == 0.0
assert intertwiner_residual_minus == 0.0
assert rank_W == 15

rank_bound = rank_fixed + 2 * min(rank_plus, rank_minus)
assert rank_bound == 15
assert rank_bound < 18

result = {
    "date": "2026-08-16",
    "gate": "version5_flip_twisted_trace_positivity_gate",
    "abstract_rho_trace": {
        "convention": "tau(a b) = tau(rho(b) a)",
        "central_flip": "rho(e_plus)=e_minus, rho(e_minus)=e_plus",
        "solution_on_flipped_idempotents": {
            "tau_e_plus": 0,
            "tau_e_minus": 0,
        },
        "faithful": False,
        "positivity_needed_for_no_go": False,
    },
    "represented_weight": {
        "Hilbert_dimension": 18,
        "rank_P_plus": rank_plus,
        "rank_P_minus": rank_minus,
        "rank_fixed_complement": rank_fixed,
        "intertwiner_rank_upper_bound": rank_bound,
        "sharp_example_rank": rank_W,
        "intertwiner_residual_plus": float(intertwiner_residual_plus),
        "intertwiner_residual_minus": float(intertwiner_residual_minus),
        "invertible_weight_exists": False,
        "positive_faithful_weight_exists": False,
    },
    "finite_modular_state": {
        "faithful_density_matrix_is_invertible": True,
        "modular_automorphism_is_inner": True,
        "center_fixed_pointwise": True,
        "rank_mismatched_central_flip_possible": False,
    },
    "normalization": {
        "common_kinetic_curvature_trace": False,
        "singular_support_projector_required": True,
        "new_measure_data_required": True,
    },
    "verdict": {
        "faithful_abstract_rho_trace": "impossible",
        "positive_invertible_represented_weight": "impossible",
        "faithful_finite_modular_flip": "impossible",
        "finite_real_scalar_twisted_route": "closed",
        "type_III_or_indefinite_replacement": "new_architecture",
        "physical_closure": False,
    },
    "next_gate": "version5_derived_moment_map_minimal_data_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))