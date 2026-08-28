#!/usr/bin/env python3
"""Audit the Real, anomaly and mass admission of the minimal mirror pair."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_minimal_mirror_pair_real_anomaly_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def strict_edge(a: tuple[str, str, str], b: tuple[str, str, str]) -> bool:
    i, j, grade = a
    k, ell, other_grade = b
    return grade != other_grade and (i == k or j == ell)


def real_image(vertex: tuple[str, str, str]) -> tuple[str, str, str]:
    left, right, grade = vertex
    return right, left, "R" if grade == "L" else "L"


def anomaly_coefficients(fields: list[dict]) -> dict[str, Fraction | int]:
    """Use the Tome-IV convention: right-handed fields enter with minus sign."""
    a221 = Fraction(0)
    agrav = Fraction(0)
    a111 = Fraction(0)
    weak_doublets = 0
    for field in fields:
        sign = 1 if field["chirality"] == "L" else -1
        color = field["color_dimension"]
        weak = field["weak_dimension"]
        hypercharge = field["hypercharge"]
        if weak == 2:
            a221 += sign * color * hypercharge
            weak_doublets += color
        agrav += sign * color * weak * hypercharge
        a111 += sign * color * weak * hypercharge**3
    return {
        "A_221": a221,
        "A_grav_grav_1": agrav,
        "A_111": a111,
        "weak_doublet_count_mod_2": weak_doublets % 2,
    }


def fractions_to_strings(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: fractions_to_strings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [fractions_to_strings(item) for item in value]
    return value


def main() -> None:
    branch = load_result("s2t_v7_r2_minimal_architecture_branch_gate_results.json")
    a2_gate = load_result("s2t_v7_r2_generalized_fluctuation_seed_origin_gate_results.json")
    assert a2_gate["verdict"]["zero_new_vertex_generalized_route_as_derivation"] == "closed_circular"

    minimum = branch["strict_first_order_mirror_vertex_branch"]["dimension_minimal_solution"]
    assert minimum["new_vertex_types"] == [["C", "C", "L"], ["H", "C", "R"]]

    vertices = {
        "Q_L": ("H", "M3", "L"),
        "L_L": ("H", "C", "L"),
        "u_R": ("C", "M3", "R"),
        "e_R": ("C", "C", "R"),
        "X_L": ("C", "C", "L"),
        "Y_R": ("H", "C", "R"),
    }
    cycle = ["Q_L", "u_R", "X_L", "e_R", "L_L", "Y_R", "Q_L"]
    edge_checks = [strict_edge(vertices[a], vertices[b]) for a, b in zip(cycle, cycle[1:])]
    assert all(edge_checks)

    real_orbit = {
        name: list(real_image(vertices[name]))
        for name in ("X_L", "Y_R")
    }

    canonical_mirror_fields = [
        {
            "name": "X_L",
            "chirality": "L",
            "color_dimension": 1,
            "weak_dimension": 1,
            "hypercharge": Fraction(-1),
        },
        {
            "name": "Y_R",
            "chirality": "R",
            "color_dimension": 1,
            "weak_dimension": 2,
            "hypercharge": Fraction(-1, 2),
        },
    ]
    canonical_anomalies = anomaly_coefficients(canonical_mirror_fields)
    assert canonical_anomalies == {
        "A_221": Fraction(1, 2),
        "A_grav_grav_1": Fraction(0),
        "A_111": Fraction(-3, 4),
        "weak_doublet_count_mod_2": 1,
    }

    # For arbitrary hypercharges x=Y(X_L), y=Y(Y_R), local cancellation gives
    # -y=0 and x-2y=0, hence x=y=0.  The single weak doublet nevertheless
    # leaves the mod-two Witten obstruction.
    general_charge_solution = {"Y_X_L": Fraction(0), "Y_Y_R": Fraction(0)}
    general_solution_local_anomalies = anomaly_coefficients([
        {**canonical_mirror_fields[0], "hypercharge": Fraction(0)},
        {**canonical_mirror_fields[1], "hypercharge": Fraction(0)},
    ])
    assert general_solution_local_anomalies["weak_doublet_count_mod_2"] == 1

    # The coarse bimodule types coincide with the old charged-lepton singlet
    # and lepton doublet, so gauge-invariant opposite-chirality mass blocks are
    # allowed and are generically full rank.
    direct_mass_edges = {
        "X_L-e_R": strict_edge(vertices["X_L"], vertices["e_R"]),
        "L_L-Y_R": strict_edge(vertices["L_L"], vertices["Y_R"]),
    }
    assert all(direct_mass_edges.values())

    # A conservative anomaly-safe repair adds independent opposite chiralities
    # for both new representations.  This is a four-vertex vectorlike sector,
    # not the advertised two-vertex completion.
    vectorlike_repair_fields = canonical_mirror_fields + [
        {
            "name": "X_R",
            "chirality": "R",
            "color_dimension": 1,
            "weak_dimension": 1,
            "hypercharge": Fraction(-1),
        },
        {
            "name": "Y_L",
            "chirality": "L",
            "color_dimension": 1,
            "weak_dimension": 2,
            "hypercharge": Fraction(-1, 2),
        },
    ]
    repair_anomalies = anomaly_coefficients(vectorlike_repair_fields)
    assert repair_anomalies == {
        "A_221": Fraction(0),
        "A_grav_grav_1": Fraction(0),
        "A_111": Fraction(0),
        "weak_doublet_count_mod_2": 0,
    }

    result = {
        "gate": "version7_minimal_mirror_pair_real_anomaly_gate",
        "input": {
            "new_physical_vertices": {"X_L": list(vertices["X_L"]), "Y_R": list(vertices["Y_R"])},
            "cycle": cycle,
            "canonical_mirror_interpretation": {
                "X_L": "charged-lepton singlet with Y=-1",
                "Y_R": "right-handed weak doublet with Y=-1/2",
            },
        },
        "strict_first_order": {
            "cycle_edge_checks": edge_checks,
            "all_cycle_edges_admitted": all(edge_checks),
        },
        "real_completion": {
            "J_images": real_orbit,
            "formal_J_orbit_can_be_added": True,
            "J_doubling_supplies_independent_physical_Weyl_multiplets": False,
            "anomaly_cancellation_follows_from_Real_completion": False,
        },
        "canonical_anomaly_audit": canonical_anomalies,
        "arbitrary_hypercharge_audit": {
            "local_equations": ["-y=0", "x-2y=0", "x^3-2y^3=0"],
            "only_local_solution": general_charge_solution,
            "local_anomalies_at_solution": general_solution_local_anomalies,
            "Witten_mod2_obstruction_remains": True,
        },
        "mass_pairing_audit": {
            "direct_gauge_admissible_blocks": direct_mass_edges,
            "generic_full_rank_blocks_pair_old_SM_leptons": True,
            "light_chiral_H15_preserved_without_rank_condition": False,
        },
        "minimal_conservative_repair": {
            "additional_vertices_beyond_X_L_Y_R": ["X_R", "Y_L"],
            "total_new_chiral_vertices": 4,
            "anomalies": repair_anomalies,
            "anomaly_free": True,
            "derived_from_current_parent": False,
        },
        "verdict": {
            "two_vertex_mirror_cycle_first_order_admitted": True,
            "two_vertex_mirror_cycle_real_formally_completable": True,
            "two_vertex_mirror_cycle_anomaly_free": False,
            "two_vertex_mirror_cycle_preserves_light_H15_generically": False,
            "dimension_minimal_pair_physically_admitted": False,
            "next_gate": "compare a four-vertex vectorlike closure with a complete mirror generation and reject arbitrary Yukawa enlargement",
        },
    }
    OUTPUT.write_text(json.dumps(fractions_to_strings(result), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()