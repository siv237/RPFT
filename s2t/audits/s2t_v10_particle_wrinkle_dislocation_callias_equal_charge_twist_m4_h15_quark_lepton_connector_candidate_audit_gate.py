#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.direct_augmented_incidence.rank() == 4
    assert c.chirality * c.direct_bridge == sp.zeros(1, 1)
    assert c.color_label * c.direct_bridge == sp.ones(1, 1)
    assert c.hypercharge6 * c.direct_bridge == sp.ImmutableMatrix([[4]])
    assert c.r2_augmented_incidence.rank() == 4
    assert c.r2_augmented_incidence.cols - c.r2_augmented_incidence.rank() == 1
    assert c.r2_first_order_defect == sp.ones(2, 1)
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(11, 1)

    candidates = [
        "direct_Q_L_L_L_graph_edge",
        "inherited_Higgs_forest",
        "minimal_R2_pair_strict_SM_geometry",
        "R2_plus_tilde_R2_strict_geometry",
        "R2_generalized_first_order",
        "Pati_Salam_SU4_enlargement",
        "neutral_Callias_bridge",
        "composite_inherited_paths",
        "unified_vector_connector",
        "target_loaded_generalized_R2",
        "normalization_only_parent",
    ]
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "direct_graph_bridge": {
            "edge": "Q_L-L_L",
            "connects_components": True,
            "augmented_incidence_rank": 4,
            "laplacian_rank": 4,
            "kernel_dimension": 1,
            "chirality_difference": 0,
            "color_label_difference": 1,
            "six_hypercharge_difference": 4,
            "physical_Dirac_edge": False,
        },
        "minimal_typed_completion": {
            "multiplet": "R2=(3,2)_{7/6}",
            "edges": ["L_L-u_R", "Q_L-e_R"],
            "edge_count": 2,
            "augmented_incidence_rank": 4,
            "laplacian_rank": 4,
            "kernel_dimension": 1,
            "mixed_cycle_dimension": 1,
            "gauge_typed": True,
            "opposite_chirality": True,
        },
        "strict_first_order": {
            "vertex_coordinates": {
                "Q_L": ["H", "M3"],
                "L_L": ["H", "C"],
                "u_R": ["C", "M3"],
                "d_R": ["C", "M3"],
                "e_R": ["C", "C"],
            },
            "existing_edge_pass": [1, 1, 1],
            "missing_edge_pass": [0, 0, 0],
            "R2_edge_defects": [1, 1],
            "R2_admitted_on_fixed_SM_geometry": False,
        },
        "candidate_audit": {
            "criteria": [
                "connects_quark_lepton_components",
                "odd_chirality",
                "gauge_typed",
                "strict_first_order",
                "inherited_carrier",
                "independent_normalization",
            ],
            "candidates": candidates,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "matrix_rank": 6,
            "scores": list(map(int, c.score_vector)),
            "pass": list(map(int, c.pass_vector)),
            "coverage": list(map(int, c.coverage)),
            "passing_candidates": 0,
        },
        "status": {
            "abstract_direct_bridge": "graphically sufficient but physically mistyped",
            "minimal_physical_graph_completion": "R2 pair",
            "fixed_SM_strict_first_order": "closed",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "direct_Q_L_L_L_edge_is_physical": False,
            "R2_is_unique_one_multiplet_minimal_completion": True,
            "R2_passes_strict_first_order_on_fixed_SM_geometry": False,
            "connector_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()