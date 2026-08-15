import json


result = {
    "date": "2026-08-11",
    "version": "S2T-IV",
    "status": "spin_sum_measure_not_derived_antiperiodic_ranking_remains_conditional",
    "fixed_background_parent": {
        "algebra": "Cinf(K) tensor A_F",
        "hilbert_space": "L2(K,S_s) tensor H8 for one fixed spin structure s",
        "dirac_operator": "D_{K,s,rho} tensor 1 + gamma_K tensor chi D_F",
        "contains_spin_transition_field": False,
        "contains_sum_over_spin_structures": False,
    },
    "candidate_sum": {
        "formula": "Z_sum=sum_s w_s Z_s",
        "weights_fixed_by_local_spectral_action": False,
        "equal_weights_follow_from_current_axioms": False,
        "unique_equal_counting_measure_if_full_spin_torsor_translation_symmetry_is_postulated": True,
        "full_spin_torsor_translation_symmetry_derived": False,
    },
    "additional_structures_that_could_define_the_sum": [
        "a direct-sum or groupoid Hilbert space over spin structures",
        "a dynamical Z2 topological gauge sector",
        "a spin-TQFT or invertible topological weight",
        "a declared cobordism/filling prescription fixing relative phases",
    ],
    "source_conflict": {
        "legacy_RPFT_choice": "periodic S1 boundary condition fixed because S1 is spatial",
        "current_determinant_result": "if periodic and antiperiodic branches are summed with equal prior weights, the antiperiodic branch has lower fermion effective action",
        "resolution": "a spatial circle admits both spin structures; antiperiodicity is thermal only when imposed on the Euclidean-time circle. The legacy periodic choice is a model input, not a theorem from spatiality alone.",
    },
    "verdict": {
        "spin_sum_measure_closed": False,
        "antiperiodic_branch_dynamically_selected_in_current_parent": False,
        "antiperiodic_branch_scheme_independently_ranked_under_equal_weight_sum": True,
        "new_theory_required_for_dynamic_spin_sum": True,
        "absolute_scale_status_changed": False,
    },
    "next_allowed_options": [
        "freeze one spin structure as explicit background input and continue the determinant calculation",
        "construct a new Z2/spin-TQFT measure and repeat anomaly, reality and determinant gates",
    ],
}

with open(
    "s2t_v4_spin_sum_measure_gate_results.json", "w", encoding="utf-8"
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result["verdict"], ensure_ascii=False, indent=2))