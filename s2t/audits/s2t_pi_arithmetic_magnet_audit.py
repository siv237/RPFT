import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


ALPHA_INVERSE = 137.035999177
M_MU_MEV = 105.6583755
RANDOM_SEED = 20260804


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


def grammar_rows(base, include_alpha=True, max_complexity=None):
    alpha = 1.0 / ALPHA_INVERSE
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
    if not include_alpha:
        alpha_coefficients = [Fraction(0)]

    rows = []
    for linear_coefficient in range(5):
        for rational in simple_rationals(4, 6):
            for alpha_coefficient in alpha_coefficients:
                complexity = formula_complexity(
                    linear_coefficient, rational, alpha_coefficient
                )
                if max_complexity is not None and complexity > max_complexity:
                    continue
                rows.append(
                    {
                        "linear_coefficient": linear_coefficient,
                        "rational": str(rational),
                        "alpha_coefficient": str(alpha_coefficient),
                        "complexity": complexity,
                        "value": (
                            base**2
                            + linear_coefficient * base
                            + float(rational)
                            + float(alpha_coefficient) * alpha
                        ),
                    }
                )
    return rows


def union_coverage(values, tolerance, lower, upper):
    intervals = []
    for value in sorted(set(values)):
        left = max(lower, value - tolerance)
        right = min(upper, value + tolerance)
        if left < right:
            intervals.append((left, right))
    if not intervals:
        return 0.0

    covered = 0.0
    current_left, current_right = intervals[0]
    for left, right in intervals[1:]:
        if left <= current_right:
            current_right = max(current_right, right)
        else:
            covered += current_right - current_left
            current_left, current_right = left, right
    covered += current_right - current_left
    return covered / (upper - lower)


def nearest_error_for_bases(bases, offsets_by_linear, target):
    best = np.full(bases.shape, np.inf)
    for linear_coefficient, offsets in offsets_by_linear.items():
        residual = target - bases**2 - linear_coefficient * bases
        positions = np.searchsorted(offsets, residual)
        lower_positions = np.clip(positions - 1, 0, len(offsets) - 1)
        upper_positions = np.clip(positions, 0, len(offsets) - 1)
        lower_error = np.abs(residual - offsets[lower_positions])
        upper_error = np.abs(residual - offsets[upper_positions])
        best = np.minimum(best, np.minimum(lower_error, upper_error))
    return best


def exact_base_coverage(offsets_by_linear, target, tolerance, lower, upper):
    intervals = []
    for linear_coefficient, offsets in offsets_by_linear.items():
        for offset in offsets:
            lower_level = target - tolerance - offset
            upper_level = target + tolerance - offset
            lower_discriminant = linear_coefficient**2 + 4.0 * lower_level
            upper_discriminant = linear_coefficient**2 + 4.0 * upper_level
            if upper_discriminant < 0.0:
                continue
            left = (
                -linear_coefficient
                + math.sqrt(max(0.0, lower_discriminant))
            ) / 2.0
            right = (
                -linear_coefficient + math.sqrt(upper_discriminant)
            ) / 2.0
            left = max(lower, left)
            right = min(upper, right)
            if left < right:
                intervals.append((left, right))
    if not intervals:
        return 0.0
    intervals.sort()
    covered = 0.0
    current_left, current_right = intervals[0]
    for left, right in intervals[1:]:
        if left <= current_right:
            current_right = max(current_right, right)
        else:
            covered += current_right - current_left
            current_left, current_right = left, right
    covered += current_right - current_left
    return covered / (upper - lower)


def offsets_by_linear(max_complexity=None):
    alpha = 1.0 / ALPHA_INVERSE
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
    result = {}
    for linear_coefficient in range(5):
        values = []
        for rational in simple_rationals(4, 6):
            for alpha_coefficient in alpha_coefficients:
                complexity = formula_complexity(
                    linear_coefficient, rational, alpha_coefficient
                )
                if max_complexity is not None and complexity > max_complexity:
                    continue
                values.append(float(rational) + float(alpha_coefficient) * alpha)
        result[linear_coefficient] = np.array(sorted(set(values)))
    return result


def base_control(name, base, target, tolerance, claimed_complexity):
    rows = grammar_rows(base)
    restricted_rows = grammar_rows(base, max_complexity=claimed_complexity)
    nearest = min(rows, key=lambda row: abs(row["value"] - target))
    restricted_nearest = min(
        restricted_rows, key=lambda row: abs(row["value"] - target)
    )
    return {
        "name": name,
        "base": base,
        "best_error": abs(nearest["value"] - target),
        "beats_pi_tolerance": abs(nearest["value"] - target) <= tolerance,
        "best_formula": nearest,
        "restricted_best_error": abs(restricted_nearest["value"] - target),
        "restricted_best_formula": restricted_nearest,
    }


def main():
    tau_results = json.loads(
        Path("s2t_tau_uniqueness_normalization_results.json").read_text()
    )
    target = tau_results["current_control"]["target_ratio"]
    ratio_sigma = tau_results["current_control"]["ratio_sigma"]
    claimed_value = tau_results["claimed_formula"]["factor"]
    observed_error = abs(claimed_value - target)
    claimed_complexity = tau_results["look_elsewhere_diagnostic"][
        "claimed_complexity"
    ]

    all_rows = grammar_rows(math.pi)
    restricted_rows = grammar_rows(
        math.pi, max_complexity=claimed_complexity
    )
    no_alpha_rows = grammar_rows(math.pi, include_alpha=False)
    all_values = [row["value"] for row in all_rows]
    restricted_values = [row["value"] for row in restricted_rows]
    no_alpha_values = [row["value"] for row in no_alpha_rows]

    support_lower = min(all_values)
    support_upper = max(all_values)
    domains = {
        "full_grammar_support": (support_lower, support_upper),
        "tau_centered_width_10": (target - 5.0, target + 5.0),
        "tau_centered_width_4": (target - 2.0, target + 2.0),
        "tau_centered_width_2": (target - 1.0, target + 1.0),
        "tau_centered_width_1": (target - 0.5, target + 0.5),
    }
    tolerances = {
        "observed_error": observed_error,
        "one_sigma": ratio_sigma,
        "two_sigma": 2.0 * ratio_sigma,
    }
    coverage = {}
    for domain_name, (lower, upper) in domains.items():
        coverage[domain_name] = {}
        for tolerance_name, tolerance in tolerances.items():
            coverage[domain_name][tolerance_name] = {
                "all_grammar": union_coverage(
                    all_values, tolerance, lower, upper
                ),
                "complexity_at_most_claimed": union_coverage(
                    restricted_values, tolerance, lower, upper
                ),
                "without_alpha_term": union_coverage(
                    no_alpha_values, tolerance, lower, upper
                ),
            }

    sorted_values = np.array(sorted(set(all_values)))
    insertion = int(np.searchsorted(sorted_values, target))
    local_values = sorted_values[max(0, insertion - 5) : insertion + 5]
    local_rows = [
        {
            "value": float(value),
            "signed_offset": float(value - target),
            "absolute_offset": float(abs(value - target)),
        }
        for value in local_values
    ]

    rng = np.random.default_rng(RANDOM_SEED)
    random_bases = rng.uniform(2.0, 4.0, size=500_000)
    random_errors = nearest_error_for_bases(
        random_bases, offsets_by_linear(), target
    )
    restricted_random_errors = nearest_error_for_bases(
        random_bases, offsets_by_linear(claimed_complexity), target
    )
    pi_best_error = min(abs(value - target) for value in all_values)
    pi_restricted_best_error = min(
        abs(value - target) for value in restricted_values
    )

    named_controls = [
        base_control("sqrt(2)", math.sqrt(2.0), target, pi_best_error, claimed_complexity),
        base_control("golden_ratio", (1.0 + math.sqrt(5.0)) / 2.0, target, pi_best_error, claimed_complexity),
        base_control("sqrt(3)", math.sqrt(3.0), target, pi_best_error, claimed_complexity),
        base_control("e", math.e, target, pi_best_error, claimed_complexity),
        base_control("pi", math.pi, target, pi_best_error, claimed_complexity),
        base_control("sqrt(10)", math.sqrt(10.0), target, pi_best_error, claimed_complexity),
    ]

    random_fraction_beating_pi = float(
        np.mean(random_errors <= pi_best_error)
    )
    restricted_fraction_beating_pi = float(
        np.mean(restricted_random_errors <= pi_restricted_best_error)
    )
    exact_base_fraction_beating_pi = exact_base_coverage(
        offsets_by_linear(), target, pi_best_error, 2.0, 4.0
    )
    exact_restricted_base_fraction_beating_pi = exact_base_coverage(
        offsets_by_linear(claimed_complexity),
        target,
        pi_restricted_best_error,
        2.0,
        4.0,
    )
    random_quantiles = {
        str(percentile): float(np.quantile(random_errors, percentile))
        for percentile in [0.01, 0.05, 0.1, 0.25, 0.5, 0.9]
    }

    full_support_observed_coverage = coverage["full_grammar_support"][
        "observed_error"
    ]["all_grammar"]
    local_observed_coverage = coverage["tau_centered_width_2"][
        "observed_error"
    ]["all_grammar"]
    if exact_base_fraction_beating_pi >= 0.05 or local_observed_coverage >= 0.05:
        status = "pi_is_an_arithmetic_magnet_inside_the_posthoc_grammar"
        verdict = (
            "The rank-one statement is misleading: after accounting for target "
            "coverage and base choice, coincidences at least this close are not rare."
        )
    else:
        status = "pi_remains_unusually_selective_inside_the_frozen_grammar"
        verdict = (
            "The coincidence remains statistically selective inside this grammar, "
            "although it is still post hoc and has no physical derivation."
        )

    results = {
        "status": status,
        "date": "2026-08-04",
        "hypothesis": (
            "Short expressions involving pi, small rationals and alpha form a dense "
            "arithmetic net, so a unique best formula can arise without physics."
        ),
        "frozen_grammar": {
            "expression": "x^2+n*x+p/q+c*alpha",
            "n": "0..4",
            "rational_rule": "reduced |p|<=4 and q<=6",
            "alpha_coefficients": "0,+/-1,+/-1/2,+/-1/3,+/-2/3",
            "candidate_count": len(all_rows),
            "distinct_value_count": len(set(all_values)),
            "claimed_complexity": claimed_complexity,
            "restricted_candidate_count": len(restricted_rows),
            "no_alpha_candidate_count": len(no_alpha_rows),
        },
        "tau_target": {
            "ratio": target,
            "ratio_sigma": ratio_sigma,
            "claimed_value": claimed_value,
            "observed_absolute_error": observed_error,
            "observed_error_in_sigma": observed_error / ratio_sigma,
            "pi_best_error": pi_best_error,
            "pi_restricted_best_error": pi_restricted_best_error,
        },
        "exact_target_coverage": {
            "interpretation": (
                "Probability that a uniformly chosen target in the declared interval "
                "lies within the stated tolerance of at least one grammar value."
            ),
            "domains": {
                name: {"lower": bounds[0], "upper": bounds[1]}
                for name, bounds in domains.items()
            },
            "coverage_fractions": coverage,
            "headline_full_support_observed": full_support_observed_coverage,
            "headline_local_width_2_observed": local_observed_coverage,
        },
        "random_base_control": {
            "base_distribution": "uniform x in [2,4]",
            "sample_size": len(random_bases),
            "seed": RANDOM_SEED,
            "fraction_with_best_error_at_most_pi": random_fraction_beating_pi,
            "exact_fraction_of_base_interval_beating_pi": exact_base_fraction_beating_pi,
            "pi_percentile_as_small_error": exact_base_fraction_beating_pi,
            "restricted_fraction_with_best_error_at_most_pi": restricted_fraction_beating_pi,
            "exact_restricted_fraction_of_base_interval_beating_pi": exact_restricted_base_fraction_beating_pi,
            "error_quantiles": random_quantiles,
            "named_constants": named_controls,
        },
        "local_pi_neighborhood": local_rows,
        "ablation": {
            "full_support_coverage_with_alpha": full_support_observed_coverage,
            "full_support_coverage_without_alpha": coverage[
                "full_grammar_support"
            ]["observed_error"]["without_alpha_term"],
            "local_width_2_coverage_with_alpha": local_observed_coverage,
            "local_width_2_coverage_without_alpha": coverage[
                "tau_centered_width_2"
            ]["observed_error"]["without_alpha_term"],
        },
        "scientific_verdict": {
            "verdict": verdict,
            "what_rank_one_did_show": (
                "The chosen expression is the closest member of the frozen finite list."
            ),
            "what_rank_one_did_not_show": (
                "It did not measure the look-elsewhere effect over targets, bases, "
                "grammar choices or earlier formula-search decisions."
            ),
            "physical_status": (
                "No physical evidence is created either way; an operator derivation "
                "and prospective prediction remain mandatory."
            ),
        },
    }

    assert len(all_rows) == 1485
    assert abs(pi_best_error - observed_error) < 1e-14
    assert 0.0 <= full_support_observed_coverage <= 1.0
    assert 0.0 <= random_fraction_beating_pi <= 1.0
    assert abs(random_fraction_beating_pi - exact_base_fraction_beating_pi) < 0.002

    Path("s2t_pi_arithmetic_magnet_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": status,
                "observed_error": observed_error,
                "full_support_coverage": full_support_observed_coverage,
                "local_width_2_coverage": local_observed_coverage,
                "random_bases_beating_pi": random_fraction_beating_pi,
                "exact_base_fraction_beating_pi": exact_base_fraction_beating_pi,
                "restricted_random_bases_beating_pi": restricted_fraction_beating_pi,
                "exact_restricted_base_fraction_beating_pi": exact_restricted_base_fraction_beating_pi,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()