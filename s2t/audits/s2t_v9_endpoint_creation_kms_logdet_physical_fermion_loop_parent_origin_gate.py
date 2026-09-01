#!/usr/bin/env python3
"""Exact and ProofDSL audit of physical fermion-loop origin for KMS logdet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_physical_fermion_loop_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_physical_fermion_loop_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_logdet_minimal_stueckelberg_"
        "shift_parent_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 11
    assert certificate.target_projector.rank() == 5
    assert certificate.doubled_operator.rank() == 10
    assert certificate.composite_kernel.det() == certificate.doubled_operator.det()

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "physical_carrier": {
            "creation_cell_dimension": 6,
            "configuration_source_dimension": 1,
            "physical_target_multiplet_dimension": 5,
            "type_multiplicities": [1, 1, 3],
            "independent_physical_target_multiplets": 1,
            "linear_determinant_capacity": 1,
            "required_independent_package_determinants": 2,
        },
        "target": {
            "effective_action": "-log det R_theta-log det R_kappa",
            "partition_factor": "det R_theta det R_kappa",
            "gap_determinant": "theta_s theta_a theta_t^3",
            "conductance_determinant": "kappa_s kappa_a kappa_t^3",
            "common_scaling_degree": 10,
        },
        "single_physical_loop": {
            "kernel_dimension": 5,
            "homogeneous_linear_common_scaling_degree": 5,
            "can_supply_both_independent_linear_determinants": False,
            "gap_block_capacity_conditional": True,
            "conductance_is_hamiltonian_bilinear": False,
        },
        "real_pfaffian_audit": {
            "real_lift_dimension": 10,
            "real_lift_determinant": "(det R_theta)^2",
            "physical_pfaffian_half_count": "det R_theta",
            "independent_second_package_created_by_real_doubling": False,
            "generic_exchange_pairing_commutator_rank": 10,
        },
        "conditional_routes": {
            "two_independent_five_channel_fermion_multiplets": {
                "operator": "R_theta direct_sum R_kappa",
                "dimension": 10,
                "target_determinant": True,
                "inherited_second_physical_multiplet": False,
            },
            "single_composite_kernel": {
                "operator": "R_theta R_kappa",
                "dimension": 5,
                "target_determinant": True,
                "mixed_derivative": 1,
                "inherited_multiplicative_bilinear": False,
                "target_loaded": True,
            },
        },
        "candidate_origin_audit": {
            "single_gap_loop": False,
            "single_conductance_loop": False,
            "real_double_as_second_package": False,
            "keldysh_branch_as_second_species": False,
            "two_physical_multiplets": False,
            "composite_product_kernel": False,
            "satisfied": 0,
            "tested": 6,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "ProofDSL checks finite determinant, degree, rank, Real-pairing, "
                "and mixed-kernel identities; functional integration and Keldysh "
                "normalization remain external lemmas"
            ),
        },
        "ledgers": {
            "physical_target_carrier_satisfied": 5,
            "physical_target_carrier_tested": 5,
            "independent_determinant_capacity_satisfied": 1,
            "independent_determinant_capacity_tested": 2,
            "candidate_parent_origin_satisfied": 0,
            "candidate_parent_origin_tested": 6,
            "physical_logdet_parent_satisfied": 0,
            "physical_logdet_parent_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "one_physical_five_channel_loop_is_available": True,
            "one_loop_can_carry_one_degree_five_determinant": True,
            "real_doubling_creates_independent_conductance_loop": False,
            "conductance_block_has_physical_fermion_bilinear_origin": False,
            "algebraic_target_representations_exist": True,
            "algebraic_representation_is_physical_origin": False,
            "physical_fermion_loop_derives_full_target": False,
            "fermionic_bath_or_microscopic_environment_required": True,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_minimal_fermion_bath_"
            "architecture_gate"
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