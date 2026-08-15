#!/usr/bin/env python3
import json
import math
from pathlib import Path

import sympy as sp


def main():
    pi = sp.pi
    halfshift_trace = pi**4 / 3

    full_ranks = {"two_form": 6, "one_form": 4, "scalar": 1}
    full_gamma_coefficients = {
        "two_form": sp.Rational(1, 2),
        "one_form": -sp.Integer(1),
        "scalar": sp.Rational(3, 2),
    }
    transverse_ranks = {"two_form": 3, "one_form": 3, "scalar": 1}
    transverse_gamma_coefficients = {
        "two_form": sp.Rational(1, 2),
        "one_form": -sp.Rational(1, 2),
        "scalar": sp.Rational(1, 2),
    }

    full_effective_count = sum(
        full_ranks[name] * full_gamma_coefficients[name]
        for name in full_ranks
    )
    transverse_effective_count = sum(
        transverse_ranks[name] * transverse_gamma_coefficients[name]
        for name in transverse_ranks
    )

    bosonic_zero_shell_hessian = sp.simplify(
        -full_effective_count * halfshift_trace
    )
    statistics_reversed_zero_shell_hessian = -bosonic_zero_shell_hessian
    copies_for_positive_pi4_zero_shell = sp.simplify(
        pi**4 / statistics_reversed_zero_shell_hessian
    )

    # Real cohomology of RP3: b0=b3=1 and b1=b2=0. Therefore the spatially
    # harmonic pure S1 tower exists only in the scalar ghost-for-ghost block.
    rp3_betti = [1, 0, 0, 1]
    harmonic_gamma_coefficient = transverse_gamma_coefficients["scalar"]
    harmonic_bosonic_hessian = sp.simplify(
        -harmonic_gamma_coefficient * halfshift_trace
    )

    x = sp.symbols("x", positive=True)
    massive_halfshift_sum = sp.simplify(
        pi * sp.tanh(pi * x) / (2 * x**3)
        - pi**2 / (2 * x**2 * sp.cosh(pi * x) ** 2)
    )

    shell_cutoffs = [0, 2, 4, 10, 20, 50, 100, 200, 500]
    reversed_partial_sums = []
    for cutoff in shell_cutoffs:
        total = 0.0
        for ell in range(0, cutoff + 1, 2):
            if ell == 0:
                circle_sum = math.pi**4 / 3.0
            else:
                eigenvalue = ell * (ell + 2)
                root = math.sqrt(eigenvalue)
                argument = math.pi * root
                sech_squared = (
                    0.0 if argument > 350 else 1.0 / math.cosh(argument) ** 2
                )
                circle_sum = (
                    math.pi * math.tanh(argument) / (2 * root**3)
                    - math.pi**2 * sech_squared / (2 * root**2)
                )
            total += (ell + 1) ** 2 * circle_sum / 2.0
        reversed_partial_sums.append(
            {
                "maximum_even_ell": cutoff,
                "statistics_reversed_partial_Hessian": total,
                "ratio_to_pi4": total / math.pi**4,
            }
        )

    results = {
        "status": "standard_twisted_twoform_BV_complex_has_log_divergent_4d_Hessian_and_zero_shell_minus_pi4_over_6",
        "date": "2026-08-06",
        "minimal_BV_complex": {
            "field": "bosonic B_2 in Omega^2(K,L_minus)",
            "gauge_symmetry": "delta B_2=d_L Lambda_1",
            "reducibility": "Lambda_1 -> Lambda_1+d_L phi_0",
            "minimal_ghosts": [
                "Grassmann one-form ghost c_1",
                "bosonic scalar ghost-for-ghost c_0",
            ],
            "twist_consistency": (
                "B_2, c_1 and c_0 are sections of the same flat line bundle L_minus, "
                "because d_L preserves the coefficient bundle. Hence the whole tower, not "
                "one selected determinant, has the half-integer S1 spectrum."
            ),
        },
        "determinant_representations": {
            "full_forms": {
                "partition_function": (
                    "Z_2=det'(Delta_2)^(-1/2) det'(Delta_1)^(+1) "
                    "det'(Delta_0)^(-3/2) times zero-mode/topological factors"
                ),
                "Gamma_coefficients": {
                    key: str(value) for key, value in full_gamma_coefficients.items()
                },
                "bundle_ranks": full_ranks,
                "effective_count": str(full_effective_count),
            },
            "transverse_forms": {
                "partition_function": (
                    "Z_2=det'(Delta_2^T)^(-1/2) det'(Delta_1^T)^(+1/2) "
                    "det'(Delta_0)^(-1/2)"
                ),
                "Gamma_coefficients": {
                    key: str(value)
                    for key, value in transverse_gamma_coefficients.items()
                },
                "polarization_ranks": transverse_ranks,
                "effective_count": str(transverse_effective_count),
            },
            "representations_agree": full_effective_count == transverse_effective_count,
            "physical_degrees_of_freedom": int(2 - 1),
        },
        "halfshift_hessian": {
            "per_scalar_trace": str(halfshift_trace),
            "identity": "sum_{n in Z}(n+1/2)^(-4)=pi^4/3",
            "bosonic_spatial_zero_shell": str(bosonic_zero_shell_hessian),
            "statistics_reversed_spatial_zero_shell": str(
                statistics_reversed_zero_shell_hessian
            ),
            "target": "pi^4",
            "independent_statistics_reversed_zero_shell_copies_required": str(
                copies_for_positive_pi4_zero_shell
            ),
        },
        "spatial_harmonic_gate": {
            "RP3_real_betti_numbers": rp3_betti,
            "harmonic_two_form_channels": rp3_betti[2],
            "harmonic_one_form_channels": rp3_betti[1],
            "harmonic_scalar_channels": rp3_betti[0],
            "pure_S1_bosonic_Hessian": str(harmonic_bosonic_hessian),
            "finding": (
                "RP3 supplies no harmonic one- or two-form triplet. The only exact pure "
                "half-shifted S1 tower in the standard complex is the scalar ghost-for-ghost "
                "tower, again giving -pi^4/6 for bosonic B_2."
            ),
        },
        "nonzero_RP3_modes": {
            "sum_formula": str(massive_halfshift_sum),
            "definition": (
                "sum_n [((n+1/2)^2+x^2)^(-2)] with x^2 an RP3 eigenvalue"
            ),
            "finding": (
                "Nonzero spatial modes produce hyperbolic functions of the RP3 eigenvalues, "
                "not a universal rational multiple of pi^4. With scalar RP3 eigenvalues "
                "ell(ell+2), even ell and multiplicity (ell+1)^2, the shell contribution "
                "falls only as 1/ell. The four-dimensional Hessian is logarithmically "
                "ultraviolet divergent and requires a local subtraction scheme."
            ),
            "statistics_reversed_partial_sums": reversed_partial_sums,
            "large_even_ell_asymptotic_per_shell": "pi/(4 ell)",
            "divergence": "logarithmic",
        },
        "corrections_to_previous_controls": {
            "invalid_raw_count": (
                "Using transverse exponents (+1/2,-1/2,+1/2) with full ranks (6,4,1) "
                "gave the spurious effective count 3/2."
            ),
            "correct_raw_count": (
                "Full ranks require full-form exponents (+1/2,-1,+3/2), giving 1/2."
            ),
            "isolated_six_component_ghost": (
                "Treating the six components of a Grassmann two-form as unconstrained gives "
                "+pi^4, but the reducible gauge quotient lowers a complete statistics-reversed "
                "two-form complex to +pi^4/6 in the spatial zero shell. The full local "
                "four-dimensional trace is divergent."
            ),
        },
        "scientific_verdict": {
            "standard_bosonic_complex": "wrong_sign_and_UV_divergent",
            "single_statistics_reversed_complex": (
                "positive but UV divergent; its spatial zero shell is pi4/6"
            ),
            "positive_pi4_requires": (
                "a derived renormalization prescription and a nonstandard graded parent "
                "complex; six copies match only the isolated spatial zero shell"
            ),
            "status": "standard_BV_route_closed_as_a_pi4_derivation",
            "next_allowed_route": (
                "Only a separately derived graded parent symmetry may fix the field content, "
                "counterterm scheme and source map. Selecting the spatial zero shell or adding "
                "six copies because they fit the target is prohibited."
            ),
        },
    }

    assert full_effective_count == sp.Rational(1, 2)
    assert transverse_effective_count == sp.Rational(1, 2)
    assert bosonic_zero_shell_hessian == -pi**4 / 6
    assert statistics_reversed_zero_shell_hessian == pi**4 / 6
    assert copies_for_positive_pi4_zero_shell == 6
    assert harmonic_bosonic_hessian == -pi**4 / 6

    Path("s2t_twisted_twoform_bv_complete_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "full_effective_count": str(full_effective_count),
                "transverse_effective_count": str(transverse_effective_count),
                "bosonic_zero_shell_Hessian": str(bosonic_zero_shell_hessian),
                "statistics_reversed_zero_shell_Hessian": str(
                    statistics_reversed_zero_shell_hessian
                ),
                "full_four_dimensional_trace": "logarithmically divergent",
                "copies_for_zero_shell_positive_pi4": str(
                    copies_for_positive_pi4_zero_shell
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()