#!/usr/bin/env python3
"""Точный аудит концевого допуска минимальной симплектической достройки."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.completed_complex_dimension == 26
    assert certificate.completed_real_dimension == 52
    assert certificate.invariant_form_dimension == 23
    assert certificate.standard_form.rank() == 26
    assert certificate.standard_form.T == -certificate.standard_form
    assert certificate.standard_form * (-certificate.standard_form) == sp.eye(26)
    assert certificate.standard_form != certificate.alternative_form
    assert certificate.endpoint_multiplicity_deficit == 3
    assert certificate.new_complex_directions == 6
    assert certificate.first_field.T * certificate.standard_form * certificate.second_field == sp.ones(1, 1)
    assert not certificate.standard_form.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate"
    )
    assert len(gate["obligations"]) == 15
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "formal_completion": {
            "decomposition": "4 H_plus + 4 H_minus + C_plus + C_minus + 4 S_zero",
            "complex_dimension": certificate.completed_complex_dimension,
            "real_dimension": certificate.completed_real_dimension,
            "invariant_alternating_form_dimension": certificate.invariant_form_dimension,
            "standard_form_rank": certificate.standard_form.rank(),
            "standard_form_determinant": int(certificate.standard_form.det()),
            "gauge_generator_checks": len(certificate.gauge_generators),
            "nondegenerate_invariant_form_exists": True,
            "unique_form_selected": False,
        },
        "endpoint_origin": {
            "current_H_plus_multiplicity": certificate.current_positive_weak_multiplicity,
            "required_H_plus_multiplicity": certificate.required_positive_weak_multiplicity,
            "multiplicity_deficit": certificate.endpoint_multiplicity_deficit,
            "new_complex_directions": certificate.new_complex_directions,
            "new_real_directions": 2 * certificate.new_complex_directions,
            "derived_from_current_endpoint_carrier": False,
            "requires_new_cotangent_arrow_data": True,
            "requires_new_fermions_if_realized_as_new_endpoints": "not_decided",
        },
        "phase_pairing": {
            "single_bosonic_self_contraction": 0,
            "two_independent_field_witness": 1,
            "physical_horizontal_phase_lift": False,
            "reason": "the required dual fields are not endpoint-derived",
        },
        "verdict": {
            "abstract_balanced_symplectic_carrier_admitted": True,
            "existing_endpoint_realization_admitted": False,
            "canonical_polarization_admitted": False,
            "current_parent_extended": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()