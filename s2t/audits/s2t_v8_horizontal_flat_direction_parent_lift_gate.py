#!/usr/bin/env python3
"""Точный аудит происхождения горизонтальной фазовой нулевой моды."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_flat_direction_parent_lift_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_flat_direction_parent_lift import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.phase_coordinates.rank() == 2
    assert certificate.phase_metric == sp.diag(6, 20)
    assert certificate.orbit_phase_coupling == sp.Matrix([[0, 0], [0, 0], [-6, 8]])
    coefficients = sp.Matrix([4, 3])
    assert (coefficients.T * certificate.phase_metric * coefficients)[0] == 276
    assert not certificate.phase_coordinates.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_flat_direction_parent_lift_gate"
    )
    assert len(gate["obligations"]) == 10
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "phase_plane": {
            "dimension": 2,
            "metric": "diag(6,20)",
            "orbit_coupling": [[0, 0], [0, 0], [-6, 8]],
            "horizontal_coefficients": [4, 3],
            "horizontal_norm_squared": 276,
        },
        "all_order_invariance": {
            "phase_action": "diag(z^4 I_3,z^3 I_7) A0",
            "left_gram_invariant": True,
            "right_gram_invariant": True,
            "gram_trace_word_parent_can_lift": False,
        },
        "determinant_line_boundary": {
            "transfer_shape": [10, 11],
            "rank": 10,
            "maximal_minor_carrier_dimension": 11,
            "ordinary_scalar_determinant_exists": False,
            "extra_contraction_or_orientation_required": True,
        },
        "verdict": {
            "horizontal_flat_mode_origin_identified": True,
            "existing_gram_parent_lifts_mode": False,
            "new_free_mass_term_admitted": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_determinant_line_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()