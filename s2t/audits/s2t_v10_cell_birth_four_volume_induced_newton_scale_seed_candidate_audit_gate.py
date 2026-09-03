#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (10, 6)
    assert certificate.candidate_matrix.rank() == 5
    assert certificate.pass_vector == sp.zeros(10, 1)
    assert certificate.independent_parent_anchor_vector == sp.zeros(10, 1)
    assert certificate.noncircular_orbit_breaker_vector == sp.zeros(10, 1)
    assert certificate.relative_scale_map.rank() == 4
    assert certificate.relative_scale_map * certificate.scale_vector == sp.zeros(4, 1)
    assert len(certificate.relative_scale_map.nullspace()) == 1
    assert certificate.externally_anchored_map.rank() == 5

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "candidates": [
            "growth_curvature",
            "inverse_cell_area",
            "spectral_cutoff_squared",
            "clock_wavenumber_squared",
            "KMS_thermal_wavenumber_squared",
            "Dirac_gap_squared",
            "topological_density_square_root",
            "vacuum_Hessian_gap",
            "dimensional_transmutation_squared",
            "observed_Newton_inverse_area",
        ],
        "criteria": [
            "inverse_area_dimension",
            "internally_available",
            "target_independent",
            "selected_by_common_parent",
            "typed_into_A_B",
            "breaks_scale_orbit",
        ],
        "candidate_matrix": [
            list(map(int, certificate.candidate_matrix.row(index)))
            for index in range(certificate.candidate_matrix.rows)
        ],
        "candidate_matrix_rank": 5,
        "passing_candidates": 0,
        "maximum_score": "4/6",
        "relative_scale_system": {
            "variables": ["m", "q", "E_C", "kappa", "Lambda"],
            "rank": 4,
            "nullity": 1,
            "kernel": [-2, 2, -1, -1, -2],
            "invariants": ["m*q", "m/E_C^2", "m/kappa^2", "m/Lambda"],
            "external_seed_row_rank": 5,
        },
        "route_status": {
            "dimensional_transmutation": "breaks orbit conditionally but beta function and boundary datum are not parent-derived",
            "observed_Newton_constant": "forbidden target-loaded inversion",
        },
        "status": {
            "candidate_coverage": "10/10",
            "candidate_origin": "0/10",
            "origin_ledger": "3/6",
            "scale_seed_origin": "0/1",
            "absolute_Newton_constant": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "current_corpus_selects_scale_seed": False,
            "relative_calibrations_remove_absolute_orbit": False,
            "observed_G_is_admissible_seed": False,
            "dimensional_transmutation_requires_dedicated_parent_test": True,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()