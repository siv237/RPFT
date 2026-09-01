#!/usr/bin/env python3
"""Exact and ProofDSL audit of possible measure origins of the KMS logdet parent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_logdet_measure_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_relative_shape_logdet_parent_measure_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_relative_shape_selector_source_"
        "minimal_invariant_parent_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10

    rs, ra, rt = sp.symbols("r_s r_a r_t", positive=True)
    determinant = rs * ra * rt**3
    assert sp.Poly(determinant, rs, ra, rt).total_degree() == 5
    assert certificate.doubled_operator.shape == (10, 10)

    u, v = sp.symbols("u v", real=True)
    z = sp.exp(u) + sp.exp(v) + 3
    chart_rs, chart_ra, chart_rt = 5 * sp.exp(u) / z, 5 * sp.exp(v) / z, 5 / z
    chart_jacobian = sp.det(sp.Matrix([
        [sp.diff(chart_rs, u), sp.diff(chart_rs, v)],
        [sp.diff(chart_ra, u), sp.diff(chart_ra, v)],
    ]))
    assert sp.simplify(chart_jacobian - sp.Rational(3, 5) * chart_rs * chart_ra * chart_rt) == 0
    assert sp.simplify(
        (chart_rs * chart_ra * chart_rt**3) / chart_jacobian
        - sp.Rational(5, 3) * chart_rt**2
    ) == 0

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "target_parent": {
            "single_package": "-log det R",
            "two_packages": "-log det R_theta-log det R_kappa",
            "type_multiplicities": [1, 1, 3],
        },
        "measure_candidates": [
            {
                "candidate": "flat Lebesgue measure",
                "effective_logdet_coefficient": 0,
                "target_sign_and_coefficient": False,
            },
            {
                "candidate": "real bosonic Gaussian",
                "effective_logdet_coefficient": "1/2",
                "target_sign_and_coefficient": False,
            },
            {
                "candidate": "complex bosonic Gaussian",
                "effective_logdet_coefficient": 1,
                "target_sign_and_coefficient": False,
            },
            {
                "candidate": "complex fermionic Berezin Gaussian",
                "effective_logdet_coefficient": -1,
                "target_sign_and_coefficient": True,
            },
            {
                "candidate": "Majorana Pfaffian Gaussian",
                "effective_logdet_coefficient": "-1/2",
                "target_sign_and_coefficient": False,
            },
            {
                "candidate": "log-ratio coordinate Jacobian",
                "effective_logdet_coefficient": "nonmatching multiplicity",
                "target_sign_and_coefficient": False,
            },
            {
                "candidate": "Faddeev-Popov ghost determinant",
                "effective_logdet_coefficient": -1,
                "target_sign_and_coefficient": "conditional on an absent gauge Jacobian R",
            },
        ],
        "conditional_fermionic_representation": {
            "identity": "integral exp(-bar(psi) R psi) = det R",
            "effective_action": "-log Z_F(R) = -log det R",
            "minimal_complex_pairs_per_package": 5,
            "minimal_complex_pairs_two_packages": 10,
            "block_operator": "R_theta direct_sum R_kappa",
            "block_determinant_factorization": True,
            "coefficient_one_requires_one_copy_per_package": True,
        },
        "coordinate_measure_no_go": {
            "chart": "r=5(exp(u),exp(v),1)/(exp(u)+exp(v)+3)",
            "jacobian": "(3/5) r_s r_a r_t",
            "target_determinant": "r_s r_a r_t^3",
            "target_to_jacobian_ratio": "(5/3) r_t^2",
            "ratio_nonconstant": True,
        },
        "carrier_audit": {
            "existing_creation_cell_complex_dimension": 6,
            "existing_typed_grassmann_auxiliary_module": False,
            "existing_gauge_map_with_jacobian_R": False,
            "new_auxiliary_module_required": True,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "Berezin and ordinary Gaussian integration identities are external "
                "lemmas; ProofDSL checks their determinant/sign consequences"
            ),
        },
        "ledgers": {
            "measure_candidate_classes_satisfied": 1,
            "measure_candidate_classes_tested": 7,
            "conditional_measure_representation_satisfied": 1,
            "conditional_measure_representation_tested": 1,
            "proofdsl_obligations_satisfied": 10,
            "proofdsl_obligations_tested": 10,
            "inherited_measure_origin_satisfied": 0,
            "inherited_measure_origin_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "correct_measure_mechanism_identified": True,
            "minimal_auxiliary_dimension_derived": True,
            "coordinate_jacobian_origin_excluded": True,
            "existing_carrier_supplies_required_auxiliary_fields": False,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_auxiliary_fermion_module_"
            "admission_gate"
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