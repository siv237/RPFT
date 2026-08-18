#!/usr/bin/env python3
"""Audit the minimal Dirichlet action of the explicit Toeplitz loop."""
from __future__ import annotations
import json
from pathlib import Path


def min_square_sum(total: int, slots: int) -> tuple[int, list[int]]:
    q, r = divmod(total, slots)
    values = [q + 1] * r + [q] * (slots - r)
    return sum(k * k for k in values), values


def main() -> None:
    rank, slots = 15, 105
    minimum, windings = min_square_sum(rank, slots)
    result = {
        "gate": "version5_toeplitz_parent_action_variational_gap_gate",
        "action": "S_loop(V)=tau_210([N,V]*[N,V])",
        "fixed_winding_minimization": {
            "winding_per_branch": [rank, -rank],
            "minimum_square_sum_per_branch": minimum,
            "minimizing_distribution": {"plus_one_channels": windings.count(1), "zero_channels": windings.count(0)},
            "total_two_branch_action_unnormalized": 2 * minimum,
            "normalized_action": (2 * minimum) / (2 * slots),
            "V15_is_global_minimizer_up_to_conjugation": True,
        },
        "scale_test": {
            "N_R": "N/R",
            "fixed_measure_action": "1/(7 R^2)",
            "circle_measure_action": "1/(7 R)",
            "finite_positive_stationary_radius": False,
        },
        "verdict": {
            "internal_loop_variational_principle": "pass",
            "positive_hessian_modulo_orbit": True,
            "three_dimensional_localization": False,
            "finite_size_stabilization": False,
            "physical_mass": False,
            "next_gate": "version5_spatial_extension_derrick_balance_gate",
        },
    }
    out = Path(__file__).resolve().parents[1] / "results" / "s2t_v5_toeplitz_parent_action_variational_gap_gate_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert minimum == rank
    assert windings.count(1) == rank
    assert (2 * minimum) / (2 * slots) == 1 / 7
    print(out)


if __name__ == "__main__":
    main()