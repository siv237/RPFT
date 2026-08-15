#!/usr/bin/env python3
import json
import math
from pathlib import Path


def relative_error(value, reference):
    return abs(value - reference) / max(1.0, abs(reference))


def main():
    alpha_inverse = 137.035999177
    electron_mass_mev = 0.51099895069
    muon_mass_mev = 105.6583755
    alpha = 1.0 / alpha_inverse

    s_geo = 4.0 * math.pi**3 + math.pi**2 + math.pi
    periodic_term = 1.0 / (24.0 * s_geo)
    pi4_compression_term = 1.0 / (math.pi**4 * s_geo**2)
    s_vac = s_geo - periodic_term - pi4_compression_term
    tau_mass_mev = muon_mass_mev * (
        math.pi**2 + 2.0 * math.pi + 2.0 / 3.0 - alpha / 3.0
    )
    tau_control_mev = 1776.86
    tau_relative_control_residual = (
        tau_mass_mev - tau_control_mev
    ) / tau_control_mev
    v_s2t_gev = (
        tau_mass_mev * s_vac * (1.0 + math.pi**-4) / 1000.0
    )
    g_f_s2t = 1.0 / (math.sqrt(2.0) * v_s2t_gev**2)
    lambda_h = (1.0 + 1.0 / (3.0 * math.pi**2)) / 8.0
    higgs_mass_gev = math.sqrt(2.0 * lambda_h) * v_s2t_gev

    document_values = {
        "S_geo": 137.036303775878,
        "periodic_term": 3.0405568e-4,
        "pi4_compression_term": 5.4667502954e-7,
        "S_vac": 137.035999173522,
        "tau_mass_MeV": 1776.859428563,
        "tau_relative_control_residual": -3.22e-7,
        "v_S2T_GeV": 245.993409261,
        "G_F_S2T_GeV_minus2": 1.1685251368e-5,
        "lambda_H": 0.129221715985,
        "Higgs_mass_GeV": 125.056486039,
    }
    computed_values = {
        "S_geo": s_geo,
        "periodic_term": periodic_term,
        "pi4_compression_term": pi4_compression_term,
        "S_vac": s_vac,
        "tau_mass_MeV": tau_mass_mev,
        "tau_relative_control_residual": tau_relative_control_residual,
        "v_S2T_GeV": v_s2t_gev,
        "G_F_S2T_GeV_minus2": g_f_s2t,
        "lambda_H": lambda_h,
        "Higgs_mass_GeV": higgs_mass_gev,
    }
    row_checks = {}
    for name, value in computed_values.items():
        reference = document_values[name]
        error = relative_error(value, reference)
        tolerance = 5e-8 if name == "tau_relative_control_residual" else 5e-9
        row_checks[name] = {
            "computed": value,
            "document": reference,
            "relative_error": error,
            "tolerance": tolerance,
            "passes": error <= tolerance,
        }

    h1_projection = json.loads(
        Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text(
            encoding="utf-8"
        )
    )
    h1_final = json.loads(
        Path("s2t_c6_same_scheme_final_verdict_results.json").read_text(
            encoding="utf-8"
        )
    )
    h2_bridge = json.loads(
        Path("s2t_ambient_reciprocal_duality_bridge_results.json").read_text(
            encoding="utf-8"
        )
    )

    results = {
        "status": "revision_R1_internal_maturity_5_route_H1_closed_H2_not_test_ready",
        "date": "2026-08-07",
        "frozen_train_inputs": {
            "alpha_inverse": alpha_inverse,
            "electron_mass_MeV": electron_mass_mev,
            "muon_mass_MeV": muon_mass_mev,
            "note": "The displayed R1 rows use alpha_inverse and muon mass; electron mass is a frozen but unused train anchor in this subset.",
        },
        "H0_revision_R1": {
            "implementation": "independent direct formula evaluation without importing prior numerical scripts",
            "computed_values": computed_values,
            "row_checks": row_checks,
            "all_rows_reproduced": all(
                row["passes"] for row in row_checks.values()
            ),
            "alpha_residual": s_vac - alpha_inverse,
            "claim_statuses": {
                "S_geo": "geometric success",
                "periodic_1_over_24": "conditional determinant branch",
                "pi4_term": "strong structural compression, not an exact determinant theorem",
                "tau_mass": "strong conditional relation",
                "v_and_Higgs_mass": "conditional inherited bridge",
                "closed_physical_predictions": 0,
            },
            "revision_integrity": {
                "exact_pi4_theorem_removed": True,
                "C6_no_go_retained": True,
                "parent_action_no_go_retained": True,
                "numerical_reproducibility_does_not_upgrade_claim_status": True,
            },
            "maturity_effect": {
                "old_internal_score": 4,
                "new_internal_score": 5,
                "basis": (
                    "The Tome II rubric explicitly allows 4->5 after a revision "
                    "without the exact pi^-4 theorem plus an independent audit."
                ),
                "external_reproduction_completed": False,
                "next_threshold": "5->6 requires external reproduction of the audit and blind table",
            },
        },
        "H1_C6_reopening": {
            "status": "already_falsified_in_current_model",
            "explicit_n3_projected_trace": h1_projection["projection"][
                "projected_gram_trace"
            ],
            "explicit_n3_projected_rank": h1_projection["projection"][
                "projected_rank_numeric"
            ],
            "hypothesized_zero": False,
            "final_same_scheme_status": h1_final["status"],
            "reason": (
                "The explicit quotient-normalized n=3 projection is nonzero "
                "(trace 80, rank 6), and the final same-scheme audit found no "
                "mandatory compensation. H1 repeats a completed gate."
            ),
            "reopen_only_if": h1_final["reopen_conditions"],
        },
        "H2_reciprocal_plus_defect": {
            "status": "not_test_ready_and_not_a_6_to_7_route",
            "ambient_bridge_status": h2_bridge["status"],
            "relative_normalization_derived": False,
            "common_parent_action_present": False,
            "blind_observable_map_present": False,
            "reason": (
                "The reciprocal minimum is produced by imposed symmetrization, "
                "while the defect saddle is conditional. Adding the two requires "
                "a common dimension, relative coefficient and observable map. "
                "Without them the sum is a new underdefined model, not a blind test."
            ),
            "scale_mismatch": (
                "The internal 6->7 threshold is specifically parameter-free EW/QCD "
                "matching after external reproduction at 5->6."
            ),
        },
        "scientific_verdict": {
            "recommended_move": "publish/freeze revision R1 and prepare external reproducibility package",
            "H0": "passes as an internal maturity upgrade, not a physical closure",
            "H1": "stop; closed negatively unless a new mandatory sector appears",
            "H2": "do not run until a common parent action and blind map are defined",
            "R_sci_internal": 5,
            "N_closed_physical": 0,
        },
    }

    assert results["H0_revision_R1"]["all_rows_reproduced"] is True
    assert abs(results["H0_revision_R1"]["alpha_residual"]) < 4e-9
    assert abs(
        results["H1_C6_reopening"]["explicit_n3_projected_trace"] - 80.0
    ) < 1e-10
    assert results["H1_C6_reopening"]["hypothesized_zero"] is False
    assert results["H2_reciprocal_plus_defect"][
        "relative_normalization_derived"
    ] is False
    assert results["scientific_verdict"]["N_closed_physical"] == 0

    Path("s2t_revision_r1_route_triage_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()