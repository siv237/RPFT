#!/usr/bin/env python3
"""Test whether generic localized states are dynamically captured by the compacton."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_dynamical_capture_gate_results.json"
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


def balanced_vector(rng: np.random.Generator) -> np.ndarray:
    weak = rng.normal(size=2) + 1.0j * rng.normal(size=2)
    weak *= 0.5 / np.linalg.norm(weak)
    right = 0.5 * np.exp(1.0j * rng.uniform(0.0, 2.0 * np.pi))
    return np.array([weak[0], weak[1], right], dtype=complex)


def two_site_state(left: np.ndarray, right: np.ndarray, sites: int) -> np.ndarray:
    center = sites // 2
    state = np.zeros((sites, 2, 3), dtype=complex)
    state[center, 1, :] = left
    state[center + 1, 0, :] = right
    return state


def optimized_phase_residual(reference: np.ndarray, candidate: np.ndarray) -> float:
    overlap = np.vdot(reference, candidate)
    if abs(overlap) < 1.0e-15:
        return float(np.sqrt(np.vdot(reference, reference).real + np.vdot(candidate, candidate).real))
    phase = overlap / abs(overlap)
    return float(np.linalg.norm(candidate - phase * reference))


def manifold_diagnostic(state: np.ndarray) -> dict[str, float | int | str]:
    directional_norm = np.sum(np.abs(state) ** 2, axis=2)
    weak_norm = np.sum(np.abs(state[:, :, :2]) ** 2, axis=2)

    candidates = []
    for name, left_direction, right_direction in (
        ("inward", 1, 0),
        ("outward", 0, 1),
    ):
        n_left = directional_norm[:, left_direction]
        n_right = np.roll(directional_norm[:, right_direction], -1)
        w_left = weak_norm[:, left_direction]
        w_right = np.roll(weak_norm[:, right_direction], -1)
        selected_probability = n_left + n_right
        defect = np.sqrt(
            (1.0 - selected_probability) ** 2
            + (n_left - 0.5) ** 2
            + (n_right - 0.5) ** 2
            + (w_left - 0.5 * n_left) ** 2
            + (w_right - 0.5 * n_right) ** 2
        )
        index = int(np.argmin(defect))
        candidates.append(
            (
                float(defect[index]),
                float(selected_probability[index]),
                index,
                name,
            )
        )
    defect, probability, site, orientation = min(candidates, key=lambda item: item[0])
    return {
        "manifold_defect": defect,
        "selected_two_direction_probability": probability,
        "left_site": site,
        "orientation": orientation,
    }


def time_samples(state: np.ndarray, coupling: float, final_time: int = 80) -> dict[str, dict[str, float | int | str]]:
    output = {}
    for time in range(final_time + 1):
        if time % 4 == 0:
            output[str(time)] = manifold_diagnostic(state)
        if time < final_time:
            state = step(state, coupling)
    return output


def random_initial_state(kind: str, rng: np.random.Generator, sites: int) -> np.ndarray:
    center = sites // 2
    state = np.zeros((sites, 2, 3), dtype=complex)
    if kind == "one_site_random":
        state[center] = rng.normal(size=(2, 3)) + 1.0j * rng.normal(size=(2, 3))
    elif kind == "two_site_random":
        state[center : center + 2] = rng.normal(size=(2, 2, 3)) + 1.0j * rng.normal(size=(2, 2, 3))
    elif kind == "gaussian_random_internal":
        internal = rng.normal(size=(2, 3)) + 1.0j * rng.normal(size=(2, 3))
        for offset in range(-6, 7):
            state[center + offset] = np.exp(-(offset**2) / 8.0) * internal
    else:
        raise ValueError(kind)
    state /= np.linalg.norm(state)
    return state


def main() -> None:
    coupling = 2.0 * np.pi
    rng = np.random.default_rng(20260821)

    manifold_residuals = []
    manifold_defects = []
    for _ in range(32):
        state = two_site_state(balanced_vector(rng), balanced_vector(rng), 64)
        evolved_twice = step(step(state, coupling), coupling)
        manifold_residuals.append(float(np.linalg.norm(evolved_twice + state)))
        manifold_defects.append(float(manifold_diagnostic(state)["manifold_defect"]))

    phase_scan = {}
    base = np.array([0.5, 0.0, 0.5], dtype=complex)
    one_step_eigenphase_count = 0
    for phase in np.linspace(0.0, 2.0 * np.pi, 17)[:-1]:
        state = two_site_state(base, np.exp(1.0j * phase) * base, 64)
        once = step(state, coupling)
        twice = step(once, coupling)
        one_residual = optimized_phase_residual(state, once)
        two_residual = float(np.linalg.norm(twice + state))
        if one_residual < 1.0e-10:
            one_step_eigenphase_count += 1
        phase_scan[str(phase / np.pi)] = {
            "relative_phase_over_pi": float(phase / np.pi),
            "one_step_eigenstate_residual": one_residual,
            "two_step_minus_identity_residual": two_residual,
            "core_probability_after_two_steps": float(
                manifold_diagnostic(twice)["selected_two_direction_probability"]
            ),
        }

    amplitude_scan = {}
    for population in (0.1, 0.2, 0.3, 0.4, 0.45, 0.48, 0.49, 0.5, 0.51, 0.52, 0.55, 0.6, 0.7, 0.8, 0.9):
        left = base * np.sqrt(population / 0.5)
        right = 1.0j * base * np.sqrt((1.0 - population) / 0.5)
        history = time_samples(two_site_state(left, right, 256), coupling)
        amplitude_scan[str(population)] = {
            "left_population": population,
            "initial_defect": history["0"]["manifold_defect"],
            "final_defect": history["80"]["manifold_defect"],
            "final_selected_probability": history["80"]["selected_two_direction_probability"],
            "minimum_post_burnin_defect": min(
                item["manifold_defect"] for time, item in history.items() if int(time) >= 20
            ),
        }

    chiral_scan = {}
    for weak_fraction in (0.1, 0.2, 0.3, 0.4, 0.45, 0.48, 0.49, 0.5, 0.51, 0.52, 0.55, 0.6, 0.7, 0.8, 0.9):
        vector = np.array(
            [np.sqrt(0.5 * weak_fraction), 0.0, np.sqrt(0.5 * (1.0 - weak_fraction))],
            dtype=complex,
        )
        history = time_samples(two_site_state(vector, 1.0j * vector, 256), coupling)
        chiral_scan[str(weak_fraction)] = {
            "weak_fraction": weak_fraction,
            "initial_defect": history["0"]["manifold_defect"],
            "final_defect": history["80"]["manifold_defect"],
            "final_selected_probability": history["80"]["selected_two_direction_probability"],
            "minimum_post_burnin_defect": min(
                item["manifold_defect"] for time, item in history.items() if int(time) >= 20
            ),
        }

    ensembles = {}
    for kind in ("one_site_random", "two_site_random", "gaussian_random_internal"):
        trials = []
        captures = 0
        for trial in range(12):
            history = time_samples(random_initial_state(kind, rng, 192), coupling)
            late = [item for time, item in history.items() if int(time) >= 60]
            captured = all(
                item["manifold_defect"] < 1.0e-3
                and item["selected_two_direction_probability"] > 0.99
                for item in late
            )
            captures += int(captured)
            trials.append(
                {
                    "trial": trial,
                    "captured": captured,
                    "minimum_post_burnin_defect": min(
                        item["manifold_defect"] for time, item in history.items() if int(time) >= 20
                    ),
                    "maximum_post_burnin_selected_probability": max(
                        item["selected_two_direction_probability"]
                        for time, item in history.items()
                        if int(time) >= 20
                    ),
                    "final_defect": history["80"]["manifold_defect"],
                    "final_selected_probability": history["80"]["selected_two_direction_probability"],
                }
            )
        ensembles[kind] = {
            "trial_count": len(trials),
            "capture_count": captures,
            "smallest_post_burnin_defect": min(item["minimum_post_burnin_defect"] for item in trials),
            "largest_final_selected_probability": max(item["final_selected_probability"] for item in trials),
            "trials": trials,
        }

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_dynamical_capture_gate",
        "exact_invariant_manifold": {
            "definition": "two adjacent inward directional blocks, each with norm squared 1/2 and equal weak/right chiral populations",
            "independent_left_and_right_balanced_vectors_allowed": True,
            "random_family_sample_count": len(manifold_residuals),
            "maximum_F2_plus_identity_residual": max(manifold_residuals),
            "maximum_manifold_defect": max(manifold_defects),
            "return_law": "F^2(Psi)=-Psi",
            "isolated_orbit": False,
        },
        "relative_phase_scan": {
            "phase_count": len(phase_scan),
            "one_step_eigenstate_phase_count": one_step_eigenphase_count,
            "one_step_eigenstate_relative_phases": ["pi/2", "3*pi/2"],
            "all_relative_phases_are_two_step_compactons": True,
            "maximum_two_step_residual": max(item["two_step_minus_identity_residual"] for item in phase_scan.values()),
            "scan": phase_scan,
        },
        "amplitude_balance_scan": amplitude_scan,
        "chiral_balance_scan": chiral_scan,
        "generic_capture_protocol": {
            "coupling": coupling,
            "lattice_sites": 192,
            "steps": 80,
            "sample_every_steps": 4,
            "capture_condition": "manifold defect <1e-3 and selected probability >0.99 at every sample from t=60 through t=80",
            "seed": 20260821,
            "ensembles": ensembles,
            "total_trials": sum(item["trial_count"] for item in ensembles.values()),
            "total_captures": sum(item["capture_count"] for item in ensembles.values()),
        },
        "interpretation": {
            "exact_compacton_family_exists": True,
            "one_step_phase_plus_or_minus_i_unique_within_fixed_vector_pair": True,
            "localized_endpoint_unique": False,
            "amplitude_balance_dynamically_restored": False,
            "chiral_balance_dynamically_restored": False,
            "generic_localized_state_capture_observed": False,
            "open_capture_basin_certified": False,
            "previous_local_stability_reinterpreted_as_stability_of_a_nonisolated_lattice_manifold": True,
        },
        "verdict": {
            "R2_endogenous_trigger": False,
            "R3_rate": False,
            "R4_unique_stable_endpoint": False,
            "status": "the kappa=2*pi rule contains a continuous exact two-site invariant manifold with F^2=-1, while the plus/minus i eigenstates are only special phase points; amplitude and chiral balance are not dynamically selected, and none of 36 prospective generic localized trials is captured, so the unchanged compacton branch does not provide a matter-birth mechanism",
        },
        "next_gate": "version6_spectral_transition_discrete_compacton_branch_status_freeze_gate",
    }

    assert max(manifold_residuals) < 1.0e-12
    assert max(manifold_defects) < 1.0e-12
    assert one_step_eigenphase_count == 2
    assert result["relative_phase_scan"]["maximum_two_step_residual"] < 1.0e-12
    assert amplitude_scan["0.5"]["final_defect"] < 1.0e-12
    assert all(
        amplitude_scan[key]["minimum_post_burnin_defect"] > 1.0e-3
        for key in amplitude_scan
        if key != "0.5"
    )
    assert chiral_scan["0.5"]["final_defect"] < 1.0e-12
    assert all(
        chiral_scan[key]["minimum_post_burnin_defect"] > 1.0e-3
        for key in chiral_scan
        if key != "0.5"
    )
    assert result["generic_capture_protocol"]["total_captures"] == 0

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()