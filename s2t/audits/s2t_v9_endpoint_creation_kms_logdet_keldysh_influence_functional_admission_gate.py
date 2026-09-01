#!/usr/bin/env python3
"""Exact ProofDSL audit of the normalized KMS Keldysh influence functional."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_keldysh_influence_functional import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_keldysh_influence_functional_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_"
        "fermion_bath_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] in {
        gate,
        "version9_endpoint_creation_kms_logdet_keldysh_causal_fermion_"
        "bath_architecture_gate",
    }
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert len(verified.obligations) == 13
    assert certificate.full_kernel.shape == (10, 10)
    assert certificate.damping_operator.rank() == 5
    assert certificate.keldysh_block.rank() == 5
    assert sp.simplify(certificate.witness_kernel.det()) == 32768

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "causal_kernel": {
            "formula": "K_SK=[[K_R,K_K],[0,K_A]]",
            "retarded": "K_R=R_theta-i R_kappa",
            "advanced": "K_A=R_theta+i R_kappa=K_R^dagger",
            "statistical": "K_K=(K_R-K_A)F=-2 i R_kappa F",
            "lower_left_block_zero": True,
            "damping_rank": 5,
            "noise_rank": 5,
        },
        "determinants": {
            "causal": (
                "(theta_s^2+kappa_s^2)(theta_a^2+kappa_a^2)"
                "(theta_t^2+kappa_t^2)^3"
            ),
            "target": (
                "theta_s theta_a theta_t^3 kappa_s kappa_a kappa_t^3"
            ),
            "keldysh_block_changes_determinant": False,
            "retarded_advanced_pair_equals_target_generically": False,
            "normalized_closed_contour_ratio": 1,
            "normalized_source_free_effective_action": 0,
        },
        "exact_witness": {
            "R_theta": "2 I5",
            "R_kappa": "2 I5",
            "F": "I5/2",
            "causal_determinant": 32768,
            "target_determinant": 1024,
            "determinant_defect": 31744,
            "causal_to_target_ratio": 32,
            "normalized_ratio": 1,
        },
        "admission": {
            "causal_ra_k_architecture_satisfied": 5,
            "causal_ra_k_architecture_tested": 5,
            "kms_fdt_satisfied": 1,
            "kms_fdt_tested": 1,
            "nonzero_dissipative_carrier_satisfied": 1,
            "nonzero_dissipative_carrier_tested": 1,
            "unnormalized_target_logdet_satisfied": 0,
            "unnormalized_target_logdet_tested": 1,
            "normalized_target_logdet_satisfied": 0,
            "normalized_target_logdet_tested": 1,
            "reservoir_markov_origin_satisfied": 0,
            "reservoir_markov_origin_tested": 1,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "ProofDSL checks the exact finite RA/K kernel and normalized "
                "Gaussian ratio; continuum reservoir and Markov limits remain "
                "outside the finite certificate"
            ),
        },
        "verdict": {
            "causal_keldysh_architecture_admitted": True,
            "kms_noise_dissipation_relation_admitted": True,
            "nonzero_conductance_carried": True,
            "triangular_factorization_produces_target_logdet": False,
            "closed_contour_normalization_preserves_target_logdet": False,
            "physical_logdet_parent_derived": False,
            "physical_four_slot_parent_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_reservoir_spectral_"
            "density_parent_origin_gate"
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