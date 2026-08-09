#!/usr/bin/env python3

import json
import math
from pathlib import Path


def stable_mode_log_ratio(rho, beta):
    q = math.exp(-2.0 * math.pi * rho)
    cosine = math.cos(2.0 * math.pi * beta)
    return math.log(
        (1.0 - 2.0 * cosine * q + q * q) / ((1.0 - q) ** 2)
    )


def massive_relative_gamma(beta, radius_ratio, n_max=160):
    scalar = 0.0
    coexact = 0.0
    for n in range(1, n_max + 1):
        if n % 2 == 1:
            coexact += (
                2
                * n
                * (n + 2)
                * stable_mode_log_ratio(radius_ratio * (n + 1), beta)
            )
        elif n >= 2:
            scalar += (
                (n + 1) ** 2
                * stable_mode_log_ratio(
                    radius_ratio * math.sqrt(n * (n + 2)), beta
                )
            )
    return 0.5 * coexact - 0.5 * scalar


def low_coexact_product_spectrum(radius_ratio, beta, n_max=9, m_max=8):
    rows = []
    for n in range(1, n_max + 1, 2):
        multiplicity = 2 * n * (n + 2)
        for momentum in range(-m_max, m_max + 1):
            eigenvalue = (n + 1) ** 2 + ((momentum + beta) / radius_ratio) ** 2
            rows.append(
                {
                    "eigenvalue": eigenvalue,
                    "multiplicity": multiplicity,
                    "n": n,
                    "momentum": momentum,
                }
            )
    return sorted(rows, key=lambda row: row["eigenvalue"])


def compare_low_spectra(radius_ratio, beta, count=30):
    direct = low_coexact_product_spectrum(radius_ratio, beta)[:count]
    inverse = low_coexact_product_spectrum(1.0 / radius_ratio, beta)[:count]
    exact_position_matches = 0
    relative_differences = []
    multiplicity_matches = 0
    for left, right in zip(direct, inverse):
        scale = max(abs(left["eigenvalue"]), abs(right["eigenvalue"]), 1.0)
        difference = abs(left["eigenvalue"] - right["eigenvalue"]) / scale
        relative_differences.append(difference)
        if difference < 1e-12 and left["multiplicity"] == right["multiplicity"]:
            exact_position_matches += 1
        if left["multiplicity"] == right["multiplicity"]:
            multiplicity_matches += 1
    return {
        "radius_ratio": radius_ratio,
        "inverse_radius_ratio": 1.0 / radius_ratio,
        "compared_levels": count,
        "exact_position_matches": exact_position_matches,
        "multiplicity_position_matches": multiplicity_matches,
        "mean_relative_eigenvalue_difference": sum(relative_differences) / count,
        "max_relative_eigenvalue_difference": max(relative_differences),
        "first_direct_levels": direct[:8],
        "first_inverse_levels": inverse[:8],
    }


quarter_beta = 0.25
response_asymmetry = []
for radius_ratio in [0.4, 0.5, 0.75, 1.25, 2.0, 2.5]:
    direct = massive_relative_gamma(quarter_beta, radius_ratio)
    inverse = massive_relative_gamma(quarter_beta, 1.0 / radius_ratio)
    response_asymmetry.append(
        {
            "radius_ratio": radius_ratio,
            "G_r": direct,
            "G_inverse_r": inverse,
            "absolute_difference": abs(direct - inverse),
            "relative_difference": abs(direct - inverse)
            / max(abs(direct), abs(inverse), 1e-300),
        }
    )

spectrum_tests = [
    compare_low_spectra(radius_ratio, quarter_beta)
    for radius_ratio in [0.5, 0.75, 1.25, 2.0]
]

paired = json.loads(
    Path("s2t_c6_paired_sector_search_results.json").read_text(encoding="utf-8")
)
qcycle = json.loads(
    Path("s2t_neutrino_qcycle_geodesic_gram_results.json").read_text(
        encoding="utf-8"
    )
)

maxwell_duality_row = next(
    row
    for row in paired["candidate_table"]
    if row["candidate_sector"] == "Maxwell_scalar_duality_sector"
)

radius_samples = [0.5, 0.75, 1.25, 2.0]
zero_mode_scaling = []
for radius_ratio in radius_samples:
    logdet_direct = 2.0 * math.log(2.0 * math.pi * radius_ratio)
    logdet_inverse = 2.0 * math.log(2.0 * math.pi / radius_ratio)
    zero_mode_scaling.append(
        {
            "radius_ratio": radius_ratio,
            "logdet_prime_circle_scalar": logdet_direct,
            "logdet_prime_at_inverse_radius": logdet_inverse,
            "difference": logdet_direct - logdet_inverse,
            "expected_4_log_r": 4.0 * math.log(radius_ratio),
            "identity_error": abs(
                (logdet_direct - logdet_inverse)
                - 4.0 * math.log(radius_ratio)
            ),
        }
    )

ambient_isospectral = all(
    row["exact_position_matches"] == row["compared_levels"]
    for row in spectrum_tests
)
single_response_dual = all(
    row["relative_difference"] < 1e-12 for row in response_asymmetry
)
zero_mode_dual = all(abs(row["difference"]) < 1e-12 for row in zero_mode_scaling)
maxwell_duality_additive = maxwell_duality_row["status"] != "fail_duality_not_additive"

results = {
    "status": "ambient_reciprocal_duality_bridge_fails_in_current_Maxwell_FP_model",
    "date": "2026-08-03",
    "bridge_claim_tested": (
        "The intrinsic Qcycle involution should force equal-weight pairing of the full "
        "ambient Maxwell--FP relative determinants at r and 1/r."
    ),
    "tests": {
        "low_coexact_product_spectra": spectrum_tests,
        "single_relative_response": response_asymmetry,
        "scalar_zero_mode_measure_scaling": zero_mode_scaling,
        "known_Maxwell_duality_candidate": maxwell_duality_row,
    },
    "source_domains": {
        "Qcycle": {
            "space": qcycle["integral_cycle_complex"]["space"],
            "duality": qcycle["Qcycle"]["duality"],
            "scope": "intrinsic H0(gamma) direct_sum H1(gamma) Gram complex",
        },
        "ambient_Maxwell_FP": {
            "space": (
                "coexact one-forms and nonzero scalars on RP3 x S1 with KK momentum"
            ),
            "radius_action": (
                "r inversion rescales circle KK eigenvalues but does not exchange them "
                "with RP3 p-form shells or their multiplicities"
            ),
        },
    },
    "checks": {
        "ambient_low_spectra_isospectral_under_r_inversion": ambient_isospectral,
        "single_relative_response_is_dual": single_response_dual,
        "zero_mode_measure_is_dual": zero_mode_dual,
        "Maxwell_duality_supplies_additive_inverse_radius_sector": maxwell_duality_additive,
        "zero_mode_scaling_identity_verified": max(
            row["identity_error"] for row in zero_mode_scaling
        )
        < 1e-14,
    },
    "interpretation": {
        "spectral_failure": (
            "The product spectra at r and 1/r are not isospectral away from r=1. "
            "Circle KK momentum is not exchanged with RP3 coexact/scalar shells."
        ),
        "response_failure": (
            "The computed single determinant response G(r) is strongly asymmetric; "
            "G(r)+G(1/r) becomes dual only because the second term is appended."
        ),
        "zero_mode_failure": (
            "For the constant scalar circle branch, det'(-d^2)= (2*pi*R1)^2, "
            "so radius inversion produces the nonzero shift 4 log r before gauge-volume bookkeeping."
        ),
        "duality_failure": (
            "Ordinary Maxwell duality rewrites physical modes; it does not add a second "
            "inverse-radius determinant with equal positive weight."
        ),
        "category_warning": (
            "Qcycle duality is an intrinsic primal/dual Hodge relation on the defect cycle. "
            "No ambient operator intertwiner from that complex to the Maxwell--FP Hilbert space is defined."
        ),
    },
    "decision": {
        "reciprocal_completion_mandatory_in_current_model": False,
        "unit_radius_minimum_status": "symmetrized_candidate_not_derived_vacuum_selection",
        "new_model_required": (
            "a genuine winding sector, string-like T-duality, or an explicit ambient "
            "operator involution with the zero-mode measure included"
        ),
        "alpha_status": "no_claim",
    },
    "verdict": (
        "The ambient reciprocal bridge fails for the current Maxwell--FP field content. "
        "The intrinsic Qcycle involution does not make the RP3 x S1 product spectrum, "
        "the single relative determinant, or the scalar zero-mode measure invariant under "
        "r -> 1/r. The stable r=1 minimum of the dual-completed functional is therefore "
        "a property of an imposed symmetrization, not yet a consequence of Tome II.A. "
        "It can be revived only by deriving a genuinely new mandatory dual sector or ambient intertwiner."
    ),
}

assert not results["checks"]["ambient_low_spectra_isospectral_under_r_inversion"]
assert not results["checks"]["single_relative_response_is_dual"]
assert not results["checks"]["zero_mode_measure_is_dual"]
assert not results["checks"]["Maxwell_duality_supplies_additive_inverse_radius_sector"]
assert results["checks"]["zero_mode_scaling_identity_verified"]

Path("s2t_ambient_reciprocal_duality_bridge_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "checks": results["checks"],
            "response_asymmetry": response_asymmetry,
            "first_spectrum_test": spectrum_tests[0],
        },
        ensure_ascii=False,
        indent=2,
    )
)