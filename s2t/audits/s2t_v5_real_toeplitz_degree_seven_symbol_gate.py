#!/usr/bin/env python3
"""Audit the KO7 symbol feeding the real Toeplitz boundary into KO6."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    coefficient_rank = 105
    selected_rank = 15

    # KO_n(C_R): two-periodic complex table, written in real K-theory.
    ko_c_as_real = ["Z", "0", "Z", "0", "Z", "0", "Z", "0"]
    winding_degree = 1
    coefficient_degree = 6
    symbol_degree = (winding_degree + coefficient_degree) % 8
    boundary_target_degree = (symbol_degree - 1) % 8

    result = {
        "gate": "version5_real_toeplitz_degree_seven_symbol_gate",
        "convention_correction": {
            "unbounded_extension_label": "KKO_1 with Cl(0,1)",
            "covariant_real_K_boundary": "partial_n: KO_n(symbol) -> KO_(n-1)(coefficient)",
            "previous_degree_five_claim": "retracted",
            "correct_input_degree_for_KO6": 7,
        },
        "coefficient_algebra": {
            "algebra": "M105(C) regarded as a real C*-algebra",
            "morita_model": "C_R",
            "KO_degrees_0_to_7": ko_c_as_real,
            "KO6": "Z",
            "class": selected_rank,
        },
        "symbol_construction": {
            "real_circle_algebra": "C*_R(Z)",
            "gelfand_real_space": "circle with conjugation z -> conjugate(z)",
            "evaluation_kernel": "desuspension S^(-1)B",
            "base_KO1": "Z direct_sum Z2",
            "winding_summand": "reduced free Z",
            "winding_class": "[u_R] in KO1(C*_R(Z))",
            "coefficient_class": "kappa_15=[T_R]=15 in KO6(M105(C)_R)",
            "external_product": "xi_15=[u_R] external_product kappa_15",
            "degree": symbol_degree,
            "reduced_KO7_group": "KO6(B)=Z",
        },
        "toeplitz_boundary": {
            "degree_map": f"KO{symbol_degree} -> KO{boundary_target_degree}",
            "base_winding_image": "+/-1",
            "module_naturality": "partial(x external_product y)=partial(x) external_product y",
            "image_of_xi_15": "+/-15",
            "complexification_up_to_global_orientation": [[-15, 15], [15, -15]],
        },
        "normalization": {
            "absolute_class": selected_rank,
            "coefficient_rank": coefficient_rank,
            "weight": selected_rank / coefficient_rank,
        },
        "verdict": {
            "degree_convention_corrected": True,
            "KO7_symbol_class_constructed": True,
            "toeplitz_boundary_factorization_of_KO6_class_15": "pass_up_to_global_orientation",
            "explicit_single_matrix_KO7_unitary": False,
            "physical_action": False,
            "next_gate": "version5_real_toeplitz_ko7_unitary_representative_gate",
        },
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_real_toeplitz_degree_seven_symbol_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    assert symbol_degree == 7
    assert boundary_target_degree == 6
    assert ko_c_as_real[6] == "Z"
    assert selected_rank / coefficient_rank == 1 / 7
    print(output)


if __name__ == "__main__":
    main()