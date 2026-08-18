#!/usr/bin/env python3
"""Аудит научного языка, в котором переход является первичным объектом."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_transition_primitive_scientific_language_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


morita = load_result("s2t_v5_morita_linking_parent_gate_results.json")
walk = load_result("s2t_v5_local_defect_transfer_operator_gate_results.json")
loop = load_result("s2t_v5_order_four_resonant_loop_transport_gate_results.json")

assert morita["morita_carrier"]["equivalence_bimodule"] == "E=M20x15(C)"
assert morita["architecture_interpretation"]["physical_carrier_is_the_space_of_transitions"]
assert walk["verdict"]["minimal_transfer_language_validated"]
assert walk["continuum_limit"]["common_light_cone"]
assert loop["early_hypothesis_reconstruction"]["full_return_after_four_steps"] == "1"


def matrix_units(rows, cols):
    units = []
    for i in range(rows):
        for j in range(cols):
            unit = sp.zeros(rows, cols)
            unit[i, j] = 1
            units.append(unit)
    return units


e_units = matrix_units(3, 2)
estar_units = [unit.T for unit in e_units]
left_products = [a * b for a in e_units for b in estar_units]
right_products = [b * a for b in estar_units for a in e_units]
left_vectors = sp.Matrix.hstack(*[sp.Matrix(product).reshape(9, 1) for product in left_products])
right_vectors = sp.Matrix.hstack(*[sp.Matrix(product).reshape(4, 1) for product in right_products])
left_span_rank = left_vectors.rank()
right_span_rank = right_vectors.rank()
assert left_span_rank == 9
assert right_span_rank == 4

U = sp.Matrix(
    [
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
)
assert U**4 == sp.eye(4)

roots = [sp.Integer(1), sp.I, -sp.Integer(1), -sp.I]
projectors = []
for eigenvalue in roots:
    projector = sp.simplify(
        sum(((eigenvalue ** (-n)) * (U**n) for n in range(4)), sp.zeros(4)) / 4
    )
    assert sp.simplify(projector**2 - projector) == sp.zeros(4)
    assert projector.rank() == 1
    assert sp.simplify(U * projector - eigenvalue * projector) == sp.zeros(4)
    projectors.append(projector)

for i, first in enumerate(projectors):
    for j, second in enumerate(projectors):
        if i != j:
            assert sp.simplify(first * second) == sp.zeros(4)
assert sp.simplify(sum(projectors, sp.zeros(4)) - sp.eye(4)) == sp.zeros(4)

edge_phases = [sp.Integer(1), sp.I, sp.Integer(1), sp.Integer(1)]
gauge = [sp.Integer(1), -sp.Integer(1), sp.I, -sp.I]
holonomy = sp.prod(edge_phases)
transformed_edges = [
    sp.simplify(gauge[(j + 1) % 4] * edge_phases[j] / gauge[j])
    for j in range(4)
]
transformed_holonomy = sp.simplify(sp.prod(transformed_edges))
assert holonomy == sp.I
assert transformed_holonomy == holonomy

result = {
    "gate": "version5_transition_primitive_scientific_language_gate",
    "anti_circle_boundary": {
        "closed_earlier_candidate": "category of reductions among whole geometric, spectral and correlation readings",
        "new_candidate": "local typed transition as the physical primitive",
        "requires_inverse_spectral_reconstruction": False,
        "same_as_closed_reduction_triangle": False,
    },
    "project_native_transition_carrier": {
        "left_corner": "M20(C)",
        "right_corner": "M15(C)",
        "transition_correspondence": "E=M20x15(C)",
        "linking_algebra": "[[M20,E],[E*,M15]]=M35(C)",
        "interpretation": "off-diagonal elements are typed transitions; their opposite compositions generate diagonal observables",
    },
    "composition_proxy_audit": {
        "proxy_correspondence": "M3x2(C)",
        "left_product": "E E*=M3(C)",
        "left_span_rank": left_span_rank,
        "left_corner_dimension": 9,
        "right_product": "E* E=M2(C)",
        "right_span_rank": right_span_rank,
        "right_corner_dimension": 4,
        "diagonal_corners_generated_by_transition_composition": True,
    },
    "four_step_character_inheritance": {
        "step_order": 4,
        "eigencharacters": [str(value) for value in roots],
        "projector_ranks": [projector.rank() for projector in projectors],
        "projectors_idempotent": True,
        "projectors_pairwise_orthogonal": True,
        "projectors_resolve_identity": True,
        "interpretation": "observable sectors may inherit characters, signs and orientations of a primitive cycle rather than its literal geometric shape",
    },
    "holonomy_audit": {
        "edge_phases": [str(value) for value in edge_phases],
        "local_gauge_phases": [str(value) for value in gauge],
        "transformed_edge_phases": [str(value) for value in transformed_edges],
        "loop_holonomy": str(holonomy),
        "transformed_loop_holonomy": str(transformed_holonomy),
        "gauge_invariant": True,
        "candidate_defect_identity": "conjugacy class, spectrum or index of closed-path transport",
    },
    "scientific_language_stack": {
        "C_star_correspondences_and_Morita": "type and compose arrows",
        "quivers_and_groupoids": "record sources, targets, paths and holonomy",
        "quantum_walks_and_QCA": "supply local reversible update and continuum tests",
        "holonomy_and_index_theory": "distinguish protected defects from arbitrary profiles",
        "categorical_process_theory": "provides compositional grammar but not a unique dynamics",
        "causal_sets_spin_foams_tensor_networks": "deferred until the existing local carrier passes a nonlinear defect test",
    },
    "existing_project_certificates": {
        "Morita_transition_carrier": True,
        "local_unitary_transfer": walk["verdict"]["local_unitary_transfer_exists"],
        "Dirac_continuum_limit": walk["verdict"]["Dirac_continuum_limit_exists"],
        "common_light_cone": walk["continuum_limit"]["common_light_cone"],
        "order_four_cycle": True,
        "nontrivial_holonomy_tools": True,
        "localized_protected_moving_defect": False,
    },
    "verdict": {
        "scientific_languages_for_transition_ontology_exist": True,
        "all_minimal_language_layers_have_project_representatives": True,
        "states_as_composites_of_transitions_algebraically_supported": True,
        "inheritance_of_similarity_formalized_as_representation_character": True,
        "unique_fundamental_update_rule_derived": False,
        "standard_model_particle_spectrum_derived": False,
        "physical_closure": False,
        "status": "The transition ontology can be expressed without metaphor by combining Morita correspondences, path/groupoid composition, local unitary quantum dynamics and holonomy/index invariants. The project already contains representatives of all four layers, but it has not derived the nonlinear update rule that creates and transports a protected defect.",
    },
    "next_gate": "version5_defect_transport_part_conclusion_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))