#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_clock_energy_geometric_anchor_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate_results.json"
)


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v10_cell_birth_clock_energy_common_parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (9, 5)
    assert certificate.candidate_matrix.rank() == 5
    assert certificate.pass_vector == sp.zeros(9, 1)
    assert certificate.internal_break_vector == sp.zeros(9, 1)
    assert certificate.relative_scale_map.rank() == 3
    assert certificate.relative_scale_map.nullspace() == [sp.ones(4, 1)]
    assert certificate.externally_anchored_map.rank() == 4
    assert sum(certificate.audit_coverage) == 9
    assert sum(certificate.physical_ledger) == 0

    candidates = [
        "inverse_proper_cell_time",
        "inverse_proper_cell_length",
        "growth_curvature_or_cosmological_constant",
        "spectral_cutoff",
        "casimir_energy_from_free_radius",
        "kms_temperature",
        "planck_energy_imported_through_G",
        "observed_hubble_rate",
        "dimensionless_vacuum_action",
    ]
    criteria = [
        "correct_energy_dimension",
        "internally_available",
        "independent_of_clock_rate",
        "typed_map_to_clock_energy",
        "breaks_scale_orbit_without_external_input",
    ]
    matrix = certificate.candidate_matrix
    scores = [int(sum(matrix.row(index))) for index in range(9)]
    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "candidates": candidates,
        "criteria": criteria,
        "candidate_matrix": [
            list(map(int, matrix.row(index))) for index in range(9)
        ],
        "candidate_scores": scores,
        "candidate_matrix_rank": 5,
        "passing_candidates": 0,
        "maximum_score": "3/5",
        "internal_orbit_breakers": 0,
        "relative_calibration": {
            "variables": ["E_C", "Omega", "Gamma_B", "H_B"],
            "map_rank": 3,
            "map_nullity": 1,
            "kernel": "common rescaling of all four dimensional rates",
            "rank_after_imported_energy_anchor": 4,
        },
        "cosmological_circularity": {
            "growth_rate": "H_B=Delta_zeta*E_C/hbar",
            "growth_curvature": "Lambda_growth=3*(H_B/c)^2",
            "curvature_energy": "E_Lambda=hbar*c*sqrt(Lambda_growth/3)=Delta_zeta*E_C",
            "attempted_recovery": "E_Lambda/Delta_zeta=E_C",
            "independent_anchor": False,
        },
        "geometric_scale_orbits": {
            "proper_cell_time": "E_tau*tau_cell=hbar",
            "proper_cell_length": "E_ell*ell_cell=hbar*c",
            "casimir_radius": "24*E_Cas*R=hbar*c",
            "selected_cell_time_or_length": False,
        },
        "external_breakers": {
            "planck_energy": "would break the orbit only after importing G",
            "observed_hubble_rate": "would break the orbit as target data",
            "admissible_internal_origin": False,
        },
        "status": {
            "candidate_audit_coverage": "9/9",
            "candidate_origin": "0/9",
            "absolute_clock_energy": "0/1",
            "physical_cosmological_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "existing_geometric_clock_anchor_found": False,
            "growth_cosmological_constant_is_independent_anchor": False,
            "external_dimensional_constant_would_remove_orbit": True,
            "absolute_clock_energy_derived": False,
            "new_intrinsic_geometric_datum_required": True,
        },
        "next_gate": "version10_cell_birth_intrinsic_four_volume_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()