#!/usr/bin/env python3
"""Audit whether Tome VIII has closed a unique physical dynamics.

The audit deliberately separates exact finite-dimensional mathematics from
the extra data required to interpret a QMS as one physical time evolution.
It does not search for a new selector.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_dynamic_physical_closure_redteam_gate_results.json"
RESULTS = ROOT / "s2t/results"


def load(name: str) -> dict:
    path = RESULTS / name
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    clock = load("s2t_v8_intrinsic_noise_clock_dilation_gate_results.json")
    primitive = load("s2t_v8_full_primitive_markov_generator_assembly_gate_results.json")
    kms = load("s2t_v8_kms_nontracial_relative_rate_selector_gate_results.json")
    bohr = load("s2t_v8_modular_bohr_parent_origin_gate_results.json")
    orientation = load("s2t_v8_chain_orientation_index_defect_selector_gate_results.json")
    rates = load("s2t_v8_common_chain_dirichlet_rate_metric_gate_results.json")
    kernel = load("s2t_v8_correlation_kernel_short_time_rate_selector_gate_results.json")
    action = load("s2t_v8_physical_correlation_kernel_parent_action_origin_gate_results.json")
    mobility = load("s2t_v8_fluctuation_dissipation_mobility_origin_gate_results.json")
    frame = load("s2t_v8_canonical_noise_frame_common_trace_gate_results.json")
    symmetry = load("s2t_v8_noise_isotropy_symmetry_admission_gate_results.json")

    assert clock["verdict"]["canonical_dimensionless_lindblad_time_exists"]
    assert not clock["verdict"]["intrinsic_physical_rate_derived"]
    assert not clock["verdict"]["autonomous_fresh_noise_supply_derived"]
    assert primitive["verdict"]["complete_positivity_has_lindblad_jump_certificate"]
    assert primitive["verdict"]["full_fixed_algebra_is_scalar"]
    assert not primitive["verdict"]["unique_relative_rate_metric_derived"]
    assert not kms["verdict"]["KMS_selects_current_six_relative_rates"]
    assert bohr["verdict"]["chain_number_supplies_correct_common_Bohr_grading"]
    assert bohr["directed_chain_number_QMS"]["both_orientations_are_primitive_KMS_processes"]
    assert orientation["remaining_boundary"]["dimensionless_orientation_selected"]
    assert not orientation["remaining_boundary"]["physical_time_unit_selected"]
    assert not orientation["remaining_boundary"]["physical_energy_unit_selected"]
    assert not rates["verdict"]["unique_relative_rate_metric_derived"]
    assert not kernel["verdict"]["current_project_supplies_independent_physical_full_kernel"]
    assert action["verdict"]["same_action_can_have_different_physical_kernels"]
    assert not mobility["verdict"]["single_six_family_mobility_derived"]
    assert not frame["status_boundary"]["trace_isotropy_forced_by_physical_symmetry"]
    assert not symmetry["verdict"]["physical_symmetry_forces_trace_isotropy"]

    # The two modular branches are exactly reciprocal.  The fixed Hodge sign
    # chooses compatibility with one branch, but reciprocity itself contains
    # no dimensional energy or time calibration.
    beta_delta = sp.Integer(2)
    forward_ratio = sp.exp(-beta_delta)
    reverse_ratio = sp.exp(beta_delta)
    reciprocal_residual = sp.simplify(forward_ratio * reverse_ratio - 1)
    assert reciprocal_residual == 0

    kappa = sp.Symbol("kappa", positive=True)
    eigenvalue = sp.Symbol("lambda")
    scale_zero_equivalence = sp.solve(sp.Eq(kappa * eigenvalue, 0), eigenvalue)
    assert scale_zero_equivalence == [0]

    mathematical_closure = {
        "typed_finite_dimensional_generator": True,
        "complete_positivity_certificate": True,
        "scalar_fixed_algebra": True,
        "dimensionless_semigroup": True,
        "common_dimensionless_Bohr_grading": True,
        "orientation_compatible_with_fixed_Hodge_parent": True,
        "status": "operator_algebraic_process_class_closed",
    }
    physical_requirements = {
        "unique_relative_rate_metric": False,
        "absolute_time_scale": False,
        "physical_energy_or_temperature_calibration": False,
        "autonomous_environment_or_fresh_ancilla_supply": False,
        "microscopic_system_bath_coupling_or_spectral_density": False,
        "independent_physical_correlation_kernel": False,
        "symmetry_forced_noise_metric": False,
        "preregistered_empirical_observable": False,
    }
    failed_requirements = [
        name for name, satisfied in physical_requirements.items() if not satisfied
    ]
    physical_closure = all(physical_requirements.values())
    assert not physical_closure
    assert len(failed_requirements) == 8

    source_names = [
        "s2t_v8_intrinsic_noise_clock_dilation_gate_results.json",
        "s2t_v8_full_primitive_markov_generator_assembly_gate_results.json",
        "s2t_v8_kms_nontracial_relative_rate_selector_gate_results.json",
        "s2t_v8_modular_bohr_parent_origin_gate_results.json",
        "s2t_v8_chain_orientation_index_defect_selector_gate_results.json",
        "s2t_v8_common_chain_dirichlet_rate_metric_gate_results.json",
        "s2t_v8_correlation_kernel_short_time_rate_selector_gate_results.json",
        "s2t_v8_physical_correlation_kernel_parent_action_origin_gate_results.json",
        "s2t_v8_fluctuation_dissipation_mobility_origin_gate_results.json",
        "s2t_v8_canonical_noise_frame_common_trace_gate_results.json",
        "s2t_v8_noise_isotropy_symmetry_admission_gate_results.json",
    ]

    result = {
        "date": "2026-08-29",
        "gate": "version8_dynamic_physical_closure_redteam_gate",
        "audit_rule": (
            "A unique physical dynamics requires a typed generator, unique relative "
            "rates, dimensional energy and time calibration, a non-circular microscopic "
            "environment or correlation kernel, a symmetry-derived noise metric, and a "
            "preregistered observable."
        ),
        "exact_invariance_checks": {
            "forward_ratio": "exp(-2)",
            "reverse_ratio": "exp(2)",
            "forward_times_reverse": "1",
            "positive_generator_rescaling_preserves_zero_eigenspace": True,
            "interpretation": (
                "The fixed Hodge sign selects an internal orientation convention, while "
                "the operator process still lacks dimensional rate and bath calibration."
            ),
        },
        "mathematical_closure": mathematical_closure,
        "physical_closure_requirements": physical_requirements,
        "failed_physical_requirements": failed_requirements,
        "counts": {
            "physical_requirements": len(physical_requirements),
            "failed_physical_requirements": len(failed_requirements),
        },
        "source_artifacts": {
            name: sha256(RESULTS / name) for name in source_names
        },
        "verdict": {
            "mathematical_program_in_dead_end": False,
            "unique_physical_dynamics_closed": physical_closure,
            "selector_chasing_risk": True,
            "lcf_migration_may_continue_as_audit": True,
            "new_physical_selector_allowed_without_microscopic_input": False,
            "status": "mathematical_process_positive_physical_dynamic_closure_no_go",
            "next_gate": (
                "microscopic_system_bath_spectral_density_or_preregistered_observable_gate"
            ),
        },
    }

    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["verdict"], ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()