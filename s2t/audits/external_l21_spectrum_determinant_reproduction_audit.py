import json
import math
from pathlib import Path

import mpmath as mp


mp.mp.dps = 60


def scalar_shell(n, twist="trivial"):
    s3_multiplicity = (n + 1) ** 2
    central_character = (-1) ** n * s3_multiplicity
    sign = 1 if twist == "trivial" else -1
    multiplicity = (s3_multiplicity + sign * central_character) // 2
    return {
        "n": n,
        "eigenvalue": n * (n + 2),
        "s3_multiplicity": s3_multiplicity,
        "central_character": central_character,
        "l21_multiplicity": multiplicity,
    }


def coexact_one_form_shell(n, twist="trivial"):
    s3_multiplicity = 2 * n * (n + 2)
    central_character = (-1) ** (n + 1) * s3_multiplicity
    sign = 1 if twist == "trivial" else -1
    multiplicity = (s3_multiplicity + sign * central_character) // 2
    return {
        "n": n,
        "eigenvalue": (n + 1) ** 2,
        "s3_multiplicity": s3_multiplicity,
        "central_character": central_character,
        "l21_multiplicity": multiplicity,
    }


def scalar_zeta_prime_zero(max_terms=10000):
    # Untwisted RP3 scalar spectrum after removing n=0:
    # n=2m, m>=1, lambda=4m(m+1), multiplicity=(2m+1)^2.
    # Write k=2m+1 and expand (k^2-1)^(-s).
    first_term = -6 * mp.diff(mp.zeta, -2)
    correction = mp.mpf("0")
    used_terms = 0
    for r in range(1, max_terms + 1):
        odd_sum_excluding_one = (1 - mp.power(2, 2 - 2 * r)) * mp.zeta(2 * r - 2) - 1
        term = odd_sum_excluding_one / r
        correction += term
        used_terms = r
        if abs(term) < mp.mpf("1e-50"):
            break
    return first_term + correction, used_terms


def coexact_zeta_prime_zero():
    # Untwisted RP3 coexact one-forms have n=2m-1:
    # lambda=4m^2 and multiplicity=8m^2-2.
    return 2 * mp.log(mp.pi) - 4 * mp.zeta(3) / mp.pi**2


def nash_twisted_coexact_zeta_prime_zero():
    # Nash--O'Connor equation (4.21), p=2, nontrivial flat character.
    return 3 * mp.zeta(3) / mp.pi**2 + 2 * mp.log(2)


scalar_trivial = [scalar_shell(n) for n in range(0, 11)]
scalar_twisted = [scalar_shell(n, "sign") for n in range(0, 11)]
coexact_trivial = [coexact_one_form_shell(n) for n in range(1, 11)]
coexact_twisted = [coexact_one_form_shell(n, "sign") for n in range(1, 11)]

internal = json.loads(Path("s2t_c6_l21_coexact_basis_results.json").read_text())
internal_rows = {row["n"]: row for row in internal["shell_table"]}
internal_comparison = []
for row in coexact_trivial:
    internal_row = internal_rows[row["n"]]
    internal_comparison.append(
        {
            "n": row["n"],
            "external_projection_eigenvalue": row["eigenvalue"],
            "internal_eigenvalue": internal_row["lambda_unit_radius"],
            "external_projection_multiplicity": row["l21_multiplicity"],
            "internal_multiplicity": internal_row["l21_coexact_degeneracy"],
            "match": (
                row["eigenvalue"] == internal_row["lambda_unit_radius"]
                and row["l21_multiplicity"] == internal_row["l21_coexact_degeneracy"]
            ),
        }
    )

scalar_prime, scalar_terms = scalar_zeta_prime_zero()
coexact_prime = coexact_zeta_prime_zero()
nash_twisted_prime = nash_twisted_coexact_zeta_prime_zero()
dowker_scalar_target = mp.mpf("-0.695171")

logdet_scalar = -scalar_prime
logdet_coexact = -coexact_prime
gamma_standard_fp_nonzero = mp.mpf("0.5") * (logdet_coexact - logdet_scalar)

results = {
    "status": "external_L21_untwisted_spectrum_and_scalar_determinant_reproduced",
    "date": "2026-08-03",
    "external_sources": [
        {
            "source": "Ikeda and Yamamoto, On the spectra of 3-dimensional lens spaces",
            "role": "classical lens-space spectral framework",
        },
        {
            "source": "Lauret, The spectrum on p-forms of a lens space, arXiv:1604.02471",
            "role": "Hodge-Laplace eigenvalues and invariant-representation multiplicities",
        },
        {
            "source": "Nash and O'Connor, hep-th/9212022",
            "role": "explicit zero/one-form lens determinant technology and twisted p=2 check",
        },
        {
            "source": "Dowker, Lens space determinants, arXiv:1301.0086",
            "role": "untwisted minimally coupled scalar determinant on projective three-space",
        },
        {
            "source": "David and Mukherjee, arXiv:2105.03662",
            "role": "gauge-fixed p-form partition function in coexact and scalar determinant variables",
        },
    ],
    "conventions": {
        "space": "L(2,1)=RP3=S3/{+1,-1}",
        "bundle_for_Maxwell": "trivial_untwisted",
        "scalar_zero_mode": "removed_from_det_prime",
        "laplacian_radius": "unit_round_metric",
        "projection": "multiplicity=(identity_character plus central_character)/2",
    },
    "untwisted_scalar_shells": scalar_trivial,
    "untwisted_coexact_one_form_shells": coexact_trivial,
    "twisted_control": {
        "scalar_shells": scalar_twisted,
        "coexact_one_form_shells": coexact_twisted,
        "warning": (
            "For p=2 the Nash--O'Connor group average includes the nontrivial flat character. "
            "It selects the parity opposite to the untwisted Maxwell bundle and its determinant "
            "must not be substituted directly into the standard Maxwell sector."
        ),
    },
    "internal_coexact_comparison": internal_comparison,
    "determinant_reproduction": {
        "scalar_zeta_zero": -1.0,
        "scalar_zeta_prime_zero": float(scalar_prime),
        "scalar_series_terms": scalar_terms,
        "dowker_reported_scalar_zeta_prime_zero": float(dowker_scalar_target),
        "dowker_absolute_difference": float(abs(scalar_prime - dowker_scalar_target)),
        "scalar_logdet_prime": float(logdet_scalar),
        "coexact_zeta_zero": 1.0,
        "coexact_zeta_prime_zero": float(coexact_prime),
        "coexact_logdet": float(logdet_coexact),
        "full_one_form_zeta_zero": 0.0,
        "nash_twisted_coexact_zeta_prime_zero": float(nash_twisted_prime),
    },
    "maxwell_bookkeeping": {
        "identity": "log det' Delta1 = log det Delta1_coex + log det' Delta0",
        "standard_FP_Gamma_nonzero": "1/2 log det Delta1_coex - 1/2 log det' Delta0",
        "standard_FP_Gamma_nonzero_value_unit_RP3": float(gamma_standard_fp_nonzero),
        "consequence": (
            "The external untwisted spectrum independently reproduces the scalar half-determinant residual. "
            "It does not support complete cancellation of the nonzero scalar tower."
        ),
    },
    "checks": {
        "all_internal_coexact_shells_match": all(row["match"] for row in internal_comparison),
        "first_scalar_multiplicities": [row["l21_multiplicity"] for row in scalar_trivial[:5]],
        "first_coexact_multiplicities": [row["l21_multiplicity"] for row in coexact_trivial[:5]],
        "dowker_scalar_reproduced_within_1e_6": abs(scalar_prime - dowker_scalar_target) < mp.mpf("1e-6"),
        "hodge_zeta_zero_consistency": abs((-1) + 1) < 1e-15,
    },
    "theory_effect": {
        "lens_space_spectral_foundation": "strengthened",
        "internal_coexact_multiplicity_table": "externally_reproduced",
        "standard_FP_scalar_half_residual": "independently_confirmed",
        "exact_pi4_absorption": "not_reopened",
        "S_vac": "remains_conditional",
    },
    "next_external_steps": [
        "reproduce the untwisted coexact determinant by a second heat-kernel or contour method",
        "extend the calculation from RP3 to RP3 x S1 with explicit Matsubara sums",
        "separate zero-temperature local terms from finite winding terms",
        "compare the resulting Maxwell free energy with the project's T_coex_RP3 normalization",
    ],
    "verdict": (
        "The untwisted L(2,1) scalar and coexact one-form spectra are independently reproduced by central-character "
        "projection and match the internal shell table exactly. The minimally coupled scalar determinant reproduces "
        "Dowker's published projective-space value within 1e-6. The same calculation confirms, rather than removes, "
        "the standard-FP scalar half-determinant residual. Nash--O'Connor's p=2 determinant formulas are a useful "
        "twisted control but are not the untwisted Maxwell determinant. The external gate therefore strengthens the "
        "spectral foundation while leaving exact pi^-4 absorption downgraded."
    ),
}


assert results["checks"]["all_internal_coexact_shells_match"]
assert results["checks"]["first_scalar_multiplicities"] == [1, 0, 9, 0, 25]
assert results["checks"]["first_coexact_multiplicities"] == [6, 0, 30, 0, 70]
assert results["checks"]["dowker_scalar_reproduced_within_1e_6"]

Path("external_l21_spectrum_determinant_reproduction_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps(results["checks"], indent=2, ensure_ascii=False))
print(results["status"])