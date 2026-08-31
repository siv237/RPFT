#!/usr/bin/env python3
"""Exact independent audit of external canonical weights and the G_eta no-go."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_canonical_weights_geta_no_go_gate_results.json"
REFERENCE = ROOT / "s2t/results/s2t_v8_canonical_noise_frame_common_trace_gate_results.json"


def exact_string(expr: sp.Expr) -> str:
    return str(sp.factor(sp.cancel(expr)))


def main() -> None:
    x, eta = sp.symbols("x eta", positive=True)
    a = 1 / (11 + 10 * x)
    b = x / (11 + 10 * x)
    ab = sp.simplify(a + b)

    weights_from_trace = {
        "linking": 1 / (13 * ab),
        "SU3": 1 / ab,
        "SU2": 1 / ((5 * a + b) / 2),
        "U1": 1 / ((13 * a + 25 * b) / 6),
        "QLYR": 1 / (2 * ab),
        "XLdR": 1 / (2 * ab),
    }
    claimed_weights = {
        "linking": (10 * x + 11) / (13 * (x + 1)),
        "SU3": (10 * x + 11) / (x + 1),
        "SU2": (20 * x + 22) / (x + 5),
        "U1": (60 * x + 66) / (25 * x + 13),
        "QLYR": (10 * x + 11) / (2 * (x + 1)),
        "XLdR": (10 * x + 11) / (2 * (x + 1)),
    }
    weight_identities = {
        name: sp.simplify(weights_from_trace[name] - claimed_weights[name]) == 0
        for name in claimed_weights
    }

    with REFERENCE.open(encoding="utf-8") as handle:
        reference = json.load(handle)
    printed = reference["relation_to_old_six_family_diagonal_cone"][
        "least_squares_diagonal_weights"
    ]
    order = ["linking", "SU3", "SU2", "U1", "QLYR", "XLdR"]
    evaluated = [float(sp.N(claimed_weights[name].subs(x, sp.exp(-2)), 17)) for name in order]
    display_errors = [abs(left - right) for left, right in zip(evaluated, printed)]

    target = sp.Rational(977, 3490)
    numerator = 104 * (25 * x**2 + 38 * x + 13)
    d_transfer = 425 * x**3 + 2346 * x**2 + 1105 * x
    d_gauge = 3692 * x**2 + 12584 * x + 5564
    value_eta = sp.factor(numerator / (eta * d_transfer + d_gauge))
    derivative_eta = sp.factor(sp.diff(value_eta, eta))
    eta_star = sp.factor(sp.solve(sp.Eq(value_eta, target), eta)[0])
    supremum = sp.factor(numerator / d_gauge)
    target_minus_supremum = sp.factor(target - supremum)

    sign_polynomial = 105133 * x**2 + 28806 * x - 13799
    sign_derivative = sp.diff(sign_polynomial, x)
    sign_at_one_seventh = sp.factor(sign_polynomial.subs(x, sp.Rational(1, 7)))

    # Exact elementary certificate: e^2 exceeds the partial exponential sum
    # through n=4, which equals 7, so exp(-2)<1/7.  The sign polynomial is
    # strictly increasing for x>0 and is still negative at 1/7.
    exp2_partial_sum = sum(sp.Rational(2) ** n / sp.factorial(n) for n in range(5))
    exp_minus_two_below_one_seventh = bool(
        exp2_partial_sum == 7 and sign_at_one_seventh < 0
    )
    sign_polynomial_negative_at_exp_minus_two = bool(
        exp_minus_two_below_one_seventh and sign_derivative.is_positive
    )

    base_value = sp.factor(value_eta.subs(eta, 1))
    external_residual = sp.factor(1 - base_value / target)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_canonical_weights_geta_no_go_gate",
        "field": "Q(x), x=exp(-2)",
        "canonical_weights": {
            name: {
                "exact": exact_string(claimed_weights[name]),
                "trace_identity_exact": weight_identities[name],
                "display_at_exp_minus_2": format(evaluated[index], ".15g"),
                "reference_display": format(printed[index], ".15g"),
                "absolute_display_error": format(display_errors[index], ".3e"),
            }
            for index, name in enumerate(order)
        },
        "normalization": {
            "a": "1/(11+10*x)",
            "b": "x/(11+10*x)",
            "11a_plus_10b_exact": sp.simplify(11 * a + 10 * b) == 1,
            "b_over_a_exact": sp.simplify(b / a - x) == 0,
            "maximum_reference_display_error": format(max(display_errors), ".3e"),
        },
        "G_eta_slice": {
            "value": exact_string(value_eta),
            "derivative": exact_string(derivative_eta),
            "strictly_decreasing_for_x_eta_positive": True,
            "target_external": "977/3490",
            "eta_star": exact_string(eta_star),
            "supremum_eta_positive": exact_string(supremum),
            "target_minus_supremum": exact_string(target_minus_supremum),
            "sign_polynomial": exact_string(sign_polynomial),
            "sign_polynomial_derivative": exact_string(sign_derivative),
            "exp2_partial_sum_n0_to_n4": exact_string(exp2_partial_sum),
            "exp_minus_2_less_than_one_seventh_exact": exp_minus_two_below_one_seventh,
            "sign_at_one_seventh": exact_string(sign_at_one_seventh),
            "sign_negative_at_exp_minus_2_exact": sign_polynomial_negative_at_exp_minus_two,
            "eta_star_negative_at_exp_minus_2_exact": sign_polynomial_negative_at_exp_minus_two,
            "target_above_entire_positive_slice_exact": sign_polynomial_negative_at_exp_minus_two,
            "base_value": exact_string(base_value),
            "base_display": format(float(sp.N(base_value.subs(x, sp.exp(-2)), 17)), ".15g"),
            "supremum_display": format(float(sp.N(supremum.subs(x, sp.exp(-2)), 17)), ".15g"),
            "eta_star_display": format(float(sp.N(eta_star.subs(x, sp.exp(-2)), 17)), ".15g"),
            "external_relative_residual_display": format(
                float(sp.N(external_residual.subs(x, sp.exp(-2)), 17)), ".15g"
            ),
        },
        "status_boundary": {
            "weights_canonical_on_stabilizer_branch": True,
            "G_eta_no_go_exact_inside_baryon_mapping": True,
            "baryon_discriminator_unique_from_tome8_alone": False,
            "directed_transfer_convention_resolved": False,
            "target_is_internal_prediction": False,
            "physical_baryon_mass_theorem": False,
        },
        "verdict": {
            "accept_exact_weight_provenance": True,
            "accept_conditional_G_eta_no_go": True,
            "reject_canonical_8_21_percent_as_unconditional": True,
            "next_gate": "version8_baryon_directed_transfer_convention_selector_gate",
        },
    }

    assert all(weight_identities.values())
    assert sp.simplify(11 * a + 10 * b) == 1
    assert sp.simplify(b / a) == x
    assert max(display_errors) < 1e-12
    assert derivative_eta.is_negative
    assert sign_polynomial_negative_at_exp_minus_two
    assert sign_at_one_seventh == -sp.Rational(52768, 7)

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()