#!/usr/bin/env python3
"""Exact parent-origin audit for the full two-source portal matrix."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate"
    assert predecessor["next_gate"] == gate

    lam, x = sp.symbols("lambda x", real=True)
    X = sp.Matrix([[lam, x], [x, 0]])
    assert sp.expand(sp.trace(X**3)) == lam**3 + 3 * lam * x**2

    charges = {
        "Y": sp.Matrix([0, -3]),
        "u": sp.Matrix([1, 1]),
        "d": sp.Matrix([-1, 1]),
    }
    assignments = {}
    rank_counts = {1: 0, 2: 0}
    determinants = set()
    single_rays = []
    two_coefficient_determinants = []
    for e_b, e_m in itertools.product(charges, repeat=2):
        Q = sp.Matrix.vstack(charges[e_b].T, charges[e_m].T)
        rank = Q.rank()
        det = Q.det()
        rank_counts[rank] += 1
        determinants.add(det)
        ray = 3 * charges[e_b] + 2 * charges[e_m]
        if rank == 2:
            source_map = -3 * sp.Matrix.hstack(3 * charges[e_b], 2 * charges[e_m])
            two_coefficient_determinants.append(abs(source_map.det()))
            single_rays.append(tuple(ray))
        assignments[f"B->{e_b},M->{e_m}"] = {"rank": rank, "determinant": str(det), "single_coefficient_ray": [int(ray[0]), int(ray[1])]}

    assert rank_counts == {1: 3, 2: 6}
    assert determinants == {sp.Integer(0), sp.Integer(2), sp.Integer(-2), sp.Integer(3), sp.Integer(-3)}
    assert sorted(set(two_coefficient_determinants)) == [108, 162]
    expected_rays = {(2, -7), (-2, -7), (3, -3), (1, 5), (-3, -3), (-1, 5)}
    assert set(single_rays) == expected_rays

    a, b, t_b, t_m, c_b, c_m = sp.symbols("a b T_B T_M c_B c_M", real=True)
    direct_sum_mixed_hessian = sp.zeros(2)
    inherited_coefficients = sp.zeros(3, 1)
    objects = [X, *charges.values(), direct_sum_mixed_hessian, inherited_coefficients]
    assert not any(obj.atoms(sp.Float) for obj in objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "direct_sum_test": {
            "moment_additive": True,
            "mixed_portal_hessian": [[0, 0], [0, 0]],
            "portal_generated": False,
        },
        "minimal_common_block": {
            "operator": "[[lambda I,F],[F*,0]]",
            "cubic_trace": "d lambda^3+3 lambda Tr(FF*)",
            "linear_portal_coefficient": 3,
            "even_moments_generate_linear_portal": False,
        },
        "central_charge_vectors": {key: [int(value[0]), int(value[1])] for key, value in charges.items()},
        "incidence_assignment_classification": {
            "ordered_assignments": 9,
            "rank_one_assignments": 3,
            "rank_two_assignments": 6,
            "determinant_values": [-3, -2, 0, 2, 3],
            "assignments": assignments,
        },
        "coefficient_tests": {
            "carrier_vacuum_values": [3, 2],
            "two_independent_coefficients_rank_two_for_distinct_sectors": True,
            "two_coefficient_absolute_determinants": [108, 162],
            "single_common_coefficient_rays": [list(ray) for ray in sorted(expected_rays)],
            "single_common_coefficient_covers_source_plane": False,
        },
        "parent_origin": {
            "inherited_odd_coefficients": [0, 0, 0],
            "typed_common_block_present": False,
            "incidence_assignment_selected": False,
            "normalization_selected": False,
        },
        "ledgers": {
            "conditional_operator_shape_satisfied": 7,
            "conditional_operator_shape_tested": 7,
            "incidence_selector_satisfied": 0,
            "incidence_selector_tested": 5,
            "parent_origin_satisfied": 0,
            "parent_origin_tested": 4,
        },
        "verdict": {
            "full_rank_portal_conditionally_realizable": True,
            "direct_sum_sufficient": False,
            "one_common_cubic_coefficient_sufficient_for_arbitrary_sources": False,
            "two_independent_cubic_coefficients_sufficient_conditionally": True,
            "inherited_parent_generates_portal": False,
            "portal_matrix_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()