import json
import math
from math import gcd
from pathlib import Path

import scipy.integrate as integrate


ALPHA_INVERSE = 137.035999177
M_MU_MEV = 105.6583755


def primitive_triplet(first, second, third):
    return gcd(gcd(abs(first), abs(second)), abs(third)) == 1


def main():
    tau_audit = json.loads(
        Path("s2t_tau_uniqueness_normalization_results.json").read_text()
    )
    scorecard = json.loads(
        Path("s2t_blind_prediction_scorecard_results.json").read_text()
    )
    tau_row = next(
        row for row in scorecard["rows"] if row["observable"] == "m_tau_MeV"
    )
    tau_control = tau_row["control"]
    tau_sigma = tau_row["control_sigma"]
    alpha = 1.0 / ALPHA_INVERSE

    rp3_constant_norm = math.pi**2
    circle_constant_norm = 2.0 * math.pi
    transverse_average = integrate.quad(
        lambda theta: math.sin(theta) ** 3 / 2.0,
        0.0,
        math.pi,
        epsabs=1e-14,
        epsrel=1e-14,
    )[0]
    gram_seed = rp3_constant_norm + circle_constant_norm + transverse_average
    declared_seed = math.pi**2 + 2.0 * math.pi + 2.0 / 3.0

    lattice_rows = []
    for first in range(-3, 4):
        for second in range(-3, 4):
            for third in range(-3, 4):
                if first == 0 or second == 0 or third == 0:
                    continue
                if not primitive_triplet(first, second, third):
                    continue
                norm = (
                    first**2 * rp3_constant_norm
                    + second**2 * circle_constant_norm
                    + third**2 * transverse_average
                )
                lattice_rows.append(
                    {
                        "coefficients": [first, second, third],
                        "norm_squared": norm,
                    }
                )
    lattice_rows.sort(key=lambda row: row["norm_squared"])
    minimum_norm = lattice_rows[0]["norm_squared"]
    minimum_rows = [
        row
        for row in lattice_rows
        if abs(row["norm_squared"] - minimum_norm) < 1e-12
    ]

    bessel_sum = tau_audit["qed_integral_audit"]["accelerated_sum"]
    raw_coefficient_magnitude = abs(bessel_sum) / math.pi
    quotient_volume_ratio = 0.5
    projection_candidates = {
        "normalized_single_channel": 1.0,
        "quotient_measure_only": quotient_volume_ratio,
        "traceless_rank9_quotient_trace": quotient_volume_ratio * 9.0,
        "full_rank10_quotient_trace": quotient_volume_ratio * 10.0,
        "rank10_plus_holonomy_line": quotient_volume_ratio * 11.0,
    }

    candidate_rows = {}
    for name, jacobian in projection_candidates.items():
        coefficient = jacobian * raw_coefficient_magnitude
        factor = gram_seed - coefficient * alpha
        mass = M_MU_MEV * factor
        candidate_rows[name] = {
            "jacobian": jacobian,
            "alpha_coefficient": coefficient,
            "factor": factor,
            "prediction_MeV": mass,
            "pull": (mass - tau_control) / tau_sigma,
        }

    rank9 = candidate_rows["traceless_rank9_quotient_trace"]
    exact_one_third = tau_audit["claimed_formula"]

    results = {
        "status": "tau_seed_gram_constructed_rank9_quotient_trace_candidate_predicts_tau_conditionally",
        "date": "2026-08-04",
        "epistemic_status": {
            "classification": "post_audit_zero_parameter_operator_candidate",
            "warning": "the rank9 quotient-trace identification was proposed after the missing Jacobian magnitude was known and is not blind evidence",
        },
        "charged_lepton_gram_seed": {
            "space": "L2(RP3) direct_sum L2(S1) direct_sum normalized transverse angular channel on S2",
            "vector": "Xi_tau=(1_RP3,1_S1,P_perp n)",
            "components": {
                "RP3_constant_norm_squared": rp3_constant_norm,
                "S1_constant_norm_squared": circle_constant_norm,
                "normalized_transverse_average": transverse_average,
            },
            "norm_squared": gram_seed,
            "declared_rho0": declared_seed,
            "identity_error": abs(gram_seed - declared_seed),
            "primitive_lattice_rule": "all three channels present with nonzero primitive integer coefficients",
            "minimum_norm_squared": minimum_norm,
            "minimum_sign_degeneracy": len(minimum_rows),
            "minimum_coefficients": [row["coefficients"] for row in minimum_rows],
            "conditionality": "the direct-sum metric is canonical once the three channels are declared, but their common coupling to the charged-lepton transition operator is not yet derived",
        },
        "projection_trace_candidate": {
            "traceless_space": "Sym^2_0(R4)",
            "rank": 9,
            "quotient_volume_ratio_RP3_over_S3": quotient_volume_ratio,
            "candidate_J_RP3": projection_candidates[
                "traceless_rank9_quotient_trace"
            ],
            "rule": "J_candidate=(Vol(RP3)/Vol(S3))*Tr(P_traceless)=9/2",
            "motivation": "the Tome already states that the relative lepton operator retains a traceless RP3 component; rank9 and the quotient factor are pre-existing geometric data",
            "open_operator_gate": "prove that the compact self-energy uses the unnormalized quotient trace over all nine strain channels rather than a normalized per-channel trace",
        },
        "predictions": candidate_rows,
        "comparison_to_claimed_one_third": {
            "claimed_alpha_coefficient": 1.0 / 3.0,
            "rank9_alpha_coefficient": rank9["alpha_coefficient"],
            "relative_coefficient_difference": rank9["alpha_coefficient"]
            / (1.0 / 3.0)
            - 1.0,
            "claimed_prediction_MeV": exact_one_third["prediction_MeV"],
            "rank9_prediction_MeV": rank9["prediction_MeV"],
            "mass_difference_MeV": rank9["prediction_MeV"]
            - exact_one_third["prediction_MeV"],
        },
        "scientific_verdict": {
            "positive": "rho0 has an exact minimal Gram-norm realization and the pre-existing traceless rank9 plus quotient volume supplies a zero-parameter Jacobian candidate",
            "prediction": "the resulting revised tau mass is 1776.90237 MeV, about -0.31 current experimental sigma",
            "negative": "neither the common charged-lepton coupling of the three Gram channels nor the use of an unnormalized nine-channel trace has been derived from the EFT vertex",
            "theory_effect": "this is the first explicit operator-level completion candidate for both tau gaps, but it remains exploratory rather than restoring theorem status",
            "next_gate": "construct the ambient charged-lepton superconnection and calculate its one-loop projection trace to decide between J=1, 1/2, or 9/2 without using m_tau",
        },
    }

    assert results["charged_lepton_gram_seed"]["identity_error"] < 1e-14
    assert len(minimum_rows) == 8
    assert all(
        all(abs(value) == 1 for value in row["coefficients"])
        for row in minimum_rows
    )
    assert abs(rank9["pull"]) < 0.4
    assert candidate_rows["normalized_single_channel"]["pull"] > 1.5

    Path("s2t_tau_operator_projection_candidate_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "gram_seed": gram_seed,
                "rank9_J": results["projection_trace_candidate"][
                    "candidate_J_RP3"
                ],
                "rank9_alpha_coefficient": rank9["alpha_coefficient"],
                "rank9_tau_prediction_MeV": rank9["prediction_MeV"],
                "rank9_pull": rank9["pull"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()