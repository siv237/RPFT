import json
import math
from pathlib import Path

import numpy as np


ALPHA_INVERSE = 137.035999177
M_MU_MEV = 105.6583755


def tau_prediction(seed, loop_coefficient, control, sigma):
    alpha = 1.0 / ALPHA_INVERSE
    mass = M_MU_MEV * (seed - loop_coefficient * alpha)
    return {
        "alpha_coefficient": loop_coefficient,
        "prediction_MeV": mass,
        "pull": (mass - control) / sigma,
    }


def main():
    tau_loop = json.loads(
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
    bessel_sum = tau_loop["qed_integral_audit"]["accelerated_sum"]
    raw_loop_coefficient = abs(bessel_sum) / math.pi

    rank = 9
    identity = np.eye(rank)
    antipodal_action = np.eye(rank)
    quotient_projector = 0.5 * (identity + antipodal_action)
    quotient_trace = float(np.trace(quotient_projector))

    unnormalized_vertex = identity
    unnormalized_hs_norm_squared = float(
        np.trace(unnormalized_vertex.T @ unnormalized_vertex)
    )
    canonical_vertex = unnormalized_vertex / math.sqrt(
        unnormalized_hs_norm_squared
    )
    canonical_hs_norm_squared = float(
        np.trace(canonical_vertex.T @ canonical_vertex)
    )

    volume_cover = 2.0 * math.pi**2
    volume_quotient = math.pi**2
    cover_constant = 1.0 / math.sqrt(volume_cover)
    quotient_constant = 1.0 / math.sqrt(volume_quotient)
    lifted_quotient_to_cover_ratio = quotient_constant / cover_constant
    quotient_normalized_integral = volume_quotient * quotient_constant**2

    raw_seed = math.pi**2 + 2.0 * math.pi + 2.0 / 3.0
    normalized_seed = 1.0 + 1.0 + 2.0 / 3.0

    predictions = {
        "canonical_single_collective_mode_J_1": tau_prediction(
            raw_seed, raw_loop_coefficient, tau_control, tau_sigma
        ),
        "incorrect_half_rank_J_9_over_2": tau_prediction(
            raw_seed,
            0.5 * rank * raw_loop_coefficient,
            tau_control,
            tau_sigma,
        ),
        "nine_independent_channels_J_9": tau_prediction(
            raw_seed,
            rank * raw_loop_coefficient,
            tau_control,
            tau_sigma,
        ),
    }

    results = {
        "status": "canonical_ambient_trace_rejects_rank9_half_candidate_tau_relation_remains_conditional",
        "date": "2026-08-04",
        "quotient_trace": {
            "space": "even traceless Sym^2_0(R4) sector",
            "rank": rank,
            "antipodal_action": "+I because quadratic strains are even",
            "projector": "P_plus=(I+U)/2",
            "trace_P_plus": quotient_trace,
            "naive_half_rank": rank / 2.0,
            "finding": "the image term equals the identity term on the even sector, so the quotient trace is 9 rather than 9/2",
        },
        "mode_normalization": {
            "Vol_S3": volume_cover,
            "Vol_RP3": volume_quotient,
            "normalized_cover_constant": cover_constant,
            "normalized_quotient_constant": quotient_constant,
            "lifted_quotient_mode_relative_to_cover_mode": lifted_quotient_to_cover_ratio,
            "integral_RP3_of_normalized_mode_squared": quotient_normalized_integral,
            "finding": "the half-volume is canceled by the sqrt(2) normalization of the quotient mode in a quadratic matrix element",
        },
        "collective_vertex_normalization": {
            "unnormalized_vertex": "P_tr=I_9",
            "unnormalized_HS_norm_squared": unnormalized_hs_norm_squared,
            "canonical_vertex": "P_tr/sqrt(Tr P_tr^2)=I_9/3",
            "canonical_HS_norm_squared": canonical_hs_norm_squared,
            "single_collective_mode_loop_trace": canonical_hs_norm_squared,
            "nine_independent_channel_loop_trace": unnormalized_hs_norm_squared,
            "finding": "a canonically normalized single collective field gives J=1; nine independent fields give J=9; neither gives 9/2",
        },
        "gram_seed_normalization": {
            "background_unnormalized_seed": raw_seed,
            "canonical_normalized_constant_mode_seed": normalized_seed,
            "finding": "pi^2+2pi arises from unnormalized background geometry modes; canonical charged-lepton wavefunctions would replace the two volume norms by one each",
        },
        "tau_predictions": predictions,
        "scientific_verdict": {
            "rank9_half_candidate": "closed negatively in the minimal normalized ambient trace",
            "canonical_result": "J=1 predicts m_tau=1777.06887 MeV, about +1.54 sigma",
            "remaining_relation": "the original low-complexity tau formula remains numerically strong, but neither its seed nor alpha/3 coefficient follows from canonical mode normalization",
            "reopen_condition": "derive a noncanonical stiffness, boundary measure, or multiplicity operator from the charged-lepton action that produces a fixed weight other than 1 or 9 before comparison",
            "program_effect": "do not use the rank9/2 postdiction as evidence or as the Higgs-scale foundation",
        },
    }

    assert abs(quotient_trace - 9.0) < 1e-14
    assert abs(canonical_hs_norm_squared - 1.0) < 1e-14
    assert abs(quotient_normalized_integral - 1.0) < 1e-14
    assert abs(predictions["canonical_single_collective_mode_J_1"]["pull"]) < 2.0
    assert predictions["nine_independent_channels_J_9"]["pull"] < -2.0

    Path("s2t_tau_ambient_trace_normalization_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "quotient_trace": quotient_trace,
                "canonical_collective_trace": canonical_hs_norm_squared,
                "rank9_half_candidate": rank / 2.0,
                "canonical_tau_prediction": predictions[
                    "canonical_single_collective_mode_J_1"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()