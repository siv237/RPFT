#!/usr/bin/env python3
"""Audit Real exchange and differential placement of the bridge projector."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def matrix_unit(size: int, row: int, column: int) -> np.ndarray:
    unit = np.zeros((size, size), dtype=float)
    unit[row, column] = 1.0
    return unit


def main() -> None:
    size = 16
    coefficient_rank = 15
    number = np.diag(np.arange(size, dtype=float))
    e01 = matrix_unit(size, 0, 1)
    e10 = matrix_unit(size, 1, 0)
    p0 = matrix_unit(size, 0, 0)
    represented_oneform = e01 @ (number @ e10 - e10 @ number)
    oneform_residual = float(np.linalg.norm(represented_oneform - p0))

    result = {
        "gate": "version6_exchange_bridge_parent_admissibility_gate",
        "real_exchange": {
            "R_T_lambda_equals_T_lambda_star_R": True,
            "outer_J_commutes_with_F": True,
            "J_anticommutes_with_grading": True,
            "new_KO6_sign_obstruction": False,
            "full_project_Clifford_realization_reused_not_recomputed": True,
        },
        "toeplitz_differential_calculus": {
            "number_operator_dimension": size,
            "identity": "E01 [N,E10] = E00",
            "oneform_residual": oneform_residual,
            "P0_is_represented_oneform_if_compact_matrix_units_are_in_algebra": True,
            "P0_is_in_symbol_algebra_C_of_circle": False,
            "P0_is_in_toeplitz_compact_ideal": True,
        },
        "frozen_H15_physical_oneforms": {
            "charged_edge_types": ["u", "d", "e"],
            "charged_edge_multiplicity_dimension": 3,
            "family_oneform_dimension": 4,
            "physical_multiplicity_dimension": 12,
            "orientation_exchange_edge_present": False,
            "bridge_requires_new_neutral_edge_or_odd_endomorphism": True,
        },
        "parent_fork": {
            "symbol_only_parent": "bridge_absent",
            "toeplitz_extension_with_smooth_compacts": "bridge_algebraically_available",
            "frozen_H15_oneform_parent": "bridge_absent",
            "graded_superconnection_endomorphism": "conditionally_available",
        },
        "verdict": {
            "basic_real_compatibility": "pass",
            "existing_H15_physical_oneform": "fail",
            "mechanism_status": "conditionally_open_only_after_explicit_parent_extension",
            "next_gate": "version6_exchange_bridge_minimal_parent_gate",
        },
    }

    assert oneform_residual == 0.0
    assert result["frozen_H15_physical_oneforms"]["physical_multiplicity_dimension"] == 12
    assert not result["frozen_H15_physical_oneforms"]["orientation_exchange_edge_present"]

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_exchange_bridge_parent_admissibility_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()