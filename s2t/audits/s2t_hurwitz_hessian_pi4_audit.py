#!/usr/bin/env python3
import json
import math
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80


def main():
    pi = mp.pi
    half_shift = mp.mpf("0.5")
    s_geo = 4 * pi**3 + pi**2 + pi
    alpha_inverse_train = mp.mpf("137.035999177")
    zeta4_half = mp.zeta(4, half_shift)
    target_coefficient = 1 / pi**4
    target_term = target_coefficient / s_geo**2

    # A_R has eigenvalues ((n+a)/R)^2. Its spectral zeta is
    # Z_A(s;R)=R^(2s) zeta(2s,a), hence logdet A_R=-Z_A'(0;R).
    zeta0_half = mp.zeta(0, half_shift)
    logdet_scale_slope = -2 * zeta0_half
    logdet_log_radius_hessian = mp.mpf("0")

    # The inverse-square trace is the first standard object carrying zeta(4,a).
    # F(R)=Tr A_R^-2=R^4 zeta(4,a). With t=log R, F''(t)=16F(t).
    inverse_square_trace_at_one = zeta4_half
    inverse_square_log_radius_hessian = 16 * zeta4_half

    candidates = {
        "direct_zeta4_moment": zeta4_half,
        "six_times_zeta4_equals_pi4": 6 * zeta4_half,
        "direct_scale_hessian_Tr_A_minus2": inverse_square_log_radius_hessian,
        "inverse_zeta4": 1 / zeta4_half,
        "inverse_direct_scale_hessian": 1 / inverse_square_log_radius_hessian,
        "normalized_inverse_one_over_6_zeta4": 1 / (6 * zeta4_half),
    }
    candidate_rows = []
    for name, coefficient in candidates.items():
        candidate_rows.append(
            {
                "name": name,
                "coefficient": float(coefficient),
                "ratio_to_required_one_over_pi4": float(
                    coefficient / target_coefficient
                ),
                "term_after_dividing_by_S2": float(coefficient / s_geo**2),
                "required_extra_multiplier": float(
                    target_coefficient / coefficient
                ),
            }
        )

    first_correction = 1 / (24 * s_geo)
    s_without_pi4 = s_geo - first_correction
    s_with_pi4 = s_without_pi4 - target_term

    # Hessians depend on the normalization of the deformation coordinate.
    # If x=c t, then d2/dx2 = c^-2 d2/dt2.
    coordinate_rescalings = []
    for scale in [mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2"), mp.pi]:
        rescaled_hessian = inverse_square_log_radius_hessian / scale**2
        coordinate_rescalings.append(
            {
                "x_equals_scale_times_logR": float(scale),
                "hessian": float(rescaled_hessian),
                "ratio_to_unscaled": float(
                    rescaled_hessian / inverse_square_log_radius_hessian
                ),
            }
        )

    required_collective_channel_count = target_coefficient ** (-1) / zeta4_half
    collective_candidates = [
        {
            "source": "single_SU5_X_block_raw_dimension",
            "channel_count": 6,
            "inverse_collective_susceptibility": float(1 / (6 * zeta4_half)),
            "matches_one_over_pi4": True,
            "gate": (
                "Raw dimension six matches algebraically, but an electromagnetic/gauge Hessian "
                "weights generator squares. The previously audited X block has subgroup indices "
                "(5/2,3/2,1), not a universal unit weight six."
            ),
        },
        {
            "source": "SU5_X_plus_conjugate_pair",
            "channel_count": 12,
            "inverse_collective_susceptibility": float(1 / (12 * zeta4_half)),
            "matches_one_over_pi4": False,
            "gate": "The charge-conjugate pair doubles the raw multiplicity and gives one half of the required coefficient.",
        },
        {
            "source": "P02_scalar_shell_rank",
            "channel_count": 10,
            "inverse_collective_susceptibility": float(1 / (10 * zeta4_half)),
            "matches_one_over_pi4": False,
            "gate": "The established P02 count is ten, not six.",
        },
        {
            "source": "symmetric_metric_strain_components_in_3D",
            "channel_count": 6,
            "inverse_collective_susceptibility": float(1 / (6 * zeta4_half)),
            "matches_one_over_pi4": True,
            "gate": (
                "Sym^2(T*) has dimension six, but the proposed constant conformal/radius "
                "deformation is a single trace direction. Summing all six strains changes the observable."
            ),
        },
    ]

    results = {
        "status": "hurwitz_half_shift_is_real_but_direct_Hessian_does_not_generate_inverse_pi4",
        "date": "2026-08-05",
        "numerical_anchor": {
            "S_geo": float(s_geo),
            "S_after_one_over_24S": float(s_without_pi4),
            "one_over_pi4_S2": float(target_term),
            "S_vac": float(s_with_pi4),
            "difference_from_train_alpha_inverse": float(
                s_with_pi4 - alpha_inverse_train
            ),
        },
        "hurwitz_identity": {
            "zeta_4_half": float(zeta4_half),
            "pi4_over_6": float(pi**4 / 6),
            "absolute_error": float(abs(zeta4_half - pi**4 / 6)),
            "identity": "zeta(4,1/2)=(2^4-1)zeta(4)=pi^4/6",
        },
        "scale_logdet_model": {
            "eigenvalues": "lambda_n(R)=((n+1/2)/R)^2",
            "spectral_zeta": "Z_A(s;R)=R^(2s) zeta(2s,1/2)",
            "zeta_0_half": float(zeta0_half),
            "logdet_slope_in_logR": float(logdet_scale_slope),
            "logdet_Hessian_in_logR": float(logdet_log_radius_hessian),
            "finding": (
                "For the pure half-integer one-dimensional tower zeta(0,1/2)=0. "
                "The zeta-regularized logdet has no scale Hessian, and zeta(4,1/2) "
                "does not appear in this derivative."
            ),
        },
        "inverse_square_trace_model": {
            "functional": "F(R)=Tr A_R^-2=R^4 zeta(4,1/2)",
            "F_at_R1": float(inverse_square_trace_at_one),
            "Hessian_in_logR_at_R1": float(
                inverse_square_log_radius_hessian
            ),
            "closed_form_Hessian": "16 zeta(4,1/2)=8 pi^4/3",
            "finding": (
                "The standard spectral functional that actually contains zeta(4,1/2) "
                "produces a direct pi^4 response, not an inverse-pi^4 response."
            ),
        },
        "coefficient_candidates": candidate_rows,
        "normalization_obstruction": {
            "direct_moment_required_multiplier": float(6 / pi**8),
            "inverse_moment_required_multiplier": float(mp.mpf(1) / 6),
            "exact_inverse_candidate": "1/[6 zeta(4,1/2)]=1/pi^4",
            "why_not_a_derivation": (
                "The reciprocal response and the factor 1/6 must be specified by the "
                "parent functional or by an inverse covariance/Legendre-dual rule. They "
                "do not follow from taking the direct Hessian."
            ),
        },
        "six_channel_inverse_susceptibility": {
            "required_channel_count": float(required_collective_channel_count),
            "identity": "[6 zeta(4,1/2)]^-1=pi^-4",
            "candidate_sources": collective_candidates,
            "status": "sharp_II_B_candidate_not_current_EM_derivation",
            "interpretation": (
                "The factor six need not be arbitrary if a parent theory supplies six equal, "
                "unit-normalized fluctuation channels and the physical correction is the inverse "
                "collective Hessian. No current II.A electromagnetic block satisfies all three conditions."
            ),
        },
        "coordinate_dependence": {
            "rule": "for x=c log R, H_x=H_logR/c^2",
            "samples": coordinate_rescalings,
            "consequence": (
                "A bare numerical Hessian coefficient is not invariant until the deformation "
                "coordinate and its kinetic norm are fixed independently."
            ),
        },
        "S_inverse_square_gate": {
            "finding": (
                "Dividing a spectral moment or Hessian by S_geo^2 is an additional response map. "
                "It is not implied by the scale derivative of logdet or Tr A^-2."
            ),
            "required_parent_statement": (
                "The theory must define S_geo as the background expectation, identify the "
                "physical correction with a normalized inverse susceptibility, and fix both "
                "the deformation norm and the factor 1/6 before alpha is used."
            ),
        },
        "comparison_with_C6": {
            "same_determinant_interpretation": (
                "If the Hessian is still the Maxwell-ghost logdet Hessian, C6 remains the "
                "relevant same-scheme calculation and the new wording does not bypass it."
            ),
            "new_functional_interpretation": (
                "If the correction is an inverse susceptibility of another spectral functional, "
                "this is a genuinely new II.B model. It must also explain why that response is "
                "combined with the independent 1/24 determinant branch."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The half-shifted zeta value is exact and suggests a sharply testable inverse-response model."
            ),
            "negative": (
                "The proposed direct-Hessian inference reverses the pi power: direct moments give "
                "pi^4, while 1/pi^4 appears only after taking a reciprocal and fixing an extra factor 1/6."
            ),
            "reopening_condition": (
                "Construct one parent action whose Legendre-dual or covariance calculation "
                "forces six equal unit-normalized channels and the response "
                "1/[6 zeta(4,1/2) S_geo^2] with a fixed deformation metric."
            ),
        },
    }

    assert abs(zeta4_half - pi**4 / 6) < mp.mpf("1e-70")
    assert zeta0_half == 0
    assert logdet_log_radius_hessian == 0
    assert abs(candidates["normalized_inverse_one_over_6_zeta4"] - target_coefficient) < mp.mpf("1e-70")
    assert abs(s_with_pi4 - mp.mpf("137.035999173522")) < mp.mpf("1e-12")

    Path("s2t_hurwitz_hessian_pi4_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "zeta4_half": results["hurwitz_identity"]["zeta_4_half"],
                "logdet_scale_hessian": results["scale_logdet_model"]["logdet_Hessian_in_logR"],
                "direct_inverse_square_trace_hessian": results["inverse_square_trace_model"]["Hessian_in_logR_at_R1"],
                "direct_zeta4_ratio_to_target": candidate_rows[0]["ratio_to_required_one_over_pi4"],
                "inverse_zeta4_ratio_to_target": candidate_rows[3]["ratio_to_required_one_over_pi4"],
                "required_collective_channels": float(required_collective_channel_count),
                "exact_only_after_factor": "1/[6 zeta(4,1/2)]",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()