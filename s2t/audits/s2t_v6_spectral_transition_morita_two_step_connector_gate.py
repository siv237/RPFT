#!/usr/bin/env python3
"""Аудит двухшагового моритова коннектора семейной и слабой одноформ."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_morita_two_step_connector_gate_results.json"


def normalized_trace(a: np.ndarray) -> complex:
    return np.trace(a) / a.shape[0]


def relative_action(x: float, s: float, q: np.ndarray) -> float:
    ff = np.sqrt(x) * q
    fo = s * np.eye(2)
    curvature = np.kron(ff, np.eye(2)) - np.kron(np.eye(3), fo.T)
    return float(normalized_trace(curvature.conj().T @ curvature).real)


def main() -> None:
    direct = json.loads(
        (RESULTS / "s2t_v6_spectral_transition_radial_bridge_vortex_connector_gate_results.json").read_text()
    )
    degree_two = json.loads(
        (RESULTS / "s2t_v4_family_defect_degree_two_junk_gate_results.json").read_text()
    )
    tangent = json.loads(
        (RESULTS / "s2t_v5_rank_one_tangent_junk_gate_results.json").read_text()
    )
    morita = json.loads(
        (RESULTS / "s2t_v5_morita_linking_parent_gate_results.json").read_text()
    )
    superconnection = json.loads(
        (RESULTS / "s2t_v5_graded_correspondence_superconnection_gate_results.json").read_text()
    )
    centered = json.loads(
        (RESULTS / "s2t_v5_centered_connection_potential_gate_results.json").read_text()
    )

    rng = np.random.default_rng(20260821)
    zf = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    af = np.block([[np.zeros((2, 2)), zf.conj().T], [zf, np.zeros((2, 2))]])
    gamma_f = np.diag([1.0, 1.0, -1.0, -1.0])
    zh = 0.7 - 0.4j
    ah = np.array([[0.0, np.conj(zh)], [zh, 0.0]], dtype=complex)

    d_total = np.kron(af, np.eye(2)) + np.kron(gamma_f, ah)
    separated_square = np.kron(af @ af, np.eye(2)) + np.kron(np.eye(4), ah @ ah)
    graded_cross_residual = float(np.linalg.norm(d_total @ d_total - separated_square))
    grading_residual = float(np.linalg.norm(gamma_f @ af + af @ gamma_f))

    d_ungraded = np.kron(af, np.eye(2)) + np.kron(np.eye(4), ah)
    ungraded_cross = d_ungraded @ d_ungraded - separated_square
    ungraded_cross_norm = float(np.linalg.norm(ungraded_cross))

    q = np.diag([1.0, -1.0, 0.0]) / np.sqrt(2.0)
    x0, s0, h = 0.8, 0.7, 1.0e-4
    mixed_difference = (
        relative_action(x0 + h, s0 + h, q)
        - relative_action(x0 + h, s0 - h, q)
        - relative_action(x0 - h, s0 + h, q)
        + relative_action(x0 - h, s0 - h, q)
    ) / (4.0 * h * h)
    expected_additive = x0 * float(normalized_trace(q @ q).real) + s0 * s0
    additive_residual = abs(relative_action(x0, s0, q) - expected_additive)

    generic = degree_two["backgrounds"][0]["complexified_calculus"]
    tangent_structure = tangent["structural_result"]
    relative = morita["relative_bimodule_curvature"]
    curvature_comparison = superconnection["curvature_comparison"]

    result = {
        "gate": "version6_spectral_transition_morita_two_step_connector_gate",
        "input_certificates": {
            "direct_connector_exists": direct["verdict"]["canonical_direct_family_vortex_Higgs_connector_in_established_fields"],
            "mixed_oneform_module_exists": direct["verdict"]["mixed_physical_oneform_module_exists"],
            "mixed_module_selects_unique_connector": direct["verdict"]["mixed_module_selects_unique_nonzero_connector"],
        },
        "graded_product_audit": {
            "formula": "D_tot=D_f tensor 1+gamma_f tensor D_H",
            "family_oddness_residual": grading_residual,
            "mixed_square_residual": graded_cross_residual,
            "mixed_two_step_term_survives": False,
            "ungraded_control_cross_norm": ungraded_cross_norm,
            "ungraded_control_is_admissible_Dirac_product": False,
            "reason": "the graded cross terms cancel by gamma_f D_f + D_f gamma_f=0; removing gamma_f restores a cross term but violates the graded product",
        },
        "ordinary_degree_two_boundary": {
            "generic_particle_middle_quotient_rank": generic["canonical_quotient_particle_middle_rank"],
            "generic_traceless_symmetric_quotient_rank": generic["canonical_quotient_conjugate_middle_traceless_symmetric_rank"],
            "ordinary_family_shape_twoform_survives": False,
            "status": degree_two["verdict"]["ordinary_degree_two_junk_route"],
        },
        "rank_one_quotient_boundary": {
            "represented_two_forms": tangent_structure["represented_two_forms"],
            "degree_two_junk": tangent_structure["degree_two_junk"],
            "degree_two_quotient": tangent_structure["degree_two_quotient"],
            "quotient_complex_dimension": tangent_structure["quotient_complex_dimension"],
            "middle_shape_curvature_survives": tangent_structure["middle_shape_curvature_survives"],
        },
        "relative_curvature_audit": {
            "formula": relative["normalized_operator_trace_formula"],
            "centered_formula": relative["centered_formula"],
            "sample_additive_residual": additive_residual,
            "mixed_derivative_in_TrQ2_and_H2": float(mixed_difference),
            "Tr_Q": float(np.trace(q).real),
            "shape_Higgs_portal_generated": False,
            "interpretation": "centering kills the only bilinear trace cross term, leaving a sum of sector norms rather than Tr(Q^2) H^dagger H",
        },
        "superconnection_boundary": {
            "standard_middle_block": curvature_comparison["standard_superconnection"]["middle_block"],
            "standard_produces_moment_map_difference": curvature_comparison["standard_superconnection"]["produces_moment_map_difference"],
            "holomorphic_path_norm": curvature_comparison["holomorphic_superconnection"]["norm"],
            "holomorphic_produces_moment_map_difference": curvature_comparison["holomorphic_superconnection"]["produces_moment_map_difference"],
            "Hodge_requires_extra_primitive": curvature_comparison["Hodge_moment_map"]["requires_Hermitian_moment_map_primitive"],
        },
        "higher_functional_boundary": {
            "allowed_product_invariant": "Tr(Q^2) H^dagger H",
            "appears_in_current_quadratic_curvature_norm": False,
            "could_be_inserted_as_product_of_sector_norms": True,
            "product_coefficient_fixed_by_current_parent": False,
            "centered_connection_unique_orbit": centered["verdict"]["unique_Yukawa_connection"],
        },
        "verdict": {
            "graded_two_step_composition_generates_connector": False,
            "ordinary_degree_two_quotient_preserves_shape": False,
            "Morita_relative_curvature_generates_shape_Higgs_portal": False,
            "current_mixed_oneform_module_closes_connector": False,
            "current_architecture_has_internal_vortex_Higgs_connector": False,
            "physical_closure": False,
            "status": "the graded product cancels the mixed two-step operator, ordinary junk removes the family shape, and centered Morita curvature is additive; a nonzero portal would require a new higher functional or new carrier",
        },
        "next_gate": "version6_spectral_transition_connector_architecture_branch_decision_gate",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()