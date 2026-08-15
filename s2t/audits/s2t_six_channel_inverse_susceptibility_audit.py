#!/usr/bin/env python3
import json
import math
from pathlib import Path


def main():
    pi = math.pi
    zeta4_half = pi**4 / 6.0
    channel_count = 6
    target = 1.0 / pi**4

    # Six independent real Gaussian channels with ordinary component sum:
    # Gamma=1/2 zeta sum_i x_i^2. For qbar=(1/N)sum_i x_i,
    # Var(qbar)=1/(N zeta).
    ordinary_mode_variance = 1.0 / zeta4_half
    ordinary_average_variance = ordinary_mode_variance / channel_count

    # With normalized trace in the action:
    # Gamma=1/2 zeta (1/N)sum_i x_i^2. Each mode variance becomes N/zeta,
    # so Var(qbar)=1/zeta and the rank factor cancels.
    normalized_trace_mode_variance = channel_count / zeta4_half
    normalized_trace_average_variance = 1.0 / zeta4_half

    su5 = json.loads(
        Path("s2t_su5_rank_action_gate_results.json").read_text(encoding="utf-8")
    )
    mixed = su5["mixed_block"]["single_complex_block"]
    mixed_pair = su5["mixed_block"]["charge_conjugate_pair_indices"]

    candidates = [
        {
            "candidate": "Lambda2_of_four_dimensional_carrier",
            "raw_channel_count": math.comb(4, 2),
            "half_integer_tower": False,
            "equal_unit_EM_weights": False,
            "statistics": "bosonic",
            "reality_or_constraint": (
                "A curvature two-form has six pointwise components, but F=dA obeys the "
                "Bianchi constraint and the Maxwell partition function reduces to Hodge "
                "determinants rather than six unconstrained scalar towers. Gauge/ghost S1 modes are periodic."
            ),
            "passes": False,
        },
        {
            "candidate": "Sym2_metric_strains_on_RP3",
            "raw_channel_count": math.comb(3 + 1, 2),
            "half_integer_tower": False,
            "equal_unit_EM_weights": False,
            "statistics": "bosonic",
            "reality_or_constraint": (
                "Sym2 has dimension six, but a constant conformal deformation is one trace "
                "direction. Summing all six strains is not the proposed radius Hessian."
            ),
            "passes": False,
        },
        {
            "candidate": "single_complex_SU5_X_block",
            "raw_channel_count": mixed["dimension"],
            "half_integer_tower": False,
            "equal_unit_EM_weights": False,
            "statistics": "bosonic gauge block",
            "physical_indices": {
                "U1_GUT": mixed["U1_GUT_index"],
                "SU2": mixed["SU2_Dynkin_index"],
                "SU3": mixed["SU3_Dynkin_index"],
            },
            "reality_or_constraint": (
                "One complex (3,2) block has raw dimension six, but a real adjoint gauge "
                "field contains the conjugate block as well. Gauge Hessians use Dynkin indices, not raw rank."
            ),
            "passes": False,
        },
        {
            "candidate": "SU5_X_plus_conjugate",
            "raw_channel_count": 12,
            "half_integer_tower": False,
            "equal_unit_EM_weights": False,
            "statistics": "real bosonic adjoint pair",
            "physical_indices": {
                "U1_GUT": mixed_pair["U1_GUT_index"],
                "SU2": mixed_pair["SU2_Dynkin_index"],
                "SU3": mixed_pair["SU3_Dynkin_index"],
            },
            "reality_or_constraint": "Reality restores twelve real broken generators, not six equal channels.",
            "passes": False,
        },
        {
            "candidate": "one_generation_Q_left_block",
            "raw_channel_count": 6,
            "half_integer_tower": True,
            "equal_unit_EM_weights": False,
            "statistics": "chiral Grassmann",
            "electromagnetic_charge_square_sum": 3
            * ((2.0 / 3.0) ** 2 + (-1.0 / 3.0) ** 2),
            "reality_or_constraint": (
                "The six Weyl components can inherit the antiperiodic spin tower, but their "
                "electromagnetic weights sum to 5/3 rather than six. Three generations give "
                "eighteen components, and Grassmann covariance is not a positive bosonic susceptibility."
            ),
            "passes": False,
        },
        {
            "candidate": "abstract_six_equal_antiperiodic_scalar_channels",
            "raw_channel_count": 6,
            "half_integer_tower": True,
            "equal_unit_EM_weights": True,
            "statistics": "bosonic auxiliary",
            "reality_or_constraint": (
                "This realizes the identity exactly, but no such six-channel auxiliary block "
                "is present in the frozen II.A field content."
            ),
            "passes": "algebraically_only",
        },
    ]

    # Two ways to turn the covariance into a correction.
    variance_observable_coefficient = ordinary_average_variance
    # For Gamma(q)=H q^2/2 + J q, eliminating q gives -J^2/(2H).
    collective_hessian = channel_count * zeta4_half
    required_linear_source = math.sqrt(2.0)  # J=sqrt(2)/S gives -1/(H S^2).

    results = {
        "status": "six_channel_inverse_identity_is_exact_but_no_current_carrier_passes_statistics_boundary_weight_and_trace_gates",
        "date": "2026-08-05",
        "exact_identity": {
            "channel_count": channel_count,
            "zeta4_half": zeta4_half,
            "collective_hessian": collective_hessian,
            "inverse_collective_hessian": 1.0 / collective_hessian,
            "target_one_over_pi4": target,
            "absolute_error": abs(1.0 / collective_hessian - target),
        },
        "gaussian_average_model": {
            "ordinary_trace_action": "Gamma=1/2 zeta sum_i x_i^2",
            "collective_coordinate": "qbar=(1/6) sum_i x_i",
            "single_mode_variance": ordinary_mode_variance,
            "qbar_variance": ordinary_average_variance,
            "matches_one_over_pi4": abs(ordinary_average_variance - target) < 1e-14,
            "interpretation": (
                "With an unnormalized component sum, the arithmetic mean of six independent "
                "equal channels has the desired variance."
            ),
        },
        "trace_normalization_gate": {
            "normalized_trace_action": "Gamma=1/2 zeta tau6(x^2)",
            "single_mode_variance": normalized_trace_mode_variance,
            "qbar_variance": normalized_trace_average_variance,
            "ratio_to_target": normalized_trace_average_variance / target,
            "finding": (
                "The normalized trace cancels the multiplicity-six suppression and gives "
                "6/pi^4. The exact route therefore requires an ordinary component sum or an "
                "independently fixed overall trace normalization."
            ),
        },
        "carrier_scan": candidates,
        "response_map_gate": {
            "variance_readout": (
                "If the observable contains -qbar^2/S_geo^2 with unit coefficient, Gaussian "
                "averaging gives exactly -1/(pi^4 S_geo^2). The unit quadratic readout is a new coupling."
            ),
            "auxiliary_elimination": {
                "action": "Gamma(q)=H q^2/2 + J q/S_geo",
                "on_shell_correction": "-J^2/(2 H S_geo^2)",
                "required_J": required_linear_source,
                "finding": (
                    "A linear-source derivation requires J=sqrt(2), another normalization "
                    "that must be fixed by the parent action."
                ),
            },
            "sign": (
                "The negative sign follows only after choosing a variance subtraction or "
                "integrating out a linearly sourced stable mode; it is not supplied by the zeta identity alone."
            ),
        },
        "boundary_and_statistics_gate": {
            "half_shift_requirement": (
                "zeta(4,1/2) requires antiperiodic/half-integer modes in the relevant direction."
            ),
            "current_EM_boundary_condition": "periodic integer Maxwell/ghost modes on S1",
            "consequence": (
                "Raw bosonic sixes in Lambda2 or SU5 gauge blocks do not carry the required "
                "half-integer tower. The natural half-shifted six Q components are fermionic "
                "and not equally electromagnetically weighted."
            ),
        },
        "unified_parent_action_gate": {
            "ordinary_vs_normalized_trace": "unresolved and normalization-sensitive",
            "combination_with_one_over_24": (
                "The 1/24 branch is a periodic Maxwell-ghost finite part, whereas the six-channel "
                "candidate needs a half-shifted auxiliary sector. A graded parent action must fix "
                "their relative sign and normalization before alpha is used."
            ),
            "passes_two_sector_requirement": False,
        },
        "scientific_verdict": {
            "positive": (
                "The six-channel Gaussian average is an explicit model, not merely arithmetic: "
                "ordinary-trace covariance of the channel mean equals pi^-4 exactly."
            ),
            "negative": (
                "Every natural six-dimensional carrier currently in the project fails at least "
                "one of the half-shift, equal-weight, reality/gauge, statistics or trace-normalization gates."
            ),
            "reopening_condition": (
                "Derive a bosonic six-channel antiperiodic auxiliary block with ordinary trace "
                "normalization and a unit variance readout, or an equivalent graded parent action, "
                "before comparison with alpha."
            ),
        },
    }

    assert abs(collective_hessian - pi**4) < 1e-12
    assert abs(ordinary_average_variance - target) < 1e-14
    assert abs(normalized_trace_average_variance / target - 6.0) < 1e-12
    assert mixed["dimension"] == 6
    assert mixed_pair == {
        "SU3_Dynkin_index": 2.0,
        "SU2_Dynkin_index": 3.0,
        "U1_GUT_index": 5.0,
    }
    assert not any(candidate["passes"] is True for candidate in candidates)

    Path("s2t_six_channel_inverse_susceptibility_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "collective_hessian": collective_hessian,
                "ordinary_average_variance": ordinary_average_variance,
                "normalized_trace_average_variance": normalized_trace_average_variance,
                "normalized_trace_ratio_to_target": normalized_trace_average_variance / target,
                "candidate_count": len(candidates),
                "physical_pass_count": sum(candidate["passes"] is True for candidate in candidates),
                "algebraic_only": [
                    candidate["candidate"]
                    for candidate in candidates
                    if candidate["passes"] == "algebraically_only"
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()