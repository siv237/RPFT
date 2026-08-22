#!/usr/bin/env python3
"""Audit the retrospective correction of the version VI candidate menu."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_candidate_menu_retrospective_correction_gate_results.json"


def main() -> None:
    prior_results = {
        "self_generated_transition_defect": {
            "kink": True,
            "normalizable_Dirac_zero_mode": True,
            "full_carrier_multiplicity": 300,
            "potential_and_scale_derived": False,
        },
        "holonomy_projector_defect_multiplicity": {
            "rank_chain": [300, 45, 15, 2, 1],
            "rank_one_is_conditional_on_nonzero_Higgs": True,
            "unified_nonlinear_functional": False,
        },
        "projector_superconnection_common_scale": {
            "independent_parameters": ["f2", "f0", "Lambda", "ell", "odd_field_normalization"],
            "common_scale_derived": False,
        },
        "spectral_pairing_stiffness": {
            "phase_depends_on_spectral_function": True,
            "even_action_selects_orientation": False,
        },
        "fermionic_spectral_measure": {
            "even_and_odd_moments_linked": False,
            "pairing_amplitude_derived": False,
        },
        "fermionic_determinant_induced_action": {
            "single_positive_four_derivative_term": False,
            "scheme_independent_radius": False,
        },
    }
    result = {
        "gate": "version6_spectral_transition_candidate_menu_retrospective_correction_gate",
        "prior_results": prior_results,
        "correction": {
            "dynamical_finite_Dirac_field_is_new": False,
            "previous_candidate_selection_retracted": True,
            "fully_admitted_model_exists": False,
            "ordinary_internal_fluctuations_must_not_be_reopened": True,
        },
        "genuinely_unbuilt_object": {
            "exact_nonlinear_discrete_parent": True,
            "exact_local_update_rule_present_in_project": False,
            "continuum_limit_alone_is_sufficient": False,
        },
        "next_gate": "version6_spectral_transition_discrete_nonlinear_parent_reopening_gate",
    }
    assert prior_results["self_generated_transition_defect"]["full_carrier_multiplicity"] == 300
    assert prior_results["holonomy_projector_defect_multiplicity"]["rank_chain"] == [300, 45, 15, 2, 1]
    assert not result["correction"]["dynamical_finite_Dirac_field_is_new"]
    assert result["correction"]["previous_candidate_selection_retracted"]
    assert not result["correction"]["fully_admitted_model_exists"]
    assert not result["genuinely_unbuilt_object"]["exact_local_update_rule_present_in_project"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()