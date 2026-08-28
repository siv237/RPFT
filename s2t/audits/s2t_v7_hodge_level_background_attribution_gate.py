#!/usr/bin/env python3
"""Audit whether the frozen H15 moment uniquely fixes the edge Hodge level."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_hodge_level_background_attribution_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def matrix_to_int_list(matrix: np.ndarray) -> list[list[int]]:
    return [[int(round(value.real)) for value in row] for row in matrix]


def main() -> None:
    projector_result = load_result(
        "s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json"
    )
    edge_order = projector_result["edge_space"]["ordered_new_edges"]
    selected = set(projector_result["projector_union"]["selected_support"])
    assert len(edge_order) == 11 and len(selected) == 6

    # The typed H15 background is the direct sum of the three inequivalent
    # two-term Yukawa complexes.  This is the edge-resolved compression used
    # after the orthogonality result of the common-Higgs gate.
    baseline_order = ["u", "d", "e"]
    d15 = np.zeros((6, 6), dtype=complex)
    for index in range(3):
        d15[3 + index, index] = 1.0
    chi15 = np.diag([-1.0] * 3 + [1.0] * 3)
    k15 = d15 @ d15.conj().T - d15.conj().T @ d15
    dirac15 = d15 + d15.conj().T

    edge_projectors = []
    compressed_energies = []
    for index in range(3):
        projector = np.zeros((6, 6), dtype=complex)
        projector[index, index] = 1.0
        projector[3 + index, 3 + index] = 1.0
        edge_projectors.append(projector)
        compressed_energies.append(
            0.5 * np.trace(chi15 @ projector @ k15).real
        )
    compressed_energies = np.array(compressed_energies)
    assert np.max(np.abs(compressed_energies - 1.0)) < 1.0e-12
    assert abs(np.trace(dirac15 @ dirac15).real - 6.0) < 1.0e-12

    gamma_e = np.diag([-1.0 if edge in selected else 1.0 for edge in edge_order])
    gamma_hat = np.block(
        [
            [gamma_e, np.zeros_like(gamma_e)],
            [np.zeros_like(gamma_e), -gamma_e],
        ]
    )
    chi_e = np.diag([-1.0] * 11 + [1.0] * 11)
    source_real_exchange = np.block(
        [
            [np.zeros((3, 3)), np.eye(3)],
            [np.eye(3), np.zeros((3, 3))],
        ]
    )
    real_exchange = np.block(
        [
            [np.zeros((11, 11)), np.eye(11)],
            [np.eye(11), np.zeros((11, 11))],
        ]
    )

    # Every coefficient vector c defines an equivariant linear map
    # Psi_c(k)=<c,k> Gamma_hat.  The three coordinate functionals are linearly
    # independent as maps even though their images lie in the same target line.
    map_gram = np.eye(3) * np.trace(gamma_hat.conj().T @ gamma_hat).real
    map_space_dimension = int(np.linalg.matrix_rank(map_gram))
    assert map_space_dimension == 3

    # Exact gauge types distinguish all three old Yukawa edges.  If hypercharge
    # is forgotten, only u<->d remains; even then the invariant map space is 2D.
    exact_types = {
        "u": ("3", "1", "2/3"),
        "d": ("3", "1", "-1/3"),
        "e": ("1", "1", "-1"),
    }
    coarse_types = {
        edge: (representation[0], representation[1])
        for edge, representation in exact_types.items()
    }

    def type_orbits(types: dict[str, tuple[str, ...]]) -> list[list[str]]:
        classes: dict[tuple[str, ...], list[str]] = {}
        for edge, representation in types.items():
            classes.setdefault(representation, []).append(edge)
        return sorted((sorted(items) for items in classes.values()), key=lambda x: x[0])

    exact_type_orbits = type_orbits(exact_types)
    coarse_type_orbits = type_orbits(coarse_types)
    exact_invariant_dimension = len(exact_type_orbits)
    coarse_invariant_dimension = len(coarse_type_orbits)

    # Three scalar trace conventions from the preregistration.
    trace_d2 = float(np.trace(dirac15 @ dirac15).real)
    scalar_normalizations = {
        "full_vertex_trace_div_9": trace_d2 / 9.0,
        "active_vertex_trace_div_5": trace_d2 / 5.0,
        "oriented_edge_average_div_6": trace_d2 / 6.0,
    }

    # A general unequal family background exposes the unresolved direction in
    # coefficient space after the family-blind point (1,1,1) is left.
    unequal_k = np.array([1.0, 4.0, 9.0])
    normalized_positive_choices = {
        "equal_edge_weights": np.array([1.0, 1.0, 1.0]) / 3.0,
        "quark_symmetric_weights": np.array([0.25, 0.25, 0.5]),
        "strictly_positive_asymmetric_weights": np.array([0.5, 1.0 / 3.0, 1.0 / 6.0]),
    }
    unequal_outputs = {
        name: float(weights @ unequal_k)
        for name, weights in normalized_positive_choices.items()
    }
    assert len({round(value, 12) for value in unequal_outputs.values()}) == 3

    residuals = {
        "source_selfadjoint": float(np.linalg.norm(k15 - k15.conj().T)),
        "source_real_oddness": float(
            np.linalg.norm(
                source_real_exchange @ k15.conj() @ source_real_exchange + k15
            )
        ),
        "target_selfadjoint": float(np.linalg.norm(gamma_hat - gamma_hat.conj().T)),
        "target_involution": float(np.linalg.norm(gamma_hat @ gamma_hat - np.eye(22))),
        "target_grading_commutator": float(np.linalg.norm(chi_e @ gamma_hat - gamma_hat @ chi_e)),
        "target_real_oddness": float(
            np.linalg.norm(real_exchange @ gamma_hat.conj() @ real_exchange + gamma_hat)
        ),
    }
    assert max(residuals.values()) < 1.0e-12

    result = {
        "gate": "version7_hodge_level_background_attribution_gate",
        "typed_H15_background": {
            "baseline_edge_order": baseline_order,
            "two_term_complex_dimension": 6,
            "d15": matrix_to_int_list(d15),
            "chi15": matrix_to_int_list(chi15),
            "K15_commutator": matrix_to_int_list(k15),
            "Tr_D15_squared": trace_d2,
            "compressed_positive_edge_moments": compressed_energies.tolist(),
        },
        "target_edge_level": {
            "edge_order": edge_order,
            "selected_edges": sorted(selected),
            "Gamma_E_diagonal": [int(value) for value in np.diag(gamma_e)],
            "Gamma_hat_squared_trace": float(
                np.trace(gamma_hat.conj().T @ gamma_hat).real
            ),
            "residuals": residuals,
        },
        "equivariant_map_classification": {
            "formula": "Psi_c(K15)=(c_u*k_u+c_d*k_d+c_e*k_e)*Gamma_hat",
            "exact_baseline_gauge_types": {
                edge: list(representation)
                for edge, representation in exact_types.items()
            },
            "exact_gauge_type_orbits": exact_type_orbits,
            "minimal_exact_gauge_equivariant_real_dimension": exact_invariant_dimension,
            "coarse_u_d_exchange_orbits": coarse_type_orbits,
            "minimal_coarse_invariant_real_dimension": coarse_invariant_dimension,
            "map_gram_matrix": map_gram.tolist(),
            "map_space_rank": map_space_dimension,
            "positive_normalized_exact_family_dimension": 2,
            "positive_normalized_coarse_family_dimension": 1,
            "one_dimensional_unique_map_space": False,
            "full_S3_edge_symmetry_would_force_equal_weights": True,
            "full_S3_edge_symmetry_is_physically_available": False,
        },
        "normalization_comparison": {
            "family_blind_edge_moments": compressed_energies.tolist(),
            "scalar_trace_conventions": scalar_normalizations,
            "all_three_conventions_equal": len(
                {round(value, 12) for value in scalar_normalizations.values()}
            ) == 1,
            "normalization_fixed_by_word_normalized_trace": False,
        },
        "unequal_family_background": {
            "edge_moments": unequal_k.tolist(),
            "positive_normalized_weight_choices": {
                name: weights.tolist()
                for name, weights in normalized_positive_choices.items()
            },
            "resulting_relative_levels": unequal_outputs,
            "choice_independent": False,
        },
        "verdict": {
            "H15_supplies_nonzero_scale_observables": True,
            "H15_uniquely_selects_map_to_Gamma_hat": False,
            "relative_mu_over_H15_norm_derived": False,
            "absolute_scale_derived": False,
            "status": "no_go_nonunique_background_level_attribution",
            "next_gate": "freeze internal scale derivation and test whether one declared dimensionful calibration input suffices for all remaining Hodge-parent observables",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()