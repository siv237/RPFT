#!/usr/bin/env python3
"""Точный аудит котангенциального удвоенного колчанного родителя."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_cotangent_doubled_quiver_parent_admission import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.symplectic_form.rank() == 26
    assert certificate.moment_span_dimension == 13
    assert certificate.moment_span_matrix * certificate.generator_relation == sp.zeros(676, 1)
    assert all(matrix.T == matrix for matrix in certificate.moment_quadratic_matrices)
    assert certificate.cotangent_phase_action.T * certificate.symplectic_form * certificate.cotangent_phase_action == certificate.symplectic_form
    assert not certificate.moment_vector.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate"
    )
    assert len(gate["obligations"]) == 12
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "retrospective": {
            "version3_bf_aksz_pairing": "symplectic bracket without positive metric or selected polarization",
            "version5_derived_moment_map": "preprojective relation without physical positive-star polarization",
            "new_progress": "the 26-dimensional balanced carrier supplies an exact polarization and a nonzero moment map",
        },
        "moment_map": {
            "gauge_generator_count": len(certificate.gauge_generators),
            "independent_component_dimension": certificate.moment_span_dimension,
            "central_relation_count": 1,
            "quadratic_matrices_symmetric": True,
            "nonzero_weak_pair_witness": ["-1"] + ["0"] * 12 + ["-1/2"],
        },
        "cotangent_phase": {
            "symplectic": True,
            "commutes_with_gauge_action": True,
            "all_moment_components_invariant": True,
            "moment_square_parent_invariant": True,
            "horizontal_phase_lifted": False,
        },
        "parent_freedoms": {
            "overall_coupling_selected": False,
            "moment_map_level_selected": False,
            "positive_metric_selected_by_symplectic_form": False,
        },
        "verdict": {
            "formal_doubled_quiver_moment_map_admitted": True,
            "nonzero_physical_gauge_moment_map_obtained": True,
            "canonical_parent_selected": False,
            "horizontal_phase_mass_obtained": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_cotangent_complex_structure_metric_selector_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()