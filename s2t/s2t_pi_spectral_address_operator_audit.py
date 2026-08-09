import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def polynomial(terms):
    return {int(power): Fraction(value) for power, value in terms.items()}


FORMULAS = [
    {
        "name": "strong_coupling",
        "numerator": polynomial({0: 1}),
        "denominator": polynomial({2: Fraction(1, 4), 0: 6}),
    },
    {
        "name": "weinberg_angle",
        "numerator": polynomial({0: 8, -1: Fraction(-3, 4)}),
        "denominator": polynomial({0: 21, 1: 4}),
    },
    {
        "name": "bottom_over_proton",
        "numerator": polynomial({1: 1, 0: Fraction(4, 3)}),
        "denominator": polynomial({0: 1}),
    },
    {
        "name": "proton_over_strange_denominator",
        "numerator": polynomial({0: 1}),
        "denominator": polynomial({2: 1, 0: Fraction(1, 3)}),
    },
    {
        "name": "down_over_electron",
        "numerator": polynomial({2: 1, 0: -1}),
        "denominator": polynomial({0: 1}),
    },
    {
        "name": "up_over_electron",
        "numerator": polynomial({1: 1, 0: 1}),
        "denominator": polynomial({0: 1}),
    },
    {
        "name": "tau_over_muon_core",
        "numerator": polynomial({2: 1, 1: 2, 0: Fraction(2, 3)}),
        "denominator": polynomial({0: 1}),
        "extension": "+2*alpha/3 in atlas; alpha belongs to the same fraction field if S_vac(pi) is substituted",
    },
    {
        "name": "v_cb",
        "numerator": polynomial({0: 1}),
        "denominator": polynomial({0: 24, -1: -1}),
    },
    {
        "name": "omega_lambda",
        "numerator": polynomial({0: 1, -1: -1}),
        "denominator": polynomial({0: 1}),
    },
    {
        "name": "omega_dark_matter",
        "numerator": polynomial({-1: 1, -2: Fraction(-1, 2)}),
        "denominator": polynomial({0: 1}),
    },
    {
        "name": "omega_baryon",
        "numerator": polynomial({-2: Fraction(1, 2)}),
        "denominator": polynomial({0: 1}),
    },
]


def evaluate(poly, base):
    return sum(float(coefficient) * base**power for power, coefficient in poly.items())


def in_z_one_over_24(coefficient):
    return 24 % coefficient.denominator == 0


def coefficient_matrix(poly, powers):
    coefficients = [float(poly.get(power, 0)) for power in powers]
    return np.diag(coefficients)


def main():
    powers = list(range(-4, 4))
    dilation_generator = np.diag(powers)
    pi_scaling_operator = np.diag([math.pi**power for power in powers])

    rows = []
    coefficient_values = set()
    total_nonzero_slots = 0
    for formula in FORMULAS:
        numerator = formula["numerator"]
        denominator = formula["denominator"]
        all_coefficients = list(numerator.values()) + list(denominator.values())
        coefficient_values.update(all_coefficients)
        coefficient_lattice_pass = all(
            in_z_one_over_24(coefficient) for coefficient in all_coefficients
        )
        numerator_matrix = coefficient_matrix(numerator, powers)
        denominator_matrix = coefficient_matrix(denominator, powers)
        numerator_trace = float(np.trace(numerator_matrix @ pi_scaling_operator))
        denominator_trace = float(
            np.trace(denominator_matrix @ pi_scaling_operator)
        )
        direct_value = evaluate(numerator, math.pi) / evaluate(
            denominator, math.pi
        )
        operator_value = numerator_trace / denominator_trace
        nonzero_slots = len(numerator) + len(denominator)
        total_nonzero_slots += nonzero_slots
        rows.append(
            {
                "name": formula["name"],
                "numerator": {
                    str(power): str(coefficient)
                    for power, coefficient in sorted(numerator.items())
                },
                "denominator": {
                    str(power): str(coefficient)
                    for power, coefficient in sorted(denominator.items())
                },
                "coefficient_lattice_Z_one_over_24": coefficient_lattice_pass,
                "nonzero_coefficient_slots": nonzero_slots,
                "direct_value": direct_value,
                "operator_trace_ratio": operator_value,
                "operator_identity_error": abs(direct_value - operator_value),
                "extension": formula.get("extension"),
            }
        )

    all_lattice_pass = all(
        row["coefficient_lattice_Z_one_over_24"] for row in rows
    )
    all_operator_pass = all(
        row["operator_identity_error"] < 1e-13 for row in rows
    )

    s_geo = 4.0 * math.pi**3 + math.pi**2 + math.pi
    s_vac = s_geo - 1.0 / (24.0 * s_geo) - 1.0 / (
        math.pi**4 * s_geo**2
    )
    alpha = 1.0 / s_vac
    tau_core = next(
        row["direct_value"] for row in rows if row["name"] == "tau_over_muon_core"
    )

    results = {
        "status": "common_pi_spectral_address_algebra_found_but_address_selector_missing",
        "date": "2026-08-04",
        "hypothesis": (
            "The short RPFT formulas are observable-specific matrix elements of one "
            "dilation operator rather than unrelated numerical coincidences."
        ),
        "coefficient_ring": {
            "ring": "A_24=Z[1/24][Pi,Pi^-1]",
            "fraction_field": "Frac(A_24)",
            "formula_count_tested": len(rows),
            "all_coefficients_in_ring": all_lattice_pass,
            "distinct_coefficients": sorted(
                [str(value) for value in coefficient_values]
            ),
            "exception_outside_ring": {
                "claim": "delta_CKM=pi/e",
                "reason": "Euler's e is not generated by the pi Laurent ring",
            },
            "alpha_closure": {
                "S_geo": "4*pi^3+pi^2+pi",
                "S_vac": "S_geo-1/(24*S_geo)-1/(pi^4*S_geo^2)",
                "conclusion": "alpha=1/S_vac belongs to Frac(A_24)",
                "numeric_alpha": alpha,
                "atlas_tau_full_value": tau_core + 2.0 * alpha / 3.0,
            },
        },
        "universal_operator": {
            "hilbert_basis": "|k>, k=-4,...,3",
            "generator": "D|k>=k|k>",
            "scaling_operator": "Pi=exp(log(pi)*D), hence Pi|k>=pi^k|k>",
            "observable_rule": "O_f=Tr(C_num*Pi)/Tr(C_den*Pi)",
            "all_trace_identities_verified": all_operator_pass,
            "matrix_dimension": len(powers),
            "generator_diagonal": powers,
        },
        "formula_rows": rows,
        "selection_problem": {
            "total_nonzero_coefficient_slots": total_nonzero_slots,
            "observable_specific_coefficient_matrices": 2 * len(rows),
            "problem": (
                "The common operator supplies the powers of pi, but a different pair "
                "of sparse coefficient matrices is still assigned to every observable."
            ),
            "no_go": (
                "Without a symmetry that derives the coefficient matrices from particle "
                "quantum numbers, the construction is an exact encoding, not a prediction."
            ),
        },
        "new_lead": {
            "observation": (
                "All tested rational coefficients have denominators dividing 24; the "
                "same number appears as the SU(5) adjoint dimension and in the S_vac "
                "Casimir correction."
            ),
            "caution": (
                "This may merely reflect the preference for small fractions. The next "
                "gate must derive 1/24 from the parent representation, not notice it "
                "after the formulas are known."
            ),
            "next_gate": (
                "Map each particle representation and menu sector to one coefficient "
                "matrix C_f using only ranks, characters and normalized traces."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "A nontrivial common algebraic compression exists: eleven strong formulas "
                "share one Laurent coefficient ring and one dilation-operator realization."
            ),
            "negative": (
                "The observable address is not derived, so the result does not yet reduce "
                "the formula-search freedom or create a physical prediction."
            ),
        },
    }

    assert all_lattice_pass
    assert all_operator_pass
    assert len(rows) == 11
    assert total_nonzero_slots == 34

    Path("s2t_pi_spectral_address_operator_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "formula_count": len(rows),
                "all_in_A24": all_lattice_pass,
                "operator_identities": all_operator_pass,
                "coefficient_slots": total_nonzero_slots,
                "exception": "delta_CKM=pi/e",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()