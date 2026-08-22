#!/usr/bin/env python3
"""Audit exact component selection rules versus unavailable creation rates."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_componentwise_creation_observable_gate_results.json"


def normalize(values: list[int]) -> list[Fraction]:
    total = sum(values)
    return [Fraction(value, total) for value in values]


def main() -> None:
    component_ranks = [12, 3]
    toeplitz_weights = [Fraction(12, 105), Fraction(3, 105)]
    sphaleron_flows = [3, 1]
    charge_changes = [1, 1]
    higgs_resolved_ranks = [6, 6, 2, 1]

    normalized_rank_candidate = normalize(component_ranks)
    normalized_flow_candidate = normalize(sphaleron_flows)
    normalized_charge_candidate = normalize(charge_changes)

    candidates = {
        "rank_candidate": [str(value) for value in normalized_rank_candidate],
        "flow_candidate": [str(value) for value in normalized_flow_candidate],
        "charge_candidate": [str(value) for value in normalized_charge_candidate],
    }
    unique_candidates = {tuple(values) for values in candidates.values()}

    result = {
        "gate": "version6_spectral_transition_componentwise_creation_observable_gate",
        "exact_component_ledgers": {
            "KO6_Toeplitz_ranks": component_ranks,
            "normalized_Toeplitz_weights": [str(value) for value in toeplitz_weights],
            "weight_ratio": "4:1",
            "physical_sphaleron_flows": sphaleron_flows,
            "flow_ratio": "3:1",
            "anomaly_charge_changes": {
                "delta_B": 1,
                "delta_L": 1,
                "delta_B_minus_L": 0,
                "charge_ratio": "1:1",
            },
            "Higgs_resolved_support_ranks": higgs_resolved_ranks,
        },
        "probability_candidate_test": {
            **candidates,
            "number_of_distinct_normalized_candidates": len(unique_candidates),
            "single_canonical_probability_measure_selected": len(unique_candidates) == 1,
        },
        "missing_rate_inputs": {
            "calibrated_transition_barrier": False,
            "physical_temperature_or_nonequilibrium_distribution": False,
            "real_time_kinetic_operator": False,
            "dynamical_prefactor": False,
            "common_component_fluctuation_measure": False,
            "stable_observed_fermionic_endpoint": False,
        },
        "surviving_exact_statements": {
            "component_K_classes": True,
            "standard_sphaleron_flow_selection_rule": True,
            "delta_B_equals_delta_L": True,
            "B_minus_L_conserved": True,
            "local_rank_change_Wnu_zero_to_one_is_possible_at_H_zero": True,
        },
        "not_derived": {
            "quark_to_lepton_creation_branching_ratio": True,
            "absolute_creation_rate": True,
            "created_particle_multiplicity": True,
            "product_mass": True,
            "product_size": True,
            "probability_of_stable_matter_formation": True,
        },
        "verdict": {
            "parameter_free_component_selection_rules_exist": True,
            "parameter_free_component_creation_probability_exists": False,
            "Toeplitz_weights_are_branching_fractions": False,
            "dynamic_closure": False,
            "status": "the current parent fixes distinct rank, flow and charge ledgers but contains no measure or real-time dynamics selecting a creation probability",
        },
        "next_gate": "version6_spectral_transition_dynamic_closure_status_gate",
    }

    assert component_ranks == [12, 3]
    assert toeplitz_weights == [Fraction(4, 35), Fraction(1, 35)]
    assert sphaleron_flows == [3, 1]
    assert charge_changes == [1, 1]
    assert sum(higgs_resolved_ranks) == 15
    assert normalized_rank_candidate == [Fraction(4, 5), Fraction(1, 5)]
    assert normalized_flow_candidate == [Fraction(3, 4), Fraction(1, 4)]
    assert normalized_charge_candidate == [Fraction(1, 2), Fraction(1, 2)]
    assert len(unique_candidates) == 3
    assert not result["probability_candidate_test"]["single_canonical_probability_measure_selected"]
    assert not result["verdict"]["parameter_free_component_creation_probability_exists"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()