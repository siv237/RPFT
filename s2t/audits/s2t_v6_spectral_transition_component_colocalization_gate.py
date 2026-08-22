#!/usr/bin/env python3
"""Аудит пространственной колокализации спектральных компонент 12 и 3."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_component_colocalization_gate_results.json"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def gaussian_density(x: np.ndarray, center: float, sigma: float) -> np.ndarray:
    density = np.exp(-0.5 * ((x - center) / sigma) ** 2)
    return density / np.trapezoid(density, x)


def main() -> None:
    boundary = load("s2t_v6_spectral_transition_component_boundary_gate_results.json")
    morita = load("s2t_v5_morita_linking_parent_gate_results.json")
    oneforms = load("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
    torsion = load("s2t_v5_h15_spectral_torsion_selector_gate_results.json")
    mass_portal = load("s2t_v6_bosonic_defect_mass_portal_parent_gate_results.json")
    family_connection = load("s2t_v6_bosonic_defect_family_connection_parent_identification_gate_results.json")
    field_id = load("s2t_v6_bosonic_defect_field_identification_gate_results.json")
    callias = load("s2t_v6_composite_connection_callias_fredholm_gate_results.json")
    comparison = load("s2t_v6_callias_toeplitz_index_comparison_gate_results.json")
    spin_cover = load("s2t_v6_spin_cover_carrier_parent_derivation_gate_results.json")
    two_copy = load("s2t_v6_two_copy_spin_cover_multiplicity_gate_results.json")

    rng = np.random.default_rng(20260821)
    r_quark = rng.normal(size=(20, 12)) + 1j * rng.normal(size=(20, 12))
    r_lepton = rng.normal(size=(20, 3)) + 1j * rng.normal(size=(20, 3))
    r_full = np.concatenate([r_quark, r_lepton], axis=1)
    morita_additivity_residual = abs(
        np.vdot(r_full, r_full).real
        - np.vdot(r_quark, r_quark).real
        - np.vdot(r_lepton, r_lepton).real
    )

    p_quark = np.diag([1.0] * 12 + [0.0] * 3)
    p_lepton = np.eye(15) - p_quark
    a_family = np.array(
        [[0.0, 0.7, -0.2], [-0.7, 0.0, 0.5], [0.2, -0.5, 0.0]],
        dtype=complex,
    )
    a_h45 = np.kron(a_family, np.eye(15))
    p_quark_h45 = np.kron(np.eye(3), p_quark)
    p_lepton_h45 = np.kron(np.eye(3), p_lepton)
    family_commutator_residuals = {
        "quark": float(np.linalg.norm(a_h45 @ p_quark_h45 - p_quark_h45 @ a_h45)),
        "lepton": float(np.linalg.norm(a_h45 @ p_lepton_h45 - p_lepton_h45 @ a_h45)),
    }

    x = np.linspace(-12.0, 12.0, 24001)
    sigma = 0.8
    weights = {
        "quark": boundary["component_cycles"]["quark"]["normalized_weight"],
        "lepton": boundary["component_cycles"]["lepton"]["normalized_weight"],
    }
    separations = [0.0, 0.5, 1.0, 2.0, 4.0]
    separation_scan = []
    for separation in separations:
        rho_q = gaussian_density(x, -separation / 2.0, sigma)
        rho_l = gaussian_density(x, separation / 2.0, sigma)
        self_q = float(np.trapezoid(rho_q**2, x))
        self_l = float(np.trapezoid(rho_l**2, x))
        overlap = float(np.trapezoid(rho_q * rho_l, x))
        current_energy = weights["quark"] * self_q + weights["lepton"] * self_l
        hypothetical_attractive_energy = current_energy - overlap
        separation_scan.append(
            {
                "separation": separation,
                "quark_self": self_q,
                "lepton_self": self_l,
                "overlap": overlap,
                "current_additive_energy": current_energy,
                "hypothetical_energy_if_binding_coefficient_were_one": hypothetical_attractive_energy,
            }
        )

    current_energies = np.array([row["current_additive_energy"] for row in separation_scan])
    hypothetical_energies = np.array(
        [row["hypothetical_energy_if_binding_coefficient_were_one"] for row in separation_scan]
    )

    edge_names = [edge["name"] for edge in oneforms["charged_edge_multiplicity_space"]["edges"]]
    result = {
        "gate": "version6_spectral_transition_component_colocalization_gate",
        "input_certificates": {
            "component_classes": {
                "quark": boundary["component_cycles"]["quark"]["KO6_integer_class"],
                "lepton": boundary["component_cycles"]["lepton"]["KO6_integer_class"],
            },
            "global_class_requires_sum": boundary["global_class_ledger"]["global_class_requires_both_component_classes_in_total"],
            "previous_binding_term": boundary["additivity_and_binding_test"]["current_action_contains_quark_lepton_binding_term"],
        },
        "direct_finite_connector_audit": {
            "charged_edges": edge_names,
            "quark_edges": ["u", "d"],
            "lepton_edges": ["e"],
            "quark_lepton_Dirac_edge_count": 0,
            "edge_intertwiner_algebra": oneforms["charged_edge_multiplicity_space"]["bimodule_endomorphism_algebra"],
            "KO6_identifies_u_d_e_edges": oneforms["connection_affine_space"]["KO6_identifies_distinct_u_d_e_edges"],
            "direct_finite_colocalizing_connector": False,
        },
        "morita_curvature_audit": {
            "carrier_split": "M20x15 = M20x12 direct_sum M20x3",
            "hilbert_schmidt_additivity_residual": float(morita_additivity_residual),
            "centered_relative_curvature_formula": morita["relative_bimodule_curvature"]["centered_formula"],
            "quark_lepton_cross_term_in_centered_norm": 0.0,
            "common_left_M20_action_is_a_spatial_binding_operator": False,
            "colocalization_derived": False,
        },
        "higgs_and_torsion_audit": {
            "same_Higgs_doublet_appears_on_d_and_e_edges": True,
            "same_Higgs_field_creates_direct_quark_lepton_Dirac_edge": False,
            "torsion_down_lepton_invariant": torsion["H15_spectral_torsion_invariants"]["down_lepton_self"],
            "mixed_derivative_of_3b2_plus_c2_with_respect_to_b_c": 0.0,
            "squared_torsion_potential_contains_b2_c2_cross_term": True,
            "squared_torsion_potential_allowed_as_parent_selector": torsion["forbidden_potential_repair"]["allowed_as_parent_derived_selector"],
            "minimal_shape_Higgs_portal_coefficient": mass_portal["higgs_portal_test"]["Tr_Q2_H2_coefficient_in_minimal_M300_parent"],
            "radial_Higgs_coupling_locates_quark_and_lepton_spectral_cores": False,
            "Higgs_colocalization_derived": False,
        },
        "family_gauge_and_order_parameter_audit": {
            "family_connection_action": "A_fam tensor I_H15",
            "family_connection_commutator_residuals": family_commutator_residuals,
            "family_connection_is_rank_blind_on_H15": True,
            "family_connection_dynamical_localization_derived": family_connection["verdict"]["dynamical_localization_of_family_symmetry_derived"],
            "Q_field_SM_representation": field_id["field_representation"]["standard_model_representation"],
            "Q_fermion_minimum_independent_species_coefficients": field_id["fermion_coupling_boundary"]["minimum_independent_species_coefficients"],
            "Q_unique_nonzero_fermion_coupling_selected": field_id["fermion_coupling_boundary"]["current_parent_selects_unique_nonzero_coupling"],
            "ordinary_inner_fluctuation_generates_Q_fermion_coupling": field_id["fermion_coupling_boundary"]["ordinary_inner_fluctuation_generates_family_Q_coupling"],
            "single_Q_profile_would_conditionally_be_common_to_all_H15_states": True,
            "single_Q_profile_is_derived_as_component_localizing_mass": False,
        },
        "callias_common_core_candidate": {
            "conditional_mass": "(n(x) dot sigma) tensor (q_quark + q_lepton)",
            "conditional_common_profile_would_colocalize_12_and_3": True,
            "coefficient_Callias_index": callias["spin_cover_mass"]["coefficient_Callias_index_magnitude"],
            "same_clutching_unitary_as_Toeplitz": comparison["comparison"]["same_clutching_unitary_as_tome5_real_toeplitz_symbol"],
            "spatial_Callias_operator_identified_with_Toeplitz_boundary": callias["toeplitz_stable_index"]["spatial_Callias_operator_identified_with_Toeplitz_boundary"],
            "finite_parent_derives_spin_cover_carrier": spin_cover["verdict"]["finite_parent_derives_required_doublet"],
            "two_copy_loophole_available": not two_copy["verdict"]["spin_cover_fermion_branch_closed_in_current_finite_parent"],
            "common_core_is_currently_physical": False,
            "independent_component_profiles_remain_allowed": True,
        },
        "separation_test": {
            "model": "two normalized Gaussian defect densities with the current additive component weights",
            "component_weights": weights,
            "scan": separation_scan,
            "current_energy_spread_over_separation": float(np.max(current_energies) - np.min(current_energies)),
            "current_energy_has_minimum_at_zero_separation": False,
            "hypothetical_attractive_cross_term_would_minimize_at_zero": int(np.argmin(hypothetical_energies)) == 0,
            "current_cross_coefficient": 0.0,
        },
        "global_index_boundary": {
            "total_KO6_class_conserved": 15,
            "separated_centers_can_carry_classes_12_and_3": True,
            "K_theory_addition_requires_same_spatial_center": False,
            "global_index_conservation_is_binding_energy": False,
        },
        "verdict": {
            "direct_quark_lepton_connector_exists": False,
            "current_Morita_or_Toeplitz_actions_colocalize_components": False,
            "current_Higgs_or_torsion_terms_colocalize_components": False,
            "current_family_QTB_sector_colocalizes_observed_components": False,
            "conditional_single_Callias_profile_would_colocalize": True,
            "conditional_Callias_profile_is_parent_derived": False,
            "global_class_15_is_a_proved_bound_particle": False,
            "spatial_colocalization_derived": False,
            "physical_closure": False,
            "status": "all derived terms remain block-additive or rank-blind; the only common-core construction is the unproved spin-cover Callias ansatz, so class 15 is not a derived bound particle",
        },
        "next_gate": "version6_spectral_transition_higgs_resolved_support_gate",
    }

    assert boundary["verdict"]["their_direct_sum_is_the_original_class_15"]
    assert edge_names == ["u", "d", "e"]
    assert morita_additivity_residual < 1.0e-10
    assert all(value < 1.0e-12 for value in family_commutator_residuals.values())
    assert mass_portal["higgs_portal_test"]["Tr_Q2_H2_coefficient_in_minimal_M300_parent"] == 0.0
    assert not torsion["forbidden_potential_repair"]["allowed_as_parent_derived_selector"]
    assert not spin_cover["verdict"]["finite_parent_derives_required_doublet"]
    assert two_copy["verdict"]["spin_cover_fermion_branch_closed_in_current_finite_parent"]
    assert result["separation_test"]["current_energy_spread_over_separation"] < 1.0e-12
    assert result["separation_test"]["hypothetical_attractive_cross_term_would_minimize_at_zero"]
    assert not result["verdict"]["spatial_colocalization_derived"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()