#!/usr/bin/env python3
import json
import math
from pathlib import Path


def main():
    raw_tau_seed = math.pi**2 + 2.0 * math.pi + 2.0 / 3.0
    canonical_tau_seed = 1.0 + 1.0 + 2.0 / 3.0
    neutrino_norm = 23.0 + 1.0 / math.pi

    components = [
        {
            "name": "tau_RP3_constant",
            "object": "1_RP3",
            "form_degree": 0,
            "raw_norm_squared": math.pi**2,
            "canonical_norm_squared": 1.0,
            "quantized_period": False,
            "derived_tier": "propagating_if_it_is_a_field_amplitude",
            "finding": (
                "A constant zero-form has no integral holonomy period. Compact "
                "support alone does not fix its amplitude normalization."
            ),
        },
        {
            "name": "tau_S1_constant",
            "object": "1_S1",
            "form_degree": 0,
            "raw_norm_squared": 2.0 * math.pi,
            "canonical_norm_squared": 1.0,
            "quantized_period": False,
            "derived_tier": "propagating_if_it_is_a_field_amplitude",
            "finding": (
                "The constant function on S1 is not the integral one-form dtheta/(2pi). "
                "Its raw volume norm is not protected by a charge lattice."
            ),
        },
        {
            "name": "tau_angular_average",
            "object": "P_perp n averaged over S2",
            "form_degree": 0,
            "raw_norm_squared": 2.0 / 3.0,
            "canonical_norm_squared": 2.0 / 3.0,
            "quantized_period": False,
            "derived_tier": "finite_internal_average",
            "finding": (
                "The factor 2/3 is an angular expectation, not a compact-volume "
                "or propagating-wavefunction normalization."
            ),
        },
        {
            "name": "neutrino_heavy_collective_mode",
            "object": "P_H tensor e0_hat",
            "form_degree": 0,
            "raw_norm_squared": None,
            "canonical_norm_squared": 23.0,
            "quantized_period": False,
            "derived_tier": "propagating",
            "finding": "The collective amplitude is L2 normalized and contributes rank 23.",
        },
        {
            "name": "neutrino_integral_cycle_mode",
            "object": "P_kernel tensor e1",
            "form_degree": 1,
            "raw_norm_squared": 1.0 / math.pi,
            "canonical_norm_squared": None,
            "quantized_period": True,
            "derived_tier": "integral_holonomy",
            "finding": (
                "The one-form e1 has unit period and therefore a topologically fixed "
                "norm pi^-1 on the unit systolic cycle."
            ),
        },
    ]

    deterministic_rule = {
        "statement": (
            "Use integral-period normalization only for variables carrying a "
            "quantized period; L2-normalize ordinary zero-form field amplitudes."
        ),
        "tau_output": canonical_tau_seed,
        "neutrino_output": neutrino_norm,
        "raw_tau_output": None,
        "passes_neutrino": True,
        "passes_canonical_tau_control": True,
        "passes_raw_tau_seed": False,
    }

    raw_tau_rule = {
        "statement": (
            "Keep unnormalized constant background functions on every compact factor."
        ),
        "tau_output": raw_tau_seed,
        "passes_raw_tau_seed": True,
        "problem": (
            "This rule is not selected by form degree or a quantized period and cannot "
            "also interpret the same constants as canonically normalized field modes."
        ),
    }

    results = {
        "status": "tiered_parent_action_P1_algebraic_number_gate_passes_but_single_measure_and_type_assignment_gates_fail",
        "date": "2026-08-07",
        "proposal": {
            "compact_tier": "integral-period holonomy and zero-mode coordinates",
            "propagating_tier": "L2-normalized wavefunctions and collective amplitudes",
            "claimed_targets": [
                "23+pi^-1",
                "pi^2+2pi+2/3",
                "8/3",
            ],
        },
        "component_classification": components,
        "algebraic_number_gate": {
            "raw_tau_seed": raw_tau_seed,
            "canonical_tau_control": canonical_tau_seed,
            "neutrino_norm": neutrino_norm,
            "all_three_values_reproduced_by_available_normalizations": True,
            "finding": (
                "The three numbers are valid norms of related but differently "
                "normalized representatives. This is bookkeeping, not yet one action."
            ),
        },
        "deterministic_tier_rule": deterministic_rule,
        "alternative_raw_tau_rule": raw_tau_rule,
        "same_tangent_gate": {
            "RP3_rescaling_raw_to_canonical": 1.0 / math.pi,
            "S1_rescaling_raw_to_canonical": 1.0 / math.sqrt(2.0 * math.pi),
            "raw_and_canonical_are_same_coordinate": False,
            "field_redefinition_requires_vertex_rescaling": True,
            "finding": (
                "Raw and canonical constants describe the same geometric directions "
                "with different field coordinates. A physical prediction cannot count "
                "both norms without a separately derived observable map or coupling."
            ),
        },
        "one_measure_gate": {
            "minimum_distinct_tau_metrics_or_readouts": 2,
            "derived_map_between_readouts_present": False,
            "passes": False,
            "reason": (
                "A fixed type assignment gives either the raw tau seed or the canonical "
                "8/3 control for the two constant zero-forms, not both. Producing both "
                "requires a second readout whose origin is not specified by the proposal."
            ),
        },
        "two_sector_gate": {
            "neutrino_sector_passes": True,
            "charged_lepton_raw_seed_passes_under_same_rule": False,
            "observed_predictive_sector_count": 1,
            "required_predictive_sector_count": 2,
            "passes": False,
        },
        "interpretation_of_8_over_3": {
            "value": canonical_tau_seed,
            "is_new_physical_observable": False,
            "role": (
                "It remains the canonical-normalization control that previously "
                "destroyed the raw tau seed. Reproducing a failed alternative readout "
                "does not add a second predictive sector."
            ),
        },
        "architecture_verdicts": {
            "A_tiered_superconnection": (
                "Retains the neutrino graded trace-Hodge result but does not derive "
                "the raw charged-lepton seed from the stated type rule."
            ),
            "B_BF_two_layer_rotor_defect": (
                "Remains an independent loop-level candidate; it cannot repair the "
                "tree-level P1 type-assignment failure without an explicit coupling map."
            ),
            "A_plus_B_hybrid": (
                "Not rejected as a future model, but P1 does not yet provide its common "
                "measure. P2-P4 should not be counted as one parent action until this map "
                "is written locally and fixed by symmetry or boundary data."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The degree-zero propagating versus degree-one integral distinction is "
                "real and already closes the neutrino relative-weight gate."
            ),
            "negative": (
                "Extending that distinction to unnormalized tau constant zero-forms is "
                "not type-derived. Compact support is not a quantized holonomy, and one "
                "fixed rule cannot yield both the raw tau seed and 8/3."
            ),
            "P1_status": "algebraic_pass_operator_fail",
            "next_gate": (
                "Write an explicit local or boundary action with a derived map from "
                "background compact moduli to normalized charged-lepton vertices. The "
                "map must also predict the loop coefficient before tau data are used."
            ),
            "closed_physical_predictions_added": 0,
        },
    }

    assert abs(raw_tau_seed - 16.819456374935612) < 1e-12
    assert abs(canonical_tau_seed - 8.0 / 3.0) < 1e-15
    assert abs(neutrino_norm - 23.31830988618379) < 1e-12
    assert deterministic_rule["passes_raw_tau_seed"] is False
    assert results["one_measure_gate"]["passes"] is False
    assert results["two_sector_gate"]["observed_predictive_sector_count"] == 1
    assert results["scientific_verdict"]["closed_physical_predictions_added"] == 0

    Path("s2t_tiered_parent_action_p1_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()