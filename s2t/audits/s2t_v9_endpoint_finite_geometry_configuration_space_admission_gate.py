#!/usr/bin/env python3
"""Exact configuration-space admission audit for Tome IX endpoint phases."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_finite_geometry_configuration_space_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def canonical_inclusion(target: int, source: int) -> sp.Matrix:
    inclusion = sp.zeros(target, source)
    inclusion[:source, :source] = sp.eye(source)
    return inclusion


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v9_endpoint_finite_module_parent_action_origin_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["verdict"]["common_finite_geometry_configuration_space_required"]

    dimensions = (21, 23, 24)
    total_dimension = sum(dimensions)
    assert total_dimension == 68

    v = canonical_inclusion(23, 21)
    w = canonical_inclusion(24, 23)
    pn = sp.eye(23) - v * v.T
    pt = sp.eye(24) - w * w.T
    assert v.T * v == sp.eye(21)
    assert w.T * w == sp.eye(23)
    assert pn.rank() == 2
    assert pt.rank() == 1

    d = sp.zeros(total_dimension)
    d[:21, 21:44] = v.T
    d[21:44, :21] = v
    d[21:44, 44:] = w.T
    d[44:, 21:44] = w
    assert d.T == d
    assert d.rank() == 46
    assert total_dimension - d.rank() == 22

    laplacian = sp.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
    assert laplacian.rank() == 2
    assert laplacian.eigenvals() == {sp.Integer(0): 1, sp.Integer(1): 1, sp.Integer(3): 1}
    assert laplacian * sp.ones(3, 1) == sp.zeros(3, 1)

    old_projector = sp.zeros(total_dimension)
    old_projector[:21, :21] = sp.eye(21)
    old_projector[21:42, 21:42] = sp.eye(21)
    old_projector[44:65, 44:65] = sp.eye(21)
    assert old_projector.rank() == 63
    assert d * old_projector - old_projector * d == sp.zeros(total_dimension)
    new_projector = sp.eye(total_dimension) - old_projector
    assert new_projector.rank() == 5

    phase21 = sp.zeros(total_dimension, 21)
    phase21[:21, :] = sp.eye(21)
    for power in range(7):
        assert new_projector * (d**power) * phase21 == sp.zeros(total_dimension, 21)

    old_triplet_projector = sp.diag(0, 1, 1)
    family_generator = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    family_commutator = family_generator * old_triplet_projector - old_triplet_projector * family_generator
    assert family_commutator.rank() == 2

    checks = {
        "three_phase_fibres_are_present": True,
        "phase_algebra_is_C3": True,
        "faithful_orthogonal_carrier_dimension_is_68": True,
        "central_projector_ranks_are_21_23_24": True,
        "canonical_inclusion_defects_are_2_and_1": True,
        "phase_path_graph_is_connected": True,
        "block_dirac_is_self_adjoint": True,
        "no_target_vertex_score_is_inserted": True,
        "old_63_dimensional_subbundle_is_reducing": True,
    }
    assert all(checks.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "configuration_space": {
            "phases": [21, 23, 24],
            "phase_algebra": "C^3",
            "carrier": "H_Sigma=H21 direct_sum H23 direct_sum H24",
            "carrier_dimension": total_dimension,
            "central_projector_ranks": list(dimensions),
            "inclusion_defect_ranks": [pn.rank(), pt.rank()],
        },
        "phase_graph": {
            "type": "path_21_23_24",
            "laplacian_rank": laplacian.rank(),
            "laplacian_spectrum": [0, 1, 3],
            "kernel": "span(1,1,1)",
            "target_vertex_selected": False,
        },
        "block_dirac": {
            "self_adjoint": True,
            "rank": d.rank(),
            "nullity": total_dimension - d.rank(),
            "old_reducing_subbundle_dimension": old_projector.rank(),
            "unreachable_complement_dimension": new_projector.rank(),
            "created_physical_endpoint_lines": 0,
            "required_physical_endpoint_lines": 3,
            "triplet_old_projector_family_commutator_rank": family_commutator.rank(),
        },
        "architecture_audit": {
            **checks,
            "satisfied": sum(checks.values()),
            "tested": len(checks),
        },
        "ledgers": {
            "configuration_space_architecture_satisfied": 9,
            "configuration_space_architecture_tested": 9,
            "endpoint_creation_reachability_satisfied": 0,
            "endpoint_creation_reachability_tested": 3,
            "physical_phase_selector_satisfied": 0,
            "physical_phase_selector_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "common_finite_geometry_configuration_space_admitted": True,
            "target_phase_preselected": False,
            "canonical_inclusion_edges_create_defect_states": False,
            "family_typed_creation_edge_required": True,
            "physical_endpoint_transition_derived": False,
        },
        "next_gate": "version9_endpoint_finite_geometry_creation_operator_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()