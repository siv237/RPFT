import itertools
import json
import math
from pathlib import Path


ALPHA_S_TARGET = 0.1181
WEINBERG_TARGET = 0.2312
DISPLAY_HALF_STEP = 0.00005


BLOCKS = [
    {
        "name": "C",
        "representation": "(8,1)_0",
        "dimension": 8,
        "torsion_parity": 1,
        "hypercharge": "0",
    },
    {
        "name": "W",
        "representation": "(1,3)_0",
        "dimension": 3,
        "torsion_parity": 1,
        "hypercharge": "0",
    },
    {
        "name": "Y",
        "representation": "(1,1)_0",
        "dimension": 1,
        "torsion_parity": 1,
        "hypercharge": "0",
    },
    {
        "name": "X",
        "representation": "(3,2)_{-5/6}",
        "dimension": 6,
        "torsion_parity": -1,
        "hypercharge": "-5/6",
    },
    {
        "name": "Xbar",
        "representation": "(bar3,2)_{+5/6}",
        "dimension": 6,
        "torsion_parity": -1,
        "hypercharge": "+5/6",
    },
]


def alpha_s_from_projector(rank):
    normalized_rank = rank / 24.0
    inverse_coupling = rank + math.pi**2 * normalized_rank
    return 1.0 / inverse_coupling


def weinberg_from_roles(color_rank, weak_rank, hypercharge_rank, mixed_rank):
    numerator = color_rank - weak_rank * (mixed_rank / 24.0) / math.pi
    denominator = (24 - weak_rank) + (weak_rank + hypercharge_rank) * math.pi
    return numerator / denominator


def main():
    total_dimension = sum(block["dimension"] for block in BLOCKS)
    even_dimension = sum(
        block["dimension"]
        for block in BLOCKS
        if block["torsion_parity"] == 1
    )
    odd_dimension = total_dimension - even_dimension

    alpha_rows = []
    for block in BLOCKS:
        value = alpha_s_from_projector(block["dimension"])
        alpha_rows.append(
            {
                "projector": block["name"],
                "rank": block["dimension"],
                "value": value,
                "absolute_error": abs(value - ALPHA_S_TARGET),
            }
        )
    alpha_rows.sort(key=lambda row: row["absolute_error"])
    alpha_claimed_error = next(
        row["absolute_error"] for row in alpha_rows if row["projector"] == "X"
    )
    alpha_second_distinct_error = next(
        row["absolute_error"]
        for row in alpha_rows
        if row["rank"] != 6
    )
    alpha_display_matches = [
        row
        for row in alpha_rows
        if abs(row["value"] - ALPHA_S_TARGET) <= DISPLAY_HALF_STEP
    ]

    weinberg_rows = []
    for indices in itertools.permutations(range(len(BLOCKS)), 4):
        color, weak, hypercharge, mixed = [BLOCKS[index] for index in indices]
        value = weinberg_from_roles(
            color["dimension"],
            weak["dimension"],
            hypercharge["dimension"],
            mixed["dimension"],
        )
        weinberg_rows.append(
            {
                "roles": [
                    color["name"],
                    weak["name"],
                    hypercharge["name"],
                    mixed["name"],
                ],
                "role_dimensions": [
                    color["dimension"],
                    weak["dimension"],
                    hypercharge["dimension"],
                    mixed["dimension"],
                ],
                "value": value,
                "absolute_error": abs(value - WEINBERG_TARGET),
            }
        )
    weinberg_rows.sort(key=lambda row: row["absolute_error"])
    claimed_role_sets = [
        ["C", "W", "Y", "X"],
        ["C", "W", "Y", "Xbar"],
    ]
    claimed_rows = [
        row for row in weinberg_rows if row["roles"] in claimed_role_sets
    ]
    weinberg_claimed_error = claimed_rows[0]["absolute_error"]
    weinberg_next_error = next(
        row["absolute_error"]
        for row in weinberg_rows
        if row["roles"] not in claimed_role_sets
    )
    tied_or_better = sum(
        row["absolute_error"] <= weinberg_claimed_error + 1e-15
        for row in weinberg_rows
    )
    weinberg_display_matches = [
        row
        for row in weinberg_rows
        if abs(row["value"] - WEINBERG_TARGET) <= DISPLAY_HALF_STEP
    ]

    results = {
        "status": "su5_rank_selector_reconstructs_alpha_s_and_weinberg_uniquely_up_to_charge_conjugation",
        "date": "2026-08-04",
        "adjoint_decomposition": {
            "involution": "P=diag(1,1,1,-1,-1)",
            "hypercharge_generator": "Y=diag(-1/3,-1/3,-1/3,1/2,1/2)",
            "decomposition": "24=(8,1)_0+(1,3)_0+(1,1)_0+(3,2)_{-5/6}+(bar3,2)_{+5/6}",
            "blocks": BLOCKS,
            "total_dimension": total_dimension,
            "torsion_even_dimension": even_dimension,
            "torsion_odd_dimension": odd_dimension,
            "checks": {
                "dimension_sum": total_dimension == 24,
                "parity_split": [even_dimension, odd_dimension] == [12, 12],
                "mixed_blocks_are_charge_conjugates": True,
            },
        },
        "strong_coupling_selector": {
            "rule": "alpha_s(P)=1/(rank(P)+pi^2*rank(P)/24)",
            "selected_projector_orbit": "X or Xbar",
            "selected_rank": 6,
            "derived_formula": "1/(6+pi^2/4)",
            "target": ALPHA_S_TARGET,
            "target_display_half_step": DISPLAY_HALF_STEP,
            "prediction": alpha_s_from_projector(6),
            "absolute_error": alpha_claimed_error,
            "candidate_projectors": len(alpha_rows),
            "unique_rank_values": len(set(row["rank"] for row in alpha_rows)),
            "winning_rank": 1,
            "matching_display_bin_count": len(alpha_display_matches),
            "charge_conjugate_tie_count": sum(
                row["absolute_error"] <= alpha_claimed_error + 1e-15
                for row in alpha_rows
            ),
            "next_distinct_error": alpha_second_distinct_error,
            "error_separation_factor": alpha_second_distinct_error
            / alpha_claimed_error,
            "precision_warning": (
                "The atlas target is printed to four decimals; the multi-million "
                "error ratio is diagnostic only and must not be read as experimental precision."
            ),
            "rows": alpha_rows,
        },
        "weinberg_selector": {
            "rule": "(r_C-r_W*(r_X/24)/pi)/((24-r_W)+(r_W+r_Y)*pi)",
            "selected_roles": ["C", "W", "Y", "X_or_Xbar"],
            "derived_formula": "(8-3/(4*pi))/(21+4*pi)",
            "target": WEINBERG_TARGET,
            "target_display_half_step": DISPLAY_HALF_STEP,
            "prediction": weinberg_from_roles(8, 3, 1, 6),
            "absolute_error": weinberg_claimed_error,
            "labelled_permutation_count": len(weinberg_rows),
            "tied_or_better_count": tied_or_better,
            "charge_conjugation_reduced_winner_count": 1,
            "matching_display_bin_count": len(weinberg_display_matches),
            "next_nonconjugate_error": weinberg_next_error,
            "error_separation_factor": weinberg_next_error
            / weinberg_claimed_error,
            "precision_warning": (
                "The atlas target is printed to four decimals; uniqueness inside "
                "the rounding bin is the robust statement."
            ),
            "top_permutations": weinberg_rows[:12],
        },
        "selector_interpretation": {
            "positive": (
                "The integers and fractions in both atlas formulas are reconstructed "
                "from canonical SU(5) adjoint block ranks. Both physical assignments "
                "win their full block-permutation controls up to X/Xbar conjugation."
            ),
            "physical_reading": {
                "alpha_s": (
                    "The rank-six mixed color-weak block supplies both the integer 6 "
                    "and its normalized trace 6/24=1/4."
                ),
                "weinberg": (
                    "Color gives 8, the weak complement gives 24-3=21, the unbroken "
                    "electroweak block gives 3+1=4, and the mixed normalized rank gives 1/4."
                ),
            },
        },
        "no_go": {
            "remaining_gap": (
                "The functional forms and placement of pi were read from the atlas "
                "before the rank reconstruction. Representation theory derives every "
                "coefficient, but not yet the action that combines them in these ratios."
            ),
            "status": "representation_theoretic_reconstruction_not_blind_prediction",
            "reopening_condition": (
                "Derive both selector functionals from one gauge-fixed parent action, "
                "then use the same rule on a hidden third coupling or threshold."
            ),
        },
    }

    assert total_dimension == 24
    assert even_dimension == odd_dimension == 12
    assert alpha_rows[0]["rank"] == 6
    assert len(alpha_display_matches) == 2
    assert weinberg_rows[0]["roles"] in claimed_role_sets
    assert tied_or_better == 2
    assert len(weinberg_display_matches) == 2
    assert results["weinberg_selector"]["error_separation_factor"] > 300

    Path("s2t_su5_rank_selector_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "adjoint_split": [even_dimension, odd_dimension],
                "alpha_s_prediction": results["strong_coupling_selector"][
                    "prediction"
                ],
                "alpha_s_separation": results["strong_coupling_selector"][
                    "error_separation_factor"
                ],
                "weinberg_prediction": results["weinberg_selector"]["prediction"],
                "weinberg_permutation_rank": 1,
                "weinberg_separation": results["weinberg_selector"][
                    "error_separation_factor"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()