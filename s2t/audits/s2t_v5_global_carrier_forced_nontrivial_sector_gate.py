#!/usr/bin/env python3
"""Audit whether the global circle carrier forces a nonzero sector."""
from __future__ import annotations

import json
from pathlib import Path


def carrier_record(n: int) -> dict[str, object]:
    if n == 0:
        return {
            "chern_number": 0,
            "fundamental_group": "Z",
            "total_space": "S2 x S1",
        }
    order = abs(n)
    if order == 1:
        total_space = "S3 = L(1,1)"
        fundamental_group = "0"
    elif order == 2:
        total_space = "RP3 = L(2,1)"
        fundamental_group = "Z/2Z"
    else:
        total_space = f"L({order},1)"
        fundamental_group = f"Z/{order}Z"
    return {
        "chern_number": n,
        "fundamental_group": fundamental_group,
        "total_space": total_space,
    }


def main() -> None:
    carriers = [carrier_record(n) for n in range(-4, 5)]
    s3_classes = [
        row["chern_number"] for row in carriers if str(row["total_space"]).startswith("S3")
    ]
    rp3_classes = [
        row["chern_number"] for row in carriers if str(row["total_space"]).startswith("RP3")
    ]

    coefficient_rank = 15
    ambient_rank = 105
    hopf_charges = [coefficient_rank * n for n in s3_classes]

    result = {
        "gate": "version5_global_carrier_forced_nontrivial_sector_gate",
        "circle_bundle_classification": {
            "base": "S2",
            "classification_group": "H2(S2,Z) = Z",
            "boundary_map": "multiplication by n=c1",
            "sample_carriers": carriers,
            "S3_forces_classes": s3_classes,
            "RP3_forces_classes": rp3_classes,
            "trivial_class_total_space": "S2 x S1",
        },
        "coefficient_lift": {
            "coefficient_rank": coefficient_rank,
            "ambient_rank": ambient_rank,
            "S3_oriented_charges": hopf_charges,
            "minimal_positive_defect_weight": coefficient_rank / ambient_rank,
            "zero_class_charge": 0,
            "RP3_oriented_charges": [-2 * coefficient_rank, 2 * coefficient_rank],
        },
        "morita_audit": {
            "degree_E": 1,
            "degree_E_star": -1,
            "selects_L_versus_dual_after_L_is_fixed": True,
            "trivial_line_respects_composition": True,
            "selects_chern_magnitude": False,
        },
        "project_cross_audit": {
            "spin3_carrier_present_in_background": True,
            "rp3_vector_quotient_present_in_background": True,
            "projective_defect_target": "RP2",
            "oriented_defect_lift_to_S2_derived": False,
            "defect_S2_identified_with_Spin3_over_Spin2": False,
            "physical_phase_bundle_identified_with_spin_frame_bundle": False,
            "spatial_SO3_derived_from_M35_trace": False,
        },
        "verdict": {
            "topological_theorem": "PASS",
            "S3_carrier_excludes_zero_sector": True,
            "current_parent_proves_S3_is_physical_defect_carrier": False,
            "current_version_excludes_zero_sector": False,
            "conditional_sector_if_bridge_passes": [-15, 15],
            "next_gate": "version5_spin_cover_defect_sphere_bridge_gate",
        },
    }

    assert s3_classes == [-1, 1]
    assert rp3_classes == [-2, 2]
    assert carrier_record(0)["fundamental_group"] == "Z"
    assert carrier_record(1)["fundamental_group"] == "0"
    assert hopf_charges == [-15, 15]
    assert coefficient_rank / ambient_rank == 1 / 7
    assert result["morita_audit"]["trivial_line_respects_composition"]
    assert not result["morita_audit"]["selects_chern_magnitude"]
    assert not result["verdict"]["current_version_excludes_zero_sector"]

    out = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "s2t_v5_global_carrier_forced_nontrivial_sector_gate_results.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()