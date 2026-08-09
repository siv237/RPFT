#!/usr/bin/env python3
import json
import math
from pathlib import Path


def kernel_row(kind, parameter=None):
    if kind == "linear":
        first = 1.0
        second = 0.0
        label = "f(x)=x"
    elif kind == "exponential":
        rate = float(parameter)
        first = -rate
        second = rate**2
        label = f"f(x)=exp(-{rate:g}x)"
    elif kind == "rational":
        power = float(parameter)
        first = -power
        second = power * (power + 1.0)
        label = f"f(x)=(1+x)^(-{power:g})"
    else:
        raise ValueError(kind)

    quartic_coefficient = 0.5 * second
    stable_quartic = quartic_coefficient > 0.0
    tachyonic_quadratic = first < 0.0
    if stable_quartic and tachyonic_quadratic:
        lambda_gl = second
        vacuum_scale_sq = -first / second
        threshold_product = lambda_gl * vacuum_scale_sq
    else:
        lambda_gl = None
        vacuum_scale_sq = None
        threshold_product = None

    return {
        "kernel": label,
        "f_prime_0": first,
        "f_second_0": second,
        "quadratic_coefficient": first,
        "quartic_coefficient": quartic_coefficient,
        "stable_quartic": stable_quartic,
        "tachyonic_quadratic": tachyonic_quadratic,
        "lambda_GL": lambda_gl,
        "v_squared": vacuum_scale_sq,
        "lambda_v_squared": threshold_product,
    }


def main():
    parent = json.loads(
        Path("s2t_neutrino_parent_superconnection_embedding_results.json").read_text(
            encoding="utf-8"
        )
    )
    saddle = json.loads(
        Path("s2t_nonuniform_pairing_saddle_results.json").read_text(
            encoding="utf-8"
        )
    )
    phase_mass = json.loads(
        Path("s2t_eta_phase_mass_gate_results.json").read_text(
            encoding="utf-8"
        )
    )

    rows = [
        kernel_row("linear"),
        kernel_row("exponential", 1.0),
        kernel_row("exponential", 2.0),
        kernel_row("rational", 3.0),
        kernel_row("rational", 4.0),
    ]
    geometric_threshold = saddle["geometry"][
        "minimum_absolute_covariant_momentum"
    ] ** 2

    for row in rows:
        value = row["lambda_v_squared"]
        row["above_unit_RP3_threshold"] = (
            value is not None and value > geometric_threshold
        )
        row["at_critical_threshold"] = (
            value is not None
            and abs(value - geometric_threshold) < 1e-12
        )
        if row["above_unit_RP3_threshold"]:
            row["phase"] = "condensed"
        elif row["at_critical_threshold"]:
            row["phase"] = "critical"
        else:
            row["phase"] = "normal_or_unstable"

    k_plus = math.pi / math.pi
    k_minus = -math.pi / math.pi
    even_spectral_invariants = {
        "k_squared": [k_plus**2, k_minus**2],
        "k_fourth": [k_plus**4, k_minus**4],
        "absolute_k": [abs(k_plus), abs(k_minus)],
    }
    all_even_invariants_equal = all(
        abs(values[0] - values[1]) < 1e-12
        for values in even_spectral_invariants.values()
    )

    results = {
        "status": "existing_spectral_function_menu_does_not_uniquely_fix_pairing_condensation_and_parity_even_actions_cannot_select_orientation",
        "date": "2026-08-06",
        "reduced_spectral_expansion": {
            "formula": (
                "f(a^2)=f(0)+f'(0)a^2+(1/2)f''(0)a^4+..."
            ),
            "identification": {
                "quadratic_mass_coefficient": "c2=f'(0)",
                "quartic_coefficient": "c4=f''(0)/2",
                "lambda_GL": "f''(0)",
                "v_squared": "-f'(0)/f''(0)",
                "threshold_product": "lambda_GL*v^2=-f'(0)",
            },
            "scope": (
                "This is the one-amplitude control reduction with canonical kinetic "
                "normalization; a full spectral action must still derive the derivative "
                "term and its relative normalization."
            ),
        },
        "unit_RP3_threshold": geometric_threshold,
        "spectral_function_menu": rows,
        "menu_summary": {
            "normal_or_unstable_count": sum(
                row["phase"] == "normal_or_unstable" for row in rows
            ),
            "critical_count": sum(row["phase"] == "critical" for row in rows),
            "condensed_count": sum(row["phase"] == "condensed" for row in rows),
            "unique_phase_selected": len({row["phase"] for row in rows}) == 1,
        },
        "configuration_metric_crosscheck": {
            "collective_norm_squared": parent["canonical_configuration_metric"][
                "result"
            ],
            "fixes_kinetic_norm": True,
            "fixes_negative_quadratic_coefficient": False,
            "finding": (
                "The norm 23+pi^(-1) supplies a positive configuration-space metric. "
                "It does not determine the sign of f'(0) and therefore cannot by itself "
                "force the pairing instability."
            ),
        },
        "orientation_no_go": {
            "lowest_covariant_momenta": [k_plus, k_minus],
            "tested_even_invariants": even_spectral_invariants,
            "all_even_invariants_equal": all_even_invariants_equal,
            "statement": (
                "Any real parity-even action depending only on D^2 or even powers of "
                "the covariant momentum assigns equal energy to n=0 and n=-1."
            ),
            "required_new_term": (
                "A real orientation-odd contribution or a derived chiral boundary "
                "condition is required to split the conjugate branches."
            ),
            "eta_phase_does_not_supply_real_split_in_minimal_model": (
                "fails" in phase_mass["scientific_verdict"]["program_effect"]
                or "does not generate a real mass shift"
                in phase_mass["scientific_verdict"]["negative"]
            ),
        },
        "scientific_verdict": {
            "positive": (
                "For each declared spectral function the reduced quadratic and quartic "
                "coefficients determine the condensation threshold without fitting."
            ),
            "negative": (
                "The currently admitted spectral functions give three different outcomes: "
                "no stable condensate, a critical point, or condensation. The program has "
                "not derived which function and scale are fundamental."
            ),
            "orientation": (
                "The real parity-even spectral action cannot choose between the two "
                "conjugate windings. The previously tested eta phase does not become a "
                "real energy splitting in the minimal vectorlike theory."
            ),
            "program_effect": (
                "Neither the existence of the Majorana condensate nor its orientation is "
                "predicted by the current parent action. Both remain new action-level gates."
            ),
        },
    }

    assert rows[0]["phase"] == "normal_or_unstable"
    assert rows[1]["phase"] == "critical"
    assert rows[2]["phase"] == "condensed"
    assert rows[3]["phase"] == "condensed"
    assert rows[4]["phase"] == "condensed"
    assert results["menu_summary"]["unique_phase_selected"] is False
    assert all_even_invariants_equal is True
    assert results["configuration_metric_crosscheck"][
        "fixes_negative_quadratic_coefficient"
    ] is False

    Path("s2t_spectral_pairing_stiffness_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()