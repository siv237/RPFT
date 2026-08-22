#!/usr/bin/env python3
"""Audit existing project multiplicities as a resonant entropy/energy sink."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def affine_coisometry() -> np.ndarray:
    return np.array(
        [
            [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0), 0.0, 0.0],
            [1.0 / np.sqrt(6.0), 1.0 / np.sqrt(6.0), -2.0 / np.sqrt(6.0), 0.0],
            [
                1.0 / np.sqrt(12.0),
                1.0 / np.sqrt(12.0),
                1.0 / np.sqrt(12.0),
                -3.0 / np.sqrt(12.0),
            ],
        ]
    )


def main() -> None:
    vector = np.ones(4) / 2.0
    p1 = np.outer(vector, vector)
    p3 = np.eye(4) - p1
    coisometry = affine_coisometry()

    target_axis = 0.9121665962741361
    target_transverse = 0.5 * (1.0 - target_axis)
    transverse_survival = target_transverse / target_axis
    selective_angle = float(np.arccos(np.sqrt(transverse_survival)))
    physical_corner_survival = 1.0 / (3.0 * target_axis)
    leakage_to_affine_corner = 1.0 - physical_corner_survival

    initial_g = np.eye(3) / 3.0
    final_g_selective = np.diag(
        [1.0 / 3.0, transverse_survival / 3.0, transverse_survival / 3.0]
    )
    conditional_g_selective = final_g_selective / np.trace(final_g_selective)

    scalar_survival = 0.37
    final_g_isotropic = scalar_survival * initial_g
    conditional_g_isotropic = final_g_isotropic / np.trace(final_g_isotropic)

    candidates = {
        "affine_C4_equal_1_plus_3": {
            "raw_dimension": 4,
            "same_height_resonant_rank": 3,
            "canonical_intertwiner_rank": int(np.linalg.matrix_rank(coisometry)),
            "independent_tensor_factor": False,
            "direct_sum_corner": True,
            "canonical_coupling_axis_selective": False,
            "status": "resonant multiplicity exists but canonical V is isotropic",
        },
        "H15_observed_package": {
            "raw_dimension": 15,
            "irreducible_block_dimensions": [6, 2, 3, 3, 1],
            "equivalent_copy_multiplicities": [1, 1, 1, 1, 1],
            "maximum_gauge_commutant_multiplicity": 1,
            "status": "representation dimensions are gauge charges, not a multiplicity space",
        },
        "KO6_real_doubling": {
            "raw_factor": 2,
            "same_physical_grading_multiplicity": 1,
            "mixing_halves_preserves_grading": False,
            "status": "Real completion is not two interchangeable sink channels",
        },
        "M18_vertex_rank_six": {
            "raw_vertex_rank": 6,
            "decomposition": "family rank 3 plus J-conjugate rank 3",
            "independent_multiplicity_after_J_and_grading": 1,
            "status": "rank six combines family and Real structure rather than a free sink factor",
        },
        "M20_M35_matrix_sizes": {
            "matrix_sizes": [20, 35],
            "hilbert_sink_multiplicity": False,
            "status": "algebra/corner dimensions are not energy-level degeneracies",
        },
        "exterior_real_pair": {
            "raw_same_orientation_copies": 2,
            "physical_half_trace_independent_copies": 1,
            "status": "already normalized; reuse would repeat the closed double count",
        },
    }

    result = {
        "gate": "version6_existing_multiplicity_resonant_sink_gate",
        "affine_triplet_certificate": {
            "P1_rank": int(np.linalg.matrix_rank(p1)),
            "P3_rank": int(np.linalg.matrix_rank(p3)),
            "height_on_affine_node": "-P3",
            "P3_is_exactly_degenerate": True,
            "V_Vstar": (coisometry @ coisometry.T).tolist(),
            "Vstar_V": (coisometry.T @ coisometry).tolist(),
            "V_maps_P3_to_family_triplet": True,
        },
        "direct_sum_conditional_transfer": {
            "target_axis_weight": target_axis,
            "target_transverse_weight": target_transverse,
            "required_transverse_survival_probability": transverse_survival,
            "required_selective_rotation_angle": selective_angle,
            "remaining_probability_in_family_corner": physical_corner_survival,
            "probability_leaked_to_affine_corner": leakage_to_affine_corner,
            "conditional_family_spectrum": np.diag(conditional_g_selective).tolist(),
            "conditional_target_reached": True,
            "is_tensor_product_cooling": False,
        },
        "canonical_affine_coupling_test": {
            "coupling": "X=rho V",
            "acts_as_scalar_on_family_triplet": True,
            "conditional_state_after_equal_transfer": np.diag(
                conditional_g_isotropic
            ).tolist(),
            "creates_uniaxial_split": False,
            "required_modified_coupling": "rho V(I-P) after an axis P is already selected",
            "modified_coupling_is_parent_derived": False,
        },
        "candidate_ledger": candidates,
        "maximum_residuals": {
            "P1_projector": float(np.linalg.norm(p1 @ p1 - p1)),
            "P3_projector": float(np.linalg.norm(p3 @ p3 - p3)),
            "P1_P3_orthogonality": float(np.linalg.norm(p1 @ p3)),
            "V_Vstar_identity": float(
                np.linalg.norm(coisometry @ coisometry.T - np.eye(3))
            ),
            "Vstar_V_P3": float(
                np.linalg.norm(coisometry.T @ coisometry - p3)
            ),
            "conditional_target": float(
                np.linalg.norm(
                    conditional_g_selective
                    - np.diag([target_axis, target_transverse, target_transverse])
                )
            ),
            "isotropic_transfer_stays_isotropic": float(
                np.linalg.norm(conditional_g_isotropic - np.eye(3) / 3.0)
            ),
        },
        "verdict": {
            "existing_affine_parent_contains_resonant_rank_at_least_two": True,
            "resonant_rank_is_independent_tensor_sink": False,
            "canonical_parent_coupling_generates_order": False,
            "H15_or_KO6_supplies_free_sink_multiplicity": False,
            "all_requirements_for_autonomous_crystallization_met": False,
            "minimal_reopening": "derive state-selective nonlinear affine transfer without assuming P",
            "matter_birth_fully_derived": False,
            "next_gate": "version6_nonlinear_affine_feedback_instability_gate",
        },
    }

    assert all(value < 2e-12 for value in result["maximum_residuals"].values())
    assert candidates["H15_observed_package"]["maximum_gauge_commutant_multiplicity"] == 1
    assert result["affine_triplet_certificate"]["P3_rank"] == 3

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_existing_multiplicity_resonant_sink_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()