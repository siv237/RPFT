#!/usr/bin/env python3
"""Exact and ProofDSL audit of the minimal contractible KMS BRST complex."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_minimal_brst_complex import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_minimal_brst_complex_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "statistics_parent_origin_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10
    q = certificate.brst_differential
    assert q**2 == sp.zeros(40)
    assert q.rank() == 20
    assert len(q.nullspace()) == 20
    assert certificate.fp_operator.rank() == 10

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "brst_quartet": {
            "base_dimension": 10,
            "fields": [
                {"name": "x", "parity": "even", "ghost_number": 0, "dimension": 10},
                {"name": "b", "parity": "even", "ghost_number": 0, "dimension": 10},
                {"name": "c", "parity": "odd", "ghost_number": 1, "dimension": 10},
                {"name": "bar_c", "parity": "odd", "ghost_number": -1, "dimension": 10},
            ],
            "even_dimension": 20,
            "odd_dimension": 20,
            "superdimension": 0,
            "total_auxiliary_dimension": 40,
        },
        "brst_differential": {
            "action": {"s_x": "c", "s_c": 0, "s_bar_c": "b", "s_b": 0},
            "nilpotent": True,
            "rank": 20,
            "nullity": 20,
            "image_dimension": 20,
            "kernel_dimension": 20,
            "cohomology_dimension": 0,
            "raises_ghost_number_by": 1,
            "odd_operator": True,
        },
        "gauge_fixing": {
            "fermion": "Psi=bar_c^T(D_aux x-alpha b/2)",
            "exact_action": "s Psi=b^T D_aux x-alpha b^T b/2-bar_c^T D_aux c",
            "fp_operator": "D_aux=R_theta direct sum R_kappa",
            "fp_rank": 10,
            "fp_determinant": (
                "theta_s theta_a theta_t^3 "
                "kappa_s kappa_a kappa_t^3"
            ),
            "ghost_integral_reproduces_target_logdet": True,
        },
        "physical_decoupling": {
            "physical_creation_dimension": 6,
            "brst_operator_annihilates_physical_inclusion": True,
            "auxiliary_cohomology": 0,
            "new_physical_states": 0,
            "creation_qms_unchanged": True,
        },
        "origin_boundary": {
            "fp_operator_inherited_from_kms_type_operators": True,
            "contractible_quartet_architecture_constructed": True,
            "shift_gauge_redundancy_inherited": False,
            "brst_differential_physically_derived": False,
            "gauge_fixing_fermion_physically_derived": False,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "ProofDSL checks the finite complex and FP determinant; path-integral "
                "gauge independence and physical gauge origin remain external"
            ),
        },
        "ledgers": {
            "minimal_brst_architecture_satisfied": 10,
            "minimal_brst_architecture_tested": 10,
            "contractible_cohomology_satisfied": 1,
            "contractible_cohomology_tested": 1,
            "conditional_fp_determinant_satisfied": 1,
            "conditional_fp_determinant_tested": 1,
            "shift_gauge_symmetry_origin_satisfied": 0,
            "shift_gauge_symmetry_origin_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "minimal_contractible_brst_complex_constructed": True,
            "auxiliary_statistics_generated_by_brst_architecture": True,
            "fp_determinant_matches_logdet_parent": True,
            "auxiliary_complex_changes_physical_cohomology": False,
            "shift_gauge_symmetry_physically_derived": False,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_brst_shift_symmetry_"
            "parent_origin_gate"
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