#!/usr/bin/env python3
"""Решение между буквальной нитью и спектральным примитивом перехода."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_single_thread_scale_hierarchy_branch_decision_gate_results.json"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def main() -> None:
    scale_v3 = load("s2t_v3_absolute_scale_no_go_results.json")
    scale_v5 = load("s2t_v5_projector_superconnection_common_scale_gate_results.json")
    scale_v6 = load("s2t_v6_bosonic_defect_mass_portal_parent_gate_results.json")
    thread = load("s2t_v6_single_thread_excluded_volume_reconnection_barrier_gate_results.json")
    toeplitz = load("s2t_v5_one_seventh_toeplitz_boundary_map_gate_results.json")
    unbounded = load("s2t_v5_real_toeplitz_unbounded_parent_cycle_gate_results.json")
    transfer = load("s2t_v5_local_defect_transfer_operator_gate_results.json")

    coefficient_rank = int(toeplitz["coefficient_projection"]["rank"])
    ambient_rank = int(toeplitz["coefficient_projection"]["ambient_rank"])
    normalized_weight = float(toeplitz["coefficient_projection"]["normalized_trace"])

    rank_one_decomposition = [1 for _ in range(coefficient_rank)]
    result = {
        "gate": "version6_single_thread_scale_hierarchy_branch_decision_gate",
        "scale_ledger": {
            "version3_absolute_scale_from_topology": scale_v3["verdict"]["topology_fixes_absolute_scale"],
            "version3_absolute_scale_from_normalized_geometry": scale_v3["verdict"]["normalized_geometry_fixes_absolute_scale"],
            "version5_common_superconnection_scale": scale_v5["verdict"]["common_scale_from_current_parent"],
            "version5_finite_radius_prediction": scale_v5["verdict"]["finite_radius_prediction"],
            "version6_absolute_length_scale": scale_v6["two_scale_degeneracy"]["absolute_length_scale_derived"],
            "version6_absolute_energy_scale": scale_v6["two_scale_degeneracy"]["absolute_energy_scale_derived"],
            "thread_hard_core_from_parent": thread["verdict"]["excluded_volume_derived_from_current_parent"],
            "thread_reconnection_barrier_from_parent": thread["verdict"]["infinite_reconnection_barrier_derived"],
            "hidden_scale_hierarchy_available": False,
        },
        "spectral_transition_skeleton": {
            "hilbert_module": unbounded["infinite_exact_cycle"]["hilbert_space"],
            "number_operator": unbounded["infinite_exact_cycle"]["number_operator"],
            "bilateral_shift": unbounded["infinite_exact_cycle"]["bilateral_shift"],
            "hardy_projection_derived_from_N": unbounded["verdict"]["hardy_polarization_derived_from_N"],
            "compact_defect_projection": toeplitz["toeplitz_operator"]["compact_defect_projection"],
            "compact_defect_rank": toeplitz["toeplitz_operator"]["compact_defect_projection_rank"],
            "normalized_defect_weight": normalized_weight,
            "oriented_indices": [
                toeplitz["toeplitz_operator"]["coefficient_Fredholm_index"],
                toeplitz["orientation_reversal"]["coefficient_Fredholm_index"],
            ],
            "local_transfer_has_common_light_cone": transfer["continuum_limit"]["common_light_cone"],
            "local_transfer_dispersion": transfer["continuum_limit"]["emergent_dispersion"],
            "nonzero_mass_parameter_derived": False,
            "physical_parent_action_complete": False,
        },
        "primitivity_warning": {
            "coefficient_rank": coefficient_rank,
            "ambient_rank": ambient_rank,
            "K0_class_integer": coefficient_rank,
            "rank_one_decomposition": rank_one_decomposition,
            "rank_one_decomposition_sum": sum(rank_one_decomposition),
            "complex_matrix_projection_is_algebraically_primitive": coefficient_rank == 1,
            "class_15_is_15_times_complex_K0_generator": True,
            "Real_or_gauge_equivariant_splitting_allowed": None,
            "physical_indivisibility_proved": False,
            "required_next_test": "classify invariant subprojections under the full algebra, Real structure, grading, gauge action and transfer dynamics",
        },
        "dictionary": {
            "historical_thread": "ordered composition of local transitions",
            "winding_turn": "power U^n measured by N",
            "fabric": "homogeneous phase of the transition network / quantum walk",
            "matter_candidate": "localized finite-rank topological defect of the transition operator",
            "particle_antiparticle": "Real-conjugate oriented index pair -15/+15",
            "mass_candidate": "spectral or quasienergy gap of the local transfer operator",
            "spatial_size_candidate": "localization length derived from velocity divided by a parent-derived gap",
        },
        "branch_decision": {
            "literal_continuous_rope_branch_active": False,
            "literal_thread_retained_as_history_and_coarse_metaphor": True,
            "spectral_transition_primitive_selected": True,
            "effective_Hopf_field_branch_retained": True,
            "rank_15_declared_elementary_particle": False,
            "absolute_spatial_size_derived": False,
            "next_gate": "version6_spectral_transition_minimal_support_gate",
        },
    }

    assert not any(result["scale_ledger"].values())
    assert coefficient_rank == 15
    assert ambient_rank == 105
    assert abs(normalized_weight - 1.0 / 7.0) < 1.0e-15
    assert sum(rank_one_decomposition) == coefficient_rank
    assert result["spectral_transition_skeleton"]["local_transfer_has_common_light_cone"]
    assert not result["branch_decision"]["rank_15_declared_elementary_particle"]
    assert result["branch_decision"]["spectral_transition_primitive_selected"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()