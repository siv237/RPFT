#!/usr/bin/env python3
"""Развилка H15/H16 и разделение степеней нейтринного сектора."""

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_h15_neutrino_degree_split_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


observed = load_result("s2t_v5_sm_linking_corner_gate_results.json")
morita = load_result("s2t_v5_morita_linking_parent_gate_results.json")
yukawa = load_result("s2t_v4_higgs_yukawa_gate_results.json")
majorana = load_result("s2t_majorana_defect_parent_action_gate_results.json")

assert observed["exact_observed_reading"]["particle_dimension"] == 15
assert morita["morita_carrier"]["complex_dimension_E"] == 300
assert yukawa["allowed_vertex_count"] == 4
assert yukawa["weinberg_operator_dimension"] == 5

family_dimension = 20
h15_blocks = {"Q_L": 6, "L_L": 2, "u_R": 3, "d_R": 3, "e_R": 1}
h16_blocks = {**h15_blocks, "nu_R": 1}

allowed_vertices = yukawa["allowed_renormalizable_yukawa_vertices"]
h15_vertices = [vertex for vertex in allowed_vertices if "nu_R" not in vertex]
h16_vertices = list(allowed_vertices)


def architecture(observed_dimension, blocks, vertices):
    total = family_dimension + observed_dimension
    return {
        "observed_dimension": observed_dimension,
        "observed_blocks": blocks,
        "transition_carrier": f"M20x{observed_dimension}(C)",
        "transition_dimension": family_dimension * observed_dimension,
        "linking_algebra": f"M{total}(C)",
        "linking_representation_dimension": total,
        "linking_vector_space_dimension": total**2,
        "family_corner_weight": str(Fraction(family_dimension, total)),
        "observed_corner_weight": str(Fraction(observed_dimension, total)),
        "renormalizable_dirac_edges": vertices,
        "renormalizable_dirac_edge_count": len(vertices),
    }


h15 = architecture(15, h15_blocks, h15_vertices)
h16 = architecture(16, h16_blocks, h16_vertices)

assert sum(h15_blocks.values()) == 15
assert sum(h16_blocks.values()) == 16
assert h15["transition_dimension"] == 300
assert h16["transition_dimension"] == 320
assert h15["linking_algebra"] == "M35(C)"
assert h16["linking_algebra"] == "M36(C)"
assert h15["family_corner_weight"] == "4/7"
assert h15["observed_corner_weight"] == "3/7"
assert h16["family_corner_weight"] == "5/9"
assert h16["observed_corner_weight"] == "4/9"
assert len(h15_vertices) == 3
assert len(h16_vertices) == 4

result = {
    "gate": "version5_h15_neutrino_degree_split_gate",
    "input_certificates": {
        "exact_H15_observed_reading": "pass",
        "M20x15_Morita_parent": "pass",
        "four_edge_H16_Yukawa_menu": "pass",
        "conditional_Majorana_defect_model": "pass_as_conditional_not_derived",
    },
    "architecture_comparison": {"H15": h15, "H16": h16},
    "nontrivial_change_under_H16": {
        "carrier_dimension_change": 20,
        "linking_algebra_change": "M35(C) -> M36(C)",
        "corner_weights_change": "(4/7,3/7) -> (5/9,4/9)",
        "is_harmless_extension_of_current_parent": False,
    },
    "degree_split": {
        "degree_one_renormalizable_sector_on_H15": ["u", "d", "e"],
        "neutrino_dirac_edge_on_H15": False,
        "lowest_gauge_invariant_neutrino_mass_operator_without_nu_R": "Weinberg operator",
        "operator_mass_dimension": 5,
        "project_native_alternative": "Majorana/defect operator of higher differential degree",
        "project_native_alternative_dynamically_derived": False,
    },
    "selection_rule": {
        "rule": "preserve already derived carrier and one-trace architecture unless an enlargement is independently forced",
        "selected_for_next_gate": "H15 charged one-form sector",
        "neutrino_status": "separate higher-degree sector; open, not discarded and not claimed derived",
        "H16_status": "admissible future replacement only with a rebuilt M36 parent and repeated normalization gates",
    },
    "verdict": {
        "H15_matches_current_M35_parent": True,
        "H15_contains_exactly_three_charged_Yukawa_edges": True,
        "H15_contains_Dirac_neutrino_edge": False,
        "H16_preserves_current_trace_weights": False,
        "neutrino_higher_degree_dynamics_closed": False,
        "physical_closure": False,
        "status": "freeze H15 for the next one-form gate and keep neutrino mass in a separate unclosed higher-degree sector",
    },
    "next_gate": (
        "Construct the H15 physical one-form bimodule for the three charged edges "
        "u,d,e, test projectivity, differential compatibility, KO6 and whether the "
        "rank-one Grassmann connection selects a unique orbit before any potential."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))