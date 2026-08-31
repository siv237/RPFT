#!/usr/bin/env python3
"""Exact admission audit for the minimal isotypic channel extension."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate_results.json"


def strict_edge(a: tuple[str, str, str], b: tuple[str, str, str]) -> bool:
    left_a, right_a, grade_a = a
    left_b, right_b, grade_b = b
    return grade_a != grade_b and (left_a == left_b or right_a == right_b)


def edge_name(a: str, b: str) -> str:
    return "--".join(sorted((a, b)))


def edge_set(vertices: dict[str, tuple[str, str, str]]) -> set[str]:
    return {
        edge_name(a, b)
        for a, b in itertools.combinations(vertices, 2)
        if strict_edge(vertices[a], vertices[b])
    }


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coherence_channel_triplet_promotion_bimodule_compatibility_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate"

    old_vertices = {
        "Q_L": ("H", "M3", "L"),
        "L_L": ("H", "C", "L"),
        "u_R": ("C", "M3", "R"),
        "d_R": ("C", "M3", "R"),
        "e_R": ("C", "C", "R"),
        "X_L": ("C", "C", "L"),
        "X_R": ("C", "C", "R"),
        "Y_L": ("H", "C", "L"),
        "Y_R": ("H", "C", "R"),
    }
    old_edges = edge_set(old_vertices)
    assert len(old_edges) == 14

    single_vertices = old_vertices | {"Z_R": ("C", "C", "R")}
    single_edges = edge_set(single_vertices)
    single_new_edges = single_edges - old_edges
    assert single_new_edges == {
        edge_name("L_L", "Z_R"),
        edge_name("X_L", "Z_R"),
        edge_name("Y_L", "Z_R"),
    }
    desired_coherence_edges = {edge_name("L_L", "Z_R"), edge_name("Y_L", "Z_R")}
    assert len(single_new_edges - desired_coherence_edges) == 1

    # Same gauge representation as e_R,X_R fixes the canonical hypercharge q=-1.
    q = sp.Integer(-1)
    single_anomalies = {
        "A221": sp.Integer(0),
        "Agravity1": -q,
        "A111": -(q**3),
    }
    assert single_anomalies == {"A221": 0, "Agravity1": 1, "A111": 1}
    old_charged_singlet_index = sp.Integer(1) - sp.Integer(2)
    single_charged_singlet_index = sp.Integer(1) - sp.Integer(3)
    assert (old_charged_singlet_index, single_charged_singlet_index) == (-1, -2)

    # The physical vectorlike repair needs an independent left Weyl endpoint.
    pair_vertices = single_vertices | {"Z_L": ("C", "C", "L")}
    pair_edges = edge_set(pair_vertices)
    pair_new_edges = pair_edges - old_edges
    assert len(pair_edges) == 23
    assert len(pair_new_edges) == 9
    selected_pair_edges = desired_coherence_edges | {edge_name("Z_L", "Z_R")}
    unselected_pair_edges = pair_new_edges - selected_pair_edges
    assert len(selected_pair_edges) == 3
    assert len(unselected_pair_edges) == 6

    pair_anomalies = {
        "A221": sp.Integer(0),
        "Agravity1": q - q,
        "A111": q**3 - q**3,
    }
    assert pair_anomalies == {"A221": 0, "Agravity1": 0, "A111": 0}
    pair_charged_singlet_index = sp.Integer(2) - sp.Integer(3)
    assert pair_charged_singlet_index == old_charged_singlet_index

    # One generation: two left singlets versus a right isotypic triplet.
    mass_a = sp.Matrix([[1, 0, 1], [0, 1, 1]])
    mass_b = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    assert mass_a.rank() == mass_b.rank() == 2
    kernel_a = mass_a.nullspace()[0]
    kernel_b = mass_b.nullspace()[0]
    assert kernel_a != kernel_b
    assert len(kernel_a) == len(kernel_b) == 3

    # If the two left singlets carry the current trivial channel action, an
    # SO(3)-covariant 2x3 mass must vanish.
    l12 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    l13 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    l23 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
    variables = sp.symbols("m0:6")
    mass = sp.Matrix(2, 3, variables)
    equations = []
    for generator in (l12, l13, l23):
        equations.extend(list(mass * generator))
    covariance_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    assert covariance_matrix.rank() == 6
    assert len(variables) - covariance_matrix.rank() == 0

    selected_chain_dimensions = {"H0": 1, "H1": 2 * 3, "H2": 1 * 3}
    assert selected_chain_dimensions == {"H0": 1, "H1": 6, "H2": 3}

    exact_objects = [q, *single_anomalies.values(), *pair_anomalies.values(), mass_a, mass_b, kernel_a, kernel_b, mass, covariance_matrix, l12, l13, l23]
    assert not any(obj.atoms(sp.Float) if hasattr(obj, "atoms") else False for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate",
        "single_endpoint_candidate": {
            "new_endpoint": "Z_R=(C,C,R), Y=-1",
            "formal_Real_image": "JZ_R=(C,C,L) in the antiparticle sector",
            "physical_left_partner_present": False,
            "new_strict_edges": sorted(single_new_edges),
            "desired_coherence_edges": sorted(desired_coherence_edges),
            "unwanted_new_edges": sorted(single_new_edges - desired_coherence_edges),
            "local_anomalies": {key: int(value) for key, value in single_anomalies.items()},
            "Witten_doublet_parity_change": 0,
            "charged_singlet_chiral_index_before": int(old_charged_singlet_index),
            "charged_singlet_chiral_index_after": int(single_charged_singlet_index),
            "physically_admitted": False,
        },
        "minimal_vectorlike_completion": {
            "additional_endpoint": "Z_L=(C,C,L), Y=-1",
            "new_physical_vertices_total": 2,
            "local_anomalies": {key: int(value) for key, value in pair_anomalies.items()},
            "Witten_doublet_parity_change": 0,
            "charged_singlet_chiral_index": int(pair_charged_singlet_index),
            "old_chiral_index_preserved": True,
            "strict_edges_total": len(pair_edges),
            "new_strict_edges": sorted(pair_new_edges),
            "selected_new_edges": sorted(selected_pair_edges),
            "allowed_but_unselected_edges": sorted(unselected_pair_edges),
            "new_allowed_3x3_complex_matrices": len(pair_new_edges),
            "raw_real_parameters_before_quotients": 18 * len(pair_new_edges),
            "selected_coherence_chain_dimensions": selected_chain_dimensions,
        },
        "mass_and_selector_obstruction": {
            "one_generation_mass_shape": [2, 3],
            "generic_mass_rank": 2,
            "right_kernel_dimension": 1,
            "two_allowed_masses_choose_same_kernel": False,
            "kernel_examples": [list(map(int, kernel_a)), list(map(int, kernel_b))],
            "SO3_covariant_mass_system_rank": covariance_matrix.rank(),
            "SO3_covariant_mass_nullity": 0,
            "nonzero_vectorlike_mass_preserves_full_channel_SO3": False,
            "old_rank_one_condensate_inherited": False,
        },
        "ledgers": {
            "single_endpoint_admission_satisfied": 4,
            "single_endpoint_admission_tested": 7,
            "vectorlike_structural_shape_satisfied": 6,
            "vectorlike_structural_shape_tested": 6,
            "selector_and_origin_satisfied": 0,
            "selector_and_origin_tested": 6,
            "new_parent_inputs": [
                "Z_R endpoint",
                "physical Z_L partner",
                "three-of-nine edge selector",
                "mass tensor or dynamical SO(3)-breaking field",
                "new rank-one condensate on (e,X,Z)",
                "diagonal family-channel lock",
            ],
        },
        "verdict": {
            "one_endpoint_extension_physically_admitted": False,
            "formal_Real_completion_cancels_physical_anomaly": False,
            "minimal_anomaly_safe_completion_is_vectorlike_pair": True,
            "vectorlike_pair_structurally_admitted": True,
            "canonical_edge_and_mass_selector_obtained": False,
            "portal_parent_origin_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()