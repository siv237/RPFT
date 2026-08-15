#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def translation_matrix(delta):
    matrix = np.zeros((4, 4), dtype=complex)
    for point in POINTS:
        image = ((point[0] + delta[0]) % 2, (point[1] + delta[1]) % 2)
        matrix[POINT_INDEX[image], POINT_INDEX[point]] = 1.0
    return matrix


def oriented_incidence(edges):
    incidence = np.zeros((4, len(edges)), dtype=complex)
    for column, (source, target, phase, weight) in enumerate(edges):
        incidence[source, column] = -math.sqrt(weight)
        incidence[target, column] = math.sqrt(weight) * phase
    return incidence


def spectrum(matrix):
    return np.linalg.eigvalsh(matrix).real.tolist()


def multiplicities(values, tolerance=1e-9):
    groups = []
    for value in sorted(values):
        if not groups or abs(value - groups[-1][0]) > tolerance:
            groups.append([value, 1])
        else:
            groups[-1][1] += 1
    return [{"eigenvalue": value, "multiplicity": count} for value, count in groups]


def main():
    weight_rp3 = 1.0 / math.pi
    weight_s1 = 1.0 / (2.0 * math.pi)
    # One oriented representative for each undirected edge of the weighted square.
    trivial_edges = [
        (0, 1, 1.0, weight_rp3),
        (2, 3, 1.0, weight_rp3),
        (0, 2, 1.0, weight_s1),
        (1, 3, 1.0, weight_s1),
    ]
    # Put the unique nontrivial Z2 holonomy on one edge. The plaquette product is -1.
    pi_flux_edges = [
        (0, 1, 1.0, weight_rp3),
        (2, 3, 1.0, weight_rp3),
        (0, 2, 1.0, weight_s1),
        (1, 3, -1.0, weight_s1),
    ]

    incidence_trivial = oriented_incidence(trivial_edges)
    incidence_flux = oriented_incidence(pi_flux_edges)
    laplacian_trivial = incidence_trivial @ incidence_trivial.conj().T
    laplacian_flux = incidence_flux @ incidence_flux.conj().T
    translation_rp3 = translation_matrix((1, 0))
    translation_s1 = translation_matrix((0, 1))
    uniform = np.ones(4, dtype=complex) / 2.0
    triplet_projector = np.eye(4) - np.outer(uniform, uniform.conj())

    trivial_spectrum = spectrum(laplacian_trivial)
    flux_spectrum = spectrum(laplacian_flux)
    flux_uniform_leakage = float(
        np.linalg.norm(
            np.outer(uniform, uniform.conj())
            @ laplacian_flux
            @ triplet_projector
        )
    )

    # Eta/determinant values attached separately to the four spin structures
    # define multiplication operators unless a parallel transport is supplied.
    example_phase_values = np.array([1.0, -1.0, 1j, -1j], dtype=complex)
    determinant_phase_operator = np.diag(example_phase_values)

    results = {
        "status": "cellular_Dirac_and_determinant_line_reduce_to_commuting_diagonal_or_projective_even_multiplicity_cases",
        "date": "2026-08-05",
        "cellular_Dirac": {
            "vertex_space": "C[F2^2]",
            "edge_complex": "weighted square with RP3 and S1 edge directions",
            "Dirac_form": "D=[[0,B],[B*,0]]",
            "vertex_Laplacian": "Delta0=B B*",
            "trivial_connection_spectrum": trivial_spectrum,
            "expected_spectrum": [
                0.0,
                2 * weight_s1,
                2 * weight_rp3,
                2 * (weight_rp3 + weight_s1),
            ],
            "commutator_with_T_RP3": float(
                np.linalg.norm(
                    laplacian_trivial @ translation_rp3
                    - translation_rp3 @ laplacian_trivial
                )
            ),
            "commutator_with_T_S1": float(
                np.linalg.norm(
                    laplacian_trivial @ translation_s1
                    - translation_s1 @ laplacian_trivial
                )
            ),
            "finding": (
                "The canonical cellular Dirac square is exactly the weighted factor "
                "Laplacian already audited. It distinguishes labels but remains a commuting convolution operator."
            ),
        },
        "determinant_line_values": {
            "data_type": "one complex line/value for each spin structure",
            "without_parallel_transport": "diagonal multiplication operator",
            "example_off_diagonal_norm": float(
                np.linalg.norm(
                    determinant_phase_operator
                    - np.diag(np.diag(determinant_phase_operator))
                )
            ),
            "consequence": (
                "Eta invariants or determinant magnitudes can weight the three labels but do "
                "not define transition amplitudes between different spin structures."
            ),
        },
        "connection_classification": {
            "menu_translation_group": "Z2 x Z2",
            "projective_U1_classes": 2,
            "classes": [
                {
                    "plaquette_holonomy": "+1",
                    "result": "gauge-equivalent to the trivial commuting connection",
                },
                {
                    "plaquette_holonomy": "-1",
                    "result": "the projective pi-flux class UV=-VU",
                },
            ],
            "finding": (
                "A determinant-line parallel transport adds no third topological option on "
                "the Z2^2 torsor: it is either trivial or the already-audited projective class."
            ),
        },
        "pi_flux_cellular_test": {
            "spectrum": flux_spectrum,
            "multiplicities": multiplicities(flux_spectrum),
            "uniform_triplet_leakage": flux_uniform_leakage,
            "finding": (
                "The magnetic cellular Laplacian has two doubly-degenerate levels and does "
                "not preserve the uniform-plus-triplet split."
            ),
        },
        "spectral_flow_gate": {
            "edge_integers_or_phases": (
                "Spectral flow can orient or phase a chosen path between determinant fibers, "
                "but a graph of such paths is extra connection data."
            ),
            "closed_loop_content": (
                "Only the gauge-invariant plaquette holonomy survives vertex rephasings, "
                "reducing again to the trivial/projective dichotomy."
            ),
        },
        "scientific_verdict": {
            "cellular_Dirac": "returns the commuting factor Laplacian",
            "eta_or_determinant_values": "return diagonal weights",
            "determinant_connection": "returns either trivial transport or pi flux",
            "no_go": (
                "None of the canonical spin-structure spectral constructions selects one of "
                "the twelve outside-D8 full-M3 incidence directions."
            ),
            "reopening_condition": (
                "A boundary theory must supply a non-flat, non-translation-generated graph "
                "connection with fixed edge magnitudes and sector assignment."
            ),
        },
    }

    assert np.allclose(sorted(trivial_spectrum), sorted(results["cellular_Dirac"]["expected_spectrum"]))
    assert results["cellular_Dirac"]["commutator_with_T_RP3"] < 1e-12
    assert results["cellular_Dirac"]["commutator_with_T_S1"] < 1e-12
    assert results["determinant_line_values"]["example_off_diagonal_norm"] == 0.0
    assert [row["multiplicity"] for row in results["pi_flux_cellular_test"]["multiplicities"]] == [2, 2]
    assert flux_uniform_leakage > 0.1

    Path("s2t_spin_menu_dirac_determinant_line_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "trivial_spectrum": trivial_spectrum,
                "trivial_translation_commutators": [
                    results["cellular_Dirac"]["commutator_with_T_RP3"],
                    results["cellular_Dirac"]["commutator_with_T_S1"],
                ],
                "connection_classes": 2,
                "pi_flux_multiplicities": results["pi_flux_cellular_test"]["multiplicities"],
                "pi_flux_triplet_leakage": flux_uniform_leakage,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()