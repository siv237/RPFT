#!/usr/bin/env python3
"""Exact ProofDSL audit of KMS reservoir spectral-density origin."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version9_kms_reservoir_spectral_density_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_keldysh_"
        "influence_functional_admission_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate
    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert len(verified.obligations) == 12

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "spectral_profiles": {
            "interval": [0, 4],
            "gaps": [1, 2, 3],
            "baseline": "J0(omega)=1",
            "deformation": "q=(omega-1)^2(omega-2)^2(omega-3)^2",
            "perturbed": "J1(omega)=1+q/16",
            "both_positive": True,
        },
        "on_shell_map": {
            "polynomial_dimension": 7,
            "evaluation_rank": 3,
            "evaluation_nullity": 4,
            "baseline_rates": [1, 1, 1],
            "perturbed_rates": [1, 1, 1],
            "weighted_normalization": 5,
            "one_rate_normalization_rank": 1,
            "relative_type_strength_freedom": 2,
        },
        "off_shell_witness": {
            "baseline_zeroth_moment": 4,
            "perturbed_zeroth_moment": "527/105",
            "zeroth_moment_defect": "107/105",
            "baseline_first_moment": 8,
            "perturbed_first_moment": "1054/105",
            "first_moment_defect": "214/105",
            "same_rates_different_self_energy_asymptotics": True,
            "same_rates_determine_bath_logdet": False,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "Global positivity follows from the displayed square profile; "
                "the exact certificate checks sampling, moments and asymptotic coefficients"
            ),
        },
        "ledgers": {
            "positive_reservoir_profiles_satisfied": 2,
            "positive_reservoir_profiles_tested": 2,
            "equal_on_shell_conductances_satisfied": 3,
            "equal_on_shell_conductances_tested": 3,
            "unique_off_shell_spectral_density_satisfied": 0,
            "unique_off_shell_spectral_density_tested": 1,
            "conductances_determine_logdet_satisfied": 0,
            "conductances_determine_logdet_tested": 1,
            "reservoir_spectral_density_parent_origin_satisfied": 0,
            "reservoir_spectral_density_parent_origin_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "on_shell_rates_can_be_reproduced": True,
            "spectral_density_is_unique_from_rates": False,
            "off_shell_self_energy_is_unique_from_rates": False,
            "bath_logdet_is_unique_from_rates": False,
            "reservoir_parent_origin_derived": False,
            "physical_logdet_parent_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_reservoir_measure_"
            "anomaly_parent_origin_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()