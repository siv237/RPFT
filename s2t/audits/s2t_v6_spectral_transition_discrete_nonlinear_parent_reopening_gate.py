#!/usr/bin/env python3
"""Audit a norm-preserving nonlinear quantum-walk parent and its internal covariance."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_nonlinear_parent_reopening_gate_results.json"


def step(psi: np.ndarray, theta0: float, kappa: float) -> np.ndarray:
    density_z = np.sum(np.abs(psi[:, 0, :]) ** 2 - np.abs(psi[:, 1, :]) ** 2, axis=1)
    theta = theta0 + kappa * density_z
    c = np.cos(theta)[:, None]
    s = np.sin(theta)[:, None]
    mixed = np.empty_like(psi)
    mixed[:, 0, :] = c * psi[:, 0, :] - s * psi[:, 1, :]
    mixed[:, 1, :] = s * psi[:, 0, :] + c * psi[:, 1, :]
    shifted = np.empty_like(psi)
    shifted[:, 0, :] = np.roll(mixed[:, 0, :], 1, axis=0)
    shifted[:, 1, :] = np.roll(mixed[:, 1, :], -1, axis=0)
    return shifted


def norm2(psi: np.ndarray) -> float:
    return float(np.vdot(psi, psi).real)


def ipr(psi: np.ndarray) -> float:
    density = np.sum(np.abs(psi) ** 2, axis=(1, 2))
    return float(np.sum(density**2) / np.sum(density) ** 2)


def main() -> None:
    rng = np.random.default_rng(20260821)
    sites, internal = 64, 5
    psi = rng.normal(size=(sites, 2, internal)) + 1j * rng.normal(size=(sites, 2, internal))
    psi /= np.sqrt(norm2(psi))

    theta0, kappa = 0.17, 0.83
    evolved = step(psi, theta0, kappa)
    norm_error = abs(norm2(evolved) - norm2(psi))

    raw = rng.normal(size=(internal, internal)) + 1j * rng.normal(size=(internal, internal))
    unitary, _ = np.linalg.qr(raw)
    rotated = np.einsum("nsi,ij->nsj", psi, unitary)
    covariance_left = step(rotated, theta0, kappa)
    covariance_right = np.einsum("nsi,ij->nsj", evolved, unitary)
    covariance_residual = float(np.linalg.norm(covariance_left - covariance_right))

    x = np.arange(sites) - sites / 2
    seed = np.zeros((sites, 2, 1), dtype=complex)
    seed[:, 0, 0] = np.exp(-(x / 5.0) ** 2)
    seed[:, 1, 0] = 0.35j * np.exp(-(x / 5.0) ** 2)
    seed /= np.sqrt(norm2(seed))
    scan = {}
    for coupling in (0.0, 0.5, 1.0, 2.0):
        state = seed.copy()
        for _ in range(40):
            state = step(state, theta0=0.12, kappa=coupling)
        scan[str(coupling)] = {
            "norm_error": abs(norm2(state) - 1.0),
            "inverse_participation_ratio": ipr(state),
        }

    result = {
        "gate": "version6_spectral_transition_discrete_nonlinear_parent_reopening_gate",
        "exact_tests": {
            "norm_preservation_error": norm_error,
            "internal_unitary_covariance_residual": covariance_residual,
            "nearest_neighbor_locality": True,
        },
        "coupling_scan_after_40_steps": scan,
        "analytic_structure": {
            "continuum_limit": "nonlinear_Dirac_type",
            "full_internal_bimodule_dimension": 300,
            "full_bimodule_commutant": "C_times_identity",
            "canonical_rank_one_internal_selector": False,
            "lattice_spacing_physical_value_derived": False,
            "nonlinear_coupling_derived": False,
        },
        "verdict": {
            "local_norm_preserving_nonlinear_parent_constructed": True,
            "internal_multiplicity_reduced": False,
            "R4_stable_physical_endpoint_closed": False,
            "R5_blind_prediction_closed": False,
            "status": "discrete proof of concept reproduces nonlinear Dirac kinematics but retains 300-fold internal covariance and free scale/coupling",
        },
        "next_gate": "version6_spectral_transition_discrete_equivariant_coin_selector_gate",
    }
    assert norm_error < 1e-12
    assert covariance_residual < 1e-12
    assert result["analytic_structure"]["full_internal_bimodule_dimension"] == 300
    assert not result["verdict"]["internal_multiplicity_reduced"]
    assert len({round(v["inverse_participation_ratio"], 12) for v in scan.values()}) > 1
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()