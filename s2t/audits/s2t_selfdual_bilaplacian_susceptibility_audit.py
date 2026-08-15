#!/usr/bin/env python3
import json
import math
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80


def main():
    pi = mp.pi
    zeta2_half = mp.zeta(2, mp.mpf("0.5"))
    zeta4_half = mp.zeta(4, mp.mpf("0.5"))
    full_second_order_sum = 2 * zeta2_half
    full_fourth_order_sum = 2 * zeta4_half
    selfdual_rank = 3
    second_order_total = selfdual_rank * full_second_order_sum
    fourth_order_total = selfdual_rank * full_fourth_order_sum
    target = 1 / pi**4

    cutoffs = [2, 5, 10, 25, 100, 500]
    convergence = []
    for cutoff in cutoffs:
        partial = mp.fsum(
            1 / (mp.mpf(n) + mp.mpf("0.5")) ** 4
            for n in range(-cutoff, cutoff + 1)
        )
        total = selfdual_rank * partial
        convergence.append(
            {
                "cutoff": cutoff,
                "three_channel_partial_sum": float(total),
                "absolute_error_vs_pi4": float(abs(total - pi**4)),
            }
        )

    results = {
        "status": "selfdual_rank_three_full_half_integer_bilaplacian_has_exact_pi4_susceptibility_but_requires_new_twisted_fourth_order_sector",
        "date": "2026-08-05",
        "geometric_count": {
            "four_dimensional_two_form_rank": math.comb(4, 2),
            "Hodge_split": "Lambda2=Lambda2_plus direct_sum Lambda2_minus",
            "selfdual_rank": selfdual_rank,
            "interpretation": (
                "On an oriented Euclidean four-manifold the Hodge star canonically splits "
                "two-forms into two rank-three bundles."
            ),
        },
        "full_half_integer_tower": {
            "one_sided_zeta4_half": float(zeta4_half),
            "full_Z_sum": float(full_fourth_order_sum),
            "identity": "sum_{n in Z}(n+1/2)^-4=2 zeta(4,1/2)=pi^4/3",
            "three_selfdual_channels": float(fourth_order_total),
            "target_pi4": float(pi**4),
            "absolute_error": float(abs(fourth_order_total - pi**4)),
            "inverse": float(1 / fourth_order_total),
            "target_inverse_pi4": float(target),
            "convergence": convergence,
        },
        "kinetic_order_gate": {
            "second_order_full_sum_per_channel": float(full_second_order_sum),
            "three_channel_second_order_total": float(second_order_total),
            "second_order_closed_form": "3 pi^2",
            "fourth_order_operator": "K=(-partial_S1^2)^2 on an antiperiodic real line bundle",
            "fourth_order_covariance_trace": "Tr K^-1=pi^4 for three selfdual components",
            "finding": (
                "The exact pi^4 requires a bi-Laplacian/fourth-order kinetic operator. "
                "An ordinary second-order Maxwell or scalar Hessian gives 3 pi^2 instead."
            ),
        },
        "trace_normalization_gate": {
            "ordinary_component_trace": float(fourth_order_total),
            "normalized_rank_three_trace": float(fourth_order_total / selfdual_rank),
            "inverse_ordinary_trace": float(1 / fourth_order_total),
            "inverse_normalized_trace": float(
                selfdual_rank / fourth_order_total
            ),
            "normalized_to_target_ratio": float(selfdual_rank),
            "finding": (
                "The exact coefficient uses the ordinary trace over the rank-three bundle. "
                "A normalized trace gives 3/pi^4 after inversion."
            ),
        },
        "boundary_condition_gate": {
            "required": "B_plus(theta+2pi)=-B_plus(theta)",
            "mathematical_realization": "sections of a nontrivial real Z2 line bundle over S1",
            "current_EM_condition": "periodic Maxwell and Faddeev-Popov sectors",
            "finding": (
                "The antiperiodic bosonic twist is mathematically consistent but is not part "
                "of the frozen II.A electromagnetic field content."
            ),
        },
        "gauge_and_reality_gate": {
            "selfdual_choice": (
                "Selecting Lambda2_plus rather than both chiralities is an orientation-dependent "
                "chiral choice. Ordinary real Maxwell contains both electric/magnetic sectors "
                "and is constrained by F=dA and dF=0."
            ),
            "auxiliary_interpretation": (
                "The clean realization is a new selfdual auxiliary two-form sector, not a recounting "
                "of the existing Maxwell coexact determinant."
            ),
        },
        "inverse_response_gate": {
            "susceptibility": "chi=Tr K^-1=pi^4",
            "desired_readout": "Delta S=-chi^-1/S_geo^2",
            "open_map": (
                "The parent action must explain why the physical correction uses the inverse "
                "of the integrated susceptibility and why its quadratic readout has unit coefficient."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The factor six now has a canonical geometric decomposition: rank three selfdual "
                "two-forms times the two-sided half-integer spectrum. No arbitrary multiplicity is needed."
            ),
            "negative": (
                "The construction requires three ingredients absent from II.A: a chiral selfdual "
                "auxiliary sector, antiperiodic bosonic holonomy, and a fourth-order kinetic operator."
            ),
            "status": "precise_new_II_B_parent_action_candidate",
            "next_gate": (
                "Construct the minimal local quadratic action for a twisted selfdual two-form, "
                "derive its determinant/constraint tower, and test whether integrating it out "
                "produces -chi^-1/S_geo^2 without an adjustable source coefficient."
            ),
        },
    }

    assert math.comb(4, 2) == 6
    assert abs(full_second_order_sum - pi**2) < mp.mpf("1e-70")
    assert abs(full_fourth_order_sum - pi**4 / 3) < mp.mpf("1e-70")
    assert abs(fourth_order_total - pi**4) < mp.mpf("1e-70")
    assert abs(1 / fourth_order_total - target) < mp.mpf("1e-70")

    Path("s2t_selfdual_bilaplacian_susceptibility_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "selfdual_rank": selfdual_rank,
                "full_half_integer_sum_per_channel": float(
                    full_fourth_order_sum
                ),
                "three_channel_susceptibility": float(fourth_order_total),
                "inverse_susceptibility": float(1 / fourth_order_total),
                "second_order_control": float(second_order_total),
                "new_structures_required": [
                    "selfdual auxiliary two-form",
                    "bosonic antiperiodic Z2 twist",
                    "fourth-order kinetic operator",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()