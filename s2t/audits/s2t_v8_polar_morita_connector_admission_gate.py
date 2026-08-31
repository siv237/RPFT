#!/usr/bin/env python3
"""Audit the canonical polar Morita connector suggested by Tome VII."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks
from s2t_v7_incidence_transfer_markov_weight_gate import polar_coisometry
from s2t_v7_weak_aligned_cycle_competition_gate import DIMS


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_polar_morita_connector_admission_gate_results.json"
TOL = 1.0e-10


def block_diagonal(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    result = np.zeros(
        (first.shape[0] + second.shape[0], first.shape[1] + second.shape[1]),
        dtype=complex,
    )
    result[: first.shape[0], : first.shape[1]] = first
    result[first.shape[0] :, first.shape[1] :] = second
    return result


def random_unitary(rng: np.random.Generator, dimension: int) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, triangular = np.linalg.qr(raw)
    phases = np.diag(triangular)
    return unitary @ np.diag(np.conj(phases / np.abs(phases)))


def main() -> None:
    reference, _, _, _ = physical_blocks()
    transfer, support, defect = polar_coisometry(reference)
    source = reference.shape[1]
    target = reference.shape[0]
    edge_dimension = 2 * source
    endpoint_dimension = source + target

    identity_source = np.eye(source)
    zero_source_target = np.zeros((source, target))
    zero_source = np.zeros((source, source))

    # K_E=C^11+C^11 and K_V=C^11+C^10 share the first source copy.
    # The polar coisometry supplies the only missing block C^10 -> C^11.
    connector = np.block([
        [identity_source, zero_source_target],
        [zero_source, transfer.conj().T],
    ])
    connector_initial = connector.conj().T @ connector
    connector_final = connector @ connector.conj().T
    expected_final = block_diagonal(identity_source, support)

    # The self-adjoint edge background is the exchange of the two C^11 copies.
    edge_exchange = np.block([
        [zero_source, identity_source],
        [identity_source, zero_source],
    ])
    endpoint_exchange = np.block([
        [np.zeros((source, source)), transfer.conj().T],
        [transfer, np.zeros((target, target))],
    ])
    compressed_intertwining = edge_exchange @ connector - connector @ endpoint_exchange
    expected_compressed_defect = np.block([
        [np.zeros((source, source)), np.zeros((source, target))],
        [defect, np.zeros((source, target))],
    ])

    # Complete the target by the already existing index-defect line ker(A0).
    defect_values, defect_vectors = np.linalg.eigh(defect)
    defect_vector = defect_vectors[:, np.argmax(defect_values)].reshape(source, 1)
    completed_polar_unitary = np.column_stack([transfer.conj().T, defect_vector])
    completed_connector = block_diagonal(identity_source, completed_polar_unitary)
    completed_endpoint_exchange = np.block([
        [zero_source, completed_polar_unitary],
        [completed_polar_unitary.conj().T, zero_source],
    ])
    completed_intertwining = (
        edge_exchange @ completed_connector
        - completed_connector @ completed_endpoint_exchange
    )

    # In the natural two-block polar ansatz the relative phase is the only
    # continuous ambiguity after imposing the isometry condition.  Background
    # intertwining fixes that phase; the remaining mismatch is exactly Q.
    phase_samples = np.linspace(-np.pi, np.pi, 257)
    phase_residuals_squared = []
    maximum_phase_formula_residual = 0.0
    for phase in phase_samples:
        phased = np.block([
            [identity_source, zero_source_target],
            [zero_source, np.exp(1j * phase) * transfer.conj().T],
        ])
        residual_squared = float(
            np.linalg.norm(edge_exchange @ phased - phased @ endpoint_exchange) ** 2
        )
        expected = 1.0 + 40.0 * (1.0 - np.cos(phase))
        maximum_phase_formula_residual = max(
            maximum_phase_formula_residual, abs(residual_squared - expected)
        )
        phase_residuals_squared.append(residual_squared)
    minimizing_phase = float(phase_samples[int(np.argmin(phase_residuals_squared))])

    # A single nonzero off-diagonal element is cyclic for the full left/right
    # matrix actions: E_ap T E_qb spans every matrix unit in M_22x21.
    pivot = np.unravel_index(np.argmax(np.abs(connector)), connector.shape)
    pivot_value = connector[pivot]
    orbit_vectors = []
    for row in range(edge_dimension):
        for column in range(endpoint_dimension):
            matrix_unit = np.zeros_like(connector)
            matrix_unit[row, column] = pivot_value
            orbit_vectors.append(matrix_unit.reshape(-1))
    orbit_span = np.column_stack(orbit_vectors)
    orbit_span_rank = int(np.linalg.matrix_rank(orbit_span, tol=TOL))

    # The commutant of M22+M21 consists of two corner scalars.  Commuting with
    # any nonzero connector imposes equality of those scalars.
    central_constraint = np.array([[np.linalg.norm(connector), -np.linalg.norm(connector)]])
    linked_commutant_dimension = 2 - int(np.linalg.matrix_rank(central_constraint, tol=TOL))

    # Naturality under independent changes of source and target bases.
    rng = np.random.default_rng(20260828)
    maximum_covariance_residual = 0.0
    for _ in range(20):
        source_unitary = random_unitary(rng, source)
        target_unitary = random_unitary(rng, target)
        transformed_reference = target_unitary @ reference @ source_unitary.conj().T
        transformed_transfer, _, _ = polar_coisometry(transformed_reference)
        transformed_connector = np.block([
            [identity_source, zero_source_target],
            [zero_source, transformed_transfer.conj().T],
        ])
        edge_change = block_diagonal(source_unitary, source_unitary)
        endpoint_change = block_diagonal(source_unitary, target_unitary)
        covariant_image = edge_change @ connector @ endpoint_change.conj().T
        maximum_covariance_residual = max(
            maximum_covariance_residual,
            float(np.linalg.norm(transformed_connector - covariant_image)),
        )

    edge_data = json.loads((
        ROOT / "s2t/results/s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json"
    ).read_text(encoding="utf-8"))
    edge_labels = edge_data["edge_space"]["ordered_new_edges"]
    canonical_name = {
        "Q_L": "QL", "L_L": "LL", "u_R": "uR", "d_R": "dR",
        "e_R": "eR", "X_L": "XL", "X_R": "XR", "Y_L": "YL",
        "Y_R": "YR",
    }
    full_arrow_module_dimension = sum(
        DIMS[canonical_name[first]] * DIMS[canonical_name[second]]
        for first, second in (label.split("--") for label in edge_labels)
    )

    # Red-team the hidden I11.  The first C11 is an edge-label multiplicity
    # space, whereas the second is the physical left-state space.  Replacing
    # the coordinate identification by any j in U(11) preserves all formal
    # isometry and defect identities, so the old data do not select j.
    identification_residuals = []
    identification_separations = []
    identifications = [random_unitary(rng, source) for _ in range(8)]
    for identification in identifications:
        candidate = np.block([
            [identification, zero_source_target],
            [zero_source, identification @ transfer.conj().T],
        ])
        identification_residuals.append(float(np.linalg.norm(
            edge_exchange @ candidate - candidate @ endpoint_exchange
        )))
    for first, second in zip(identifications, identifications[1:]):
        identification_separations.append(float(np.linalg.norm(first - second)))

    connector_initial_residual = float(
        np.linalg.norm(connector_initial - np.eye(endpoint_dimension))
    )
    connector_final_residual = float(np.linalg.norm(connector_final - expected_final))
    compressed_defect_residual = float(
        np.linalg.norm(compressed_intertwining - expected_compressed_defect)
    )
    completed_unitarity_residual = float(
        np.linalg.norm(
            completed_polar_unitary.conj().T @ completed_polar_unitary
            - np.eye(source)
        )
    )
    completed_intertwining_residual = float(np.linalg.norm(completed_intertwining))

    assert reference.shape == (10, 11)
    assert edge_dimension == 22 and endpoint_dimension == 21
    assert np.linalg.matrix_rank(connector, TOL) == 21
    assert connector_initial_residual < TOL
    assert connector_final_residual < TOL
    assert np.linalg.matrix_rank(np.eye(edge_dimension) - connector_final, TOL) == 1
    assert compressed_defect_residual < TOL
    assert abs(np.linalg.norm(compressed_intertwining) - 1.0) < TOL
    assert completed_unitarity_residual < TOL
    assert completed_intertwining_residual < TOL
    assert maximum_phase_formula_residual < 1.0e-9
    assert abs(minimizing_phase) < TOL
    assert orbit_span_rank == edge_dimension * endpoint_dimension == 462
    assert linked_commutant_dimension == 1
    assert maximum_covariance_residual < 1.0e-10
    assert full_arrow_module_dimension == 36
    assert max(abs(value - 1.0) for value in identification_residuals) < TOL
    assert min(identification_separations) > 2.0

    result = {
        "gate": "version8_polar_morita_connector_admission_gate",
        "existing_carriers": {
            "edge_hodge_decomposition": [source, source],
            "linking_endpoint_decomposition": [source, target],
            "edge_dimension": edge_dimension,
            "linking_endpoint_dimension": endpoint_dimension,
            "reference_incidence_shape": list(reference.shape),
            "reference_incidence_rank": int(np.linalg.matrix_rank(reference, TOL)),
            "index_defect_rank": int(np.linalg.matrix_rank(defect, TOL)),
        },
        "canonical_polar_connector": {
            "formula": "T_j=diag(j,jU*) after choosing j:C11_state->C11_edge_labels",
            "shape": list(connector.shape),
            "rank": int(np.linalg.matrix_rank(connector, TOL)),
            "initial_projection_residual": connector_initial_residual,
            "final_projection_residual": connector_final_residual,
            "cokernel_dimension": int(
                np.linalg.matrix_rank(np.eye(edge_dimension) - connector_final, TOL)
            ),
            "maximum_basis_covariance_residual": maximum_covariance_residual,
            "new_continuous_matrix_parameters_if_j_is_not_derived": 121,
        },
        "physical_typing_red_team": {
            "edge_C11_meaning": "multiplicity space of eleven arrow labels",
            "linking_source_C11_meaning": "physical left-state space QL+LL+XL+YL",
            "same_dimension_implies_same_module": False,
            "identity_I11_derived": False,
            "full_physical_arrow_module_complex_dimension": full_arrow_module_dimension,
            "compressed_edge_label_dimension": len(edge_labels),
            "tested_unitary_identifications": len(identifications),
            "all_identifications_have_same_hodge_defect_norm": identification_residuals,
            "minimum_separation_between_tested_identifications": min(
                identification_separations
            ),
            "identification_moduli": "U(11)",
            "identification_moduli_real_dimension": source * source,
        },
        "hodge_background_compatibility": {
            "compressed_intertwining_residual_norm": float(
                np.linalg.norm(compressed_intertwining)
            ),
            "compressed_residual_equals_index_defect": True,
            "compressed_defect_identity_residual": compressed_defect_residual,
            "polar_ansatz_complex_dimension_before_isometry": 2,
            "relative_phase_after_isometry": "one U(1)",
            "phase_residual_squared_formula": "1+40*(1-cos(phi))",
            "maximum_phase_formula_residual": maximum_phase_formula_residual,
            "minimizing_relative_phase": minimizing_phase,
            "relative_phase_fixed_by_background_intertwining": True,
        },
        "index_defect_completion": {
            "completed_target": "C10 direct_sum ker(A0)",
            "completed_polar_map": "[U*, inclusion_ker] : C10+ker(A0) -> C11",
            "completed_map_unitarity_residual": completed_unitarity_residual,
            "completed_connector_shape": list(completed_connector.shape),
            "completed_background_intertwining_residual": completed_intertwining_residual,
            "requires_choice_of_defect_line": False,
            "coordinate_defect_vector_phase_is_gauge": True,
        },
        "morita_generation": {
            "diagonal_factor": "M22(C) direct_sum M21(C)",
            "offdiagonal_module_dimension": edge_dimension * endpoint_dimension,
            "single_connector_left_right_orbit_span_rank": orbit_span_rank,
            "commutant_dimension_before_connector": 2,
            "commutant_dimension_after_connector": linked_commutant_dimension,
            "generated_star_algebra_with_full_diagonal_factors": "M43(C)",
            "four_hundred_sixty_two_independent_inputs_required_after_j_choice": False,
        },
        "trace_and_physical_boundary": {
            "M43_normalized_corner_weights": ["22/43", "21/43"],
            "raw_corner_trace_coefficients_equal": True,
            "simple_factor_trace_unique_if_unproved_identification_j_is_admitted": True,
            "connector_lives_on_auxiliary_field_curvature_carriers": True,
            "fermionic_finite_spectral_triple_embedding_proved": False,
            "full_connector_superconnection_hessian_computed": False,
            "unique_physical_mass_metric_derived": False,
        },
        "verdict": {
            "canonical_existing_data_connector_found": False,
            "dimension_462_is_module_dimension_not_parameter_count": True,
            "algebraic_simple_completion_obtained_conditionally": True,
            "index_defect_is_the_only_compressed_hodge_mismatch": True,
            "edge_state_module_identification_derived": False,
            "pre_tome_direction_admitted": False,
            "complete_physical_parent_obtained": False,
            "status": "compressed_dimension_coincidence_no_go_physical_intertwiner_open",
            "next_gate": "version8_physical_arrow_endpoint_intertwiner_classification_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()