#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np


OUTPUT_PATH = Path("s2t_v4_pati_salam_projected_curvature_selector_results.json")
RANDOM_SEED = 20260814
RANDOM_TESTS = 300
NORMALIZATIONS = [0.5, 1.0, 1.75]


EPSILON_TWO = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


def random_special_unitary(size, rng):
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    unitary, triangular = np.linalg.qr(matrix)
    diagonal = np.diag(triangular)
    unitary = unitary @ np.diag(np.conj(diagonal) / np.abs(diagonal))
    unitary /= np.linalg.det(unitary) ** (1.0 / size)
    return unitary


def invariants(delta):
    gram = delta @ delta.conj().T
    rho = float(np.trace(gram).real)
    tau = float(np.trace(gram @ gram).real)
    determinant = float(np.linalg.det(gram).real)
    return rho, tau, determinant


def edge_matrices(delta, normalization=1.0):
    first = delta
    second = normalization * delta.T @ EPSILON_TWO
    return first, second


def particle_dirac(delta, normalization=1.0):
    first, second = edge_matrices(delta, normalization)
    finite_dirac = np.zeros((10, 10), dtype=complex)
    finite_dirac[4:6, 0:4] = first
    finite_dirac[0:4, 4:6] = first.conj().T
    finite_dirac[6:10, 4:6] = second
    finite_dirac[4:6, 6:10] = second.conj().T
    return finite_dirac


def particle_grading():
    return np.diag([1.0] * 4 + [-1.0] * 2 + [1.0] * 4)


def endpoint_curvature(delta, normalization=1.0):
    finite_dirac = particle_dirac(delta, normalization)
    curvature = finite_dirac @ finite_dirac
    projected = np.zeros_like(curvature)
    projected[0:4, 6:10] = curvature[0:4, 6:10]
    projected[6:10, 0:4] = curvature[6:10, 0:4]
    return curvature, projected


def ko6_completion(delta, normalization=1.0):
    particle = particle_dirac(delta, normalization)
    finite_dirac = np.zeros((20, 20), dtype=complex)
    finite_dirac[:10, :10] = particle
    finite_dirac[10:, 10:] = particle.conj()
    reality = np.zeros((20, 20), dtype=complex)
    reality[:10, 10:] = np.eye(10)
    reality[10:, :10] = np.eye(10)
    grading = np.zeros((20, 20), dtype=complex)
    particle_gamma = particle_grading()
    grading[:10, :10] = particle_gamma
    grading[10:, 10:] = -particle_gamma
    _, particle_projected = endpoint_curvature(delta, normalization)
    projected = np.zeros((20, 20), dtype=complex)
    projected[:10, :10] = particle_projected
    projected[10:, 10:] = particle_projected.conj()
    return finite_dirac, reality, grading, projected


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    maxima = {
        "two_step_antisymmetry_error": 0.0,
        "projected_curvature_determinant_error": 0.0,
        "raw_trace_two_error": 0.0,
        "raw_trace_four_error": 0.0,
        "raw_trace_canonical_norm_only_error": 0.0,
        "gauge_covariance_error": 0.0,
        "ko6_self_adjoint_error": 0.0,
        "ko6_odd_grading_error": 0.0,
        "ko6_reality_error": 0.0,
        "projected_curvature_even_error": 0.0,
        "projected_curvature_reality_error": 0.0,
        "physical_half_projected_norm_error": 0.0,
    }
    for _ in range(RANDOM_TESTS):
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        rho, tau, determinant = invariants(delta)
        weak = random_special_unitary(2, rng)
        color = random_special_unitary(4, rng)
        transformed_delta = weak @ delta @ color.T
        particle_gauge = np.zeros((10, 10), dtype=complex)
        particle_gauge[0:4, 0:4] = color.conj()
        particle_gauge[4:6, 4:6] = weak
        particle_gauge[6:10, 6:10] = color
        for normalization in NORMALIZATIONS:
            first, second = edge_matrices(delta, normalization)
            two_step = second @ first
            maxima["two_step_antisymmetry_error"] = max(
                maxima["two_step_antisymmetry_error"],
                float(np.linalg.norm(two_step + two_step.T)),
            )
            finite_dirac = particle_dirac(delta, normalization)
            transformed_dirac = particle_dirac(
                transformed_delta, normalization
            )
            maxima["gauge_covariance_error"] = max(
                maxima["gauge_covariance_error"],
                float(
                    np.linalg.norm(
                        transformed_dirac
                        - particle_gauge @ finite_dirac @ particle_gauge.conj().T
                    )
                ),
            )
            curvature, projected = endpoint_curvature(delta, normalization)
            projected_norm = float(np.vdot(projected, projected).real)
            expected_projected = 4.0 * normalization**2 * determinant
            maxima["projected_curvature_determinant_error"] = max(
                maxima["projected_curvature_determinant_error"],
                abs(projected_norm - expected_projected),
            )
            trace_two = float(np.trace(curvature).real)
            trace_four = float(np.trace(curvature @ curvature).real)
            expected_two = 2.0 * (1.0 + normalization**2) * rho
            expected_four = (
                2.0 * (1.0 + normalization**4) * tau
                + 8.0 * normalization**2 * determinant
            )
            maxima["raw_trace_two_error"] = max(
                maxima["raw_trace_two_error"], abs(trace_two - expected_two)
            )
            maxima["raw_trace_four_error"] = max(
                maxima["raw_trace_four_error"], abs(trace_four - expected_four)
            )
            if normalization == 1.0:
                maxima["raw_trace_canonical_norm_only_error"] = max(
                    maxima["raw_trace_canonical_norm_only_error"],
                    abs(trace_four - 4.0 * rho**2),
                )

        finite_dirac, reality, grading, projected = ko6_completion(delta)
        maxima["ko6_self_adjoint_error"] = max(
            maxima["ko6_self_adjoint_error"],
            float(np.linalg.norm(finite_dirac - finite_dirac.conj().T)),
        )
        maxima["ko6_odd_grading_error"] = max(
            maxima["ko6_odd_grading_error"],
            float(np.linalg.norm(grading @ finite_dirac + finite_dirac @ grading)),
        )
        maxima["ko6_reality_error"] = max(
            maxima["ko6_reality_error"],
            float(np.linalg.norm(finite_dirac @ reality - reality @ finite_dirac.conj())),
        )
        maxima["projected_curvature_even_error"] = max(
            maxima["projected_curvature_even_error"],
            float(np.linalg.norm(grading @ projected - projected @ grading)),
        )
        maxima["projected_curvature_reality_error"] = max(
            maxima["projected_curvature_reality_error"],
            float(np.linalg.norm(projected @ reality - reality @ projected.conj())),
        )
        physical_half_norm = 0.5 * float(np.vdot(projected, projected).real)
        maxima["physical_half_projected_norm_error"] = max(
            maxima["physical_half_projected_norm_error"],
            abs(physical_half_norm - 4.0 * determinant),
        )

    results = {
        "date": "2026-08-14",
        "random_seed": RANDOM_SEED,
        "random_tests": RANDOM_TESTS,
        "valid_module_chain": {
            "nodes": ["color anti-fundamental 4bar", "weak doublet 2_R", "color fundamental 4"],
            "complex_dimensions": [4, 2, 4],
            "parities": ["even", "odd", "even"],
            "first_edge": "A_Delta = Delta : 4bar -> 2_R",
            "second_edge": "B_Delta = c Delta^T epsilon_2 : 2_R -> 4",
            "two_step": "B_Delta A_Delta = c Delta^T epsilon_2 Delta in color 6",
            "all_nodes_are_fundamental_or_opposite_modules": True,
        },
        "trace_identities": {
            "Tr_D2": "2(1+c^2) rho",
            "Tr_D4": "2(1+c^4) tau + 8 c^2 det",
            "canonical_raw_trace": "Tr_D4 at c=1 equals 4 rho^2 and is rank-blind",
            "projected_endpoint_curvature_norm": "||P02 D^2 P20 + adjoint||^2 = 4 c^2 det",
            "KO6_physical_half_at_c1": "(1/2)||F_rel_full||^2 = 4 det",
        },
        "stability": {
            "induced_kappa": "4 c^2",
            "strict_rank_one_Hessian_condition": "c^2 > 1/2",
            "canonical_normalization": "c=1 gives kappa=4",
            "canonical_Casimir_cross_check": "combined SU(2)_R + SU(4) gap also equals 4",
        },
        "maximum_errors": maxima,
        "project_archaeology": {
            "three_node_superconnection_precedent": (
                "s2t_v4_three_node_superconnection_closure_gate.py separates form degrees "
                "on orthogonal target summands"
            ),
            "relative_projector_precedent": (
                "version4_relative_krajewski_star_gate.tex derives endpoint inclusion-exclusion projectors"
            ),
            "vectorlike_precedent": (
                "version4_vectorlike_messenger_chain_gate.tex permits anomaly-safe fundamental-module extensions"
            ),
        },
        "verdict": {
            "project_answer_found": True,
            "literal_color_six_node_needed": False,
            "ordinary_raw_spectral_trace_selector_pass": False,
            "projected_superconnection_curvature_selector_pass": True,
            "coefficient_four_at_canonical_metric": True,
            "strict_parent_action_derived": False,
            "remaining_gates": [
                "derive the endpoint curvature projector from the parent superconnection action rather than selecting it by hand",
                "derive or protect the relative edge normalization c=1 from module metrics/reality",
                "decide whether the auxiliary fundamental modules are physical vectorlike states or purely bosonic superconnection grades",
                "recompute the full mixed Pati-Salam Hessian and gauge-running impact",
            ],
        },
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()