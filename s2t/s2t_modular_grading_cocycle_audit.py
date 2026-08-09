#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


TREE_EDGES = [(1, 0), (2, 1)]
TRIANGLE_EDGES = [(1, 0), (2, 1), (2, 0)]


def incidence_matrix(edges):
    matrix = np.zeros((3, len(edges)), dtype=int)
    for column, (target, source) in enumerate(edges):
        matrix[source, column] = -1
        matrix[target, column] = 1
    return matrix


def admissible_gradings(edges):
    rows = []
    for signs in itertools.product([-1, 1], repeat=3):
        odd_edges = [signs[target] == -signs[source] for target, source in edges]
        if all(odd_edges):
            rows.append(list(signs))
    return rows


def matrix_unit(row, column):
    result = np.zeros((3, 3), dtype=complex)
    result[row, column] = 1.0
    return result


def phased_edge(edge, phase):
    target, source = edge
    unit = matrix_unit(target, source)
    return np.exp(1j * phase) * unit + np.exp(-1j * phase) * unit.conj().T


def diagonalizer(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    minimum_gap = float(np.min(np.abs(np.diff(eigenvalues))))
    return eigenvectors, minimum_gap


def jarlskog(matrix):
    return float(
        np.imag(
            matrix[0, 0]
            * matrix[1, 1]
            * np.conj(matrix[0, 1])
            * np.conj(matrix[1, 0])
        )
    )


def mixing_test(upper, lower):
    upper_vectors, upper_gap = diagonalizer(upper)
    lower_vectors, lower_gap = diagonalizer(lower)
    mixing = upper_vectors.conj().T @ lower_vectors
    invariant = jarlskog(mixing)
    return {
        "upper_minimum_gap": upper_gap,
        "lower_minimum_gap": lower_gap,
        "minimum_absolute_entry": float(np.min(np.abs(mixing))),
        "full_mixing": bool(np.all(np.abs(mixing) > 1e-8)),
        "Jarlskog": invariant,
        "nonzero_CP": abs(invariant) > 1e-9,
    }


def exact_triangle_invariant():
    phase_10, phase_21, phase_20 = sp.symbols(
        "phi_10 phi_21 phi_20", real=True
    )
    imaginary_unit = sp.I
    level_operator = sp.diag(1 / sp.pi, 2 / sp.pi, 3 / sp.pi)

    def exact_unit(row, column):
        return sp.eye(3)[:, row] * sp.eye(3)[column, :]

    def exact_edge(edge, phase):
        target, source = edge
        unit = exact_unit(target, source)
        return (
            sp.exp(imaginary_unit * phase) * unit
            + sp.exp(-imaginary_unit * phase) * unit.conjugate().T
        )

    upper = level_operator + exact_edge((2, 0), phase_20)
    lower = (
        level_operator
        + exact_edge((1, 0), phase_10)
        + exact_edge((2, 1), phase_21)
    )
    commutator = upper * lower - lower * upper
    trace_cube = sp.trigsimp(
        sp.simplify(sp.expand_complex(sp.trace(commutator**3)))
    )
    expected = (
        12
        * imaginary_unit
        * (1 + sp.pi**2)
        * sp.sin(phase_10 + phase_21 - phase_20)
        / sp.pi**3
    )
    assert sp.simplify(trace_cube - expected) == 0
    return {
        "flux": "Phi=phi_10+phi_21-phi_20",
        "trace_commutator_cube": "12*i*(1+pi^2)*sin(Phi)/pi^3",
        "CP_condition": "sin(Phi) nonzero",
    }


def main():
    identity2 = np.eye(2, dtype=int)
    translation_x = affine_permutation(identity2, (1, 0))
    translation_y = affine_permutation(identity2, (0, 1))
    basis = triplet_basis()
    restricted_x = restrict(permutation_matrix(translation_x), basis)
    restricted_y = restrict(permutation_matrix(translation_y), basis)
    factor_operator = (1.0 / math.pi) * (np.eye(3) - restricted_x) + (
        1.0 / (2.0 * math.pi)
    ) * (np.eye(3) - restricted_y)
    factor_eigenvalues = np.linalg.eigvalsh(factor_operator)
    expected_levels = np.arange(1, 4, dtype=float) / math.pi
    modular_frequencies = {
        (target, source): expected_levels[target] - expected_levels[source]
        for target, source in itertools.product(range(3), repeat=2)
        if expected_levels[target] > expected_levels[source]
    }
    minimum_frequency = min(modular_frequencies.values())
    derived_tree_edges = [
        edge
        for edge, frequency in modular_frequencies.items()
        if abs(frequency - minimum_frequency) < 1e-12
    ]

    tree_incidence = incidence_matrix(TREE_EDGES)
    triangle_incidence = incidence_matrix(TRIANGLE_EDGES)
    tree_rank = int(np.linalg.matrix_rank(tree_incidence))
    triangle_rank = int(np.linalg.matrix_rank(triangle_incidence))
    tree_cycle_rank = len(TREE_EDGES) - tree_rank
    triangle_cycle_rank = len(TRIANGLE_EDGES) - triangle_rank

    tree_gradings = admissible_gradings(TREE_EDGES)
    triangle_gradings = admissible_gradings(TRIANGLE_EDGES)
    level_operator = np.diag([1.0, 2.0, 3.0]).astype(complex) / math.pi

    phase_grid = np.linspace(0.0, 2.0 * math.pi, 17, endpoint=False)
    shared_tree_rows = []
    for primitive in TREE_EDGES:
        for phase_10, phase_21 in itertools.product(phase_grid, repeat=2):
            phase_by_edge = {
                (1, 0): phase_10,
                (2, 1): phase_21,
            }
            shared_tree_rows.append(
                {
                    "primitive_edge": list(primitive),
                    "phase_10": float(phase_10),
                    "phase_21": float(phase_21),
                    **mixing_test(
                        level_operator + phased_edge(primitive, phase_by_edge[primitive]),
                        level_operator
                        + phased_edge((1, 0), phase_10)
                        + phased_edge((2, 1), phase_21),
                    ),
                }
            )

    relative_sector_rows = []
    for primitive in TREE_EDGES:
        for upper_phase, lower_phase_10, lower_phase_21 in itertools.product(
            np.linspace(0.0, 2.0 * math.pi, 9, endpoint=False), repeat=3
        ):
            relative_sector_rows.append(
                {
                    "primitive_edge": list(primitive),
                    "upper_phase": float(upper_phase),
                    "lower_phase_10": float(lower_phase_10),
                    "lower_phase_21": float(lower_phase_21),
                    **mixing_test(
                        level_operator + phased_edge(primitive, upper_phase),
                        level_operator
                        + phased_edge((1, 0), lower_phase_10)
                        + phased_edge((2, 1), lower_phase_21),
                    ),
                }
            )

    triangle_rows = []
    for flux in np.linspace(0.0, 2.0 * math.pi, 65, endpoint=False):
        triangle_rows.append(
            {
                "flux": float(flux),
                **mixing_test(
                    level_operator + phased_edge((2, 0), -flux),
                    level_operator
                    + phased_edge((1, 0), 0.0)
                    + phased_edge((2, 1), 0.0),
                ),
            }
        )

    exact_invariant = exact_triangle_invariant()
    results = {
        "status": "the_A3_grading_is_unique_but_tree_cocycles_are_trivial_and_the_minimal_CP_cycle_conflicts_with_an_odd_Dirac_graph",
        "date": "2026-08-06",
        "blind_protocol": {
            "observed_CKM_or_masses_loaded": False,
            "continuous_parameters_fitted": False,
            "input": "the modular A3 chain and unit edge coefficients",
        },
        "factor_modular_gate": {
            "operator": "L=pi^(-1)(I-T_RP3)+(2pi)^(-1)(I-T_S1)",
            "computed_eigenvalues": factor_eigenvalues.tolist(),
            "exact_spectrum": ["1/pi", "2/pi", "3/pi"],
            "maximum_absolute_error": float(
                np.max(np.abs(factor_eigenvalues - expected_levels))
            ),
            "minimum_positive_modular_frequency": "beta/pi",
            "derived_minimal_edges": [list(edge) for edge in derived_tree_edges],
            "unique_composition": "E_21 E_10=E_20",
            "positive_log_status": "Delta_rho(X)=rho X rho^(-1) is positive and has a unique self-adjoint logarithm, but it is a superoperator on M3 and is not Log(U)",
        },
        "grading_gate": {
            "condition": "Gamma D + D Gamma=0 requires opposite vertex signs across every Dirac edge",
            "tree_gradings": tree_gradings,
            "tree_projective_gradings": len(tree_gradings) // 2,
            "canonical_representative": [1, -1, 1],
            "triangle_gradings": triangle_gradings,
            "finding": "A3 has one grading up to global sign. Adding the 0-2 chord makes an odd cycle, so no Z2 grading can keep all three edges Dirac-odd.",
        },
        "cohomology_gate": {
            "tree": {
                "vertices": 3,
                "edges": len(TREE_EDGES),
                "incidence_rank": tree_rank,
                "cycle_rank": tree_cycle_rank,
                "H1_dimension": tree_cycle_rank,
                "finding": "Every U(1) edge phase on A3 is a vertex-gauge coboundary.",
            },
            "triangle": {
                "vertices": 3,
                "edges": len(TRIANGLE_EDGES),
                "incidence_rank": triangle_rank,
                "cycle_rank": triangle_cycle_rank,
                "H1_dimension": triangle_cycle_rank,
                "gauge_invariant_flux": exact_invariant["flux"],
            },
        },
        "shared_tree_connection_gate": {
            "phase_grid_per_edge": 17,
            "cases": len(shared_tree_rows),
            "full_mixing_cases": sum(row["full_mixing"] for row in shared_tree_rows),
            "nonzero_CP_cases": sum(row["nonzero_CP"] for row in shared_tree_rows),
            "maximum_absolute_Jarlskog": max(
                abs(row["Jarlskog"]) for row in shared_tree_rows
            ),
            "finding": "Arbitrary phases on one shared A3 connection are simultaneously gauge-removable from both sector readouts.",
        },
        "sector_specific_tree_warning": {
            "phase_grid_per_variable": 9,
            "cases": len(relative_sector_rows),
            "nonzero_CP_cases": sum(
                row["nonzero_CP"] for row in relative_sector_rows
            ),
            "finding": "Independent upper and lower edge phases can create CP, but they are two sector-specific connections and reintroduce the missing relative cocycle by hand.",
        },
        "minimal_cycle_gate": {
            "split_readout": "upper sector uses chord E_20; lower sector uses chain edges E_10 and E_21",
            "exact_CP_odd_invariant": exact_invariant,
            "sampled_fluxes": len(triangle_rows),
            "nonzero_CP_samples": sum(row["nonzero_CP"] for row in triangle_rows),
            "CP_zero_at_flux_zero": not triangle_rows[0]["nonzero_CP"],
            "finding": "The single triangle flux is sufficient for full mixing and CP whenever sin(Phi) is nonzero.",
        },
        "minimal_action_gate": {
            "positive_stiffness_potential": "V(Phi)=kappa*(1-cos(Phi)), kappa>0",
            "selected_flux": "Phi=0 mod 2pi",
            "CP_result": "zero",
            "negative_stiffness_warning": "Phi=pi also has sin(Phi)=0 and is CP-conserving",
            "nontrivial_flux_requirement": "A frustrated higher-harmonic potential, a discrete flux law or an explicitly oriented term is required; its coefficient or quantization rule is not derived by A3.",
        },
        "scientific_verdict": {
            "positive": "The modular chain fixes a unique projective grading, and closing it by one chord produces exactly one gauge-invariant flux with an exact CP-odd invariant proportional to sin(Phi).",
            "negative": "The unclosed A3 tree has no cohomological phase. The triangle cannot be the graph of a wholly odd Dirac operator under the same grading, and the minimal positive plaquette action selects the CP-conserving flux zero.",
            "status": "grading_gate_pass_tree_CP_no_go_triangle_flux_exists_but_parent_action_gate_fail",
            "next_gate": "Test a two-layer or graded-superconnection model in which A3 edges are Dirac-odd while the 0-2 chord is an even Higgs or curvature field, and require its flux potential to be fixed without CKM data.",
        },
    }

    assert tree_gradings == [[-1, 1, -1], [1, -1, 1]]
    assert np.allclose(factor_eigenvalues, expected_levels, atol=1e-12)
    assert derived_tree_edges == TREE_EDGES
    assert triangle_gradings == []
    assert tree_cycle_rank == 0
    assert triangle_cycle_rank == 1
    assert results["shared_tree_connection_gate"]["nonzero_CP_cases"] == 0
    assert results["sector_specific_tree_warning"]["nonzero_CP_cases"] > 0
    assert results["minimal_cycle_gate"]["nonzero_CP_samples"] == 64

    Path("s2t_modular_grading_cocycle_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "projective_A3_gradings": results["grading_gate"][
                    "tree_projective_gradings"
                ],
                "factor_spectrum": results["factor_modular_gate"]["exact_spectrum"],
                "tree_H1_dimension": tree_cycle_rank,
                "shared_tree_CP_cases": results["shared_tree_connection_gate"][
                    "nonzero_CP_cases"
                ],
                "triangle_H1_dimension": triangle_cycle_rank,
                "triangle_nonzero_CP_samples": results["minimal_cycle_gate"][
                    "nonzero_CP_samples"
                ],
                "triangle_odd_gradings": len(triangle_gradings),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()