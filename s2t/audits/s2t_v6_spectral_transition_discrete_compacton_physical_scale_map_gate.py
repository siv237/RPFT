#!/usr/bin/env python3
"""Audit whether the exact compacton fixes an absolute physical scale."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_physical_scale_map_gate_results.json"
HBAR_C_GEV_M = 1.973269804e-16


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def main() -> None:
    theta = 0.5 * np.pi
    kappa = 2.0 * np.pi
    support_cells = 2

    constraint_matrix = np.array(
        [
            [1.0, -1.0, 0.0],  # log(a)-log(dt)=log(c)
            [0.0, 1.0, 1.0],   # log(dt)+log(E)=log(hbar*theta)
        ]
    )
    rank = int(np.linalg.matrix_rank(constraint_matrix))
    nullity = int(constraint_matrix.shape[1] - rank)
    scale_null_vector = np.array([1.0, 1.0, -1.0])
    null_residual = float(np.linalg.norm(constraint_matrix @ scale_null_vector))

    rescaling_family = {}
    for scale in (0.1, 1.0, 10.0):
        lattice_step = scale
        time_step = scale
        energy = theta / time_step
        size = support_cells * lattice_step
        continuum_coupling = kappa / lattice_step
        rescaling_family[str(scale)] = {
            "a_natural_units": lattice_step,
            "delta_t_natural_units": time_step,
            "energy_natural_units": energy,
            "diameter_natural_units": size,
            "effective_continuum_coupling": continuum_coupling,
            "a_over_delta_t": lattice_step / time_step,
            "energy_times_delta_t": energy * time_step,
            "energy_times_diameter": energy * size,
            "energy_over_effective_coupling": energy / continuum_coupling,
        }

    lambda_s2t = np.sqrt(np.pi) * 1.0e16
    arbitrary_scale_assignments = {}
    for alpha in (0.1, 1.0, float(np.pi)):
        lattice_step_m = alpha * HBAR_C_GEV_M / lambda_s2t
        diameter_m = support_cells * lattice_step_m
        energy_gev = theta * lambda_s2t / alpha
        coupling_gev = kappa * lambda_s2t / alpha
        compton_length_m = HBAR_C_GEV_M / energy_gev
        arbitrary_scale_assignments[str(alpha)] = {
            "assumption": "a=alpha*hbar*c/Lambda_S2T",
            "lattice_step_m": lattice_step_m,
            "diameter_m": diameter_m,
            "minimal_zone_energy_GeV": energy_gev,
            "effective_continuum_coupling_GeV": coupling_gev,
            "compton_length_m": compton_length_m,
            "diameter_over_compton_length": diameter_m / compton_length_m,
            "energy_times_diameter_over_hbar_c": energy_gev * diameter_m / HBAR_C_GEV_M,
        }

    quasienergy_aliases = {}
    for sign in (-1, 1):
        quasienergy_aliases[str(sign)] = [
            float(sign * theta + 2.0 * np.pi * branch) for branch in range(-2, 3)
        ]

    v4_scale = load_result("s2t_v4_absolute_scale_eft_validity_gate_results.json")
    v5_scale = load_result("s2t_v5_projector_superconnection_common_scale_gate_results.json")
    v6_scale = load_result("s2t_v6_single_thread_scale_hierarchy_branch_decision_gate_results.json")

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_physical_scale_map_gate",
        "exact_dimensionless_data": {
            "compacton_coupling": kappa,
            "minimal_quasienergy_phase_magnitude": theta,
            "support_cells": support_cells,
            "conditional_relations": {
                "causal_speed": "c=a/delta_t",
                "minimal_zone_energy": "E=pi*hbar/(2*delta_t)",
                "diameter": "L=2*a",
                "mass_size_product": "E*L=pi*hbar*c",
                "diameter_over_compton_length": "L/lambda_C=pi",
                "continuum_coupling": "g=kappa/a=2*pi/a",
                "energy_over_coupling_at_c_equal_1": "E/g=1/4",
            },
        },
        "dimensional_rank_test": {
            "variables": ["log_a", "log_delta_t", "log_E"],
            "constraints": ["a/delta_t=c", "E*delta_t=hbar*pi/2"],
            "constraint_rank": rank,
            "scale_nullity": nullity,
            "scale_null_vector": scale_null_vector.tolist(),
            "null_residual": null_residual,
            "rescaling_symmetry": "(a,delta_t,E,g)->(lambda*a,lambda*delta_t,E/lambda,g/lambda)",
            "rescaling_examples": rescaling_family,
        },
        "quasienergy_modularity": {
            "eigenphases": ["+i", "-i"],
            "principal_zone_phases": [-theta, theta],
            "aliases_theta_plus_2pi_n": quasienergy_aliases,
            "absolute_energy_branch_selected_by_current_parent": False,
            "relative_phase_to_vacuum_can_be_defined": True,
            "time_step_still_required": True,
        },
        "continuum_limit_test": {
            "controlled_nonlinear_dirac_scaling": "kappa=g*a with fixed finite g and a->0",
            "compacton_requirement": "kappa=2*pi",
            "fixed_g_continuum_survival": False,
            "required_behavior_to_keep_compacton": "g=2*pi/a diverges as a->0",
            "compacton_is_lattice_scale_object": True,
        },
        "existing_project_scale_ledger": {
            "Lambda_S2T_GeV": lambda_s2t,
            "equation_linking_compacton_a_to_Lambda_S2T_found": False,
            "arbitrary_alpha_assignments": arbitrary_scale_assignments,
            "version4_planck_matching_controlled": v4_scale["same_scale_validity"]["valid"],
            "version4_absolute_scale_verdict": v4_scale["verdict"],
            "version5_common_superconnection_scale": v5_scale["verdict"]["common_scale_from_current_parent"],
            "version5_finite_radius_prediction": v5_scale["verdict"]["finite_radius_prediction"],
            "version6_hidden_scale_hierarchy": v6_scale["scale_ledger"]["hidden_scale_hierarchy_available"],
            "version6_absolute_length_scale": v6_scale["scale_ledger"]["version6_absolute_length_scale"],
            "version6_absolute_energy_scale": v6_scale["scale_ledger"]["version6_absolute_energy_scale"],
        },
        "interpretation": {
            "absolute_lattice_step_derived": False,
            "absolute_time_step_derived": False,
            "absolute_mass_derived": False,
            "conditional_mass_size_product_derived": True,
            "conditional_dimensionless_ratio": "E*L/(hbar*c)=pi",
            "blind_observable_prediction_closed": False,
            "new_dimensionful_input_required": True,
        },
        "verdict": {
            "R4_status": "local_lattice_endpoint_only",
            "R5_status": "failed_for_absolute_scale_and_mass",
            "status": "the exact phase and two-cell support imply only the conditional reciprocal relation E*L=pi*hbar*c; one continuous scale remains free, quasienergy is modular, and keeping kappa=2*pi forces the continuum coupling to diverge as a->0, so neither a physical size nor a mass is predicted",
        },
        "next_gate": "version6_spectral_transition_discrete_compacton_dynamical_capture_gate",
    }

    assert rank == 2 and nullity == 1 and null_residual < 1.0e-14
    assert all(abs(item["a_over_delta_t"] - 1.0) < 1.0e-14 for item in rescaling_family.values())
    assert all(abs(item["energy_times_delta_t"] - theta) < 1.0e-14 for item in rescaling_family.values())
    assert all(abs(item["energy_times_diameter"] - np.pi) < 1.0e-14 for item in rescaling_family.values())
    assert all(abs(item["energy_over_effective_coupling"] - 0.25) < 1.0e-14 for item in rescaling_family.values())
    assert all(
        abs(item["energy_times_diameter_over_hbar_c"] - np.pi) < 1.0e-12
        for item in arbitrary_scale_assignments.values()
    )
    assert all(
        abs(item["diameter_over_compton_length"] - np.pi) < 1.0e-12
        for item in arbitrary_scale_assignments.values()
    )
    assert result["existing_project_scale_ledger"]["version4_planck_matching_controlled"] is False
    assert result["existing_project_scale_ledger"]["version5_common_superconnection_scale"] is False
    assert result["existing_project_scale_ledger"]["version6_hidden_scale_hierarchy"] is False

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()