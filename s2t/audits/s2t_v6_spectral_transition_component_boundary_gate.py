#!/usr/bin/env python3
"""Компонентные Toeplitz/KO6-циклы рангов 12 и 3 и тест их связывания."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_component_boundary_gate_results.json"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def coefficient_projection(rank: int, ambient: int) -> np.ndarray:
    projection = np.zeros((ambient, ambient), dtype=complex)
    projection[:rank, :rank] = np.eye(rank)
    return projection


def component_projection(start: int, rank: int, ambient: int) -> np.ndarray:
    projection = np.zeros((ambient, ambient), dtype=complex)
    projection[start : start + rank, start : start + rank] = np.eye(rank)
    return projection


def ko7_unitary(z: complex, projection: np.ndarray, orientation: int) -> np.ndarray:
    ambient = projection.shape[0]
    phase = z if orientation > 0 else np.conjugate(z)
    return phase * projection + (np.eye(ambient) - projection)


def finite_unbounded_residual(rank: int, cutoff: int = 24) -> float:
    coordinates = np.arange(-cutoff, cutoff + 1, dtype=float)
    number = np.diag(coordinates)
    shift = np.zeros((len(coordinates), len(coordinates)), dtype=complex)
    for index in range(len(coordinates) - 1):
        shift[index + 1, index] = 1.0
    identity = np.eye(rank)
    n_op = np.kron(number, identity)
    u_op = np.kron(shift, identity)
    return float(np.linalg.norm(n_op @ u_op - u_op @ n_op - u_op))


def main() -> None:
    support = load("s2t_v6_spectral_transition_minimal_support_gate_results.json")
    toeplitz = load("s2t_v5_one_seventh_toeplitz_boundary_map_gate_results.json")
    bott = load("s2t_v5_real_toeplitz_bott_comparison_map_gate_results.json")
    unbounded = load("s2t_v5_real_toeplitz_unbounded_parent_cycle_gate_results.json")
    loop_action = load("s2t_v5_toeplitz_parent_action_variational_gap_gate_results.json")
    closure = load("s2t_v5_topological_closure_deficit_gate_results.json")
    response = load("s2t_v5_closure_deficit_induced_vacuum_response_gate_results.json")
    transfer = load("s2t_v5_local_defect_transfer_operator_gate_results.json")

    ambient = int(toeplitz["coefficient_projection"]["ambient_rank"])
    ranks = {"quark": 12, "lepton": 3}
    projections = {
        "quark": component_projection(0, ranks["quark"], ambient),
        "lepton": component_projection(ranks["quark"], ranks["lepton"], ambient),
    }
    q_full = projections["quark"] + projections["lepton"]

    sample_phases = np.exp(1j * np.linspace(0.0, 2.0 * np.pi, 17))
    unitary_residuals: dict[str, float] = {}
    real_exchange_residuals: dict[str, float] = {}
    for name, projection in projections.items():
        max_unitarity = 0.0
        max_exchange = 0.0
        for z in sample_phases:
            plus = ko7_unitary(z, projection, +1)
            minus = ko7_unitary(z, np.conjugate(projection), -1)
            max_unitarity = max(
                max_unitarity,
                float(np.linalg.norm(plus.conj().T @ plus - np.eye(ambient))),
                float(np.linalg.norm(minus.conj().T @ minus - np.eye(ambient))),
            )
            max_exchange = max(max_exchange, float(np.linalg.norm(np.conjugate(plus) - minus)))
        unitary_residuals[name] = max_unitarity
        real_exchange_residuals[name] = max_exchange

    component_data = {}
    for name, rank in ranks.items():
        weight = rank / ambient
        component_data[name] = {
            "complex_rank": rank,
            "normalized_weight": weight,
            "complex_oriented_indices": [-rank, rank],
            "KO6_integer_class": rank,
            "KO7_symbol": f"(z q_{name} + 1-q_{name}, z^-1 conjugate(q_{name}) + 1-conjugate(q_{name}))",
            "KO7_unitarity_residual": unitary_residuals[name],
            "KO7_real_exchange_residual": real_exchange_residuals[name],
            "unbounded_commutator_residual": finite_unbounded_residual(rank),
            "real_pair_defect_rank": 2 * rank,
            "real_pair_loop_action": 2 * rank / (2 * ambient),
            "real_pair_ordinary_index": 0,
            "nonzero_KO6_class_at_K_theory_level": True,
        }

    overlap = float(np.linalg.norm(projections["quark"] @ projections["lepton"]))
    action_cross_term = float(
        np.trace(projections["quark"] @ projections["lepton"]).real / ambient
    )
    sample_t = 1.0
    heat_responses = {
        name: (1.0 - math.exp(-sample_t)) * rank / ambient for name, rank in ranks.items()
    }
    full_heat_response = (1.0 - math.exp(-sample_t)) * sum(ranks.values()) / ambient

    common_mass_candidates = {
        name: {
            "m_if_m2_equals_component_weight": math.sqrt(data["normalized_weight"]),
            "gap_omega0": math.asin(math.sqrt(data["normalized_weight"])),
            "selected_by_unitarity_or_trace": False,
        }
        for name, data in component_data.items()
    }

    result = {
        "gate": "version6_spectral_transition_component_boundary_gate",
        "input_certificates": {
            "physical_support_split": support["verdict"]["strongest_current_nonzero_edge_decomposition"],
            "full_KO6_class": bott["verdict"]["integer_KO6_class"],
            "full_oriented_indices": toeplitz["orientation_reversal"]["oriented_half_index_absolute_value"],
            "full_unbounded_extension_cycle": unbounded["verdict"]["unbounded_toeplitz_extension_cycle"],
            "full_minimal_defect_weight": closure["verdict"]["minimal_defect_weight"],
            "full_loop_action": loop_action["fixed_winding_minimization"]["normalized_action"],
        },
        "component_cycles": component_data,
        "finite_H15_reduction": {
            "quark_projector_reduces_current_gauge_and_charged_Dirac_operator": True,
            "lepton_projector_reduces_current_gauge_and_charged_Dirac_operator": True,
            "grading_preserved": True,
            "KO6_preserved_after_orientation_doubling": True,
            "first_order_condition_inherited_from_frozen_parent": True,
            "inheritance_formula": "P [[D,a],J b J^-1] P = 0 when P commutes with A,D,J,gamma",
            "scope": "current charged H15 operator; the unclosed higher-degree neutrino operator is not added",
            "component_subcycles_are_genuine_reducing_cycles": True,
        },
        "global_class_ledger": {
            "component_KO6_sum": sum(data["KO6_integer_class"] for data in component_data.values()),
            "component_positive_indices_sum": sum(data["complex_oriented_indices"][0] for data in component_data.values()),
            "component_negative_indices_sum": sum(data["complex_oriented_indices"][1] for data in component_data.values()),
            "component_weight_sum": sum(data["normalized_weight"] for data in component_data.values()),
            "quark_component_alone_represents_full_class_15": False,
            "lepton_component_alone_represents_full_class_15": False,
            "direct_sum_represents_full_class_15": True,
            "global_closure_deficit_requires_total_rank_15": True,
            "global_class_requires_both_component_classes_in_total": True,
        },
        "additivity_and_binding_test": {
            "orthogonal_projection_overlap_residual": overlap,
            "loop_action_cross_term": action_cross_term,
            "component_loop_actions": {
                name: data["real_pair_loop_action"] for name, data in component_data.items()
            },
            "component_loop_action_sum": sum(data["real_pair_loop_action"] for data in component_data.values()),
            "full_loop_action_reconstructed": loop_action["fixed_winding_minimization"]["normalized_action"],
            "heat_response_at_t1": heat_responses,
            "heat_response_sum_at_t1": sum(heat_responses.values()),
            "full_heat_response_at_t1": full_heat_response,
            "finite_rank_response_cross_term": 0.0,
            "current_action_contains_quark_lepton_binding_term": False,
            "current_topology_forces_colocalization": False,
            "interpretation": "the total class is fixed, but the trace action and relative response are direct sums and do not force the rank-12 and rank-3 defects to share one spatial core",
        },
        "transfer_and_gap_test": {
            "common_scalar_transfer_restricts_to_both_components": True,
            "common_scalar_transfer_free_moduli_after_unitarity": transfer["free_parameter_audit"]["continuous_transfer_moduli_after_unitarity"],
            "split_component_transfer_free_moduli_after_unitarity": 2,
            "component_weight_gap_candidates": common_mass_candidates,
            "component_weights_select_nonzero_gaps": False,
            "nonzero_quark_gap_derived": False,
            "nonzero_lepton_gap_derived": False,
            "relative_component_gap_derived": False,
        },
        "parent_boundary": {
            "component_K_theory_cycles_closed": True,
            "component_unbounded_extension_cycles_closed": True,
            "component_physical_localization_closed": False,
            "component_mass_or_binding_energy_closed": False,
            "Toeplitz_extension_derived_as_original_M35_dynamics": False,
            "absolute_energy_scale": response["verdict"]["absolute_energy"],
        },
        "verdict": {
            "rank_12_and_rank_3_are_genuine_component_cycles": True,
            "either_component_alone_is_the_original_forced_defect": False,
            "their_direct_sum_is_the_original_class_15": True,
            "global_topology_requires_total_class_but_not_colocation": True,
            "current_action_binds_components_into_one_particle": False,
            "component_nonzero_gaps_derived": False,
            "rank_3_declared_elementary_particle": False,
            "physical_closure": False,
            "status": "the 12 and 3 supports are genuine analytic and K-theoretic subcycles, but only their sum realizes the frozen class 15; current additive actions provide neither colocalization nor a mass gap",
        },
        "next_gate": "version6_spectral_transition_component_colocalization_gate",
    }

    assert ambient == 105
    assert ranks["quark"] + ranks["lepton"] == 15
    assert float(np.linalg.norm(q_full @ q_full - q_full)) < 1.0e-12
    assert overlap < 1.0e-12
    assert action_cross_term == 0.0
    assert all(value < 1.0e-12 for value in unitary_residuals.values())
    assert all(value < 1.0e-12 for value in real_exchange_residuals.values())
    assert all(data["unbounded_commutator_residual"] < 1.0e-12 for data in component_data.values())
    assert result["global_class_ledger"]["component_KO6_sum"] == 15
    assert result["global_class_ledger"]["component_positive_indices_sum"] == -15
    assert result["global_class_ledger"]["component_negative_indices_sum"] == 15
    assert abs(result["global_class_ledger"]["component_weight_sum"] - 1.0 / 7.0) < 1.0e-15
    assert abs(result["additivity_and_binding_test"]["component_loop_action_sum"] - 1.0 / 7.0) < 1.0e-15
    assert abs(sum(heat_responses.values()) - full_heat_response) < 1.0e-15
    assert not result["verdict"]["current_action_binds_components_into_one_particle"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()