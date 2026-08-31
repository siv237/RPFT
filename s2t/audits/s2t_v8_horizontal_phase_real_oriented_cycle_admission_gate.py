#!/usr/bin/env python3
"""Точный аудит Real-ориентированного голоморфного цикла."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_real_oriented_cycle_admission_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_real_oriented_cycle_admission import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.raising_operator**2 == sp.zeros(9)
    assert certificate.reverse_operator**2 == sp.zeros(9)
    assert certificate.odd_trace_moments == sp.zeros(1, 3)
    assert certificate.even_trace_moments == sp.Matrix([[22, 110, 682]])
    assert certificate.physical_transfer_real_dimension == 40
    assert certificate.independent_reverse_real_dimension == 80
    assert certificate.independent_reverse_excess == 40
    assert not certificate.phased_real_completion.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_phase_real_oriented_cycle_admission_gate"
    )
    assert len(gate["obligations"]) == 13
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "two_layer_quiver": {
            "vertex_count": 9,
            "forward_edge_count": 11,
            "raising_rank": int(certificate.raising_operator.rank()),
            "raising_nilpotence_order": 2,
            "reverse_nilpotence_order": 2,
            "real_completion_rank": int(certificate.real_completion.rank()),
        },
        "real_structure": {
            "reverse_is_independent": False,
            "reverse_phase_weights_are_opposite": True,
            "real_completion_is_odd": True,
            "horizontal_phase_action": "similarity",
            "odd_trace_moments_1_3_5": [0, 0, 0],
            "even_trace_moments_2_4_6": [22, 110, 682],
        },
        "carrier_dimensions": {
            "transfer_complex": 20,
            "physical_real_completion_real": certificate.physical_transfer_real_dimension,
            "independent_reverse_completion_real": certificate.independent_reverse_real_dimension,
            "unjustified_new_real_directions": certificate.independent_reverse_excess,
        },
        "orientation_obstruction": {
            "formal_orientation_condition": "alpha*beta=-1",
            "positive_involution_condition": "beta=conjugate(alpha)",
            "resulting_norm_condition": "abs(alpha)^2=-1",
            "compatible": False,
        },
        "verdict": {
            "holomorphic_directed_cycle_exists": False,
            "real_completion_adds_independent_reverse_field": False,
            "real_completed_trace_detects_horizontal_phase": False,
            "real_oriented_cycle_lifts_horizontal_mode": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_complex_symplectic_polarization_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()