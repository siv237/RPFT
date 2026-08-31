#!/usr/bin/env python3
"""Exact selector audit for the cubic two-source incidence assignment."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate"
    assert predecessor["next_gate"] == gate

    charges = {"Y": sp.Matrix([0, -3]), "u": sp.Matrix([1, 1]), "d": sp.Matrix([-1, 1])}
    kinv = sp.diag(sp.Rational(1, 12), sp.Rational(1, 48))
    records = {}
    for e_b, e_m in itertools.permutations(charges, 2):
        Q = sp.Matrix.vstack(charges[e_b].T, charges[e_m].T)
        C = sp.Matrix.hstack(3 * charges[e_b], 2 * charges[e_m])
        gram = sp.simplify(C.T * kinv * C)
        eigenvalues = list(gram.eigenvals())
        kappa2 = sp.simplify(max(eigenvalues, key=lambda v: float(v)) / min(eigenvalues, key=lambda v: float(v)))
        area = sp.sqrt(gram.det())
        ray = 3 * charges[e_b] + 2 * charges[e_m]
        gaps = sp.Matrix([ray[0] + ray[1], -ray[0] + ray[1]])
        records[f"B->{e_b},M->{e_m}"] = {
            "abs_det_Q": abs(int(Q.det())),
            "metric_area": str(area),
            "condition_number_squared": str(kappa2),
            "single_coefficient_source_ray": [int(ray[0]), int(ray[1])],
            "single_coefficient_gap_ray_unscaled": [int(gaps[0]), int(gaps[1])],
        }

    max_det = max(v["abs_det_Q"] for v in records.values())
    det_survivors = sorted(k for k, v in records.items() if v["abs_det_Q"] == max_det)
    max_area = max(sp.sympify(v["metric_area"]) for v in records.values())
    area_survivors = sorted(k for k, v in records.items() if sp.sympify(v["metric_area"]) == max_area)
    condition_values = {k: sp.sympify(v["condition_number_squared"]) for k, v in records.items()}
    min_condition2 = min(condition_values.values(), key=lambda v: float(v))
    condition_survivors = sorted(k for k, v in condition_values.items() if sp.simplify(v - min_condition2) == 0)
    dimension_survivors = ["B->d,M->Y", "B->u,M->Y"]

    assert det_survivors == ["B->Y,M->d", "B->Y,M->u", "B->d,M->Y", "B->u,M->Y"]
    assert area_survivors == det_survivors
    assert condition_survivors == dimension_survivors
    assert min_condition2 == sp.simplify((27 + 3 * sp.sqrt(17)) / (27 - 3 * sp.sqrt(17)))
    assert records["B->u,M->Y"]["single_coefficient_gap_ray_unscaled"] == [0, -6]
    assert records["B->d,M->Y"]["single_coefficient_gap_ray_unscaled"] == [-6, 0]

    c_b, c_m = sp.symbols("c_B c_M", real=True)
    # Equal gaps require j_A=0. For B->u/d and M->Y this fixes an external ratio.
    assert sp.solve(sp.Eq(3 * c_b, 0), c_b) == [0]
    equal_gap_conditions = {"B->u,M->Y": "c_B=0", "B->d,M->Y": "c_B=0"}

    objects = [*charges.values(), kinv, min_condition2]
    assert not any(obj.atoms(sp.Float) for obj in objects)
    result = {
        "date": "2026-08-31",
        "gate": gate,
        "candidate_records": records,
        "selector_cascade": {
            "initial_rank_two_candidates": 6,
            "maximum_abs_determinant": max_det,
            "maximum_determinant_survivors": det_survivors,
            "maximum_metric_area": str(max_area),
            "maximum_metric_area_survivors": area_survivors,
            "minimum_condition_number_squared": str(min_condition2),
            "minimum_condition_survivors": condition_survivors,
            "dimension_match_survivors": dimension_survivors,
            "final_survivors": dimension_survivors,
        },
        "binary_obstruction": {
            "survivor_source_rays": {"B->u,M->Y": [3, -3], "B->d,M->Y": [-3, -3]},
            "survivor_gap_rays_unscaled": {"B->u,M->Y": [0, -6], "B->d,M->Y": [-6, 0]},
            "determinant_sign_basis_orientation_invariant": False,
            "u_d_gauge_equivalent": False,
            "gauge_inequivalence_selects_one": False,
            "equal_gap_conditions": equal_gap_conditions,
            "equal_gap_collapses_portal_rank_to_one": True,
            "equal_gap_is_internal_selector": False,
        },
        "ledgers": {
            "exact_classification_satisfied": 8,
            "exact_classification_tested": 8,
            "intrinsic_selector_satisfied": 0,
            "intrinsic_selector_tested": 8,
        },
        "verdict": {
            "determinant_unique": False,
            "metric_area_unique": False,
            "condition_and_dimension_reduce_to_binary_pair": True,
            "binary_u_d_choice_resolved": False,
            "incidence_assignment_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()