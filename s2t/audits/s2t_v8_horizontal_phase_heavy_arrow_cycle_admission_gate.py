#!/usr/bin/env python3
"""Точный аудит тяжёлых стрелочных циклов горизонтальной фазы."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_heavy_arrow_cycle_admission_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_heavy_arrow_cycle_admission import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.graph_rank == 8
    assert certificate.cycle_rank == 3
    assert certificate.incidence_cycle_rank == 0
    assert certificate.heavy_cycle_rank == 3
    assert certificate.boundary_matrix * certificate.cycle_basis == sp.zeros(9, 3)
    assert certificate.cycle_basis[0, :] == sp.zeros(1, 3)
    assert certificate.target_phase_weights * certificate.cycle_basis == sp.zeros(1, 3)
    assert not certificate.cycle_basis.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_phase_heavy_arrow_cycle_admission_gate"
    )
    assert len(gate["obligations"]) == 9
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "support_graph": {
            "vertex_count": 9,
            "edge_count": 11,
            "incidence_edge_count": 7,
            "heavy_edge_count": 4,
            "boundary_rank": certificate.graph_rank,
            "connected_component_count": 1,
            "cycle_rank": certificate.cycle_rank,
            "incidence_cycle_rank": certificate.incidence_cycle_rank,
            "heavy_projection_rank": certificate.heavy_cycle_rank,
        },
        "cycle_basis": [
            [int(certificate.cycle_basis[row, column]) for row in range(11)]
            for column in range(3)
        ],
        "horizontal_phase": {
            "target_edge_weights": [int(value) for value in certificate.target_phase_weights],
            "cycle_charges": [0, 0, 0],
            "up_sector_edge_index": 0,
            "up_sector_edge_cycle_coordinates": [0, 0, 0],
            "up_sector_degree": 1,
        },
        "verdict": {
            "heavy_arrows_create_cycles": True,
            "all_independent_cycles_use_heavy_arrows": True,
            "any_cycle_contains_up_sector_edge": False,
            "any_cycle_detects_horizontal_phase": False,
            "heavy_cycle_lifts_horizontal_mode": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_real_oriented_cycle_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()