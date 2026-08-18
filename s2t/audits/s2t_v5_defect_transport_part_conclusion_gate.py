#!/usr/bin/env python3
"""Machine-readable freeze of Tome V, Part II."""

from __future__ import annotations

import json
from pathlib import Path


RESULT = {
    "gate": "version5_defect_transport_part_conclusion_gate",
    "established": {
        "transition_language": True,
        "local_unitary_transport": True,
        "order_four_delay_character": True,
        "self_generated_nonlinear_wall_defect": True,
        "projective_RP2_point_charge": 1,
        "spinor_lift_first_Chern_number": 1,
        "conditional_internal_readout_rank_chain": [300, 45, 15, 2, 1],
    },
    "not_established": {
        "scalar_kink_is_point_particle_in_3_plus_1": False,
        "ungauged_projective_hedgehog_has_finite_energy": False,
        "vector_projector_mass_has_nonzero_Chern_index": False,
        "spinor_lift_is_function_of_projector_alone": False,
        "order_four_root_is_mandatorily_assigned_to_H15": False,
        "single_normalized_parent_functional": False,
        "physical_particle_closure": False,
    },
    "required_joint_extension": {
        "finite_energy_layer": "spatial family connection A_i with D_i P",
        "unit_index_layer": "oriented root/spinor lift from P to n.sigma",
        "must_share_one_parent_origin": True,
        "independent_sector_repairs_allowed": False,
    },
    "historical_intuition_status": {
        "literal_slow_light_particle": "rejected",
        "literal_time_loop_eternity": "rejected",
        "order_four_internal_phase": "retained",
        "unoriented_axis_and_double_lift": "retained",
        "particle_as_stable_transition_defect": "retained_as_program",
    },
    "verdict": {
        "part_II_as_scoped_mathematical_audit": "complete",
        "unified_physical_theory": "not_constructed",
        "automatic_next_gate": None,
        "reopening_condition": (
            "one preregistered normalized parent principle must derive both "
            "the spatial family connection and the oriented spinor lift"
        ),
    },
}


def validate(result: dict) -> None:
    assert result["established"]["projective_RP2_point_charge"] == 1
    assert result["established"]["spinor_lift_first_Chern_number"] == 1
    assert result["established"]["conditional_internal_readout_rank_chain"] == [
        300,
        45,
        15,
        2,
        1,
    ]
    assert not any(result["not_established"].values())
    assert result["required_joint_extension"]["must_share_one_parent_origin"]
    assert not result["required_joint_extension"]["independent_sector_repairs_allowed"]
    assert result["verdict"]["automatic_next_gate"] is None


def main() -> None:
    validate(RESULT)
    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_defect_transport_part_conclusion_gate_results.json"
    )
    output.write_text(json.dumps(RESULT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(RESULT, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()