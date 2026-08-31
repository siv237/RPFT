#!/usr/bin/env python3
"""Migrate the intrinsic noise-clock gate to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_intrinsic_noise_clock_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_noise_clock import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.kernel_dimension == 46
    assert certificate.unit_gap == sp.Rational(1, 2)
    assert certificate.maximum_decay == 8
    assert certificate.dissipative_projector_norm_squared == 72
    assert sum(multiplicity for _, multiplicity in certificate.spectrum) == 221

    old = json.loads(
        (ROOT / "s2t/results/s2t_v8_intrinsic_noise_clock_dilation_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    assert old["dimensionless_semigroup"]["cross_generator_kernel_dimension"] == 46
    assert abs(old["dimensionless_semigroup"]["unit_rate_smallest_nonzero_decay"] - 0.5) < 1e-12
    assert abs(old["dimensionless_semigroup"]["unit_rate_largest_decay"] - 8.0) < 1e-12
    assert old["fresh_ancilla_collision_limit"]["continuous_limit_recovered"]

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"] == "version8_intrinsic_noise_clock_dilation_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 8

    result = {
        "date": "2026-08-29",
        "gate": "version8_intrinsic_noise_clock_lcf_migration_gate",
        "exact_dimensionless_semigroup": {
            "formula": "T_u=exp(u L_cross)",
            "endpoint_operator_dimension": 221,
            "decay_spectrum": [
                {"eigenvalue": str(value), "multiplicity": multiplicity}
                for value, multiplicity in certificate.spectrum
            ],
            "kernel_dimension": 46,
            "unit_rate_gap": "1/2",
            "unit_rate_maximum_decay": "8",
            "positive_rate_rescaling_preserves_kernel": True,
            "physical_rate_kappa_derived": False,
        },
        "modular_time_no_go": {
            "uniform_modular_action_on_sector_projectors": "zero",
            "faithful_central_modular_action_on_sector_projectors": "zero",
            "cross_dissipative_projector_motion_norm_squared": "72",
            "modular_flow_reproduces_cross_dissipation": False,
        },
        "collision_limit": {
            "rule": "p=u/n",
            "convergence": "operator norm by finite-dimensional Chernoff product rule",
            "fresh_13_dimensional_environment_each_step": True,
            "dimensionless_semigroup_recovered": True,
            "fresh_environment_supply_derived": False,
            "physical_tick_duration_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_intrinsic_noise_clock_dilation_gate"
            ],
        },
        "verdict": {
            "dimensionless_noise_time_lcf_checked": True,
            "physical_clock_rate_still_open": True,
            "status": "lcf-checked-dimensionless-time-physical-rate-open",
            "next_gate": "version8_full_primitive_markov_generator_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()