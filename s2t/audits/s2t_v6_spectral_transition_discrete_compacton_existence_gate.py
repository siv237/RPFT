#!/usr/bin/env python3
"""Certify exact one-site obstruction and a two-site compacton branch."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_existence_gate_results.json"
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


def compacton(branch: int, sites: int = 64) -> tuple[np.ndarray, float, complex]:
    center = sites // 2
    state = np.zeros((sites, 2, 3), dtype=complex)
    local_vector = np.array([0.5, 0.0, 0.5], dtype=complex)
    sign = (-1) ** branch
    eigenphase = 1.0j
    state[center, 1, :] = local_vector
    state[center + 1, 0, :] = eigenphase * sign * local_vector
    coupling = 2.0 * (2 * branch + 1) * np.pi
    return state, coupling, eigenphase


def main() -> None:
    branches = {}
    for branch in range(3):
        state, coupling, eigenphase = compacton(branch)
        evolved = step(state, coupling)
        density = np.sum(np.abs(evolved) ** 2, axis=(1, 2))
        center = len(state) // 2
        branches[str(branch)] = {
            "coupling": coupling,
            "coupling_over_pi": coupling / np.pi,
            "eigenphase_real": float(eigenphase.real),
            "eigenphase_imag": float(eigenphase.imag),
            "eigenstate_residual": float(np.linalg.norm(evolved - eigenphase * state)),
            "leakage_probability": float(1.0 - density[center] - density[center + 1]),
            "norm_error": abs(float(np.vdot(evolved, evolved).real) - 1.0),
        }

    one_site = np.zeros((64, 2, 3), dtype=complex)
    one_site[32, 0, :] = np.array([0.5, 0.0, 0.5], dtype=complex) * np.sqrt(2.0)
    evolved_one = step(one_site, 2.0 * np.pi)
    one_site_stationary_residual = min(
        float(np.linalg.norm(evolved_one - phase * one_site))
        for phase in (1.0, -1.0, 1.0j, -1.0j)
    )
    one_site_center_probability = float(np.sum(np.abs(evolved_one[32]) ** 2))

    exact_state, exact_coupling, _ = compacton(0)
    center = len(exact_state) // 2
    detuning = {}
    for relative in (0.001, 0.01, 0.05, 0.1):
        evolved = step(exact_state, exact_coupling * (1.0 + relative))
        density = np.sum(np.abs(evolved) ** 2, axis=(1, 2))
        leakage = float(1.0 - density[center] - density[center + 1])
        predicted = float(np.sin(0.5 * np.pi * relative) ** 2)
        detuning[str(relative)] = {
            "one_step_leakage_probability": leakage,
            "analytic_leakage_probability": predicted,
            "residual": abs(leakage - predicted),
        }

    state = exact_state.copy()
    for _ in range(100):
        state = step(state, exact_coupling)
    density = np.sum(np.abs(state) ** 2, axis=(1, 2))
    hundred_step_core = float(density[center] + density[center + 1])

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_existence_gate",
        "one_site_obstruction": {
            "nonzero_stationary_one_site_profile_exists": False,
            "reason": "the conditional shift sends the two directional outputs to distinct neighboring sites",
            "test_stationary_residual": one_site_stationary_residual,
            "center_probability_after_one_step": one_site_center_probability,
        },
        "symmetric_two_site_branch": {
            "local_vector": "(ell,e)=(1/2,1/2) with one weak component",
            "local_norm_squared": 0.5,
            "balanced_chiral_populations": True,
            "full_flip_condition": "kappa*local_norm_squared=(2m+1)*pi",
            "allowed_couplings": "kappa=2*(2m+1)*pi",
            "minimal_positive_coupling": 2.0 * np.pi,
            "eigenphase": "plus_or_minus_i",
            "branches": branches,
        },
        "detuning": detuning,
        "long_run_exactness": {
            "steps": 100,
            "core_probability": hundred_step_core,
            "norm_error": abs(float(np.vdot(state, state).real) - 1.0),
        },
        "interpretation": {
            "exact_finite_support_compacton_exists": True,
            "dimensionless_existential_quantization_found": True,
            "minimal_branch_value": "2*pi",
            "physical_lattice_spacing_derived": False,
            "nonlinear_stability_proved": False,
            "observational_map_for_2pi": False,
        },
        "verdict": {
            "compacton_loophole_closed_by_existence": True,
            "R4_stable_physical_endpoint_closed": False,
            "R5_blind_prediction_closed": False,
            "status": "an exact two-site compacton exists at kappa=2(2m+1)pi; the minimal 2pi branch is a new discrete existence value, but stability, physical length and observational meaning remain open",
        },
        "next_gate": "version6_spectral_transition_discrete_compacton_stability_quantization_gate",
    }

    assert one_site_center_probability < 1e-12
    assert one_site_stationary_residual > 1.0
    assert max(item["eigenstate_residual"] for item in branches.values()) < 1e-12
    assert max(abs(item["leakage_probability"]) for item in branches.values()) < 1e-12
    assert max(item["residual"] for item in detuning.values()) < 1e-12
    assert abs(hundred_step_core - 1.0) < 1e-12
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()