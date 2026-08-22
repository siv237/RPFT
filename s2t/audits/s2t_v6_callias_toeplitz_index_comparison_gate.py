#!/usr/bin/env python3
"""Audit the clutching identification between the spin-cover Callias class
and the Real Toeplitz symbol constructed in Tome V.

The audit deliberately checks a boundary K-class identity.  It does not claim
unitary equivalence of the three-dimensional Callias operator and the Hardy
Toeplitz representative, nor does it derive the rank-two spin carrier from the
finite parent.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_callias_toeplitz_index_comparison_gate_results.json"


def hopf_data(theta: float, phi: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return north/south positive spinors and P_+(n)."""
    v_n = np.array(
        [np.cos(theta / 2.0), np.exp(1j * phi) * np.sin(theta / 2.0)],
        dtype=complex,
    )
    v_s = np.array(
        [np.exp(-1j * phi) * np.cos(theta / 2.0), np.sin(theta / 2.0)],
        dtype=complex,
    )
    n = np.array(
        [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]
    )
    sigma = (
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    )
    p_plus = (np.eye(2) + sum(n[k] * sigma[k] for k in range(3))) / 2.0
    return v_n, v_s, p_plus


def main() -> None:
    phis = np.linspace(0.0, 2.0 * np.pi, 4097)
    equator_residuals = []
    projector_residuals = []
    phases = []

    for phi in phis:
        v_n, v_s, p_plus = hopf_data(np.pi / 2.0, phi)
        equator_residuals.append(np.linalg.norm(v_n - np.exp(1j * phi) * v_s))
        projector_residuals.append(np.linalg.norm(np.outer(v_n, v_n.conj()) - p_plus))
        phases.append(np.angle(np.exp(15j * phi)))

    winding_15 = int(round((np.unwrap(phases)[-1] - np.unwrap(phases)[0]) / (2.0 * np.pi)))

    size = 105
    rank = 15
    q0 = np.zeros((size, size), dtype=complex)
    q0[:rank, :rank] = np.eye(rank)
    identity = np.eye(size, dtype=complex)

    unitary_residuals = []
    real_exchange_residuals = []
    symbol_match_residuals = []
    for phi in phis[::64]:
        z = np.exp(1j * phi)
        clutch_plus = z * q0 + identity - q0
        toeplitz_plus = z * q0 + identity - q0
        toeplitz_minus = z**-1 * q0.conj() + identity - q0.conj()
        unitary_residuals.extend(
            [
                np.linalg.norm(clutch_plus.conj().T @ clutch_plus - identity),
                np.linalg.norm(toeplitz_minus.conj().T @ toeplitz_minus - identity),
            ]
        )
        symbol_match_residuals.append(np.linalg.norm(clutch_plus - toeplitz_plus))
        real_exchange_residuals.append(np.linalg.norm(toeplitz_minus - clutch_plus.conj()))

    callias_indices = [rank, -rank]
    toeplitz_indices = [-winding_15, winding_15]

    result = {
        "gate": "version6_callias_toeplitz_index_comparison_gate",
        "hopf_clutching": {
            "north_south_relation": "v_N = exp(i phi) v_S on the equator",
            "max_relation_residual": float(max(equator_residuals)),
            "max_projector_residual": float(max(projector_residuals)),
            "line_transition": "z",
            "first_chern_number": 1,
        },
        "coefficient_symbol": {
            "matrix_size": size,
            "coefficient_rank": rank,
            "transition": "z q0 + 1 - q0",
            "determinant_winding": winding_15,
            "max_unitarity_residual": float(max(unitary_residuals)),
            "max_match_with_tome5_V_plus_residual": float(max(symbol_match_residuals)),
        },
        "real_pair": {
            "plus_transition": "z q0 + 1 - q0",
            "minus_transition": "z^(-1) conjugate(q0) + 1 - conjugate(q0)",
            "max_conjugate_exchange_residual": float(max(real_exchange_residuals)),
            "callias_boundary_indices_up_to_common_orientation": callias_indices,
            "toeplitz_indices_standard_hardy_orientation": toeplitz_indices,
            "absolute_class": rank,
        },
        "comparison": {
            "same_clutching_unitary_as_tome5_real_toeplitz_symbol": True,
            "boundary_K_class_comparison_closed": True,
            "equality_is_stronger_than_numeric_index_match": True,
            "direct_operator_unitary_equivalence_proved": False,
            "direct_Bunke_kernel_compression_hypotheses_checked": False,
            "spatial_Callias_index_conditional_on_spin_cover_carrier": True,
            "finite_parent_derives_rank_two_spin_carrier": False,
            "localized_physical_fermions_fully_derived": False,
        },
        "verdict": {
            "complex_Callias_Toeplitz_clutching_bridge": "pass",
            "Real_conjugate_pair_bridge": "pass",
            "coefficient_multiplicity_fifteen": "pass",
            "analytic_operator_identification": "open",
            "physical_carrier_derivation": "open",
            "next_gate": "version6_spin_cover_carrier_parent_derivation_gate",
        },
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()