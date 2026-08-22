#!/usr/bin/env python3
"""Audit external-Higgs and composite-Higgs chiral coins on L_L plus e_R."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_chiral_coin_closure_gate_results.json"


def generator(state: np.ndarray) -> np.ndarray:
    ell = state[:2]
    electron = state[2]
    higgs_eff = ell * np.conj(electron)
    out = np.zeros((3, 3), dtype=complex)
    out[:2, 2] = higgs_eff
    out[2, :2] = np.conj(higgs_eff)
    return out


def unitary_from_hermitian(matrix: np.ndarray, coupling: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * np.exp(-1.0j * coupling * values)) @ vectors.conj().T


def step(state: np.ndarray, coupling: float) -> np.ndarray:
    return unitary_from_hermitian(generator(state), coupling) @ state


def population(state: np.ndarray) -> float:
    return float(np.vdot(state[:2], state[:2]).real)


def main() -> None:
    rng = np.random.default_rng(20260821)
    state = rng.normal(size=3) + 1.0j * rng.normal(size=3)
    state /= np.linalg.norm(state)
    coupling = 0.83

    evolved = step(state, coupling)
    norm_error = abs(float(np.vdot(evolved, evolved).real) - 1.0)
    hermiticity_error = float(np.linalg.norm(generator(state) - generator(state).conj().T))

    raw = rng.normal(size=(2, 2)) + 1.0j * rng.normal(size=(2, 2))
    weak_unitary, _ = np.linalg.qr(raw)
    phase = np.exp(0.37j)
    gauge = np.zeros((3, 3), dtype=complex)
    gauge[:2, :2] = weak_unitary
    gauge[2, 2] = phase
    transformed = gauge @ state
    covariance_generator = float(
        np.linalg.norm(generator(transformed) - gauge @ generator(state) @ gauge.conj().T)
    )
    covariance_step = float(np.linalg.norm(step(transformed, coupling) - gauge @ evolved))

    p = population(state)
    q = 1.0 - p
    phi = coupling * np.sqrt(p * q)
    predicted = p * np.cos(phi) ** 2 + q * np.sin(phi) ** 2
    population_map_residual = abs(population(evolved) - predicted)

    scans = {}
    seed = np.array([np.sqrt(0.91), 0.0, np.sqrt(0.09)], dtype=complex)
    for value in (0.25, 0.75, 1.5):
        current = seed.copy()
        series = [population(current)]
        for _ in range(80):
            current = step(current, value)
            series.append(population(current))
        scans[str(value)] = {
            "initial_left_population": series[0],
            "final_left_population": series[-1],
            "minimum_distance_to_balanced_population": min(abs(item - 0.5) for item in series),
            "norm_error": abs(float(np.vdot(current, current).real) - 1.0),
        }

    pure_left = np.array([1.0, 0.0, 0.0], dtype=complex)
    pure_right = np.array([0.0, 0.0, 1.0], dtype=complex)
    boundary_left_residual = float(np.linalg.norm(step(pure_left, coupling) - pure_left))
    boundary_right_residual = float(np.linalg.norm(step(pure_right, coupling) - pure_right))

    result = {
        "gate": "version6_spectral_transition_discrete_chiral_coin_closure_gate",
        "external_higgs_branch": {
            "equivariant_intertwiner_complex_dimension": 1,
            "free_complex_amplitude": True,
            "normalized_direction_defined_at_H_zero": False,
            "new_relative_to_H15_yukawa_edge": False,
        },
        "composite_higgs_branch": {
            "definition": "H_eff=ell*conjugate(e_R)",
            "lowest_bilinear_is_gauge_covariant": True,
            "local_generator_is_hermitian": True,
            "exact_norm_preserving_update": True,
            "nonlinear_coupling_derived": False,
            "physical_length_scale_derived": False,
        },
        "exact_tests": {
            "hermiticity_error": hermiticity_error,
            "norm_preservation_error": norm_error,
            "generator_gauge_covariance_residual": covariance_generator,
            "step_gauge_covariance_residual": covariance_step,
            "analytic_population_map_residual": population_map_residual,
            "pure_left_fixed_stratum_residual": boundary_left_residual,
            "pure_right_fixed_stratum_residual": boundary_right_residual,
        },
        "population_scan": scans,
        "analytic_population_map": {
            "p_prime": "p*cos(kappa*sqrt(p*(1-p)))^2+(1-p)*sin(kappa*sqrt(p*(1-p)))^2",
            "balanced_population_fixed": True,
            "pure_left_fixed": True,
            "pure_right_fixed": True,
            "unique_endpoint": False,
        },
        "verdict": {
            "external_higgs_coin_closes_without_free_yukawa": False,
            "endogenous_composite_higgs_coin_constructed": True,
            "unique_chiral_endpoint_selected": False,
            "spatial_localization_closed": False,
            "R4_stable_physical_endpoint_closed": False,
            "R5_blind_prediction_closed": False,
            "status": "the lowest composite Higgs bilinear gives an exact gauge-covariant nonlinear coin, but it has multiple invariant strata and leaves coupling and length scale free",
        },
        "next_gate": "version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate",
    }

    assert hermiticity_error < 1e-12
    assert norm_error < 1e-12
    assert covariance_generator < 1e-12
    assert covariance_step < 1e-12
    assert population_map_residual < 1e-12
    assert boundary_left_residual < 1e-12
    assert boundary_right_residual < 1e-12
    assert not result["verdict"]["unique_chiral_endpoint_selected"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()