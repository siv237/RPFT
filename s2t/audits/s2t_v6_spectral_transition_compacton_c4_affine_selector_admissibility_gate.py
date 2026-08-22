#!/usr/bin/env python3
"""Audit whether the compacton C4 characters can canonically drive the affine sink."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_compacton_c4_affine_selector_admissibility_gate_results.json"


def affine_coisometry() -> np.ndarray:
    return np.array(
        [
            [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0), 0.0, 0.0],
            [1.0 / np.sqrt(6.0), 1.0 / np.sqrt(6.0), -2.0 / np.sqrt(6.0), 0.0],
            [
                1.0 / np.sqrt(12.0),
                1.0 / np.sqrt(12.0),
                1.0 / np.sqrt(12.0),
                -3.0 / np.sqrt(12.0),
            ],
        ],
        dtype=complex,
    )


def permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((len(permutation), len(permutation)), dtype=complex)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(permutation)))
    for _ in range(exponent):
        result = compose(permutation, result)
    return result


def cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    visited = set()
    lengths = []
    for start in range(len(permutation)):
        if start in visited:
            continue
        current = start
        length = 0
        while current not in visited:
            visited.add(current)
            current = permutation[current]
            length += 1
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def character_projector(operator: np.ndarray, eigenvalue: complex) -> np.ndarray:
    return sum(
        eigenvalue ** (-exponent) * np.linalg.matrix_power(operator, exponent)
        for exponent in range(4)
    ) / 4.0


def commutant_dimension(representatives: list[np.ndarray], dimension: int) -> tuple[int, np.ndarray]:
    constraints = []
    identity = np.eye(dimension)
    for representative in representatives:
        constraints.append(
            np.kron(identity, representative)
            - np.kron(representative.T, identity)
        )
    system = np.vstack(constraints)
    singular_values = np.linalg.svd(system, compute_uv=False)
    rank = int(np.sum(singular_values > 1.0e-10))
    return dimension * dimension - rank, singular_values


def phase_defect(state: np.ndarray, operator: np.ndarray) -> float:
    normalized = state / np.linalg.norm(state)
    return float(1.0 - abs(np.vdot(normalized, operator @ normalized)) ** 2)


def main() -> None:
    identity4 = np.eye(4, dtype=complex)
    uniform = np.ones(4, dtype=complex) / 2.0
    p1 = np.outer(uniform, uniform.conj())
    p3 = identity4 - p1
    coisometry = affine_coisometry()

    # The exact compacton manifold carries this reduced four-step action.
    orbit_step = np.array([[0.0, -1.0], [1.0, 0.0]], dtype=complex)
    orbit_step_internal = np.kron(orbit_step, np.eye(3))
    orbit_projectors = {
        "+i": character_projector(orbit_step, 1.0j),
        "-i": character_projector(orbit_step, -1.0j),
    }

    base_internal = np.array([1.0, 0.0, 1.0j], dtype=complex)
    base_internal /= np.linalg.norm(base_internal)
    phase_scan = []
    for phase in np.linspace(0.0, 2.0 * np.pi, 65)[:-1]:
        state = np.concatenate(
            [base_internal, np.exp(1.0j * phase) * base_internal]
        ) / np.sqrt(2.0)
        defect = phase_defect(state, orbit_step_internal)
        weights = {
            label: float(
                np.vdot(
                    state,
                    np.kron(projector, np.eye(3)) @ state,
                ).real
            )
            for label, projector in orbit_projectors.items()
        }
        phase_scan.append(
            {
                "phase_over_pi": float(phase / np.pi),
                "character_defect": defect,
                "weight_plus_i": weights["+i"],
                "weight_minus_i": weights["-i"],
                "four_weight_product": 4.0 * weights["+i"] * weights["-i"],
            }
        )

    rng = np.random.default_rng(20260821)
    random_identity_residuals = []
    for _ in range(64):
        state = rng.normal(size=6) + 1.0j * rng.normal(size=6)
        state /= np.linalg.norm(state)
        weights = [
            float(
                np.vdot(state, np.kron(projector, np.eye(3)) @ state).real
            )
            for projector in orbit_projectors.values()
        ]
        random_identity_residuals.append(
            abs(phase_defect(state, orbit_step_internal) - 4.0 * weights[0] * weights[1])
        )

    permutations = list(itertools.permutations(range(4)))
    permutation_matrices = [permutation_matrix(item) for item in permutations]
    four_cycles = [item for item in permutations if cycle_type(item) == (4,)]
    cyclic_subgroups = {
        frozenset(power(item, exponent) for exponent in range(4))
        for item in four_cycles
    }

    selected_cycle = (1, 2, 3, 0)
    selected_cycle_matrix = permutation_matrix(selected_cycle)
    affine_character_projectors = {
        label: character_projector(selected_cycle_matrix, eigenvalue)
        for label, eigenvalue in (
            ("1", 1.0),
            ("+i", 1.0j),
            ("-1", -1.0),
            ("-i", -1.0j),
        )
    }

    oriented_plus_i_projectors = []
    unoriented_pm_i_planes = []
    for item in four_cycles:
        matrix = permutation_matrix(item)
        plus = character_projector(matrix, 1.0j)
        minus = character_projector(matrix, -1.0j)
        if not any(np.linalg.norm(plus - old) < 1.0e-10 for old in oriented_plus_i_projectors):
            oriented_plus_i_projectors.append(plus)
        plane = plus + minus
        if not any(np.linalg.norm(plane - old) < 1.0e-10 for old in unoriented_pm_i_planes):
            unoriented_pm_i_planes.append(plane)

    full_commutant_dimension, full_commutant_singular_values = commutant_dimension(
        permutation_matrices, 4
    )
    transported_triplet_representatives = [
        coisometry @ matrix @ coisometry.conj().T for matrix in permutation_matrices
    ]
    triplet_commutant_dimension, triplet_commutant_singular_values = commutant_dimension(
        transported_triplet_representatives, 3
    )

    plus_i_affine = affine_character_projectors["+i"]
    minus_i_affine = affine_character_projectors["-i"]
    chosen_character_plane = plus_i_affine + minus_i_affine
    maximum_chosen_plane_commutator = max(
        float(np.linalg.norm(matrix @ chosen_character_plane - chosen_character_plane @ matrix))
        for matrix in permutation_matrices
    )

    # The canonical link is isotropic after the P3-to-triplet identification.
    induced_family_metric = coisometry @ p3 @ coisometry.conj().T
    maximum_isotropic_commutator = max(
        float(np.linalg.norm(induced_family_metric @ matrix - matrix @ induced_family_metric))
        for matrix in transported_triplet_representatives
    )

    # A finite coherent sink is recurrent rather than contractive.
    coherent_sink_hamiltonian = np.block(
        [
            [np.zeros((3, 3)), np.eye(3)],
            [np.eye(3), np.zeros((3, 3))],
        ]
    )
    initial_source = np.concatenate([np.array([1.0, 0.0, 0.0]), np.zeros(3)]).astype(complex)
    coherent_survival = []
    for time in (0.0, np.pi / 4.0, np.pi / 2.0, 3.0 * np.pi / 4.0, np.pi):
        values, vectors = np.linalg.eigh(coherent_sink_hamiltonian)
        evolution = (vectors * np.exp(-1.0j * time * values)) @ vectors.conj().T
        evolved = evolution @ initial_source
        coherent_survival.append(
            {
                "time_over_pi": float(time / np.pi),
                "source_probability": float(np.linalg.norm(evolved[:3]) ** 2),
                "sink_probability": float(np.linalg.norm(evolved[3:]) ** 2),
            }
        )

    maximum_projector_residual = max(
        float(np.linalg.norm(projector @ projector - projector))
        for projector in [*orbit_projectors.values(), *affine_character_projectors.values()]
    )
    maximum_character_orthogonality_residual = max(
        float(np.linalg.norm(left @ right))
        for left_label, left in affine_character_projectors.items()
        for right_label, right in affine_character_projectors.items()
        if left_label != right_label
    )

    result = {
        "gate": "version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate",
        "compacton_character_selector": {
            "reduced_orbit_step": orbit_step.real.tolist(),
            "F2_equals_minus_identity_residual": float(
                np.linalg.norm(orbit_step @ orbit_step + np.eye(2))
            ),
            "F4_equals_identity_residual": float(
                np.linalg.norm(np.linalg.matrix_power(orbit_step, 4) - np.eye(2))
            ),
            "character_projector_ranks": {
                label: int(np.linalg.matrix_rank(projector, tol=1.0e-10))
                for label, projector in orbit_projectors.items()
            },
            "selector": "D_chi(Psi)=1-|<Psi,F(Psi)>|^2=4 w_(+i) w_(-i) on the exact compacton manifold",
            "selector_is_coefficient_free": True,
            "selector_zero_locus": "F(Psi)=+i Psi or F(Psi)=-i Psi",
            "selector_also_enforces": [
                "equal two-site norm",
                "relative phase plus or minus pi/2",
                "collinearity of the two internal balanced vectors",
            ],
            "phase_scan_count": len(phase_scan),
            "zero_phase_points": [
                item["phase_over_pi"]
                for item in phase_scan
                if item["character_defect"] < 1.0e-12
            ],
            "maximum_defect_weight_identity_residual": max(random_identity_residuals),
            "phase_scan": phase_scan,
        },
        "affine_C4_character_decomposition": {
            "full_affine_group": "AGL(2,2)=S4",
            "four_cycle_count_in_S4": len(four_cycles),
            "distinct_C4_subgroup_count": len(cyclic_subgroups),
            "selected_cycle_is_parent_canonical": False,
            "selected_cycle_character_ranks": {
                label: int(np.linalg.matrix_rank(projector, tol=1.0e-10))
                for label, projector in affine_character_projectors.items()
            },
            "plus_i_and_minus_i_lie_in_P3": bool(
                np.linalg.norm(p3 @ plus_i_affine - plus_i_affine) < 1.0e-10
                and np.linalg.norm(p3 @ minus_i_affine - minus_i_affine) < 1.0e-10
            ),
            "distinct_oriented_plus_i_projectors": len(oriented_plus_i_projectors),
            "distinct_unoriented_plus_minus_i_planes": len(unoriented_pm_i_planes),
            "maximum_chosen_character_plane_S4_commutator": maximum_chosen_plane_commutator,
            "interpretation": "a chosen four-cycle supplies the desired plus/minus i channels inside P3, but choosing one of three C4 subgroups and one of two orientations is new symmetry-breaking data",
        },
        "equivariance_obstruction": {
            "full_C4_permutation_commutant_dimension": full_commutant_dimension,
            "full_C4_expected_commutant": "span{I,J}",
            "P3_triplet_commutant_dimension": triplet_commutant_dimension,
            "P3_triplet_expected_commutant": "complex scalars",
            "canonical_link": "X=rho V",
            "canonical_link_induced_metric_residual_from_identity": float(
                np.linalg.norm(induced_family_metric - np.eye(3))
            ),
            "maximum_isotropic_metric_S4_commutator": maximum_isotropic_commutator,
            "canonical_link_distinguishes_plus_minus_i": False,
            "C4_projectors_require_chosen_four_cycle": True,
            "full_commutant_smallest_nonzero_singular_value": float(
                min(value for value in full_commutant_singular_values if value > 1.0e-10)
            ),
            "triplet_commutant_smallest_nonzero_singular_value": float(
                min(value for value in triplet_commutant_singular_values if value > 1.0e-10)
            ),
        },
        "dynamical_obstruction": {
            "C4_equivariant_linear_unitary_preserves_character_weights": True,
            "therefore_D_chi_is_conserved": True,
            "finite_direct_sum_sink_is_contracting": False,
            "coherent_source_sink_survival": coherent_survival,
            "recurrence_residual_at_pi": abs(coherent_survival[-1]["source_probability"] - 1.0),
            "required_new_structure": "a derived open, measured, noisy, or nonlinear state-dependent evolution",
        },
        "maximum_residuals": {
            "character_projector_idempotence": maximum_projector_residual,
            "character_projector_orthogonality": maximum_character_orthogonality_residual,
            "coisometry_VVstar": float(np.linalg.norm(coisometry @ coisometry.conj().T - np.eye(3))),
            "coisometry_VstarV": float(np.linalg.norm(coisometry.conj().T @ coisometry - p3)),
            "compacton_character_identity": max(random_identity_residuals),
        },
        "verdict": {
            "coefficient_free_kinematic_selector_exists": True,
            "selector_is_parent_action_term": False,
            "affine_sink_contains_plus_minus_i_after_choosing_C4": True,
            "C4_choice_is_canonical_under_full_affine_symmetry": False,
            "canonical_affine_link_drives_character_purification": False,
            "autonomous_capture_mechanism_derived": False,
            "status": "the compacton orbit has an exact coefficient-free character-purity defect whose zero locus is the plus/minus i pair, but the full affine S4 parent has no canonical C4 subgroup, its canonical link is isotropic, and finite coherent transfer preserves character weights and recurs; the clue is a valid diagnostic, not a derived matter-birth dynamics",
            "next_gate": "version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate",
        },
    }

    assert result["compacton_character_selector"]["zero_phase_points"] == [0.5, 1.5]
    assert full_commutant_dimension == 2
    assert triplet_commutant_dimension == 1
    assert len(four_cycles) == 6
    assert len(cyclic_subgroups) == 3
    assert len(oriented_plus_i_projectors) == 6
    assert len(unoriented_pm_i_planes) == 3
    assert maximum_chosen_plane_commutator > 1.0
    assert all(value < 2.0e-12 for value in result["maximum_residuals"].values())
    assert result["dynamical_obstruction"]["recurrence_residual_at_pi"] < 1.0e-12

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()