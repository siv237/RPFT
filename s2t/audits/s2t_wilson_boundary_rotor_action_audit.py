#!/usr/bin/env python3
import json
import math
from pathlib import Path

import sympy as sp


def main():
    c = sp.symbols("c", real=True)
    response = sp.Rational(1, 45) + sp.Rational(8, 3) * (2 + c) / (1 - c) ** 2
    potential = (
        sp.Rational(8, 3) * (sp.Rational(3, 1) / (1 - c) + sp.log(1 - c))
        - sp.Rational(44, 45) * c
    )
    derivative_check = sp.simplify(sp.diff(potential, c) - (response - 1))

    target_cosine = (sp.Integer(26) - 9 * sp.sqrt(15)) / 11
    target_curvature = sp.simplify(sp.diff(potential, c, 2).subs(c, target_cosine))

    solutions = []
    for mode_count in range(1, 129):
        for trace_rank in range(1, 25):
            log_coefficient = sp.Rational(mode_count, 2 * trace_rank)
            if log_coefficient != sp.Rational(8, 3):
                continue
            for charge_norm_squared in range(1, 13):
                inverse_coefficient = (
                    sp.Rational(mode_count * charge_norm_squared, 2 * trace_rank)
                )
                if inverse_coefficient == 8:
                    solutions.append(
                        {
                            "mode_count": mode_count,
                            "trace_rank": trace_rank,
                            "charge_norm_squared": charge_norm_squared,
                        }
                    )

    minimal_solution = min(
        solutions, key=lambda row: (row["mode_count"], row["trace_rank"])
    )

    su2_casimirs = []
    for twice_spin in range(0, 13):
        spin = sp.Rational(twice_spin, 2)
        casimir = sp.simplify(spin * (spin + 1))
        su2_casimirs.append(
            {
                "spin": str(spin),
                "dimension": int(2 * spin + 1),
                "quadratic_casimir": str(casimir),
                "equals_required_three": casimir == 3,
            }
        )

    canonical_vector_prediction = {
        "SO3_vector_casimir": 2,
        "log_coefficient": str(sp.Rational(8, 3)),
        "inverse_coefficient": str(sp.Rational(16, 3)),
        "required_inverse_coefficient": "8",
        "relative_shortfall": float(1 - sp.Rational(16, 3) / 8),
    }

    reducible_representations = []

    def scan_representations(remaining_dimension, remaining_weight4, minimum_dimension, parts):
        if remaining_dimension == 0 and remaining_weight4 == 0:
            spins = [sp.Rational(dimension - 1, 2) for dimension in parts]
            reducible_representations.append(
                {
                    "irrep_dimensions": parts,
                    "spins": [str(spin) for spin in spins],
                    "all_half_integer": all(spin.q == 2 for spin in spins),
                    "center_action_minus_one_on_all_blocks": all(
                        spin.q == 2 for spin in spins
                    ),
                    "contains_singlets": 1 in parts,
                }
            )
            return
        if remaining_dimension <= 0 or remaining_weight4 < 0:
            return
        for dimension in range(minimum_dimension, remaining_dimension + 1):
            weight4 = dimension * (dimension * dimension - 1)
            if weight4 <= remaining_weight4:
                scan_representations(
                    remaining_dimension - dimension,
                    remaining_weight4 - weight4,
                    dimension,
                    parts + [dimension],
                )

    scan_representations(16, 192, 1, [])
    all_half_integer_representations = [
        row for row in reducible_representations if row["all_half_integer"]
    ]

    results = {
        "status": "canonical_reducible_SU2_boundary_rotor_candidate_matches_gap_coefficients_and_half_shift",
        "date": "2026-08-06",
        "target_functional": {
            "response": str(response),
            "potential": str(potential),
            "derivative_identity_residual": str(derivative_check),
            "target_cosine": str(target_cosine),
            "curvature_at_target": str(target_curvature),
            "curvature_numeric": float(sp.N(target_curvature, 16)),
        },
        "local_rotor_ansatz": {
            "description": (
                "N stable real boundary rotors with mass squared m^2(c)=1-c, "
                "a normalized channel trace 1/d, and fixed charge norm q^2."
            ),
            "one_loop_log_coefficient": "N/(2d)",
            "fixed_charge_inverse_coefficient": "N*q^2/(2d)",
            "signs": {
                "bosonic_log_determinant": "positive",
                "fixed_charge_Routhian": "positive",
                "ordinary_fixed_source_elimination": "negative and therefore unsuitable",
            },
        },
        "integer_scan": {
            "equations": ["N/(2d)=8/3", "N*q^2/(2d)=8"],
            "solutions_up_to_bounds": solutions,
            "minimal_solution": minimal_solution,
            "interpretation": (
                "The minimal arithmetic architecture is N=16, d=3, q^2=3. "
                "The numbers match dim End(R^4)=16 and the triplet trace rank d=3."
            ),
        },
        "gauge_representation_gate": {
            "required_charge_norm_squared": 3,
            "SU2_SO3_irrep_casimir_scan": su2_casimirs,
            "any_standard_irrep_has_casimir_three": any(
                row["equals_required_three"] for row in su2_casimirs
            ),
            "canonical_vector_prediction": canonical_vector_prediction,
            "dimension_16_reducible_representations_with_average_casimir_three": reducible_representations,
            "all_half_integer_solutions": all_half_integer_representations,
            "finding": (
                "No irreducible representation has Casimir three, but exactly three reducible "
                "dimension-16 representations have normalized average Casimir three. The unique "
                "solution with only half-integer spins is 2 V_(1/2) plus 3 V_(3/2). Its center "
                "acts as minus one on every block, so the same representation also supplies the "
                "required antiperiodic half-shift."
            ),
        },
        "tree_term_gate": {
            "required_linear_term": "-(44/45)c = -c + c/45",
            "candidate_reading": (
                "canonical unit Wilson stiffness plus the periodic zero-mode contribution 1/45"
            ),
            "derived_from_local_action": False,
        },
        "scientific_verdict": {
            "positive": (
                "A stable local fixed-charge rotor mechanism naturally gives the positive inverse "
                "resolvent sign that ordinary Gaussian source elimination could not provide. "
                "The exact coefficient pair has a unique minimal integer factorization 16/3 with "
                "average q^2=3. A canonical reducible SU(2) representation, "
                "2 V_(1/2) plus 3 V_(3/2), realizes dimension 16, average Casimir three and "
                "antiperiodic center action simultaneously."
            ),
            "negative": (
                "The multiplicities two and three, the coupling to the Wilson axis, the linear tree "
                "term and the full BV/BRST completion are not yet derived from the parent geometry. "
                "Therefore this is a sharply specified local candidate, not yet a completed theory."
            ),
            "next_gate": (
                "Construct the explicit boundary kinetic operator for "
                "2 V_(1/2) plus 3 V_(3/2), compute its determinant and fixed-charge Routhian on "
                "RP3 times S1, and test whether BV/BRST completion preserves the coefficient pair."
            ),
        },
    }

    Path("s2t_wilson_boundary_rotor_action_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "derivative_residual": str(derivative_check),
                "minimal_solution": minimal_solution,
                "canonical_inverse_coefficient": canonical_vector_prediction[
                    "inverse_coefficient"
                ],
                "casimir_three_exists": results["gauge_representation_gate"][
                    "any_standard_irrep_has_casimir_three"
                ],
                "reducible_dimension_16_solutions": reducible_representations,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()