#!/usr/bin/env python3
"""Classify candidate Real forms for the balanced Toeplitz KO6 cycle."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    ko_R = ["Z", "Z2", "Z2", "0", "Z", "0", "0", "0"]
    ko_C_as_real = ["Z", "0", "Z", "0", "Z", "0", "Z", "0"]
    degree = 6
    q_rank = 15

    result = {
        "gate": "version5_real_toeplitz_kr_classification_gate",
        "Bott_tables": {
            "KO_n_R_n_0_to_7": ko_R,
            "KO_n_C_as_real_n_0_to_7": ko_C_as_real,
            "degree_tested": degree,
        },
        "candidate_real_forms": {
            "single_branch_pointwise_conjugation": {
                "fixed_algebra": "M105(R)",
                "Morita_base": "R",
                "KO6": ko_R[degree],
                "encodes_L_to_Lstar_exchange": False,
                "verdict": "not_the_project_real_structure",
            },
            "exchange_conjugation_on_oriented_pair": {
                "ambient_complex_algebra": "M105(C) direct_sum M105(C)",
                "involution": "rho(a,b)=(conjugate(b),conjugate(a))",
                "fixed_real_algebra": "{(a,conjugate(a))} isomorphic to M105(C)_as_real",
                "Morita_base": "C_as_real",
                "KO6": ko_C_as_real[degree],
                "encodes_L_to_Lstar_exchange": True,
                "verdict": "selected_by_project_J",
            },
            "quaternionic_single_branch": {
                "compatible_with_J_squared_plus_one": False,
                "compatible_with_odd_complex_rank_105_as_global_quaternionic_module": False,
                "verdict": "excluded",
            },
        },
        "classification_consequence": {
            "ordinary_complex_total_index": 0,
            "oriented_complex_indices": [-q_rank, q_rank],
            "selected_real_group": "KO6(M105(C)_as_real)=Z",
            "nonzero_integer_real_class_is_allowed": True,
            "candidate_integer_magnitude": q_rank,
            "candidate_normalized_weight": q_rank / 105,
            "ordinary_index_cancellation_implies_real_class_zero": False,
        },
        "remaining_proof_obligation": {
            "explicit_Cl06_linear_Fredholm_cycle": False,
            "comparison_map_sends_real_generator_to_oriented_pair": False,
            "sign_and_magnitude_15_certified_in_KO6": False,
            "unbounded_parent_and_physical_localization": False,
        },
        "verdict": {
            "real_form_selected": "exchange_conjugation",
            "KO6_group": "Z",
            "real_class_candidate_survives": True,
            "real_class_proved": False,
            "physical_closure": False,
            "status": "integer_KO6_candidate_15_requires_explicit_Cl06_index",
        },
        "next_gate": "version5_real_toeplitz_cl06_index_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_real_toeplitz_kr_classification_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert ko_R[6] == "0"
    assert ko_C_as_real[6] == "Z"
    assert q_rank / 105 == 1 / 7
    print(output)


if __name__ == "__main__":
    main()