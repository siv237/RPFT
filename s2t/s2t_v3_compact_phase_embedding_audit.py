#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp


def main():
    phase_metric, potential_scale = sp.symbols(
        "phase_metric potential_scale", positive=True
    )
    volume_rp3 = sp.pi**2
    length_s1 = 2 * sp.pi
    volume_k = sp.simplify(volume_rp3 * length_s1)

    derivative_constant_hessian = sp.Integer(0)
    potential_hessian_rp3 = potential_scale * volume_rp3
    potential_hessian_s1 = potential_scale * length_s1
    stratified_unit_hessian = sp.simplify(volume_rp3 + length_s1)

    results = {
        "date": "2026-08-09",
        "version": "S2T-III",
        "status": "minimal_local_compact_phase_no_go_stratified_pairing_open",
        "compact_coordinate": {
            "period": "2*pi",
            "continuous_rescaling_is_group_automorphism": False,
            "allowed_primitive_coordinate_changes": [1, -1],
            "charge_lattice_fixes_vertex_powers": True,
            "embedding_scale_kinematically_fixed": True,
        },
        "minimal_local_action": {
            "derivative_constant_mode_hessian": str(derivative_constant_hessian),
            "group_metric_coefficient": str(phase_metric),
            "group_metric_coefficient_fixed_by_period": False,
            "potential_scale": str(potential_scale),
            "potential_scale_fixed_by_compactness": False,
            "potential_hessian_RP3": str(potential_hessian_rp3),
            "potential_hessian_S1": str(potential_hessian_s1),
        },
        "locality_test": {
            "volume_K": str(volume_k),
            "target_factor_sum": str(stratified_unit_hessian),
            "single_local_constant_field_gives_factor_sum": False,
            "stratified_direct_sum_gives_factor_sum": True,
            "stratified_origin_from_parent_action": False,
        },
        "verdict": {
            "minimal_local_compact_phase_passed": False,
            "kinematic_embedding_gap_closed": True,
            "dynamic_hessian_gap_closed": False,
            "next_gate": "derive a common boundary/defect symplectic pairing",
        },
    }

    assert derivative_constant_hessian == 0
    assert volume_k == 2 * sp.pi**3
    assert sp.simplify(stratified_unit_hessian - (sp.pi**2 + 2 * sp.pi)) == 0
    assert not results["verdict"]["minimal_local_compact_phase_passed"]

    Path("s2t_v3_compact_phase_embedding_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()