#!/usr/bin/env python3
"""Audit whether the current parent forces an equivariant nonzero sector."""
from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> None:
    projector = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    projector_squared = [
        [sum(projector[i][k] * projector[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]
    assert projector_squared == projector

    # A homomorphism from Z2 to the torsion-free group Z must vanish.
    possible_restrictions = [n for n in range(-8, 9) if 2 * n == 0]
    assert possible_restrictions == [0]

    zero_winding = 0
    matter_winding = 15
    ambient_rank = 105
    loop_action_zero = zero_winding / ambient_rank
    loop_action_matter = matter_winding / ambient_rank

    mass_squared = 2.0
    defect_scale = 1.0
    vacuum_response = (1 / 7) * math.log((mass_squared + defect_scale) / mass_squared)

    liftable_closed_sample_charges = [1, -1]
    assert sum(liftable_closed_sample_charges) == 0

    result = {
        "gate": "version5_equivariant_boundary_sector_selection_gate",
        "explicit_zero_sector": {
            "constant_projector": projector,
            "idempotent": projector_squared == projector,
            "spatial_derivative": 0,
            "projective_charge": 0,
            "induced_Hopf_Chern_number": 0,
            "admissible_in_current_product_finite_geometry": True,
        },
        "carrier_topology": {
            "historical_carrier": "RP3 x S1",
            "pi2": 0,
            "H2_cohomology": "Z2",
            "free_H2_cohomology_rank": 0,
            "torsion_restriction_candidates_in_H2_S2_equals_Z": possible_restrictions,
            "torsion_can_force_local_Chern_one": False,
            "late_S4_H2_cohomology": 0,
        },
        "closed_space_charge_audit": {
            "scope": "globally liftable branch without disclination lines",
            "oriented_boundary_relation": "sum_i [S2_i] = 0",
            "sample_point_charges": liftable_closed_sample_charges,
            "total_charge": sum(liftable_closed_sample_charges),
            "single_uncompensated_plus_one_forced": False,
        },
        "functional_cross_audit": {
            "identity_loop_winding": zero_winding,
            "identity_loop_action": loop_action_zero,
            "matter_loop_winding": matter_winding,
            "matter_sector_minimum_action": loop_action_matter,
            "global_action_prefers_zero_if_all_sectors_are_allowed": True,
            "sample_positive_defect_response": vacuum_response,
            "defect_response_destabilizes_zero": False,
        },
        "project_background": {
            "zero_prompt_carrier_inevitability_passed": False,
            "carrier_measure_derived": False,
            "self_generated_defect_boundary_sector_was_input": True,
            "spin_cover_bridge_for_selected_hedgehog_passed": True,
            "topological_closure_deficit_inside_sector_passed": True,
            "zero_sector_negative_Hessian_mode_derived": False,
            "global_anomaly_excluding_zero_derived": False,
        },
        "verdict": {
            "equivariant_boundary_condition_forced": False,
            "nonzero_sector_selected_by_current_topology": False,
            "nonzero_sector_selected_by_current_functionals": False,
            "matter_inevitability_proved": False,
            "topological_branch_status": "STOP until a zero-sector instability or anomaly is derived",
            "next_gate": "version5_zero_sector_instability_parent_gate",
        },
    }

    assert result["explicit_zero_sector"]["admissible_in_current_product_finite_geometry"]
    assert not result["carrier_topology"]["torsion_can_force_local_Chern_one"]
    assert loop_action_zero == 0
    assert loop_action_matter == 1 / 7
    assert vacuum_response > 0
    assert not result["verdict"]["matter_inevitability_proved"]

    out = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "s2t_v5_equivariant_boundary_sector_selection_gate_results.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()