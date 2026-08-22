#!/usr/bin/env python3
"""Положительная толщина, локальная упаковка и барьер пересоединения."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT / "s2t/results/s2t_v6_single_thread_framed_winding_embedding_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_excluded_volume_reconnection_barrier_gate_results.json"


def parallel_contact_energy(delta: float) -> float:
    """Double integral for two parallel unit segments with kernel |x-y|^-2."""
    return 2.0 * math.atan(1.0 / delta) / delta - math.log((1.0 + delta**2) / delta**2)


def packing_radius_ratio(count: int) -> float:
    """Hexagonal disk-packing upper bound a/ell for count passages."""
    return math.sqrt(1.0 / (2.0 * math.sqrt(3.0) * count))


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    counts = tuple(int(x) for x in parent["input"]["unsigned_counts"])
    unsigned_total = sum(counts)
    real_total = 2 * unsigned_total

    deltas = [10.0 ** (-k) for k in range(1, 7)]
    contact = [parallel_contact_energy(delta) for delta in deltas]
    scaled = [delta * value for delta, value in zip(deltas, contact)]

    max_count = max(counts)
    result = {
        "gate": "version6_single_thread_excluded_volume_reconnection_barrier_gate",
        "input": {
            "unsigned_counts": counts,
            "unsigned_total_passes": unsigned_total,
            "Real_doubled_oriented_visits": real_total,
        },
        "positive_thickness_geometry": {
            "tube_condition": "radius a must not exceed curve reach",
            "reach_components": [
                "local curvature radius",
                "half the nonlocal self-distance",
            ],
            "current_parent_supplies_fundamental_radius": False,
            "existing_effective_vortex_width_is_fundamental_radius": False,
            "strict_continuum_dense_filling_with_uniform_positive_reach_certified": False,
            "finite_cutoff_weave_remains_possible": True,
        },
        "conditional_cross_section_packing": {
            "assumption": "all counted visits cross one coarse square cell simultaneously as disjoint circular tubes",
            "hexagonal_packing_fraction": math.pi / (2.0 * math.sqrt(3.0)),
            "largest_axis_count": max_count,
            "largest_axis_radius_to_cell_ratio_upper_bound": packing_radius_ratio(max_count),
            "all_unsigned_passes_radius_to_cell_ratio_upper_bound": packing_radius_ratio(unsigned_total),
            "all_Real_visits_radius_to_cell_ratio_upper_bound": packing_radius_ratio(real_total),
            "equal_thread_and_cell_scale_compatible": False,
            "counts_are_physical_planck_pass_numbers": False,
            "interpretation": "the integer counts are moment approximants; without a derived scale map they cannot be used as literal Planck packing data",
        },
        "local_action_collision_test": {
            "geometry": "two straight parallel unit segments separated by delta",
            "deltas": deltas,
            "Nambu_Goto_length_energy": [2.0 for _ in deltas],
            "local_bending_energy": [0.0 for _ in deltas],
            "inverse_square_contact_energy": contact,
            "delta_times_contact_energy": scaled,
            "limiting_delta_times_contact_energy": math.pi,
            "local_tension_or_curvature_diverges_at_contact": False,
            "nonlocal_contact_kernel_diverges_at_contact": True,
        },
        "project_operator_audit": {
            "known_thread_terms": [
                "local tension / Nambu-Goto term",
                "local derivative and curvature terms",
                "internal rank-loss barriers",
                "topological winding and Hopf labels",
            ],
            "pairwise_nonlocal_self_distance_operator_found": False,
            "hard_core_positive_reach_constraint_found": False,
            "coefficient_free_OHara_or_tangent_point_energy_found": False,
            "topological_charge_alone_forbids_reconnection": False,
            "reason": "reconnection may pass through a finite core where the order parameter leaves the vacuum manifold",
        },
        "verdict": {
            "literal_planck_thickness_planck_cell_multi_pass_packing_derived": False,
            "finite_cutoff_single_cycle_embedding_refuted": False,
            "excluded_volume_derived_from_current_parent": False,
            "infinite_reconnection_barrier_derived": False,
            "literal_unbreakable_single_thread_derived": False,
            "effective_multi_pass_order_parameter_picture_survives": True,
            "stable_Hopf_soliton_route_survives": True,
            "single_thread_hypothesis_requires_new_microscopic_axiom_or_scale_hierarchy": True,
            "next_gate": "version6_single_thread_scale_hierarchy_branch_decision_gate",
        },
    }

    assert unsigned_total == 25185499
    assert real_total == 50370998
    assert result["conditional_cross_section_packing"]["largest_axis_radius_to_cell_ratio_upper_bound"] < 1.2e-4
    assert abs(scaled[-1] - math.pi) < 5.0e-5
    assert contact[-1] > 1.0e6
    assert not result["verdict"]["excluded_volume_derived_from_current_parent"]
    assert not result["verdict"]["literal_unbreakable_single_thread_derived"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()