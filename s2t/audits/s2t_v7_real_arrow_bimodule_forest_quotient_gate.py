#!/usr/bin/env python3
"""Audit the Real arrow-module lift and the flavour-frame forest quotient."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_real_arrow_bimodule_forest_quotient_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def connected_components(vertices: list[str], edges: list[tuple[str, str]]) -> list[list[str]]:
    neighbours = {vertex: set() for vertex in vertices}
    for source, target in edges:
        neighbours[source].add(target)
        neighbours[target].add(source)
    unseen = set(vertices)
    components = []
    while unseen:
        root = min(unseen)
        stack = [root]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(neighbours[vertex] - component)
        unseen -= component
        components.append(sorted(component))
    return sorted(components)


def incidence_matrix(vertices: list[str], edges: list[tuple[str, str]]) -> np.ndarray:
    matrix = np.zeros((len(vertices), len(edges)))
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    for column, (source, target) in enumerate(edges):
        matrix[vertex_index[source], column] = -1.0
        matrix[vertex_index[target], column] = 1.0
    return matrix


def nullspace(matrix: np.ndarray, tolerance: float = 1.0e-12) -> np.ndarray:
    _, singular_values, right_vectors = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > tolerance))
    return right_vectors[rank:].conj().T


def main() -> None:
    graph = load_result("s2t_v7_four_vertex_vectorlike_selector_gate_results.json")
    hodge = load_result(
        "s2t_v7_edge_grading_hodge_superconnection_parent_gate_results.json"
    )
    assert hodge["verdict"]["status"] == (
        "positive_field_space_hodge_parent_physical_embedding_open"
    )

    edge_order = hodge["carrier"]["edge_count"]
    all_edges = graph["carrier"]["new_allowed_edges"]
    selected_names = graph["carrier"]["desired_cycle_plus_vector_masses"]
    assert edge_order == len(all_edges) == 11
    assert len(selected_names) == 6

    vertices = sorted({vertex for item in all_edges for vertex in item.split("--")})
    selected_edges = [tuple(item.split("--")) for item in selected_names]
    baseline_names = graph["carrier"]["baseline_edges"]
    baseline_edges = [tuple(item.split("--")) for item in baseline_names]
    full_edges = baseline_edges + selected_edges
    selected_components = connected_components(vertices, selected_edges)
    full_components = connected_components(vertices, full_edges)

    selected_incidence = incidence_matrix(vertices, selected_edges)
    baseline_incidence = incidence_matrix(vertices, baseline_edges)
    full_incidence = incidence_matrix(vertices, full_edges)
    incidence_rank = int(np.linalg.matrix_rank(selected_incidence))
    baseline_incidence_rank = int(np.linalg.matrix_rank(baseline_incidence))
    full_incidence_rank = int(np.linalg.matrix_rank(full_incidence))
    selected_cycle_rank = len(selected_edges) - len(vertices) + len(selected_components)
    full_cycle_rank = len(full_edges) - len(vertices) + len(full_components)
    assert len(vertices) == 9
    assert len(selected_components) == 3
    assert len(full_components) == 1
    assert incidence_rank == 6
    assert baseline_incidence_rank == 3
    assert full_incidence_rank == 8
    assert selected_cycle_rank == 0
    assert full_cycle_rank == 1

    # At Z_e=mu I_3 a vertex flavour-frame change gives delta Z_e=xi_t-xi_s.
    # Because H15 is frozen, admissible frame changes must first preserve its
    # three baseline edges.  Restrict the new-edge incidence map to that
    # kernel.  The remaining cokernel is the holonomy of the single cycle in
    # the full baseline-plus-selected graph.
    flavour_generator_dimension = 9
    baseline_kernel = nullspace(baseline_incidence.T)
    relative_frame_map = selected_incidence.T @ baseline_kernel
    relative_vertex_dimension = baseline_kernel.shape[1] * flavour_generator_dimension
    relative_orbit_rank = (
        int(np.linalg.matrix_rank(relative_frame_map)) * flavour_generator_dimension
    )
    full_stabilizer_dimension = (
        len(vertices) - full_incidence_rank
    ) * flavour_generator_dimension
    vacuum_zero_modes = hodge["family_lift"]["vacuum_hessian_signature"]["zero"]
    quotient_moduli_dimension = vacuum_zero_modes - relative_orbit_rank
    assert relative_vertex_dimension == 54
    assert relative_orbit_rank == 45
    assert full_stabilizer_dimension == 9
    assert vacuum_zero_modes == 54
    assert quotient_moduli_dimension == 9

    # The two edge-space projectors act on complete summands.  On two equal
    # copies of the edge module they commute with every diagonal central
    # action.  This is the finite-dimensional shadow of A-bimodule linearity.
    selected = set(selected_names)
    p_selected = np.diag([float(item in selected) for item in all_edges])
    p_unwanted = np.eye(len(all_edges)) - p_selected
    zero = np.zeros_like(p_selected)
    delta = np.block([[zero, p_selected], [p_unwanted, zero]])
    rng = np.random.default_rng(20260827)
    central_character = np.diag(rng.normal(size=len(all_edges)))
    doubled_action = np.block(
        [[central_character, zero], [zero, central_character]]
    )
    bimodule_commutator_residual = float(
        np.max(np.abs(delta @ doubled_action - doubled_action @ delta))
    )
    assert bimodule_commutator_residual < 1.0e-12

    # A dynamic family matrix also acts only on multiplicity space and hence
    # commutes with the represented finite algebra.  Consequently this arrow
    # superconnection is not generated as an ordinary inner one-form a[D,b].
    family_z = np.diag(
        rng.normal(size=len(all_edges)) + 1j * rng.normal(size=len(all_edges))
    )
    dynamic = np.block([[zero, zero], [family_z, zero]])
    dynamic_inner_commutator_residual = float(
        np.max(np.abs(dynamic @ doubled_action - doubled_action @ dynamic))
    )
    assert dynamic_inner_commutator_residual < 1.0e-12

    chain_grading = np.block(
        [[-np.eye(len(all_edges)), zero], [zero, np.eye(len(all_edges))]]
    )
    exchange = np.block([[zero, np.eye(len(all_edges))], [np.eye(len(all_edges)), zero]])
    odd_background = delta + delta.conj().T
    real_oddness_residual = float(
        np.max(np.abs(chain_grading @ odd_background + odd_background @ chain_grading))
    )
    assert real_oddness_residual < 1.0e-12
    assert np.max(np.abs(exchange @ chain_grading @ exchange + chain_grading)) < 1.0e-12

    result = {
        "gate": "version7_real_arrow_bimodule_forest_quotient_gate",
        "real_arrow_module": {
            "carrier": "E_new^0 direct_sum E_new^1 with formal orientation-reversed Real partner",
            "edge_summands": len(all_edges),
            "projectors_act_on_complete_bimodule_summands": True,
            "background_delta_is_odd": True,
            "background_delta_is_nilpotent": bool(np.max(np.abs(delta @ delta)) < 1.0e-12),
            "central_bimodule_commutator_residual": bimodule_commutator_residual,
            "Real_exchange_reverses_chain_grading": True,
            "Real_oddness_residual": real_oddness_residual,
            "auxiliary_first_order_condition": "trivial because delta is A-bimodule linear",
        },
        "ordinary_inner_fluctuation_test": {
            "dynamic_central_commutator_residual": dynamic_inner_commutator_residual,
            "ordinary_one_form_span_from_auxiliary_operator": "zero",
            "is_standard_finite_Dirac_inner_fluctuation": False,
            "requires_new_physical_fermion_vertices": False,
            "valid_status": "Real equivariant arrow-space superconnection/correspondence",
        },
        "selected_vacuum_graph": {
            "vertices": vertices,
            "selected_edges": selected_names,
            "selected_components": selected_components,
            "vertex_count": len(vertices),
            "edge_count": len(selected_edges),
            "component_count": len(selected_components),
            "incidence_rank": incidence_rank,
            "cycle_rank": selected_cycle_rank,
            "is_forest": selected_cycle_rank == 0,
        },
        "full_graph_relative_to_frozen_H15": {
            "family_lift_assumption": "the current family-blind H15 lift uses unitary orientation I3 on each baseline edge",
            "baseline_edges": baseline_names,
            "all_nonzero_edges": baseline_names + selected_names,
            "components": full_components,
            "edge_count": len(full_edges),
            "incidence_rank": full_incidence_rank,
            "cycle_rank": full_cycle_rank,
            "unique_cycle_holonomy_dimension_for_U3": 9,
        },
        "family_frame_quotient": {
            "vertex_frame_group": "product over nine vertices U(3)_v",
            "vertex_frame_group_real_dimension": len(vertices) * flavour_generator_dimension,
            "frames_preserving_frozen_H15_dimension": relative_vertex_dimension,
            "linearized_action": "delta Z_e=xi_t-xi_s",
            "orbit_dimension_on_new_edges_relative_to_H15": relative_orbit_rank,
            "full_graph_stabilizer": "one diagonal U(3) on the connected graph",
            "full_graph_stabilizer_real_dimension": full_stabilizer_dimension,
            "hessian_zero_modes": vacuum_zero_modes,
            "frame_vertical_zero_modes": relative_orbit_rank,
            "relative_cycle_zero_modes": quotient_moduli_dimension,
            "all_hessian_zero_modes_are_frame_vertical": False,
            "linearized_quotient_dimension_at_identity": quotient_moduli_dimension,
            "holonomy_representative": "one U(3) matrix around the unique H15-rooted cycle",
            "nonlinear_frame_quotient": "U(3)/Ad U(3)",
            "generic_conjugacy_class_dimension": 3,
            "class_invariants": "three eigenphases before any further spectral potential",
            "nontrivial_CKM_PMNS_from_unitary_orientations": False,
        },
        "remaining_physical_gap": {
            "physical_gauge_group_equals_vertex_frame_group": False,
            "basis_quotient_is_not_new_gauge_boson_dynamics": True,
            "overall_scale_mu_derived": False,
            "nondegenerate_family_singular_values_derived": False,
            "quotient_recomputed_for_nondegenerate_H15_family_matrices": False,
            "physical_mixing_observable_derived": False,
            "standard_almost_commutative_spectral_triple_embedding": False,
        },
        "verdict": {
            "status": "positive_real_arrow_correspondence_partial_frame_quotient_one_cycle_holonomy_physical_inner_fluctuation_no_go",
            "two_colours_have_one_Real_arrow_module": True,
            "family_orientation_zero_modes_closed_as_frame_redundancy": False,
            "family_orientation_zero_modes_reduced_from_54_to_9": True,
            "complete_physical_spectral_parent_obtained": False,
            "next_gate": "test whether the unique U(3) cycle holonomy enters a derived spectral invariant and whether the moment-map level mu follows from the frozen H15 background",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()