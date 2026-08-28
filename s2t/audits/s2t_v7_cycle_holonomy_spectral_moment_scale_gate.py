#!/usr/bin/env python3
"""Audit spectral visibility of the unique U(3) cycle holonomy and its scale."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_cycle_holonomy_spectral_moment_scale_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def random_unitary(rng: np.random.Generator, size: int = 3) -> np.ndarray:
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(matrix)
    phases = np.diag(r)
    phases = phases / np.abs(phases)
    return q @ np.diag(phases.conj())


def hermitian_basis_3() -> list[np.ndarray]:
    basis = []
    for index in range(3):
        matrix = np.zeros((3, 3), dtype=complex)
        matrix[index, index] = 1.0
        basis.append(matrix)
    for first in range(3):
        for second in range(first + 1, 3):
            symmetric = np.zeros((3, 3), dtype=complex)
            symmetric[first, second] = symmetric[second, first] = 1.0 / np.sqrt(2.0)
            basis.append(symmetric)
            antisymmetric = np.zeros((3, 3), dtype=complex)
            antisymmetric[first, second] = -1j / np.sqrt(2.0)
            antisymmetric[second, first] = 1j / np.sqrt(2.0)
            basis.append(antisymmetric)
    assert len(basis) == 9
    gram = np.array([[np.trace(a @ b).real for b in basis] for a in basis])
    assert np.max(np.abs(gram - np.eye(9))) < 1.0e-12
    return basis


def unitary_exponential(hermitian: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(hermitian)
    return vectors @ np.diag(np.exp(1j * values)) @ vectors.conj().T


def numerical_hessian(function, size: int, step: float = 2.0e-4) -> np.ndarray:
    origin = np.zeros(size)
    value_origin = function(origin)
    hessian = np.zeros((size, size))
    for first in range(size):
        ei = np.zeros(size)
        ei[first] = step
        hessian[first, first] = (
            function(ei) - 2.0 * value_origin + function(-ei)
        ) / step**2
        for second in range(first + 1, size):
            ej = np.zeros(size)
            ej[second] = step
            value = (
                function(ei + ej)
                - function(ei - ej)
                - function(-ei + ej)
                + function(-ei - ej)
            ) / (4.0 * step**2)
            hessian[first, second] = hessian[second, first] = value
    return hessian


def signature(matrix: np.ndarray, tolerance: float = 1.0e-4) -> dict[str, int]:
    values = np.linalg.eigvalsh(matrix)
    return {
        "negative": int(np.sum(values < -tolerance)),
        "zero": int(np.sum(np.abs(values) <= tolerance)),
        "positive": int(np.sum(values > tolerance)),
    }


def main() -> None:
    previous = load_result(
        "s2t_v7_real_arrow_bimodule_forest_quotient_gate_results.json"
    )
    assert previous["verdict"]["status"] == (
        "positive_real_arrow_correspondence_partial_frame_quotient_one_cycle_holonomy_physical_inner_fluctuation_no_go"
    )

    vertices = previous["selected_vacuum_graph"]["vertices"]
    baseline_edges = previous["full_graph_relative_to_frozen_H15"]["baseline_edges"]
    selected_edges = previous["selected_vacuum_graph"]["selected_edges"]
    full_edges = baseline_edges + selected_edges
    assert len(vertices) == len(full_edges) == 9

    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    holonomy_edge = "Q_L--Y_R"

    def adjacency(holonomy: np.ndarray, radius: float = 1.0) -> np.ndarray:
        matrix = np.zeros((3 * len(vertices), 3 * len(vertices)), dtype=complex)
        identity = np.eye(3)
        for name in full_edges:
            source, target = name.split("--")
            block = holonomy if name == holonomy_edge else identity
            if name in selected_edges:
                block = radius * block
            first = slice(3 * vertex_index[source], 3 * vertex_index[source] + 3)
            second = slice(3 * vertex_index[target], 3 * vertex_index[target] + 3)
            matrix[first, second] = block
            matrix[second, first] = block.conj().T
        return matrix

    rng = np.random.default_rng(20260827)
    identity = np.eye(3)
    maximum_second_residual = 0.0
    maximum_fourth_residual = 0.0
    maximum_sixth_residual = 0.0
    for _ in range(200):
        holonomy = random_unitary(rng)
        radius = float(rng.uniform(0.2, 1.8))
        operator = adjacency(holonomy, radius)
        reference = adjacency(identity, radius)
        traces = {
            degree: float(np.trace(np.linalg.matrix_power(operator, degree)).real)
            for degree in (2, 4, 6)
        }
        reference_traces = {
            degree: float(np.trace(np.linalg.matrix_power(reference, degree)).real)
            for degree in (2, 4, 6)
        }
        maximum_second_residual = max(
            maximum_second_residual, abs(traces[2] - reference_traces[2])
        )
        maximum_fourth_residual = max(
            maximum_fourth_residual, abs(traces[4] - reference_traces[4])
        )
        predicted_sixth_difference = (
            12.0 * radius**4 * (np.trace(holonomy).real - 3.0)
        )
        maximum_sixth_residual = max(
            maximum_sixth_residual,
            abs(traces[6] - reference_traces[6] - predicted_sixth_difference),
        )
    assert maximum_second_residual < 1.0e-10
    assert maximum_fourth_residual < 1.0e-10
    assert maximum_sixth_residual < 2.0e-9

    # Exact radial trace polynomials for the family-blind representative and
    # W=I.  Direct integer walk counts verify them at several radii.
    def radial_formulas(radius: float) -> dict[int, float]:
        return {
            2: 18.0 * (2.0 * radius**2 + 1.0),
            4: 6.0 * (18.0 * radius**4 + 10.0 * radius**2 + 5.0),
            6: 18.0
            * (18.0 * radius**6 + 19.0 * radius**4 + 8.0 * radius**2 + 3.0),
        }

    maximum_radial_residual = 0.0
    for radius in np.linspace(0.0, 2.0, 17):
        operator = adjacency(identity, float(radius))
        formulas = radial_formulas(float(radius))
        for degree in (2, 4, 6):
            direct = float(np.trace(np.linalg.matrix_power(operator, degree)).real)
            maximum_radial_residual = max(
                maximum_radial_residual, abs(direct - formulas[degree])
            )
    assert maximum_radial_residual < 1.0e-8

    # The first holonomy potential is 12*c6*Re Tr W.  Its minima are central,
    # and the full nine-dimensional tangent is lifted for c6 != 0.
    basis = hermitian_basis_3()
    holonomy_hessians = {}
    for coefficient in (-1.0, 1.0):
        central_minimum = identity if coefficient < 0.0 else -identity

        def potential(vector: np.ndarray) -> float:
            hermitian = sum(value * generator for value, generator in zip(vector, basis))
            holonomy = central_minimum @ unitary_exponential(hermitian)
            return float(12.0 * coefficient * np.trace(holonomy).real)

        hessian = numerical_hessian(potential, 9)
        hessian_signature = signature(hessian)
        assert hessian_signature == {"negative": 0, "zero": 0, "positive": 9}
        holonomy_hessians[str(coefficient)] = {
            "minimum": "I3" if coefficient < 0.0 else "-I3",
            "signature": hessian_signature,
            "eigenvalue_min": float(np.min(np.linalg.eigvalsh(hessian))),
            "eigenvalue_max": float(np.max(np.linalg.eigvalsh(hessian))),
        }

    # For S=c2 Tr D^2+c4 Tr D^4+c6 Tr D^6 and the minimizing central
    # holonomy (c6>0), the radial derivative is
    # 2r(a+2b r^2+3c r^4).  H15 fixes integer walk multiplicities but not the
    # three spectral-profile coefficients, so it cannot determine r=mu.
    radial_coefficients = {
        "a_r2": "36*c2+60*c4+144*c6",
        "b_r4_at_c6_positive_minimum": "108*c4+270*c6",
        "c_r6": "324*c6",
        "stationary_equation": "r*(a+2*b*r^2+3*c*r^4)=0",
    }

    result = {
        "gate": "version7_cycle_holonomy_spectral_moment_scale_gate",
        "graph": {
            "vertices": vertices,
            "baseline_edges": baseline_edges,
            "selected_edges": selected_edges,
            "unique_cycle": [
                "Q_L--u_R",
                "X_L--u_R",
                "X_L--e_R",
                "L_L--e_R",
                "L_L--Y_R",
                "Q_L--Y_R",
            ],
            "family_blind_baseline_assumption": True,
        },
        "spectral_visibility": {
            "degrees_tested": [2, 4, 6],
            "first_holonomy_sensitive_degree": 6,
            "TrD2_holonomy_independent": True,
            "TrD4_holonomy_independent": True,
            "TrD6_holonomy_term": "12*r^4*ReTr(W_C)",
            "maximum_second_moment_residual": maximum_second_residual,
            "maximum_fourth_moment_residual": maximum_fourth_residual,
            "maximum_sixth_identity_residual": maximum_sixth_residual,
        },
        "exact_radial_traces_at_trivial_holonomy": {
            "TrD2": "18*(2*r^2+1)",
            "TrD4": "6*(18*r^4+10*r^2+5)",
            "TrD6": "18*(18*r^6+19*r^4+8*r^2+3)",
            "maximum_direct_residual": maximum_radial_residual,
        },
        "sixth_moment_holonomy_potential": {
            "formula": "V6(W)=12*c6*r^4*ReTr(W)",
            "c6_negative_minimum": "W=I3",
            "c6_positive_minimum": "W=-I3",
            "noncentral_minimum_selected": False,
            "hessians": holonomy_hessians,
            "CKM_PMNS_derived": False,
        },
        "scale_test": {
            "spectral_polynomial": "S=c2 TrD2+c4 TrD4+c6 TrD6",
            "radial_coefficients": radial_coefficients,
            "H15_determines_integer_walk_multiplicities": True,
            "H15_determines_c2_c4_c6": False,
            "mu_determined_by_H15_alone": False,
            "nonzero_scale_requires_profile_coefficients_or_another_dynamic_level": True,
            "all_nonnegative_c2_c4_c6_make_origin_radially_stable": True,
        },
        "verdict": {
            "status": "positive_sixth_moment_holonomy_visibility_central_minimum_scale_no_go",
            "unique_cycle_holonomy_enters_derived_spectral_invariant": True,
            "holonomy_zero_modes_lifted_if_c6_nonzero": True,
            "nontrivial_family_mixing_selected": False,
            "moment_map_level_mu_derived": False,
            "complete_physical_parent_obtained": False,
            "next_gate": "test whether independently derived higher cycle characters can produce a noncentral conjugacy-class minimum without free spectral-profile ratios; otherwise freeze the family-mixing branch",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()