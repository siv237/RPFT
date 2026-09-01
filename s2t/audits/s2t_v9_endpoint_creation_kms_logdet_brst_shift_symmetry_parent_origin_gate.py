#!/usr/bin/env python3
"""Exact and ProofDSL audit of the parent origin of the KMS BRST shift orbit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_brst_shift_symmetry_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_brst_shift_symmetry_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_logdet_minimal_brst_"
        "complex_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10
    assert certificate.required_shift_map.rank() == 10
    assert certificate.kms_parameter_tangent.rank() == 6
    assert len(certificate.kms_parameter_tangent.T.nullspace()) == 4
    assert certificate.normalized_shape_tangent.rank() == 4
    assert len(certificate.phase_laplacian.nullspace()) == 1

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "required_gauge_orbit": {
            "transformation": "x -> x + epsilon",
            "parameter_space": "V_type tensor P_KMS",
            "complex_dimension": 10,
            "generator_map": "I10",
            "rank": 10,
        },
        "inherited_continuous_directions": {
            "all_six_kms_type_parameters_rank": 6,
            "all_six_kms_type_parameters_cokernel": 4,
            "normalized_relative_shapes_rank": 4,
            "endpoint_phase_zero_modes": 1,
            "type_conjugation_orbit_rank_on_scalar_blocks": 0,
            "transport_continuous_tangent_rank": 0,
            "maximum_relevant_inherited_rank": 6,
            "required_rank": 10,
            "rank_deficit": 4,
        },
        "parent_hessian_audit": {
            "trivial_spectator_extension_hessian_rank": 0,
            "trivial_extension_has_full_translation_symmetry": True,
            "trivial_extension_is_parent_derived": False,
            "positive_auxiliary_quadratic_hessian_rank": 10,
            "positive_auxiliary_quadratic_preserves_full_shift": False,
            "fp_operator_can_appear_only_in_gauge_fixing_not_bare_shift_invariant_action": True,
        },
        "origin_candidates": [
            {
                "candidate": "six KMS type parameters",
                "origin_pass": False,
                "reason": "rank 6 with cokernel 4",
            },
            {
                "candidate": "four normalized relative shapes",
                "origin_pass": False,
                "reason": "rank 4 and they are physical parameters not gauge directions",
            },
            {
                "candidate": "endpoint phase zero mode",
                "origin_pass": False,
                "reason": "nullity 1 rather than 10",
            },
            {
                "candidate": "type and family conjugations",
                "origin_pass": False,
                "reason": "scalar isotypic blocks have orbit rank 0",
            },
            {
                "candidate": "transport orientation",
                "origin_pass": False,
                "reason": "discrete choice has tangent rank 0",
            },
            {
                "candidate": "zero-action spectator extension",
                "origin_pass": False,
                "reason": "full shift exists only because the new field was declared absent from the parent",
            },
        ],
        "conditional_shift_extension": {
            "formula": "S0(R,x)=S_invariant(R)",
            "full_shift_symmetry": True,
            "shift_rank": 10,
            "bounded_below_if_original_parent_bounded_below": True,
            "flat_direction_dimension": 10,
            "target_loaded_zero_coupling": True,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "the kernel checks tangent ranks and translation breaking; deciding "
                "whether a new spectator field is physically mandatory is outside LCF"
            ),
        },
        "ledgers": {
            "shift_origin_candidates_satisfied": 0,
            "shift_origin_candidates_tested": 6,
            "conditional_zero_action_shift_satisfied": 1,
            "conditional_zero_action_shift_tested": 1,
            "fp_operator_origin_satisfied": 1,
            "fp_operator_origin_tested": 1,
            "shift_gauge_symmetry_origin_satisfied": 0,
            "shift_gauge_symmetry_origin_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "existing_parent_has_required_ten_dimensional_gauge_orbit": False,
            "conditional_trivial_shift_extension_exists": True,
            "conditional_extension_is_physical_origin": False,
            "positive_bare_parent_can_preserve_full_shift": False,
            "minimal_stueckelberg_architecture_required": True,
            "logdet_parent_physically_derived": False,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_logdet_minimal_stueckelberg_"
            "shift_parent_architecture_gate"
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