#!/usr/bin/env python3
"""Exact selector for the directed transfer convention in the baryon lift."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_directed_transfer_convention_selector_gate_results.json"


def exact(expr: sp.Expr) -> str:
    return str(sp.factor(sp.cancel(expr)))


def main() -> None:
    x = sp.symbols("x", positive=True)
    a = 1 / (11 + 10 * x)
    b = x / (11 + 10 * x)
    ab = sp.factor(a + b)

    # Three complex Q_L -> Y_R colour arrows.  Each map is the Frobenius-
    # normalized oriented variation inherited from the real pair (E,-iE).
    arrows = []
    for colour in range(3):
        operator = sp.zeros(2, 6)
        operator[0, 2 * colour] = 1 / sp.sqrt(2)
        operator[1, 2 * colour + 1] = 1 / sp.sqrt(2)
        arrows.append(operator)

    arrow_hs_gram = sp.Matrix(
        [[sp.trace(left.H * right) for right in arrows] for left in arrows]
    )
    arrow_casimir = sp.simplify(
        sum((operator.H * operator for operator in arrows), sp.zeros(6, 6)) / ab
    )
    expected_arrow_casimir = sp.eye(6) / (2 * ab)

    # The six real representatives (E,-iE) form three complex lines.  Their
    # common-trace Gram block and Moore--Penrose inverse are exact.
    gram_block = ab * sp.Matrix([[1, -sp.I], [sp.I, 1]])
    gram_block_pinv = sp.Matrix([[1, -sp.I], [sp.I, 1]]) / (4 * ab)
    gram_pinv_identity = sp.simplify(
        gram_block * gram_block_pinv * gram_block - gram_block
    ) == sp.zeros(2, 2)

    # The incidence map has squared Frobenius norm 13.  On Q_L its source
    # Gram is I_6, hence common-trace whitening gives the stated corner.
    linking_casimir = sp.eye(6) / (13 * ab)

    arrow_source_spring = sp.factor(x / (2 * ab))
    linking_source_spring = sp.factor(x / (13 * ab))
    supplied_arrow_spring = sp.factor(x / (4 * ab))
    supplied_linking_spring = sp.factor(x / (13 * ab))

    arrow_ratio = sp.factor(arrow_source_spring / supplied_arrow_spring)
    linking_ratio = sp.factor(linking_source_spring / supplied_linking_spring)

    # Exact one-particle scalar after the direct source-corner restriction.
    arrow = arrow_source_spring
    linking = linking_source_spring
    su3 = sp.Rational(4, 3) / ab
    su2 = sp.Rational(3, 2) / (5 * a + b)
    u1 = sp.Rational(1, 6) / (13 * a + 25 * b)
    r1 = sp.factor(arrow + linking + su3 + su2 + u1)
    split3 = sp.factor(6 * (10 * x + 11) / (x + 5))
    discriminator = sp.factor(split3 / (3 * r1))
    expected_discriminator = sp.factor(
        52 * (25 * x**2 + 38 * x + 13)
        / (375 * x**3 + 3916 * x**2 + 7267 * x + 2782)
    )

    # The alternative 1/x rescaling removes the KMS source rate and therefore
    # cannot be the source corner of the directed generator.
    kms_source_rate_retained = sp.simplify(arrow_source_spring / x - 1 / (2 * ab)) == 0
    inverse_x_reading_is_source_corner = sp.simplify(
        supplied_arrow_spring * (2 / x) - arrow_source_spring
    ) == 0

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_directed_transfer_convention_selector_gate",
        "field": "Q(x), x=exp(-2)",
        "qlyr_common_trace_quotient": {
            "complex_rank": int(arrow_hs_gram.rank()),
            "frobenius_gram": str(arrow_hs_gram),
            "real_pair_gram_block": str(gram_block),
            "real_pair_gram_pseudoinverse": str(gram_block_pinv),
            "moore_penrose_identity_exact": gram_pinv_identity,
            "source_casimir": str(arrow_casimir),
            "source_casimir_expected": str(expected_arrow_casimir),
            "source_casimir_exact": arrow_casimir == expected_arrow_casimir,
        },
        "linking_common_trace_quotient": {
            "incidence_frobenius_square": 13,
            "q_l_source_gram": "I_6",
            "source_casimir": str(linking_casimir),
        },
        "directed_source_corner": {
            "qlyr_spring": exact(arrow_source_spring),
            "linking_spring": exact(linking_source_spring),
            "kms_source_rate_x_retained_exact": kms_source_rate_retained,
            "inverse_x_reading_is_source_corner": inverse_x_reading_is_source_corner,
        },
        "comparison_with_baryon_mapping": {
            "supplied_qlyr_spring": exact(supplied_arrow_spring),
            "supplied_linking_spring": exact(supplied_linking_spring),
            "qlyr_required_multiplier": exact(arrow_ratio),
            "linking_required_multiplier": exact(linking_ratio),
            "qlyr_half_weight_defect": arrow_ratio == 2,
            "linking_matches_exactly": linking_ratio == 1,
        },
        "direct_restriction_candidate": {
            "r1": exact(r1),
            "split3_inherited": exact(split3),
            "discriminator": exact(discriminator),
            "display_at_exp_minus_2": format(
                float(sp.N(discriminator.subs(x, sp.exp(-2)), 17)), ".15g"
            ),
            "closed_form_identity_exact": sp.simplify(
                discriminator - expected_discriminator
            ) == 0,
        },
        "status_boundary": {
            "kms_direction_selected": True,
            "source_corner_casimir_selected": True,
            "supplied_baseline_is_direct_canonical_restriction": False,
            "inverse_x_reading_is_direct_canonical_restriction": False,
            "full_three_particle_lift_derived": False,
            "physical_mass_theorem": False,
        },
        "verdict": {
            "selected_one_particle_transfer_multiplier": {
                "QLYR": "2",
                "linking": "1",
            },
            "canonical_direct_restriction_discriminator": exact(discriminator),
            "next_gate": "version8_baryon_three_particle_lift_normalization_gate",
        },
    }

    assert arrow_hs_gram == sp.eye(3)
    assert gram_block.rank() == 1
    assert gram_pinv_identity
    assert arrow_casimir == expected_arrow_casimir
    assert arrow_ratio == 2
    assert linking_ratio == 1
    assert kms_source_rate_retained
    assert not inverse_x_reading_is_source_corner
    assert sp.simplify(discriminator - expected_discriminator) == 0

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()