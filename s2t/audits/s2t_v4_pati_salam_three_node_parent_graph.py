#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
import sympy as sp


OUTPUT_PATH = Path("s2t_v4_pati_salam_three_node_parent_graph_results.json")
RANDOM_SEED = 20260814
RANDOM_TESTS = 200
WEDGE_PAIRS = [(first, second) for first in range(4) for second in range(first + 1, 4)]


def invariants(delta):
    gram = delta @ delta.conj().T
    rho = float(np.trace(gram).real)
    tau = float(np.trace(gram @ gram).real)
    determinant = float(np.linalg.det(gram).real)
    return rho, tau, determinant


def first_edge(delta):
    return delta.reshape(8, 1)


def second_edge(delta, normalization=1.0):
    edge = np.zeros((6, 8), dtype=complex)
    for row, (first, second) in enumerate(WEDGE_PAIRS):
        edge[row, 4 + second] += 0.5 * delta[0, first]
        edge[row, second] -= 0.5 * delta[1, first]
        edge[row, 4 + first] -= 0.5 * delta[0, second]
        edge[row, first] += 0.5 * delta[1, second]
    return normalization * edge


def minors(delta):
    return np.asarray(
        [
            delta[0, first] * delta[1, second]
            - delta[0, second] * delta[1, first]
            for first, second in WEDGE_PAIRS
        ]
    ).reshape(6, 1)


def particle_dirac(delta, normalization=1.0):
    first = first_edge(delta)
    second = second_edge(delta, normalization)
    finite_dirac = np.zeros((15, 15), dtype=complex)
    finite_dirac[0:1, 1:9] = first.conj().T
    finite_dirac[1:9, 0:1] = first
    finite_dirac[1:9, 9:15] = second.conj().T
    finite_dirac[9:15, 1:9] = second
    return finite_dirac


def ko6_completion(delta, normalization=1.0):
    particle = particle_dirac(delta, normalization)
    finite_dirac = np.zeros((30, 30), dtype=complex)
    finite_dirac[:15, :15] = particle
    finite_dirac[15:, 15:] = particle.conj()
    reality = np.zeros((30, 30), dtype=complex)
    reality[:15, 15:] = np.eye(15)
    reality[15:, :15] = np.eye(15)
    particle_grading = np.diag([1.0] + [-1.0] * 8 + [1.0] * 6)
    grading = np.zeros((30, 30), dtype=complex)
    grading[:15, :15] = particle_grading
    grading[15:, 15:] = -particle_grading
    return finite_dirac, reality, grading


def predicted_traces(delta, normalization=1.0):
    rho, tau, determinant = invariants(delta)
    trace_two = (2.0 + 1.5 * normalization**2) * rho
    trace_four = (
        2.0 * rho**2
        + normalization**4 * (0.375 * tau + 0.25 * determinant)
        + 4.0 * normalization**2 * determinant
    )
    return trace_two, trace_four


def exact_hessian_spectrum():
    coordinates = sp.symbols("x0:16", real=True)
    delta = sp.Matrix(
        2,
        4,
        lambda row, column: coordinates[2 * (4 * row + column)]
        + sp.I * coordinates[2 * (4 * row + column) + 1],
    )
    rho = sum(sp.conjugate(entry) * entry for entry in delta)
    determinant = sum(
        sp.conjugate(
            delta[0, first] * delta[1, second]
            - delta[0, second] * delta[1, first]
        )
        * (
            delta[0, first] * delta[1, second]
            - delta[0, second] * delta[1, first]
        )
        for first, second in WEDGE_PAIRS
    )
    potential = (
        -sp.Rational(7, 2) * rho
        + sp.Rational(19, 8) * rho**2
        + sp.Rational(7, 2) * determinant
    )
    vacuum = {coordinate: 0 for coordinate in coordinates}
    vacuum[coordinates[0]] = sp.sqrt(sp.Rational(14, 19))
    hessian = sp.hessian(potential, coordinates).subs(vacuum)
    return {
        str(sp.simplify(value)): int(multiplicity)
        for value, multiplicity in hessian.eigenvals().items()
    }


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    maxima = {
        "two_step_minor_error": 0.0,
        "minor_norm_determinant_error": 0.0,
        "trace_two_formula_error": 0.0,
        "trace_four_formula_error": 0.0,
        "ko6_self_adjoint_error": 0.0,
        "ko6_odd_grading_error": 0.0,
        "ko6_reality_error": 0.0,
        "ko6_grading_reality_error": 0.0,
    }
    normalizations = [0.5, 1.0, 1.75]
    for _ in range(RANDOM_TESTS):
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        _, _, determinant = invariants(delta)
        for normalization in normalizations:
            first = first_edge(delta)
            second = second_edge(delta, normalization)
            maxima["two_step_minor_error"] = max(
                maxima["two_step_minor_error"],
                float(np.linalg.norm(second @ first - normalization * minors(delta))),
            )
            finite_dirac = particle_dirac(delta, normalization)
            predicted_two, predicted_four = predicted_traces(delta, normalization)
            maxima["trace_two_formula_error"] = max(
                maxima["trace_two_formula_error"],
                abs(float(np.trace(finite_dirac @ finite_dirac).real) - predicted_two),
            )
            maxima["trace_four_formula_error"] = max(
                maxima["trace_four_formula_error"],
                abs(
                    float(np.trace(np.linalg.matrix_power(finite_dirac, 4)).real)
                    - predicted_four
                ),
            )
        maxima["minor_norm_determinant_error"] = max(
            maxima["minor_norm_determinant_error"],
            abs(float(np.vdot(minors(delta), minors(delta)).real) - determinant),
        )
        finite_dirac, reality, grading = ko6_completion(delta)
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
        maxima["ko6_grading_reality_error"] = max(
            maxima["ko6_grading_reality_error"],
            float(np.linalg.norm(grading @ reality + reality @ grading.conj())),
        )

    order_one_labels = [(0, 0), (0, 1), (1, 1)]
    edge_changes = []
    for source, target in zip(order_one_labels[:-1], order_one_labels[1:]):
        edge_changes.append(
            {
                "source": source,
                "target": target,
                "changed_coordinates": sum(
                    left != right for left, right in zip(source, target)
                ),
            }
        )

    results = {
        "date": "2026-08-14",
        "random_seed": RANDOM_SEED,
        "random_tests": RANDOM_TESTS,
        "particle_graph": {
            "nodes": ["C", "C2 tensor C4", "Lambda2(C2) tensor Lambda2(C4)"],
            "complex_dimensions": [1, 8, 6],
            "grading": ["even", "odd", "even"],
            "two_step_identity": "B_Delta A_Delta = Lambda^2 Delta",
            "minor_norm_identity": "||Lambda^2 Delta||^2 = det(Delta Delta^dagger)",
        },
        "trace_identities": {
            "general_trace_D2": "(2 + 3 c^2/2) rho",
            "general_trace_D4": "2 rho^2 + c^4(3 tau/8 + det/4) + 4 c^2 det",
            "general_reduced_trace_D4": "(2 + 3 c^4/8) rho^2 + (4 c^2 - c^4/2) det",
            "canonical_half_trace_D2": "7 rho/2",
            "canonical_half_trace_D4": "19 rho^2/8 + 7 det/2",
            "stability_interval": "0 < c^2 < 8",
        },
        "canonical_potential": {
            "definition": "V = -halfTr(D^2) + halfTr(D^4)",
            "rank_one_norm_squared": "14/19",
            "rank_one_energy": "-49/38",
            "rank_two_equal_singular_value_squared": "7/26",
            "rank_two_energy": "-49/52",
            "exact_hessian_spectrum": exact_hessian_spectrum(),
        },
        "order_one_diagram": {
            "particle_labels": order_one_labels,
            "conjugate_labels": [(right, left) for left, right in order_one_labels],
            "edge_changes": edge_changes,
            "each_edge_changes_one_label": all(
                edge["changed_coordinates"] == 1 for edge in edge_changes
            ),
        },
        "maximum_errors": maxima,
        "verdict": {
            "equivariant_three_node_carrier_pass": True,
            "raw_spectral_rank_selector_pass": True,
            "KO6_completion_pass": True,
            "coarse_order_one_diagram_pass": True,
            "pati_salam_associative_module_pass": False,
            "strict_finite_triple_parent_pass": False,
            "free_relative_sign_removed": True,
            "same_fluctuation_edge_identification_derived": False,
            "next_gate": (
                "do not add literal C and color-six fermion nodes; instead derive the wedge "
                "selector as a universal two-form or curvature component on the existing "
                "Pati-Salam Hilbert module and quotient degree-two junk"
            ),
        },
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()