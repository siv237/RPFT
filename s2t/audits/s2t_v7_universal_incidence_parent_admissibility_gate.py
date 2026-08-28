#!/usr/bin/env python3
"""Audit basis independence of the proposed universal incidence selector."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_universal_incidence_parent_admissibility_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def main() -> None:
    previous = load_result("s2t_v7_modular_copy_projector_origin_gate_results.json")
    assert previous["architectural_status"]["status"] == "conditional_positive_parity_selector"

    identity = np.eye(2, dtype=complex)
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sigma_y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    paulis = [identity, sigma_x, sigma_y, sigma_z]
    minus = (identity - sigma_x) / 2.0

    def twirl(matrix: np.ndarray, group: list[np.ndarray]) -> np.ndarray:
        return sum(unitary @ matrix @ unitary.conj().T for unitary in group) / len(group)

    pauli_twirl_exchange = twirl(sigma_x, paulis)
    pauli_twirl_minus = twirl(minus, paulis)
    assert np.linalg.norm(pauli_twirl_exchange) < 1e-12
    assert np.linalg.norm(pauli_twirl_minus - identity / 2.0) < 1e-12

    # A finite dihedral subgroup already tests the surviving Real/O(2)
    # covariance: rotations by multiples of pi/2 and their reflections.
    reflection = sigma_z.real
    orthogonal_group = []
    for step in range(4):
        angle = step * np.pi / 2.0
        rotation = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=complex,
        )
        orthogonal_group.extend([rotation, reflection @ rotation])
    orthogonal_twirl_exchange = twirl(sigma_x, orthogonal_group)
    orthogonal_twirl_minus = twirl(minus, orthogonal_group)
    assert np.linalg.norm(orthogonal_twirl_exchange) < 1e-12
    assert np.linalg.norm(orthogonal_twirl_minus - identity / 2.0) < 1e-12

    # Independent allowed arrows produce an incoherent covariance.  Three
    # common neighbours multiply it by three but do not create cross terms.
    e1 = np.array([[1.0], [0.0]], dtype=complex)
    e2 = np.array([[0.0], [1.0]], dtype=complex)
    one_neighbour_incoherent = e1 @ e1.conj().T + e2 @ e2.conj().T
    three_neighbour_incoherent = 3.0 * one_neighbour_incoherent
    assert np.linalg.norm(one_neighbour_incoherent - identity) < 1e-12
    assert np.linalg.norm(three_neighbour_incoherent - 3.0 * identity) < 1e-12
    incoherent_selector = three_neighbour_incoherent / 3.0 - identity
    assert np.linalg.norm(incoherent_selector) < 1e-12

    # The labeled binary graph instead inserts a coherent vector e1+e2.
    coherent = e1 + e2
    one_neighbour_coherent = coherent @ coherent.conj().T
    three_neighbour_coherent = 3.0 * one_neighbour_coherent
    coherent_selector = three_neighbour_coherent / 3.0 - identity
    assert np.linalg.norm(coherent_selector - sigma_x) < 1e-12

    phase_samples = []
    for phase in np.linspace(0.0, 2.0 * np.pi, 17):
        vector = e1 + np.exp(1j * phase) * e2
        selector = vector @ vector.conj().T - identity
        expected = np.array(
            [[0.0, np.exp(-1j * phase)], [np.exp(1j * phase), 0.0]],
            dtype=complex,
        )
        residual = float(np.linalg.norm(selector - expected))
        assert residual < 1e-12
        phase_samples.append(
            {
                "phase": float(phase),
                "selector_real": selector.real.tolist(),
                "selector_imag": selector.imag.tolist(),
                "formula_residual": residual,
            }
        )

    # Generic copy rotations leave the represented algebra pi0 tensor I2
    # unchanged but rotate the proposed exchange operator.
    rotations = []
    maximum_exchange_displacement = 0.0
    for theta in np.linspace(0.0, np.pi / 2.0, 17):
        unitary = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]],
            dtype=complex,
        )
        moved = unitary @ sigma_x @ unitary.conj().T
        displacement = float(np.linalg.norm(moved - sigma_x, "fro"))
        maximum_exchange_displacement = max(maximum_exchange_displacement, displacement)
        rotations.append({"theta": float(theta), "exchange_displacement": displacement})
    assert maximum_exchange_displacement > 2.8

    commutator_residuals = {
        "with_sigma_x": float(np.linalg.norm(sigma_x @ sigma_x - sigma_x @ sigma_x)),
        "with_sigma_y": float(np.linalg.norm(sigma_x @ sigma_y - sigma_y @ sigma_x)),
        "with_sigma_z": float(np.linalg.norm(sigma_x @ sigma_z - sigma_z @ sigma_x)),
    }
    assert commutator_residuals["with_sigma_y"] > 2.8
    assert commutator_residuals["with_sigma_z"] > 2.8

    result = {
        "gate": "version7_universal_incidence_parent_admissibility_gate",
        "isotypic_symmetry": {
            "multiplicity_space": "C2",
            "complex_basis_group": "U2",
            "Real_basis_group": "O2",
            "canonical_endomorphism_commutant": "C times I2",
            "exchange_commutators": commutator_residuals,
            "maximum_exchange_displacement_under_real_rotations": maximum_exchange_displacement,
            "rotation_samples": rotations,
        },
        "allowed_arrow_covariance": {
            "one_common_neighbour_incoherent": one_neighbour_incoherent.real.tolist(),
            "three_common_neighbours_incoherent": three_neighbour_incoherent.real.tolist(),
            "derived_incoherent_selector": incoherent_selector.real.tolist(),
            "one_common_neighbour_coherent": one_neighbour_coherent.real.tolist(),
            "three_common_neighbours_coherent": three_neighbour_coherent.real.tolist(),
            "derived_coherent_selector": coherent_selector.real.tolist(),
            "coherent_relative_phase_was_fixed_by_first_order": False,
            "phase_orbit": phase_samples,
        },
        "twirling": {
            "pauli_exchange_residual": float(np.linalg.norm(pauli_twirl_exchange)),
            "pauli_projector_to_half_identity_residual": float(
                np.linalg.norm(pauli_twirl_minus - identity / 2.0)
            ),
            "orthogonal_exchange_residual": float(np.linalg.norm(orthogonal_twirl_exchange)),
            "orthogonal_projector_to_half_identity_residual": float(
                np.linalg.norm(orthogonal_twirl_minus - identity / 2.0)
            ),
        },
        "universal_calculus": {
            "allowed_block_space_is_canonical": True,
            "canonical_nonzero_element_of_each_block_space": False,
            "represented_forms_require_D": True,
            "binary_support_implies_equal_amplitudes": False,
            "binary_support_implies_common_phase": False,
        },
        "verdict": {
            "previous_modular_parity_calculation_mathematically_valid_conditionally": True,
            "maximal_binary_incidence_derived_from_current_parent": False,
            "basis_independent_copy_selector_obtained": False,
            "status": "closed_as_internal_universal_incidence_parent",
            "missing_object": "rank-one coherent covariance or condensate on the allowed-arrow multiplicity space",
            "next_gate": "derive or exclude a rank-one edge-coherence condensate from one invariant action and test its full Hessian and Real completion",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()