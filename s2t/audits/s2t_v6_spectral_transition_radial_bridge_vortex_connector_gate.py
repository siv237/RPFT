#!/usr/bin/env python3
"""Классификация прямых коннекторов семейного вихря со слабым дублетом."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_radial_bridge_vortex_connector_gate_results.json"


def spin_generators(j: float) -> list[np.ndarray]:
    """Эрмитовы генераторы su(2) в стандартном базисе |m>."""
    dim = int(round(2 * j + 1))
    ms = np.array([j - k for k in range(dim)], dtype=float)
    jp = np.zeros((dim, dim), dtype=complex)
    for col, m in enumerate(ms):
        target = m + 1
        rows = np.where(np.isclose(ms, target))[0]
        if len(rows):
            jp[rows[0], col] = np.sqrt((j - m) * (j + m + 1))
    jm = jp.conj().T
    return [(jp + jm) / 2, (jp - jm) / (2j), np.diag(ms)]


def nullity(matrix: np.ndarray, tol: float = 1.0e-10) -> int:
    singular = np.linalg.svd(matrix, compute_uv=False)
    return int(matrix.shape[1] - np.sum(singular > tol))


def invariant_covector_dimension(j: int) -> int:
    gens = spin_generators(float(j))
    constraint = np.vstack([g.T for g in gens])
    return nullity(constraint)


def weak_singlet_to_doublet_dimension() -> int:
    gens = spin_generators(0.5)
    constraint = np.vstack(gens + [0.5 * np.eye(2)])
    return nullity(constraint)


def direct_product_intertwiner_dimension(j_family: int) -> int:
    """Hom_{SO3 x SU2 x U1}((j,1,0),(0,2,1/2))."""
    d = 2 * j_family + 1
    jf = spin_generators(float(j_family))
    jw = spin_generators(0.5)
    constraints = []
    # vec(A J_f)= (J_f^T tensor I_2) vec(A)
    constraints.extend(np.kron(g.T, np.eye(2)) for g in jf)
    # vec(J_w A)= (I_d tensor J_w) vec(A) in column-major convention
    constraints.extend(np.kron(np.eye(d), g) for g in jw)
    constraints.append(0.5 * np.eye(2 * d))
    return nullity(np.vstack(constraints))


def main() -> None:
    localization = json.loads(
        (RESULTS / "s2t_v6_spectral_transition_rank_change_localization_gate_results.json").read_text()
    )
    field = json.loads(
        (RESULTS / "s2t_v6_bosonic_defect_field_identification_gate_results.json").read_text()
    )
    commuting = json.loads(
        (RESULTS / "s2t_v5_commuting_square_readout_gate_results.json").read_text()
    )
    oneforms = json.loads(
        (RESULTS / "s2t_v5_h15_physical_oneform_bimodule_gate_results.json").read_text()
    )
    corner = json.loads(
        (RESULTS / "s2t_v5_physical_corner_connection_classification_gate_results.json").read_text()
    )
    coordinate = json.loads(
        (RESULTS / "s2t_v5_m300_coordinate_algebra_wellposedness_gate_results.json").read_text()
    )

    defect_spins = {"B_family_connection": 1, "Q_shape": 2, "T_tetrahedral": 3}
    invariant_covectors = {name: invariant_covector_dimension(j) for name, j in defect_spins.items()}
    direct_homs = {name: direct_product_intertwiner_dimension(j) for name, j in defect_spins.items()}
    required_new_carrier_dimensions = {name: 2 * (2 * j + 1) for name, j in defect_spins.items()}

    field_content = commuting["equivariant_field_content"]
    oneform_module = oneforms["physical_oneform_bimodule"]
    corner_verdict = corner["verdict"]

    result = {
        "gate": "version6_spectral_transition_radial_bridge_vortex_connector_gate",
        "input_certificates": {
            "radial_bridge_localization_pass": localization["verdict"]["existing_radial_bridge_localizes_H_zero"],
            "Q_SM_representation": field["field_representation"]["standard_model_representation"],
            "Q_family_spin": 2,
            "M300_is_ambient_not_coordinate_algebra": coordinate["full_matrix_coordinate_interpretation"]["coordinate_algebra"] == "M300(C) in its defining representation on C300" and coordinate["verdict"]["M300_as_coordinate_algebra_on_C300"] == "fail",
        },
        "representation_audit": {
            "symmetry_group": "SO(3)_fam x SU(2)_L x U(1)_Y",
            "H_representation": "(j_f=0,j_w=1/2,Y=1/2)",
            "defect_representations": {
                "B_family_connection": "(1,0,0)",
                "Q_shape": "(2,0,0)",
                "T_tetrahedral": "(3,0,0)",
            },
            "SO3_invariant_covector_dimensions": invariant_covectors,
            "direct_defect_to_H_intertwiner_dimensions": direct_homs,
            "weak_singlet_to_H_doublet_intertwiner_dimension": weak_singlet_to_doublet_dimension(),
            "all_direct_linear_connectors_zero": all(v == 0 for v in direct_homs.values()),
            "minimal_complex_dimensions_if_new_mixed_carriers_are_added": required_new_carrier_dimensions,
        },
        "existing_equivariant_arrows": {
            "family_left_arrow_dimension": field_content["Hom_A4(C4_triplet,C3_triplet)_dimension"],
            "family_left_arrow": field_content["left_arrow"],
            "radial_right_arrow_dimension": field_content["End_A4(C3_triplet)_dimension"],
            "radial_right_arrow": field_content["right_arrow"],
            "continuous_family_orientation_fields": field_content["continuous_family_orientation_fields"],
            "orientation_sensitive_family_Higgs_arrow_present": False,
            "reason": "the only common curvature arrow is proportional to the family identity, so its mixed trace sees T |H|^2 and annihilates traceless Q",
        },
        "physical_oneform_boundary": {
            "module": oneform_module["formula"],
            "complex_dimension": oneform_module["total_multiplicity_complex_dimension"],
            "charged_edge_types": [edge["name"] for edge in oneforms["charged_edge_multiplicity_space"]["edges"]],
            "relative_connection_dimension": oneforms["connection_affine_space"]["relative_real_dimension_after_common_quotient"],
            "canonical_nonzero_section_selected": False,
            "interpretation": "a mixed tensor-product module exists, but it is an affine space of connections rather than a uniquely selected bosonic connector",
        },
        "Morita_connection_boundary": {
            "minimum_physical_connection_ambiguity_complex_dimension": corner_verdict["minimum_complex_ambiguity_dimension"],
            "minimum_centered_ambiguity_complex_dimension": corner_verdict["minimum_centered_ambiguity_dimension"],
            "trace_selects_nonzero_connection": corner_verdict["trace_alone_selects_Yukawa"],
            "unique_Yukawa_connection": corner_verdict["unique_Yukawa_connection"],
        },
        "full_M300_boundary": {
            "full_one_form_classification_from_existing_data": coordinate["verdict"]["full_one_form_classification_from_existing_data"],
            "hidden_arrow_claim_from_M300_matrix_units_is_valid": False,
            "reason": "M300 is the ambient endomorphism/trace carrier; it does not define Omega_D^1 without coordinate and bimodule data",
            "absolute_absence_of_every_possible_extended_connector_proved": False,
        },
        "quadratic_invariant_boundary": {
            "Tr_Q2_HdaggerH_symmetry_allowed": True,
            "coefficient_in_current_minimal_parent": localization["input_certificates"]["Q_shape_Higgs_portal_coefficient"],
            "symmetry_permission_implies_parent_origin": False,
        },
        "verdict": {
            "canonical_direct_family_vortex_Higgs_connector_in_established_fields": False,
            "current_M300_radial_arrow_is_orientation_sensitive": False,
            "mixed_physical_oneform_module_exists": True,
            "mixed_module_selects_unique_nonzero_connector": False,
            "hidden_connector_can_be_claimed_from_ambient_M300": False,
            "new_bifundamental_would_extend_the_model": True,
            "physical_closure": False,
            "status": "all established direct equivariant arrows are radial or family-only; the mixed oneform module is nonunique, and ambient M300 supplies no hidden physical arrow",
        },
        "next_gate": "version6_spectral_transition_morita_two_step_connector_gate",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()