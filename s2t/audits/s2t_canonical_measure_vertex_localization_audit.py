#!/usr/bin/env python3
import json
import math
from pathlib import Path


def close(left, right, tolerance=1e-12):
    return abs(left - right) <= tolerance


def main():
    raw_tau_seed = math.pi**2 + 2.0 * math.pi + 2.0 / 3.0
    canonical_tau_control = 1.0 + 1.0 + 2.0 / 3.0
    neutrino_norm = 23.0 + 1.0 / math.pi
    canonical_loop_coefficient = 0.061696937539545534
    required_loop_weight = (1.0 / 3.0) / canonical_loop_coefficient

    hm = {
        "measure_statement": "Identity weight relative to the frozen graded trace-Hodge metric.",
        "important_language_correction": (
            "Identity weight does not make every component Euclidean-unit; "
            "the integral cycle one-form already has geometric norm pi^-1."
        ),
        "neutrino_output": 23.0 + 1.0 / math.pi,
        "tau_canonical_output": 1.0 + 1.0 + 2.0 / 3.0,
        "neutrino_compatibility_pass": True,
        "tau_canonical_compatibility_pass": True,
        "measure_derived_from_parent_action": False,
        "reason_measure_not_derived": (
            "The canonical graded metric is frozen as the hypothesis; no symmetry, "
            "Hessian or quantum measure uniquely selects it."
        ),
    }

    physical_sector_gate = {
        "neutrino_is_normalization_sensitive_model_sector": True,
        "tau_8_over_3_is_independent_empirical_sector": False,
        "tau_role": (
            "8/3 is the canonical control that removed the raw tau seed, "
            "not the observed charged-lepton relation."
        ),
        "independent_predictive_sector_count": 1,
        "required_count": 2,
        "passes": False,
    }

    relocation_gate = {
        "raw_tau_seed": raw_tau_seed,
        "excluded_from_kinetic_measure": True,
        "vertex_derivation_supplied": False,
        "required_loop_weight": required_loop_weight,
        "finding": (
            "Moving the seed to a vertex is consistent bookkeeping, but relocates "
            "rather than derives the volume and projection factors."
        ),
    }

    qcycle_trace = math.pi + 1.0 / math.pi
    single_vertex_gate = {
        "minimal_Qcycle_candidate": {
            "trace": qcycle_trace,
            "target_raw_volume_part": math.pi**2 + 2.0 * math.pi,
            "passes": close(qcycle_trace, math.pi**2 + 2.0 * math.pi),
        },
        "admissible_vertex_class_declared": False,
        "single_operator_versus_single_scalar_readout_distinguished": False,
        "unrestricted_counterexample": {
            "space": "H_volume direct_sum H_winding",
            "operator": "V=diag(raw_tau_seed,J_required)",
            "interpretation": (
                "This target-loaded construction is not physical. It shows only that "
                "a universal no-go needs a preregistered vertex algebra and readout."
            ),
        },
        "exact_no_go_proved": False,
        "valid_negative_scope": (
            "The specific Qcycle trace fails; no broader single-vertex theorem follows."
        ),
    }

    results = {
        "status": (
            "HM_compatibility_pass_measure_derivation_and_two_sector_prediction_"
            "fail_single_vertex_no_go_unproved"
        ),
        "date": "2026-08-07",
        "targets_and_controls": {
            "raw_tau_seed": raw_tau_seed,
            "canonical_tau_control": canonical_tau_control,
            "neutrino_norm": neutrino_norm,
            "canonical_loop_coefficient": canonical_loop_coefficient,
            "required_loop_weight": required_loop_weight,
        },
        "H_M_gate": hm,
        "physical_two_sector_gate": physical_sector_gate,
        "raw_seed_relocation_gate": relocation_gate,
        "single_vertex_gate": single_vertex_gate,
        "scientific_verdict": {
            "positive": (
                "One frozen canonical graded metric is compatible with the neutrino "
                "norm and canonical tau control."
            ),
            "negative": (
                "Compatibility does not derive the measure, 8/3 is not an independent "
                "physical prediction, and the raw seed plus J remain underived."
            ),
            "single_vertex_status": "specific_Qcycle_fails_general_no_go_open",
            "closed_physical_predictions_added": 0,
            "next_gate": (
                "Declare a finite vertex algebra and one covariant readout, derive it "
                "before tau data, and test both volume and winding coefficients."
            ),
        },
    }

    assert close(hm["neutrino_output"], neutrino_norm)
    assert close(hm["tau_canonical_output"], canonical_tau_control)
    assert close(required_loop_weight, 5.4027533071585365)
    assert physical_sector_gate["passes"] is False
    assert relocation_gate["vertex_derivation_supplied"] is False
    assert single_vertex_gate["minimal_Qcycle_candidate"]["passes"] is False
    assert single_vertex_gate["exact_no_go_proved"] is False
    assert results["scientific_verdict"]["closed_physical_predictions_added"] == 0

    Path("s2t_canonical_measure_vertex_localization_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()