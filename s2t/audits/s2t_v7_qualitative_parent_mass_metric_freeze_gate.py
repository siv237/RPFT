#!/usr/bin/env python3
"""Build the final qualitative/quantitative status registry for Tome VII."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    edge_hessians,
    physical_blocks,
    signature,
)
from s2t_v7_incidence_transfer_markov_weight_gate import polar_coisometry
from s2t_v7_polar_transfer_cross_curvature_origin_gate import (
    relative_transfer_vacuum_hessian,
)


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUTPUT = RESULTS / "s2t_v7_qualitative_parent_mass_metric_freeze_gate_results.json"
TOL = 1.0e-10


def load(stem: str) -> dict:
    path = RESULTS / f"s2t_v7_{stem}_gate_results.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    common = load("common_chain_number_hodge_relative_trace")
    support = load("minimal_curvature_support_trace")
    mixing = load("higher_cycle_character_mixing_freeze")
    scale = load("single_scale_calibration_closure")
    spacetime = load("spacetime_kinetic_potential_ratio_admission")
    gauge = load("full_gauge_weighted_edge_carrier")
    color = load("color_preserving_quadratic_selector_origin")
    corrected = load("corrected_vacuum_relative_edge_hessian")

    reference, variations, _, down_cut = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    linking_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )

    linking_values = eigvalsh(linking_vacuum)
    assert linking_values[0] > -TOL
    assert np.linalg.matrix_rank(linking_vacuum, TOL) == 22

    weights = (0.0, 1.0e-6, 0.25, 1.0, 4.0, 1.0e3, 1.0e6)
    stability_scan = []
    for weight in weights:
        origin_values = eigvalsh(edge_origin)
        vacuum_values = eigvalsh(
            edge_vacuum + 2.0 * weight * linking_vacuum
        )
        stability_scan.append({
            "relative_metric_weight": weight,
            "origin_signature": signature(origin_values),
            "vacuum_signature": signature(vacuum_values),
            "origin_heavy_gap": float(origin_values[7]),
            "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            "vacuum_maximum_eigenvalue": float(vacuum_values[-1]),
        })

    assert all(
        row["origin_signature"] == [7, 0, 20]
        and row["vacuum_signature"] == [0, 0, 27]
        for row in stability_scan
    )

    assert common["verdict"]["one_unweighted_common_trace_exists"]
    assert common["verdict"]["common_trace_correct_origin_selector"]
    assert common["verdict"]["common_trace_strictly_stable_vacuum"]
    assert not common["verdict"]["unique_relative_hodge_metric_derived"]
    assert support["verdict"]["linking_factor_trace_unique"]
    assert not support["verdict"]["common_direct_sum_trace_unique"]
    assert mixing["verdict"]["family_mixing_branch_frozen_in_current_single_cycle_parent"]
    assert not mixing["verdict"]["single_conjugacy_class_can_select_CKM_eigenvectors"]
    assert scale["verdict"]["dimensionless_mass_ratio_sqrt_2_predicted"]
    assert not scale["verdict"]["one_input_suffices_for_full_nonlinear_EFT"]
    assert not spacetime["verdict"][
        "unique_kinetic_to_potential_ratio_from_current_parent"
    ]
    assert not gauge["verdict"]["physical_color_preserving_vacuum_survives"]
    assert color["verdict"]["color_preserving_quadratic_selector_obtained"]
    assert corrected["contract_update"]["relative_edge_alignment"] == "not_selected"

    task_registry = [
        {
            "task": "common_rank_changing_carrier",
            "status": "passed_after_carrier_correction",
            "scope": "E_aff tensor Lambda_ch and the associated edge/linking carriers",
        },
        {
            "task": "stationary_unstable_zero",
            "status": "passed_on_tested_real_slice",
            "result": "origin signature (7,0,20)",
        },
        {
            "task": "finite_nonlinear_saturation",
            "status": "passed_on_tested_real_slice",
            "result": "target signature (0,0,27)",
        },
        {
            "task": "one_curvature_action",
            "status": "passed_qualitatively",
            "result": "S_eta=S_E+eta||R_U||^2 for eta>0",
        },
        {
            "task": "unique_relative_mass_metric",
            "status": "failed",
            "reason": "nontrivial center leaves a relative trace weight",
        },
        {
            "task": "family_phase_and_mixing_selection",
            "status": "failed_in_single_cycle_parent",
            "reason": "one conjugacy class does not select relative family axes",
        },
        {
            "task": "absolute_scale_and_full_nonlinear_EFT",
            "status": "partial",
            "reason": "one mass fixes the linear scale but f0 and the quartic remain external",
        },
        {
            "task": "full_gauge_spacetime_physical_closure",
            "status": "not_reached",
            "reason": "the color-preserving selector is derived, but no unique common physical gauge trace exists",
        },
        {
            "task": "particle_mass_and_CKM_PMNS_predictions",
            "status": "forbidden",
            "reason": "mass metric and family axes are not derived",
        },
    ]

    result = {
        "gate": "version7_qualitative_parent_mass_metric_freeze_gate",
        "tested_real_slice": {
            "dimension": len(variations),
            "root_directions": 7,
            "heavy_directions": 20,
            "relative_linking_hessian_rank_at_vacuum": int(
                np.linalg.matrix_rank(linking_vacuum, TOL)
            ),
            "relative_linking_hessian_positive_semidefinite": True,
            "positive_metric_scan": stability_scan,
        },
        "task_registry": task_registry,
        "frozen_positive_core": {
            "common_carrier_exists": True,
            "one_unweighted_representative_action_exists": True,
            "stationary_zero_has_seven_negative_modes": True,
            "twenty_heavy_competitors_are_positive_at_origin": True,
            "target_is_strictly_stable_on_tested_slice": True,
            "qualitative_signatures_hold_for_all_positive_relative_weights": True,
            "linking_endpoint_generates_M21": True,
            "color_preserving_quadratic_selector_exists": True,
        },
        "frozen_boundaries": {
            "unique_parent_action_derived": False,
            "unique_mass_metric_derived": False,
            "full_field_space_hessian_completed": False,
            "family_phases_selected": False,
            "CKM_PMNS_derived": False,
            "absolute_scale_derived": False,
            "full_spacetime_gauge_closure_obtained": False,
            "new_particle_names_authorized": False,
        },
        "reopening_conditions": [
            "derive a physical offdiagonal connector between the edge and linking sectors",
            "derive a second noncommuting family tensor for phase and mixing selection",
            "derive one common gauge-spacetime trace fixing the kinetic and mass metrics",
        ],
        "verdict": {
            "qualitative_radial_incidence_universality_class_closed": True,
            "complete_physical_rank_changing_parent_obtained": False,
            "tome7_research_question_completed": True,
            "numerical_mass_predictions_allowed": False,
            "particle_identification_allowed": False,
            "status": "tome7_qualitative_class_closed_full_physical_closure_not_obtained",
            "next_document": "version7_final_conclusion_and_next_program",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()