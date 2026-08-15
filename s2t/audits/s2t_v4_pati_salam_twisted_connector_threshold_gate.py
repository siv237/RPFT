#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

from s2t_v4_pati_salam_first_order_kernel import dirac_from_channels
from s2t_v4_pati_salam_ko6_phi_sigma_hessian_gate import (
    composite_yukawa,
    crossed_majorana,
    phi_hessian,
    signature,
)


OUTPUT = Path("s2t_v4_pati_salam_twisted_connector_threshold_gate_results.json")


def phi_matrices(sigma):
    matrices = []
    for coordinate in range(8):
        values = np.zeros(8)
        values[coordinate] = 1.0
        phi = np.array(
            [
                [values[0] + 1j * values[1], values[2] + 1j * values[3]],
                [values[4] + 1j * values[5], values[6] + 1j * values[7]],
            ]
        )
        matrices.append(composite_yukawa(phi, sigma))
    return matrices


def yukawa_gram(sigma):
    matrices = phi_matrices(sigma)
    gram = np.zeros((8, 8))
    for row, first in enumerate(matrices):
        for column, second in enumerate(matrices[: row + 1]):
            value = float(np.vdot(first, second).real)
            gram[row, column] = value
            gram[column, row] = value
    return gram


def rounded_multiplicities(values, digits=8):
    ledger = {}
    for value in values:
        key = f"{float(value):.{digits}f}"
        ledger[key] = ledger.get(key, 0) + 1
    return ledger


def main():
    vacuum_value = 2.0 ** (-0.25)
    delta = np.zeros((2, 4), dtype=complex)
    delta[0, 0] = vacuum_value
    majorana = crossed_majorana(delta)
    background = dirac_from_channels(None, majorana, None)
    sigma_bl = np.diag([0.75, -0.25, -0.25, -0.25])

    phi_matrix = phi_hessian(background, sigma_bl)
    gram = yukawa_gram(sigma_bl)
    critical_modes = eigh(-phi_matrix, 2.0 * gram, eigvals_only=True)
    critical_zeta = float(np.max(critical_modes))

    scans = {}
    for zeta in (0.0, 1.9, 2.0, 2.1):
        scans[str(zeta)] = signature(phi_matrix + 2.0 * zeta * gram)

    output = {
        "gate": "version4_pati_salam_twisted_connector_threshold",
        "rank_one_background": {
            "Delta_entry": vacuum_value,
            "Majorana_nonzero_singular_square": 0.5,
            "Sigma_B_minus_L_direction": [0.75, -0.25, -0.25, -0.25],
            "project_Yukawa_seed": {"nu": 0.7, "e": 0.2, "u": 1.1, "d": 0.4},
        },
        "connected_scalar_channel": {
            "added_potential": "zeta ||Y(phi,Sigma)||_F^2",
            "Hessian_shift": "2 zeta G_Y",
            "Gram_eigenvalue_multiplicities": rounded_multiplicities(np.linalg.eigvalsh(gram)),
            "generalized_critical_mode_multiplicities": rounded_multiplicities(critical_modes),
            "critical_zeta": critical_zeta,
            "strict_phi_stability_condition": "zeta > 2",
            "scan": scans,
        },
        "Sigma_obstruction": {
            "Hermitian_traceless_real_dimension": 15,
            "scalar_channel_rank_at_phi_zero": 0,
            "remaining_flat_directions": 15,
            "reason": "Y(0,Sigma)=0 for every Sigma, so every potential depending only on ||Y||^2 has zero Sigma Hessian",
        },
        "route_ledger": {
            "direct_sum_singlet": "closed: exact portal zero",
            "universal_total_norm_portal": "closed: cannot split required and unwanted modes",
            "connected_scalar_Y_channel": "conditional phi pass for zeta>2, but Sigma remains flat",
            "twisted_scalar_vector_parent": "open architecture: can in principle supply both a scalar mass shift and an independent vector/Sigma potential without new fermions",
            "two_scale_spectral_action": "open architecture: must derive both stationary scales and relative coefficients",
        },
        "verdict": (
            "A scalar-only connector is insufficient. The exact normalized threshold for all eight phi modes is zeta>2, "
            "while all fifteen Sigma directions remain flat. The next minimal parent must generate two linked effects: "
            "a connected scalar channel above threshold and a direct representation-sensitive Sigma/vector potential."
        ),
        "next_gate": (
            "construct a reduced twisted spectral triple with an explicit exchange automorphism and compute whether its "
            "spectral action generates both required quadratic terms with fixed coefficients"
        ),
        "literature_targets": [
            "arXiv:1304.0415",
            "arXiv:1411.1320",
            "arXiv:1905.04533",
        ],
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()