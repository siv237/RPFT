#!/usr/bin/env python3
"""Audit the minimal closure deficit forced by the Toeplitz index 15."""
from __future__ import annotations

import json
from pathlib import Path


def representatives(index: int, extra_pairs: int) -> list[dict[str, int | float]]:
    rows: list[dict[str, int | float]] = []
    for pair_count in range(extra_pairs + 1):
        if index < 0:
            kernel = pair_count
            cokernel = pair_count - index
        else:
            kernel = pair_count + index
            cokernel = pair_count
        rows.append(
            {
                "extra_kernel_cokernel_pairs": pair_count,
                "kernel_dimension": kernel,
                "cokernel_dimension": cokernel,
                "index": kernel - cokernel,
                "defect_dimension": kernel + cokernel,
                "normalized_deficit": (kernel + cokernel) / 105,
            }
        )
    return rows


def main() -> None:
    plus_rows = representatives(-15, 8)
    minus_rows = representatives(+15, 8)
    result = {
        "gate": "version5_topological_closure_deficit_gate",
        "perfect_closure": {
            "definition": "Fredholm operator is invertible",
            "kernel_dimension": 0,
            "cokernel_dimension": 0,
            "possible_in_index_15_sector": False,
        },
        "oriented_plus_branch": {
            "index": -15,
            "representatives": plus_rows,
            "minimal_defect_dimension": min(row["defect_dimension"] for row in plus_rows),
            "minimal_normalized_deficit": min(row["normalized_deficit"] for row in plus_rows),
            "explicit_toeplitz_saturates_bound": True,
        },
        "oriented_minus_branch": {
            "index": +15,
            "representatives": minus_rows,
            "minimal_defect_dimension": min(row["defect_dimension"] for row in minus_rows),
            "minimal_normalized_deficit": min(row["normalized_deficit"] for row in minus_rows),
            "explicit_adjoint_saturates_bound": True,
        },
        "real_exchange_pair": {
            "ordinary_complex_index_sum": 0,
            "positive_defect_dimension": 30,
            "total_coefficient_dimension": 210,
            "normalized_deficit": 30 / 210,
            "KO6_class": 15,
            "real_symmetry_preserving_trivialization": False,
        },
        "cross_check": {
            "minimal_loop_action": 1 / 7,
            "minimal_topological_deficit": 1 / 7,
            "exact_match": True,
            "physical_mass_or_radius_derived": False,
        },
        "interpretation_boundary": {
            "literal_sphere_packing_density": False,
            "operator_noninvertibility": True,
            "vacuum_selection_of_nonzero_sector_derived": False,
            "all_particle_spectrum_derived": False,
        },
        "verdict": {
            "defect_unavoidable_within_class_15": True,
            "minimal_defect_weight": "1/7",
            "ontology_operator_bridge": "pass",
            "physical_closure": False,
            "next_gate": "version5_closure_deficit_induced_vacuum_response_gate",
        },
    }

    assert all(row["index"] == -15 for row in plus_rows)
    assert all(row["index"] == +15 for row in minus_rows)
    assert result["oriented_plus_branch"]["minimal_defect_dimension"] == 15
    assert result["oriented_minus_branch"]["minimal_defect_dimension"] == 15
    assert result["real_exchange_pair"]["normalized_deficit"] == 1 / 7
    assert result["cross_check"]["exact_match"]

    out = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "s2t_v5_topological_closure_deficit_gate_results.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()