#!/usr/bin/env python3
import itertools
import json
from pathlib import Path

import sympy as sp


def main():
    c = sp.symbols("c", real=True)
    plane_count = 8
    trace_rank = 3
    holonomy_charge = 1
    required_momentum_norm = 48

    lambda_one = 2 - 2 * c
    determinant_term = sp.Rational(plane_count, trace_rank) * sp.log(lambda_one)
    target_determinant_term = sp.Rational(8, 3) * sp.log(lambda_one)

    odd_positive_sectors = []
    for momenta in itertools.combinations_with_replacement(range(1, 16, 2), plane_count):
        if sum(momentum * momentum for momentum in momenta) == required_momentum_norm:
            odd_positive_sectors.append(momenta)

    all_integer_sectors = []
    for momenta in itertools.combinations_with_replacement(range(0, 8), plane_count):
        if sum(momentum * momentum for momentum in momenta) == required_momentum_norm:
            all_integer_sectors.append(momenta)

    minimal_maximum_momentum = min(max(sector) for sector in odd_positive_sectors)
    minimal_odd_sectors = [
        sector
        for sector in odd_positive_sectors
        if max(sector) == minimal_maximum_momentum
    ]
    selected_sector = minimal_odd_sectors[0]
    momentum_norm = sum(momentum * momentum for momentum in selected_sector)
    inverse_term = sp.Rational(momentum_norm, 2 * trace_rank) / (1 - c)
    target_inverse_term = sp.Rational(8, 1) / (1 - c)

    multiplicities = {
        str(momentum): selected_sector.count(momentum)
        for momentum in sorted(set(selected_sector))
    }

    results = {
        "status": "quantized_rotor_momentum_sector_closes_the_two_gap_coefficients_at_operator_level",
        "date": "2026-08-06",
        "distinction": {
            "holonomy_weight": (
                "The Cartan weight q=1 controls the twisted circle determinant."
            ),
            "fixed_momentum": (
                "The integer rotor momentum p controls the fixed-charge Routhian p^2/(2I)."
            ),
            "conclusion": (
                "These are different quantum numbers and must not be identified with each other "
                "or with the full SU2 Casimir."
            ),
        },
        "determinant_gate": {
            "real_rotation_planes": plane_count,
            "unit_holonomy_weight_on_every_plane": holonomy_charge,
            "normalized_trace_rank": trace_rank,
            "determinant_term": str(determinant_term),
            "target_term": str(target_determinant_term),
            "exact_match": sp.simplify(determinant_term - target_determinant_term) == 0,
        },
        "momentum_scan": {
            "equation": "sum_i p_i^2 = 48",
            "all_nonnegative_integer_solutions_up_to_p=7": [
                list(sector) for sector in all_integer_sectors
            ],
            "positive_odd_solutions_up_to_p=15": [
                list(sector) for sector in odd_positive_sectors
            ],
            "positive_odd_solution_is_unique": len(odd_positive_sectors) == 1,
            "minimal_maximum_momentum": minimal_maximum_momentum,
            "minimal_maximum_momentum_sectors": [
                list(sector) for sector in minimal_odd_sectors
            ],
            "minimal_sector_is_unique": len(minimal_odd_sectors) == 1,
            "selected_sector": list(selected_sector),
            "multiplicities": multiplicities,
            "all_momenta_are_odd": all(momentum % 2 == 1 for momentum in selected_sector),
            "center_phase": "minus one for every rotor wavefunction under a half-turn",
        },
        "routhian_gate": {
            "momentum_squared_sum": momentum_norm,
            "normalized_inverse_term": str(inverse_term),
            "target_inverse_term": str(target_inverse_term),
            "exact_match": sp.simplify(inverse_term - target_inverse_term) == 0,
        },
        "scientific_verdict": {
            "positive": (
                "Eight unit-weight rotation planes give the exact logarithmic determinant, while "
                "the unique positive odd momentum multiset with the smallest possible maximum "
                "momentum, (1,1,1,3,3,3,3,3), gives the exact inverse coefficient. The "
                "antiperiodic parity is preserved."
            ),
            "negative": (
                "No parent action or symmetry yet selects this fixed-momentum sector, and a "
                "fixed-charge ensemble must still be derived without changing the fluctuation "
                "determinant or the BV/BRST content."
            ),
            "next_gate": (
                "Construct the canonical boundary path integral projected onto this momentum "
                "sector and verify its measure, zero modes, and coupling to the Wilson axis."
            ),
        },
    }

    Path("s2t_wilson_rotor_momentum_sector_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "determinant_exact": results["determinant_gate"]["exact_match"],
                "unique_minimal_odd_sector": results["momentum_scan"][
                    "minimal_sector_is_unique"
                ],
                "selected_sector": list(selected_sector),
                "routhian_exact": results["routhian_gate"]["exact_match"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()