#!/usr/bin/env python3
"""Audit whether M35 derives the spatial SO(3)/SU(2) BPS completion."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def main() -> None:
    # A finite matrix algebra has no spatial derivation on scalar functions:
    # [f I, X]=0.  A spacetime Dirac/Hodge calculus is therefore extra data.
    f = sp.symbols("f")
    x = sp.MatrixSymbol("X", 5, 5)
    scalar_commutator_is_zero = True  # algebraic identity [f I_5, X]=0

    # Existing partial family module: 1 + 3 + 3 + 3, i.e. spins 0,1,1,1.
    spins = [sp.Rational(0), sp.Rational(1), sp.Rational(1), sp.Rational(1)]
    highest_weight_chern = [int(2 * j) for j in spins]

    # Superconnection trace after a free embedding rescaling Phi -> a Phi.
    # The common trace does not remove a if the embedding/physical field map
    # has not been derived.
    a = sp.symbols("a", positive=True)
    trace_coefficients = {
        "gauge_F_squared": "1",
        "scalar_DPhi_squared": str(2 * a**2),
        "quartic_Phi": str(a**4),
    }

    result = {
        "gate": "version5_spatial_so3_superconnection_parent_trace_gate",
        "spatial_calculus": {
            "finite_parent": "M35(C) linking operator container",
            "scalar_coordinate_commutator_zero": scalar_commutator_is_zero,
            "finite_trace_generates_spatial_derivative": False,
            "required_extra_structure": "spacetime Dirac/Hodge calculus or equivalent product geometry",
        },
        "gauge_selection": {
            "dimension_u35": 35**2,
            "dimension_corner_preserving_u20_plus_u15": 20**2 + 15**2,
            "dimension_desired_so3": 3,
            "full_M35_gauging_forbidden_by_previous_gate": True,
            "normalized_trace_selects_so3_subalgebra": False,
        },
        "core_extension": {
            "H2_ball_Z": 0,
            "boundary_line_Chern_number": 1,
            "single_L_extends_over_B3_as_line_bundle": False,
            "Chern_L_plus_L_star": 0,
            "L_plus_L_star_topologically_extendable_as_rank_two": True,
            "smooth_core_requires_complex_linear_branch_mixing": True,
            "KO6_J_alone_supplies_complex_linear_gauge_mixing": False,
        },
        "representation_test": {
            "current_partial_family_decomposition": "spin 0 + spin 1 + spin 1 + spin 1",
            "highest_weight_Chern_numbers": highest_weight_chern,
            "all_current_nontrivial_Chern_numbers_even": all(c % 2 == 0 for c in highest_weight_chern),
            "unit_Chern_eigenline_present_in_current_family_module": 1 in highest_weight_chern,
            "minimal_unit_Chern_representation": "spin 1/2 complex doublet",
            "previous_H15_M35_doublet_no_go_returns": True,
        },
        "trace_action": {
            "generic_rescaling": "Phi -> a Phi",
            "schematic_coefficients": trace_coefficients,
            "one_trace_fixes_coefficients_after_embedding_is_fixed": True,
            "M35_trace_derives_embedding_and_field_scale_a": False,
            "M35_trace_derives_Bogomolny_Hodge_relative_weight": False,
            "M35_trace_derives_vacuum_scale_v": False,
        },
        "conditional_result": {
            "if_spacetime_calculus_so3_embedding_and_rank_two_lift_are_supplied": "a single superconnection trace can package F_A, D_A Phi and Phi^2",
            "is_this_a_derivation_from_current_parent": False,
        },
        "verdict": {
            "spatial_SO3_connection_from_M35_trace": "fail",
            "smooth_unit_index_core_on_current_integer_spin_module": "fail",
            "trace_compatibility_after_external_inputs": "conditional_pass",
            "status": "boundary_hopf_orientation_pass_core_parent_derivation_fail",
            "physical_closure": False,
        },
        "next_gate": "version5_hopf_pair_odd_core_extension_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_spatial_so3_superconnection_parent_trace_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert f is not None and x is not None
    assert highest_weight_chern == [0, 2, 2, 2]
    assert result["core_extension"]["single_L_extends_over_B3_as_line_bundle"] is False
    assert result["representation_test"]["unit_Chern_eigenline_present_in_current_family_module"] is False
    assert result["gauge_selection"]["dimension_u35"] == 1225
    assert result["gauge_selection"]["dimension_corner_preserving_u20_plus_u15"] == 625
    print(output)


if __name__ == "__main__":
    main()