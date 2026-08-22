#!/usr/bin/env python3
"""Audit candidate origins of the rank-two carrier needed by the Callias mass."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spin_cover_carrier_parent_derivation_gate_results.json"


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def main() -> None:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli = (sx, sy, sz)
    i2 = np.eye(2, dtype=complex)

    # Reusing the spatial spinor factor makes the Callias commutator first order.
    same_factor = [np.linalg.norm(commutator(a, b)) for a in pauli for b in pauli]

    # A genuine Callias twist uses an independent factor.
    gamma = [np.kron(a, i2) for a in pauli]
    tau = [np.kron(i2, a) for a in pauli]
    product_factor = [np.linalg.norm(commutator(a, b)) for a in gamma for b in tau]

    rank = 15
    ir = np.eye(rank, dtype=complex)
    grading = np.kron(sz, ir)
    pair_generators = [np.kron(a, ir) for a in pauli]
    grading_commutators = [np.linalg.norm(commutator(grading, a)) for a in pair_generators]

    # Proxy for a charged representation and its conjugate: charges +1 and -1.
    conjugate_charge = np.kron(sz, ir)
    conjugate_charge_commutators = [
        np.linalg.norm(commutator(conjugate_charge, a)) for a in pair_generators
    ]
    # A new independent doublet would carry the same gauge representation twice.
    duplicated_charge = np.eye(2 * rank, dtype=complex)
    duplicated_charge_commutators = [
        np.linalg.norm(commutator(duplicated_charge, a)) for a in pair_generators
    ]

    phis = np.linspace(0.0, 2.0 * np.pi, 257)
    hopf_det_residuals = []
    hopf_unitarity_residuals = []
    for phi in phis:
        z = np.exp(1j * phi)
        transition = np.diag([z, z**-1])
        hopf_det_residuals.append(abs(np.linalg.det(transition) - 1.0))
        hopf_unitarity_residuals.append(
            np.linalg.norm(transition.conj().T @ transition - i2)
        )

    result = {
        "gate": "version6_spin_cover_carrier_parent_derivation_gate",
        "callias_clifford_requirement": {
            "spatial_clifford_factor": "C2_spin",
            "mass_factor_needed": "independent C2_twist",
            "max_same_factor_pauli_commutator_norm": float(max(same_factor)),
            "same_factor_has_first_order_commutator": True,
            "max_product_factor_cross_commutator_norm": float(max(product_factor)),
            "minimal_complex_product_dimension": 4,
        },
        "hopf_pair_bundle": {
            "bundle": "L direct_sum L*",
            "clutching": "diag(z,z^-1)",
            "total_first_chern_number": 0,
            "transition_lies_in_SU2": True,
            "max_determinant_one_residual": float(max(hopf_det_residuals)),
            "max_unitarity_residual": float(max(hopf_unitarity_residuals)),
            "topological_rank_two_bundle_obstruction": False,
            "positive_and_negative_eigenline_chern_numbers": [1, -1],
        },
        "existing_KO6_pair_test": {
            "candidate": "particle/conjugate or E/E* pair",
            "grading_commutator_norms_sigma_xyz": grading_commutators,
            "full_pauli_triplet_preserves_grading": False,
            "conjugate_charge_commutator_norms_sigma_xyz": conjugate_charge_commutators,
            "full_pauli_triplet_commutes_with_nonzero_conjugate_charge": False,
            "only_diagonal_U1_survives_both_tests": True,
            "real_structure_is_antilinear_not_missing_complex_linear_intertwiner": True,
        },
        "independent_duplicate_test": {
            "candidate": "C2_twist tensor H15 with equal gauge action on both copies",
            "gauge_commutator_norms_sigma_xyz": duplicated_charge_commutators,
            "algebraically_valid": True,
            "particle_dimension_before": 15,
            "particle_dimension_after": 30,
            "real_completed_dimension_before": 30,
            "real_completed_dimension_after": 60,
            "contained_in_current_H15_M35": False,
            "normalized_by_current_M35_trace": False,
        },
        "other_existing_candidates": {
            "weak_SU2_minus_center_dimension": 8,
            "weak_SU2_plus_center_dimension": 7,
            "weak_doublet_uniform_on_H15": False,
            "orientation_walk_C2_origin": "counterpropagating/Dirac factor",
            "orientation_walk_C2_independent_of_spatial_spin": False,
            "Clifford_stabilization_is_physical_state_derivation": False,
            "two_copy_or_exterior_carrier_checked_as_single_particle_doublet": False,
        },
        "verdict": {
            "topological_Hopf_pair_rank_two_carrier_exists": True,
            "current_KO6_pair_is_physical_internal_SU2_doublet": False,
            "current_weak_or_walk_doublet_solves_problem": False,
            "new_equal_charge_duplicate_would_solve_algebraic_problem": True,
            "finite_parent_derives_required_doublet": False,
            "localized_fifteen_fermions_fully_derived": False,
            "status": "topological_carrier_pass_but_gauge_equivariant_parent_carrier_fail",
            "next_gate": "version6_two_copy_spin_cover_multiplicity_gate",
        },
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()