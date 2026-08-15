#!/usr/bin/env python3
import json
import math
from pathlib import Path

import sympy as sp


def main():
    c = sp.symbols("c", real=True)
    theta = sp.acos(c)

    def laplacian_factor(charge):
        return sp.simplify(2 - 2 * sp.cos(charge * theta))

    lambda1 = laplacian_factor(1)
    lambda3 = laplacian_factor(3)
    target_log = sp.Rational(8, 3) * sp.log(lambda1)

    # For 2 V_(1/2) + 3 V_(3/2), after doubling the Cartan generator so that
    # fundamental weights have charges +/-1, the positive charge planes are:
    # q=1 with multiplicity 5 and q=3 with multiplicity 3.
    reducible_log = sp.Rational(1, 3) * (
        5 * sp.log(lambda1) + 3 * sp.log(lambda3)
    )
    reducible_difference = sp.simplify(sp.expand_log(reducible_log - target_log))
    ratio_lambda3_lambda1 = sp.simplify(sp.trigsimp(lambda3 / lambda1))

    target_cosine = (sp.Integer(26) - 9 * sp.sqrt(15)) / 11
    difference_at_target = sp.N(reducible_difference.subs(c, target_cosine), 16)
    derivative_at_target = sp.N(
        sp.diff(reducible_difference, c).subs(c, target_cosine), 16
    )

    # Four complex SU(2) doublets have real dimension 16. Restricted to the
    # Cartan circle they give eight real charge planes with |q|=1.
    fundamental_plane_count = 8
    fundamental_log = sp.Rational(fundamental_plane_count, 3) * sp.log(lambda1)
    fundamental_difference = sp.simplify(fundamental_log - target_log)

    required_charge_norm = sp.solve(
        sp.Eq(
            sp.Rational(fundamental_plane_count, 2 * 3) * sp.Symbol("q2"),
            8,
        ),
        sp.Symbol("q2"),
    )[0]
    axial_charge_norm = 1
    axial_inverse_coefficient = sp.Rational(fundamental_plane_count, 2 * 3)
    axial_shortfall_factor = sp.Rational(8, 1) / axial_inverse_coefficient

    results = {
        "status": "exact_weight_determinant_rejects_the_2Vhalf_plus_3Vthreehalf_completion_and_leaves_a_trace_charge_mismatch",
        "date": "2026-08-06",
        "circle_operator": {
            "operator": "-D_theta^2 on S1",
            "zeta_determinant_per_real_rotation_plane": "2-2*cos(q*theta)",
            "fundamental_factor": str(lambda1),
            "charge_three_factor": str(lambda3),
            "ratio_lambda3_over_lambda1": str(ratio_lambda3_lambda1),
        },
        "reducible_candidate": {
            "representation": "2 V_(1/2) plus 3 V_(3/2)",
            "positive_charge_plane_multiplicities": {"q=1": 5, "q=3": 3},
            "normalized_log_determinant": str(reducible_log),
            "target_log_term": str(target_log),
            "difference": str(reducible_difference),
            "difference_at_target": float(difference_at_target),
            "derivative_at_target": float(derivative_at_target),
            "exact_match": reducible_difference == 0,
            "verdict": (
                "The average Casimir matches only the quadratic expansion. The q=3 weights "
                "add the nonconstant term log(lambda_3/lambda_1), so the full determinant is wrong."
            ),
        },
        "fundamental_only_candidate": {
            "representation": "four complex SU2 doublets, real dimension 16",
            "real_charge_planes": fundamental_plane_count,
            "normalized_log_determinant": str(fundamental_log),
            "exact_log_match": fundamental_difference == 0,
            "fixed_charge_gate": {
                "required_mean_q_squared": str(required_charge_norm),
                "axial_q_squared": axial_charge_norm,
                "inverse_coefficient_with_axial_charge": str(
                    axial_inverse_coefficient
                ),
                "required_inverse_coefficient": "8",
                "axial_shortfall_factor": str(axial_shortfall_factor),
                "casimir_substitution_is_admissible": False,
                "reason": (
                    "The circle determinant and the fixed-charge Routhian use the "
                    "same Cartan generator. Replacing its axial charge q^2=1 by the "
                    "full SU2 Casimir C2=3 mixes inequivalent normalizations."
                ),
            },
            "verdict": (
                "The fundamental-only spectrum gives the exact logarithmic function, but with "
                "the same normalized trace its canonical fixed-charge term is too small."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The exact determinant audit identifies the unique simple weight pattern needed "
                "for the logarithm: eight equal unit-charge rotation planes."
            ),
            "negative": (
                "The previously proposed reducible representation fails beyond the Casimir "
                "approximation. Four fundamental doublets repair the determinant but require "
                "mean axial charge norm six for the inverse term, while the canonical axial "
                "norm is one. The full Casimir cannot replace this axial charge."
            ),
            "next_gate": (
                "Separate the unit holonomy weight that fixes the determinant from the conserved "
                "rotor momentum that fixes the Routhian, and test all quantized momentum sectors."
            ),
        },
    }

    Path("s2t_wilson_rotor_exact_determinant_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "reducible_exact_match": results["reducible_candidate"][
                    "exact_match"
                ],
                "reducible_difference_at_target": float(difference_at_target),
                "fundamental_exact_log_match": results[
                    "fundamental_only_candidate"
                ]["exact_log_match"],
                "required_mean_q_squared": str(required_charge_norm),
                "canonical_axial_inverse_coefficient": str(axial_inverse_coefficient),
                "axial_shortfall_factor": str(axial_shortfall_factor),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()