#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate_results.json"


def rows(matrix: sp.ImmutableMatrix) -> list[list[int]]:
    return [list(map(int, matrix.row(index))) for index in range(matrix.rows)]


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.combined_matrix.shape == (16, 5)
    assert certificate.combined_matrix.rank() == 5
    assert all(vector == sp.zeros(4, 1) for vector in certificate.pass_vectors)
    assert certificate.package_dependency.rank() == 4
    assert certificate.package_availability == sp.zeros(4, 1)
    assert certificate.conditional_anchor_map.rank() == 1
    assert len(certificate.conditional_anchor_map.nullspace()) == 3
    assert certificate.fully_anchored_map.rank() == 4

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "criteria": [
            "correct_type_and_dimension",
            "internally_available",
            "independent_of_kappa",
            "common_parent_origin",
            "non_circular",
        ],
        "candidate_menus": {
            "G": {
                "candidates": ["induced_Einstein_coefficient", "spectral_action_coefficient", "imported_Newton_constant", "solved_from_target_relation"],
                "matrix": rows(certificate.gravity_candidates),
                "rank": 3,
                "maximum_score": "3/5",
                "passing": 0,
            },
            "Theta": {
                "candidates": ["KMS_energy", "endpoint_spectral_gap", "external_Landauer_temperature", "vacuum_action"],
                "matrix": rows(certificate.temperature_candidates),
                "rank": 4,
                "maximum_score": "4/5",
                "passing": 0,
            },
            "v_cell": {
                "candidates": ["intrinsic_cell_volume", "spectral_counting_volume", "topological_volume_quantum", "cosmological_radius_volume"],
                "matrix": rows(certificate.volume_candidates),
                "rank": 2,
                "maximum_score": "4/5",
                "passing": 0,
            },
            "T_flow": {
                "candidates": ["entropy_scalar", "isotropic_vacuum_ansatz", "metric_variation_of_current_parent", "Keldysh_response_tensor"],
                "matrix": rows(certificate.stress_candidates),
                "rank": 3,
                "maximum_score": "4/5",
                "passing": 0,
            },
        },
        "combined_audit": {
            "candidate_count": 16,
            "criterion_count": 5,
            "combined_matrix_rank": 5,
            "complete_candidates": 0,
        },
        "package_dependency": {
            "components": ["G", "Theta", "v_cell", "T_flow"],
            "dependency_rank": 4,
            "complete_components": "0/4",
            "conditional_scale_relation_rank": 1,
            "conditional_scale_relation_nullity": 3,
            "rank_after_complete_package": 4,
        },
        "status": {
            "audit_coverage": "16/16",
            "individual_candidate_passes": "0/16",
            "complete_anchor_components": "0/4",
            "absolute_conductance": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "any_complete_G_candidate": False,
            "any_complete_Theta_candidate": False,
            "any_complete_volume_candidate": False,
            "any_complete_stress_candidate": False,
            "complete_Einstein_anchor_package_exists": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()