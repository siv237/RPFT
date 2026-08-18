#!/usr/bin/env python3
"""Audit the one-Hilbert-space/one-trace Version V boundary control."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_boundary_parent_trace_freeze_gate_results.json"

required_sources = {
    "route_assessment": "wiki/syntheses/version5-open-paths-assessment-2026-08-15.md",
    "wilson_parent": "s2t/gates/version4_wilson_defect_parent_superconnection_gate.tex",
    "rotor_momentum": "s2t/gates/wilson_rotor_momentum_sector_gate.tex",
    "family_axis": "s2t/gates/version4_family_defect_projector_supercurvature_gate.tex",
    "pairing_moment_map": "s2t/gates/version4_family_defect_quiver_moment_map_gate.tex",
    "ko6_sign": "s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex",
    "degree_two_junk": "s2t/gates/version4_family_defect_degree_two_junk_gate.tex",
    "fermionic_measure": "s2t/gates/version4_family_defect_fermionic_measure_hs_gate.tex",
    "majorana_parent": "s2t/gates/majorana_defect_parent_action_gate.tex",
    "majorana_selector": "s2t/gates/family_wilson_majorana_core_selector_gate.tex",
    "parent_trace_precedent": "s2t/gates/parent_trace_tensor_product_gate.tex",
}
source_presence = {key: (ROOT / path).exists() for key, path in required_sources.items()}
assert all(source_presence.values())

target_momentum = sp.Matrix([1, 1, 1, 3, 3, 3, 3, 3])
one_gauss = sp.Matrix([[1] * 8])
two_block_gauss = sp.Matrix(
    [
        [1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ]
)
full_constraint = sp.eye(8)

constraint_ledger = {
    "one_diagonal_u1": {
        "rank": one_gauss.rank(),
        "solution_dimension": 8 - one_gauss.rank(),
        "unique_target": False,
    },
    "two_irrep_blocks": {
        "rank": two_block_gauss.rank(),
        "solution_dimension": 8 - two_block_gauss.rank(),
        "unique_target": False,
    },
    "componentwise_projector": {
        "rank": full_constraint.rank(),
        "solution_dimension": 8 - full_constraint.rank(),
        "unique_target": True,
        "target": [int(value) for value in target_momentum],
        "status": "additional operator-valued datum in the frozen carrier",
    },
}
assert constraint_ledger["one_diagonal_u1"]["solution_dimension"] == 7
assert constraint_ledger["two_irrep_blocks"]["solution_dimension"] == 6
assert constraint_ledger["componentwise_projector"]["solution_dimension"] == 0

central_blocks = [
    "wilson_gaussian_root_family",
    "ko6_quiver_pairing",
    "bdg_majorana_core",
]
relative_trace_parameters = len(central_blocks) - 1
assert relative_trace_parameters == 2

output_ledger = {
    "odd_wilson_branch": {
        "local_result": "exact coefficient pair",
        "parent_status": "fail",
        "reason": "fixed-charge projector or imaginary coherent source is not derived",
    },
    "pairing_condensate": {
        "local_result": "stable normalized quiver moment-map saddle",
        "parent_status": "conditional",
        "reason": "ordinary trace has wrong mixed sign; degree-two and Pfaffian routes fail",
    },
    "tetrahedral_axis": {
        "local_result": "exact 2pi/3 oriented three-cycle selection",
        "parent_status": "conditional",
        "reason": "projector curvature is not embedded in the Wilson Gaussian parent block",
    },
    "exact_one_majorana": {
        "local_result": "rank-two family generator leaves one real kernel",
        "parent_status": "conditional",
        "reason": "root flux, condensate and core restriction are not jointly derived",
    },
    "independent_normalization": {
        "local_result": "conditional trace averaging and exact Wilson coefficients",
        "parent_status": "fail",
        "reason": "normalizations are used in construction or lack one action-level relative weight",
    },
}

candidate_ledger = {
    "fixed_charge_boundary": {
        "coefficient_pair": True,
        "one_trace": False,
        "selection_rule": False,
        "failure": "one or two Gauss laws do not select the eight-component target",
    },
    "coherent_source_gaussian": {
        "coefficient_pair": True,
        "one_trace": "conditional",
        "selection_rule": False,
        "failure": "axis-dependent imaginary source, contour and unit coefficient are external",
    },
    "direct_sum_superconnection": {
        "coefficient_pair": "sectorwise",
        "one_trace": False,
        "selection_rule": False,
        "failure": "at least three central sectors leave two relative trace weights",
    },
    "full_matrix_factor": {
        "coefficient_pair": "not tested",
        "one_trace": True,
        "selection_rule": False,
        "failure": "requires new off-diagonal connectors mixing inequivalent charge/grade sectors",
    },
}

result = {
    "date": "2026-08-15",
    "gate": "version5_boundary_parent_trace_freeze_gate",
    "source_presence": source_presence,
    "frozen_requirements": list(output_ledger),
    "central_trace_audit": {
        "current_inequivalent_blocks": central_blocks,
        "block_count": len(central_blocks),
        "free_relative_trace_parameters_after_normalization": relative_trace_parameters,
        "single_symmetry_derived_trace": False,
    },
    "fixed_charge_constraint_audit": constraint_ledger,
    "candidate_ledger": candidate_ledger,
    "five_output_ledger": output_ledger,
    "verdict": {
        "common_boundary_kinematics": "partial_pass",
        "exact_wilson_coefficient_pair": "operator_pass",
        "one_parent_trace": False,
        "fixed_charge_or_source_selection": False,
        "joint_condensate_axis_majorana_derivation": False,
        "mathematical_parent_architecture_pass": False,
        "physical_closure": False,
        "boundary_source_current_realization": "closed_as_version5_parent_architecture",
        "reason": (
            "exact local modules exist, but the symmetry-preserving direct sum has free central "
            "weights and neither the charge projector nor the coherent source is selected"
        ),
    },
    "next_gate": {
        "name": "version5_finite_geometry_complexity_bound_gate",
        "purpose": (
            "bound and enumerate genuinely new irreducible finite geometries without reopening "
            "closed KO6, rank-one Pati-Salam or direct-sum boundary actions"
        ),
    },
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))