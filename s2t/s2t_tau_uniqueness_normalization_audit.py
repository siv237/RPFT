import json
import math
from fractions import Fraction
from pathlib import Path

import scipy.integrate as integrate
import scipy.special as special


ALPHA_INVERSE = 137.035999177
M_MU_MEV = 105.6583755


def simple_rationals(max_numerator, max_denominator):
    values = set()
    for denominator in range(1, max_denominator + 1):
        for numerator in range(-max_numerator, max_numerator + 1):
            values.add(Fraction(numerator, denominator))
    return sorted(values)


def formula_complexity(pi_coefficient, rational, alpha_coefficient):
    return (
        1
        + abs(pi_coefficient)
        + abs(rational.numerator)
        + rational.denominator
        + abs(alpha_coefficient.numerator)
        + alpha_coefficient.denominator
    )


def compact_bessel_sum():
    # Infinite-domain pieces are exact:
    # integral_0^infinity K0(2 pi q x) dx = 1/(4q),
    # integral_0^infinity x K0(2 pi q x) dx = 1/(4 pi^2 q^2).
    accelerated = -math.log(2.0) / 4.0 - 1.0 / 48.0
    correction_rows = []
    for winding in range(1, 9):
        finite = integrate.quad(
            lambda coordinate: (1.0 + coordinate)
            * special.k0(2.0 * math.pi * winding * coordinate),
            0.0,
            1.0,
            epsabs=1e-13,
            epsrel=1e-13,
            limit=500,
        )[0]
        infinite = 1.0 / (4.0 * winding) + 1.0 / (
            4.0 * math.pi**2 * winding**2
        )
        correction = (-1) ** winding * (finite - infinite)
        accelerated += correction
        correction_rows.append(
            {
                "winding": winding,
                "finite_integral": finite,
                "infinite_integral": infinite,
                "alternating_correction": correction,
            }
        )
    return accelerated, correction_rows


def main():
    scorecard = json.loads(
        Path("s2t_blind_prediction_scorecard_results.json").read_text()
    )
    tau_row = next(
        row for row in scorecard["rows"] if row["observable"] == "m_tau_MeV"
    )
    tau_control = tau_row["control"]
    tau_sigma = tau_row["control_sigma"]
    target_ratio = tau_control / M_MU_MEV
    ratio_sigma = tau_sigma / M_MU_MEV
    alpha = 1.0 / ALPHA_INVERSE

    seed = math.pi**2 + 2.0 * math.pi + 2.0 / 3.0
    claimed_factor = seed - alpha / 3.0
    claimed_mass = M_MU_MEV * claimed_factor
    seed_mass = M_MU_MEV * seed

    rationals = simple_rationals(4, 6)
    alpha_coefficients = [
        Fraction(0),
        Fraction(1),
        Fraction(-1),
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(1, 3),
        Fraction(-1, 3),
        Fraction(2, 3),
        Fraction(-2, 3),
    ]
    candidates = []
    for pi_coefficient in range(5):
        for rational in rationals:
            for alpha_coefficient in alpha_coefficients:
                value = (
                    math.pi**2
                    + pi_coefficient * math.pi
                    + float(rational)
                    + float(alpha_coefficient) * alpha
                )
                pull = (value - target_ratio) / ratio_sigma
                candidates.append(
                    {
                        "pi_coefficient": pi_coefficient,
                        "rational": str(rational),
                        "alpha_coefficient": str(alpha_coefficient),
                        "factor": value,
                        "absolute_pull": abs(pull),
                        "signed_pull": pull,
                        "complexity": formula_complexity(
                            pi_coefficient, rational, alpha_coefficient
                        ),
                    }
                )
    candidates.sort(key=lambda row: row["absolute_pull"])

    claimed_complexity = formula_complexity(
        2, Fraction(2, 3), Fraction(-1, 3)
    )
    claimed_pull = (claimed_mass - tau_control) / tau_sigma
    lower_complexity_candidates = [
        row for row in candidates if row["complexity"] <= claimed_complexity
    ]

    bessel_sum, correction_rows = compact_bessel_sum()
    raw_coefficient = bessel_sum / math.pi
    required_jacobian_for_magnitude = (1.0 / 3.0) / abs(raw_coefficient)
    raw_negative_mass = M_MU_MEV * (seed - abs(raw_coefficient) * alpha)

    results = {
        "status": "tau_formula_numerically_unique_but_seed_and_qed_normalization_not_derived",
        "date": "2026-08-04",
        "current_control": {
            "m_tau_MeV": tau_control,
            "sigma_MeV": tau_sigma,
            "target_ratio": target_ratio,
            "ratio_sigma": ratio_sigma,
        },
        "claimed_formula": {
            "formula": "m_tau/m_mu=pi^2+2pi+2/3-alpha/3",
            "factor": claimed_factor,
            "prediction_MeV": claimed_mass,
            "current_control_pull": claimed_pull,
            "seed_without_QED_prediction_MeV": seed_mass,
            "seed_without_QED_pull": (seed_mass - tau_control) / tau_sigma,
            "provenance_gap": "the Tome states rho0=pi^2+2pi+2/3 as an input to the QED theorem rather than deriving it from the lepton operator",
        },
        "look_elsewhere_diagnostic": {
            "warning": "this is a diagnostic inside a declared grammar, not a universal probability of accidental formulas",
            "grammar": "pi^2+n*pi+p/q+c*alpha with n=0..4, reduced |p|<=4, q<=6, c in {0,+/-1,+/-1/2,+/-1/3,+/-2/3}",
            "candidate_count": len(candidates),
            "within_one_sigma": sum(
                row["absolute_pull"] <= 1.0 for row in candidates
            ),
            "within_two_sigma": sum(
                row["absolute_pull"] <= 2.0 for row in candidates
            ),
            "at_least_as_close_as_claimed": sum(
                row["absolute_pull"] <= abs(claimed_pull) for row in candidates
            ),
            "claimed_rank": next(
                index + 1
                for index, row in enumerate(candidates)
                if row["pi_coefficient"] == 2
                and row["rational"] == "2/3"
                and row["alpha_coefficient"] == "-1/3"
            ),
            "claimed_complexity": claimed_complexity,
            "lower_or_equal_complexity_count": len(lower_complexity_candidates),
            "lower_or_equal_complexity_within_one_sigma": sum(
                row["absolute_pull"] <= 1.0
                for row in lower_complexity_candidates
            ),
            "top_candidates": candidates[:10],
        },
        "qed_integral_audit": {
            "declared_sum": "sum_q>=1 (-1)^q integral_0^1 (1+x) K0(2 pi q x) dx",
            "accelerated_sum": bessel_sum,
            "raw_coefficient_sum_over_pi": raw_coefficient,
            "target_coefficient_magnitude": 1.0 / 3.0,
            "required_jacobian_magnitude": required_jacobian_for_magnitude,
            "declared_jacobian_status": "J_RP3 is named but no explicit operator trace or numerical value is supplied",
            "canonical_unit_jacobian_prediction_MeV_using_desired_sign": raw_negative_mass,
            "canonical_unit_jacobian_pull": (
                raw_negative_mass - tau_control
            )
            / tau_sigma,
            "finite_interval_corrections": correction_rows,
        },
        "ablation": {
            "full_formula_pull": claimed_pull,
            "remove_QED_term_pull": (seed_mass - tau_control) / tau_sigma,
            "replace_one_third_by_raw_unit_jacobian_pull": (
                raw_negative_mass - tau_control
            )
            / tau_sigma,
            "interpretation": "the alpha/3 term improves the current control from 2.07 sigma to 0.78 sigma, but the written loop expression supplies only coefficient magnitude 0.06170 before an unspecified normalization",
        },
        "scientific_verdict": {
            "positive": "within the frozen low-complexity grammar the claimed formula is the unique candidate inside one sigma and ranks first among 1485 candidates",
            "negative": "rho0 is postulated and the displayed Bessel sum does not produce 1/3 without an unexplained Jacobian of magnitude 5.40275",
            "status_change": "downgrade m_tau from closed derivation to a strong conditional numerical relation",
            "next_gate": "derive rho0 from an explicit charged-lepton operator and compute the RP3 projection trace that fixes J_RP3 before using tau as an independent foundation for the Higgs scale",
        },
    }

    assert results["look_elsewhere_diagnostic"]["within_one_sigma"] == 1
    assert results["look_elsewhere_diagnostic"]["claimed_rank"] == 1
    assert required_jacobian_for_magnitude > 5.0
    assert abs(claimed_pull) < 1.0
    assert results["ablation"]["remove_QED_term_pull"] > 2.0

    Path("s2t_tau_uniqueness_normalization_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "claimed_pull": claimed_pull,
                "grammar_candidate_count": len(candidates),
                "within_one_sigma": results["look_elsewhere_diagnostic"][
                    "within_one_sigma"
                ],
                "bessel_sum": bessel_sum,
                "raw_coefficient": raw_coefficient,
                "required_jacobian_magnitude": required_jacobian_for_magnitude,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()