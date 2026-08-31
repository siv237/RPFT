#!/usr/bin/env python3
"""Точный аудит комплексной симплектической поляризации."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_complex_symplectic_polarization_admission_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_complex_symplectic_polarization_admission import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.invariant_form_dimension == 11
    assert certificate.maximum_invariant_rank == 14
    assert certificate.minimum_radical_dimension == 6
    assert certificate.first_invariant_form.rank() == 14
    assert certificate.generic_invariant_form.rank() == 14
    assert certificate.generic_invariant_form.nullspace().__len__() == 6
    assert certificate.first_invariant_form.T == -certificate.first_invariant_form
    assert certificate.first_invariant_form != certificate.second_invariant_form
    assert certificate.missing_dual_complex_dimension == 6
    assert certificate.completed_complex_dimension == 26
    assert not certificate.generic_invariant_form.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_phase_complex_symplectic_polarization_admission_gate"
    )
    assert len(gate["obligations"]) == 13
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "typed_transfer_representation": {
            "decomposition": "H_plus + 4 H_minus + C_plus + C_minus + 4 S_zero",
            "irrep_dimensions": {"H": 2, "C": 3, "S_zero": 1},
            "complex_dimension": 20,
            "gauge_generator_checks": len(certificate.gauge_generators),
        },
        "invariant_alternating_forms": {
            "linear_system_shape": list(certificate.invariance_system.shape),
            "dimension": certificate.invariant_form_dimension,
            "maximum_rank": certificate.maximum_invariant_rank,
            "minimum_radical_dimension": certificate.minimum_radical_dimension,
            "two_distinct_rank_14_witnesses": True,
            "canonical_form_selected": False,
            "bosonic_self_contraction": 0,
        },
        "minimal_symplectic_completion": {
            "weak_dual_multiplicities_before": [1, 4],
            "missing_dual_complex_directions": certificate.missing_dual_complex_dimension,
            "complex_dimension_after_completion": certificate.completed_complex_dimension,
            "new_endpoint_data_required": True,
        },
        "verdict": {
            "nonzero_invariant_alternating_forms_exist": True,
            "nondegenerate_invariant_symplectic_form_exists": False,
            "unique_polarization_exists": False,
            "single_bosonic_field_produces_quadratic_phase_scalar": False,
            "current_carrier_lifts_horizontal_mode": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()