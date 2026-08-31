#!/usr/bin/env python3
"""Exact finite audit of named dimensionless candidates for c0."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_typed_internal_map_candidate_audit_gate_results.json"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> None:
    score = load("s2t/results/s2t_v3_one_scale_blind_scorecard_results.json")
    gauge = load("s2t/results/s2t_v3_a4_gauge_coupling_results.json")
    profile = load("s2t/results/s2t_v7_common_spectral_profile_singlet_virtual_ratio_gate_results.json")
    curvature = load("s2t/results/s2t_v8_baryon_spacetime_supercurvature_cubic_projection_admission_gate_results.json")
    previous = load("s2t/results/s2t_v8_baryon_dimensional_transmutation_input_origin_gate_results.json")

    assert score["predictions"]["fermion_mass_ratios"] == [1, 1]
    assert score["predictions"]["scalar_mass_ratios"] == [2, 2, 2]
    assert gauge["mass_and_supertrace"]["m_A_squared_over_chi_squared"] == "3"
    assert gauge["coupling"]["g_squared"] == "3/8"
    assert profile["pure_heat_kernel_profile"]["R_chi"] == "1"
    assert curvature["coefficient_shape"]["lambda_3_squared_over_alpha_beta"] == "4"
    assert previous["next_gate"] == "version8_baryon_c0_typed_internal_map_candidate_audit_gate"

    values = {
        "finite_dirac_mass_squared_ratio": sp.Integer(1),
        "vector_mass_squared_ratio": sp.Integer(3),
        "scalar_mass_squared_ratio": sp.Integer(4),
        "spectral_gauge_coupling_squared": sp.Rational(3, 8),
        "index_selected_kms_ratio": sp.exp(-2),
        "pure_heat_profile_ratio": sp.Integer(1),
        "shifted_curvature_shape_ratio": sp.Integer(4),
    }
    ledger = {
        "finite_dirac_mass_squared_ratio": (True, True, False, False, True),
        "vector_mass_squared_ratio": (True, True, False, False, True),
        "scalar_mass_squared_ratio": (True, True, False, False, True),
        "spectral_gauge_coupling_squared": (True, True, False, False, True),
        "index_selected_kms_ratio": (True, True, False, False, True),
        "pure_heat_profile_ratio": (True, False, False, False, True),
        "shifted_curvature_shape_ratio": (True, True, True, False, True),
    }
    admissions = {name: all(flags) for name, flags in ledger.items()}
    assert len(values) == 7
    assert sum(admissions.values()) == 0
    assert values["scalar_mass_squared_ratio"] == values["shifted_curvature_shape_ratio"]
    assert ledger["shifted_curvature_shape_ratio"][2]
    assert not ledger["shifted_curvature_shape_ratio"][3]
    assert not any(
        atom.is_Float for value in values.values() for atom in sp.preorder_traversal(value)
    )

    condition_names = [
        "dimensionless",
        "internally_selected",
        "same_carrier_or_declared_typed_map",
        "appears_in_auxiliary_pole_hessian",
        "target_independent",
    ]
    candidates = {}
    for name, value in values.items():
        candidates[name] = {
            "exact_value": sp.sstr(value),
            "conditions": dict(zip(condition_names, ledger[name])),
            "admitted_as_c0": admissions[name],
        }

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_typed_internal_map_candidate_audit_gate",
        "required_role": "m_pole^2=c0*a in the quadratic Hessian of the auxiliary six-point carrier",
        "candidate_count": 7,
        "candidates": candidates,
        "admitted_count": 0,
        "strongest_near_miss": {
            "candidate": "shifted_curvature_shape_ratio",
            "value": "4",
            "same_baryon_trace_carrier": True,
            "defect": "lambda_3^2/(alpha*beta) is an interaction-shape ratio, not m_pole^2/a",
        },
        "exact_collision": {
            "value": "4",
            "roles": ["scalar_mass_squared_ratio", "shifted_curvature_shape_ratio"],
            "typed_identification_allowed": False,
        },
        "verdict": {
            "named_internal_ratio_registry_exhausted": True,
            "typed_c0_map_found": False,
            "universal_future_map_no_go_claimed": False,
        },
        "next_gate": "version8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()