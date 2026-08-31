#!/usr/bin/env python3
"""Lift and red-team the unique QL--YR Real intertwiner into uR."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_qlyr_ur_real_connector_lift_gate_results.json"
TOL = 1.0e-10


def random_unitary(rng, dimension):
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    q, r = np.linalg.qr(raw)
    phase = np.diag(r)
    return q @ np.diag(np.conj(phase / np.abs(phase)))


def main():
    previous = json.loads((ROOT / "s2t/results/s2t_v8_physical_arrow_endpoint_intertwiner_classification_gate_results.json").read_text(encoding="utf-8"))
    color = json.loads((ROOT / "s2t/results/s2t_v7_color_preserving_quadratic_selector_origin_gate_results.json").read_text(encoding="utf-8"))
    assert previous["intertwiner_dimensions"]["real_doubled_selected_hodge_support_to_endpoint"] == 1

    # Hom(C2_YR,C3_color tensor C2_weak) -> C3_uR by normalized weak trace.
    connector = np.zeros((3, 12), complex)
    for color_index in range(3):
        for weak in range(2):
            row = 2 * color_index + weak
            column = weak
            connector[color_index, row * 2 + column] = 1.0 / np.sqrt(2.0)

    initial = connector.conj().T @ connector
    final = connector @ connector.conj().T
    rng = np.random.default_rng(20260828)
    maximum_covariance_residual = 0.0
    for _ in range(30):
        g3 = random_unitary(rng, 3)
        g2 = random_unitary(rng, 2)
        phase = np.exp(1j * rng.uniform(-np.pi, np.pi) * 2.0 / 3.0)
        arrow_action = phase * np.kron(g3, np.kron(g2, g2.conj()))
        endpoint_action = phase * g3
        maximum_covariance_residual = max(maximum_covariance_residual, float(np.linalg.norm(
            connector @ arrow_action - endpoint_action @ connector
        )))

    zero12 = np.zeros((12, 12), complex)
    zero3 = np.zeros((3, 3), complex)
    real_operator = np.block([[zero12, connector.conj().T], [connector, zero3]])
    grading = np.diag(np.concatenate([np.ones(12), -np.ones(3)]))
    oddness = float(np.linalg.norm(grading @ real_operator + real_operator @ grading))
    square = real_operator @ real_operator

    negative_edges = set(color["hodge_selector"]["negative_edges"])
    positive_edges = set(color["hodge_selector"]["positive_edges"])
    qlyr = "Q_L--Y_R"
    active_projected_connector_norm = 0.0 if qlyr not in negative_edges else float(np.linalg.norm(connector))

    assert np.linalg.matrix_rank(connector, TOL) == 3
    assert np.linalg.norm(final - np.eye(3)) < TOL
    assert np.linalg.matrix_rank(initial, TOL) == 3
    assert np.linalg.norm(initial @ initial - initial) < TOL
    assert maximum_covariance_residual < TOL
    assert oddness < TOL
    assert np.linalg.norm(square - np.block([[initial, np.zeros((12, 3))], [np.zeros((3, 12)), np.eye(3)]])) < TOL
    assert qlyr in positive_edges and qlyr not in negative_edges
    assert active_projected_connector_norm == 0.0

    result = {
        "gate": "version8_qlyr_ur_real_connector_lift_gate",
        "normalized_weak_trace_connector": {
            "formula": "J(X)=Tr_weak(X)/sqrt(2)",
            "domain": "Hom(C2_YR,C3_color tensor C2_weak)",
            "codomain": "C3_uR",
            "matrix_shape": list(connector.shape),
            "rank": int(np.linalg.matrix_rank(connector, TOL)),
            "coisometry_residual": float(np.linalg.norm(final - np.eye(3))),
            "singlet_projector_rank": int(np.linalg.matrix_rank(initial, TOL)),
            "singlet_projector_residual": float(np.linalg.norm(initial @ initial - initial)),
            "maximum_gauge_covariance_residual": maximum_covariance_residual,
        },
        "real_lift": {
            "carrier_dimension": 15,
            "self_adjoint": True,
            "operator_rank": int(np.linalg.matrix_rank(real_operator, TOL)),
            "oddness_residual": oddness,
            "square_blocks": ["P_weak_singlet_rank3", "I3_uR"],
        },
        "final_color_selector_test": {
            "edge": qlyr,
            "casimir_eigenvalue": "8/5",
            "classified_as": "cycle_colored_virtual_bridge",
            "edge_is_positive_gapped_direction": qlyr in positive_edges,
            "edge_is_in_color_preserving_vacuum": qlyr in negative_edges,
            "active_projected_connector_norm": active_projected_connector_norm,
        },
        "reducibility": {
            "connected_arrow_singlet_rank": 3,
            "arrow_kernel_rank": 9,
            "connected_endpoint_rank": 3,
            "endpoint_complement_rank": 18,
            "nontrivial_reducing_complements_remain": True,
            "unique_common_trace_derived": False,
        },
        "verdict": {
            "unique_channel_has_explicit_canonical_lift": True,
            "real_and_gauge_compatibility_pass": True,
            "channel_survives_final_color_preserving_projector": False,
            "channel_connects_full_physical_carriers": False,
            "mass_metric_fixed": False,
            "branch_as_tome8_parent_closed": True,
            "status": "canonical_rank_three_lift_gapped_by_final_color_selector_no_go",
            "next_step": "return_to_pre_tome_trilemma_second_family_tensor_or_common_gauge_spacetime_trace",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()