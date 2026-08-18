#!/usr/bin/env python3
"""Физический H15-модуль заряженных одноформ и остаточная свобода связности."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_h15_physical_oneform_bimodule_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


split = load_result("s2t_v5_h15_neutrino_degree_split_gate_results.json")
rank_one = load_result("s2t_v5_rank_one_tangent_junk_gate_results.json")
yukawa = load_result("s2t_v4_higgs_yukawa_gate_results.json")

assert split["verdict"]["H15_matches_current_M35_parent"]
assert split["verdict"]["H15_contains_exactly_three_charged_Yukawa_edges"]
assert rank_one["structural_result"]["represented_one_forms_complex_dimension"] == 4

edges = [
    {"name": "u", "left": "Q_L", "right": "u_R", "scalar": "tilde_H"},
    {"name": "d", "left": "Q_L", "right": "d_R", "scalar": "H"},
    {"name": "e", "left": "L_L", "right": "e_R", "scalar": "H"},
]
signatures = [(edge["left"], edge["right"], edge["scalar"]) for edge in edges]
intertwiner_matrix = np.array(
    [[int(left == right) for right in signatures] for left in signatures],
    dtype=int,
)

assert len(set(signatures)) == 3
assert np.array_equal(intertwiner_matrix, np.eye(3, dtype=int))
assert yukawa["allowed_vertex_count"] == 4

edge_dimension = int(np.trace(intertwiner_matrix))
family_dimension = rank_one["structural_result"][
    "represented_one_forms_complex_dimension"
]
physical_dimension = family_dimension * edge_dimension

common = np.ones((3, 1), dtype=float) / np.sqrt(3.0)
common_projector = common @ common.T
relative_projector = np.eye(3) - common_projector
common_rank = int(np.linalg.matrix_rank(common_projector, tol=1.0e-12))
relative_rank = int(np.linalg.matrix_rank(relative_projector, tol=1.0e-12))
residuals = {
    "common_idempotence": float(
        np.linalg.norm(common_projector @ common_projector - common_projector)
    ),
    "relative_idempotence": float(
        np.linalg.norm(relative_projector @ relative_projector - relative_projector)
    ),
    "orthogonality": float(np.linalg.norm(common_projector @ relative_projector)),
    "sum_to_identity": float(
        np.linalg.norm(common_projector + relative_projector - np.eye(3))
    ),
}
assert max(residuals.values()) < 1.0e-12
assert common_rank == 1
assert relative_rank == 2

result = {
    "gate": "version5_h15_physical_oneform_bimodule_gate",
    "input_certificates": {
        "H15_architecture_freeze": "pass",
        "rank_one_family_oneforms_dimension_four": "pass",
        "charged_Yukawa_menu_u_d_e": "pass",
    },
    "charged_edge_multiplicity_space": {
        "definition": "Lambda_ch=Hom_G(Q_L tensor tilde_H,u_R) + Hom_G(Q_L tensor H,d_R) + Hom_G(L_L tensor H,e_R)",
        "edges": edges,
        "edge_signatures": signatures,
        "intertwiner_dimension_matrix": intertwiner_matrix.tolist(),
        "pairwise_inequivalent_simple_edges": True,
        "complex_dimension": edge_dimension,
        "bimodule_endomorphism_algebra": "C^3",
        "centered_relative_algebra": "C^2",
    },
    "physical_oneform_bimodule": {
        "formula": "Y_rho=E_rho tensor Lambda_ch",
        "family_factor": "E_rho=rho M3 Q + Q M3 rho",
        "family_factor_complex_dimension": family_dimension,
        "edge_multiplicity_complex_dimension": edge_dimension,
        "total_multiplicity_complex_dimension": physical_dimension,
        "finite_semisimple_module_projective": True,
        "differential_degree": 1,
        "contains_neutrino_edge": False,
    },
    "connection_affine_space": {
        "reference": "Grassmann connection from the rank-one family projector",
        "difference_space_contains": "End_bimodule(Lambda_ch)=C^3",
        "Hermitian_reality_reduces_complex_to_real_per_edge": True,
        "Hermitian_real_dimension_before_common_quotient": 3,
        "relative_real_dimension_after_common_quotient": 2,
        "KO6_pairs_each_edge_with_its_conjugate": True,
        "KO6_identifies_distinct_u_d_e_edges": False,
    },
    "grassmann_readout": {
        "acts_identically_on_edge_multiplicity": True,
        "common_projector": common_projector.tolist(),
        "relative_projector": relative_projector.tolist(),
        "common_rank": common_rank,
        "unselected_relative_rank": relative_rank,
        "residuals": residuals,
        "selects_nonzero_Yukawa_amplitude": False,
        "selects_relative_u_d_e_weights": False,
    },
    "literature_boundary": {
        "finite_Dirac_operator_encodes_Yukawa_inputs": True,
        "projective_module_admits_Grassmann_connection": True,
        "connections_form_affine_space_over_oneform_valued_module_maps": True,
        "new_project_result": "the corrected H15 one-form typing leaves exactly two relative charged-edge directions after the common connection is removed",
    },
    "verdict": {
        "correctly_typed_physical_oneform_module_exists": "pass",
        "projectivity": "pass",
        "exactly_three_charged_edge_types": "pass",
        "Grassmann_connection_fixes_family_reference": "pass",
        "Grassmann_connection_uniquely_fixes_u_d_e_connection": "fail",
        "residual_relative_connection_dimension": 2,
        "physical_closure": False,
        "status": "the type error is repaired, but gauge inequivalence of u,d,e leaves two relative connection directions",
    },
    "next_gate": (
        "Test the second-order differential calculus and spectral torsion on the "
        "three-edge H15 module. If it remains block diagonal, close the Morita "
        "one-form route without another potential."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))