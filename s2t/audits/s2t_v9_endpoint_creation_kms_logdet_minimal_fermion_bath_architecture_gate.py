#!/usr/bin/env python3
"""Exact and ProofDSL audit of the minimal coupled KMS fermion bath."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_minimal_fermion_bath import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_logdet_physical_fermion_loop_"
        "parent_origin_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 12
    assert certificate.full_kernel.shape == (10, 10)
    assert certificate.coupling_operator.rank() == 5
    assert certificate.stable_witness.det() == 243

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "minimal_carrier": {
            "system_type_dimension": 5,
            "bath_type_dimension": 5,
            "total_fermion_dimension": 10,
            "type_multiplicities": [1, 1, 3],
            "missing_determinant_degree": 5,
            "one_bath_copy_is_degree_minimal": True,
        },
        "coupled_kernel": {
            "formula": "K=[[R_theta,G],[G,R_kappa]]",
            "coupling": "G=diag(g_s,g_a,g_t,g_t,g_t)",
            "coupling_rank": 5,
            "determinant": (
                "(theta_s kappa_s-g_s^2)(theta_a kappa_a-g_a^2)"
                "(theta_t kappa_t-g_t^2)^3"
            ),
            "schur_system_kernel": "R_theta-G R_kappa^-1 G",
            "strictly_positive_when_each_g2_less_than_theta_kappa": True,
        },
        "determinant_comparison": {
            "target": "det R_theta det R_kappa",
            "ratio": (
                "(1-g_s^2/(theta_s kappa_s))"
                "(1-g_a^2/(theta_a kappa_a))"
                "(1-g_t^2/(theta_t kappa_t))^3"
            ),
            "nonzero_stable_coupling_preserves_exact_target": False,
            "zero_coupling_preserves_exact_target": True,
            "zero_coupling_generates_conductance": False,
        },
        "exact_witness": {
            "R_theta": "2 I5",
            "R_kappa": "2 I5",
            "G": "I5",
            "full_spectrum": [[1, 5], [3, 5]],
            "full_determinant": 243,
            "target_determinant": 1024,
            "determinant_defect": 781,
            "target_ratio": "243/1024",
        },
        "architecture": {
            "carrier_and_type_architecture_satisfied": 10,
            "carrier_and_type_architecture_tested": 10,
            "all_channel_active_coupling": True,
            "stable_positive_witness": True,
            "exact_target_at_active_coupling": False,
            "decoupled_bath_is_spectator": True,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "ProofDSL checks exact Schur and determinant identities and a "
                "strict positive witness; the universal stable-cone inequality "
                "and Markov reservoir limit remain external lemmas"
            ),
        },
        "ledgers": {
            "minimal_bath_carrier_architecture_satisfied": 10,
            "minimal_bath_carrier_architecture_tested": 10,
            "nonzero_hermitian_coupling_satisfied": 1,
            "nonzero_hermitian_coupling_tested": 1,
            "active_coupled_target_determinant_satisfied": 0,
            "active_coupled_target_determinant_tested": 1,
            "zero_coupling_target_determinant_satisfied": 1,
            "zero_coupling_target_determinant_tested": 1,
            "joint_conductance_and_logdet_origin_satisfied": 0,
            "joint_conductance_and_logdet_origin_tested": 1,
            "physical_bath_parent_origin_satisfied": 0,
            "physical_bath_parent_origin_tested": 1,
            "physical_logdet_parent_satisfied": 0,
            "physical_logdet_parent_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "minimal_five_channel_bath_carrier_constructed": True,
            "nonzero_type_covariant_coupling_constructed": True,
            "coupled_kernel_is_bounded_below_on_stable_cone": True,
            "coupling_deforms_target_determinant": True,
            "exact_target_requires_zero_hermitian_coupling": True,
            "zero_coupling_bath_generates_rates": False,
            "minimal_hermitian_bath_derives_target_logdet": False,
            "causal_nonhermitian_keldysh_route_required": True,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_keldysh_causal_fermion_"
            "bath_architecture_gate"
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