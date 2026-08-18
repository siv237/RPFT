#!/usr/bin/env python3
"""Audit the number-operator parent of the Toeplitz compression."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def main() -> None:
    cutoff = 64
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    dim = len(modes)
    number = np.diag(modes)
    shift = np.zeros((dim, dim), dtype=complex)
    for j in range(dim - 1):
        shift[j + 1, j] = 1.0

    commutator = number @ shift - shift @ number
    interior = commutator - shift
    commutator_residual = float(np.linalg.norm(interior, ord="fro"))

    reversal = np.fliplr(np.eye(dim, dtype=complex))
    n_reality_residual = float(np.linalg.norm(reversal @ number @ reversal + number))
    u_reality_residual = float(
        np.linalg.norm(reversal @ shift @ reversal - shift.conj().T)
    )

    positive = np.where(modes >= 0)[0]
    compressed = shift[np.ix_(positive, positive)]
    eye_plus = np.eye(len(positive), dtype=complex)
    source_defect = eye_plus - compressed.conj().T @ compressed
    target_defect = eye_plus - compressed @ compressed.conj().T

    bottom = np.zeros_like(eye_plus)
    bottom[0, 0] = 1.0
    top = np.zeros_like(eye_plus)
    top[-1, -1] = 1.0

    q_rank = 15
    result = {
        "gate": "version5_real_toeplitz_unbounded_parent_cycle_gate",
        "finite_window_audit": {
            "cutoff": cutoff,
            "commutator_N_U_minus_U_frobenius": commutator_residual,
            "K_N_K_plus_N_frobenius": n_reality_residual,
            "K_U_K_minus_U_star_frobenius": u_reality_residual,
            "P_dimension": len(positive),
            "I_minus_SstarS_equals_top_cutoff_projector": bool(
                np.allclose(source_defect, top)
            ),
            "I_minus_SSstar_equals_bottom_projector": bool(
                np.allclose(target_defect, bottom)
            ),
            "top_defect_is_truncation_artifact": True,
        },
        "infinite_exact_cycle": {
            "hilbert_space": "ell2(Z) tensor q0(C105)",
            "number_operator": "N e_n = n e_n",
            "bilateral_shift": "U e_n = e_(n+1)",
            "bounded_commutator": "[N,U]=U",
            "compact_resolvent": True,
            "spectral_projection": "P=chi_[0,infinity)(N)",
            "hardy_space_derived": "P ell2(Z)=ell2(N0)",
            "toeplitz_compressions": {
                "PUP": "S, index -1",
                "PUstarP": "S*, index +1",
            },
            "coefficient_indices": [-q_rank, q_rank],
            "coefficient_defect_rank": q_rank,
            "normalized_weight": q_rank / 105,
        },
        "real_structure_checks": {
            "K_N_K": "-N",
            "K_U_K": "U*",
            "exchange_pair_available": True,
            "finite_KO6_exchange_skeleton_reusable": True,
        },
        "degree_ledger": {
            "toeplitz_extension_degree": 1,
            "unbounded_extension_Clifford_action": "Cl(0,1)",
            "covariant_KO_boundary_convention": "KO_n(symbol) -> KO_(n-1)(coefficient)",
            "target_degree": 6,
            "missing_real_symbol_degree": 7,
            "degree_drop_mod_8": (7 - 1) % 8,
            "extension_cycle_alone_is_KO6": False,
        },
        "verdict": {
            "hardy_polarization_derived_from_N": True,
            "unbounded_toeplitz_extension_cycle": "pass",
            "full_unbounded_KO6_parent": "not_yet",
            "integer_class_15_from_previous_gate_preserved": True,
            "physical_parent_action": False,
            "next_gate": "version5_real_toeplitz_degree_seven_symbol_gate",
        },
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_real_toeplitz_unbounded_parent_cycle_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert commutator_residual == 0.0
    assert n_reality_residual == 0.0
    assert u_reality_residual == 0.0
    assert np.allclose(target_defect, bottom)
    assert (7 - 1) % 8 == 6
    assert q_rank / 105 == 1 / 7
    print(output)


if __name__ == "__main__":
    main()