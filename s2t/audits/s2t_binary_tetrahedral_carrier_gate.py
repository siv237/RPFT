#!/usr/bin/env python3
import json
import math
from pathlib import Path

from scipy.special import k1


ALPHA_INV = 137.035999177


def chebyshev_u(degree, value):
    if degree == 0:
        return 1.0
    if degree == 1:
        return 2.0 * value
    previous = 1.0
    current = 2.0 * value
    for _ in range(2, degree + 1):
        previous, current = current, 2.0 * value * current - previous
    return current


def invariant_dimension(degree):
    real_parts = [1.0, -1.0] + [0.0] * 6 + [0.5] * 8 + [-0.5] * 8
    average = sum(chebyshev_u(degree, value) for value in real_parts) / 24.0
    return int(round(average))


def coexact_multiplicity(level):
    return (
        invariant_dimension(level + 1) * level
        + invariant_dimension(level - 1) * (level + 2)
    )


def bessel_tail(max_level=101, max_winding=30):
    levels = []
    total = 0.0
    for level in range(1, max_level):
        multiplicity = coexact_multiplicity(level)
        if multiplicity == 0:
            continue
        rho = level + 1.0
        contribution = multiplicity * rho * sum(
            k1(2.0 * math.pi * winding * rho) / winding
            for winding in range(1, max_winding)
        )
        total += contribution
        levels.append(
            {
                "level": level,
                "eigenvalue": (level + 1) ** 2,
                "multiplicity": multiplicity,
                "contribution": float(contribution),
            }
        )
    return float(total), levels


def vacuum_scalar(value):
    return value - 1.0 / (24.0 * value) - 1.0 / (math.pi**4 * value**2)


def main():
    scalar_shells = [
        {
            "degree": degree,
            "eigenvalue": degree * (degree + 2),
            "invariant_dimension": invariant_dimension(degree),
            "quotient_multiplicity": invariant_dimension(degree) * (degree + 1),
        }
        for degree in range(25)
        if invariant_dimension(degree) > 0
    ]
    coexact_total, coexact_levels = bessel_tail()

    original_s_geo = 4.0 * math.pi**3 + math.pi**2 + math.pi
    quotient_volume = math.pi**2 / 12.0
    systole = math.pi / 3.0
    candidate_s_geo = 4.0 * math.pi**3 + quotient_volume + systole
    candidate_s_vac = vacuum_scalar(candidate_s_geo)

    regular_dimension = 24
    augmentation_dimension = regular_dimension - 1
    q8_coset_count = 3
    q8_invariants_in_augmentation = q8_coset_count - 1

    results = {
        "date": "2026-08-09",
        "status": "binary_tetrahedral_direct_carrier_route_closed",
        "group": {
            "name": "binary tetrahedral group 2T = SL(2,3)",
            "order": 24,
            "abelianization": "Z3",
            "quotient_volume_unit_radius": quotient_volume,
            "systole_unit_radius": systole,
            "flat_U1_character_count": 3,
        },
        "carrier_tests": {
            "required_Z_A": math.pi**2,
            "candidate_Z_A": quotient_volume,
            "volume_ratio_required": 12.0,
            "required_flat_phase_step": math.pi,
            "candidate_flat_phase_step": 2.0 * math.pi / 3.0,
            "passes_original_carrier_definition": False,
        },
        "vacuum_scalar_direct_substitution": {
            "original_S_geo": original_s_geo,
            "original_S_vac": vacuum_scalar(original_s_geo),
            "candidate_S_geo_using_geometric_systole": candidate_s_geo,
            "candidate_S_vac": candidate_s_vac,
            "candidate_minus_alpha_inverse": candidate_s_vac - ALPHA_INV,
            "natural_spectral_compensation_identified": False,
        },
        "scalar_spectrum": {
            "character_average": "dim Sym^ell(C2)^2T = |2T|^-1 sum_g U_ell(Re g)",
            "nonzero_shells_through_degree_24": scalar_shells,
            "first_positive_degree": scalar_shells[1]["degree"],
            "first_positive_eigenvalue": scalar_shells[1]["eigenvalue"],
            "first_positive_multiplicity": scalar_shells[1]["quotient_multiplicity"],
        },
        "coexact_spectrum": {
            "multiplicity_formula": (
                "n*dim Sym^(n+1)(C2)^2T + (n+2)*dim Sym^(n-1)(C2)^2T"
            ),
            "first_levels": coexact_levels[:8],
            "positive_Bessel_tail": coexact_total,
            "first_level_fraction": coexact_levels[0]["contribution"]
            / coexact_total,
            "C6_tail_cancelled": False,
        },
        "regular_representation_gate": {
            "regular_dimension": regular_dimension,
            "augmentation_ideal_dimension": augmentation_dimension,
            "unique_2T_invariant_line_in_regular_representation": True,
            "2T_invariant_lines_in_augmentation_ideal": 0,
            "Q8_acts_on_regular_representation": True,
            "Q8_invariant_dimension_in_regular_representation": q8_coset_count,
            "Q8_invariant_dimension_in_augmentation_ideal": (
                q8_invariants_in_augmentation
            ),
            "quotient_spectrum_keeps_Gamma_invariants_not_augmentation_ideal": True,
            "augmentation_ideal_is_natural_physical_spectral_sector": False,
        },
        "verdict": (
            "S3/2T fails the locked volume and phase carrier tests. Its coexact tail "
            "remains positive. The canonical 23-dimensional augmentation ideal belongs "
            "to the deck-group regular representation, whereas the quotient spectrum "
            "keeps invariant states and projects that ideal out. The route survives only "
            "as a new model with an added internal C[2T] fiber."
        ),
    }

    assert results["carrier_tests"]["passes_original_carrier_definition"] is False
    assert results["scalar_spectrum"]["first_positive_degree"] == 6
    assert results["scalar_spectrum"]["first_positive_eigenvalue"] == 48
    assert results["coexact_spectrum"]["first_levels"][0]["level"] == 1
    assert results["coexact_spectrum"]["first_levels"][0]["multiplicity"] == 3
    assert results["coexact_spectrum"]["positive_Bessel_tail"] > 0.0
    assert results["regular_representation_gate"][
        "Q8_invariant_dimension_in_augmentation_ideal"
    ] == 2

    Path("s2t_binary_tetrahedral_carrier_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()