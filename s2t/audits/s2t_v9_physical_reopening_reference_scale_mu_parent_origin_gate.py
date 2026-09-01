#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_reference_scale_mu_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
STEM = "physical_reopening_reference_scale_mu_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v9_physical_reopening_gaussian_reference_"
        "state_parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (8, 5)
    assert certificate.candidate_matrix.rank() == 4
    assert certificate.pass_vector == sp.zeros(8, 1)
    assert certificate.relative_scale_map.rank() == 7
    assert len(certificate.relative_scale_map.nullspace()) == 1

    candidates = [
        "inverse_kms_temperature",
        "clock_energy",
        "reservoir_cutoff",
        "inverse_compactification_radius",
        "spectral_dirac_scale",
        "observed_mass",
        "vacuum_hessian_gap",
        "dimensional_transmutation",
    ]
    criteria = [
        "correct_energy_dimension",
        "internally_selected",
        "typed_map_to_gaussian_carrier",
        "breaks_common_scale_orbit",
        "target_independent",
    ]
    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "candidates": candidates,
        "criteria": criteria,
        "candidate_matrix": [list(map(int, certificate.candidate_matrix.row(index))) for index in range(8)],
        "candidate_scores": [int(sum(certificate.candidate_matrix.row(index))) for index in range(8)],
        "passing_candidates": 0,
        "candidate_matrix_rank": 4,
        "relative_scale_map": {
            "shape": [7, 8],
            "rank": 7,
            "nullity": 1,
            "kernel": "common positive rescaling of all energy candidates and mu",
        },
        "closest_candidate": {
            "name": "dimensional_transmutation",
            "score": "3/5",
            "missing": ["internally_selected", "typed_map_to_gaussian_carrier"],
        },
        "scores": {
            "candidate_origin": "0/8",
            "physical_reference_scale_origin": "0/1",
            "physical_origin_packages": "0/2",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "existing_reference_scale_mu_derived": False,
            "relative_calibrations_break_absolute_scale_orbit": False,
            "dimensional_transmutation_available_in_current_parent": False,
            "physical_program_reopened": False,
            "tome9_final_physical_no_go_ready": True,
        },
        "next_gate": "version9_final_conclusion_and_tome10_program_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()