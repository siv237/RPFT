#!/usr/bin/env python3
"""Identify the exact quantum-number content of the surviving bosonic Q defect."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_field_identification_gate_results.json"


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def standard_model_generators() -> list[np.ndarray]:
    zero_q = np.zeros((6, 6), dtype=complex)
    zero_l = np.zeros((2, 2), dtype=complex)
    zero_c = np.zeros((3, 3), dtype=complex)
    zero_e = np.zeros((1, 1), dtype=complex)
    identity2 = np.eye(2, dtype=complex)
    identity3 = np.eye(3, dtype=complex)

    gell_mann = [
        np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        np.diag([1, -1, 0]).astype(complex),
        np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
        np.diag([1, 1, -2]).astype(complex) / np.sqrt(3.0),
    ]
    pauli = [
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.diag([1, -1]).astype(complex),
    ]

    generators = []
    for matrix in gell_mann:
        color = matrix / 2.0
        generators.append(
            block_diag(np.kron(color, identity2), zero_l, color, color, zero_e)
        )
    for matrix in pauli:
        weak = matrix / 2.0
        generators.append(
            block_diag(np.kron(identity3, weak), weak, zero_c, zero_c, zero_e)
        )
    hypercharge = np.diag(
        [1 / 6] * 6 + [-1 / 2] * 2 + [2 / 3] * 3 + [-1 / 3] * 3 + [-1]
    ).astype(complex)
    generators.append(hypercharge)
    return generators


def symmetric_traceless_basis() -> list[np.ndarray]:
    basis = []
    basis.append(np.diag([2.0, -1.0, -1.0]) / np.sqrt(6.0))
    basis.append(np.diag([0.0, 1.0, -1.0]) / np.sqrt(2.0))
    for i, j in ((1, 2), (0, 2), (0, 1)):
        matrix = np.zeros((3, 3), dtype=float)
        matrix[i, j] = matrix[j, i] = 1.0 / np.sqrt(2.0)
        basis.append(matrix)
    return basis


def family_spin_two_generators() -> list[np.ndarray]:
    epsilon = np.zeros((3, 3, 3), dtype=float)
    epsilon[0, 1, 2] = epsilon[1, 2, 0] = epsilon[2, 0, 1] = 1.0
    epsilon[0, 2, 1] = epsilon[2, 1, 0] = epsilon[1, 0, 2] = -1.0
    rotations = [-epsilon[a] for a in range(3)]
    basis = symmetric_traceless_basis()
    representation = []
    for rotation in rotations:
        matrix = np.zeros((5, 5), dtype=float)
        for column, vector in enumerate(basis):
            image = commutator(rotation, vector)
            for row, test in enumerate(basis):
                matrix[row, column] = float(np.trace(test.T @ image))
        representation.append(matrix)
    return representation


def main() -> None:
    q = np.diag([2.0, -1.0, -1.0]) / np.sqrt(6.0)
    identity15 = np.eye(15, dtype=complex)
    identity3 = np.eye(3, dtype=complex)
    full_q = np.kron(q, identity15)
    gauge_generators = [np.kron(identity3, generator) for generator in standard_model_generators()]
    gauge_commutators = [float(np.linalg.norm(commutator(full_q, generator))) for generator in gauge_generators]

    spin_two = family_spin_two_generators()
    casimir = -sum(generator @ generator for generator in spin_two)
    invariant_equations = np.vstack(spin_two)
    singular_values = np.linalg.svd(invariant_equations, compute_uv=False)
    invariant_linear_dimension = 5 - int(np.sum(singular_values > 1e-10))

    rng = np.random.default_rng(20260820)
    projector_residuals = []
    for _ in range(200):
        vector = rng.normal(size=3)
        vector /= np.linalg.norm(vector)
        plus = np.outer(vector, vector)
        minus = np.outer(-vector, -vector)
        projector_residuals.append(float(np.linalg.norm(plus - minus)))

    eta = json.loads(
        (ROOT / "s2t/results/s2t_v5_eta_wzw_real_pair_phase_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    connection = json.loads(
        (ROOT / "s2t/results/s2t_v5_physical_corner_connection_classification_gate_results.json").read_text(
            encoding="utf-8"
        )
    )

    result = {
        "gate": "version6_bosonic_defect_field_identification_gate",
        "field_representation": {
            "field": "Q(x)=R(x)-I3/3",
            "spacetime_tensor_indices": 0,
            "current_spacetime_reading": "Lorentz scalar order parameter",
            "internal_family_representation": "real symmetric traceless rank-two tensor of SO(3)",
            "internal_dimension": 5,
            "family_casimir_residual_to_spin2_value_6": float(
                np.linalg.norm(casimir - 6.0 * np.eye(5))
            ),
            "standard_model_representation": "(1,1,0)",
            "maximum_SM_gauge_commutator_norm": max(gauge_commutators),
            "is_standard_model_Higgs_doublet": False,
            "is_spacetime_spin_two_field": False,
        },
        "portal_selection": {
            "trace_Q": float(np.trace(q)),
            "SO3_invariant_linear_functional_dimension": invariant_linear_dimension,
            "linear_SM_singlet_portal_preserving_family_SO3": False,
            "first_scalar_invariant": "Tr(Q^2)",
            "cubic_scalar_invariant": "Tr(Q^3)",
            "renormalizable_Higgs_portal": "Tr(Q^2) H^dagger H",
            "Higgs_portal_symmetry_allowed": True,
            "Higgs_portal_coefficient_parent_derived": False,
            "linear_gauge_kinetic_portal_from_common_trace": False,
            "quadratic_gauge_kinetic_portal": "Tr(Q^2) Tr(F_SM^2)",
            "quadratic_gauge_kinetic_portal_is_higher_dimension": True,
        },
        "fermion_coupling_boundary": {
            "possible_form": "sum_s y_s Q_ij bar(psi_s^i) psi_s^j",
            "observed_species_blocks": ["Q_L", "L_L", "u_R", "d_R", "e_R"],
            "minimum_independent_species_coefficients": connection["observed_block_restriction"][
                "commutant_complex_dimension"
            ],
            "centered_ambiguity_dimension": connection["observed_block_restriction"][
                "centered_commutant_complex_dimension"
            ],
            "current_parent_selects_unique_nonzero_coupling": False,
            "ordinary_inner_fluctuation_generates_family_Q_coupling": False,
        },
        "topological_charge_reading": {
            "vacuum_manifold": "RP2",
            "based_point_charge": "pi2(RP2)=Z",
            "lift_n_degree": 1,
            "lift_minus_n_degree": -1,
            "Q_projector_is_identical_for_opposite_lifts": True,
            "maximum_projector_difference_n_minus_n": max(projector_residuals),
            "intrinsic_unbased_bosonic_charge": "magnitude |k|; sign requires a lift/base orientation",
            "coefficient_magnitude_for_minimal_lift": 15,
            "oriented_plus_minus_15_is_intrinsic_to_Q_alone": False,
        },
        "statistics_and_observed_charge": {
            "color_charge": 0,
            "weak_isospin": 0,
            "hypercharge": 0,
            "electric_charge": 0,
            "baryon_or_lepton_number_parent_derived": False,
            "full_real_WZW_phase": eta["pfaffian_parity"]["full_real_pair"],
            "Pfaffian_line_orientation_derived": eta["pfaffian_parity"][
                "pfaffian_line_orientation_derived"
            ],
            "fermionic_Finkelstein_Rubinstein_constraint_derived": False,
            "quantum_statistics": "not derived; no present basis for calling the defect a fermion",
        },
        "verdict": {
            "surviving_object": "neutral bosonic family-quintet order parameter and its projective defects",
            "minimal_defect_is_standard_model_particle": False,
            "minimal_defect_is_gauge_neutral_dark_sector_candidate": True,
            "direct_SM_visibility": "only through uncomputed portal or nonunique family-fermion coupling",
            "oriented_particle_antiparticle_pair_from_Q_alone": False,
            "matter_field_identification_status": "neutral_bosonic_topological_candidate_not_observed_particle",
            "next_gate": "version6_bosonic_defect_collective_quantization_gate",
        },
    }

    assert result["field_representation"]["family_casimir_residual_to_spin2_value_6"] < 1e-12
    assert result["field_representation"]["maximum_SM_gauge_commutator_norm"] < 1e-12
    assert invariant_linear_dimension == 0
    assert max(projector_residuals) == 0.0
    assert result["statistics_and_observed_charge"]["full_real_WZW_phase"] == 1

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()