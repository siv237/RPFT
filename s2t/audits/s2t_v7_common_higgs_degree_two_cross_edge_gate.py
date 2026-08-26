#!/usr/bin/env python3
"""Degree-two cross-edge support on the corrected H15 common-Higgs carrier."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_common_higgs_degree_two_cross_edge_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def normalized_higgs(rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=2) + 1j * rng.normal(size=2)
    return vector / np.linalg.norm(vector)


def higgs_conjugate(higgs: np.ndarray) -> np.ndarray:
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    return epsilon @ np.conj(higgs)


def physical_edges(higgs: np.ndarray) -> list[np.ndarray]:
    """Return u,d,e maps H_L^8 -> H_R^7 for one normalized Higgs doublet."""
    tilde = higgs_conjugate(higgs)
    up = np.zeros((7, 8), dtype=complex)
    down = np.zeros((7, 8), dtype=complex)
    electron = np.zeros((7, 8), dtype=complex)
    for colour in range(3):
        weak_slice = slice(2 * colour, 2 * colour + 2)
        up[colour, weak_slice] = np.conj(tilde)
        down[3 + colour, weak_slice] = np.conj(higgs)
    electron[6, 6:8] = np.conj(higgs)
    return [up, down, electron]


def random_field(rng: np.random.Generator) -> np.ndarray:
    return rng.normal(size=(3, 4)) + 1j * rng.normal(size=(3, 4))


def odd_arrow(operator: np.ndarray) -> np.ndarray:
    source = operator.shape[1]
    target = operator.shape[0]
    result = np.zeros((source + target, source + target), dtype=complex)
    result[source:, :source] = operator
    return result


def main() -> None:
    oneform = load_result("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
    endpoint = load_result("s2t_v7_corrected_vacuum_relative_edge_hessian_gate_results.json")
    torsion = load_result("s2t_v5_h15_spectral_torsion_selector_gate_results.json")

    intertwiner_matrix = np.array(
        oneform["charged_edge_multiplicity_space"]["intertwiner_dimension_matrix"]
    )
    assert np.array_equal(intertwiner_matrix, np.eye(3, dtype=int))
    assert endpoint["trace_metric_generalized_hessian"]["zero_count"] == 27

    rng = np.random.default_rng(20260826)
    higgs_orthogonality = []
    physical_left_cross = []
    physical_right_cross = []
    lifted_left_cross = []
    lifted_right_cross = []
    square_decomposition = []
    commutator_decomposition = []

    for _ in range(64):
        higgs = normalized_higgs(rng)
        tilde = higgs_conjugate(higgs)
        higgs_orthogonality.append(abs(np.vdot(tilde, higgs)))
        edges = physical_edges(higgs)
        fields = [random_field(rng) for _ in range(3)]
        lifted = [np.kron(field, edge) for field, edge in zip(fields, edges)]

        for first in range(3):
            for second in range(3):
                if first == second:
                    continue
                physical_left_cross.append(
                    np.linalg.norm(edges[first] @ edges[second].conj().T)
                )
                physical_right_cross.append(
                    np.linalg.norm(edges[first].conj().T @ edges[second])
                )
                lifted_left_cross.append(
                    np.linalg.norm(lifted[first] @ lifted[second].conj().T)
                )
                lifted_right_cross.append(
                    np.linalg.norm(lifted[first].conj().T @ lifted[second])
                )

        total = sum(lifted)
        square_decomposition.append(
            np.linalg.norm(
                total.conj().T @ total
                - sum(operator.conj().T @ operator for operator in lifted)
            )
            + np.linalg.norm(
                total @ total.conj().T
                - sum(operator @ operator.conj().T for operator in lifted)
            )
        )

        arrows = [odd_arrow(operator) for operator in lifted]
        total_arrow = sum(arrows)
        total_commutator = total_arrow @ total_arrow.conj().T - total_arrow.conj().T @ total_arrow
        edge_commutators = sum(
            arrow @ arrow.conj().T - arrow.conj().T @ arrow for arrow in arrows
        )
        commutator_decomposition.append(np.linalg.norm(total_commutator - edge_commutators))

    maxima = {
        "higgs_tilde_higgs_inner_product": float(max(higgs_orthogonality)),
        "physical_Ta_Tb_adjoint": float(max(physical_left_cross)),
        "physical_Ta_adjoint_Tb": float(max(physical_right_cross)),
        "lifted_Da_Db_adjoint": float(max(lifted_left_cross)),
        "lifted_Da_adjoint_Db": float(max(lifted_right_cross)),
        "degree_two_square_decomposition": float(max(square_decomposition)),
        "hodge_commutator_decomposition": float(max(commutator_decomposition)),
    }

    result = {
        "gate": "version7_common_higgs_degree_two_cross_edge_gate",
        "scope": {
            "carrier": "corrected E_aff tensor Lambda_ch on H_L^8 -> H_R^7",
            "physical_edges": ["u", "d", "e"],
            "common_normalized_Higgs": True,
            "degree": 2,
            "claim_about_raw_universal_forms_with_arbitrary_zero_form_insertions": False,
            "claim_about_physical_bimodule_endomorphism_projection": True,
        },
        "input_certificates": {
            "edge_intertwiner_dimension_matrix": intertwiner_matrix.tolist(),
            "pairwise_inequivalent_edges": oneform["charged_edge_multiplicity_space"][
                "pairwise_inequivalent_simple_edges"
            ],
            "current_endpoint_zero_modes": endpoint["trace_metric_generalized_hessian"][
                "zero_count"
            ],
        },
        "common_higgs_identities": {
            "formula": "tilde_H=i sigma_2 conjugate(H), H^* tilde_H=0",
            "maximum_residuals_over_64_trials": maxima,
        },
        "degree_two_support": {
            "mixed_physical_edge_word_count_before_projection": 6,
            "nonzero_direct_mixed_word_count": 0,
            "mixed_bimodule_endomorphism_dimension": int(
                np.sum(intertwiner_matrix) - np.trace(intertwiner_matrix)
            ),
            "full_square_equals_sum_of_edge_squares": True,
            "hodge_commutator_equals_sum_of_edge_commutators": True,
            "junk_quotient_can_create_absent_mixed_class": False,
        },
        "higher_degree_boundary": {
            "spectral_torsion_has_u_d_cross_sensitivity": torsion["verdict"][
                "spectral_torsion_is_nontrivial_on_H15"
            ]
            == "pass",
            "spectral_torsion_selects_unique_relative_Yukawa_ratios": torsion[
                "verdict"
            ]["spectral_torsion_selects_unique_relative_Yukawa_ratios"],
            "first_remaining_candidate_level": "derived quartic or higher typed invariant",
        },
        "verdict": {
            "common_Higgs_direct_degree_two_cross_edge_curvature": "closed_zero",
            "ordinary_physical_degree_two_lifts_relative_U3_frames": False,
            "full_raw_universal_calculus_classified": False,
            "reason": "direct mixed products vanish before junk and off-diagonal edge morphisms are absent after physical bimodule projection",
            "next_gate": "admission of a coefficient-free derived quartic cross-edge invariant on the corrected carrier",
        },
    }

    assert max(maxima.values()) < 1.0e-10
    assert result["degree_two_support"]["nonzero_direct_mixed_word_count"] == 0
    assert result["degree_two_support"]["mixed_bimodule_endomorphism_dimension"] == 0
    assert not result["verdict"]["ordinary_physical_degree_two_lifts_relative_U3_frames"]

    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()