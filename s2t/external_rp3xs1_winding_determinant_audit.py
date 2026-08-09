import json
from pathlib import Path

import mpmath as mp


mp.mp.dps = 60


def untwisted_coexact_modes(m_max):
    # n=2m-1 on untwisted RP3, so rho=n+1=2m and d=2n(n+2)=8m^2-2.
    for m in range(1, m_max + 1):
        yield {
            "m": m,
            "n": 2 * m - 1,
            "rho": mp.mpf(2 * m),
            "multiplicity": 8 * m * m - 2,
        }


def bessel_inner(rho, q_max=200, tolerance=mp.mpf("1e-55")):
    total = mp.mpf("0")
    used = 0
    for q in range(1, q_max + 1):
        term = mp.besselk(1, 2 * mp.pi * q * rho) / q
        total += term
        used = q
        if abs(term) < tolerance:
            break
    return total, used


def evaluate(m_max=40):
    bessel_positive = mp.mpf("0")
    logdet_winding = mp.mpf("0")
    rows = []
    for mode in untwisted_coexact_modes(m_max):
        inner, q_used = bessel_inner(mode["rho"])
        bessel_contribution = mode["multiplicity"] * mode["rho"] * inner
        logdet_contribution = (
            2
            * mode["multiplicity"]
            * mp.log(1 - mp.e ** (-2 * mp.pi * mode["rho"]))
        )
        bessel_positive += bessel_contribution
        logdet_winding += logdet_contribution
        rows.append(
            {
                "m": mode["m"],
                "n": mode["n"],
                "rho": float(mode["rho"]),
                "multiplicity": mode["multiplicity"],
                "q_used": q_used,
                "positive_Bessel_T_contribution": float(bessel_contribution),
                "logdet_winding_contribution": float(logdet_contribution),
            }
        )
    return bessel_positive, logdet_winding, rows


T_bessel, logdet_winding, rows = evaluate()
casimir_energy_nonlocal = -T_bessel / mp.pi
bosonic_gamma_winding = logdet_winding / 2

internal = json.loads(Path("s2t_coexact_tower_results.json").read_text())
internal_T = mp.mpf(str(internal["dimensionless_positive_sum"]["rp3_projected"]))

rho_control = mp.mpf("2")
product_identity_left = 4 * mp.sinh(mp.pi * rho_control) ** 2
product_identity_right = mp.e ** (2 * mp.pi * rho_control) * (
    1 - mp.e ** (-2 * mp.pi * rho_control)
) ** 2

results = {
    "status": "external_RP3xS1_winding_objects_separated_internal_T_reproduced",
    "date": "2026-08-03",
    "conventions": {
        "circle_length": "2*pi*R1",
        "radius_ratio": "R1/R3=1",
        "untwisted_RP3_coexact_spectrum": "rho=2m, multiplicity=8m^2-2, m>=1",
        "local_subtraction": "zero-winding/Weyl term removed",
    },
    "derived_objects": {
        "positive_Bessel_sum_T": (
            "sum d*rho*sum_{q>=1} K1(2*pi*q*rho)/q"
        ),
        "casimir_energy_nonlocal": "E_nonlocal=-T/pi for E(s)=1/2 sum_Z (m^2+rho^2)^(1/2-s)",
        "logdet_winding": "2 sum d*log(1-exp(-2*pi*rho))",
        "bosonic_effective_action_winding": "Gamma_winding=1/2 logdet_winding",
    },
    "numbers": {
        "internal_T_coex_RP3": float(internal_T),
        "independent_T_coex_RP3": float(T_bessel),
        "T_absolute_difference": float(abs(T_bessel - internal_T)),
        "casimir_energy_nonlocal": float(casimir_energy_nonlocal),
        "logdet_winding": float(logdet_winding),
        "bosonic_Gamma_winding": float(bosonic_gamma_winding),
        "abs_Gamma_over_T": float(abs(bosonic_gamma_winding) / T_bessel),
        "first_mode_fraction_T": float(
            mp.mpf(str(rows[0]["positive_Bessel_T_contribution"])) / T_bessel
        ),
        "first_mode_fraction_logdet": float(
            mp.mpf(str(rows[0]["logdet_winding_contribution"])) / logdet_winding
        ),
    },
    "controls": {
        "first_mode_product_identity_relative_error": float(
            abs(product_identity_left - product_identity_right) / product_identity_left
        ),
        "T_reproduced_within_1e_18": abs(T_bessel - internal_T) < mp.mpf("1e-18"),
        "Bessel_and_logdet_are_not_same_object": abs(
            abs(bosonic_gamma_winding) / T_bessel - 1
        ) > mp.mpf("0.1"),
    },
    "first_modes": rows[:8],
    "interpretation": {
        "positive_result": (
            "The internal T_coex value is numerically correct for the declared positive K1 Bessel sum."
        ),
        "normalization_correction": (
            "For the Epstein Casimir-energy continuation the physical nonlocal contribution is -T/pi, "
            "not T itself."
        ),
        "determinant_distinction": (
            "The finite winding part of log det(-d_tau^2+rho^2) is instead "
            "2 log(1-exp(-2*pi*rho)) per mode. Its bosonic half is about 1.374 times T in magnitude."
        ),
        "theory_effect": (
            "The old Bessel number remains a valid Casimir-energy diagnostic, but it cannot be called the "
            "RP3xS1 determinant residue without an additional derivation connecting the energy functional to S_vac."
        ),
    },
    "theory_status": {
        "coexact_nonlocal_tail": "independently_confirmed_nonzero",
        "internal_T_numeric_value": "confirmed",
        "T_as_direct_logdet_residue": "not_confirmed_objects_differ",
        "pi4_absorption_normalization": "further_weakened_requires_new_bridge",
        "S_vac": "remains_conditional",
    },
    "next_steps": [
        "state whether S_vac is defined from Casimir energy or from the Euclidean one-loop effective action",
        "derive the exact dimensional prefactor and sign from that chosen functional",
        "include the scalar half-determinant winding tower in the same convention",
        "only then compare the full Maxwell-FP result with the pi^-4 term",
    ],
    "verdict": (
        "The internal value T_coex^RP3=1.5227161455e-5 is independently reproduced with the untwisted spectrum "
        "and high-precision Bessel functions. However, T is the positive kernel used in a Casimir-energy Epstein "
        "continuation. The corresponding nonlocal energy is -T/pi. The finite winding part of the Euclidean log "
        "determinant is a different quantity, 2 sum d log(1-exp(-2*pi*rho)), whose bosonic half equals "
        "-2.0924455472e-5. Therefore the nonzero coexact obstruction is robust, but the prior identification of T "
        "with a determinant residue requires a new functional and normalization bridge and cannot support exact pi^-4."
    ),
}


assert results["controls"]["T_reproduced_within_1e_18"]
assert results["controls"]["first_mode_product_identity_relative_error"] < 1e-50
assert results["controls"]["Bessel_and_logdet_are_not_same_object"]

Path("external_rp3xs1_winding_determinant_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps(results["numbers"], indent=2, ensure_ascii=False))
print(results["status"])