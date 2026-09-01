#!/usr/bin/env python3
"""Exact and ProofDSL audit of the parent origin of auxiliary KMS statistics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_auxiliary_fermion_statistics_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_auxiliary_fermion_statistics_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "module_admission_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10

    negative_ranks = [
        sum(1 for value in grading.diagonal() if value == -1)
        for grading in certificate.candidate_gradings
    ]
    assert negative_ranks == [2, 5, 5, 8]
    assert certificate.target_grading == -sp.eye(10)
    assert certificate.closest_defect.rank() == 2

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "inherited_gradings": {
            "physical_type_grading": [1, -1, 1, 1, 1],
            "physical_type_even_rank": 4,
            "physical_type_odd_rank": 1,
            "package_sign_choices": [[1, 1], [1, -1], [-1, 1], [-1, -1]],
            "resulting_odd_ranks": negative_ranks,
            "target_odd_rank": 10,
            "target_reached": False,
        },
        "package_exchange": {
            "mixed_sign_choices_covariant": False,
            "equal_sign_choices_covariant": True,
            "swap_covariant_odd_ranks": [2, 8],
            "target_odd_rank": 10,
        },
        "closest_inherited_candidate": {
            "package_signs": [-1, -1],
            "odd_rank": 8,
            "even_defect_rank": 2,
            "defect_channels": ["theta_a", "kappa_a"],
            "required_fix": "component-specific parity flip or constant all-odd seed",
            "fix_is_inherited": False,
        },
        "origin_candidates": [
            {
                "candidate": "physical type grading tensor uniform package parity",
                "origin_pass": False,
                "reason": "odd ranks are only 2,5,5,8",
            },
            {
                "candidate": "declare both package lines odd and ignore type grading",
                "origin_pass": False,
                "reason": "the odd package declaration is the missing statistics seed",
            },
            {
                "candidate": "constant all-odd grading -I10",
                "origin_pass": False,
                "reason": "valid architecture but tautological parity seed",
            },
            {
                "candidate": "Real conjugation J",
                "origin_pass": False,
                "reason": "antilinear conjugation does not assign Grassmann parity",
            },
            {
                "candidate": "KMS modular or transport orientation",
                "origin_pass": False,
                "reason": "orders/reverses channels but supplies no ghost number",
            },
            {
                "candidate": "existing BRST/BV gauge differential",
                "origin_pass": False,
                "reason": "no gauge map or nilpotent differential acts on G_aux",
            },
        ],
        "conditional_measure_closure": {
            "all_odd_grading_is_valid_involution": True,
            "paired_basis_jacobian": "det(S) det(S^-1)=1",
            "paired_berezin_density_basis_covariant": True,
            "overall_measure_normalization_changes_action_by_additive_constant": True,
            "independent_measure_orientation_parameter_after_odd_choice": False,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "the kernel checks all inherited grading spectra and paired "
                "Jacobian cancellation; the physical BRST/BV origin of parity is absent"
            ),
        },
        "ledgers": {
            "statistics_origin_candidates_satisfied": 0,
            "statistics_origin_candidates_tested": 6,
            "conditional_all_odd_grading_satisfied": 1,
            "conditional_all_odd_grading_tested": 1,
            "paired_measure_covariance_satisfied": 1,
            "paired_measure_covariance_tested": 1,
            "independent_measure_orientation_freedom": 0,
            "unresolved_statistics_data": 1,
            "proofdsl_obligations_satisfied": 10,
            "proofdsl_obligations_tested": 10,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "inherited_grading_selects_all_odd_module": False,
            "constant_all_odd_grading_conditionally_valid": True,
            "berezin_pair_measure_is_basis_covariant": True,
            "measure_orientation_is_independent_physical_input": False,
            "odd_statistics_physically_derived": False,
            "minimal_brst_complex_required": True,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_minimal_brst_complex_"
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