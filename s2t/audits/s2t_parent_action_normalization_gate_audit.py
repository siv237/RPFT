import json
import math
from pathlib import Path


PI = math.pi
ALPHA_INVERSE = 137.035999177
M_MU_MEV = 105.6583755
M_TAU_CONTROL_MEV = 1776.93
M_TAU_SIGMA_MEV = 0.09


def spectral_hessian_weights(kind, parameter=None, mass_squared=1.0):
    x = mass_squared
    if kind == "affine":
        derivative_at_zero = 1.0
        derivative_at_x = 1.0
        second_at_x = 0.0
    elif kind == "heat":
        rate = parameter
        derivative_at_zero = -rate
        derivative_at_x = -rate * math.exp(-rate * x)
        second_at_x = rate**2 * math.exp(-rate * x)
    elif kind == "resolvent":
        power = parameter
        derivative_at_zero = -power
        derivative_at_x = -power * (1.0 + x) ** (-power - 1.0)
        second_at_x = power * (power + 1.0) * (1.0 + x) ** (-power - 2.0)
    else:
        raise ValueError(kind)

    kernel_weight = 2.0 * derivative_at_zero
    massive_weight = 2.0 * derivative_at_x + 4.0 * x * second_at_x
    return {
        "kind": kind,
        "parameter": parameter,
        "kernel_weight": kernel_weight,
        "massive_weight": massive_weight,
        "difference": massive_weight - kernel_weight,
        "equal_weights": abs(massive_weight - kernel_weight) < 1e-12,
    }


def tau_prediction(seed, loop_coefficient):
    alpha = 1.0 / ALPHA_INVERSE
    mass = M_MU_MEV * (seed - loop_coefficient * alpha)
    return {
        "seed": seed,
        "loop_coefficient": loop_coefficient,
        "prediction_MeV": mass,
        "pull": (mass - M_TAU_CONTROL_MEV) / M_TAU_SIGMA_MEV,
    }


def main():
    tau_loop = json.loads(
        Path("s2t_tau_uniqueness_normalization_results.json").read_text()
    )
    bessel_sum = tau_loop["qed_integral_audit"]["accelerated_sum"]
    raw_loop_coefficient = abs(bessel_sum) / PI

    vol_rp3 = PI**2
    length_s1 = 2.0 * PI
    transverse_average = 2.0 / 3.0
    raw_tau_seed = vol_rp3 + length_s1 + transverse_average
    canonical_tau_seed = 1.0 + 1.0 + transverse_average
    required_projection_weight = (1.0 / 3.0) / raw_loop_coefficient

    neutrino_norm = 23.0 + 1.0 / PI
    spectral_family = [
        spectral_hessian_weights("affine"),
        spectral_hessian_weights("heat", 1.0),
        spectral_hessian_weights("heat", 2.0),
        spectral_hessian_weights("resolvent", 3.0),
        spectral_hessian_weights("resolvent", 4.0),
    ]

    sector_gates = {
        "neutrino_collective_stiffness": {
            "target": "23+pi^-1",
            "parent_action_value": neutrino_norm,
            "passes_canonical_configuration_metric": True,
            "passes_generic_spectral_kernel": False,
            "reason": (
                "The rank-23 normalized zero-form and the unit-period kernel one-form are "
                "orthogonal in one trace-Hodge norm, but generic Tr f(D^2) Hessians split "
                "their weights around a nonzero heavy background."
            ),
        },
        "charged_lepton_seed": {
            "target": raw_tau_seed,
            "canonical_parent_value": canonical_tau_seed,
            "passes": False,
            "reason": (
                "For normalized constant lepton modes, the RP3 and S1 volume factors cancel "
                "from quadratic matrix elements; their contributions are 1 and 1 rather than "
                "pi^2 and 2pi."
            ),
        },
        "charged_lepton_loop": {
            "target_coefficient": 1.0 / 3.0,
            "canonical_single_vertex_coefficient": raw_loop_coefficient,
            "required_extra_weight": required_projection_weight,
            "passes": False,
            "reason": (
                "A canonically normalized collective vertex supplies unit trace. The displayed "
                "Bessel integral therefore gives |I_tau|/pi, while 1/3 requires an additional "
                "noncanonical projection weight."
            ),
        },
        "electromagnetic_exact_closure": {
            "passes": False,
            "reason": (
                "The already completed same-scheme Maxwell-ghost audit does not derive the exact "
                "pi^-4 absorption term from the canonical Hessian."
            ),
        },
        "higgs_absolute_bridge": {
            "passes": False,
            "reason": (
                "Its absolute scale inherits the conditional tau seed and electromagnetic vacuum "
                "normalization, so it is not an independent second parent-action sector."
            ),
        },
    }

    passed_predictive_sectors = [
        name
        for name, gate in sector_gates.items()
        if gate.get("passes", gate.get("passes_canonical_configuration_metric", False))
    ]

    results = {
        "status": "minimal_unified_parent_action_gate_negative_only_neutrino_metric_survives",
        "date": "2026-08-04",
        "frozen_parent_model": {
            "carrier": "K=RP3 x S1",
            "Hilbert_space": "L2(K,S_K) tensor H_F tensor H_Nambu",
            "superconnection": "A=D_K tensor I + Gamma_K tensor D_F + Phi + A^(1)",
            "single_metric": "<X,Y>=integral_K Str(X^dagger wedge star Y)",
            "quadratic_action": "S_parent^(2)=1/2 <delta A,delta A> + <Psi,D_A Psi>",
            "no_hidden_weights": (
                "No independent coefficients multiplying zero-form, one-form, lepton, Higgs, "
                "or defect summands are allowed."
            ),
        },
        "regular_spectral_kernel_equal_weight_theorem": {
            "condition": "2 f'(x)+4x f''(x)=2 f'(0) for every x>=0",
            "reduced_ode": "g(x)+2x g'(x)=g(0), where g=f'",
            "general_solution_away_from_zero": "g(x)=g(0)+C/sqrt(x)",
            "regularity_at_zero": "C=0",
            "conclusion": "f is affine; no nontrivial regular cutoff kernel forces equal weights at all backgrounds",
            "sample_kernels": spectral_family,
        },
        "normalization_data": {
            "Vol_RP3": vol_rp3,
            "Length_S1": length_s1,
            "raw_tau_seed": raw_tau_seed,
            "canonical_tau_seed": canonical_tau_seed,
            "seed_loss_under_canonical_normalization": raw_tau_seed - canonical_tau_seed,
            "bessel_sum": bessel_sum,
            "canonical_loop_coefficient": raw_loop_coefficient,
            "required_projection_weight_for_one_third": required_projection_weight,
            "neutrino_canonical_norm": neutrino_norm,
        },
        "tau_controls": {
            "published_relation": tau_prediction(raw_tau_seed, 1.0 / 3.0),
            "raw_seed_with_canonical_loop": tau_prediction(
                raw_tau_seed, raw_loop_coefficient
            ),
            "fully_canonical_minimal_parent": tau_prediction(
                canonical_tau_seed, raw_loop_coefficient
            ),
        },
        "sector_gates": sector_gates,
        "predictive_sector_count": len(passed_predictive_sectors),
        "passed_predictive_sectors": passed_predictive_sectors,
        "two_sector_gate": {
            "required_count": 2,
            "observed_count": len(passed_predictive_sectors),
            "passes": len(passed_predictive_sectors) >= 2,
        },
        "scientific_verdict": {
            "minimal_parent_action": "closed negatively as a unified predictive action",
            "surviving_result": (
                "The canonical trace-Hodge configuration metric still derives the neutrino "
                "collective norm 23+pi^-1."
            ),
            "failed_unification": (
                "The same normalization removes the raw volume factors needed by the tau seed, "
                "does not generate the coefficient 1/3, and does not repair the independently "
                "failed exact electromagnetic determinant closure."
            ),
            "reopen_condition": (
                "Derive from a prior symmetry or boundary principle one noncanonical measure or "
                "stiffness operator that fixes all sector weights before comparison with lepton, "
                "Higgs, or electromagnetic data."
            ),
            "program_effect": (
                "The geometric/topological research program is not disproved, but the current "
                "collection of numerical bridges is not generated by one minimal normalized action."
            ),
        },
    }

    assert abs(raw_tau_seed - (PI**2 + 2.0 * PI + 2.0 / 3.0)) < 1e-14
    assert abs(canonical_tau_seed - 8.0 / 3.0) < 1e-14
    assert spectral_family[0]["equal_weights"]
    assert all(not row["equal_weights"] for row in spectral_family[1:])
    assert passed_predictive_sectors == ["neutrino_collective_stiffness"]
    assert not results["two_sector_gate"]["passes"]

    Path("s2t_parent_action_normalization_gate_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "raw_tau_seed": raw_tau_seed,
                "canonical_tau_seed": canonical_tau_seed,
                "required_projection_weight": required_projection_weight,
                "passed_predictive_sectors": passed_predictive_sectors,
                "two_sector_gate": results["two_sector_gate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()