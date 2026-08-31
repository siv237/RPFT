#!/usr/bin/env python3
"""Verify the finite Page--Wootters/Stinespring history bridge in the LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_page_wootters_stinespring_history_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_page_wootters_history import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.steps == 2
    assert certificate.clock_dimension == 3
    assert certificate.system_dimension == 21
    assert certificate.environment_dimension_per_tick == 13
    assert certificate.branch_count_bounds == (1, 13, 169)
    assert certificate.padded_data_dimension == 3549
    assert certificate.full_history_dimension == 10647
    assert certificate.recovery_theorem.proposition.data["slice_traces"] == (
        "1",
        "1",
        "1",
    )
    assert certificate.history_parent_theorem.proposition.data[
        "zero_mode_family_dimension"
    ] == 21
    assert certificate.extension_freedom_theorem.proposition.data[
        "unconstrained_complement_dimension"
    ] == 252
    assert certificate.extension_freedom_theorem.proposition.data[
        "extension_real_parameter_dimension"
    ] == 63504
    assert certificate.collision_limit_theorem.proposition.data["scaling"] == "p=u/n"

    old_stinespring = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_minimal_covariant_stinespring_lcf_migration_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    old_clock = json.loads(
        (
            ROOT / "s2t/results/s2t_v8_intrinsic_noise_clock_lcf_migration_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert old_stinespring["one_step_channel"]["minimal_environment_dimension"] == 13
    assert old_clock["collision_limit"]["rule"] == "p=u/n"
    assert old_clock["verdict"]["physical_clock_rate_still_open"]

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"] == "version8_page_wootters_stinespring_history_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 5

    result = {
        "date": "2026-08-29",
        "gate": "version8_page_wootters_stinespring_history_gate",
        "finite_history": {
            "benchmark_step": "p=1/12",
            "clock_readings": [0, 1, 2],
            "clock_dimension": certificate.clock_dimension,
            "system_dimension": certificate.system_dimension,
            "environment_dimension_per_tick": certificate.environment_dimension_per_tick,
            "kraus_branch_count_bounds": list(certificate.branch_count_bounds),
            "padded_data_dimension": certificate.padded_data_dimension,
            "full_clock_data_dimension": certificate.full_history_dimension,
            "all_conditional_slice_residuals": "zero",
            "all_conditional_slice_traces": ["1", "1", "1"],
            "conditioned_reduced_state": "rho_n=Phi_*^n(rho_0)",
        },
        "stationary_parent": {
            "frustration_free_isometric_history_parent_exists": True,
            "global_history_stationary": True,
            "zero_mode_family_dimension": 21,
            "additive_H_clock_plus_H_system_constraint_derived": False,
        },
        "unitary_extension_boundary": {
            "stinespring_isometry": "C21 -> C21 tensor C13 = C273",
            "unconstrained_complement_dimension": 252,
            "extension_family": "U(252)",
            "extension_real_parameter_dimension": 63504,
            "canonical_full_unitary_tick_derived": False,
        },
        "continuum_bridge": {
            "fresh_ancilla_scaling": "p=u/n",
            "operator_norm_limit": "Phi_(u/n)^n -> exp(u L_cross)",
            "finite_history_and_collision_limit_are_compatible": True,
            "autonomous_fresh_ancilla_supply_derived": False,
            "physical_time_scale_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "gate_count": registry["gate_count"],
            "total_obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][
                "version8_page_wootters_stinespring_history_gate"
            ],
        },
        "verdict": {
            "finite_conditional_history_bridge_obtained": True,
            "stationary_isometric_history_parent_obtained": True,
            "full_autonomous_page_wootters_clock_derived": False,
            "continuous_dimensionless_limit_inherited": True,
            "physical_second_or_arrow_derived": False,
            "status": "lcf_checked_finite_history_bridge_autonomous_physical_clock_open",
            "next_gate": "canonical_autonomous_clock_unitary_extension_no_go_or_origin_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()