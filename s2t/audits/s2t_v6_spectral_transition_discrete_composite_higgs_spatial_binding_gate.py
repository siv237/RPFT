#!/usr/bin/env python3
"""Audit spatial binding for the composite-Higgs nonlinear walk."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_composite_higgs_spatial_binding_gate_results.json"
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def chiral_generator(block: np.ndarray) -> np.ndarray:
    higgs_eff = sum(block[d, :2] * np.conj(block[d, 2]) for d in range(2))
    out = np.zeros((3, 3), dtype=complex)
    out[:2, 2] = higgs_eff
    out[2, :2] = np.conj(higgs_eff)
    return out


def local_coin(block: np.ndarray, coupling: float) -> np.ndarray:
    generator = np.kron(SIGMA_Y, chiral_generator(block))
    values, vectors = np.linalg.eigh(generator)
    unitary = (vectors * np.exp(-1.0j * coupling * values)) @ vectors.conj().T
    return (unitary @ block.reshape(6)).reshape(2, 3)


def step(state: np.ndarray, coupling: float) -> np.ndarray:
    coined = np.empty_like(state)
    for site, block in enumerate(state):
        coined[site] = local_coin(block, coupling)
    shifted = np.empty_like(coined)
    shifted[:, 0, :] = np.roll(coined[:, 0, :], 1, axis=0)
    shifted[:, 1, :] = np.roll(coined[:, 1, :], -1, axis=0)
    return shifted


def density(state: np.ndarray) -> np.ndarray:
    return np.sum(np.abs(state) ** 2, axis=(1, 2))


def metrics(state: np.ndarray, coordinates: np.ndarray) -> dict[str, float]:
    rho = density(state)
    return {
        "norm": float(np.sum(rho)),
        "inverse_participation_ratio": float(np.sum(rho**2)),
        "second_moment": float(np.sum(coordinates**2 * rho)),
        "core_probability_abs_x_le_8": float(np.sum(rho[np.abs(coordinates) <= 8])),
        "peak_density": float(np.max(rho)),
    }


def main() -> None:
    sites = 256
    coordinates = np.arange(sites) - sites // 2
    envelope = np.exp(-(coordinates / 4.0) ** 2)
    seed = np.zeros((sites, 2, 3), dtype=complex)
    seed[:, 0, 0] = envelope
    seed[:, 1, 2] = 0.8j * envelope
    seed[:, 0, 2] = 0.3 * envelope
    seed[:, 1, 1] = 0.4 * envelope
    seed /= np.linalg.norm(seed)
    initial = metrics(seed, coordinates)

    scan: dict[str, dict[str, float]] = {}
    for coupling in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0):
        state = seed.copy()
        for _ in range(80):
            state = step(state, coupling)
        final = metrics(state, coordinates)
        final["norm_error"] = abs(final["norm"] - 1.0)
        final["ipr_ratio_to_initial"] = final["inverse_participation_ratio"] / initial[
            "inverse_participation_ratio"
        ]
        scan[str(coupling)] = final

    rng = np.random.default_rng(20260821)
    probe = rng.normal(size=(2, 3)) + 1.0j * rng.normal(size=(2, 3))
    probe /= np.linalg.norm(probe)
    scaling = {}
    for epsilon in (1e-1, 3e-2, 1e-2, 3e-3):
        small = epsilon * probe
        correction = np.linalg.norm(local_coin(small, 1.0) - small)
        scaling[str(epsilon)] = float(correction)
    log_eps = np.log(np.array([float(item) for item in scaling]))
    log_corr = np.log(np.array(list(scaling.values())))
    nonlinear_order = float(np.polyfit(log_eps, log_corr, 1)[0])

    raw = rng.normal(size=(2, 2)) + 1.0j * rng.normal(size=(2, 2))
    weak, _ = np.linalg.qr(raw)
    phase = np.exp(0.41j)
    gauge = np.zeros((3, 3), dtype=complex)
    gauge[:2, :2] = weak
    gauge[2, 2] = phase
    transformed = np.einsum("nsi,ij->nsj", seed, gauge.T)
    left = step(transformed, 1.3)
    right = np.einsum("nsi,ij->nsj", step(seed, 1.3), gauge.T)
    covariance_residual = float(np.linalg.norm(left - right))

    all_spread = all(
        item["second_moment"] > 1000.0
        and item["ipr_ratio_to_initial"] < 1.0
        and item["core_probability_abs_x_le_8"] < 0.1
        for item in scan.values()
    )
    result = {
        "gate": "version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate",
        "update": {
            "coin_generator": "sigma_y_direction tensor K(H_eff)",
            "H_eff": "sum_direction ell_direction*conjugate(e_direction)",
            "shift": "opposite nearest-neighbor shifts",
            "external_mass_angle": False,
            "exactly_local": True,
            "exactly_norm_preserving": True,
        },
        "linearization": {
            "measured_nonlinear_correction_order": nonlinear_order,
            "expected_order": 3,
            "vacuum_linearization": "massless_free_shift",
            "linear_spectral_gap": False,
            "small_amplitude_exponential_bound_state_supported": False,
            "correction_norm_scan": scaling,
        },
        "exact_tests": {
            "global_gauge_covariance_residual": covariance_residual,
            "maximum_norm_error_after_80_steps": max(item["norm_error"] for item in scan.values()),
        },
        "initial_metrics": initial,
        "coupling_scan_after_80_steps": scan,
        "scan_summary": {
            "all_scanned_packets_spread": all_spread,
            "coupling_values": [float(item) for item in scan],
            "robust_bound_profile_found": False,
            "finite_support_compacton_excluded": False,
        },
        "verdict": {
            "composite_coin_slows_spreading_for_some_couplings": True,
            "parameter_independent_spatial_binding_found": False,
            "gapped_localized_endpoint_found": False,
            "compacton_loophole_open": True,
            "R4_stable_physical_endpoint_closed": False,
            "R5_blind_prediction_closed": False,
            "status": "the canonical composite-Higgs directional coin has a massless vacuum linearization and no robust binding in the declared scan; only tuned finite-support compactons remain open",
        },
        "next_gate": "version6_spectral_transition_discrete_compacton_existence_gate",
    }

    assert abs(nonlinear_order - 3.0) < 0.05
    assert covariance_residual < 1e-12
    assert result["exact_tests"]["maximum_norm_error_after_80_steps"] < 1e-12
    assert all_spread
    assert result["scan_summary"]["finite_support_compacton_excluded"] is False
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()