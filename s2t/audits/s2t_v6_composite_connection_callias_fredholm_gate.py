#!/usr/bin/env python3
"""Audit Callias/Fredholm carriers for the composite projective defect."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


SIGMA = [
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
    np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex),
    np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex),
]


def chern_number(projector_type: str, theta_steps: int = 160, phi_steps: int = 320) -> float:
    delta_theta = np.pi / theta_steps
    delta_phi = 2.0 * np.pi / phi_steps
    total = 0.0j
    for theta_index in range(theta_steps):
        theta = (theta_index + 0.5) * delta_theta
        sine_theta, cosine_theta = np.sin(theta), np.cos(theta)
        for phi_index in range(phi_steps):
            phi = (phi_index + 0.5) * delta_phi
            sine_phi, cosine_phi = np.sin(phi), np.cos(phi)
            director = np.array(
                [sine_theta * cosine_phi, sine_theta * sine_phi, cosine_theta]
            )
            theta_derivative = np.array(
                [cosine_theta * cosine_phi, cosine_theta * sine_phi, -sine_theta]
            )
            phi_derivative = np.array(
                [-sine_theta * sine_phi, sine_theta * cosine_phi, 0.0]
            )
            if projector_type == "spinor":
                projector = 0.5 * (
                    np.eye(2) + sum(director[index] * SIGMA[index] for index in range(3))
                )
                derivative_theta = 0.5 * sum(
                    theta_derivative[index] * SIGMA[index] for index in range(3)
                )
                derivative_phi = 0.5 * sum(
                    phi_derivative[index] * SIGMA[index] for index in range(3)
                )
            elif projector_type == "vector":
                projector = np.outer(director, director).astype(complex)
                derivative_theta = np.outer(theta_derivative, director) + np.outer(
                    director, theta_derivative
                )
                derivative_phi = np.outer(phi_derivative, director) + np.outer(
                    director, phi_derivative
                )
            else:
                raise ValueError(projector_type)
            curvature = np.trace(
                projector
                @ (derivative_theta @ derivative_phi - derivative_phi @ derivative_theta)
            )
            total += curvature * delta_theta * delta_phi / (2.0j * np.pi)
    return float(total.real)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    odd_result = json.loads(
        (root / "results" / "s2t_v5_hopf_pair_odd_core_extension_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    toeplitz_result = json.loads(
        (root / "results" / "s2t_v5_real_toeplitz_ko7_unitary_representative_gate_results.json").read_text(
            encoding="utf-8"
        )
    )

    vector_chern = chern_number("vector")
    spinor_chern = chern_number("spinor")
    coefficient_rank = int(toeplitz_result["unitary"]["coefficient_rank"])
    coefficient_chern = coefficient_rank * spinor_chern

    rectangular = odd_result["direct_rectangular_option"]["asymptotic_maximal_rank"]
    toeplitz_indices = toeplitz_result["toeplitz_boundary_indices"]

    result = {
        "gate": "version6_composite_connection_callias_fredholm_gate",
        "vector_Q_mass": {
            "asymptotic_mass": "Q/Delta with spectrum (2/3,-1/3,-1/3)",
            "asymptotically_invertible": True,
            "positive_eigenbundle": "complexification of the real director line",
            "global_real_section": "n",
            "numeric_first_chern_number": vector_chern,
            "Callias_index_magnitude": 0,
            "Fredholm_but_no_protected_chiral_zero_mode": True,
        },
        "spin_cover_mass": {
            "mass": "n dot sigma on an auxiliary complex rank-two carrier",
            "positive_eigenbundle": "Hopf line L",
            "numeric_first_chern_number": spinor_chern,
            "minimal_Callias_index_magnitude": 1,
            "coefficient_rank": coefficient_rank,
            "coefficient_first_chern_number": coefficient_chern,
            "coefficient_Callias_index_magnitude": coefficient_rank,
            "Real_conjugate_branch_has_opposite_orientation": True,
        },
        "finite_parent_carrier_obstruction": {
            "direct_odd_map": "C15 to C20",
            "asymptotic_rank": rectangular["rank"],
            "asymptotic_kernel": rectangular["kernel_T"],
            "asymptotic_cokernel": rectangular["cokernel_T"],
            "selfadjoint_asymptotic_nullity": rectangular["nullity_selfadjoint_Q"],
            "Callias_gap_condition": False,
            "derived_complex_linear_rank_two_spinor_carrier": False,
            "composite_connection_changes_fibre_rank": False,
        },
        "toeplitz_stable_index": {
            "KO7_real_unitary_exists": True,
            "boundary_indices": toeplitz_indices,
            "absolute_class": coefficient_rank,
            "same_integer_as_spin_cover_Callias_candidate": True,
            "spatial_Callias_operator_identified_with_Toeplitz_boundary": False,
            "localized_spatial_zero_modes_follow_from_Toeplitz_alone": False,
        },
        "verdict": {
            "natural_vector_Q_Callias_operator_is_Fredholm": True,
            "natural_vector_Q_index_is_nonzero": False,
            "spin_cover_candidate_has_index_one_per_coefficient_line": True,
            "project_coefficient_candidate_has_index_fifteen": True,
            "finite_parent_derives_required_spinor_mass": False,
            "stable_Toeplitz_class_supplies_same_index_number": True,
            "index_class_comparison_map_derived": False,
            "localized_fermionic_matter_fully_derived": False,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_callias_toeplitz_index_comparison_gate",
        },
    }

    assert abs(vector_chern) < 1e-12
    assert abs(spinor_chern - 1.0) < 2e-4
    assert rectangular["cokernel_T"] == 5
    assert sorted(abs(value) for value in toeplitz_indices) == [15, 15]

    output = root / "results" / "s2t_v6_composite_connection_callias_fredholm_gate_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()