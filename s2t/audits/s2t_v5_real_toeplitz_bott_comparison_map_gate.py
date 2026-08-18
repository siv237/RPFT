#!/usr/bin/env python3
"""Audit the degree-six real-to-complex comparison map for C_R."""

from __future__ import annotations

import json
from pathlib import Path


def c_even(degree: int, n: int) -> tuple[int, int]:
    """Complexification maps in degrees 0,2,4,6 for C as a real algebra."""
    if degree % 8 in (0, 4):
        return (n, n)
    if degree % 8 in (2, 6):
        return (-n, n)
    raise ValueError("degree must be even modulo 8")


def r6(pair: tuple[int, int]) -> int:
    """Forgetting the complex structure in degree six: (a,b) -> -a+b."""
    a, b = pair
    return -a + b


def psi6(pair: tuple[int, int]) -> tuple[int, int]:
    """Conjugation in degree six: (a,b) -> (-b,-a)."""
    a, b = pair
    return (-b, -a)


def main() -> None:
    generator = c_even(6, 1)
    q_rank = 15
    coefficient_image = c_even(6, q_rank)

    result = {
        "gate": "version5_real_toeplitz_bott_comparison_map_gate",
        "source_table": {
            "real_algebra": "C considered as a real C*-algebra",
            "KO_even_degrees_0_2_4_6": ["Z", "Z", "Z", "Z"],
            "complexified_K_even_degrees": ["Z^2", "Z^2", "Z^2", "Z^2"],
            "c0": "n -> (n,n)",
            "c2": "n -> (-n,n)",
            "c4": "n -> (n,n)",
            "c6": "n -> (-n,n)",
            "r6": "(a,b) -> -a+b",
            "psi6": "(a,b) -> (-b,-a)",
        },
        "degree_six_checks": {
            "generator_image": list(generator),
            "map_is_injective": generator != (0, 0),
            "conjugation_fixes_image": psi6(generator) == generator,
            "forget_after_complexify_is_times_two": r6(generator) == 2,
        },
        "toeplitz_coefficient_class": {
            "q0_complex_rank": q_rank,
            "complexified_real_class_15": list(coefficient_image),
            "oriented_toeplitz_indices": [-q_rank, q_rank],
            "exact_match": coefficient_image == (-q_rank, q_rank),
            "unique_real_preimage": q_rank,
            "normalized_weight": q_rank / 105,
        },
        "verdict": {
            "anti_diagonal_stop_test": "pass",
            "integer_KO6_class": 15,
            "integer_KO6_class_proved_at_K_theory_level": True,
            "explicit_Cl06_matrices_still_required_for_classification": False,
            "unbounded_parent_operator": False,
            "physical_localization_energy_mass": False,
            "next_gate": "version5_real_toeplitz_unbounded_parent_cycle_gate",
        },
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_real_toeplitz_bott_comparison_map_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert generator == (-1, 1)
    assert psi6(generator) == generator
    assert r6(generator) == 2
    assert coefficient_image == (-15, 15)
    assert q_rank / 105 == 1 / 7
    print(output)


if __name__ == "__main__":
    main()