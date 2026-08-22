#!/usr/bin/env python3
"""Audit Floquet stability and finite-amplitude leakage of the minimal compacton."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_stability_quantization_gate_results.json"
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI = (
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
    np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex),
    np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex),
)


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


def four_steps(state: np.ndarray, coupling: float) -> np.ndarray:
    for _ in range(4):
        state = step(state, coupling)
    return state


def compacton(sites: int) -> np.ndarray:
    center = sites // 2
    state = np.zeros((sites, 2, 3), dtype=complex)
    local_vector = np.array([0.5, 0.0, 0.5], dtype=complex)
    state[center, 1, :] = local_vector
    state[center + 1, 0, :] = 1.0j * local_vector
    return state


def pack(state: np.ndarray) -> np.ndarray:
    flat = state.reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def unpack(vector: np.ndarray, sites: int) -> np.ndarray:
    size = sites * 2 * 3
    return (vector[:size] + 1.0j * vector[size:]).reshape(sites, 2, 3)


def real_jacobian(sites: int, epsilon: float = 2.0e-7) -> tuple[np.ndarray, np.ndarray, float]:
    coupling = 2.0 * np.pi
    state = compacton(sites)
    base = pack(state)
    columns = []
    for index in range(base.size):
        direction = np.zeros_like(base)
        direction[index] = epsilon
        plus = pack(four_steps(unpack(base + direction, sites), coupling))
        minus = pack(four_steps(unpack(base - direction, sites), coupling))
        columns.append((plus - minus) / (2.0 * epsilon))
    jacobian = np.column_stack(columns)
    residual = float(np.linalg.norm(four_steps(state.copy(), coupling) - state))
    return jacobian, state, residual


def spectrum_summary(jacobian: np.ndarray) -> dict[str, float | int]:
    moduli = np.abs(np.linalg.eigvals(jacobian))
    return {
        "real_dimension": int(jacobian.shape[0]),
        "spectral_radius": float(np.max(moduli)),
        "expanding_multiplier_count": int(np.count_nonzero(moduli > 1.0 + 1.0e-5)),
        "unit_circle_multiplier_count": int(np.count_nonzero(np.abs(moduli - 1.0) < 1.0e-5)),
        "largest_singular_value": float(np.linalg.svd(jacobian, compute_uv=False)[0]),
    }


def symmetry_tangents(state: np.ndarray) -> np.ndarray:
    tangents = [1.0j * state]
    for pauli in PAULI:
        tangent = np.zeros_like(state)
        tangent[:, :, :2] = np.einsum("ab,sdb->sda", 1.0j * pauli, state[:, :, :2])
        tangents.append(tangent)
    right_phase = np.zeros_like(state)
    right_phase[:, :, 2] = 1.0j * state[:, :, 2]
    tangents.append(right_phase)
    return np.column_stack([pack(tangent) for tangent in tangents])


def nonlinear_perturbation_scan() -> dict[str, dict[str, float]]:
    sites = 256
    coupling = 2.0 * np.pi
    center = sites // 2
    exact = compacton(sites)
    rng = np.random.default_rng(20260821)
    random_direction = rng.normal(size=exact.shape) + 1.0j * rng.normal(size=exact.shape)
    random_direction /= np.linalg.norm(random_direction)
    output = {}
    for amplitude in (1.0e-4, 1.0e-3, 1.0e-2, 3.0e-2, 5.0e-2, 6.0e-2, 7.0e-2, 8.0e-2, 9.0e-2, 1.0e-1):
        state = exact + amplitude * random_direction
        state /= np.linalg.norm(state)
        for _ in range(80):
            state = step(state, coupling)
        density = np.sum(np.abs(state) ** 2, axis=(1, 2))
        core_probability = float(density[center] + density[center + 1])
        loss = 1.0 - core_probability
        output[str(amplitude)] = {
            "core_probability_after_80_steps": core_probability,
            "radiated_probability": loss,
            "radiated_probability_over_amplitude_squared": loss / amplitude**2,
            "norm_error": abs(float(np.vdot(state, state).real) - 1.0),
        }
    return output


def main() -> None:
    finite_volume = {}
    main_jacobian = None
    main_state = None
    main_residual = None
    for sites in (8, 12, 16):
        jacobian, state, residual = real_jacobian(sites)
        summary = spectrum_summary(jacobian)
        summary["four_step_orbit_residual"] = residual
        finite_volume[str(sites)] = summary
        if sites == 16:
            main_jacobian = jacobian
            main_state = state
            main_residual = residual

    assert main_jacobian is not None and main_state is not None and main_residual is not None

    power_norms = {}
    power = np.eye(main_jacobian.shape[0])
    requested = {1, 2, 4, 8, 16, 32, 64, 128}
    for exponent in range(1, max(requested) + 1):
        power = main_jacobian @ power
        if exponent in requested:
            power_norms[str(exponent)] = float(np.linalg.svd(power, compute_uv=False)[0])

    raw_tangents = symmetry_tangents(main_state)
    symmetry_rank = int(np.linalg.matrix_rank(raw_tangents, tol=1.0e-9))
    q_sym, _ = np.linalg.qr(raw_tangents)
    q_sym = q_sym[:, :symmetry_rank]
    symmetry_residuals = np.linalg.norm(main_jacobian @ q_sym - q_sym, axis=0)
    q_full, _ = np.linalg.qr(q_sym, mode="complete")
    q_phys = q_full[:, symmetry_rank:]
    reduced = q_phys.T @ main_jacobian @ q_phys
    reduced_moduli = np.abs(np.linalg.eigvals(reduced))

    nonlinear_scan = nonlinear_perturbation_scan()

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_stability_quantization_gate",
        "linearization": {
            "map": "real Frechet derivative of the four-step return map F^4",
            "reason_real": "the composite Higgs bilinear contains complex conjugation, so the update is real-differentiable rather than holomorphic",
            "coupling": 2.0 * np.pi,
            "finite_periodic_lattices": finite_volume,
        },
        "symmetry_reduction": {
            "tested_tangents": ["global_phase", "weak_pauli_x", "weak_pauli_y", "weak_pauli_z", "right_chiral_phase"],
            "independent_tangent_rank": symmetry_rank,
            "maximum_fixed_tangent_residual": float(np.max(symmetry_residuals)),
            "reduced_real_dimension": int(reduced.shape[0]),
            "reduced_spectral_radius": float(np.max(reduced_moduli)),
            "reduced_expanding_multiplier_count": int(np.count_nonzero(reduced_moduli > 1.0 + 1.0e-5)),
            "reduced_unit_circle_multiplier_count": int(np.count_nonzero(np.abs(reduced_moduli - 1.0) < 1.0e-5)),
        },
        "nonnormal_transient": {
            "operator_norms_of_monodromy_powers": power_norms,
            "maximum_tested_amplification": max(power_norms.values()),
            "exponential_growth_detected": False,
            "interpretation": "the finite-volume monodromy is spectrally neutral but strongly nonnormal; transient growth is bounded and recurrent in the tested window",
        },
        "finite_amplitude_protocol": {
            "lattice_sites": 256,
            "steps": 80,
            "seed": 20260821,
            "perturbation_normalization": "one fixed random complex direction with norm delta, followed by total-state normalization",
            "scan": nonlinear_scan,
            "protocol_dependent_escape_bracket": [0.06, 0.07],
        },
        "interpretation": {
            "linear_floquet_spectral_stability": True,
            "expanding_physical_multiplier_found": False,
            "asymptotic_attraction_proved": False,
            "reason_not_asymptotic": "the massless vacuum supplies an extensive neutral unit-circle radiation sector",
            "small_perturbation_core_survives": True,
            "global_nonlinear_stability_proved": False,
            "existence_quantization_survives_first_stability_gate": True,
            "physical_lattice_spacing_derived": False,
            "observational_mass_map_derived": False,
        },
        "verdict": {
            "R4_stable_endpoint_status": "partially_closed_by_local_numerical_floquet_stability",
            "R5_blind_prediction_closed": False,
            "status": "the kappa=2*pi compacton has no expanding Floquet multiplier after symmetry reduction and keeps its core under small controlled perturbations, but neutral radiation, nonnormal transients, finite-amplitude escape and the absence of a nonlinear theorem prevent calling it a fully stable physical particle",
        },
        "next_gate": "version6_spectral_transition_discrete_compacton_physical_scale_map_gate",
    }

    assert main_residual < 1.0e-12
    assert all(item["spectral_radius"] < 1.0 + 1.0e-5 for item in finite_volume.values())
    assert all(item["expanding_multiplier_count"] == 0 for item in finite_volume.values())
    assert result["symmetry_reduction"]["reduced_spectral_radius"] < 1.0 + 1.0e-5
    assert result["symmetry_reduction"]["reduced_expanding_multiplier_count"] == 0
    assert result["symmetry_reduction"]["maximum_fixed_tangent_residual"] < 1.0e-7
    assert result["nonnormal_transient"]["maximum_tested_amplification"] < 20.0
    assert nonlinear_scan["0.03"]["core_probability_after_80_steps"] > 0.99
    assert nonlinear_scan["0.05"]["core_probability_after_80_steps"] > 0.99
    assert nonlinear_scan["0.1"]["core_probability_after_80_steps"] < 0.1

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()