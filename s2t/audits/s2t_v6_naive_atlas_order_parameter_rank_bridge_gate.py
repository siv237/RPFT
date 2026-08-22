#!/usr/bin/env python3
"""Retrospective audit of the naive SM atlas against Tome VI order data.

The script checks exact rational identities only.  It records, but does not
promote, the resulting bridge to a physical selector.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_naive_atlas_order_parameter_rank_bridge_gate_results.json"


def main() -> None:
    pi = math.pi
    blocks = {"C": 8, "W": 3, "Y": 1, "X": 6, "Xbar": 6}
    total = 24

    r_crit = (Fraction(2, 3), Fraction(1, 6), Fraction(1, 6))
    q_crit = tuple(x - Fraction(1, 3) for x in r_crit)
    gap = r_crit[0] - r_crit[1]
    qhat = tuple(x / gap for x in q_crit)

    color_matches = [name for name, rank in blocks.items() if Fraction(total - rank, total) == qhat[0]]
    ew_pair_matches = [
        pair
        for pair in itertools.permutations(blocks, 2)
        if Fraction(blocks[pair[0]] + blocks[pair[1]], total) == r_crit[1]
    ]
    mixed_matches = [name for name, rank in blocks.items() if Fraction(rank, total) == gap * gap]

    q_plus = qhat[0]
    q_minus = qhat[1]
    delta = gap
    delta2 = gap * gap

    original = {
        "alpha_s": 1.0 / (6.0 + pi**2 / 4.0),
        "weinberg": (8.0 - 3.0 / (4.0 * pi)) / (21.0 + 4.0 * pi),
        "bottom_over_proton": pi + 4.0 / 3.0,
        "strange_inverse_denominator": pi**2 + 1.0 / 3.0,
        "tau_over_muon_core": pi**2 + 2.0 * pi + 2.0 / 3.0,
        "omega_dark_matter": 1.0 / pi - 1.0 / (2.0 * pi**2),
        "omega_baryon": 1.0 / (2.0 * pi**2),
    }
    rewritten = {
        "alpha_s": 1.0 / (blocks["X"] + pi**2 * float(delta2)),
        "weinberg": (
            blocks["C"] - blocks["W"] * float(delta2) / pi
        ) / ((total - blocks["W"]) + (blocks["W"] + blocks["Y"]) * pi),
        "bottom_over_proton": pi + 1.0 - float(q_minus),
        "strange_inverse_denominator": pi**2 - float(q_minus),
        "tau_over_muon_core": (pi + 1.0) ** 2 + float(q_minus),
        "omega_dark_matter": 1.0 / pi - float(delta) / pi**2,
        "omega_baryon": float(delta) / pi**2,
    }
    residuals = {name: abs(original[name] - rewritten[name]) for name in original}

    dynamic_spectrum = (0.9121666003123439, 0.043916699843828066, 0.043916699843828066)
    dynamic_gap = dynamic_spectrum[0] - dynamic_spectrum[1]

    result = {
        "gate": "version6_naive_atlas_order_parameter_rank_bridge_gate",
        "source_scope": {
            "atlas": "архив-2025-2026/2026-02-проработка/Проработка/atlas.md",
            "short_formula_ledger": "s2t/results/s2t_pi_spectral_address_operator_results.json",
            "prior_SU5_rank_ledger": "s2t/results/s2t_su5_rank_selector_results.json",
            "new_data": "exact control RP2 coexistence spectrum from Tome VI",
            "retrospective_not_blind": True,
        },
        "critical_order_parameter": {
            "R_spectrum": [str(x) for x in r_crit],
            "Q_spectrum": [str(x) for x in q_crit],
            "gap": str(gap),
            "normalized_Q_spectrum": [str(x) for x in qhat],
        },
        "rank24_bridge": {
            "SU5_adjoint_blocks": blocks,
            "normalized_Q_identity": "(2/3,-1/3,-1/3)=((24-8)/24,-8/24,-8/24)",
            "R_identity": "(2/3,1/6,1/6)=(16,4,4)/24 with 16=24-8 and 4=3+1",
            "gap_identity": "1/2=12/24",
            "gap_square_identity": "(1/2)^2=1/4=6/24",
            "integer_square_identity": "12^2=24*6",
            "color_role_matches": color_matches,
            "electroweak_rank4_labelled_pair_matches": [list(x) for x in ew_pair_matches],
            "mixed_rank6_matches": mixed_matches,
            "unique_up_to_WY_order_and_XXbar_conjugation": (
                color_matches == ["C"]
                and set(ew_pair_matches) == {("W", "Y"), ("Y", "W")}
                and set(mixed_matches) == {"X", "Xbar"}
            ),
            "literal_disjoint_24_partition": False,
            "reason": "the rank-4 electroweak block is used twice in (16,4,4); this is a spectral identity, not a direct-sum decomposition",
        },
        "atlas_fraction_dictionary": {
            "1/3": "-q_minus = 8/24",
            "2/3": "q_plus = 16/24",
            "4/3": "1-q_minus",
            "3/2": "1/q_plus",
            "1/2": "Delta_crit = 12/24",
            "1/4": "Delta_crit^2 = 6/24",
            "interpretation": "several formerly inserted small fractions are eigenvalues or gap powers of the exact control order parameter",
        },
        "formula_rewrites": {
            "count": len(original),
            "atlas_short_formula_count": 11,
            "rows": {
                name: {
                    "original_value": original[name],
                    "rewritten_value": rewritten[name],
                    "absolute_residual": residuals[name],
                }
                for name in original
            },
            "maximum_residual": max(residuals.values()),
            "muon_leading_fraction": "3/2=1/q_plus",
            "tau_alpha_extension": "2 alpha/3 = alpha q_plus",
        },
        "dynamic_background_control": {
            "current_canonical_coexistence_spectrum": list(dynamic_spectrum),
            "current_gap": dynamic_gap,
            "current_gap_squared": dynamic_gap**2,
            "maximum_spectrum_difference_from_exact_control": max(
                abs(dynamic_spectrum[i] - float(r_crit[i])) for i in range(3)
            ),
            "exact_rank_bridge_applies_to_current_dynamic_minimum": False,
            "status": "exact for the kappa=log4 control transition, not for the later beta_c canonical phase",
        },
        "new_hypothesis": {
            "spectral_address_upgrade": "replace free rational coefficient slots by functions of Pi and the order-parameter operators R_crit or Q_crit/Delta",
            "two_copy_clue": "the atlas coefficient 1/4 is simultaneously Delta_crit^2 and rank(X)/24, so a tensor-square gap may be the missing bridge to the mixed rank-six sector",
            "multiplicity_clue": "(16,4,4)/24 repeats the electroweak rank-four block; the repetition must be derived by the two-copy carrier before it can be physical",
            "H16_coincidence": "the numerator 16 also equals the one-generation H16 dimension, but this is not unique evidence and is not promoted",
        },
        "verdict": {
            "new_exact_cross_tome_identity_found": True,
            "prior_atlas_numerology_fully_explained": False,
            "observable_address_selector_derived": False,
            "physical_SU5_parent_derived": False,
            "useful_for_next_two_copy_spin_cover_test": True,
            "status": "exact_retrospective_rank_spectral_clue_not_physical_derivation",
            "next_gate": "version6_two_copy_spin_cover_multiplicity_gate",
        },
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()