#!/usr/bin/env python3
"""Audit common intensive normalizations of the matter-birth free energy."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    carrier_rank = 300
    positive_classical = Fraction(33, 14)
    bridge_curvature = Fraction(-45, 16)
    ordinary_pfaffian_curvature = Fraction(135, 2)
    pfaffian_multiplicity = 15
    one_family_copy_curvature = Fraction(9, 2)

    ordinary_total = (
        positive_classical + bridge_curvature + ordinary_pfaffian_curvature
    )
    global_intensive_total = ordinary_total / carrier_rank
    hybrid_fermion_only = (
        positive_classical
        + bridge_curvature
        + ordinary_pfaffian_curvature / carrier_rank
    )
    common_large_rank = (
        positive_classical
        + bridge_curvature / carrier_rank
        + ordinary_pfaffian_curvature / carrier_rank
    )

    bridge_copy_threshold_exact = (
        carrier_rank
        * (positive_classical + ordinary_pfaffian_curvature / carrier_rank)
        / (-bridge_curvature)
    )
    minimum_bridge_copies = bridge_copy_threshold_exact.numerator // bridge_copy_threshold_exact.denominator + 1

    copy_scan = []
    for copies in [1, 6, 15, 30, 270, 275, 276, 300]:
        curvature = (
            positive_classical
            + Fraction(copies, carrier_rank) * bridge_curvature
            + ordinary_pfaffian_curvature / carrier_rank
        )
        copy_scan.append(
            {
                "independent_bridge_copies": copies,
                "curvature_exact": str(curvature),
                "curvature": float(curvature),
                "unstable": curvature < 0,
            }
        )

    result = {
        "gate": "version6_common_intensive_free_energy_normalization_gate",
        "inputs": {
            "carrier_rank": carrier_rank,
            "positive_entropy_plus_classical_curvature": str(positive_classical),
            "one_collective_bridge_loop_curvature": str(bridge_curvature),
            "ordinary_family_pfaffian_curvature": str(ordinary_pfaffian_curvature),
            "family_pfaffian_multiplicity": pfaffian_multiplicity,
            "one_logdet_copy_curvature": str(one_family_copy_curvature),
        },
        "normalization_cases": {
            "ordinary_path_integral": {
                "curvature_exact": str(ordinary_total),
                "curvature": float(ordinary_total),
                "unstable": ordinary_total < 0,
            },
            "global_division_of_entire_effective_action_by_300": {
                "curvature_exact": str(global_intensive_total),
                "curvature": float(global_intensive_total),
                "unstable": global_intensive_total < 0,
                "sign_same_as_ordinary": (global_intensive_total < 0)
                == (ordinary_total < 0),
            },
            "hybrid_divide_only_fermion_logpf_by_300": {
                "curvature_exact": str(hybrid_fermion_only),
                "curvature": float(hybrid_fermion_only),
                "unstable": hybrid_fermion_only < 0,
                "measure_status": "forbidden_sector_selective_normalization",
            },
            "common_large_rank_free_energy_density": {
                "curvature_exact": str(common_large_rank),
                "curvature": float(common_large_rank),
                "unstable": common_large_rank < 0,
                "collective_bridge_loops_scaled_by": "1/300",
                "family_pfaffian_scaled_by": "15/300",
            },
        },
        "bridge_multiplicity_test": {
            "threshold_exact": str(bridge_copy_threshold_exact),
            "minimum_integer_copies_for_instability": minimum_bridge_copies,
            "project_independent_collective_bridge_fields": 1,
            "scan": copy_scan,
        },
        "verdict": {
            "common_global_scaling_rescues_instability": False,
            "common_large_rank_intensive_limit_rescues_instability": False,
            "hybrid_fractional_pfaffian_would_rescue_but_is_common_measure": False,
            "required_bridge_replication_present": False,
            "determinant_barrier_branch_closed": True,
            "next_gate": "version6_nongaussian_spatial_stiffness_saturation_gate",
        },
    }

    assert positive_classical + bridge_curvature == Fraction(-51, 112)
    assert ordinary_total == Fraction(7509, 112)
    assert global_intensive_total == Fraction(2503, 11200)
    assert hybrid_fermion_only == Fraction(-129, 560)
    assert common_large_rank == Fraction(5763, 2240)
    assert bridge_copy_threshold_exact == Fraction(1928, 7)
    assert minimum_bridge_copies == 276
    assert ordinary_total > 0
    assert global_intensive_total > 0
    assert hybrid_fermion_only < 0
    assert common_large_rank > 0
    assert copy_scan[-2]["independent_bridge_copies"] == 276
    assert copy_scan[-2]["unstable"]

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_common_intensive_free_energy_normalization_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()