#!/usr/bin/env python3
"""Audit the chiral H15 Hodge/moment-map instability."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


LEFT_DIM = 8
RIGHT_DIM = 7
TOTAL_DIM = LEFT_DIM + RIGHT_DIM


def action(y: np.ndarray) -> float:
    left = np.eye(LEFT_DIM) - y.conj().T @ y
    right = y @ y.conj().T - np.eye(RIGHT_DIM)
    return float(
        (np.trace(left.conj().T @ left) + np.trace(right.conj().T @ right)).real
        / TOTAL_DIM
    )


def physical_edge_coisometry() -> np.ndarray:
    """u,d,e select seven charged directions and leave nu_L in the kernel."""
    y = np.zeros((RIGHT_DIM, LEFT_DIM), dtype=complex)
    y[0:3, 0:3] = np.eye(3)  # Q_L up colours -> u_R
    y[3:6, 3:6] = np.eye(3)  # Q_L down colours -> d_R
    y[6, 7] = 1.0  # charged lepton -> e_R; index 6 is nu_L
    return y


def finite_difference_coordinate_hessian(eps: float = 1.0e-4) -> np.ndarray:
    basis = []
    for i in range(RIGHT_DIM):
        for j in range(LEFT_DIM):
            e = np.zeros((RIGHT_DIM, LEFT_DIM), dtype=complex)
            e[i, j] = 1.0
            basis.append(e)
            basis.append(1j * e)
    hessian = np.empty(len(basis))
    zero = np.zeros((RIGHT_DIM, LEFT_DIM), dtype=complex)
    s0 = action(zero)
    for k, e in enumerate(basis):
        hessian[k] = (action(eps * e) - 2.0 * s0 + action(-eps * e)) / eps**2
    return hessian


def main() -> None:
    rng = np.random.default_rng(20260825)
    singular_residuals = []
    for _ in range(32):
        y = rng.normal(size=(RIGHT_DIM, LEFT_DIM)) + 1j * rng.normal(
            size=(RIGHT_DIM, LEFT_DIM)
        )
        singular_values = np.linalg.svd(y, compute_uv=False)
        formula = (1.0 + 2.0 * np.sum((1.0 - singular_values**2) ** 2)) / TOTAL_DIM
        singular_residuals.append(abs(action(y) - formula))

    y_star = physical_edge_coisometry()
    source_projector = y_star.conj().T @ y_star
    target_identity = y_star @ y_star.conj().T
    singular_values = np.linalg.svd(y_star, compute_uv=False)
    hessian = finite_difference_coordinate_hessian()
    expected_hessian = -8.0 / TOTAL_DIM

    radial_samples = []
    for t in (0.0, 0.25, 0.5, 1.0, 1.5):
        numeric = action(t * y_star)
        analytic = (1.0 + 14.0 * (1.0 - t * t) ** 2) / TOTAL_DIM
        radial_samples.append(
            {"t": t, "numeric": numeric, "analytic": analytic, "residual": abs(numeric - analytic)}
        )

    result = {
        "gate": "version7_chiral_hodge_index_instability_gate",
        "chiral_packet": {
            "left_complex_dimension": LEFT_DIM,
            "right_complex_dimension": RIGHT_DIM,
            "total_complex_dimension": TOTAL_DIM,
            "dimension_difference": LEFT_DIM - RIGHT_DIM,
            "full_real_tangent_dimension": 2 * LEFT_DIM * RIGHT_DIM,
        },
        "action": {
            "zero_value": action(np.zeros((RIGHT_DIM, LEFT_DIM), dtype=complex)),
            "minimum_lower_bound": 1.0 / TOTAL_DIM,
            "maximum_singular_value_formula_residual": max(singular_residuals),
        },
        "zero_hessian": {
            "expected_eigenvalue": expected_hessian,
            "minimum_finite_difference_eigenvalue": float(np.min(hessian)),
            "maximum_finite_difference_eigenvalue": float(np.max(hessian)),
            "maximum_residual": float(np.max(np.abs(hessian - expected_hessian))),
            "negative_direction_count": int(np.sum(hessian < -1.0e-6)),
            "zero_direction_count": int(np.sum(np.abs(hessian) <= 1.0e-6)),
        },
        "physical_edge_minimum": {
            "rank": int(np.linalg.matrix_rank(y_star)),
            "kernel_complex_dimension": LEFT_DIM - int(np.linalg.matrix_rank(y_star)),
            "singular_values": singular_values.tolist(),
            "action": action(y_star),
            "source_projector_residual": float(np.linalg.norm(source_projector @ source_projector - source_projector)),
            "target_identity_residual": float(np.linalg.norm(target_identity - np.eye(RIGHT_DIM))),
            "neutrino_basis_vector_residual": float(np.linalg.norm(y_star[:, 6])),
        },
        "radial_path": radial_samples,
        "contract_update": {
            "stationary_zero": "pass",
            "negative_zero_hessian": "pass",
            "bounded_quartic_saturation": "pass",
            "rank_seven_minimum": "pass",
            "single_kernel_line": "pass",
            "full_affine_family_lift": "open",
            "physical_particle_identification": "not_claimed",
        },
        "verdict": {
            "chiral_core": "positive_candidate",
            "full_tome7_parent": "not_yet_closed",
            "next_gate": "canonical lift from E_aff tensor Y_phys to the H15 odd operator",
        },
    }

    assert result["zero_hessian"]["negative_direction_count"] == 112
    assert result["zero_hessian"]["zero_direction_count"] == 0
    assert result["physical_edge_minimum"]["rank"] == 7
    assert result["physical_edge_minimum"]["kernel_complex_dimension"] == 1
    assert abs(result["physical_edge_minimum"]["action"] - 1.0 / 15.0) < 1.0e-14
    assert result["action"]["maximum_singular_value_formula_residual"] < 1.0e-10

    output = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_chiral_hodge_index_instability_gate_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()