#!/usr/bin/env python3
"""Exact and ProofDSL audit of the minimal KMS logdet auxiliary fermion module."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_auxiliary_fermion_module_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_auxiliary_fermion_module_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_relative_shape_logdet_parent_"
        "measure_origin_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10
    assert certificate.auxiliary_operator.shape == (10, 10)
    assert certificate.berezin_pairing.shape == (20, 20)
    assert certificate.berezin_pairing.rank() == 20
    assert certificate.package_theta + certificate.package_kappa == sp.eye(10)
    assert certificate.package_theta * certificate.package_kappa == sp.zeros(10)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "canonical_auxiliary_carrier": {
            "formula": "Pi(V_type tensor P_KMS)",
            "type_carrier": "C_s direct_sum C_a direct_sum C_t^3",
            "type_dimension": 5,
            "type_multiplicities": [1, 1, 3],
            "package_carrier": "C_theta direct_sum C_kappa",
            "package_dimension": 2,
            "complex_dimension": 10,
            "parity": "purely odd",
            "physical_state_increment": 0,
        },
        "quadratic_operator": {
            "formula": "D_aux=R_theta direct_sum R_kappa",
            "complex_shape": [10, 10],
            "determinant": (
                "theta_s theta_a theta_t^3 "
                "kappa_s kappa_a kappa_t^3"
            ),
            "total_homogeneous_degree": 10,
            "family_triplet_covariant": True,
            "package_exchange_covariant": True,
            "even_under_auxiliary_parity": True,
        },
        "berezin_completion": {
            "independent_complex_pairs": 10,
            "independent_odd_coordinates": 20,
            "antisymmetric_pairing_shape": [20, 20],
            "antisymmetric_pairing_rank": 20,
            "complex_conjugate_pairing_required": True,
        },
        "physical_decoupling": {
            "physical_creation_cell_dimension": 6,
            "total_superconfiguration_dimension": "6 even physical + 10 odd auxiliary",
            "off_diagonal_physical_auxiliary_block": 0,
            "auxiliary_operator_annihilates_physical_inclusion": True,
            "new_physical_endpoint_states": 0,
            "qms_state_space_unchanged": True,
        },
        "origin_audit": {
            "type_carrier_inherited": True,
            "two_package_index_inherited": True,
            "ungraded_carrier_functorial": True,
            "odd_statistics_derived_from_parent": False,
            "berezin_measure_orientation_derived": False,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "the kernel checks carrier, grading, symmetry, determinant and "
                "decoupling; Grassmann statistics and Berezin integration remain "
                "external structural input"
            ),
        },
        "ledgers": {
            "auxiliary_module_architecture_satisfied": 10,
            "auxiliary_module_architecture_tested": 10,
            "functorial_ungraded_carrier_origin_satisfied": 2,
            "functorial_ungraded_carrier_origin_tested": 2,
            "odd_statistics_origin_satisfied": 0,
            "odd_statistics_origin_tested": 1,
            "berezin_measure_origin_satisfied": 0,
            "berezin_measure_origin_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "minimal_auxiliary_module_admitted": True,
            "module_is_functorial_from_existing_typed_data": True,
            "module_adds_physical_states": False,
            "odd_statistics_physically_derived": False,
            "berezin_measure_physically_derived": False,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_auxiliary_fermion_"
            "statistics_parent_origin_gate"
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