#!/usr/bin/env python3
"""Exact and ProofDSL audit of the minimal Stueckelberg KMS shift parent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_minimal_stueckelberg_shift_parent import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_minimal_stueckelberg_shift_parent_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_logdet_brst_shift_symmetry_"
        "parent_origin_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10
    assert certificate.orbit_map.rank() == 10
    assert certificate.invariant_map.rank() == 10
    assert certificate.invariant_map * certificate.orbit_map == sp.zeros(10)
    assert certificate.parent_hessian.rank() == 10
    assert len(certificate.parent_hessian.nullspace()) == 10

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "stueckelberg_carrier": {
            "fields": ["x", "y"],
            "dimension_per_field": 10,
            "total_even_dimension": 20,
            "gauge_transformation": "x->x+epsilon, y->y+epsilon",
            "orbit_map": "T=(I10,I10)^T",
            "orbit_rank": 10,
            "invariant_combination": "z=x-y",
            "quotient_dimension": 10,
        },
        "gauge_invariant_parent": {
            "formula": "S_St=(x-y)^T D_aux (x-y)/2",
            "hessian_rank": 10,
            "hessian_nullity": 10,
            "hessian_kernel_equals_gauge_orbit": True,
            "isotropic_spectrum": [[0, 10], [2, 10]],
            "bounded_below": True,
        },
        "gauge_fixing": {
            "condition": "F(x)=D_aux x",
            "fp_operator": "D_aux",
            "fp_rank": 10,
            "fp_determinant": "det R_theta det R_kappa",
            "ghost_determinant_matches_target": True,
        },
        "quotient_obstruction": {
            "gauge_invariant_bosonic_modes": 10,
            "complex_bosonic_partition_factor": "1/det D_aux",
            "ghost_partition_factor": "det D_aux",
            "combined_factor": 1,
            "target_logdet_survives": False,
            "physical_or_auxiliary_quotient_modes_removed": False,
        },
        "minimality": {
            "one_compensator_copy_required": True,
            "smaller_nontrivial_joint_shift_carrier_exists": False,
            "pure_shift_dimension_10_reduces_to_zero_action_spectator": True,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "ProofDSL checks the finite gauge geometry and exact determinant "
                "cancellation; Gaussian path integration is an external lemma"
            ),
        },
        "ledgers": {
            "stueckelberg_gauge_architecture_satisfied": 10,
            "stueckelberg_gauge_architecture_tested": 10,
            "nontrivial_rank_ten_gauge_orbit_satisfied": 1,
            "nontrivial_rank_ten_gauge_orbit_tested": 1,
            "no_new_quotient_modes_satisfied": 0,
            "no_new_quotient_modes_tested": 1,
            "uncancelled_target_logdet_satisfied": 0,
            "uncancelled_target_logdet_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "minimal_stueckelberg_parent_constructed": True,
            "required_shift_orbit_generated_nontrivially": True,
            "gauge_invariant_quotient_is_nonempty": True,
            "bosonic_quotient_cancels_ghost_determinant": True,
            "stueckelberg_route_derives_target_logdet": False,
            "physical_fermion_loop_route_required": True,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_physical_fermion_loop_"
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