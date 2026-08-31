#!/usr/bin/env python3
"""Migrate the minimal cross-arrow Stinespring carrier to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_minimal_covariant_stinespring_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_stinespring import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    expected_spectrum = ((0, 9), (1, 6), (2, 3), (3, 2), (6, 1))
    assert certificate.gram_spectrum == expected_spectrum
    assert certificate.maximum_step == sp.Rational(1, 6)
    assert certificate.benchmark_step == sp.Rational(1, 12)
    assert certificate.endpoint_theorem.proposition.data["checked_matrix_units"] == 221
    assert certificate.interior_rank_theorem.proposition.data["rank"] == 13
    assert certificate.minimal_environment_theorem.proposition.data[
        "environment_dimension"
    ] == 13
    assert certificate.covariance_theorem.proposition.data[
        "environment_jump_dimension"
    ] == 12
    assert certificate.tangent_theorem.proposition.data["jump_count"] == 12

    old_path = ROOT / "s2t/results/s2t_v8_minimal_covariant_stinespring_carrier_gate_results.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    old_spectrum = old["cross_jump_space"]["sum_Da_squared_spectrum"]
    expanded = [value for value, multiplicity in expected_spectrum for _ in range(multiplicity)]
    assert old_spectrum == [float(value) for value in expanded]
    assert old["one_step_channel"]["kraus_rank_at_positive_interior_step"] == 13
    assert old["one_step_channel"]["minimal_environment_dimension"] == 13
    assert old["one_step_channel"]["allowed_step_interval"][1] == float(sp.Rational(1, 6))

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"] == "version8_minimal_covariant_stinespring_carrier_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 11

    result = {
        "date": "2026-08-29",
        "gate": "version8_minimal_covariant_stinespring_lcf_migration_gate",
        "exact_cross_jump_space": {
            "system_dimension": 21,
            "real_jump_dimension": 12,
            "hilbert_schmidt_gram": "2 I_12",
            "gram_spectrum_with_multiplicity": [
                {"eigenvalue": value, "multiplicity": multiplicity}
                for value, multiplicity in expected_spectrum
            ],
        },
        "one_step_channel": {
            "formula": "K0=sqrt(I-pG), Ka=sqrt(p)Da",
            "exact_step_interval": ["0", "1/6"],
            "benchmark_step": "1/12",
            "completely_positive": True,
            "unital": True,
            "trace_preserving": True,
            "endpoint_matrix_units_checked": 221,
            "endpoint_algebra_invariant": True,
            "positive_interior_kraus_rank": 13,
            "choi_rank": 13,
            "minimal_environment_dimension": 13,
            "environment_decomposition": "C vacuum direct_sum complexification of the 12-real cross frame",
            "new_physical_particle_required": False,
        },
        "covariance_and_continuous_time_boundary": {
            "gauge_covariance_from_exact_orthogonal_frame": True,
            "tangent_at_zero_is_cross_gksl_generator": True,
            "finite_family_is_exact_semigroup": False,
            "exact_counterexample": "Phi_(1/50) o Phi_(3/100) != Phi_(1/20)",
            "physical_step_or_rate_derived": False,
            "autonomous_continuous_time_dilation_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_minimal_covariant_stinespring_carrier_gate"
            ],
        },
        "verdict": {
            "minimal_one_step_dilation_lcf_checked": True,
            "continuous_noise_time_still_open": True,
            "status": "lcf-checked-one-step-continuous-time-open",
            "next_gate": "version8_intrinsic_noise_clock_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()